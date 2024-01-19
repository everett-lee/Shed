use pyo3::prelude::*;
use serde::Serialize;
use serde_json::Result;

#[pyclass(get_all)]
#[derive(Clone, Serialize)]
pub struct PyCard {
    pub suit: String,
    pub rank: String
}

#[pymethods]
impl PyCard {
    #[new]
    pub fn new(suit: String, rank: String) -> Self {
        return Self{suit, rank}
    } 

    pub fn get_index(&self) -> String {
        format!("{}{}", self.suit, self.rank)
    }
}