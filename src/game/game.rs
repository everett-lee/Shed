use std::str::FromStr;

use crate::game::action::Action;
use crate::game::dealer::Dealer;
use crate::game::player::Player;
use crate::game::round::Round;

use pyo3::prelude::*;

use crate::game::pycard::PyCard;

use super::pystate::PyState;

#[pyclass]
pub struct Game {
    num_starting_cards: u32,
    dealer: Dealer,
    round: Round,
    players: Vec<Player>,
    debug_mode: bool,
    game_pointer: u32,
}

#[pymethods]
impl Game {
    #[new]
    pub fn new(num_players: u32, debug_mode: bool) -> Self {
        return Game {
            num_starting_cards: 5,
            dealer: Dealer::new(),
            round: Round::new(0),
            players: (0..num_players).map(|id: u32| Player::new(id)).collect(),
            debug_mode: debug_mode,
            game_pointer: 0,
        };
    }

    pub fn init_game(&mut self) -> (PyState, u32) {
        self.dealer = Dealer::new();
        self.round = Round::new(0);
        self.players = (0..self.players.len() as u32)
            .map(|id: u32| Player::new(id))
            .collect();
        self.game_pointer = 0;

        for player in self.players.as_mut_slice() {
            for _ in 0..self.num_starting_cards {
                self.dealer.deal_card(player);
            }
        }

        (
            self.get_state(self.round.active_player_id()),
            self.round.active_player_id(),
        )
    }

    pub fn step(&mut self, action: String) -> (PyState, u32) {
        let parsed_action =
            Action::from_str(&action).expect("Provided action not a valid String representation");

        let next_active_player_id =
            self.round
                .proceed_round(&mut self.dealer, &mut self.players, parsed_action);
        self.game_pointer = next_active_player_id;

        (self.get_state(next_active_player_id), next_active_player_id)
    }

    pub fn get_num_players(&self) -> PyResult<u32> {
        Ok(self.players.len() as u32)
    }

    pub fn get_num_actions(&self) -> PyResult<u32> {
        Ok(14)
    }

    pub fn get_active_player_id(&self) -> PyResult<u32> {
        Ok(self.game_pointer)
    }

    pub fn get_position(&mut self, player_id: u32) -> u32 {
        let mut id_handsize: Vec<(u32, usize)> = self
            .players
            .iter()
            .map(|p| (p.player_id(), p.hand().len()))
            .collect();
        id_handsize.sort_by(|a, b| a.1.cmp(&b.1).reverse());
        id_handsize
            .iter()
            .map(|pair| pair.0)
            .position(|id| id == player_id)
            .expect("Player ID should be present") as u32
    }

    pub fn get_payoffs(&self) -> PyResult<Vec<u32>> {
        let winner_id = self
            .round
            .get_winner_id()
            .expect("Winner ID should be set when payoffs determined");
        let payoffs: Vec<u32> = self
            .players
            .iter()
            .map(|p| {
                let is_winner = p.player_id() == winner_id;
                match is_winner {
                    true => 1,
                    false => 0,
                }
            })
            .collect();
        Ok(payoffs)
    }

    pub fn get_legal_actions(&mut self) -> Vec<String> {
        let action_strings = self
            .round
            .get_legal_actions(&self.players, self.game_pointer)
            .iter()
            .map(|a| a.to_string())
            .collect();
        action_strings
    }

    pub fn is_over(&self) -> PyResult<bool> {
        for player in self.players.iter() {
            match player.hand().is_empty() {
                true => return Ok(true),
                false => (),
            }
        }
        Ok(false)
    }

    pub fn get_active_deck(&self) -> PyResult<Vec<PyCard>> {
        let mut out_vec = vec![];
        for c in self.round.active_deck().iter() {
            out_vec.push(PyCard::new(c.suit().to_string(), c.rank().to_string()));
        }

        Ok(out_vec)
    }

    pub fn get_state(&mut self, player_id: u32) -> PyState {
        let hand = self
            .players
            .get_mut(player_id as usize)
            .unwrap()
            .hand()
            .iter()
            .map(|c| PyCard::new(c.suit().to_string(), c.rank().to_string()))
            .collect();
        let live_deck = self
            .round
            .active_deck()
            .iter()
            .map(|c| PyCard::new(c.suit().to_string(), c.rank().to_string()))
            .collect();
        let live_deck_size = self.round.active_deck().len();
        let (top_card, top_card_count) = self.round.get_top_card_and_count();
        let current_player = self.round.active_player_id();
        let unplayed_deck_size = self.dealer.deck_size();

        PyState::new(
            self.get_legal_actions().clone(),
            hand,
            live_deck,
            live_deck_size as u32,
            top_card,
            top_card_count as u32,
            self.get_position(player_id),
            current_player,
            unplayed_deck_size as u32,
        )
    }
}
