mod round_tests {
    use crate::{
        game::{action::Action, dealer::Dealer, player::Player, round::Round},
        Card, Rank, Suit
    };

    #[test]
    fn test_remove_threes() {
        let mut round = Round::new(0);
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
    fn test_deck_burned_on_quad() {
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));
        round.play_card(Card::new(Suit::Spades, Rank::Queen));
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Spades, Rank::Three));
        assert_eq!(round.active_deck().len(), 4);

        round.play_card(Card::new(Suit::Hearts, Rank::Queen));
        assert!(round.active_deck().is_empty());
    }

    #[test]
    fn test_has_quad_empty() {
        let round = Round::new(0);
        assert!(!round.has_quad())
    }

    #[test]
    fn test_has_quad_distruped() {
        let mut round = Round::new(0);
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
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Clubs, Rank::Jack));
        round.play_card(Card::new(Suit::Diamonds, Rank::Two));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_and_count();
        assert_eq!(received_top_card, "HQ");
        assert_eq!(count, 1);
    }

    #[test]
    fn test_get_top_card_and_count_one_king() {
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Clubs, Rank::Jack));
        round.play_card(Card::new(Suit::Diamonds, Rank::Two));
        round.play_card(Card::new(Suit::Clubs, Rank::King));

        let (received_top_card, count) = round.get_top_card_and_count();
        assert_eq!(received_top_card, "CK");
        assert_eq!(count, 1);
    }

    #[test]
    fn test_get_top_card_and_count_double_king() {
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Diamonds, Rank::King));
        round.play_card(Card::new(Suit::Hearts, Rank::King));

        let (received_top_card, count) = round.get_top_card_and_count();
        assert_eq!(received_top_card, "HK");
        assert_eq!(count, 2);
    }

    #[test]
    fn test_get_top_card_and_count_empty_deck() {
        let round = Round::new(0);

        let (received_top_card, count) = round.get_top_card_and_count();
        assert_eq!(received_top_card, "");
        assert_eq!(count, 0);
    }

    #[test]
    fn test_get_top_card_and_count_triple() {
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Clubs, Rank::Two));
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_and_count();
        assert_eq!(received_top_card, "HQ");
        assert_eq!(count, 3);
    }

    #[test]
    fn test_get_top_card_and_count_triple_interupted() {
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Clubs, Rank::Two));
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));
        round.play_card(Card::new(Suit::Diamonds, Rank::Four));
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_and_count();
        assert_eq!(received_top_card, "HQ");
        assert_eq!(count, 2);
    }

    #[test]
    fn test_get_top_card_and_count_triple_with_three() {
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Clubs, Rank::Two));
        round.play_card(Card::new(Suit::Clubs, Rank::Queen));
        round.play_card(Card::new(Suit::Diamonds, Rank::Three));
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        let (received_top_card, count) = round.get_top_card_and_count();
        assert_eq!(received_top_card, "HQ");
        assert_eq!(count, 3);
    }

    #[test]
    fn test_get_legal_actions() {
        let mut round = Round::new(0);
        round.play_card(Card::new(Suit::Clubs, Rank::Nine));

        let mut player = Player::new(0);

        // player hand
        player.take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen),
            Card::new(Suit::Hearts, Rank::Queen),
            Card::new(Suit::Clubs, Rank::Two),
            Card::new(Suit::Diamonds, Rank::Two),
            Card::new(Suit::Diamonds, Rank::Nine),
            Card::new(Suit::Diamonds, Rank::Three),
            Card::new(Suit::Diamonds, Rank::Seven),
        ]);

        let legal_actions = round.get_legal_actions(&vec![player], 0);
        assert_eq!(
            legal_actions,
            vec![
                Action::Three,
                Action::Seven,
                Action::Nine,
                Action::Queen,
                Action::Pickup
            ]
        );
    }

    #[test]
    fn test_get_legal_actions_empty_active_deck() {
        let mut round = Round::new(0);
        let mut player = Player::new(0);

        // player hand
        player.take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen),
            Card::new(Suit::Hearts, Rank::Queen),
            Card::new(Suit::Clubs, Rank::Two),
            Card::new(Suit::Diamonds, Rank::Two),
            Card::new(Suit::Diamonds, Rank::Nine),
            Card::new(Suit::Diamonds, Rank::Three),
            Card::new(Suit::Diamonds, Rank::Seven),
        ]);

        let legal_actions = round.get_legal_actions(&vec![player], 0);
        assert_eq!(
            legal_actions,
            vec![
                Action::Two,
                Action::Three,
                Action::Seven,
                Action::Nine,
                Action::Queen
            ]
        )
    }

    #[test]
    fn test_pickup() {
        let mut round = Round::new(0);
        let mut dealer = Dealer::new();
        let player = Player::new(0);
        let mut players = vec![player];
        players.get_mut(0).unwrap().take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen),
            Card::new(Suit::Hearts, Rank::Queen),
        ]);
        round.play_card(Card::new(Suit::Diamonds, Rank::Queen));

        let legal_action: Vec<Action> = round.get_legal_actions(&players, 0);
        assert_eq!(legal_action, vec![Action::Queen, Action::Pickup]);

        round.handle_action(&mut dealer, &mut players, &Action::Pickup);
        assert_eq!(
            players.get_mut(0).unwrap().hand(),
            &vec![
                Card::new(Suit::Clubs, Rank::Queen),
                Card::new(Suit::Hearts, Rank::Queen),
                Card::new(Suit::Diamonds, Rank::Queen)
            ]
        );
        assert!(round.active_deck().is_empty());
    }

    #[test]
    fn test_no_pickup_empty_deck() {
        let mut round = Round::new(0);

        let player = Player::new(0);
        let mut players = vec![player];
        players.get_mut(0).unwrap().take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen),
            Card::new(Suit::Hearts, Rank::Queen),
        ]);

        let legal_action: Vec<Action> = round.get_legal_actions(&players, 0);
        assert_eq!(legal_action, vec![Action::Queen]);
    }

    #[test]
    fn test_proceed_round() {
        let mut dealer = Dealer::new();
        let mut round = Round::new(0);

        let player_1 = Player::new(0);
        let player_2 = Player::new(1);
        let mut players = vec![player_1, player_2];

        players.get_mut(0).unwrap().take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen),
            Card::new(Suit::Clubs, Rank::Two),
        ]);
        players.get_mut(1).unwrap().take_cards(&mut vec![
            Card::new(Suit::Diamonds, Rank::Queen),
            Card::new(Suit::Hearts, Rank::Two),
        ]);

        round.proceed_round(&mut dealer, &mut players, Action::Queen);
        assert_eq!(
            round.active_deck(),
            &vec![Card::new(Suit::Clubs, Rank::Queen)]
        );
        assert_eq!(players.get_mut(0).unwrap().hand().len(), 2);
        assert_eq!(round.active_player_id(), 1);
    }

    #[test]
    fn test_proceed_round_ten() {
        let mut dealer = Dealer::new();
        let mut round = Round::new(0);

        let player_1 = Player::new(0);
        let player_2 = Player::new(1);
        let mut players = vec![player_1, player_2];
        round.play_card(Card::new(Suit::Hearts, Rank::Queen));

        players.get_mut(0).unwrap().take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Queen),
            Card::new(Suit::Clubs, Rank::Ten),
        ]);
        players.get_mut(1).unwrap().take_cards(&mut vec![
            Card::new(Suit::Diamonds, Rank::Queen),
            Card::new(Suit::Hearts, Rank::Two),
        ]);

        round.proceed_round(&mut dealer, &mut players, Action::Ten);
        assert!(round.active_deck().is_empty());
        assert_eq!(players.get_mut(0).unwrap().hand().len(), 2);
        assert_eq!(round.active_player_id(), 0);
    }

    #[test]
    fn test_proceed_round_quad() {
        let mut dealer = Dealer::new();
        let mut round = Round::new(0);

        let player_1 = Player::new(0);
        let player_2 = Player::new(1);
        let mut players = vec![player_1, player_2];
        round.play_card(Card::new(Suit::Hearts, Rank::Four));
        round.play_card(Card::new(Suit::Diamonds, Rank::Four));
        round.play_card(Card::new(Suit::Spades, Rank::Four));

        players.get_mut(0).unwrap().take_cards(&mut vec![
            Card::new(Suit::Clubs, Rank::Four),
            Card::new(Suit::Clubs, Rank::Ten),
        ]);
        players.get_mut(1).unwrap().take_cards(&mut vec![
            Card::new(Suit::Diamonds, Rank::Queen),
            Card::new(Suit::Hearts, Rank::Two),
        ]);

        round.proceed_round(&mut dealer, &mut players, Action::Four);
        assert!(round.active_deck().is_empty());
        assert_eq!(players.get_mut(0).unwrap().hand().len(), 2);
        assert_eq!(round.active_player_id(), 0);
    }
}
