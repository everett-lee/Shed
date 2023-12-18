import numpy as np


class ShedPlayer:
    def __init__(self, player_id: int, np_random: np.random) -> None:
        """Initialize a player class"""
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.score = 0

    def get_player_id(self) -> int:
        """Return player's id"""
        return self.player_id
