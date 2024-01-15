pub mod game;

use pyo3::prelude::*;
use pyo3::{Python, types::PyModule};
pub use crate::game::card::{Card, Rank, Suit};
use crate::game::game::Game;

#[pymodule]
fn rust_shed(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Game>()?;
    Ok(())
}

