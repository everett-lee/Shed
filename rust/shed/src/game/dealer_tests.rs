#[cfg(test)]
mod dealer_tests {

    use crate::game::{dealer::*, player::Player};

    #[test]
    fn test_card_equals() {
        let dealer = Dealer::new();
        assert_eq!(dealer.deck().len(), 52);
        assert_eq!(dealer.deck_size(), 52);
    }

    #[test]
    fn test_deal_card_to_two() {
        let mut dealer = Dealer::new();
        let mut p1 = Player::new(0);
        let mut p2 = Player::new(1);

        dealer.deal_card(&mut p1);
        dealer.deal_card(&mut p2);
        dealer.deal_card(&mut p2);

        assert_eq!(p1.hand().len(), 1);
        assert_eq!(p2.hand().len(), 2);
        assert_eq!(dealer.deck_size(), 49);
    }

    #[test]
    fn test_max_cards_dealt() {
        let mut dealer = Dealer::new();
        let mut player = Player::new(0);
        for _ in 0..60 {
            dealer.deal_card(&mut player);
        }
        assert_eq!(player.hand().len(), 52);
    }
}
