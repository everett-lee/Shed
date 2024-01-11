use crate::{Card, Suit, Rank};

#[derive(Debug)]
pub struct Player {
    player_id: u32,
    hand: Vec<Card>,
}

impl Player {
    pub fn new(player_id: u32) -> Self {
        let hand: Vec<Card> = vec![];
        Self { player_id, hand }
    }

    pub fn take_cards(&mut self, new_cards: &mut Vec<Card>) {
        self.hand.append(new_cards);
    }


}