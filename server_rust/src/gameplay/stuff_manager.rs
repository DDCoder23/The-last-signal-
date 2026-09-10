use sqlx::SqlitePool;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use log::{debug, error, info};

use crate::gameplay::objets::{Objet, TypeObjet, NomAffiche, AjouterRetirer, Equipement, Arme, Potion, Livre};

// ============================================================
// ENUM UNIFIÉ POUR LE HASHMAP D'INVENTAIRE
// ============================================================

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum ObjetInventaire {
    Base(Objet),
    Equipement(Equipement),
    Arme(Arme),
    Potion(Potion),
    Livre(Livre),
}

impl NomAffiche for ObjetInventaire {
    fn nom_affiche(&self) -> String {
        match self {
            ObjetInventaire::Base(o) => o.nom_affiche(),
            ObjetInventaire::Equipement(e) => e.nom_affiche(),
            ObjetInventaire::Arme(a) => a.nom_affiche(),
            ObjetInventaire::Potion(p) => p.nom_affiche(),
            ObjetInventaire::Livre(l) => l.nom_affiche(),
        }
    }
}

impl AjouterRetirer for ObjetInventaire {
    fn ajouter(&mut self, qte: u32) {
        match self {
            ObjetInventaire::Base(o) => o.ajouter(qte),
            ObjetInventaire::Equipement(e) => e.ajouter(qte),
            ObjetInventaire::Arme(a) => a.ajouter(qte),
            ObjetInventaire::Potion(p) => p.ajouter(qte),
            ObjetInventaire::Livre(l) => l.ajouter(qte),
        }
    }

    fn retirer(&mut self, qte: u32) {
        match self {
            ObjetInventaire::Base(o) => o.retirer(qte),
            ObjetInventaire::Equipement(e) => e.retirer(qte),
            ObjetInventaire::Arme(a) => a.retirer(qte),
            ObjetInventaire::Potion(p) => p.retirer(qte),
            ObjetInventaire::Livre(l) => l.retirer(qte),
        }
    }
}

// ============================================================
// STRUCT INVENTAIRE
// ============================================================

pub struct Inventaire {
    pool: SqlitePool,
    account_id: i64,
    objets: HashMap<String, ObjetInventaire>,
}

#[derive(sqlx::FromRow)]
struct StuffRow {
    stuff_id: i64,
    quantity: i64,
    nom: String,
    type_objet: String,
    image_path: Option<String>,
}

#[derive(sqlx::FromRow)]
struct EquipmentRow {
    equipment_type: String,
    attack: i64,
    defense: i64,
    durability: i64,
}

#[derive(sqlx::FromRow)]
struct PotionRow {
    effect: String,
}

#[derive(sqlx::FromRow)]
struct BookRow {
    book_id: i64,
    book_level: i64,
}

#[derive(sqlx::FromRow)]
struct EnchantRow {
    enchantment_name: String,
    enchantment_level: i64,
}

impl Inventaire {
    pub async fn new(pool: SqlitePool, account_id: i64) -> Result<Self, sqlx::Error> {
        let objets = Self::charger_objets(&pool, account_id).await?;
        Ok(Self { pool, account_id, objets })
    }

    async fn charger_objets(
        pool: &SqlitePool,
        account_id: i64,
    ) -> Result<HashMap<String, ObjetInventaire>, sqlx::Error> {
        let rows = sqlx::query_as::<_, StuffRow>(
            r#"
            SELECT s.stuff_id, s.quantity, o.nom, o.type AS type_objet, o.image_path
            FROM stuff s
            JOIN objets_dispo o ON s.objet_id = o.objet_id
            WHERE s.account_id = ?
            "#,
        )
        .bind(account_id)
        .fetch_all(pool)
        .await?;

        let mut inventaire = HashMap::new();
        for row in rows {
            let objet = Self::construire_objet(pool, &row).await?;
            inventaire.insert(row.nom.clone(), objet);
        }
        Ok(inventaire)
    }

    async fn construire_objet(pool: &SqlitePool, row: &StuffRow) -> Result<ObjetInventaire, sqlx::Error> {
        let qte = row.quantity as u32;
        let image = row.image_path.as_deref();

        let result = match row.type_objet.as_str() {
            "equipment" | "armes" => {
                let eq: EquipmentRow = sqlx::query_as(
                    "SELECT equipment_type, attack, defense, durability FROM equipment WHERE stuff_id = ?",
                )
                .bind(row.stuff_id)
                .fetch_one(pool)
                .await?;

                if eq.equipment_type == "weapon" {
                    ObjetInventaire::Arme(Arme::new(
                        &row.nom, image, qte, 1, eq.durability as u32, eq.attack as i32, Vec::new(),
                    ))
                } else {
                    ObjetInventaire::Equipement(Equipement::new(
                        &row.nom, image, qte, 1, eq.defense as i32, Vec::new(),
                    ))
                }
            }

            "potion" => {
                let p: PotionRow = sqlx::query_as("SELECT effect FROM potions WHERE stuff_id = ?")
                    .bind(row.stuff_id)
                    .fetch_one(pool)
                    .await?;

                ObjetInventaire::Potion(Potion::new(&row.nom, image, qte, Some(&p.effect)))
            }

            "enchanted_book" => {
                let book: BookRow = sqlx::query_as(
                    "SELECT book_id, book_level FROM enchanted_books WHERE stuff_id = ?",
                )
                .bind(row.stuff_id)
                .fetch_one(pool)
                .await?;

                let enchant_rows: Vec<EnchantRow> = sqlx::query_as(
                    r#"
                    SELECT e.enchantment_name, be.enchantment_level
                    FROM book_enchantments be
                    JOIN enchantments e ON e.enchantment_id = be.enchantment_id
                    WHERE be.book_id = ?
                    "#,
                )
                .bind(book.book_id)
                .fetch_all(pool)
                .await?;

                let enchants: Vec<String> = enchant_rows
                    .into_iter()
                    .map(|e| format!("{} {}", e.enchantment_name, Livre::niv_to_roman(e.enchantment_level as u32)))
                    .collect();

                ObjetInventaire::Livre(Livre::new(
                    &row.nom, image, qte, None, Some(enchants), book.book_level as u32,
                ))
            }

            // "basic", "consumable", "material", "muni", "mineral"
            _ => ObjetInventaire::Base(Objet::new(&row.nom, image, qte, TypeObjet::DeBase)),
        };

        Ok(result)
    }

    pub fn objets(&self) -> &HashMap<String, ObjetInventaire> {
        &self.objets
    }

    pub fn objets_mut(&mut self) -> &mut HashMap<String, ObjetInventaire> {
        &mut self.objets
    }

    pub fn account_id(&self) -> i64 {
        self.account_id
    }
}
