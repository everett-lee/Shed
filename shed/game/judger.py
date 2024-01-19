from shed.game.player import ShedPlayer


class ShedJudger:
    def __init__(self, np_random):
        """Initialize a judger class"""
        self.np_random = np_random
        self.rank2score = {
            "A": 2,
            "2": -2,
            "3": 1,
            "4": -2,
            "5": -2,
            "6": -2,
            "7": 1,
            "8": -2,
            "9": -2,
            "T": 1,
            "J": -2,
            "Q": -1,
            "K": -1,
        }

    def judge_round(self, player: ShedPlayer):
        """Judge the target player's status"""
        score = self.judge_score(player.hand)
        return score

    def judge_score(self, cards):
        """Judge the score of a given cards set"""
        return sum([self.rank2score[card.rank] for card in cards]) - len(cards)
