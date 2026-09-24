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
    fn ajouter(&mut self, qte: u64) {
        match self {
            ObjetInventaire::Base(o) => o.ajouter(qte),
            ObjetInventaire::Equipement(e) => e.ajouter(qte),
            ObjetInventaire::Arme(a) => a.ajouter(qte),
            ObjetInventaire::Potion(p) => p.ajouter(qte),
            ObjetInventaire::Livre(l) => l.ajouter(qte),
        }
    }

    fn retirer(&mut self, qte: u64) {
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
    quantity: u64,
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
        let qte = row.quantity as u64;
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
    pub async fn retirer_objet(
    &mut self,
    nom: &str,
    quantite: u64,
) -> Result<(), sqlx::Error> {
    // Une quantité nulle n'est pas une opération valide.
    if quantite == 0 {
        return Err(sqlx::Error::Protocol(
            "La quantité à retirer doit être supérieure à 0".into(),
        ));
    }

    // ------------------------------------------------------------
    // 1. Vérification de l'objet dans l'inventaire en mémoire
    // ------------------------------------------------------------

    let objet = self.objets.get(nom).ok_or_else(|| {
        sqlx::Error::Protocol(
            format!("Objet absent de l'inventaire : {nom}").into(),
        )
    })?;

    let quantite_actuelle = match objet {
        ObjetInventaire::Base(o) => o.quantite,
        ObjetInventaire::Equipement(e) => e.quantite,
        ObjetInventaire::Arme(a) => a.quantite,
        ObjetInventaire::Potion(p) => p.quantite,
        ObjetInventaire::Livre(l) => l.quantite,
    };

    // Impossible de retirer plus que ce que possède le joueur.
    if quantite > quantite_actuelle {
        return Err(sqlx::Error::Protocol(
            format!(
                "Quantité insuffisante pour {nom} : possède {quantite_actuelle}, \
                 demande {quantite}"
            )
            .into(),
        ));
    }

    // ------------------------------------------------------------
    // 2. Récupération de l'identifiant de l'objet
    // ------------------------------------------------------------

    let objet_id: i64 = sqlx::query_scalar(
        r#"
        SELECT objet_id
        FROM objets_dispo
        WHERE nom = ?
        "#,
    )
    .bind(nom)
    .fetch_one(&self.pool)
    .await?;

    // ------------------------------------------------------------
    // 3. Modification atomique de la base
    // ------------------------------------------------------------

    let mut tx = self.pool.begin().await?;

    if quantite == quantite_actuelle {
        // --------------------------------------------------------
        // Toute la pile est retirée :
        // on supprime directement la ligne.
        // --------------------------------------------------------

        let result = sqlx::query(
            r#"
            DELETE FROM stuff
            WHERE account_id = ?
              AND objet_id = ?
              AND quantity = ?
            "#,
        )
        .bind(self.account_id)
        .bind(objet_id)
        .bind(quantite)
        .execute(&mut *tx)
        .await?;

        if result.rows_affected() == 0 {
            tx.rollback().await?;

            return Err(sqlx::Error::RowNotFound);
        }
    } else {
        // --------------------------------------------------------
        // Une partie seulement est retirée.
        //
        // La condition quantity >= ? protège contre un retrait
        // supérieur à la quantité réellement présente en base.
        // --------------------------------------------------------

        let result = sqlx::query(
            r#"
            UPDATE stuff
            SET quantity = quantity - ?
            WHERE account_id = ?
              AND objet_id = ?
              AND quantity >= ?
            "#,
        )
        .bind(quantite)
        .bind(self.account_id)
        .bind(objet_id)
        .bind(quantite)
        .execute(&mut *tx)
        .await?;

        if result.rows_affected() == 0 {
            tx.rollback().await?;

            return Err(sqlx::Error::RowNotFound);
        }
    }

    // ------------------------------------------------------------
    // 4. Validation de la transaction SQLite
    // ------------------------------------------------------------

    tx.commit().await?;

    // ------------------------------------------------------------
    // 5. Mise à jour du HashMap en mémoire
    // ------------------------------------------------------------

    if quantite == quantite_actuelle {
        self.objets.remove(nom);
    } else if let Some(objet) = self.objets.get_mut(nom) {
        objet.retirer(quantite);
    }

    Ok(())
            }
    pub async fn ajouter_objet(
    &mut self,
    nom: &str,
    quantite: u64,
) -> Result<(), sqlx::Error> {
    // ------------------------------------------------------------
    // 1. Vérification de la quantité
    // ------------------------------------------------------------

    if quantite == 0 {
        return Err(sqlx::Error::Protocol(
            "La quantité à ajouter doit être supérieure à 0".into(),
        ));
    }

    // ------------------------------------------------------------
    // 2. Récupération de l'objet dans objets_dispo
    // ------------------------------------------------------------

    let objet_id: i64 = sqlx::query_scalar(
        r#"
        SELECT objet_id
        FROM objets_dispo
        WHERE nom = ?
        "#,
    )
    .bind(nom)
    .fetch_one(&self.pool)
    .await?;

    // ------------------------------------------------------------
    // 3. Ajout atomique dans SQLite
    // ------------------------------------------------------------

    sqlx::query(
        r#"
        INSERT INTO stuff (
            account_id,
            objet_id,
            quantity
        )
        VALUES (?, ?, ?)
        ON CONFLICT(account_id, objet_id)
        DO UPDATE SET
            quantity = quantity + excluded.quantity
        "#,
    )
    .bind(self.account_id)
    .bind(objet_id)
    .bind(quantite)
    .execute(&self.pool)
    .await?;

    // ------------------------------------------------------------
    // 4. Mise à jour de l'inventaire en mémoire
    // ------------------------------------------------------------

    if let Some(objet) = self.objets.get_mut(nom) {
        objet.ajouter(quantite);
    } else {
        // L'objet n'était pas présent dans le HashMap.
        // On recharge l'inventaire depuis SQLite afin de
        // construire correctement ObjetInventaire selon son type.
        self.objets = Self::charger_objets(
            &self.pool,
            self.account_id,
        )
        .await?;
    }

    Ok(())
    }
    pub async fn get_quantity(
    &self,
    nom: &str,
) -> Result<u64, sqlx::Error> {
    let quantity: Option<i64> = sqlx::query_scalar(
        r#"
        SELECT s.quantity
        FROM stuff s
        JOIN objets_dispo o
            ON s.objet_id = o.objet_id
        WHERE s.account_id = ?
          AND o.nom = ?
        "#,
    )
    .bind(self.account_id)
    .bind(nom)
    .fetch_optional(&self.pool)
    .await?;

    match quantity {
        Some(value) => u64::try_from(value).map_err(|_| {
            sqlx::Error::Protocol(
                format!("Quantité invalide pour l'objet {nom}").into(),
            )
        }),
        None => Ok(0),
    }
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
