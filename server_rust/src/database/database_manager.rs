use std::str::FromStr;
use std::path::Path;

use sqlx::{
    sqlite::{SqliteConnectOptions, SqlitePool, SqlitePoolOptions},
    Error,
};



pub struct DatabaseManager {
    pool: SqlitePool,
}


impl DatabaseManager {
    /// Vérifie si une base SQLite existante est corrompue.
    ///
    /// Retourne :
    /// - Ok(false) → base valide
    /// - Ok(true)  → base corrompue
    /// - Err(...)  → impossible de vérifier la base
    pub async fn is_database_corrupted(
        database_url: &str,
    ) -> Result<bool, sqlx::Error> {
        let options = SqliteConnectOptions::from_str(database_url)?
            .create_if_missing(false);

        let pool = SqlitePool::connect_with(options).await?;

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

        // Use SqlitePoolOptions to limit concurrent connections for SQLite.
        // SQLite supports a single writer at a time; limiting the pool helps
        // avoid write contention and "database is locked" errors.
        let pool = SqlitePoolOptions::new()
            .max_connections(100)
            .connect_with(options)
            .await?;

        // Enable WAL properly (fixed typo from previous "pjournal_mode").
        sqlx::query("PRAGMA journal_mode = WAL;")
            .execute(&pool)
            .await?;
        
        sqlx::query("PRAGMA busy_timeout = 30000")  // 30 secondes
            .execute(&pool)
            .await?;
        
        sqlx::query("PRAGMA synchronous = NORMAL")  // Plus rapide
            .execute(&pool)
            .await?;

        sqlx::query("PRAGMA foreign_keys = ON")
            .execute(&pool)
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
        // --------------------------------------------------
        // 1. Récupérer le chemin réel de la DB
        // --------------------------------------------------

        let path = database_path
            .strip_prefix("sqlite:")
            .unwrap_or(database_path);
        let database_file = database_url
            .strip_prefix("sqlite:")
            .unwrap_or(database_url);
        
       std::fs::create_dir_all(path)
        .map_err(sqlx::Error::Io)?;
      let mut pool =Self::create_database(database_url).await?;
        

        
        
        

        // --------------------------------------------------
        // 3. Vérifier la DB si elle existe déjà
        // --------------------------------------------------

        if Path::new(database_file).exists() {
            match Self::is_database_corrupted(database_url).await {
                Ok(true) => {
                    eprintln!(
                        "⚠️ La base SQLite est corrompue. \
                         Suppression et recréation..."
                    );

                    std::fs::remove_file(database_file)
                        .map_err(sqlx::Error::Io)?;
                    pool =Self::create_database(database_url).await?;


                    
                }

                Ok(false) => {
                    eprintln!("✓ Base SQLite valide.");
                }

                Err(error) => {
                    eprintln!(
                        "❌ Impossible de vérifier l'intégrité \
                         de la base SQLite : {error}"
                    );

                    // Très important :
                    // on NE supprime pas la base ici.
                    return Err(error);
                }
            }
        } 

        
        // --------------------------------------------------
        // 5. Retourner la structure
        // --------------------------------------------------

        Ok(Self {
            pool,
        })
    }
}
