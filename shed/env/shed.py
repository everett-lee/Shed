import json
import os
from collections import OrderedDict

import numpy as np
import rlcard
from rlcard.envs import Env

from shed.game.game import ShedGame
from shed.game.utils import ShedAction

DEFAULT_GAME_CONFIG = {
    "game_num_players": 2,
}


class ShedEnv(Env):
    """Shed Environment"""

    id_to_action = {
        0: ShedAction.Ace,
        1: ShedAction.Two,
        2: ShedAction.Three,
        3: ShedAction.Four,
        4: ShedAction.Five,
        5: ShedAction.Six,
        6: ShedAction.Seven,
        7: ShedAction.Eight,
        8: ShedAction.Nine,
        9: ShedAction.Ten,
        10: ShedAction.Jack,
        11: ShedAction.Queen,
        12: ShedAction.King,
        13: ShedAction.Pickup,
    }
    action_to_id = {v: k for k, v in id_to_action.items()}

    def __init__(self, config):
        """Initialize the Shed environment"""
        self.name = "shed"
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = ShedGame()
        super().__init__(config)
        # A deck for each player's hand plus the live deck
        self.state_shape = [[53] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

        with open(
            os.path.join(rlcard.__path__[0], "games/limitholdem/card2index.json"), "r"
        ) as file:
            self.card2index = json.load(file)

    def _get_legal_actions(self):
        """Get all leagal actions

        Returns:
            encoded_action_list (list): return encoded legal action list (from str to int)
        """
        return self.game.get_legal_actions()

    def _extract_state(self, state):
        """Extract the state representation from state dictionary for agent

        Note: Currently the use the hand cards and the public cards. TODO: encode the states

        Args:
            state (dict): Original state from the game

        Returns:
            observation (list): combine the player's score and dealer's observable score for observation
        """
        extracted_state = {}

        legal_actions = OrderedDict(
            {self.action_to_id[a]: None for a in state["legal_actions"]}
        )
        extracted_state["legal_actions"] = legal_actions

        active_deck = state["active_deck"]
        hand = state["hand"]
        cards = active_deck + hand
        idx = [self.card2index[card.get_index()] for card in cards]
        obs = np.zeros(53)
        obs[idx] = 1
        obs[52] = state["player_score"]
        extracted_state["obs"] = obs

        extracted_state["raw_obs"] = state
        extracted_state["raw_legal_actions"] = [a for a in state["legal_actions"]]

        extracted_state["action_record"] = self.action_recorder

        return extracted_state

    def get_payoffs(self):
        """Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        """
        return self.game.get_payoffs()

    def _decode_action(self, action_id: int) -> ShedAction:
        """Decode the action for applying to the game

        Args:
            action id (int): action id

        Returns:
            action (str): action for the game
        """
        legal_actions = self.game.get_legal_actions()
        decoded_action = self.id_to_action[action_id]
        if decoded_action not in legal_actions:
            return ShedAction.Pickup

        return decoded_action

    def get_perfect_information(self):
        """Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        """
        state = {}
        state["active_deck"] = [c.get_index() for c in self.game.round.active_deck]
        state["hand_cards"] = [
            [c.get_index() for c in self.game.players[i].hand]
            for i in range(self.num_players)
        ]
        state["current_player"] = self.game.game_pointer
        state["legal_actions"] = self.game.get_legal_actions()
        return state
