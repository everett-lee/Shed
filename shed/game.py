from copy import deepcopy
from typing import List

import numpy as np

from dealer import ShedDealer
from player import ShedPlayer
from judger import ShedJudger
from shed.card import ShedCard


class ShedGame:
    def __init__(self, allow_step_back=False):
        """Initialize the Game"""
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_starting_cards = 5

    def configure(self, game_config) -> None:
        """Specifiy some game specific parameters, such as number of players"""
        self.num_players = game_config["game_num_players"]

    def init_game(self) -> tuple:
        """Initialilze the game"""
        self.dealer = ShedDealer(self.np_random)

        self.players = []
        for i in range(self.num_players):
            self.players.append(ShedPlayer(i, self.np_random))

        self.judger = ShedJudger(self.np_random)

        for i in range(self.num_starting_cards):
            for j in range(self.num_players):
                self.dealer.deal_card(self.players[j])

        for i in range(self.num_players):
            self.players[i].score = self.judger.judge_round(
                self.players[i]
            )

        self.winner = {}
        for i in range(self.num_players):
            self.winner["player" + str(i)] = 0

        self.history = []
        self.game_pointer = 0

        return self.get_state(self.game_pointer), self.game_pointer

    def step(self, action: Action):
        """Get the next state

        Args:
            action (str): a specific action of shed
        Returns:/
            dict: next player's state
            int: next plater's id
        """

        # action should be play or pick up
        if self.allow_step_back:
            p = deepcopy(self.players[self.game_pointer])
            d = deepcopy(self.dealer)
            w = deepcopy(self.winner)
            self.history.append((d, p, w))

        next_state = {}
        active_player = [player for player in self.players if player.get_player_id() == self.game_pointer][0]
        self.dealer.handle_action(active_player, action)

        next_state = {}

        next_state["dealer hand"] = dealer_hand
        next_state["actions"] = ("hit", "stand")
        next_state["state"] = (hand, dealer_hand)

        return next_state, self.game_pointer

    def step_back(self):
        """Return to the previous state of the game

        Returns:
            Status (bool): check if the step back is success or not
        """
        # while len(self.history) > 0:
        if len(self.history) > 0:
            (
                self.dealer,
                self.players[self.game_pointer],
                self.winner,
            ) = self.history.pop()
            return True
        return False

    def get_num_players(self):
        """Return the number of players in blackjack"""

        return self.num_players

    def get_num_actions(self) -> int:
        """Return the number of applicable actions"""

        return 13
    def get_player_id(self):
        """Return the current player's id

        Returns:
            player_id (int): current player's id
        """
        return self.game_pointer

    def get_state(self, player: ShedPlayer) -> dict:
        """Return player's state as a dict"""
        state = {"actions": self.get_legal_actions(player), "hand": player.hand}

        return state

