use std::collections::HashSet;

use crate::{
    game::{dealer::Dealer, player::Player},
    Card, Rank,
};

use super::action::Action;

#[derive(Debug)]
pub struct Round {
    active_player_id: u32,
    active_deck: Vec<Card>,
    is_over: bool,
    winner_id: Option<u32>,
    min_hand_size: u32,
}

impl Round {
    pub fn new(active_player_id: u32) -> Round {
        let active_deck = vec![];
        Self {
            active_player_id,
            active_deck,
            is_over: false,
            winner_id: None,
            min_hand_size: 5,
        }
    }

    pub fn active_deck(&self) -> &Vec<Card> {
        &self.active_deck
    }

    pub fn active_player_id(&self) -> u32 {
        self.active_player_id
    }

    pub fn proceed_round(
        &mut self,
        dealer: &mut Dealer,
        players: &mut Vec<Player>,
        action: Action,
    ) -> u32 {
        let deck_burned = self.handle_action(dealer, players, &action);

        let player = players
            .get(self.active_player_id as usize)
            .expect("Player should be present with active player ID");

        if player.hand().is_empty() {
            self.is_over = true;
            self.winner_id = Some(player.player_id());
        }

        // When deck burned player goes again
        if !deck_burned {
            self.active_player_id = (self.active_player_id + 1) % players.len() as u32;
        }
        return self.active_player_id;
    }

    pub fn handle_action(
        &mut self,
        dealer: &mut Dealer,
        players: &mut Vec<Player>,
        action: &Action,
    ) -> bool {
        let player: &mut Player = players
            .get_mut(self.active_player_id as usize)
            .expect("Players should contain player with active player ID");

        if *action == Action::Pickup {
            player.take_cards(&mut self.active_deck.to_vec());
            self.active_deck.clear();
            return false;
        } else {
            let card = player.play_card(*action);
            let deck_burned = self.play_card(card);
            if player.hand().len() < self.min_hand_size as usize {
                dealer.deal_card(player);
            }
            return deck_burned;
        }
    }

    pub fn play_card(&mut self, card: Card) -> bool {
        if card.is_ten() {
            self.active_deck.clear();
            // Return true when deck burned, player plays again
            return true;
        }

        self.active_deck.push(card);

        if self.has_quad() {
            self.active_deck.clear();
            // Return true when deck burned, player plays again
            return true;
        }
        false
    }

    pub fn get_deck_no_threes(&self) -> Vec<Card> {
        self.active_deck
            .iter()
            .filter(|c| !c.is_three())
            .cloned()
            .collect()
    }

    pub fn is_legal_card(&self, card: &Card) -> bool {
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
            return card <= top_card;
        }

        // Standard comparison, great or equal value required
        card >= top_card
    }

    pub fn get_legal_actions(&mut self, players: &Vec<Player>, player_id: u32) -> Vec<Action> {
        let mut legal_actions: HashSet<Action> = players
            .get(player_id as usize)
            .expect("No player with givne player ID")
            .hand()
            .iter()
            .filter(|c| self.is_legal_card(c))
            .map(|c| c.to_action())
            .collect();

        // Only allow pickup when deck has cards
        if !self.active_deck.is_empty() {
            legal_actions.insert(Action::Pickup);
        }

        // HashSet to Iter to remove
        let mut as_vec = Vec::from_iter(legal_actions);
        as_vec.sort();
        as_vec
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
            4 => return true,
            _ => return false,
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

    pub fn get_winner_id(&self) -> Option<u32> {
        self.winner_id
    }
}
