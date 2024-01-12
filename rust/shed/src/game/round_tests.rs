#[cfg(test)]
mod round_tests {
    use crate::{game::{player::Player, action::Action, round::Round, dealer::Dealer}, Card, Suit, Rank};


    #[test]
    fn test_remove_threes() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let mut round = Round::new(dealer, players, 0);
        round.play_card(Card::new(Suit::Spades, Rank::Ace));        
        round.play_card(Card::new(Suit::Spades, Rank::Two));        
        round.play_card(Card::new(Suit::Spades, Rank::Three));
        round.play_card(Card::new(Suit::Diamonds, Rank::Ace));
        round.play_card(Card::new(Suit::Hearts, Rank::Three));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));        

        let without_threes = round.get_deck_no_threes();
        assert_eq!(round.active_deck().len(), 6);
        assert_eq!(without_threes, vec![
            Card::new(Suit::Spades, Rank::Ace), Card::new(Suit::Spades, Rank::Two),  Card::new(Suit::Diamonds, Rank::Ace),Card::new(Suit::Hearts, Rank::Queen)
        ])
    }

    #[test]
    fn test_has_quad() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let mut round = Round::new(dealer, players, 0);
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));        
        round.play_card(Card::new(Suit::Spades, Rank::Queen));        
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Spades, Rank::Three));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));        
        round.play_card(Card::new(Suit::Hearts, Rank::Three));

        assert!(round.has_quad());
    }

    #[test]
    fn test_has_quad_empty() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let round = Round::new(dealer, players, 0);
        assert!(!round.has_quad())
    }

    #[test]
    fn test_has_quad_distruped() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let mut round = Round::new(dealer, players, 0);
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));        
        round.play_card(Card::new(Suit::Spades, Rank::Queen));        
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Spades, Rank::Two));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));        
        round.play_card(Card::new(Suit::Hearts, Rank::Three));
        assert!(!round.has_quad())
    }
}