pub mod game;

pub use crate::game::card::{Card, Rank, Suit};

mod shed {
    use pyo3::{Python, types::PyModule, PyResult};

    use crate::game::game::Game;

    fn shed(_py: Python, m: &PyModule) -> PyResult<()> {
        m.add_class::<Game>()?;
        Ok(())
    }
}