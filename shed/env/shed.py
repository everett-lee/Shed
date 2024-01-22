import json
import os
from collections import OrderedDict

import numpy as np
import rlcard
from rlcard.envs import Env

from shed.agents.AppShedAgent import AppAgent
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
        config = config if config else DEFAULT_GAME_CONFIG
        self.game = ShedGame(config=config)
        super().__init__(config)
        self.obs_size = 109
        # A deck for each player's hand plus the live deck plus score TODO handle jokers
        self.state_shape = [[self.obs_size] for _ in range(self.num_players)]
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
        """Extract the state representation from state dictionary for agent"""
        extracted_state = {}

        legal_actions = OrderedDict(
            {self.action_to_id[ShedAction[a]]: None for a in state["legal_actions"]}
        )
        extracted_state["legal_actions"] = legal_actions

        obs = np.zeros(self.obs_size)
        hand = state["hand"]
        hand_idx = [self.card2index[c] for c in hand]
        obs[hand_idx] = 1

        # TODO 1: use one hot for hand
        # TODO 2: reduce obs size by removing position and len(hand)
        top_card = state["top_card"]
        if top_card:
            # One hot encode top card index
            top_card_index = self.card2index[top_card]
            obs[top_card_index + 52] = 1

        obs[104] = state["top_card_count"]
        obs[105] = state["unplayed_deck_size"]
        obs[106] = len(hand)
        obs[107] = state["position"]
        obs[108] = state["unplayed_deck_size"]

        extracted_state["obs"] = obs

        if self.game.debug_mode:
            print(f"HAND INDEX: {obs[0:52]}")
            print(f"TOP CARD INDEX: {obs[52:104]}")
            print(f"TOP CARD: {top_card}")
            print(f"TOP CARD COUNT: {state['top_card_count']}")
            print(f"HAND SIZE: {len(hand)}")
            print(f"POSITION: {state['position']}")
            print(f"UNPLAYED DECK SIZE: {state['unplayed_deck_size']}")

        extracted_state["raw_obs"] = state
        extracted_state["raw_legal_actions"] = [a for a in state["legal_actions"]]
        extracted_state["action_record"] = self.action_recorder
        extracted_state["current_player_id"] = state["current_player"]

        return extracted_state

    def get_payoffs(self) -> np.array:
        """Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        """
        payoffs = self.game.get_payoffs()
        # TODO remove
        print(f"Payoffs: {payoffs}")
        return np.array(payoffs)

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
            raise ValueError("Action not recognised")

        return decoded_action

    def get_perfect_information(self):
        """Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        """
        state = {}
        # state["active_deck"] = [c.get_index() for c in self.game.round.active_deck]
        state["hand_cards"] = [
            [c.get_index() for c in self.game.players[i].hand]
            for i in range(self.num_players)
        ]
        state["current_player"] = self.game.game_pointer
        state["legal_actions"] = self.game.get_legal_actions()
        return state

    def get_game_state(self, player_id: int):
        return self.game.get_state(player_id)

    def set_next_action(self, player_id: int, action: ShedAction):
        agent = self.agents[player_id]
        if isinstance(agent, AppAgent):
            agent.set_next_action(action)
        else:
            raise Exception(f"No AppAgent for player id {player_id}")

    # Override
    async def run_async(self, is_training=False):
        trajectories = [[] for _ in range(self.num_players)]
        state, player_id = self.reset()

        # Loop to play the game
        trajectories[player_id].append(state)
        while not self.is_over():
            agent = self.agents[player_id]
            if isinstance(agent, AppAgent):
                action, _ = await agent.eval_step(state)
            else:
                action, _ = agent.eval_step(state)

            # Environment steps
            next_state, next_player_id = self.step(
                action, self.agents[player_id].use_raw
            )
            # Save action
            trajectories[player_id].append(action)

            # Set the state and player
            state = next_state
            player_id = next_player_id

            # Save state.
            if not self.game.is_over():
                trajectories[player_id].append(state)

        # Add a final state to all the players
        for player_id in range(self.num_players):
            state = self.get_state(player_id)
            trajectories[player_id].append(state)

        # Payoffs
        payoffs = self.get_payoffs()

        return trajectories, payoffs
