use sqlx::SqlitePool;

pub struct WalletManager {
    pool: SqlitePool,
    account_id: i64,
}

impl WalletManager {
    pub fn new(pool: SqlitePool, account_id: i64) -> Self {
        Self {
            pool,
            account_id,
        }
    }

    pub fn account_id(&self) -> i64 {
        self.account_id
    }

    /// Retourne le solde actuel du compte.
    pub async fn get_balance(&self) -> Result<i64, sqlx::Error> {
        let balance: i64 = sqlx::query_scalar(
            r#"
            SELECT balance
            FROM wallets
            WHERE account_id = ?
            "#,
        )
        .bind(self.account_id)
        .fetch_one(&self.pool)
        .await?;

        Ok(balance)
    }

    /// Crédite le portefeuille.
    pub async fn crediter(&self, montant: i64) -> Result<(), sqlx::Error> {
        if montant <= 0 {
            return Err(sqlx::Error::Protocol(
                "Le montant à créditer doit être supérieur à 0".into(),
            ));
        }

        sqlx::query(
            r#"
            UPDATE wallets
            SET balance = balance + ?
            WHERE account_id = ?
            "#,
        )
        .bind(montant)
        .bind(self.account_id)
        .execute(&self.pool)
        .await?;

        Ok(())
    }

    /// Débite le portefeuille.
    ///
    /// Le `WHERE balance >= ?` empêche le solde de devenir négatif,
    /// même en cas de concurrence entre plusieurs opérations.
    pub async fn debiter(&self, montant: i64) -> Result<(), sqlx::Error> {
        if montant <= 0 {
            return Err(sqlx::Error::Protocol(
                "Le montant à débiter doit être supérieur à 0".into(),
            ));
        }

        let result = sqlx::query(
            r#"
            UPDATE wallets
            SET balance = balance - ?
            WHERE account_id = ?
              AND balance >= ?
            "#,
        )
        .bind(montant)
        .bind(self.account_id)
        .bind(montant)
        .execute(&self.pool)
        .await?;

        if result.rows_affected() == 0 {
            return Err(sqlx::Error::Protocol(
                "Solde insuffisant ou portefeuille inexistant".into(),
            ));
        }

        Ok(())
    }
}
