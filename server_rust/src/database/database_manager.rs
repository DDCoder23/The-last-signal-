use std::path::Path;
use std::str::FromStr;

use sqlx::{
    sqlite::{SqliteConnectOptions, SqlitePool, SqlitePoolOptions},
};

pub struct DatabaseManager {
    pool: SqlitePool,
}

impl DatabaseManager {
    /// Vérifie si une base SQLite existante est corrompue.
    pub async fn is_database_corrupted(
        database_url: &str,
    ) -> Result<bool, sqlx::Error> {
        let options = SqliteConnectOptions::from_str(database_url)?
            .create_if_missing(false);

        let pool = SqlitePoolOptions::new()
            .max_connections(1)
            .connect_with(options)
            .await?;

        let integrity: String = sqlx::query_scalar(
            "PRAGMA integrity_check"
        )
        .fetch_one(&pool)
        .await?;

        pool.close().await;

        Ok(integrity.trim() != "ok")
    }

    /// Crée ou ouvre la base SQLite.
    pub async fn create_database(
        database_url: &str,
    ) -> Result<SqlitePool, sqlx::Error> {
        let options = SqliteConnectOptions::from_str(database_url)?
            .create_if_missing(true);

        let pool = SqlitePoolOptions::new()
            .max_connections(5)
            .after_connect(|conn, _meta| {
                Box::pin(async move {
                    // Attend jusqu'à 30 secondes lorsqu'un autre
                    // écrivain possède temporairement le verrou.
                    sqlx::query("PRAGMA busy_timeout = 30000")
                        .execute(&mut *conn)
                        .await?;

                    // Permet plusieurs lecteurs pendant une écriture.
                    sqlx::query("PRAGMA journal_mode = WAL")
                        .execute(&mut *conn)
                        .await?;

                    // Bon compromis performances / sécurité.
                    sqlx::query("PRAGMA synchronous = NORMAL")
                        .execute(&mut *conn)
                        .await?;

                    // Vérification des clés étrangères.
                    sqlx::query("PRAGMA foreign_keys = ON")
                        .execute(&mut *conn)
                        .await?;

                    Ok(())
                })
            })
            .connect_with(options)
            .await?;

        Ok(pool)
    }

    pub fn pool(&self) -> &SqlitePool {
        &self.pool
    }

    pub async fn ping(&self) -> Result<(), sqlx::Error> {
        sqlx::query("SELECT 1")
            .execute(&self.pool)
            .await?;

        Ok(())
    }

    pub async fn new(
        database_path: &str,
        database_url: &str,
    ) -> Result<Self, sqlx::Error> {
        let path = database_path
            .strip_prefix("sqlite:")
            .unwrap_or(database_path);

        let database_file = database_url
            .strip_prefix("sqlite:")
            .unwrap_or(database_url);

        std::fs::create_dir_all(path)
            .map_err(sqlx::Error::Io)?;

        let mut pool =
            Self::create_database(database_url).await?;

        if Path::new(database_file).exists() {
            match Self::is_database_corrupted(database_url).await {
                Ok(true) => {
                    eprintln!(
                        "⚠️ La base SQLite est corrompue. \
                         Suppression et recréation..."
                    );

                    // IMPORTANT :
                    // fermer le pool avant de supprimer le fichier.
                    pool.close().await;

                    std::fs::remove_file(database_file)
                        .map_err(sqlx::Error::Io)?;

                    pool =
                        Self::create_database(database_url)
                            .await?;
                }

                Ok(false) => {
                    eprintln!("✓ Base SQLite valide.");
                }

                Err(error) => {
                    eprintln!(
                        "❌ Impossible de vérifier l'intégrité \
                         de la base SQLite : {error}"
                    );

                    pool.close().await;

                    return Err(error);
                }
            }
        }

        Ok(Self { pool })
    }
}
