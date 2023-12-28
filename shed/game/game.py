from typing import Any, Dict, List, Tuple, Union

import numpy as np
from logzero import logger

from shed.game.dealer import ShedDealer
from shed.game.judger import ShedJudger
from shed.game.player import ShedPlayer
from shed.game.round import ShedRound
from shed.game.utils import ShedAction

StateDict = Dict[str, Any]


class ShedGame:
    def __init__(self, config: dict, num_players: int = 2):
        """Initialize the Game"""
        self.allow_step_back = False
        self.debug_mode = False
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        self.num_starting_cards = 5
        self.game_pointer = 0
        self.round = None
        self.dealer = None
        self.judger = None
        self.players = []
        self.history = []
        self.payoffs = [0 for _ in range(self.num_players)]

        self.configure(config)

    def configure(self, game_config: Dict[str, Any]) -> None:
        """Specifiy some game specific parameters, such as number of players"""

        logger.info(f"Configuring game with config: {game_config}")
        if "debug_mode" in game_config:
            self.debug_mode = game_config["debug_mode"]
        if "game_num_players" in game_config:
            self.num_players = game_config["game_num_players"]

    def init_game(self) -> Tuple[StateDict, int]:
        """Initialilse the game"""
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

    def step(self, action: ShedAction) -> Tuple[StateDict, int]:
        """Get the next state"""

        # Proceed to the next round
        self.game_pointer = self.round.proceed_round(self.players, action)
        player = self.players[self.game_pointer]
        player.score = self.judger.judge_round(player)
        if self.debug_mode:
            logger.info(f"Player hand: {[c.rank for c in player.hand]}")
            logger.info(f"New player score: {player.score}")

        next_player = self.players[self.game_pointer]
        next_state = self.get_state(next_player)

        return next_state, self.game_pointer

    def get_num_players(self) -> int:
        """Return the number of players in shed"""

        return self.num_players

    def get_num_actions(self) -> int:
        """Return the number of applicable actions"""

        return 14

    def get_player_id(self):
        """Return the current player's id"""
        return self.game_pointer

    def get_state(self, player: Union[int, ShedPlayer]) -> StateDict:
        """Return player's state as a dict"""

        if isinstance(player, int):
            player = self.players[player]

        return {
            "legal_actions": self.get_legal_actions(),
            "hand": player.hand,
            "live_deck_size": self.round.get_active_deck_size(),
            "active_deck": self.round.active_deck,
            "top_card": self.round.get_top_card(),
            "position": self.get_position(player, self.players),
            "current_player": self.game_pointer,
        }

    def is_over(self) -> bool:
        """
        Check if the game is over
        """
        return self.round.is_over

    def get_position(self, player: ShedPlayer, players: List[ShedPlayer]):
        sorted_by_hand = sorted(players, key=lambda p: len(p.hand))
        ids = [p.player_id for p in sorted_by_hand]
        return ids.index(player.player_id)

    def get_payoffs(self) -> List[int]:
        """Return the payoffs of the game"""
        winner = self.round.winner
        if winner is not None:
            # TODO make nicer
            self.payoffs[winner.player_id] += 1
            for i in range(len(self.payoffs)):
                if i != winner.player_id:
                    self.payoffs[i] -= 1

        return self.payoffs

    def get_legal_actions(self) -> List[ShedAction]:
        current_player = self.players[self.game_pointer]
        legal_actions = self.round.get_legal_actions(current_player)
        return legal_actions
