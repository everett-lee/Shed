from typing import Any, Dict, List, Optional, Tuple

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
        """Initialize the round class"""
        self.np_random = np_random
        self.dealer = dealer
        self.game_pointer = 0
        self.players = players
        self.num_players = len(players)
        self.active_deck = []
        self.is_over = False
        self.winner = None
        self.min_hand_size = 5

    def proceed_round(self, players: List[ShedPlayer], action: ShedAction) -> int:
        """Call other Classes' functions to keep one round running"""
        player = players[self.game_pointer]
        deck_burned = self.handle_action(player, action)

        if not player.hand:
            self.is_over = True
            self.winner = player

        # When deck burned player goes again
        if not deck_burned:
            self.game_pointer = (self.game_pointer + 1) % self.num_players

        return self.game_pointer

    def handle_action(self, player: ShedPlayer, action: ShedAction) -> bool:
        """Play a card according to the action. Return true if burn action taken"""

        if action == ShedAction.Pickup:
            player.take_cards(self.active_deck)
            self.active_deck = []
            return False

        else:
            card = player.play_card(action)
            deck_burned = self.play_card(card)
            if len(player.hand) < self.min_hand_size:
                self.dealer.deal_card(player)
            return deck_burned

    def _remove_threes(self, cards: List[ShedCard]) -> List[ShedCard]:
        return [c for c in cards if c.rank != "3"]

    def is_quad(self):
        """Check if top four cards, excluding see through threes, are same rank"""
        without_threes = self._remove_threes(self.active_deck)
        ranks = [c.rank for c in without_threes]
        # final four ranks are all the same
        return len(without_threes) >= 4 and len(set(ranks[-4:])) == 1

    def play_card(self, card: ShedCard) -> bool:
        card = ShedCard(card.suit, card.rank)

        if card.is_ten():
            # Ten burns the deck
            self.active_deck = []
            return True

        self.active_deck.append(card)

        if self.is_quad():
            # Quads burns the deck
            self.active_deck = []
            return True

        return False

    def get_legal_actions(self, player: ShedPlayer) -> List[ShedAction]:
        """Returns ShedAction playable from current game state"""
        typed_cards = [ShedCard(card.suit, card.rank) for card in player.hand]
        playable_cards = [card for card in typed_cards if self.is_legal_card(card)]

        full_actions = [self.rank_to_action[card.rank] for card in playable_cards]

        # Can only perform pick up when cards are present
        can_pickup = len(self.active_deck) > 0
        if can_pickup:
            full_actions = full_actions + [ShedAction.Pickup]
        unique_actions = list(set(full_actions))

        return unique_actions

    def is_legal_card(self, card: ShedCard) -> bool:
        card = ShedCard(card.suit, card.rank)
        # Threes are see-through
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

    def is_over(self) -> bool:
        """Check if the game is over"""

        for player in self.players:
            if not player.hand:
                return True

        return False

    def get_top_card_and_count(self) -> Tuple[Optional[Card], int]:
        """Get the top card in the deck and number of repetitions"""
        no_threes = self._remove_threes(self.active_deck)
        if not len(no_threes):
            return None, 0
        top_card = no_threes[-1]
        top_card_count = 0
        deck_size = len(no_threes)

        while deck_size > top_card_count:
            next_top_card = no_threes[-(top_card_count + 1)]
            if next_top_card.rank == top_card.rank:
                top_card_count += 1
            else:
                break

        return top_card, top_card_count

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
