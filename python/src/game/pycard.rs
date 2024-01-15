use pyo3::prelude::*;

#[pyclass]
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
    
    pub fn suit(&self) -> PyResult<String> {
        Ok(self.suit.clone())
    }

    pub fn rank(&self) -> PyResult<String> {
        Ok(self.rank.clone())
    }
}