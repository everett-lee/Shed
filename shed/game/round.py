from enum import StrEnum
from typing import List, Any, Dict

from shed.game.card import ShedCard
from shed.game.dealer import ShedDealer
import numpy as np

from shed.game.player import ShedPlayer


class ShedAction(StrEnum):
    Ace = "Ace"
    Two = "Two"
    Three = "Three"
    Four = "Four"
    Five = "Five"
    Six = "Six"
    Seven = "Seven"
    Eight = "Eight"
    Nine = "Nine"
    Ten = "Ten"
    Jack = "Jack"
    Queen = "Queen"
    King = "King"
    Pickup = "Pickup"


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
        self.lower_than_active = False
        self.see_through_active = False

    def handle_action(self, player: ShedPlayer, action: ShedAction):
        if action == ShedAction.Pickup:
            player.take_cards(self.active_deck)
            self.active_deck = []

        else:
            card = player.play_card(action)
            self.play_card(card)
            self.active_deck.append(card)
            self.dealer.deal_card(player)

    def can_beat_ace(self, card: ShedCard) -> bool:
        return card.suit in ["A", "3", "7"]

    def is_legal_card(self, card: ShedCard) -> bool:
        if not self.active_deck or card.suit == "A":
            return True

        if self.see_through_active:
            # No cards below the 3
            if len(self.active_deck) <= 1:
                return True
            top_card = self.active_deck[-2]
        else:
            top_card = self.active_deck[-1]

        if top_card.suit == "A":
            return self.can_beat_ace(card)

        if self.lower_than_active:
            return card <= top_card

        return card >= top_card

    def play_card(self, card: ShedCard):
        if card.rank == "3":
            self.see_through_active = True
        elif card.rank == "7":
            self.lower_than_active = True
        elif card.rank == "T":
            # Ten burns the deck
            self.active_deck = []
        elif self.is_legal_card(card):
            self.active_deck.append(card)
        else:
            raise ValueError(f"Card {card} is not a valid option")

        self.see_through_active = False
        self.lower_than_active = False

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
        playable_cards = [card for card in player.hand if self.is_legal_card(card)]
        return [self.rank_to_action[card.rank] for card in playable_cards] + [
            ShedAction.Pickup
        ]

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
