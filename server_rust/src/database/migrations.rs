use sqlx::PgPool;
use log::debug;
/// Exécute toutes les migrations SQL non encore appliquées.
pub async fn run(pool: &PgPool) -> Result<(), sqlx::Error> {
    sqlx::migrate!("./migrations")
        .run(pool)
        .await?;

    debug!("Migrations PostgreSQL appliquées.");

    Ok(())
}
