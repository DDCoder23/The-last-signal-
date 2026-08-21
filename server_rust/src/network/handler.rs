use crate::network::packet::{
    Packet,
    PacketType,LogLevel,ClientLog,
};
use crate::network::client::Client;
use crate:: network::parser::{parse_login_payload,parse_signup_payload};
use log::{trace, debug, info, warn, error};
pub struct PacketHandler;
use crate::utils::password::{verify_password,hash_password};
use sqlx::SqlitePool;
use uuid::Uuid;
impl PacketHandler {

    pub async fn handle(
        _client: &mut Client,
        packet: Packet,
        pool: SqlitePool,
    ) -> Packet {

        match packet.packet_type {
            PacketType::Log => {

    let log = match serde_json::from_slice::<ClientLog>(&packet.payload) {
        Ok(log) => log,
        Err(e) => {
            error!("Impossible de décoder le paquet LOG : {}", e);

            return Packet::new(
                PacketType::Log,
                b"INVALID_LOG".to_vec(),
            );
        }
    };

    match log.level {
        LogLevel::TRACE => {
            trace!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            );
        }

        LogLevel::DEBUG => {
            debug!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            );
        }

        LogLevel::INFO => {
            info!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            );
        }

        LogLevel::WARNING => {
            warn!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            );
        }

