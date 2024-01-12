use crate::{game::{dealer::Dealer, player::Player}, Card};


#[derive(Debug)]
pub struct Round {
    dealer: Dealer,
    players: Vec<Player>, 
    active_player_id: u32,
    num_players: usize,
    active_deck: Vec<Card>,
    is_over: bool,
    winner: Option<Player>,
    min_hand_size: u32

}


impl Round {
    pub fn new(dealer: Dealer, players: Vec<Player>, active_player_id: u32) -> Round {
        let active_deck = vec![];
        let num_players = active_deck.len();
        Self {dealer, players, active_player_id, num_players, active_deck, is_over: false, winner: None, min_hand_size: 5 }
    }

    pub fn active_deck(&self) -> &Vec<Card> {
        &self.active_deck
    }

    pub fn play_card(&mut self, card: Card) {
        // TODO handle burn conditons 
        self.active_deck.push(card);

    }

    pub fn get_deck_no_threes(&self) -> Vec<Card> {
        self.active_deck.iter().filter(|c| !c.is_three()).cloned().collect()
    }


    // TODO refactor
    pub fn has_quad(&self) -> bool {
        let no_threes = self.get_deck_no_threes();
        let first_index = no_threes.len() as i32;
        let last_index = no_threes.len() as i32 - 4;

        if last_index < 0 {
            return false;
        }

        let mut dup_count = 0;
        let mut top_rank = match no_threes.last() {
            Some(c) => c.rank(), 
            _ => return false
        };

        for i in (last_index..first_index).rev() {
            let card = no_threes.get(i as usize).expect("Index should be valid");
            if card.rank() == top_rank {
                dup_count += 1;
            }
            top_rank = card.rank();
        }  

        match dup_count {
            4 => true,
            _ => false
        }
    } 

}