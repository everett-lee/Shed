use pyo3::prelude::*;

#[pyclass]
pub struct PyCard {
    suit: String,
    rank: String
}

#[pymethods]
impl PyCard {
    #[new]
    pub fn new(suit: String, rank: String) -> Self {
        return Self{suit, rank}
    } 
}