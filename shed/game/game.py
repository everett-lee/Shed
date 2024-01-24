from typing import Any, Dict, List, Tuple

import numpy as np
import rust_shed
from logzero import logger
from rlcard.games.base import Card

from shed.game.utils import ShedAction

StateDict = Dict[str, Any]


class ShedGame:
    def __init__(self, config: dict, num_players: int = 2):
        """Initialize the Game"""
        self.allow_step_back = False
        self.debug_mode = False
        self.np_random = np.random.RandomState()
        self.game = rust_shed.Game(num_players=num_players, debug_mode=False, max_n_steps=10_000)
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

    def step(self, action: ShedAction) -> Tuple[StateDict, int]:
        """Get the next state"""
        next_state, game_pointer = self.game.step(action)
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
        state = self.game.get_state(player_id=player_id)

        return {
            "active_deck": [Card(suit=c.suit, rank=c.rank) for c in state.live_deck],
            "legal_actions": state.legal_actions,
            "hand": [c.get_index() for c in state.hand],
            "live_deck_size": state.live_deck_size,
            "top_card": state.top_card,
            "top_card_count": state.top_card_count,
            "position": state.position,
            "current_player": state.current_player,
            "unplayed_deck_size": state.unplayed_deck_size,
        }

    def is_over(self) -> bool:
        """
        Check if the game is over
        """
        return self.game.is_over()

    def get_payoffs(self) -> List[int]:
        return self.game.get_payoffs()

    def get_legal_actions(self) -> List[ShedAction]:
        return [ShedAction[a] for a in self.game.get_legal_actions()]
