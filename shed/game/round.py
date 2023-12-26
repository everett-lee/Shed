from enum import StrEnum
from typing import Any, Dict, List

import numpy as np

from shed.game.card import ShedCard
from shed.game.dealer import ShedDealer
from shed.game.player import ShedPlayer
from shed.game.utils import ShedAction


class ShedRound:
    rank_to_action = {
        "A": ShedAction.Ace,
        "2": ShedAction.Two,
        "3": ShedAction.Three,
        "4": ShedAction.Four,
        "5": ShedAction.Five,
        "6": ShedAction.Six,
        "7": ShedAction.Seven,
        "8": ShedAction.Eight,
        "9": ShedAction.Nine,
        "T": ShedAction.Ten,
        "J": ShedAction.Jack,
        "Q": ShedAction.Queen,
        "K": ShedAction.King,
    }

    def __init__(
        self, dealer: ShedDealer, players: List[ShedPlayer], np_random: np.random
    ):
        """Initialize the round class

        Args:
            dealer (object): the object of shedDealer
            num_players (int): the number of players in game
        """
        self.np_random = np_random
        self.dealer = dealer
        self.game_pointer = 0
        self.players = players
        self.num_players = len(players)
        self.direction = 1
        self.active_deck = []
        self.is_over = False
        self.winner = None

    def handle_action(self, player: ShedPlayer, action: ShedAction):
        if action == ShedAction.Pickup:
            player.take_cards(self.active_deck)
            self.active_deck = []

        else:
            card = player.play_card(action)
            self.play_card(card)
            self.dealer.deal_card(player)

    def is_legal_card(self, card: ShedCard) -> bool:
        card = ShedCard(card.suit, card.rank)
        threes_removed = [c for c in self.active_deck if c.rank != "3"]

        if not threes_removed or card.is_magic_card():
            print("^"*100)
            print("DEALING WITH MAGIC OR EMPTY")
            print("^"*100)
            return True
        else:
            top_card = threes_removed[-1]

        top_card = ShedCard(top_card.suit, top_card.rank)

        if top_card.is_ace():
            return card.is_magic_card()

        if top_card.is_seven():
            print("%"*100)
            print("DEALING WITH SEVEN")
            print(f"COMPARING {card.rank} with TOP CARD {top_card.rank}")
            print(f"RESULT {card <= top_card}")
            return card <= top_card

        return card >= top_card

    def play_card(self, card: ShedCard):
        card = ShedCard(card.suit, card.rank)

        if card.is_ten():
            # Ten burns the deck
            self.active_deck = []

        elif self.is_legal_card(card) and not card.is_ten():
            self.active_deck.append(card)
        else:
            raise ValueError(f"Card {card} is not a valid option")

    def proceed_round(self, players: List[ShedPlayer], action: ShedAction) -> int:
        """Call other Classes" functions to keep one round running"""
        player = players[self.game_pointer]
        self.handle_action(player, action)

        if not player.hand:
            self.is_over = True
            self.winner = player

        self.game_pointer = (self.game_pointer + 1) % self.num_players

        return self.game_pointer

    # TODO handle no legal actions leaves you with pickup
    def get_legal_actions(self, player: ShedPlayer) -> List[ShedAction]:
        print(f"EXAMINING HAND {[c.rank for c in player.hand]}")
        typed_cards = [ShedCard(card.suit, card.rank) for card in player.hand]
        print(f"AND TYPED {[c.rank for c in player.hand]}")
        playable_cards = [card for card in typed_cards if self.is_legal_card(card)]
        print(f"AFTER: {[c.rank for c in playable_cards]}")
        full_actions = [self.rank_to_action[card.rank] for card in playable_cards] + [
            ShedAction.Pickup
        ]
        unique_actions = list(set(full_actions))
        print("*"*100)
        print("FULL AND UNIQUE ACTIONS")
        print(sorted((full_actions)))
        print(sorted((unique_actions)))
        print("*"*100)
        return unique_actions

    def is_over(self) -> bool:
        """Check if the game is over"""

        for player in self.players:
            if not player.hand:
                return True

        return False

    def get_state(self, players: List[ShedPlayer], game_pointer: int) -> Dict[str, Any]:
        """Get player"s state"""
        state = {}
        player = players[game_pointer]
        state["hand"] = player.hand
        state["played_cards"] = self.active_deck
        state["legal_actions"] = self.get_legal_actions(player)
        state["num_cards"] = []
        for player in players:
            state["num_cards"].append(len(player.hand))
        return state

    def get_active_deck_size(self) -> int:
        return len(self.active_deck)
