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
        Some("Dev"),
)
.await?;

create_account(
    pool,
    "Superadmin@gmail.com",
    &password2_hash,
    "Morgan",
    Some("SuperDev"),
)
.await?;

    Ok(())
}

async fn create_account(
    pool: &SqlitePool,
    email: &str,
    password_hash: &str,
    account_name: &str,
    role_name: Option<&str>,
) -> Result<(), sqlx::Error> {
    let mut tx = pool.begin().await?;

    // ========================================================
    // 1. Chercher l'utilisateur existant
    // ========================================================

    let user_id: String = match sqlx::query_scalar(
        r#"
        SELECT user_id
        FROM users
        WHERE email = ?
        "#,
    )
    .bind(email)
    .fetch_optional(&mut *tx)
    .await?
    {
        Some(user_id) => user_id,

        // L'utilisateur n'existe pas : le créer
        None => {
            let user_id = Uuid::new_v4().to_string();

            sqlx::query(
                r#"
                INSERT INTO users (
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
            .execute(&mut *tx)
            .await?;

            user_id
        }
    };

    // ========================================================
    // 2. Récupérer le rôle si un rôle est demandé
    // ========================================================

    let role_id: Option<i64> = match role_name {
        Some(role_name) => {
            let role_id: Option<i64> = sqlx::query_scalar(
                r#"
                SELECT role_id
                FROM roles
                WHERE role_name = ?
                "#,
            )
            .bind(role_name)
            .fetch_optional(&mut *tx)
            .await?;

            match role_id {
                Some(id) => Some(id),

                // Le rôle demandé n'existe pas
                None => {
                    return Err(sqlx::Error::RowNotFound);
                }
            }
        }

        // Aucun rôle demandé
        None => None,
    };

    // ========================================================
    // 3. Créer le compte
    // ========================================================

    sqlx::query(
        r#"
        INSERT INTO accounts (
            user_id,
            account_name,
            role_id
        )
        VALUES (?, ?, ?)
        "#,
    )
    .bind(&user_id)
    .bind(account_name)
    .bind(role_id)
    .execute(&mut *tx)
    .await?;

    // ========================================================
    // 4. Valider la transaction
    // ========================================================

    tx.commit().await?;

    Ok(())
}
