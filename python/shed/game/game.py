import json
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import rust_shed
from logzero import logger
from rlcard.games.base import Card

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
        # TODO make parma of rust_shed, self.num_starting_cards = 5

        self.game = rust_shed.Game(num_players=num_players, debug_mode=False)
        self.configure(config)

    def configure(self, game_config: Dict[str, Any]) -> None:
        """Specifiy some game specific parameters, such as number of players"""

        logger.info(f"Configuring game with config: {game_config}")
        if "debug_mode" in game_config:
            self.debug_mode = game_config["debug_mode"]
        if "game_num_players" in game_config:
            self.num_players = game_config["game_num_players"]

    def init_game(self) -> Tuple[StateDict, int]:
        next_state, game_pointer = self.game.init_game()
        return self.get_state(player_id=game_pointer), game_pointer
        # return self.get_state(first_player), game_pointer

    def step(self, action: ShedAction) -> Tuple[StateDict, int]:
        """Get the next state"""

        # # Proceed to the next round
        # self.game_pointer = self.round.proceed_round(self.players, action)
        # player = self.players[self.game_pointer]
        # if self.debug_mode:
        #     logger.info(f"Player hand: {[c.rank for c in player.hand]}")
        #     logger.info(f"New player score: {player.score}")
        #
        # next_player = self.players[self.game_pointer]
        # next_state = self.get_state(next_player)
        #
        # # TODO debug training mode
        # # print("Round ended")
        # # print(f"Player 1 hand: {[c.get_index() for c in self.players[0].hand]}")
        # # print(f"Player 2 hand: {[c.get_index() for c in self.players[1].hand]}")
        # # print()

        # print("*"*100)
        # print(f"THE ACITON IS {action}")
        # hand = self.game.get_state(self.game.get_active_player_id()).hand
        # print(f"THE HAND IS {[c.get_index() for c in hand]}")
        # print("*"*100)

        next_state, game_pointer = self.game.step(action.value)
        return self.get_state(player_id=game_pointer), game_pointer

    def get_num_players(self) -> int:
        """Return the number of players in shed"""
        return self.game.get_num_players()

    def get_num_actions(self) -> int:
        """Return the number of applicable actions"""

        return self.game.get_num_actions()

    def get_player_id(self):
        """Return the current player's id"""
        return self.game.get_active_player_id()

    def get_state(self, player_id: int) -> StateDict:
        """Return player's state as a dict"""
        json_str = self.game.get_state_json(player_id=player_id)
        state = json.loads(json_str)

        return {
            "active_deck": [Card(suit=c["suit"], rank=c["rank"]) for c in state["live_deck"]],
            "legal_actions": state["legal_actions"],
            "hand": [f"{c['suit']}{c['rank']}" for c in state["hand"]],
            "live_deck_size": int(state["live_deck_size"]),
            "top_card": state["top_card"],
            "top_card_count": int(state["top_card_count"]),
            "position": state["positions"].index(player_id),
            "current_player": state["current_player"],
            "unplayed_deck_size": state["unplayed_deck_size"],
        }

    def is_over(self) -> bool:
        """
        Check if the game is over
        """
        return self.game.is_over()

    def get_position(self, player: ShedPlayer, players: List[ShedPlayer]):
        sorted_by_hand = sorted(players, key=lambda p: len(p.hand))
        ids = [p.player_id for p in sorted_by_hand]
        raise NotImplementedError()
        return ids.index(player.player_id)

    def get_payoffs(self) -> List[int]:
        payoffs = json.loads(self.game.get_payoffs())
        return payoffs

    def get_legal_actions(self) -> List[ShedAction]:
        return [ShedAction[a] for a in self.game.get_legal_actions()]
