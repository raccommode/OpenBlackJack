"""FastAPI application exposing the Blackjack API."""
from __future__ import annotations

import sqlite3
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status

from . import db
from .auth import authenticate, generate_token, hash_password, verify_password
from .blackjack import GameSession, session_manager
from .schemas import (
    GameActionRequest,
    GameStartRequest,
    GameStateResponse,
    LoginRequest,
    SignupRequest,
    TokenResponse,
)
from .frontend import router as frontend_router

app = FastAPI(title="OpenBlackJack", description="Single-player Blackjack API")
app.include_router(frontend_router)


def optional_user(authorization: Optional[str] = Header(default=None)) -> Optional[sqlite3.Row]:
    if not authorization:
        return None
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format.")
    token = authorization.split()[1]
    user = authenticate(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
    return user


def require_user(user: Optional[sqlite3.Row] = Depends(optional_user)) -> sqlite3.Row:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")
    return user


def ensure_owner(session: GameSession, user: Optional[sqlite3.Row]) -> None:
    if session.owner_id and (user is None or session.owner_id != user["id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Session does not belong to you.")


def settle_session(session: GameSession) -> Optional[int]:
    if not session.owner_id or not session.is_over or session.is_settled:
        return None
    user = db.get_user_by_id(session.owner_id)
    if user is None:
        session.is_settled = True
        return None
    balance = user["balance"]
    bet = session.bet
    payout = 0
    if session.outcome in {"player_win", "dealer_bust"}:
        payout = bet * 2
    elif session.outcome == "player_blackjack":
        payout = int(bet * 2.5)
    elif session.outcome == "push":
        payout = bet
    # Loss scenarios keep payout at 0
    new_balance = balance + payout
    db.update_user_balance(session.owner_id, new_balance)
    session.is_settled = True
    return new_balance


def serialize_session(session: GameSession, balance: Optional[int]) -> GameStateResponse:
    data = session.serialize()
    return GameStateResponse(
        session_id=data["session_id"],
        player_hand=data["player_hand"],
        dealer_hand=data["dealer_hand"],
        is_over=data["is_over"],
        outcome=data["outcome"],
        bet=data["bet"],
        balance=balance,
    )


@app.on_event("startup")
def on_startup() -> None:
    db.init_db()
    db.start_backup_thread()


@app.on_event("shutdown")
def on_shutdown() -> None:
    db.stop_backup_thread()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest) -> TokenResponse:
    existing = db.get_user_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists.")
    password_hash = hash_password(payload.password)
    user_id = db.create_user(payload.username, password_hash)
    token = generate_token(user_id)
    return TokenResponse(token=token)


@app.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    user = db.get_user_by_username(payload.username)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    token = generate_token(user["id"])
    return TokenResponse(token=token)


@app.get("/me")
def current_user(user: sqlite3.Row = Depends(require_user)) -> dict:
    return {
        "id": user["id"],
        "username": user["username"],
        "balance": user["balance"],
        "created_at": user["created_at"],
    }


@app.post("/game/start", response_model=GameStateResponse)
def start_game(
    payload: GameStartRequest,
    user: Optional[sqlite3.Row] = Depends(optional_user),
) -> GameStateResponse:
    bet = payload.bet or 0
    balance: Optional[int] = None
    owner_id: Optional[int] = None

    if user:
        owner_id = user["id"]
        current_balance = user["balance"]
        if bet > current_balance:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bet exceeds available balance.")
        if bet > 0:
            db.update_user_balance(owner_id, current_balance - bet)
            balance = current_balance - bet
        else:
            balance = current_balance
    else:
        if bet:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guests cannot place bets.")

    session = session_manager.create_session(bet=bet if owner_id else 0, owner_id=owner_id)

    if session.is_over:
        balance = settle_session(session) or balance
        if owner_id and balance is None:
            refreshed = db.get_user_by_id(owner_id)
            balance = refreshed["balance"] if refreshed else None

    return serialize_session(session, balance)


@app.post("/game/hit", response_model=GameStateResponse)
def hit(
    payload: GameActionRequest,
    user: Optional[sqlite3.Row] = Depends(optional_user),
) -> GameStateResponse:
    session = session_manager.get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    ensure_owner(session, user)

    session.player_hit()

    balance = None
    if session.is_over:
        balance = settle_session(session)
        if session.owner_id and balance is None:
            refreshed = db.get_user_by_id(session.owner_id)
            balance = refreshed["balance"] if refreshed else None

    return serialize_session(session, balance)


@app.post("/game/stand", response_model=GameStateResponse)
def stand(
    payload: GameActionRequest,
    user: Optional[sqlite3.Row] = Depends(optional_user),
) -> GameStateResponse:
    session = session_manager.get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    ensure_owner(session, user)

    session.player_stand()

    balance = None
    if session.is_over:
        balance = settle_session(session)
        if session.owner_id and balance is None:
            refreshed = db.get_user_by_id(session.owner_id)
            balance = refreshed["balance"] if refreshed else None

    return serialize_session(session, balance)


@app.get("/game/{session_id}", response_model=GameStateResponse)
def get_state(
    session_id: str,
    user: Optional[sqlite3.Row] = Depends(optional_user),
) -> GameStateResponse:
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    ensure_owner(session, user)

    balance = None
    if session.owner_id:
        record = db.get_user_by_id(session.owner_id)
        balance = record["balance"] if record else None
    return serialize_session(session, balance)
