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
    /// Annule un ordre d'achat et restitue les fonds correspondant
/// à la quantité restante.
pub async fn annuler_ordre_achat(
    &self,
    account_id: i64,
    ordre_id: i64,
) -> Result<(), sqlx::Error> {
    let mut tx = self.pool.begin().await?;

    let ordre: Option<(i64, i64, i64, String)> = sqlx::query_as(
        r#"
        SELECT
            objet_id,
            quantity_remaining,
            prix_unitaire_max,
            statut
        FROM ordres_achat
        WHERE ordre_id = ?
          AND account_id = ?
        "#,
    )
    .bind(ordre_id)
    .bind(account_id)
    .fetch_optional(&mut *tx)
    .await?;

    let (objet_id, quantity_remaining, prix_unitaire_max, statut) =
        ordre.ok_or_else(|| {
            sqlx::Error::Protocol(
                "Ordre d'achat inexistant".into(),
            )
        })?;

    if statut != "actif" {
        return Err(sqlx::Error::Protocol(
            "L'ordre d'achat n'est plus actif".into(),
        ));
    }

    let montant_a_rembourser = prix_unitaire_max
        .checked_mul(quantity_remaining)
        .ok_or_else(|| {
            sqlx::Error::Protocol(
                "Le montant du remboursement dépasse la capacité i64".into(),
            )
        })?;

    // Marque l'ordre comme annulé.
    let result = sqlx::query(
        r#"
        UPDATE ordres_achat
        SET statut = 'annule'
        WHERE ordre_id = ?
          AND account_id = ?
          AND statut = 'actif'
        "#,
    )
    .bind(ordre_id)
    .bind(account_id)
    .execute(&mut *tx)
    .await?;

    if result.rows_affected() != 1 {
        return Err(sqlx::Error::Protocol(
            "Impossible d'annuler l'ordre d'achat".into(),
        ));
    }

    // Restitue les fonds réservés.
    if montant_a_rembourser > 0 {
        WalletManager::crediter_tx(
            &mut tx,
            account_id,
            montant_a_rembourser,
        )
        .await?;
    }

    tx.commit().await?;

    let _ = objet_id;

    Ok(())
}
    /// Annule un ordre de vente et restitue les objets restants
/// dans l'inventaire du vendeur.
pub async fn annuler_ordre_vente(
    &self,
    account_id: i64,
    ordre_id: i64,
) -> Result<(), sqlx::Error> {
    let mut tx = self.pool.begin().await?;

    let ordre: Option<(i64, i64, String)> = sqlx::query_as(
        r#"
        SELECT
            objet_id,
            quantity_remaining,
            statut
        FROM ordres_vente
        WHERE ordre_id = ?
          AND account_id = ?
        "#,
    )
    .bind(ordre_id)
    .bind(account_id)
    .fetch_optional(&mut *tx)
    .await?;

    let (objet_id, quantity_remaining, statut) =
        ordre.ok_or_else(|| {
            sqlx::Error::Protocol(
                "Ordre de vente inexistant".into(),
            )
        })?;

    if statut != "actif" {
        return Err(sqlx::Error::Protocol(
            "L'ordre de vente n'est plus actif".into(),
        ));
    }

    let quantity_u64 = u64::try_from(quantity_remaining).map_err(|_| {
        sqlx::Error::Protocol(
            "Quantité invalide".into(),
        )
    })?;

    // Restitue les objets réservés.
    if quantity_u64 > 0 {
        Inventaire::ajouter_tx(
            &mut tx,
            account_id,
            objet_id,
            quantity_u64,
        )
        .await?;
    }

    // Marque l'ordre comme annulé.
    let result = sqlx::query(
        r#"
        UPDATE ordres_vente
        SET statut = 'annule'
        WHERE ordre_id = ?
          AND account_id = ?
          AND statut = 'actif'
        "#,
    )
    .bind(ordre_id)
    .bind(account_id)
    .execute(&mut *tx)
    .await?;

    if result.rows_affected() != 1 {
        return Err(sqlx::Error::Protocol(
            "Impossible d'annuler l'ordre de vente".into(),
        ));
    }

    tx.commit().await?;

    Ok(())
                       }
}
