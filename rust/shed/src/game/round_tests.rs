#[cfg(test)]
mod round_tests {
    

    use crate::{
        game::{dealer::Dealer, player::Player, round::Round},
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
    fn delete_me() {
        let a = vec![1, 2, 3, 4];
        for el in a[0..4].into_iter().rev() {
            println!("{el}");
        }
        println!("{}", a.get(0).unwrap());
    }
}
