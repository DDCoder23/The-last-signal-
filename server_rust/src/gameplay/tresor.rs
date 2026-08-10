use rand::Rng;
use std::collections::HashMap;

use crate::gameplay::dice::jet_de_des;

const PA: u32 = 1;
const PO: u32 = PA * 10;
const PP: u32 = PO * 10;

#[derive(Debug, Clone)]
pub struct Loot {
    pub commun: u32,
    pub peu_commun: u32,
    pub rare: u32,
    pub super_rare: u32,
    pub epique: u32,
    pub legendaire: u32,
    pub admin: u32,
}

#[derive(Debug, Clone)]
pub struct Tresor {
    
    pub loot_par_niveau: HashMap<u32, Loot>,

    pub objets_garantis: HashMap<u32, HashMap<String, u32>>,

    pub quantite_objets: HashMap<String, u32>,

    pub seuil_artefact_commun: HashMap<u32, u32>,

    pub sous_loot: HashMap<String, HashMap<String, f64>>,
    
    pub sous_loot_livre_normal: HashMap<String, f64>,
    pub sous_loot_livre_admin: HashMap<String, f64>,

    
}

impl Tresor {
    pub fn new() -> Self {
        let mut rng = rand::thread_rng();

        // -------------------------------------------------
        // LOOT PAR NIVEAU
        // -------------------------------------------------

        let mut loot_par_niveau = HashMap::new();

        loot_par_niveau.insert(
            1,
            Loot {
                commun: 0,
                peu_commun: 0,
                rare: 0,
                super_rare: 0,
                epique: 0,
                legendaire: 0,
                admin: 1,
            },
        );

        loot_par_niveau.insert(
            2,
            Loot {
                commun: 1,
                peu_commun: 0,
                rare: 0,
                super_rare: 0,
                epique: 0,
                legendaire: 0,
                admin: 1,
            },
        );

        loot_par_niveau.insert(
            3,
            Loot {
                commun: 1,
                peu_commun: 0,
                rare: 0,
                super_rare: 0,
                epique: 0,
                legendaire: 0,
                admin: 1,
            },
        );

        loot_par_niveau.insert(
            4,
            Loot {
                commun: 1,
                peu_commun: 0,
                rare: 0,
                super_rare: 0,
                epique: 0,
                legendaire: 0,
                admin: 1,
            },
        );

        loot_par_niveau.insert(
            5,
            Loot {
                commun: 1,
                peu_commun: 0,
                rare: 0,
                super_rare: 0,
                epique: 0,
                legendaire: 0,
                admin: 1,
            },
        );

        // -------------------------------------------------
        // OBJETS GARANTIS
        // -------------------------------------------------

        let mut objets_garantis = HashMap::new();

        // Niveau 1
        let mut niveau_1 = HashMap::new();

        niveau_1.insert(
            "argent".to_string(),
            jet_de_des(6, 2) * PA,
        );

        niveau_1.insert("torche".to_string(), 2);
        niveau_1.insert("sac".to_string(), 3);
        niveau_1.insert("épée de bois".to_string(), 3);

        // 1 chance sur 20 : gemme
        if jet_de_des(20, 1) >= 18 {
            niveau_1.insert("gemmes".to_string(), 1);
        }

        // 17 chances sur 20 : pain
        if jet_de_des(20, 1) >= 4 {
            niveau_1.insert(
                "pain".to_string(),
                rng.gen_range(3..=5),
            );
        }

        objets_garantis.insert(1, niveau_1);

        // Niveau 2
        let mut niveau_2 = HashMap::new();

        niveau_2.insert(
            "argent".to_string(),
            jet_de_des(6, 4) * PA,
        );

        niveau_2.insert("torche".to_string(), 1);
        niveau_2.insert("sac".to_string(), 2);
        niveau_2.insert("épée de pierre".to_string(), 1);

        if jet_de_des(20, 1) >= 16 {
            niveau_2.insert("gemmes".to_string(), 1);
        }

        objets_garantis.insert(2, niveau_2);

        // Niveau 3
        let mut niveau_3 = HashMap::new();

        niveau_3.insert(
            "argent".to_string(),
            jet_de_des(6, 1) * 10 * PA,
        );

        niveau_3.insert("torche".to_string(), 2);
        niveau_3.insert("sac".to_string(), 1);
        niveau_3.insert("épée de pierre".to_string(), 1);

        if jet_de_des(20, 1) >= 14 {
            niveau_3.insert("gemmes".to_string(), 1);
        }

        objets_garantis.insert(3, niveau_3);

        // Niveau 4
        let mut niveau_4 = HashMap::new();

        niveau_4.insert(
            "argent".to_string(),
            jet_de_des(6, 2) * 10 * PA,
        );

        if jet_de_des(20, 1) >= 12 {
            niveau_4.insert("gemmes".to_string(), 1);
        }

        objets_garantis.insert(4, niveau_4);

        // Niveau 5
        let mut niveau_5 = HashMap::new();

        niveau_5.insert(
            "argent".to_string(),
            jet_de_des(6, 3) * 10 * PA,
        );

        if jet_de_des(20, 1) >= 10 {
            niveau_5.insert("gemmes".to_string(), 1);
        }

        objets_garantis.insert(5, niveau_5);

        // -------------------------------------------------
        // QUANTITÉS DES OBJETS
        // -------------------------------------------------

        let mut quantite_objets = HashMap::new();

        for objet in [
            "cuivre",
            "fer",
            "lapiz",
            "or",
            "redstone",
            "netherite",
            "diamant",
            "balles",
            "carreau d'arbalète",
            "flèches communes",
            "flèches peu rares",
            "flèches rares",
            "flèches super rares",
            "flèches exotiques",
            "flèches épiques",
            "flèches légendaires",
        ] {
            quantite_objets.insert(
                objet.to_string(),
                rng.gen_range(2..=9),
            );
        }
        let mut sous_loot: HashMap<String, HashMap<String, f64>> =
    HashMap::new();
        sous_loot.insert(
    "Artefact commun".to_string(),
    HashMap::from([
        ("food".to_string(), 80.0),
        ("minerais".to_string(), 19.0),
        ("équi".to_string(), 1.0),
    ]),
);
        sous_loot.insert(
    "Artefact peu commun".to_string(),
    HashMap::from([
        ("food".to_string(), 50.0),
        ("minerais".to_string(), 40.0),
        ("équi".to_string(), 10.0),
    ]),
);
        sous_loot.insert(
    "Artefact rare".to_string(),
    HashMap::from([
        ("minerais".to_string(), 50.0),
        ("équi".to_string(), 25.0),
        ("potion".to_string(), 25.0),
    ]),
);
        sous_loot.insert(
    "food".to_string(),
    HashMap::from([
        ("viande".to_string(), 10.0),
        ("pain".to_string(), 70.0),
        ("fruit et légumes".to_string(), 10.0),
        ("herbes et racines".to_string(), 10.0),
    ]),
);
        sous_loot.insert(
    "Artefact super rare".to_string(),
    HashMap::from([
        ("potion".to_string(), 50.0),
        ("équi".to_string(), 40.0),
        ("minerais".to_string(), 9.9),
        ("livre enchant".to_string(), 0.1),
    ]),
);
        sous_loot.insert(
    "Artefact epique".to_string(),
    HashMap::from([
        ("potion".to_string(), 15.0),
        ("équi".to_string(), 75.0),
        ("livre enchant".to_string(), 10.0),
        
    ]),
);
        sous_loot.insert(
    "Artefact legendaire".to_string(),
    HashMap::from([
        ("potion".to_string(), 5.0),
        ("équi".to_string(), 75.0),
        ("livre enchant".to_string(), 20.0),
        
    ]),
);
        sous_loot.insert(
    "Artefact admin".to_string(),
    HashMap::from([
        ("livre enchant".to_string(), 100.0),
        
    ]),
);
            

            
        let seuil_artefact_commun: HashMap<u32, u32> = HashMap::from([
    (2, 20),
    (3, 19),
    (4, 17),
]);
        let sous_loot_livre_normal = HashMap::from([
    ("livre enchant niv 1".to_string(), 70.0),
    ("livre enchant niv 2".to_string(), 20.0),
    ("livre enchant niv 3".to_string(), 5.0),
    ("livre enchant niv 4".to_string(), 3.0),
    ("livre enchant niv 5".to_string(), 1.5),
    ("livre enchant niv 6".to_string(), 0.5),
]);

let sous_loot_livre_admin = HashMap::from([
    ("livre enchant niv 1".to_string(), 45.0),
    ("livre enchant niv 2".to_string(), 15.0),
    ("livre enchant niv 3".to_string(), 13.0),
    ("livre enchant niv 4".to_string(), 12.0),
    ("livre enchant niv 5".to_string(), 8.0),
    ("livre enchant niv 6".to_string(), 7.0),
]);

        Self {
            loot_par_niveau,
            objets_garantis,
            quantite_objets,
            sous_loot,
            seuil_artefact_commun,
            sous_loot_livre_normal,
            sous_loot_livre_admin, 
        }
    }
    pub fn ouvrir(
    &self,
    niveau: u32,
    is_admin: bool,
) -> HashMap<String, u32> {
    let mut rng = rand::thread_rng();

    let loot = self
        .loot_par_niveau
        .get(&niveau)
        .expect("Niveau de coffre invalide");

    let mut objets = HashMap::new();
    

    // ==========================================
    // OBJETS GARANTIS
    // ==========================================

    if let Some(garantis) = self.objets_garantis.get(&niveau) {
        for (objet, quantite) in garantis {
            *objets.entry(objet.clone()).or_insert(0) += *quantite;
        }
    }
        

    // Objets communs
    for _ in 0..loot.commun {
        let seuil = self
            .seuil_artefact_commun
            .get(&niveau)
            .copied()
            .unwrap_or(20);

        let jet = rng.gen_range(1..=20);

        if jet >= seuil {
            let objet = self.tirer_objet(
                "Artefact commun",
                &mut rng,
                is_admin
            );

            let quantite = self
                .quantite_objets
                .get(&objet)
                .copied()
                .unwrap_or(1);

            *objets.entry(objet).or_insert(0) += quantite;
        }
    }

    // Loot admin
    if is_admin {
        for _ in 0..loot.admin {
            let objet = self.tirer_objet(
                "Artefact admin",
                &mut rng,
                is_admin
            );

            let quantite = self
                .quantite_objets
                .get(&objet)
                .copied()
                .unwrap_or(1);

            *objets.entry(objet).or_insert(0) += quantite;
        }
    }

    objets
    }

    pub fn tirer_pondere(
    table: &HashMap<String, f64>,
    rng: &mut impl Rng,
) -> String {
    let total: f64 = table.values().sum();

    if total <= 0.0 {
        panic!("Table de loot vide");
    }

    let tirage = rng.gen_range(0.0..total);

    let mut cumul = 0.0;

    for (objet, poids) in table {
        cumul += poids;

        if tirage < cumul {
            return objet.clone();
        }
    }

    unreachable!("Le tirage n'a trouvé aucun résultat")
    }
    pub fn tirer_objet(
    &self,
    categorie: &str,
    rng: &mut impl Rng,
    is_admin: bool,
) -> String {
    let table = if categorie == "livre enchant" {
        if is_admin {
            &self.sous_loot_livre_admin
        } else {
            &self.sous_loot_livre_normal
        }
    } else {
        self
            .sous_loot
            .get(categorie)
            .unwrap_or_else(|| {
        panic!("Catégorie de loot inconnue : {:?}", categorie);
    })
    };

    let resultat = Self::tirer_pondere(
        table,
        rng,
        
    );

    if self.sous_loot.contains_key(&resultat) {
        return self.tirer_objet(
            &resultat,
            rng,
            is_admin
        );
    }

    resultat
    }
      }
