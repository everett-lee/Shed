use crate::game::card::Card;
use crate::game::action::Action;
use crate::game::dealer::Dealer;
use crate::game::player::Player;
use crate::game::round::Round;

#[derive(Debug)]
pub struct Game {
    allow_step_back: bool,
    num_starting_cards: u32,
    dealer: Dealer,
    round: Round,
    players: Vec<Player>,
    debug_mode: bool,
    game_pointer: u32,
}

impl Game {
    pub fn new(num_players: u32, debug_mode: Option<bool>) -> Self {
        return Game {
            allow_step_back: false,
            num_starting_cards: 5,
            dealer: Dealer::new(),
            round: Round::new(0),
            players: (0..num_players).map(|id: u32| Player::new(id)).collect(),
            debug_mode: debug_mode.unwrap_or_else(|| false),
            game_pointer: 0,
        };
    }

    pub fn init_game(&mut self) {
        let players = self.players.as_mut_slice();

        for player in players {
            for _ in 0..self.num_starting_cards {
                self.dealer.deal_card(player);
            }
        }

        // return game state and pointer
    }

    pub fn step(&mut self, action: Action) {
        let next_active_player_id =
            self.round
                .proceed_round(&mut self.dealer, &mut self.players, action);
        self.game_pointer = next_active_player_id;

        let next_player = self
            .players
            .get_mut(next_active_player_id as usize)
            .expect("The Player with next active player ID should be present in Players");
        // let next_state = self.get_state...
    }

    pub fn get_num_players(&self) -> u32 {
        self.players.len() as u32
    }

    pub fn get_num_actions(&self) -> u32 {
        14
    }

    pub fn get_player_id(&self) -> u32 {
        self.game_pointer
    }

    pub fn get_positions(&mut self) -> Vec<u32> {
        let mut id_handsize: Vec<(u32, usize)> = self
            .players
            .iter()
            .map(|p| (p.player_id(), p.hand().len()))
            .collect();
        id_handsize.sort_by(|a, b| a.1.cmp(&b.1).reverse());
        // Return the player ID or each sorted pair
        id_handsize.iter().map(|pair| pair.0).collect()
    }

    pub fn get_payoffs(&self) -> Vec<u32> {
        let winner_id = self
            .round
            .get_winner_id()
            .expect("Winner ID should be set when payoffs determined");
        self.players
            .iter()
            .map(|p| {
                let is_winner = p.player_id() == winner_id;
                match is_winner {
                    true => 1,
                    false => 0,
                }
            })
            .collect()
    }

    pub fn get_legal_actions(&mut self) -> Vec<Action> {
        self.round
            .get_legal_actions(&self.players, self.game_pointer)
    }

    pub fn is_over(&self) -> bool {
        for player in self.players.iter() {
            match player.hand().is_empty() {
                true => return true,
                false => (),
            }
        }
        false
    }

    pub fn get_active_deck(&self) -> &Vec<Card> {
        self.round.active_deck()
    }

    pub fn get_player(&self, player_id: usize) -> &Player {
        self.players.get(player_id).expect("Player with given ID should exist")
    }

    pub fn get_state(&self) {
        todo!()
    }
}
