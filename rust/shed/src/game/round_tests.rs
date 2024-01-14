#[cfg(test)]
mod round_tests {

    use crate::{
        game::{dealer::Dealer, player::Player, round::Round, action::Action},
        Card, Rank, Suit,
    };

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
        assert_eq!(
            without_threes,
            vec![
                Card::new(Suit::Spades, Rank::Ace),
                Card::new(Suit::Spades, Rank::Two),
                Card::new(Suit::Diamonds, Rank::Ace),
                Card::new(Suit::Hearts, Rank::Queen)
            ]
        )
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

    #[test]
    fn test_get_top_card_and_count() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let mut round = Round::new(dealer, players, 0);
        round.play_card(Card::new(Suit::Clubs, Rank::Jack));
        round.play_card(Card::new(Suit::Diamonds, Rank::Two));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_rank_and_count();
        assert_eq!(received_top_card, Some(Rank::Queen));
        assert_eq!(count, 1);
    }

    #[test]
    fn test_get_top_card_and_count_empty_deck() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let round = Round::new(dealer, players, 0);

        let (received_top_card, count) = round.get_top_card_rank_and_count();
        assert_eq!(received_top_card, None);
        assert_eq!(count, 0);
    }

    #[test]
    fn test_get_top_card_and_count_triple() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let mut round = Round::new(dealer, players, 0);
        round.play_card(Card::new(Suit::Clubs, Rank::Two));
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_rank_and_count();
        assert_eq!(received_top_card, Some(Rank::Queen));
        assert_eq!(count, 3);
    }

    #[test]
    fn test_get_top_card_and_count_triple_interupted() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let mut round = Round::new(dealer, players, 0);
        round.play_card(Card::new(Suit::Clubs, Rank::Two));
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));
        round.play_card(Card::new(Suit::Diamonds, Rank::Four));
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_rank_and_count();
        assert_eq!(received_top_card, Some(Rank::Queen));
        assert_eq!(count, 2);
    }

    #[test]
    fn test_get_top_card_and_count_triple_with_three() {
        let dealer = Dealer::new();
        let players = vec![Player::new(0)];
        let mut round = Round::new(dealer, players, 0);
        round.play_card(Card::new(Suit::Clubs, Rank::Two));
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));
        round.play_card(Card::new(Suit::Diamonds, Rank::Three));
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_rank_and_count();
        assert_eq!(received_top_card, Some(Rank::Queen));
        assert_eq!(count, 3);
    }

    #[test]
    fn test_get_legal_actions() {
        let dealer = Dealer::new();
        let mut round = Round::new(dealer, vec![Player::new(0)], 0);
        round.play_card(Card::new(Suit::Clubs, Rank::Nine));

        // player hand
        round.get_player(0).take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen), Card::new(Suit::Hearts, Rank::Queen),
            Card::new(Suit::Clubs, Rank::Two), Card::new(Suit::Diamonds, Rank::Two),
            Card::new(Suit::Diamonds, Rank::Nine), Card::new(Suit::Diamonds, Rank::Three),
            Card::new(Suit::Diamonds, Rank::Seven)  
        ]);

        let legal_actions = round.get_legal_actions(0);
        assert_eq!(legal_actions, vec![
            Action::Three, Action::Seven, Action::Nine, Action::Queen, Action::Pickup
        ])
    }


    #[test]
    fn test_get_legal_actions_empty_active_deck() {
        let dealer = Dealer::new();
        let mut round = Round::new(dealer, vec![Player::new(0)], 0);

        // player hand
        round.get_player(0).take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen), Card::new(Suit::Hearts, Rank::Queen),
            Card::new(Suit::Clubs, Rank::Two), Card::new(Suit::Diamonds, Rank::Two),
            Card::new(Suit::Diamonds, Rank::Nine), Card::new(Suit::Diamonds, Rank::Three),
            Card::new(Suit::Diamonds, Rank::Seven) 
        ]);

        let legal_actions = round.get_legal_actions(0);
        assert_eq!(legal_actions, vec![
            Action::Two, Action::Three, Action::Seven, Action::Nine, Action::Queen
        ])
    }

    #[test]
    fn test_is_over_true() {
        let dealer = Dealer::new();
        let mut round = Round::new(dealer, vec![Player::new(0), Player::new(1)], 0);

        round.get_player(0).take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen) 
        ]);
        assert!(round.is_over());

    }

    #[test]
    fn test_is_over_false() {
        let dealer = Dealer::new();
        let mut round = Round::new(dealer, vec![Player::new(0), Player::new(1)], 0);

        round.get_player(0).take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen) 
        ]);
        round.get_player(1).take_cards(&mut vec![
            Card::new(Suit::Spades, Rank::Ace) 
        ]);
        assert!(!round.is_over());

    }
}
