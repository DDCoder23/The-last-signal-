use sqlx::SqlitePool;

use crate::gameplay::stuff_manager::Inventaire;
use crate::gameplay::wallet_manager::WalletManager;

pub struct MarketManager {
    pool: SqlitePool,
}

impl MarketManager {
    pub fn new(pool: SqlitePool) -> Self {
        Self { pool }
    }

    /// Crée un ordre d'achat.
    ///
    /// Les fonds correspondant au montant maximal de l'ordre
    /// sont immédiatement réservés.
    pub async fn creer_ordre_achat(
        &self,
        account_id: i64,
        objet_id: i64,
        quantity: u64,
        prix_unitaire_max: i64,
    ) -> Result<i64, sqlx::Error> {
        if quantity == 0 {
            return Err(sqlx::Error::Protocol(
                "La quantité doit être supérieure à 0".into(),
            ));
        }

        if prix_unitaire_max <= 0 {
            return Err(sqlx::Error::Protocol(
                "Le prix unitaire doit être supérieur à 0".into(),
            ));
        }

        let quantity_i64 = i64::try_from(quantity).map_err(|_| {
            sqlx::Error::Protocol(
                "La quantité dépasse la capacité SQLite INTEGER".into(),
            )
        })?;

        let montant_total = prix_unitaire_max
            .checked_mul(quantity_i64)
            .ok_or_else(|| {
                sqlx::Error::Protocol(
                    "Le montant total dépasse la capacité i64".into(),
                )
            })?;

        let mut tx = self.pool.begin().await?;

        // Vérifie que l'objet existe.
        let existe: Option<i64> = sqlx::query_scalar(
            r#"
            SELECT objet_id
            FROM objets_dispo
            WHERE objet_id = ?
            "#,
        )
        .bind(objet_id)
        .fetch_optional(&mut *tx)
        .await?;

        if existe.is_none() {
            return Err(sqlx::Error::Protocol(
                "Objet inexistant".into(),
            ));
        }

        // Réserve l'argent.
        WalletManager::debiter_tx(
            &mut tx,
            account_id,
            montant_total,
        )
        .await?;

        // Crée l'ordre.
        let result = sqlx::query(
            r#"
            INSERT INTO ordres_achat (
                account_id,
                objet_id,
                quantity,
                quantity_remaining,
                prix_unitaire_max,
                statut
            )
            VALUES (?, ?, ?, ?, ?, 'actif')
            "#,
        )
        .bind(account_id)
        .bind(objet_id)
        .bind(quantity_i64)
        .bind(quantity_i64)
        .bind(prix_unitaire_max)
        .execute(&mut *tx)
        .await?;

        let ordre_id = result.last_insert_rowid();

        tx.commit().await?;

        Ok(ordre_id)
    }

    /// Crée un ordre de vente.
    ///
    /// Les objets vendus sont immédiatement retirés de l'inventaire
    /// afin qu'ils ne puissent pas être utilisés dans plusieurs ordres.
    pub async fn creer_ordre_vente(
        &self,
        account_id: i64,
        objet_id: i64,
        quantity: u64,
        prix_unitaire: i64,
    ) -> Result<i64, sqlx::Error> {
        if quantity == 0 {
            return Err(sqlx::Error::Protocol(
                "La quantité doit être supérieure à 0".into(),
            ));
        }

        if prix_unitaire <= 0 {
            return Err(sqlx::Error::Protocol(
                "Le prix unitaire doit être supérieur à 0".into(),
            ));
        }

        let quantity_i64 = i64::try_from(quantity).map_err(|_| {
            sqlx::Error::Protocol(
                "La quantité dépasse la capacité SQLite INTEGER".into(),
            )
        })?;

        let mut tx = self.pool.begin().await?;

        // Vérifie que l'objet existe.
        let existe: Option<i64> = sqlx::query_scalar(
            r#"
            SELECT objet_id
            FROM objets_dispo
            WHERE objet_id = ?
            "#,
        )
        .bind(objet_id)
        .fetch_optional(&mut *tx)
        .await?;

        if existe.is_none() {
            return Err(sqlx::Error::Protocol(
                "Objet inexistant".into(),
            ));
        }

        // Réserve les objets.
        Inventaire::retirer_tx(
            &mut tx,
            account_id,
            objet_id,
            quantity,
        )
        .await?;

        // Crée l'ordre.
        let result = sqlx::query(
            r#"
            INSERT INTO ordres_vente (
                account_id,
                objet_id,
                quantity,
                quantity_remaining,
                prix_unitaire,
                statut
            )
            VALUES (?, ?, ?, ?, ?, 'actif')
            "#,
        )
        .bind(account_id)
        .bind(objet_id)
        .bind(quantity_i64)
        .bind(quantity_i64)
        .bind(prix_unitaire)
        .execute(&mut *tx)
        .await?;

        let ordre_id = result.last_insert_rowid();

        tx.commit().await?;

        Ok(ordre_id)
    }
}
