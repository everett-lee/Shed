use crate::{Card, Suit, Rank};

use super::action::Action;



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

    pub fn hand(&self) -> &Vec<Card> {
        &self.hand
    }

    pub fn take_cards(&mut self, new_cards: &mut Vec<Card>) {
        self.hand.append(new_cards);
    }

    pub fn player_id(&self) -> u32 {
        self.player_id
    } 

    pub fn play_card(&mut self, action: Action) -> Card {
        let action_card = action.to_card().unwrap();
        let matching_card_index = self.hand.iter().position(|card| *card == action_card)
            .expect("No matching card matching action present in hand");
        self.hand.swap_remove(matching_card_index)
    }

}