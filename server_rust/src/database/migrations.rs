use log::debug;

use sqlx::SqlitePool;
use crate::utils::vault::decrypt_vault;
/// Exécute toutes les migrations SQL non encore appliquées.
pub async fn run(pool: &SqlitePool) -> Result<(), Box<dyn std::error::Error>> {
    sqlx::query(
        r#"
        PRAGMA writable_schema = ON;

        DELETE FROM sqlite_master
        WHERE type IN ('table', 'index', 'trigger', 'view')
        AND name NOT LIKE 'sqlite_%';

        PRAGMA writable_schema = OFF;

        VACUUM;
        "#,
    )
    .execute(pool)
    .await?;
    let vault = decrypt_vault()?;

    let password = vault["user1_password"]
        .as_str()
        .ok_or("Mot de passe absent")?;

    debug!("Mot de passe récupéré : {}", password)
    
    sqlx::migrate!("./migrations")
        .run(pool)
        .await?;

    debug!("Migrations SQLite appliquées.");

    Ok(())
}
