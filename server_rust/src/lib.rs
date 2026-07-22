use pyo3::prelude::*;
use rand::Rng;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;

// Structure pour représenter les stats d'un personnage
#[derive(Debug, Serialize, Deserialize)]
pub struct Stats {
    pub for_stat: i32,
    pub dex: i32,
    pub con: i32,
    pub int: i32,
    pub sag: i32,
    pub cha: i32,
    pub mod_for: i32,
    pub mod_dex: i32,
    pub mod_con: i32,
    pub mod_int: i32,
    pub mod_sag: i32,
    pub mod_cha: i32,
    pub pv_max: i32,
    pub pv: i32,
    pub def: i32,
}

/// Calcule le modificateur en fonction d'une valeur
#[pyfunction]
pub fn get_modifier(value: i32) -> i32 {
    let modifiers = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
    let index = ((value - 1) / 2) as usize;
    if index < modifiers.len() {
        modifiers[index]
    } else {
        0
    }
}

/// Génère des stats aléatoires pour un personnage
#[pyfunction]
pub fn generer_stats() -> PyResult<Py<PyAny>> {
    let mut rng = rand::thread_rng();
    let mut valeurs = Vec::new();

    // Génère 6 stats (FOR, DEX, CON, INT, SAG, CHA)
    for _ in 0..6 {
        let mut rolls = [0; 4];
        for roll in &mut rolls {
            *roll = rng.gen_range(1..=6);
        }
        rolls.sort_by(|a, b| b.cmp(a)); // Tri décroissant
        valeurs.push(rolls[0..3].iter().sum::<i32>());
    }

    // Crée un dictionnaire pour les stats
    let stats_names = ["FOR", "DEX", "CON", "INT", "SAG", "CHA"];
    let mut stats = HashMap::new();

    for (i, &name) in stats_names.iter().enumerate() {
        stats.insert(name.to_string(), valeurs[i]);
    }

    // Ajoute les modificateurs
    for name in stats_names {
        let value = *stats.get(name).unwrap();
        let mod_value = get_modifier(value);
        stats.insert(format!("MOD_{}", name), mod_value);
    }

    // Ajoute PV_MAX, PV et DEF
    let con = *stats.get("CON").unwrap();
    let pv_max = (con / 2) + 12;
    stats.insert("PV_MAX".to_string(), pv_max);
    stats.insert("PV".to_string(), pv_max);

    let mod_dex = *stats.get("MOD_DEX").unwrap();
    stats.insert("DEF".to_string(), 10 + mod_dex);

    // Convertit le HashMap en dictionnaire Python
    let py = Python::acquire_gil();
    let py_dict = py.eval("{}", None, None)?.downcast::<PyDict>()?;
    for (key, value) in stats {
        py_dict.set_item(key, value)?;
    }

    Ok(py_dict.into())
}

/// Module Python
#[pymodule]
fn perso_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_modifier, m)?)?;
    m.add_function(wrap_pyfunction!(generer_stats, m)?)?;
    Ok(())
}
