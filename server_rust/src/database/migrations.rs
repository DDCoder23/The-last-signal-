use log::debug;
use sqlx::SqlitePool;

/// Exécute toutes les migrations SQL non encore appliquées.
pub async fn run(pool: &SqlitePool) -> Result<(), sqlx::Error> {
    sqlx::migrate!("./migrations")
        .run(pool)
        .await?;

    debug!("Migrations SQLite appliquées.");

    Ok(())
}
