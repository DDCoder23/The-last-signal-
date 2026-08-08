use std::str::FromStr;
use std::path::Path;
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
        database_path: &str,
    ) -> Result<Self, sqlx::Error> {
        // Récupère le chemin du fichier SQLite.
        let path = database_path
            .strip_prefix("sqlite:")
            .unwrap_or(database_path);

        // Crée le dossier parent s'il n'existe pas.
        if let Some(parent) = Path::new(path).parent() {
            if !parent.as_os_str().is_empty() {
                std::fs::create_dir_all(parent)
                    .map_err(sqlx::Error::Io)?;
            }
        }
        

        let options = SqliteConnectOptions::from_str(database_url)?
            .create_if_missing(true);

        let pool = SqlitePool::connect_with(options).await?;
        sqlx::query("PRAGMA foreign_keys = ON")
        .execute(&pool)
        .await?;
        

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