        LogLevel::ERROR => {
            error!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            );
        }
    }

    Packet::new(
        PacketType::Log,
        b"OK".to_vec(),
    )
            }
            PacketType::Ping => {

                debug!("Ping reçu");

                Packet::new(
                    PacketType::Ping,
                    b"PONG".to_vec(),
                )

            }
            PacketType::SignUp => {

    // ========================================================
    // 1. Parser le packet SIGN_UP
    // ========================================================

    let (email, password) =
        match parse_signup_payload(&packet.payload) {

            Ok(signup) => signup,

            Err(error) => {

                debug!(
                    "SIGN_UP invalide : {}",
                    error
                );

                return Packet::new(
                    PacketType::SignUp,
                    b"SIGN_UP invalide".to_vec(),
                );
            }
        };


    // ========================================================
    // 2. Vérifier que l'email n'existe pas
    // ========================================================

    let email_exists = match sqlx::query_scalar(
        r#"
        SELECT EXISTS(
            SELECT 1
            FROM users
            WHERE email = ?
        )
        "#,
    )
    .bind(email)
    .fetch_one(&pool)
    .await
    {
        Ok(value) => value != 0,

        Err(error) => {

            error!(
                "Erreur lors de la vérification de l'email : {}",
                error
            );

            return Packet::new(
                PacketType::SignUp,
                b"Erreur serveur".to_vec(),
            );
        }
    };


    if email_exists {

        debug!(
            "SIGN_UP refusé : email déjà utilisé"
        );

        return Packet::new(
            PacketType::SignUp,
            b"Email deja utilise".to_vec(),
        );
    }


    // ========================================================
    // 3. Générer le hash Argon2
    // ========================================================

    let password_hash =
        match hash_password(&password) {

            Ok(hash) => hash,

            Err(error) => {

                error!(
                    "Erreur lors du hash du mot de passe : {}",
                    error
                );

                return Packet::new(
                    PacketType::SignUp,
                    b"Erreur serveur".to_vec(),
                );
            }
        };


    // ========================================================
    // 4. Générer le user_id
    // ========================================================

    let user_id =
        Uuid::new_v4().to_string();


    // ========================================================
    // 5. Créer le user
    // ========================================================

    if let Err(error) = sqlx::query(
        r#"
        INSERT INTO users (
            user_id,
            email,
            password_hash
        )
        VALUES (?, ?, ?)
        "#,
        )
        .bind(user_id)
        .bind(email)
        .bind(password_hash)
    .execute(&pool)
    .await
    {
        error!(
            "Erreur lors de la création du user : {}",
            error
        );

        return Packet::new(
            PacketType::SignUp,
            b"Impossible de creer le compte utilisateur".to_vec(),
        );
    }


    // ========================================================
    // 6. Succès
    // ========================================================

    debug!(
        "Nouvel utilisateur créé : {}",
        email
    );


    Packet::new(
        PacketType::SignUp,
        b"Utilisateur cree avec succes".to_vec(),
    )
            }

            
            PacketType::Login => {

    // ========================================================
    // 1. Parser le packet LOGIN
    // ========================================================

    let (email, password) =
        match parse_login_payload(&packet.payload) {

            Ok(login) => login,

            Err(error) => {

                debug!(
                    "LOGIN invalide : {}",
                    error
                );

                return Packet::new(
                    PacketType::Login,
                    b"LOGIN invalide".to_vec(),
                );
            }
        };


    // ========================================================
    // 2. Chercher l'utilisateur
    // ========================================================

    let user = match sqlx::query(
        r#"
        SELECT
            user_id,
            password_hash
        FROM users
        WHERE email = ?
        "#,)
        .bind(email)
    .fetch_optional(&pool)
    .await
    {
        Ok(Some(user)) => user,

        Ok(None) => {

            debug!(
                "Tentative de connexion avec un utilisateur inexistant"
            );

            return Packet::new(
                PacketType::Login,
                b"Identifiants invalides".to_vec(),
            );
        }

        Err(error) => {

            error!(
                "Erreur lors de la recherche de l'utilisateur : {}",
                error
            );

            return Packet::new(
                PacketType::Login,
                b"Erreur serveur".to_vec(),
            );
        }
    };


    // ========================================================
    // 3. Vérifier le ban permanent
    // ========================================================

    let banned_permanently =
        match sqlx::query_scalar(
            r#"
            SELECT EXISTS(
                SELECT 1
                FROM bansperm
                WHERE user_id = ?
            )
            "#,)
            .bind(user.user_id)
        .fetch_one(&pool)
        .await
        {
            Ok(value) => value != 0,

            Err(error) => {

                error!(
                    "Erreur lors de la vérification de bansperm : {}",
                    error
                );

                return Packet::new(
                    PacketType::Login,
                    b"Erreur serveur".to_vec(),
                );
            }
        };


    if banned_permanently {

        debug!(
            "Connexion refusée : utilisateur banni définitivement"
        );

        return Packet::new(
            PacketType::Login,
            b"Compte banni definitivement".to_vec(),
        );
    }


    // ========================================================
    // 4. Vérifier le ban temporaire
    // ========================================================

    let banned_temporarily =
        match sqlx::query_scalar!(
            r#"
            SELECT EXISTS(
                SELECT 1
                FROM bansferme
                WHERE user_id = ?
                  AND datetime(date_deban) > CURRENT_TIMESTAMP
            )
            "#,)
            .bind(user.user_id)
        .fetch_one(&pool)
        .await
        {
            Ok(value) => value != 0,

            Err(error) => {

                error!(
                    "Erreur lors de la vérification de bansferme : {}",
                    error
                );

                return Packet::new(
                    PacketType::Login,
                    b"Erreur serveur".to_vec(),
                );
            }
        };


    if banned_temporarily {

        debug!(
            "Connexion refusée : utilisateur temporairement banni"
        );

        return Packet::new(
            PacketType::Login,
            b"Compte temporairement banni".to_vec(),
        );
    }


    // ========================================================
    // 5. Vérifier le mot de passe
    // ========================================================

    let password_valid = verify_password(
        &password,
        &user.password_hash,
    );


    // ========================================================
    // 6. Mot de passe incorrect
    // ========================================================

    if !password_valid {

        let attempts = match sqlx::query_scalar(
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
                failed_attempts =
                    failed_attempts + 1,

                last_attempt =
                    CURRENT_TIMESTAMP

            RETURNING failed_attempts
            "#,)
            .bind(user.user_id)
        .fetch_one(&pool)
        .await
        {
            Ok(value) => value,

            Err(error) => {

                error!(
                    "Erreur lors de l'enregistrement de la tentative : {}",
                    error
                );

                return Packet::new(
                    PacketType::Login,
                    b"Erreur serveur".to_vec(),
                );
            }
        };


        debug!(
            "Mot de passe incorrect pour {} : tentative {}",
            email,
            attempts
        );


        // ====================================================
        // 3 échecs → ban de 10 minutes
        // ====================================================

        if attempts >= 3 {

            if let Err(error) = sqlx::query(
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
                    datetime(
                        CURRENT_TIMESTAMP,
                        '+10 minutes'
                    )
                )

                ON CONFLICT(user_id)
                DO UPDATE SET
                    auteur = 'system',

                    raison =
                        'Trop de tentatives de connexion échouées',

                    date_ban =
                        CURRENT_TIMESTAMP,

                    date_deban =
                        datetime(
                            CURRENT_TIMESTAMP,
                            '+10 minutes'
                        )
                "#,)
                .bind(user.user_id
            )
            .execute(&pool)
            .await
            {
                error!(
                    "Impossible de créer le ban temporaire : {}",
                    error
                );

                return Packet::new(
                    PacketType::Login,
                    b"Erreur serveur".to_vec(),
                );
            }


            // =================================================
            // Supprimer le compteur
            // =================================================

            if let Err(error) = sqlx::query!(
                r#"
                DELETE FROM login_attempts
                WHERE user_id = ?
                "#,
                user.user_id
            )
            .execute(&pool)
            .await
            {
                error!(
                    "Impossible de supprimer le compteur : {}",
                    error
                );
            }


            debug!(
                "Utilisateur {} banni pendant 10 minutes",
                email
            );


            return Packet::new(
                PacketType::Login,
                b"Trop de tentatives. Compte bloque pendant 10 minutes."
                    .to_vec(),
            );
        }


        // ====================================================
        // Échec mais moins de 3 tentatives
        // ====================================================

        return Packet::new(
            PacketType::Login,
            b"Identifiants invalides".to_vec(),
        );
    }


    // ========================================================
    // 7. Connexion réussie → remettre le compteur à zéro
    // ========================================================

    if let Err(error) = sqlx::query(
        r#"
        DELETE FROM login_attempts
        WHERE user_id = ?
        "#,)
        .bind(user.user_id
    )
    .execute(&pool)
    .await
    {
        error!(
            "Impossible de réinitialiser les tentatives : {}",
            error
        );

        return Packet::new(
            PacketType::Login,
            b"Erreur serveur".to_vec(),
        );
    }


    // ========================================================
    // 8. Connexion réussie
    // ========================================================

    debug!(
        "Utilisateur authentifié : {}",
        email
    );


    Packet::new(
        PacketType::Login,
        format!(
            "Utilisateur {} authentifié",
            email
        )
        .into_bytes(),
    )
            }

            PacketType::Chat => {

                debug!(
                    "Message : {}",
                    String::from_utf8_lossy(
                        &packet.payload
                    )
                );

                Packet::new(
                    PacketType::Chat,
                    packet.payload,
                )

            }

            PacketType::Move => {

                debug!("Déplacement reçu");

                Packet::new(
                    PacketType::Move,
                    packet.payload,
                )

            }

        }

    }

}


        
