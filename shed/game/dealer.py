import numpy as np
from rlcard.utils import init_standard_deck

from shed.game.player import ShedPlayer


class ShedDealer:
    def __init__(self, np_random: np.random):
        """Initialize a Shed dealer class"""
        self.np_random = np_random
        self.unplayed_deck = init_standard_deck()
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the deck"""
        shuffle_deck = np.array(self.unplayed_deck)
        self.np_random.shuffle(shuffle_deck)
        self.unplayed_deck = list(shuffle_deck)

    def deal_card(self, player: ShedPlayer) -> None:
        """Distribute one card to the player"""
        if len(self.unplayed_deck):
            player.hand.append(self.unplayed_deck.pop())

    def get_unplayed_deck_size(self) -> int:
        return len(self.unplayed_deck)