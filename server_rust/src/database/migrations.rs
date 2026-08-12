use log::debug;
use uuid::Uuid;
use sqlx::SqlitePool;
use crate::utils::vault::decrypt_vault;
use crate::utils::password::hash_password;
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

    let password1 = vault["user1_password"]
    .as_str()
    .ok_or("Mot de passe user1 absent")?;
    let password1_hash = hash_password(password1)
    .map_err(|e| sqlx::Error::Protocol(e))?;

    let password2 = vault["user2_password"]
    .as_str()
    .ok_or("Mot de passe user2 absent")?;
    let password2_hash = hash_password(password2)
    .map_err(|e| sqlx::Error::Protocol(e))?;
    
    
    sqlx::migrate!("./migrations")
        .run(pool)
        .await?;

    debug!("Migrations SQLite appliquées.");
    create_account(
    pool,
    "Admin@gmail.com",
    &password1_hash,
        "Cyril",
        "Admin",
)
.await?;

create_account(
    pool,
    "Superadmin@gmail.com",
    &password2_hash,
    "Morgan",
    "SuperAdmin",
)
.await?;

    Ok(())
}



async fn create_account(
    pool: &SqlitePool,
    email: &str,
    password_hash: &str,
    account_name: &str,
    perm: &str,
) -> Result<(), sqlx::Error> {
    let user_id = Uuid::new_v4().to_string();

    sqlx::query(
        r#"
        INSERT OR IGNORE INTO users (
            user_id,
            email,
            password_hash
        )
        VALUES (?, ?, ?)
        "#,
    )
    .bind(&user_id)
    .bind(email)
    .bind(password_hash)
    .execute(pool)
    .await?;
    sqlx::query(
        r#"
        INSERT OR IGNORE INTO accounts (
            user_id,
            account_name
        )
        VALUES (?, ?)
        "#,
    )
    .bind(&user_id)
    .bind(account_name)
    .execute(pool)
    .await?;
    sqlx::query(
        r#"
        INSERT OR IGNORE INTO perms (
            
            account_name,
            perm
        )
        VALUES (?, ?)
        "#,
    )
    .bind(&user_id)
    .bind(perm)
    .execute(pool)
    .await?;

    Ok(())
}
