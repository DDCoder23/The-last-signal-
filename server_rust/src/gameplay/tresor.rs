use rand::Rng;
use sqlx::SqlitePool;
use std::collections::HashMap;
use log::debug;
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
    pub seuil_artefact_peu_commun: HashMap<u32, u32>,
    pub sous_loot: HashMap<String, HashMap<String, f64>>,
    
    pub sous_loot_livre_normal: HashMap<String, f64>,
    pub sous_loot_livre_admin: HashMap<String, f64>,
    

    
}

impl Tresor {
    pub fn new() -> Self {
        let mut rng = rand::rng();

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
        loot_par_niveau.insert(
            6,
            Loot {
                commun: 2,
                peu_commun: 1,
                rare: 0,
                super_rare: 0,
                epique: 0,
                legendaire: 0,
                admin: 2,
            },
        );
        loot_par_niveau.insert(
            7,
            Loot {
                commun: 2,
                peu_commun: 1,
                rare: 0,
                super_rare: 0,
                epique: 0,
                legendaire: 0,
                admin: 2,
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
        let mut niveau_6 = HashMap::new();

        niveau_6.insert(
            "argent".to_string(),
            jet_de_des(6, 4) * 10 * PA,
        );

        if jet_de_des(20, 1) >= 8 {
            niveau_6.insert("gemmes".to_string(), 1);
        }

        objets_garantis.insert(6, niveau_6);
        let mut niveau_7 = HashMap::new();

        niveau_7.insert(
            "argent".to_string(),
            jet_de_des(6, 5) * 10 * PA,
        );

        if jet_de_des(20, 1) >= 6 {
            niveau_7.insert("gemmes".to_string(), 1);
        }

        objets_garantis.insert(7, niveau_7);

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
    (5, 15),
    (6, 15),
    (7, 14),       
]);
        let seuil_artefact_peu_commun: HashMap<u32, u32> = HashMap::from([
    (6, 20),
    (7, 19),

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
            seuil_artefact_peu_commun,
            sous_loot_livre_normal,
            sous_loot_livre_admin, 
        
        }
    }
    
      pub async fn ouvrir(
    &mut self,
    pool: &SqlitePool,
    account_id: i64,
    niveau: u32,
    is_admin: bool,
) -> Result<HashMap<String, u32>, sqlx::Error> {
    let mut rng = rand::rng();

    let loot = self
        .loot_par_niveau
        .get(&niveau)
        .cloned()
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

    // ==========================================
    // OBJETS COMMUNS
    // ==========================================

    for _ in 0..loot.commun {
        let seuil = self
            .seuil_artefact_commun
            .get(&niveau)
            .copied()
            .unwrap_or(20);

        let jet = rng.random_range(1..=20);

        if jet >= seuil {
            let objet = self
                .tirer_objet(
                    pool,
                    account_id,
                    "Artefact commun",
                    &mut rng,
                    is_admin,
                )
                .await?;

            let quantite = self
                .quantite_objets
                .get(&objet)
                .copied()
                .unwrap_or(1);

            *objets.entry(objet).or_insert(0) += quantite;
        }
    }

    // ==========================================
    // LOOT ADMIN
    // ==========================================

    if is_admin {
        for _ in 0..loot.admin {
            let objet = self
                .tirer_objet(
                    pool,
                    account_id,
                    "Artefact admin",
                    &mut rng,
                    is_admin,
                )
                .await?;

            let quantite = self
                .quantite_objets
                .get(&objet)
                .copied()
                .unwrap_or(1);

            *objets.entry(objet).or_insert(0) += quantite;
        }
    }

    Ok(objets)
                }  
            
        
            

        

            
    

            
        pub fn tirer_pondere(
    table: &HashMap<String, f64>,
    rng: &mut impl Rng,
) -> String {
    let total: f64 = table.values().sum();

    if total <= 0.0 {
        panic!("Table de loot vide");
    }

    let tirage = rng.random_range(0.0..total);

    let mut cumul = 0.0;

    for (objet, poids) in table {
        cumul += poids;

        if tirage < cumul {
            return objet.clone();
        }
    }

    unreachable!("Le tirage n'a trouvé aucun résultat")
}
pub fn cle_echec(categorie: &str, objet: &str) -> String {
    format!("{}::{}", categorie, objet)
}
    pub async fn tirer_objet(
    &mut self,
    pool: &SqlitePool,
    account_id: i64,
    categorie: &str,
    rng: &mut impl Rng,
    is_admin: bool,
) -> Result<String, sqlx::Error> {

    let mut categorie_actuelle = categorie.to_string();

    loop {
        // ==========================================
        // RÉCUPÉRATION DE LA TABLE
        // ==========================================

        let table_originale = self
            .sous_loot
            .get(&categorie_actuelle)
            .cloned()
            .unwrap_or_else(|| {
                panic!(
                    "Catégorie de loot inconnue : {:?}",
                    categorie_actuelle
                );
            });

        let total: f64 = table_originale.values().sum();

        if total <= 0.0 {
            panic!("Table de loot vide");
        }

        // ==========================================
        // CALCUL DES POIDS AVEC LE PITY SYSTEM
        // ==========================================

        let mut table_ajustee = HashMap::new();

        for (objet, poids) in &table_originale {
            let probabilite = poids / total;

            let echecs: i64 = sqlx::query_scalar(
                r#"
                SELECT nombre
                FROM echecs
                WHERE account_id = ?
                  AND categorie = ?
                  AND objet = ?
                "#,
            )
            .bind(account_id)
            .bind(&categorie_actuelle)
            .bind(objet)
            .fetch_optional(pool)
            .await?
            .unwrap_or(0);

            /*
             * PITY :
             *
             * Un objet dont la probabilité originale
             * est strictement inférieure à 3 % bénéficie
             * du bonus.
             *
             * +7,5 % du poids original par échec.
             */
            let poids_ajuste = if probabilite < 0.03 {
                *poids * (1.0 + 0.075 * echecs as f64)
            } else {
                *poids
            };

            table_ajustee.insert(
                objet.clone(),
                poids_ajuste,
            );
        }

        // ==========================================
        // TIRAGE
        // ==========================================

        let resultat = Self::tirer_pondere(
            &table_ajustee,
            rng,
        );

        // ==========================================
        // MISE À JOUR DES ÉCHECS
        // ==========================================

        for (objet, poids) in &table_originale {
            let probabilite = poids / total;

            // Le pity ne concerne que les objets < 3 %
            if probabilite >= 0.03 {
                continue;
            }

            if objet == &resultat {
                // ----------------------------------
                // OBJET OBTENU → RESET
                // ----------------------------------

                sqlx::query(
                    r#"
                    INSERT INTO echecs (
                        account_id,
                        categorie,
                        objet,
                        nombre
                    )
                    VALUES (?, ?, ?, 0)

                    ON CONFLICT (
                        account_id,
                        categorie,
                        objet
                    )
                    DO UPDATE SET
                        nombre = 0
                    "#,
                )
                .bind(account_id)
                .bind(&categorie_actuelle)
                .bind(objet)
                .execute(pool)
                .await?;

            } else {
                // ----------------------------------
                // OBJET NON OBTENU → +1 ÉCHEC
                // ----------------------------------

                sqlx::query(
                    r#"
                    INSERT INTO echecs (
                        account_id,
                        categorie,
                        objet,
                        nombre
                    )
                    VALUES (?, ?, ?, 1)

                    ON CONFLICT (
                        account_id,
                        categorie,
                        objet
                    )
                    DO UPDATE SET
                        nombre = nombre + 1
                    "#,
                )
                .bind(account_id)
                .bind(&categorie_actuelle)
                .bind(objet)
                .execute(pool)
                .await?;
            }
        }

        // ==========================================
        // LIVRE ENCHANTÉ
        // ==========================================

        if resultat == "livre enchant" {
            return self
                .tirer_livre(
                    pool,
                    account_id,
                    rng,
                    is_admin,
                )
                .await;
        }

        // ==========================================
        // SOUS-CATÉGORIE
        // ==========================================

        if self.sous_loot.contains_key(&resultat) {
            categorie_actuelle = resultat;
            continue;
        }

        // ==========================================
        // OBJET FINAL
        // ==========================================

        return Ok(resultat);
    }
    }
    pub async fn tirer_livre(
    &mut self,
    pool: &SqlitePool,
    account_id: i64,
    rng: &mut impl Rng,
    is_admin: bool,
) -> Result<String, sqlx::Error> {

    let categorie = if is_admin {
        "livre enchant admin"
    } else {
        "livre enchant normal"
    };

    let table_originale = if is_admin {
        self.sous_loot_livre_admin.clone()
    } else {
        self.sous_loot_livre_normal.clone()
    };

    let total: f64 = table_originale.values().sum();

    if total <= 0.0 {
        panic!("Table de loot des livres vide");
    }

    // ==========================================
    // CALCUL DES POIDS AVEC PITY
    // ==========================================

    let mut table_ajustee = HashMap::new();

    for (objet, poids) in &table_originale {
        let probabilite = poids / total;

        let echecs: i64 = sqlx::query_scalar(
            r#"
            SELECT nombre
            FROM echecs
            WHERE account_id = ?
              AND categorie = ?
              AND objet = ?
            "#,
        )
        .bind(account_id)
        .bind(categorie)
        .bind(objet)
        .fetch_optional(pool)
        .await?
        .unwrap_or(0);

        /*
         * Seuls les livres ayant une probabilité
         * originale < 3 % bénéficient du pity.
         
         */

        let poids_ajuste = if probabilite < 0.03 {
            *poids * (1.0 + 0.075 * echecs as f64)
        } else {
            *poids
        };

        table_ajustee.insert(
            objet.clone(),
            poids_ajuste,
        );
    }

    // ==========================================
    // TIRAGE
    // ==========================================

    let resultat = Self::tirer_pondere(
        &table_ajustee,
        rng,
    );

    // ==========================================
    // MISE À JOUR DES ÉCHECS
    // ==========================================

    for (objet, poids) in &table_originale {
        let probabilite = poids / total;

        // Pas de pity pour les objets >= 1 %
        if probabilite >= 0.03 {
            continue;
        }

        if objet == &resultat {
            // ----------------------------------
            // OBTENU → RESET
            // ----------------------------------

            sqlx::query(
                r#"
                INSERT INTO echecs (
                    account_id,
                    categorie,
                    objet,
                    nombre
                )
                VALUES (?, ?, ?, 0)

                ON CONFLICT (
                    account_id,
                    categorie,
                    objet
                )
                DO UPDATE SET
                    nombre = 0
                "#,
            )
            .bind(account_id)
            .bind(categorie)
            .bind(objet)
            .execute(pool)
            .await?;

        } else {
            // ----------------------------------
            // PAS OBTENU → +1
            // ----------------------------------

            sqlx::query(
                r#"
                INSERT INTO echecs (
                    account_id,
                    categorie,
                    objet,
                    nombre
                )
                VALUES (?, ?, ?, 1)

                ON CONFLICT (
                    account_id,
                    categorie,
                    objet
                )
                DO UPDATE SET
                    nombre = nombre + 1
                "#,
            )
            .bind(account_id)
            .bind(categorie)
            .bind(objet)
            .execute(pool)
            .await?;
        }
    }

    Ok(resultat)
    }

    

        

    
    
        
    
      }
