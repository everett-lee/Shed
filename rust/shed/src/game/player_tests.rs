#[cfg(test)]
mod player_tests {
    use crate::{game::{player::Player, action::Action}, Card, Suit, Rank};


    #[test]
    fn test_take_and_play_cards() {
        let mut player = Player::new(0);
        let mut hand = vec![Card::new(Suit::Spades, Rank::Ace), Card::new(Suit::Diamonds, Rank::Ace), Card::new(Suit::Hearts, Rank::Nine)];
        player.take_cards( &mut hand);
        assert_eq!(player.hand().len(), 3);
        
        let first_played_ace = player.play_card(Action::Ace);
        assert_eq!(*first_played_ace.rank(), Rank::Ace);
        assert_eq!(player.hand().len(), 2);
        let second_played_ace = player.play_card(Action::Ace);
        assert_eq!(*second_played_ace.rank(), Rank::Ace);
        assert_eq!(player.hand().len(), 1);
    }
}