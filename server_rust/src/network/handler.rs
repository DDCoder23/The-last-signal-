use crate::network::packet::{
    Packet,
    PacketType,LogLevel,ClientLog,
};
use crate::network::client::Client;
use crate:: network::parser::parse_login_payload;
use log::{trace, debug, info, warn, error};
pub struct PacketHandler;


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

    let user = match sqlx::query!(
        r#"
        SELECT
            user_id,
            password_hash
        FROM users
        WHERE email = ?
        "#,
        email
    )
    .fetch_optional(pool)
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
        match sqlx::query_scalar!(
            r#"
            SELECT EXISTS(
                SELECT 1
                FROM bansperm
                WHERE user_id = ?
            )
            "#,
            user.user_id
        )
        .fetch_one(pool)
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
            b"Compte banni définitivement".to_vec(),
        );
    }


    // ========================================================
    // 4. Vérifier le ban ferme
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
            "#,
            user.user_id
        )
        .fetch_one(pool)
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
    // 5. Vérification du mot de passe
    // ========================================================

    // TODO:
    // Vérifier `password` avec `user.password_hash`.


    debug!(
        "Utilisateur autorisé à poursuivre la connexion : {}",
        email
    );


    // ========================================================
    // 6. Pour l'instant : réponse temporaire
    // ========================================================

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


        
