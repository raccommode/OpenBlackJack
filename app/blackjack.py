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


NUMBER_OF_DECKS = 8


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
    """Represents a shuffled shoe of standard 52-card decks."""

    def __init__(self, number_of_decks: int = NUMBER_OF_DECKS) -> None:
        self.cards: List[Card] = [
            Card(suit=suit, rank=rank)
            for _ in range(number_of_decks)
            for suit in SUITS
            for rank in RANKS
        ]
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


@dataclass
class PlayerHandState:
    """Tracks the state of a player's individual hand."""

    hand: Hand = field(default_factory=Hand)
    bet: int = 0
    is_doubled: bool = False
    has_stood: bool = False
    outcome: Optional[str] = None

    def to_dict(
        self,
        *,
        is_active: bool,
        can_split: bool,
        can_double: bool,
    ) -> Dict[str, object]:
        return {
            "cards": [card.to_dict() for card in self.hand.cards],
            "value": self.hand.value,
            "bet": self.bet,
            "is_active": is_active,
            "can_split": can_split,
            "can_double": can_double,
            "is_doubled": self.is_doubled,
            "result": self.outcome,
        }


SIDE_BET_DEFINITIONS: Dict[str, Dict[str, object]] = {
    "pair": {
        "label": "Paire",
        "payout_multiplier": 12,  # 11:1 including the original stake
        "evaluator": lambda cards, dealer_up: len(cards) == 2 and cards[0].rank == cards[1].rank,
        "win_message": "Paire !",
        "lose_message": "Pas de paire.",
    },
    "suited_pair": {
        "label": "Paire assortie",
        "payout_multiplier": 26,  # 25:1 including the stake
        "evaluator": lambda cards, dealer_up: (
            len(cards) == 2
            and cards[0].rank == cards[1].rank
            and cards[0].suit == cards[1].suit
        ),
        "win_message": "Paire assortie !",
        "lose_message": "Paire non assortie.",
    },
}


