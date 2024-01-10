
pub mod game;
use std::vec;

pub use crate::game::card::{Card, Suit, Rank};


fn main() {
    println!("Hello, world!");
    let c = Card::new(Suit::Clubs, Rank::Jack);
    let d = Card::new(Suit::Hearts, Rank::Three);
    
    let card_vec = vec![c, d];
    let bools: Vec<bool> = card_vec.iter().map(|el| el.is_magic_card()).collect();
    
    for b in bools {
        println!("{}", b)
    }

}


