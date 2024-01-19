use pyo3::prelude::*;

#[pyclass(get_all)]
#[derive(Clone)]
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