class GameSession:
    """Manages the lifecycle of an advanced Blackjack game."""

    def __init__(
        self,
        bet: int = 0,
        owner_id: Optional[int] = None,
        side_bets: Optional[Dict[str, int]] = None,
    ) -> None:
        self.session_id: str = uuid.uuid4().hex
        self.owner_id = owner_id
        self.deck = Deck()
        self.dealer_hand = Hand()
        self.player_hands: List[PlayerHandState] = [PlayerHandState(bet=bet)]
        self.active_hand_index: Optional[int] = 0
        self.is_over = False
        self.outcome: Optional[str] = None
        self.is_settled = False
        self.side_bets: Dict[str, int] = {
            key: max(0, int(value)) for key, value in (side_bets or {}).items()
        }
        self.side_bet_results: Dict[str, Dict[str, object]] = {}
        self.initial_deal()

    @property
    def bet(self) -> int:
        return sum(hand.bet for hand in self.player_hands)

    def initial_deal(self) -> None:
        for _ in range(2):
            self.player_hands[0].hand.add_card(self.deck.draw())
            self.dealer_hand.add_card(self.deck.draw())
        self._resolve_side_bets()
        self._evaluate_naturals()

    def _resolve_side_bets(self) -> None:
        cards = self.player_hands[0].hand.cards[:2]
        dealer_up = self.dealer_hand.cards[0] if self.dealer_hand.cards else None
        all_keys = set(self.side_bets.keys()) | set(SIDE_BET_DEFINITIONS.keys())
        for key in sorted(all_keys):
            definition = SIDE_BET_DEFINITIONS.get(key)
            amount = self.side_bets.get(key, 0)
            result = {
                "bet": amount,
                "payout": 0,
                "result": "inactive" if amount <= 0 else "pending",
                "description": "",
                "label": definition["label"] if definition else key,
            }
            if not definition or amount <= 0 or len(cards) < 2:
                if amount > 0:
                    result["result"] = "loss"
                    result["description"] = (
                        definition["lose_message"] if definition else "Mise perdue."
                    )
                else:
                    result["result"] = "inactive"
                    result["description"] = definition["lose_message"] if definition else ""
                self.side_bet_results[key] = result
                continue
            evaluator = definition["evaluator"]
            win = evaluator(cards, dealer_up)
            if win:
                multiplier = definition["payout_multiplier"]
                result["payout"] = amount * multiplier
                result["result"] = "win"
                result["description"] = definition["win_message"]
            else:
                result["result"] = "loss"
                result["description"] = definition["lose_message"]
            self.side_bet_results[key] = result

    def _evaluate_naturals(self) -> None:
        player_blackjack = self.player_hands[0].hand.is_blackjack()
        dealer_blackjack = self.dealer_hand.is_blackjack()
        if player_blackjack and dealer_blackjack:
            self.player_hands[0].outcome = "push"
            self.outcome = "push"
            self.is_over = True
            self.active_hand_index = None
        elif player_blackjack:
            self.player_hands[0].outcome = "player_blackjack"
            self.outcome = "player_blackjack"
            self.is_over = True
            self.active_hand_index = None
        elif dealer_blackjack:
            for hand in self.player_hands:
                hand.outcome = "dealer_blackjack"
            self.outcome = "dealer_blackjack"
            self.is_over = True
            self.active_hand_index = None

    def can_split_hand(self, hand_index: int) -> bool:
        if self.is_over or not (0 <= hand_index < len(self.player_hands)):
            return False
        if len(self.player_hands) >= 4:
            return False
        hand_state = self.player_hands[hand_index]
        if hand_state.outcome or hand_state.has_stood:
            return False
        cards = hand_state.hand.cards
        return len(cards) == 2 and cards[0].rank == cards[1].rank

    def can_double_hand(self, hand_index: int) -> bool:
        if self.is_over or not (0 <= hand_index < len(self.player_hands)):
            return False
        hand_state = self.player_hands[hand_index]
        if hand_state.outcome or hand_state.has_stood or hand_state.is_doubled:
            return False
        return len(hand_state.hand.cards) == 2

    def double_cost(self, hand_index: Optional[int] = None) -> int:
        index = self._resolve_hand_index(hand_index)
        if index is None or not self.can_double_hand(index):
            return 0
        return self.player_hands[index].bet

    def split_cost(self, hand_index: Optional[int] = None) -> int:
        index = self._resolve_hand_index(hand_index)
        if index is None or not self.can_split_hand(index):
            return 0
        return self.player_hands[index].bet

    def _resolve_hand_index(self, hand_index: Optional[int]) -> Optional[int]:
        if hand_index is not None:
            return hand_index if 0 <= hand_index < len(self.player_hands) else None
        return self.active_hand_index

    def player_hit(self, hand_index: Optional[int] = None) -> None:
        if self.is_over:
            return
        index = self._resolve_hand_index(hand_index)
        if index is None:
            return
        state = self.player_hands[index]
        if state.outcome or state.has_stood:
            return
        state.hand.add_card(self.deck.draw())
        value = state.hand.value
        if value > 21:
            state.outcome = "player_bust"
            self._advance_hand(index)
        elif value == 21:
            state.has_stood = True
            self._advance_hand(index)

    def player_stand(self, hand_index: Optional[int] = None) -> None:
        if self.is_over:
            return
        index = self._resolve_hand_index(hand_index)
        if index is None:
            return
        state = self.player_hands[index]
        if state.outcome or state.has_stood:
            return
        state.has_stood = True
        self._advance_hand(index)

    def player_double(self, hand_index: Optional[int] = None) -> bool:
        if self.is_over:
            return False
        index = self._resolve_hand_index(hand_index)
        if index is None or not self.can_double_hand(index):
            return False
        state = self.player_hands[index]
        original_bet = state.bet
        state.bet += original_bet
        state.is_doubled = True
        state.hand.add_card(self.deck.draw())
        state.has_stood = True
        if state.hand.value > 21:
            state.outcome = "player_bust"
        self._advance_hand(index)
        return True

    def player_split(self, hand_index: Optional[int] = None) -> bool:
        if self.is_over:
            return False
        index = self._resolve_hand_index(hand_index)
        if index is None or not self.can_split_hand(index):
            return False
        state = self.player_hands[index]
        if len(state.hand.cards) != 2:
            return False
        first_card, second_card = state.hand.cards
        state.hand = Hand(cards=[first_card])
        new_state = PlayerHandState(bet=state.bet)
        new_state.hand.add_card(second_card)
        state.hand.add_card(self.deck.draw())
        new_state.hand.add_card(self.deck.draw())
        self.player_hands.insert(index + 1, new_state)
        if self.active_hand_index is not None and index < self.active_hand_index:
            self.active_hand_index += 1
        return True

    def _advance_hand(self, current_index: int) -> None:
        next_index = current_index + 1
        while next_index < len(self.player_hands):
            candidate = self.player_hands[next_index]
            if not candidate.outcome and not candidate.has_stood:
                self.active_hand_index = next_index
                return
            next_index += 1
        # No playable hand remains
        self.active_hand_index = None
        self._complete_round()

    def _complete_round(self) -> None:
        if self.is_over:
            return
        if all(hand.outcome in {"player_bust", "dealer_blackjack"} for hand in self.player_hands):
            self.is_over = True
            self.outcome = self._aggregate_outcome()
            return
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.draw())
        dealer_total = self.dealer_hand.value
        dealer_bust = dealer_total > 21
        for hand_state in self.player_hands:
            if hand_state.outcome:
                continue
            player_total = hand_state.hand.value
            if dealer_bust:
                hand_state.outcome = "dealer_bust"
            elif player_total > dealer_total:
                hand_state.outcome = "player_win"
            elif player_total < dealer_total:
                hand_state.outcome = "dealer_win"
            else:
                hand_state.outcome = "push"
        self.is_over = True
        self.outcome = self._aggregate_outcome()

    def _aggregate_outcome(self) -> str:
        outcomes = {hand.outcome for hand in self.player_hands if hand.outcome}
        if outcomes == {"push"}:
            return "push"
        if outcomes <= {"player_win", "dealer_bust", "player_blackjack"}:
            return "player_win"
        if outcomes <= {"dealer_win", "dealer_blackjack", "player_bust"}:
            return "dealer_win"
        return "mixed"

    def serialize(self) -> Dict[str, object]:
        return {
            "session_id": self.session_id,
            "player_hands": [
                state.to_dict(
                    is_active=(
                        self.active_hand_index == index and not self.is_over
                    ),
                    can_split=self.can_split_hand(index),
                    can_double=self.can_double_hand(index),
                )
                for index, state in enumerate(self.player_hands)
            ],
            "dealer_hand": {
                "cards": [card.to_dict() for card in self.dealer_hand.cards],
                "value": self.dealer_hand.value,
            },
            "is_over": self.is_over,
            "outcome": self.outcome,
            "bet": self.bet,
            "owner_id": self.owner_id,
            "is_settled": self.is_settled,
            "active_hand_index": self.active_hand_index,
            "side_bets": self.side_bet_results,
        }


class SessionManager:
    """Stores active game sessions in memory."""

    def __init__(self) -> None:
        self._sessions: Dict[str, GameSession] = {}
        self._lock = Lock()

    def create_session(
        self,
        bet: int = 0,
        owner_id: Optional[int] = None,
        side_bets: Optional[Dict[str, int]] = None,
    ) -> GameSession:
        session = GameSession(bet=bet, owner_id=owner_id, side_bets=side_bets)
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
