from typing import Dict, List, Union

import numpy as np

from shed.game.dealer import ShedDealer
from shed.game.judger import ShedJudger
from shed.game.player import ShedPlayer
from shed.game.round import ShedRound
from shed.game.utils import ShedAction


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
        self.game_pointer = 0

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
        player = self.players[self.game_pointer]
        player.score = self.judger.judge_round(player)
        print(f"PLAYER HAND: {[c.rank for c in player.hand]}")
        print(f"NEW PLAYER SCORE: {player.score}")

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

    def get_state(self, player: Union[int, ShedPlayer]) -> dict:
        if isinstance(player, int):
            player = self.players[player]

        """Return player's state as a dict"""
        state = {
            "legal_actions": self.get_legal_actions(),
            "hand": player.hand,
            "live_deck_size": self.round.get_active_deck_size(),
            "active_deck": self.round.active_deck,
            "player_score": player.score,
            "current_player": self.game_pointer,
        }

        return state

    def is_over(self) -> bool:
        """
        Check if the game is over

        Returns:
            (boolean): True if the game is over
        """
        return self.round.is_over

    def get_payoffs(self) -> List[int]:
        """Return the payoffs of the game
        F
                Returns:
                    (list): Each entry corresponds to the payoff of one player
        """
        winner = self.round.winner
        if winner is not None:
            self.payoffs[winner.player_id] += 1
        return self.payoffs

    def get_legal_actions(self) -> List[ShedAction]:
        current_player = self.players[self.game_pointer]
        legal_actions = self.round.get_legal_actions(current_player)
        return legal_actions

    #
    # def map_key_to_action(self, key: int) -> ShedAction:
    #     mapped = {
    #         0: ShedAction.Ace,
    #         1: ShedAction.Two,
    #         2: ShedAction.Three,
    #         3: ShedAction.Four,
    #         4: ShedAction.Five,
    #         5: ShedAction.Six,
    #         6: ShedAction.Seven,
    #         7: ShedAction.Eight,
    #         8: ShedAction.Nine,
    #         9: ShedAction.Ten,
    #         10: ShedAction.Jack,
    #         11: ShedAction.Queen,
    #         12: ShedAction.King,
    #         13: ShedAction.Pickup,
    #     }
    #     return mapped[key]
