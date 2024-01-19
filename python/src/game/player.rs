use std::collections::HashSet;

use crate::Card;

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

    // TODO neede
    pub fn hand_to_actions(&self) -> Vec<Action> {
        let as_set: HashSet<Action> = self.hand().iter().map(|c| c.to_action()).collect();
        let mut as_vec = Vec::from_iter(as_set);
        as_vec.sort();
        as_vec
    }

    pub fn take_cards(&mut self, new_cards: &mut Vec<Card>) {
        self.hand.append(new_cards);
    }

    pub fn player_id(&self) -> u32 {
        self.player_id
    }

    pub fn play_card(&mut self, action: Action) -> Card {
        let action_card = action.to_card();
        let matching_card_index = self
            .hand
            .iter()
            .position(|card| card.rank() == action_card.rank())
            .expect(&format!("No matching card {}{} matching action present in hand {:?}", 
            action.to_card().suit(), action.to_card().rank(), self.hand));
        self.hand.swap_remove(matching_card_index)
    }
}
