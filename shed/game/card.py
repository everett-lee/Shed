from rlcard.games.base import Card


class ShedCard(Card):
    valid_suit = ["S", "H", "D", "C", "BJ", "RJ"]
    valid_rank = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    rank_to_value = {
        "2": 2,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "J": 11,
        "Q": 12,
        "K": 13,
        "T": 14,
        "3": 15,
        "A": 16,
    }

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

    def is_magic_card(self) -> bool:
        return self.rank in ["A", "3", "T", "7"]

    def is_ace(self) -> bool:
        return self.rank == "A"

    def is_ten(self) -> bool:
        return self.rank == "T"

    def is_seven(self) -> bool:
        return self.rank == "7"

    def is_three(self) -> bool:
        return self.rank == "3"

    def __eq__(self, other: "ShedCard") -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank
        else:
            raise ValueError("Can only compare to other ShedCard")

    def __lt__(self, other: "ShedCard") -> bool:
        if other.is_ace() and not self.is_magic_card():
            return False

        if isinstance(other, Card):
            value_self = self.rank_to_value[self.rank]
            value_other = self.rank_to_value[other.rank]
            return value_self < value_other
        else:
            raise ValueError("Can only compare to other ShedCard")

    def __le__(self, other: "ShedCard") -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: "ShedCard") -> bool:
        if self.is_ace():
            return True

        if isinstance(other, Card):
            value_self = self.rank_to_value[self.rank]
            value_other = self.rank_to_value[other.rank]
            return value_self > value_other
        else:
            raise ValueError("Can only compare to other ShedCard")

    def __ge__(self, other: "ShedCard") -> bool:
        return self.__gt__(other) or self.__eq__(other)
