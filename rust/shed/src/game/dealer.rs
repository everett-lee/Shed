use strum::IntoEnumIterator;
use rand::seq::SliceRandom;

use crate::{Card, Suit, Rank};

use crate::game::player::Player;

#[derive(Debug)]
pub struct Dealer {
    unplayed_deck: Vec<Card>,
}

impl Dealer {
    pub fn new() -> Self {
        // create 52 card deck
        let mut deck: Vec<Card> = Suit::iter()
        .map({|c| Rank::iter()
        .map(move |r| Card::new(c, r))})
        .flatten().collect();

        let mut rng = rand::thread_rng();
        deck.shuffle(&mut rng);

        Self { unplayed_deck: deck }
    }

    pub fn deck(&self) -> &Vec<Card> {
        &self.unplayed_deck
    }

    pub fn deck_size(&self) -> usize {
        self.unplayed_deck.len()
    }

    pub fn deal_card(&mut self, player: &mut Player) {
        let played_card_option = self.unplayed_deck.pop();
        match played_card_option {
            Some(card) => player.take_cards(&mut vec![card]),
            None => ()
        }
    }
    
}