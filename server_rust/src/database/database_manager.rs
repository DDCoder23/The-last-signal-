use sqlx::SqlitePool;

pub struct DatabaseManager {
    pool: PgPool,
}

impl DatabaseManager {
    /// Crée un pool de connexions PostgreSQL.
    pub async fn new(
        database_url: &str,
    ) -> Result<Self, sqlx::Error> {

        let pool = SqlitePool::connect(&database_url).await?;

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
