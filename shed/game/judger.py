from shed.game.player import ShedPlayer


class ShedJudger:
    def __init__(self, np_random):
        """Initialize a judger class"""
        self.np_random = np_random
        self.rank2score = {
            "A": 5,
            "2": 0,
            "3": 2,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 2,
            "8": 0,
            "9": 0,
            "T": 2,
            "J": 0,
            "Q": 0,
            "K": 0,
        }

    def judge_round(self, player: ShedPlayer):
        """Judge the target player's status"""
        score = self.judge_score(player.hand)
        return score

    def judge_game(self, game, game_pointer):
        """Judge the winner of the game"""

        if game.players[game_pointer].status == "bust":
            game.winner["player" + str(game_pointer)] = -1
        elif game.dealer.status == "bust":
            game.winner["player" + str(game_pointer)] = 2
        else:
            if game.players[game_pointer].score > game.dealer.score:
                game.winner["player" + str(game_pointer)] = 2
            elif game.players[game_pointer].score < game.dealer.score:
                game.winner["player" + str(game_pointer)] = -1
            else:
                game.winner["player" + str(game_pointer)] = 1

    def judge_score(self, cards):
        """Judge the score of a given cards set"""
        score = 0
        count_a = 0
        for card in cards:
            card_score = self.rank2score[card.rank]
            score += card_score
            if card.rank == "A":
                count_a += 1
        while score > 21 and count_a > 0:
            count_a -= 1
            score -= 10
        return score
