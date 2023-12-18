from shed.model.card import Suit, PlayingCard, Value, Deck

values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
faces = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
pairs = list(zip(values, faces))

cards = []

for suit in [Suit.CLUBS, Suit.HEARTS, Suit.DIAMONDS, Suit.SPADES]:
    cards = cards + [
        PlayingCard(suit=suit, value=Value(display_value=face, value=value))
        for value, face in pairs
    ]

deck = Deck(cards=cards)
