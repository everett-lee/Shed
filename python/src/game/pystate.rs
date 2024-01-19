use pyo3::prelude::*;

use crate::game::pycard::PyCard;

#[pyclass(get_all)]
#[derive(Clone)]
pub struct PyState {
    pub legal_actions: Vec<String>,
    pub hand: Vec<PyCard>,
    pub live_deck: Vec<PyCard>,
    pub live_deck_size: u32,
    pub top_card: String,
    pub top_card_count: u32,
    pub position: u32,
    pub current_player: u32,
    pub unplayed_deck_size: u32
}

#[pymethods]
impl PyState {
    #[new]
    pub fn new(
        legal_actions: Vec<String>,
        hand: Vec<PyCard>,
        live_deck: Vec<PyCard>,
        live_deck_size: u32,
        top_card: String,
        top_card_count: u32,
        position: u32,
        current_player: u32,
        unplayed_deck_size: u32
    ) -> Self {
        return Self{
            legal_actions, 
            hand, 
            live_deck,
            live_deck_size, 
            top_card, 
            top_card_count,
            position, 
            current_player, 
            unplayed_deck_size, 
        }
    } 
}