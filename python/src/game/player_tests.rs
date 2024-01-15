#[cfg(test)]
mod player_tests {
    use crate::{
        game::{action::Action, player::Player},
        Card, Rank, Suit,
    };

    #[test]
    fn test_take_and_play_cards() {
        let mut player = Player::new(0);
        let mut hand = vec![
            Card::new(Suit::Spades, Rank::Ace),
            Card::new(Suit::Diamonds, Rank::Ace),
            Card::new(Suit::Hearts, Rank::Nine),
        ];
        player.take_cards(&mut hand);
        assert_eq!(player.hand().len(), 3);

        let first_played_ace = player.play_card(Action::Ace);
        assert_eq!(*first_played_ace.rank(), Rank::Ace);
        assert_eq!(player.hand().len(), 2);
        let second_played_ace = player.play_card(Action::Ace);
        assert_eq!(*second_played_ace.rank(), Rank::Ace);
        assert_eq!(player.hand().len(), 1);
    }

    #[test]
    fn test_hand_to_actions() {
        let mut player = Player::new(0);
        let mut hand = vec![
            Card::new(Suit::Spades, Rank::Ace),
            Card::new(Suit::Diamonds, Rank::Ace),
            Card::new(Suit::Hearts, Rank::Nine),
            Card::new(Suit::Hearts, Rank::Two),
            Card::new(Suit::Diamonds, Rank::Two),
            Card::new(Suit::Hearts, Rank::Two),
            Card::new(Suit::Clubs, Rank::Two),
            Card::new(Suit::Hearts, Rank::Queen),
        ];
        player.take_cards(&mut hand);
        assert_eq!(player.hand().len(), 8);

        let actions = player.hand_to_actions();
        assert_eq!(
            actions,
            vec![Action::Ace, Action::Two, Action::Nine, Action::Queen]
        );
    }
}
