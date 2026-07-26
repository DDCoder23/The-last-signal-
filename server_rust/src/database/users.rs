use chrono::{DateTime, Utc};
use uuid::Uuid;

/// Représente un utilisateur.
///
/// Un utilisateur correspond à une personne réelle.
/// Il peut posséder plusieurs comptes de jeu.
#[derive(Debug, Clone)]
pub struct User {
    pub user_id: Uuid,

    pub email: String,

    pub password_hash: String,

    pub created_at: DateTime<Utc>,

    pub last_login: Option<DateTime<Utc>>,
}

impl User {
    /// Crée un nouvel utilisateur.
    pub fn new(
        email: String,
        password_hash: String,
    ) -> Self {
        Self {
            user_id: Uuid::new_v4(),
            email,
            password_hash,
            created_at: Utc::now(),
            last_login: None,
        }
    }
}
use sqlx::PgPool;

pub struct UserRepository<'a> {
    pool: &'a PgPool,
}

impl<'a> UserRepository<'a> {
    pub fn new(pool: &'a PgPool) -> Self {
        Self { pool }
    }
}
