from rlcard.games.base import Card


class ShedCard(Card):
    valid_suit = ["S", "H", "D", "C", "BJ", "RJ"]
    valid_rank = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    rank_to_value = {
        "2": 2,
        "4": 4,
        "5": 5,
        "6": 6,
        "8": 8,
        "9": 9,
        "J": 11,
        "Q": 12,
        "K": 13,
    }

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank
        else:
            return ValueError("Can only compare to other ShedCard")

    def __lt__(self, other):
        if isinstance(other, Card):
            value_self = self.rank_to_value[self.rank]
            value_other = self.rank_to_value[other.rank]
            return value_self < value_other
        else:
            return ValueError("Can only compare to other ShedCard")

    def __gt__(self, other):
        if isinstance(other, Card):
            value_self = self.rank_to_value[self.rank]
            value_other = self.rank_to_value[other.rank]
            return value_self > value_other
        else:
            return ValueError("Can only compare to other ShedCard")
