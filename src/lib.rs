pub mod game;

pub use crate::game::card::{Card, Rank, Suit};
use crate::game::game::Game;
use pyo3::prelude::*;
use pyo3::{types::PyModule, Python};

#[pymodule]
fn rust_shed(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Game>()?;
    Ok(())
}
