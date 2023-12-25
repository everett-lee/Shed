from typing import List

import numpy as np

from shed.game.card import ShedCard
from shed.game.round import ShedAction


class ShedPlayer:
    action_to_rank = {
        ShedAction.Ace: "A",
        ShedAction.Two: "2",
        ShedAction.Three: "3",
        ShedAction.Four: "4",
        ShedAction.Five: "5",
        ShedAction.Six: "6",
        ShedAction.Seven: "7",
        ShedAction.Eight: "8",
        ShedAction.Nine: "9",
        ShedAction.Ten: "T",
        ShedAction.Jack: "J",
        ShedAction.Queen: "Q",
        ShedAction.King: "K",
    }

    def __init__(self, player_id: int, np_random: np.random) -> None:
        """Initialize a player class"""
        self.np_random = np_random
        self.player_id = player_id
        self.hand: List[ShedCard] = []
        self.score = 0

    def get_player_id(self) -> int:
        """Return player's id"""
        return self.player_id

    def take_cards(self, cards: List[ShedCard]) -> None:
        self.hand += cards

    def play_card(self, action: ShedAction) -> ShedCard:
        card_arr = [
            card for card in self.hand if card.rank == self.action_to_rank[action]
        ]
        if not card_arr:
            raise Exception(f"{action} not present in the hand")
        card = card_arr[0]
        self.hand.remove(card)
        return card
