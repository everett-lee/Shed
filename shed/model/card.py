from abc import ABC
from enum import Enum, StrEnum
from typing import Optional, List
import random


class Suit(str, StrEnum):
    HEARTS = "hearts"
    CLUBS = "clubs"
    SPADES = "spades"
    DIAMONDS = "diamonds"


class Value:
    def __init__(self, value: int, display_value: Optional[str]):
        self.value = value
        self.display_value = display_value if display_value else str(value)


class Card:
    def __init__(self, value: Value):
        self.value = value

    def get_value(self) -> Value:
        return self.value


class PlayingCard(Card):
    def __init__(self, suit: Suit, value: Value):
        super().__init__(value)
        self.suit = suit

    def get_suit(self) -> Suit:
        return self.suit


class Deck:
    def __int__(self, cards: List[Card]):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def peek(self, n_from_top: int=0) -> Card:
        self._check_index_valid(n_from_top)
        return self.cards[n_from_top]

    def take(self, n_from_top:int =0) -> Card:
        self._check_index_valid(n_from_top)
        return self.cards.pop(n_from_top)

    def _check_index_valid(self, i: int):
        deck_size = len(self.cards)
        if i >= deck_size:
            raise ValueError(f"Only {deck_size} in deck!")

