"""Blackjack game logic components."""
from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field
from threading import Lock
from typing import Dict, List, Optional

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = [
    "Ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
]


@dataclass(frozen=True)
class Card:
    """Represents a card in a standard deck of 52 cards."""

    suit: str
    rank: str

    @property
    def value(self) -> int:
        if self.rank in {"Jack", "Queen", "King"}:
            return 10
        if self.rank == "Ace":
            return 11
        return int(self.rank)

    def to_dict(self) -> Dict[str, str]:
        return {"suit": self.suit, "rank": self.rank}


class Deck:
    """Represents a shuffled deck of 52 unique cards."""

    def __init__(self) -> None:
        self.cards: List[Card] = [Card(suit=suit, rank=rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise ValueError("The deck is empty. Cannot draw more cards.")
        return self.cards.pop()


@dataclass
class Hand:
    """Represents a Blackjack hand."""

    cards: List[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def value(self) -> int:
        total = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "Ace")
        # Adjust Ace value from 11 to 1 if total busts
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value == 21

    def to_dict(self) -> Dict[str, List[Dict[str, str]]]:
        return {
            "cards": [card.to_dict() for card in self.cards],
            "value": self.value,
        }


class GameSession:
    """Manages the lifecycle of a Blackjack game."""

    def __init__(self, bet: int = 0, owner_id: Optional[int] = None) -> None:
        self.session_id: str = uuid.uuid4().hex
        self.bet = bet
        self.owner_id = owner_id
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.is_over = False
        self.outcome: Optional[str] = None
        self.is_settled = False
        self.initial_deal()

    def initial_deal(self) -> None:
        for _ in range(2):
            self.player_hand.add_card(self.deck.draw())
            self.dealer_hand.add_card(self.deck.draw())
        self._evaluate_naturals()

    def _evaluate_naturals(self) -> None:
        if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            self.is_over = True
            self.outcome = "push"
        elif self.player_hand.is_blackjack():
            self.is_over = True
            self.outcome = "player_blackjack"
        elif self.dealer_hand.is_blackjack():
            self.is_over = True
            self.outcome = "dealer_blackjack"

    def player_hit(self) -> None:
        if self.is_over:
            return
        self.player_hand.add_card(self.deck.draw())
        if self.player_hand.value > 21:
            self.is_over = True
            self.outcome = "player_bust"

    def player_stand(self) -> None:
        if self.is_over:
            return
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.draw())
        self.is_over = True
        self.outcome = self._determine_winner()

    def _determine_winner(self) -> str:
        player_total = self.player_hand.value
        dealer_total = self.dealer_hand.value
        if dealer_total > 21:
            return "dealer_bust"
        if player_total > dealer_total:
            return "player_win"
        if player_total < dealer_total:
            return "dealer_win"
        return "push"

    def serialize(self) -> Dict[str, object]:
        return {
            "session_id": self.session_id,
            "player_hand": self.player_hand.to_dict(),
            "dealer_hand": {
                "cards": [card.to_dict() for card in self.dealer_hand.cards],
                "value": self.dealer_hand.value,
            },
            "is_over": self.is_over,
            "outcome": self.outcome,
            "bet": self.bet,
            "owner_id": self.owner_id,
            "is_settled": self.is_settled,
        }


class SessionManager:
    """Stores active game sessions in memory."""

    def __init__(self) -> None:
        self._sessions: Dict[str, GameSession] = {}
        self._lock = Lock()

    def create_session(self, bet: int = 0, owner_id: Optional[int] = None) -> GameSession:
        session = GameSession(bet=bet, owner_id=owner_id)
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[GameSession]:
        with self._lock:
            return self._sessions.get(session_id)

    def remove_session(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)


session_manager = SessionManager()
