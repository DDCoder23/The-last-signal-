use sqlx::PgPool;

/// Exécute toutes les migrations SQL non encore appliquées.
pub async fn run(pool: &PgPool) -> Result<(), sqlx::Error> {
    sqlx::migrate!("./migrations")
        .run(pool)
        .await?;

    println!("Migrations PostgreSQL appliquées.");

    Ok(())
}
