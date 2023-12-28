from typing import Any, Dict, List, Optional

import numpy as np
from rlcard.games.base import Card

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
        self.min_hand_size = 5

    def handle_action(self, player: ShedPlayer, action: ShedAction) -> bool:
        if action == ShedAction.Pickup:
            player.take_cards(self.active_deck)
            self.active_deck = []

        else:
            card = player.play_card(action)
            ten_played = self.play_card(card)
            if len(player.hand) < self.min_hand_size:
                self.dealer.deal_card(player)
            return ten_played

    def _remove_threes(self, cards: List[ShedCard]) -> List[ShedCard]:
        return [c for c in cards if c.rank != "3"]

    def is_legal_card(self, card: ShedCard) -> bool:
        card = ShedCard(card.suit, card.rank)
        threes_removed = self._remove_threes(self.active_deck)

        if not threes_removed or card.is_magic_card():
            return True
        else:
            top_card = threes_removed[-1]

        top_card = ShedCard(top_card.suit, top_card.rank)

        if top_card.is_ace():
            return card.is_magic_card()

        if top_card.is_seven():
            return card <= top_card

        return card >= top_card

    def play_card(self, card: ShedCard) -> bool:
        card = ShedCard(card.suit, card.rank)

        if card.is_ten():
            # Ten burns the deck
            self.active_deck = []
            return True

        elif self.is_legal_card(card) and not card.is_ten():
            self.active_deck.append(card)
            return False

        else:
            raise ValueError(f"Card {card} is not a valid option")

    def proceed_round(self, players: List[ShedPlayer], action: ShedAction) -> int:
        """Call other Classes' functions to keep one round running"""
        player = players[self.game_pointer]
        ten_played = self.handle_action(player, action)

        if not player.hand:
            self.is_over = True
            self.winner = player

        # When 10 played / deck burned player goes again
        if not ten_played:
            self.game_pointer = (self.game_pointer + 1) % self.num_players

        return self.game_pointer

    # TODO handle no legal actions leaves you with pickup
    def get_legal_actions(self, player: ShedPlayer) -> List[ShedAction]:
        typed_cards = [ShedCard(card.suit, card.rank) for card in player.hand]
        playable_cards = [card for card in typed_cards if self.is_legal_card(card)]

        full_actions = [self.rank_to_action[card.rank] for card in playable_cards]
        can_pickup = len(self.active_deck) > 0
        if can_pickup:
            full_actions = full_actions + [ShedAction.Pickup]
        unique_actions = list(set(full_actions))

        return unique_actions

    def is_over(self) -> bool:
        """Check if the game is over"""

        for player in self.players:
            if not player.hand:
                return True

        return False

    def get_top_card(self) -> Optional[Card]:
        no_threes = self._remove_threes(self.active_deck)
        return no_threes[-1] if len(no_threes) else None

    def get_state(self, players: List[ShedPlayer], game_pointer: int) -> Dict[str, Any]:
        """Get player's state"""
        state = {}
        active_player = players[game_pointer]
        state["hand"] = active_player.hand
        state["played_cards"] = self.active_deck
        state["legal_actions"] = self.get_legal_actions(active_player)
        state["other_hands"] = []
        for player in players:
            if player.player_id != active_player.player_id:
                state["num_cards"].append(player.hand)
        return state

    def get_active_deck_size(self) -> int:
        return len(self.active_deck)
