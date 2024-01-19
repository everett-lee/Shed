#[cfg(test)]
mod card_tests {
    use crate::*;

    #[test]
    fn test_card_equals() {
        assert_eq!(
            Card::new(Suit::Spades, Rank::Ace),
            Card::new(Suit::Spades, Rank::Ace)
        );
        assert_eq!(
            Card::new(Suit::Clubs, Rank::Jack),
            Card::new(Suit::Spades, Rank::Jack)
        );
    }

    #[test]
    fn test_less_than() {
        let c1 = Card::new(Suit::Spades, Rank::Nine);
        let c2 = Card::new(Suit::Diamonds, Rank::Eight);
        assert!(c2 < c1);
    }

    #[test]
    fn test_less_than_versus_special() {
        let c1 = Card::new(Suit::Spades, Rank::Nine);
        let c2 = Card::new(Suit::Diamonds, Rank::Three);
        assert!(c2 < c1);
    }

    #[test]
    fn test_less_than_or_equal() {
        let c1 = Card::new(Suit::Spades, Rank::Nine);
        let c2 = Card::new(Suit::Diamonds, Rank::Nine);
        assert!(c2 <= c1);
    }

    #[test]
    fn test_greater_than() {
        let c1 = Card::new(Suit::Spades, Rank::Two);
        let c2 = Card::new(Suit::Diamonds, Rank::Eight);
        assert!(c2 > c1);
    }

    #[test]
    fn test_greater_than_ace() {
        let c1 = Card::new(Suit::Spades, Rank::Ace);
        let c2 = Card::new(Suit::Diamonds, Rank::King);
        assert!(!(c2 > c1));
    }

    #[test]
    fn test_greater_than_or_equal() {
        let c1 = Card::new(Suit::Spades, Rank::Nine);
        let c2 = Card::new(Suit::Diamonds, Rank::Nine);
        assert!(c2 >= c1);
    }
}
