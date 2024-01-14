pub mod game;

pub use crate::game::card::{Card, Rank, Suit};
use crate::game::{dealer::Dealer, game::Game, round::Round};

fn main() {
    println!("Hello, world!");
    let mut dealer = Dealer::new();
    let round = Round::new(0);
    let mut game = Game::new(2, Some(true));
    game.init_game();
}
