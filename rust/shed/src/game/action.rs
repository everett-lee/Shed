
#[derive(Eq, PartialEq, Debug, EnumIter, Copy, Clone, Hash)]
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
    Pickup
}