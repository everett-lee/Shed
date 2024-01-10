use std::{
    cmp::Ordering,
    fmt::{self},
};

#[derive(Eq, PartialEq, Debug)]
pub enum Suit {
    Clubs,
    Diamonds,
    Hearts,
    Spades,
}

#[derive(Eq, PartialEq, Debug)]
pub enum Rank {
    Ace,
    One,
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
}

impl fmt::Display for Suit {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Suit::Clubs => write!(f, "C"),
            Suit::Diamonds => write!(f, "D"),
            Suit::Hearts => write!(f, "H"),
            Suit::Spades => write!(f, "S"),
        }
    }
}

impl fmt::Display for Rank {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Rank::Ace => write!(f, "A"),
            Rank::One => write!(f, "1"),
            Rank::Two => write!(f, "2"),
            Rank::Three => write!(f, "3"),
            Rank::Four => write!(f, "4"),
            Rank::Five => write!(f, "5"),
            Rank::Six => write!(f, "6"),
            Rank::Seven => write!(f, "7"),
            Rank::Eight => write!(f, "8"),
            Rank::Nine => write!(f, "9"),
            Rank::Ten => write!(f, "T"),
            Rank::Jack => write!(f, "J"),
            Rank::Queen => write!(f, "Q"),
            Rank::King => write!(f, "K"),
        }
    }
}

#[derive(Eq, Debug)]
pub struct Card {
    suit: Suit,
    rank: Rank,
}

impl Card {
    pub fn new(suit: Suit, rank: Rank) -> Self {
        Self { suit, rank }
    }

    pub fn suit(&self) -> &Suit {
        return &self.suit;
    }

    pub fn rank(&self) -> &Rank {
        return &self.rank;
    }

    pub fn get_index(&self) -> String {
        return format!("{}{}", self.suit, self.rank);
    }

    pub fn is_ace(&self) -> bool {
        return self.rank == Rank::Ace;
    }

    pub fn is_ten(&self) -> bool {
        return self.rank == Rank::Ten;
    }

    pub fn is_seven(&self) -> bool {
        return self.rank == Rank::Seven;
    }

    pub fn is_three(&self) -> bool {
        return self.rank == Rank::Three;
    }

    pub fn is_magic_card(&self) -> bool {
        return self.is_ace() || self.is_three() || self.is_seven() || self.is_ten();
    }

    pub fn value(&self) -> u16 {
        match &self.rank {
            Rank::One => 1,
            Rank::Two => 2,
            Rank::Three => 3,
            Rank::Four => 4,
            Rank::Five => 5,
            Rank::Six => 6,
            Rank::Seven => 7,
            Rank::Eight => 8,
            Rank::Nine => 9,
            Rank::Ten => 10,
            Rank::Jack => 11,
            Rank::Queen => 12,
            Rank::King => 13,
            Rank::Ace => 14,
        }
    }
}

impl fmt::Display for Card {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.get_index())
    }
}

impl PartialOrd for Card {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        if self.lt(other) {
            return Some(Ordering::Less);
        };
        if self.le(other) {
            return Some(Ordering::Equal);
        };
        if self.ge(other) {
            return Some(Ordering::Equal);
        };
        if self.gt(other) {
            return Some(Ordering::Greater);
        };
        return None;
    }

    fn lt(&self, other: &Self) -> bool {
        if other.is_ace() && !self.is_magic_card() {
            return true;
        };
        return self.value().lt(&other.value());
    }

    fn le(&self, other: &Self) -> bool {
        return self.eq(other) || self.lt(other);
    }

    fn gt(&self, other: &Self) -> bool {
        if self.is_ace() {
            return true;
        };
        return self.value().gt(&other.value());
    }

    fn ge(&self, other: &Self) -> bool {
        return self.eq(other) || self.gt(other);
    }
}

impl PartialEq for Card {
    fn eq(&self, other: &Self) -> bool {
        self.rank == other.rank
    }
}
