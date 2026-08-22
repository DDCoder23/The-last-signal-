use crate::network::packet::{
    Packet,
    PacketType,
    LogLevel,
    ClientLog,
};
use crate::network::client::Client;
use crate::network::parser::{parse_login_payload, parse_signup_payload};
use crate::utils::password::{verify_password, hash_password};
use log::{trace, debug, info, warn, error};
use sqlx::{SqlitePool, Row};
use uuid::Uuid;

// Structure pour représenter un utilisateur
struct User {
    user_id: String,
    password_hash: String,
}

// Structure pour les données de login complètes
struct LoginData {
    user_id: String,
    password_hash: String,
    is_banned_perm: bool,
    is_banned_temp: bool,
}

pub struct PacketHandler;

impl PacketHandler {
    pub async fn handle(
        client: &mut Client,
        packet: Packet,
        pool: SqlitePool,
    ) -> Packet {
        match packet.packet_type {
            PacketType::Log => {
                let log = match serde_json::from_slice::<ClientLog>(&packet.payload) {
                    Ok(log) => log,
                    Err(e) => {
                        error!("Impossible de décoder le paquet LOG : {}", e);
                        return Packet::new(PacketType::Log, b"INVALID_LOG".to_vec());
                    }
                };

                match log.level {
                    LogLevel::TRACE => {
                        trace!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                    },
                    LogLevel::DEBUG => {
                        debug!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                    },
                    LogLevel::INFO => {
                        info!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                    },
                    LogLevel::WARNING => {
                        warn!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                    },
                    LogLevel::ERROR => {
                        error!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                    },
                }

                Packet::new(PacketType::Log, b"OK".to_vec())
            },

            PacketType::Ping => {
                debug!("Ping reçu");
                Packet::new(PacketType::Ping, b"PONG".to_vec())
            },

            PacketType::SignUp => {
                // 1. Parser le packet SIGN_UP
                let (email, password) = match parse_signup_payload(&packet.payload) {
                    Ok(signup) => signup,
                    Err(error) => {
                        debug!("SIGN_UP invalide : {}", error);
                        return Packet::new(PacketType::SignUp, b"SIGN_UP invalide".to_vec());
                    }
                };

                // 2. Générer le hash Argon2 AVANT la requête DB
                // (operation CPU-intensive, ne doit pas bloquer le pool)
                let password_hash = match hash_password(&password) {
                    Ok(hash) => hash,
                    Err(error) => {
                        error!("Erreur lors du hash du mot de passe : {}", error);
                        return Packet::new(PacketType::SignUp, b"Erreur serveur".to_vec());
                    }
                };

                // 3. Générer le user_id
                let user_id = Uuid::new_v4().to_string();

                // 4. Insérer directement (SQLite gère les contraintes UNIQUE)
                // Cela évite la vérification d'existence séparée
                match sqlx::query(
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
                .bind(&email)
                .bind(&password_hash)
                .execute(&pool)
                .await
                {
                    Ok(_) => {
                        debug!("Nouvel utilisateur créé : {}", email);
                        client.user_id = Some(user_id.clone());
                        Packet::new(PacketType::SignUp, b"Utilisateur cree avec succes".to_vec())
                    }
                    Err(error) => {
                        // Vérifier si c'est un conflit d'email
                        let error_msg = error.to_string();
                        if error_msg.contains("UNIQUE constraint failed") {
                            debug!("SIGN_UP refusé : email déjà utilisé");
                            Packet::new(PacketType::SignUp, b"Email deja utilise".to_vec())
                        } else {
                            error!("Erreur lors de la création du user : {}", error);
                            Packet::new(PacketType::SignUp, b"Erreur serveur".to_vec())
                        }
                    }
                }
            },

            PacketType::Login => {
                // 1. Parser le packet LOGIN
                let (email, password) = match parse_login_payload(&packet.payload) {
                    Ok(login) => login,
                    Err(error) => {
                        debug!("LOGIN invalide : {}", error);
                        return Packet::new(PacketType::Login, b"LOGIN invalide".to_vec());
                    }
                };

                // 2. OPTIMISATION : Une seule requête pour toutes les données
                let login_data = match sqlx::query(
                    r#"
                    SELECT
                        u.user_id,
                        u.password_hash,
                        u.status,
                        COALESCE((SELECT EXISTS(SELECT 1 FROM bansperm WHERE user_id = u.user_id)), 0) as is_banned_perm,
                        COALESCE((SELECT EXISTS(SELECT 1 FROM bansferme WHERE user_id = u.user_id AND datetime(date_deban) > CURRENT_TIMESTAMP)), 0) as is_banned_temp
                    FROM users u
                    WHERE u.email = ?
                    "#,
                )
                .bind(&email)
                .fetch_optional(&pool)
                .await
                {
                    Ok(Some(row)) => {
                        LoginData {
                            user_id: row.get::<String, _>("user_id"),
                            password_hash: row.get::<String, _>("password_hash"),
                            is_banned_perm: row.get::<i64, _>("is_banned_perm") != 0,
                            is_banned_temp: row.get::<i64, _>("is_banned_temp") != 0,
                        }
                    },
                    Ok(None) => {
                        debug!("Tentative de connexion avec un utilisateur inexistant");
                        return Packet::new(PacketType::Login, b"Identifiants invalides".to_vec());
                    }
                    Err(error) => {
                        error!("Erreur lors de la recherche de l'utilisateur : {}", error);
                        return Packet::new(PacketType::Login, b"Erreur serveur".to_vec());
                    }
                };

                // 3. Vérifier le ban permanent
                if login_data.is_banned_perm {
                    debug!("Connexion refusée : utilisateur banni définitivement");
                    return Packet::new(PacketType::Login, b"Compte banni definitivement".to_vec());
                }

                // 4. Vérifier le ban temporaire
                if login_data.is_banned_temp {
                    debug!("Connexion refusée : utilisateur temporairement banni");
                    return Packet::new(PacketType::Login, b"Compte temporairement banni".to_vec());
                }

                // 5. Vérifier le mot de passe
                let password_valid = verify_password(&password, &login_data.password_hash);

                // 6. Mot de passe incorrect
                if !password_valid {
                    let attempts = match sqlx::query_scalar::<_, i64>(
                        r#"
                        INSERT INTO login_attempts (
                            user_id,
                            failed_attempts,
                            last_attempt
                        )
                        VALUES (
                            ?,
                            1,
                            CURRENT_TIMESTAMP
                        )
                        ON CONFLICT(user_id)
                        DO UPDATE SET
                            failed_attempts = failed_attempts + 1,
                            last_attempt = CURRENT_TIMESTAMP
                        RETURNING failed_attempts
                        "#,
                    )
                    .bind(&login_data.user_id)
                    .fetch_one(&pool)
                    .await
                    {
                        Ok(value) => value,
                        Err(error) => {
                            error!("Erreur lors de l'enregistrement de la tentative : {}", error);
                            return Packet::new(PacketType::Login, b"Erreur serveur".to_vec());
                        }
                    };

                    debug!("Mot de passe incorrect pour {} : tentative {}", email, attempts);

                    // 3 échecs → ban de 10 minutes
                    if attempts >= 3 {
                        match sqlx::query(
    r#"
    INSERT INTO bansferme (
        user_id,
        auteur,
        raison,
        date_ban,
        date_deban
    )
    VALUES (
        ?,
        'system',
        'Trop de tentatives de connexion échouées',
        CURRENT_TIMESTAMP,
        datetime(CURRENT_TIMESTAMP, '+10 minutes')
    )
    ON CONFLICT(user_id)
    DO UPDATE SET
        auteur = CASE
            WHEN instr(bansferme.auteur, 'system') = 0
            THEN bansferme.auteur || ', system'
            ELSE bansferme.auteur
        END,

        raison = CASE
            WHEN instr(
                bansferme.raison,
                'Trop de tentatives de connexion échouées'
            ) = 0
            THEN bansferme.raison
                 || ' | '
                 || 'Trop de tentatives de connexion échouées'
            ELSE bansferme.raison
        END,

        date_ban = CURRENT_TIMESTAMP,

        date_deban = CASE
            WHEN bansferme.date_deban > CURRENT_TIMESTAMP
            THEN datetime(bansferme.date_deban, '+10 minutes')
            ELSE datetime(CURRENT_TIMESTAMP, '+10 minutes')
        END
    "#,
)
.bind(&login_data.user_id)
.execute(&pool)
.await
{
    Err(error) => {
        error!("Impossible de créer le ban temporaire : {}", error);
        return Packet::new(PacketType::Login, b"Erreur serveur".to_vec());
    }
    Ok(_) => {}
}

                        // Supprimer le compteur
                        if let Err(error) = sqlx::query(
                            r#"
                            DELETE FROM login_attempts
                            WHERE user_id = ?
                            "#,
                        )
                        .bind(&login_data.user_id)
                        .execute(&pool)
                        .await
                        {
                            error!("Impossible de supprimer le compteur : {}", error);
                        }

                        debug!("Utilisateur {} banni pendant 10 minutes", email);

                        return Packet::new(PacketType::Login, b"Trop de tentatives. Compte bloque pendant 10 minutes.".to_vec());
                    }

                    return Packet::new(PacketType::Login, b"Identifiants invalides".to_vec());
                }

                // 7. ✅ OPTIMISATION OPTION 2 : Vérification en lecture rapide + UPDATE simple
                // Vérifier d'abord si déjà connecté (lecture rapide, pas de lock)
                let is_already_connected = match sqlx::query_scalar::<_, i64>(
                    r#"
                    SELECT EXISTS(
                        SELECT 1
                        FROM users
                        WHERE user_id = ?
                          AND status = 'CONNECTED'
                    )
                    "#,
                )
                .bind(&login_data.user_id)
                .fetch_one(&pool)
                .await
                {
                    Ok(value) => value != 0,
                    Err(error) => {
                        error!("Erreur lors de la vérification de connexion : {}", error);
                        return Packet::new(PacketType::Login, b"Erreur serveur".to_vec());
                    }
                };

                if is_already_connected {
                    debug!("Tentative de connexion avec un compte déjà connecté");
                    return Packet::new(PacketType::Login, b"Ce compte est deja connecte".to_vec());
                }

                // 8. UPDATE direct sans WHERE complexe (très rapide)
                if let Err(error) = sqlx::query(
                    r#"
                    UPDATE users
                    SET status = 'CONNECTED'
                    WHERE user_id = ?
                    "#,
                )
                .bind(&login_data.user_id)
                .execute(&pool)
                .await
                {
                    error!("Erreur lors de la connexion du joueur : {}", error);
                    return Packet::new(PacketType::Login, b"Erreur serveur".to_vec());
                }

                // 9. Connexion réussie → remettre le compteur à zéro
                if let Err(error) = sqlx::query(
                    r#"
                    DELETE FROM login_attempts
                    WHERE user_id = ?
                    "#,
                )
                .bind(&login_data.user_id)
                .execute(&pool)
                .await
                {
                    error!("Impossible de réinitialiser les tentatives : {}", error);
                    return Packet::new(PacketType::Login, b"Erreur serveur".to_vec());
                }

                // 10. Connexion réussie
                debug!("Utilisateur authentifié : {}", email);
                client.user_id = Some(login_data.user_id.clone());
                Packet::new(PacketType::Login, format!("Utilisateur {} authentifié", email).into_bytes())
            },

            PacketType::Chat => {
                debug!("Message : {}", String::from_utf8_lossy(&packet.payload));
                Packet::new(PacketType::Chat, packet.payload)
            },

            PacketType::Move => {
                debug!("Déplacement reçu");
                Packet::new(PacketType::Move, packet.payload)
            },
        }
    }
}
