from shed.game.player import ShedPlayer


class ShedJudger:
    def __init__(self, np_random):
        """Initialize a judger class"""
        self.np_random = np_random
        self.rank2score = {
            "A": 5,
            "2": -1,
            "3": 2,
            "4": -1,
            "5": -1,
            "6": -1,
            "7": 2,
            "8": -1,
            "9": -1,
            "T": 2,
            "J": 0,
            "Q": 0,
            "K": 0,
        }

    def judge_round(self, player: ShedPlayer):
        """Judge the target player's status"""
        score = self.judge_score(player.hand)
        return score

    def judge_score(self, cards):
        """Judge the score of a given cards set"""
        return sum([self.rank2score[card.rank] for card in cards])