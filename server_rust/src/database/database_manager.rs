use std::str::FromStr;
use std::path::Path;

use sqlx::{
    sqlite::{SqliteConnectOptions, SqlitePool},
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

        let pool = SqlitePool::connect_with(options).await?;

        sqlx::query("PRAGMA foreign_keys = ON")
            .execute(&pool)
            .await?;

        Ok(pool)
    }
    pub fn pool(&self) -> &SqlitePool {
        &self.pool
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



    

