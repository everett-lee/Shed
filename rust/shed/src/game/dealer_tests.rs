#[cfg(test)]
mod dealer_tests {
    use std::collections::HashSet;

    use crate::{game::dealer::*, Card};

    #[test]
    fn test_card_equals() {
        let dealer = Dealer::new();
        let deck_as_set: HashSet<&Card> = dealer.deck().into_iter().collect();
        assert_eq!(deck_as_set.len(), 52);
        assert_eq!(deck_as_set.len(), dealer.deck_size());
    }

    #[test]
    fn test_deal_card() {
        let mut dealer = Dealer::new();

        for _ in 0..3 {
            let c = dealer.deal_card().unwrap();
            println!("{}", c)
        }
        println!("{}", dealer.deck().len())
    }
}