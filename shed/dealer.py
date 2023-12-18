from typing import List

from rlcard.utils import init_standard_deck
import numpy as np

from shed.card import ShedCard
from shed.player import ShedPlayer


class ShedDealer:
    def __init__(self, np_random: np.random):
        """Initialize a Shed dealer class"""
        self.np_random = np_random
        self.num_decks = 1
        self.unplayed_deck = init_standard_deck()
        self.live_deck = []
        self.shuffle()
        self.lower_than_active = False
        self.see_through_active = False

    def shuffle(self) -> None:
        """Shuffle the deck"""
        shuffle_deck = np.array(self.unplayed_deck)
        self.np_random.shuffle(shuffle_deck)
        self.unplayed_deck = list(shuffle_deck)

    def deal_card(self, player: ShedPlayer) -> None:
        """Distribute one card to the player
        """
        idx = self.np_random.choice(len(self.unplayed_deck))
        card = self.unplayed_deck[idx]
        self.unplayed_deck.pop(idx)
        player.hand.append(card)


    def can_beat_ace(self, card: ShedCard) -> bool:
        return card.suit in ["A", "3", "7"]
    def is_legal_card(self, card: ShedCard) -> bool:
        if not self.live_deck or card.suit == "A":
            return True

        if self.see_through_active:
            # No cards below the 3
            if len(self.live_deck) <= 1:
                return True
            top_card = self.live_deck[-2]
        else:
            top_card = self.live_deck[-1]

        if top_card.suit == "A":
            return self.can_beat_ace(card)

        if self.lower_than_active:
            return card <= top_card

        return card >= top_card

    def receive_card(self, card: ShedCard):
        if card.rank == "3":
            self.see_through_active = True
        elif card.rank == "7":
            self.lower_than_active = True
        elif card.rank == "T":
            # Ten burns the deck
            self.live_deck = []
        elif self.is_legal_card(card):
            self.live_deck.append(card)
        else:
            raise ValueError(f"Card {card} is not a valid option")

        self.see_through_active = False
        self.lower_than_active = False

