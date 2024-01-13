use crate::{
    game::{dealer::Dealer, player::Player},
    Card, Rank,
};

#[derive(Debug)]
pub struct Round {
    dealer: Dealer,
    players: Vec<Player>,
    active_player_id: u32,
    num_players: usize,
    active_deck: Vec<Card>,
    is_over: bool,
    winner: Option<Player>,
    min_hand_size: u32,
}

impl Round {
    pub fn new(dealer: Dealer, players: Vec<Player>, active_player_id: u32) -> Round {
        let active_deck = vec![];
        let num_players = active_deck.len();
        Self {
            dealer,
            players,
            active_player_id,
            num_players,
            active_deck,
            is_over: false,
            winner: None,
            min_hand_size: 5,
        }
    }

    pub fn active_deck(&self) -> &Vec<Card> {
        &self.active_deck
    }

    pub fn play_card(&mut self, card: Card) {
        // TODO handle burn conditons
        self.active_deck.push(card);
    }

    pub fn get_deck_no_threes(&self) -> Vec<Card> {
        self.active_deck
            .iter()
            .filter(|c| !c.is_three())
            .cloned()
            .collect()
    }

    pub fn is_legal_card(&self, card: Card) -> bool {
        let no_threes = self.get_deck_no_threes();

        let top_card_option = no_threes.last();
        if no_threes.is_empty() || card.is_magic_card() || top_card_option.is_none() {
            return true;
        }

        let top_card = top_card_option.unwrap();

        if top_card.is_ace() {
            return card.is_magic_card();
        }

        if top_card.is_seven() {
            return card <= *top_card;
        }

        // Standard comparison, great or equal value required
        card >= *top_card
    }

    // TODO refactor
    pub fn has_quad(&self) -> bool {
        let no_threes = self.get_deck_no_threes();
        let first_index = no_threes.len();
        let last_index = no_threes.len() as i32 - 4;

        if last_index < 0 {
            return false;
        }

        let mut dup_count = 0;
        let mut top_rank = match no_threes.last() {
            Some(c) => c.rank(),
            _ => return false,
        };

        for card in no_threes[last_index as usize..first_index]
            .into_iter()
            .rev()
        {
            if card.rank() == top_rank {
                dup_count += 1;
            }
            top_rank = card.rank();
        }

        match dup_count {
            4 => true,
            _ => false,
        }
    }

    pub fn get_top_card_rank_and_count(&self) -> (Option<Rank>, u32) {
        let no_threes = self.get_deck_no_threes();

        let top_rank = match no_threes.last() {
            Some(c) => c.rank(),
            _ => return (None, 0),
        };
        let mut count = 0;
        for card in no_threes.iter().rev() {
            if card.rank() == top_rank {
                count += 1;
            } else {
                return (Some(top_rank.clone()), count);
            }
        }
        (None, 0)
    }
}
