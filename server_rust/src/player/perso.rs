use serde::{Serialize, Deserialize};
use crate::dice::{jet_de_des};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Stats {
    pub for: u32,
    pub dex: u32,
    pub con: u32,
    pub int: u32,
    pub sag: u32,
    pub cha: u32,
    pub mod_for: i32,
    pub mod_dex: i32,
    pub mod_con: i32,
    pub mod_int: i32,
    pub mod_sag: i32,
    pub mod_cha: i32,
    pub pv_max: u32,
    pub pv: u32,
    pub def: u32,
}

impl Stats {
    pub fn new() -> Self {
        Self::default()
    }

    // Équivalent de `get_modifier` en Python
    pub fn get_modifier(value: u32) -> i32 {
        let modifiers = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
        let index = ((value as i32) - 1) / 2;
        if index >= 0 && (index as usize) < modifiers.len() {
            modifiers[index as usize]
        } else {
            0
        }
    }

    // Génère les stats aléatoires (équivalent de `generer_stats`)
    pub fn generer_stats() -> Self {
        let mut valeurs = [0; 6];
        for i in 0..6 {
            // Lance 4d6, garde les 3 meilleurs
            let mut jets: Vec<u32> = (0..4).map(|_| jet_de_des(6, 1)).collect();
            jets.sort_by(|a, b| b.cmp(a)); // Tri décroissant
            valeurs[i] = jets[0] + jets[1] + jets[2]; // Somme des 3 meilleurs
        }

        let [for_, dex, con, int, sag, cha] = valeurs;
        let mod_for = Self::get_modifier(for_);
        let mod_dex = Self::get_modifier(dex);
        let mod_con = Self::get_modifier(con);
        let mod_int = Self::get_modifier(int);
        let mod_sag = Self::get_modifier(sag);
        let mod_cha = Self::get_modifier(cha);

        Self {
            for_,
            dex,
            con,
            int,
            sag,
            cha,
            mod_for,
            mod_dex,
            mod_con,
            mod_int,
            mod_sag,
            mod_cha,
            pv_max: (con / 2) + 12,
            pv: (con / 2) + 12,
            def: 10 + mod_dex,
        }
    }
}

impl Default for Stats {
    fn default() -> Self {
        Self {
            for_: 10,
            dex: 10,
            con: 10,
            int: 10,
            sag: 10,
            cha: 10,
            mod_for: 0,
            mod_dex: 0,
            mod_con: 0,
            mod_int: 0,
            mod_sag: 0,
            mod_cha: 0,
            pv_max: 16,
            pv: 16,
            def: 10,
        }
    }
}
