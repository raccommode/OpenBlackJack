"""Pydantic schemas for request and response payloads."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, validator


class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6, max_length=128)

    @validator("username")
    def username_is_alphanumeric(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Username must be alphanumeric.")
        return value


class LoginRequest(BaseModel):
    username: str
    password: str


class GameStartRequest(BaseModel):
    bet: Optional[int] = Field(default=0, ge=0)


class GameActionRequest(BaseModel):
    session_id: str


class TokenResponse(BaseModel):
    token: str


class GameStateResponse(BaseModel):
    session_id: str
    player_hand: dict
    dealer_hand: dict
    is_over: bool
    outcome: Optional[str]
    bet: int
    balance: Optional[int]
