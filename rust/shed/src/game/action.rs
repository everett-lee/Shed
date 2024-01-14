use strum_macros::{Display, EnumIter};

use crate::{Card, Rank, Suit};
use lazy_static::lazy_static;

use std::collections::HashMap;

lazy_static! {
    static ref ACTION_TO_CARD: HashMap<Action, Card> = {
        // all suits are equivalent
        let mut m = HashMap::new();
        m.insert(Action::Ace, Card::new(Suit::Spades, Rank::Ace));
        m.insert(Action::Two, Card::new(Suit::Spades, Rank::Two));
        m.insert(Action::Three, Card::new(Suit::Spades, Rank::Three));
        m.insert(Action::Four, Card::new(Suit::Spades, Rank::Four));
        m.insert(Action::Five, Card::new(Suit::Spades, Rank::Five));
        m.insert(Action::Six, Card::new(Suit::Spades, Rank::Six));
        m.insert(Action::Seven, Card::new(Suit::Spades, Rank::Seven));
        m.insert(Action::Eight, Card::new(Suit::Spades, Rank::Eight));
        m.insert(Action::Nine, Card::new(Suit::Spades, Rank::Nine));
        m.insert(Action::Ten, Card::new(Suit::Spades, Rank::Ten));
        m.insert(Action::Jack, Card::new(Suit::Spades, Rank::Jack));
        m.insert(Action::Queen, Card::new(Suit::Spades, Rank::Queen));
        m.insert(Action::King, Card::new(Suit::Spades, Rank::King));
        m
    };
}

#[derive(Ord, PartialOrd, Eq, PartialEq, Debug, Display, EnumIter, Copy, Clone, Hash)]
pub enum Action {
    Ace,
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    Jack,
    Queen,
    King,
    Pickup,
}

impl Action {
    pub fn to_card(&self) -> Card {
        // TODO do i need to clone?
        ACTION_TO_CARD
            .get(&self)
            .cloned()
            .expect("There should be a matching Card")
    }
}
