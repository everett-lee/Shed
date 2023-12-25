from typing import List, Dict

import numpy as np

from dealer import ShedDealer
from player import ShedPlayer
from judger import ShedJudger
from shed.game.round import ShedRound, ShedAction


class ShedGame:
    def __init__(self, num_players: int = 2):
        """Initialize the Game"""
        self.allow_step_back = False
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        self.num_starting_cards = 5
        self.game_pointer = 0
        self.round = None
        self.dealer = None
        self.players = []
        self.payoffs = [0 for _ in range(self.num_players)]

    def configure(self, game_config) -> None:
        """Specifiy some game specific parameters, such as number of players"""
        self.num_players = game_config["game_num_players"]

    def init_game(self) -> tuple:
        """Initialilze the game"""
        self.dealer = ShedDealer(self.np_random)

        self.players = [ShedPlayer(i, self.np_random) for i in range(self.num_players)]

        self.judger = ShedJudger(self.np_random)

        for player in self.players:
            for _ in range(self.num_starting_cards):
                self.dealer.deal_card(player)
            player.score = self.judger.judge_round(player)

        # Init the round
        self.round = ShedRound(self.dealer, self.players, self.np_random)

        game_pointer = self.round.game_pointer
        first_player = self.players[0]

        self.winner = {}
        for i in range(self.num_players):
            self.winner["player" + str(i)] = 0

        self.history = []

        return self.get_state(first_player), game_pointer

    def step(self, action: ShedAction):
        """Get the next state

        Args:
            action (str): a specific action of shed
        Returns:/
            dict: next player's state
            int: next plater's id
        """

        # Then we proceed to the next round
        self.game_pointer = self.round.proceed_round(self.players, action)

        next_player = self.players[self.game_pointer]
        next_state = self.get_state(next_player)

        return next_state, self.game_pointer

    def get_num_players(self):
        """Return the number of players in blackjack"""

        return self.num_players

    def get_num_actions(self) -> int:
        """Return the number of applicable actions"""

        return 14

    def get_player_id(self):
        """Return the current player's id

        Returns:
            player_id (int): current player's id
        """
        return self.game_pointer

    def get_state(self, player: ShedPlayer) -> dict:
        """Return player's state as a dict"""
        state = {
            "legal_actions": self.round.get_legal_actions(player),
            "hand": player.hand,
            "live_deck_size": self.round.get_active_deck_size(),
            "active_deck": self.round.active_deck,
            "player_score": player.score,
        }

        return state

    def is_over(self) -> bool:
        """
        Check if the game is over

        Returns:
            (boolean): True if the game is over
        """
        return self.round.is_over()

    def get_payoffs(self) -> List[int]:
        """Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        """
        winner = self.round.winner
        if winner is not None:
            self.payoffs[winner.player_id] = 1
        return self.payoffs

    def get_legal_actions(self) -> Dict[int, ShedAction]:
        current_player = self.players[self.game_pointer]
        legal_actions = self.round.get_legal_actions(current_player)
        mapped_actions = {}
        for action in legal_actions:
            if action == ShedAction.Ace:
                mapped_actions[0] = ShedAction.Ace
            if action == ShedAction.Two:
                mapped_actions[1] = ShedAction.Two
            if action == ShedAction.Three:
                mapped_actions[2] = ShedAction.Three
            if action == ShedAction.Four:
                mapped_actions[3] = ShedAction.Four
            if action == ShedAction.Five:
                mapped_actions[4] = ShedAction.Five
            if action == ShedAction.Six:
                mapped_actions[5] = ShedAction.Six
            if action == ShedAction.Seven:
                mapped_actions[6] = ShedAction.Seven
            if action == ShedAction.Eight:
                mapped_actions[7] = ShedAction.Eight
            if action == ShedAction.Nine:
                mapped_actions[8] = ShedAction.Nine
            if action == ShedAction.Ten:
                mapped_actions[9] = ShedAction.Ten
            if action == ShedAction.Jack:
                mapped_actions[10] = ShedAction.Jack
            if action == ShedAction.Queen:
                mapped_actions[11] = ShedAction.Queen
            if action == ShedAction.King:
                mapped_actions[12] = ShedAction.King

        return mapped_actions
