#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn test_card_equals() {
        assert_eq!(Card::new(Suit::Spades, Rank::Ace), Card::new(Suit::Spades, Rank::Ace));
        assert_eq!(Card::new(Suit::Clubs, Rank::Jack), Card::new(Suit::Spades, Rank::Jack));
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
    fn ab() {
        let c1 = Card::new(Suit::Spades, Rank::Three);
        let c2 = Card::new(Suit::Diamonds, Rank::Ace);
        assert!(c2 < c1);
    }

}