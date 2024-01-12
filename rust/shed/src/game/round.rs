use crate::game::{dealer::Dealer, player::Player};

use super::dealer;


#[derive(Debug)]
pub struct Round {
    dealer: Dealer,
    players: Vec<Player>,
}


impl Round {
    pub fn new(dealer: Dealer, players: Vec<Player>) -> Round {
        Self {dealer, players}
    }

}