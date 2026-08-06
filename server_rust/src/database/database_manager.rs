use std::str::FromStr;

use sqlx::{
    sqlite::SqliteConnectOptions,
    SqlitePool,
};


pub struct DatabaseManager {
    pool: SqlitePool,
}

impl DatabaseManager {
    /// Crée un pool de connexions PostgreSQL.
    pub async fn new(
        database_url: &str,
    ) -> Result<Self, sqlx::Error> {

        let options = SqliteConnectOptions::from_str(database_url)?
            .create_if_missing(true);

        let pool = SqlitePool::connect_with(options).await?;
        

        Ok(Self {
            pool,
        })
    }

    /// Retourne le pool PostgreSQL.
    pub fn pool(&self) -> &SqlitePool {
        &self.pool
    }

    /// Vérifie que PostgreSQL répond.
    pub async fn ping(&self) -> Result<(), sqlx::Error> {

        sqlx::query("SELECT 1")
            .execute(&self.pool)
            .await?;

        Ok(())
    }
}
