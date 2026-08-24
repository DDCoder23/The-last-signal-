use tokio::{net::TcpStream,time::{sleep, Duration},io::AsyncWriteExt};
use sqlx::SqlitePool;
use uuid::Uuid;
use log::{
    info,
    debug,
    error,};
use crate::network::handler::PacketHandler;

use crate::network::packet::{
    Packet,
    PacketType,
    receive_packet,
    send_packet,
    BanType,
    BanInfo,
};

pub struct Client {
    stream: TcpStream,

    pool: SqlitePool,

    session_id: Uuid,

    client_id: Option<i64>,

    user_id: Option<String>,

    account_id: Option<i64>,
}

impl Client {

    pub fn new(
        stream: TcpStream,
        pool: SqlitePool,
    ) -> Self {

        Self {

            stream,

            pool,

            session_id: Uuid::new_v4(),
            client_id: None,

            user_id: None,

            account_id: None,

        }

    }

    pub async fn run(&mut self) {

        info!(
            "Client connecté : {} | Session : {}",
            self.stream.peer_addr().unwrap(),
            self.session_id,
        );
        loop {

            tokio::select! {

                // =====================================================
                // Réception des paquets
                // =====================================================

                packet = receive_packet(&mut self.stream) => {

                    match packet {

                        Ok(packet) => {

                            debug!(
                                "Type : {:?}",
                                packet.packet_type
                            );

                            debug!(
                                "Payload : {}",
                                String::from_utf8_lossy(
                                    &packet.payload
                                )
                            );

                            if let Some(response) =
                                PacketHandler::handle(
                                    self,
                                    packet,
                                    self.pool.clone()
                                ).await
                            {

                                if let Err(e) =
                                    send_packet(
                                        &mut self.stream,
                                        &response
                                    ).await
                                {
                                    error!(
                                        "Erreur d'envoi [{}] : {}",
                                        self.session_id,
                                        e
                                    );

                                    break;
                                }
                            }
                        }

                        Err(e) => {

                            error!(
                                "Déconnexion [{}] : {}",
                                self.session_id,
                                e
                            );

                            break;
                        }
                    }
                }

                // =====================================================
                // Vérification du ban toutes les secondes
                // =====================================================

                _ = sleep(Duration::from_secs(1)) => {

                    match self.get_ban_info().await {

                        Ok(Some(ban)) => {

                            info!(
                                "Client banni : {} | Type : {:?} | Raison : {}",
                                self.session_id,
                                ban.ban_type,
                                ban.reason
                            );

                            // -------------------------------------------------
                            // Construction du payload BAN
                            // -------------------------------------------------

                            let payload = Self::encode_ban_payload(
                                &ban
                            );

                            let packet = Packet::new(PacketType::BAN,payload);
                            if let Err(e) =
                                            send_packet(&mut self.stream, &packet).await
                            {
                               error!(
                                        "Impossible d'envoyer le BAN [{}] : {}",
                                        self.session_id,
                                          e
                                   );
                             }



                            // -------------------------------------------------
                            // Fermeture de la connexion
                            // -------------------------------------------------

                            self.disconnect().await;

                            break;
                        }

                        Ok(None) => {
                            // Aucun ban actif.
                        }

                        Err(e) => {

                            error!(
                                "Erreur vérification ban [{}] : {}",
                                self.session_id,
                                e
                            );

                            break;
                        }
                    }
                }
            }
        }

        info!(
            "Fin de session : {}",
            self.session_id
        );
    }

        

    
    pub async fn get_ban_info(
        &self,
    ) -> Result<Option<BanInfo>, sqlx::Error> {

        let user_id = match self.user_id() {

            Some(id) => id,

            None => {
                return Ok(None);
            }
        };

        // ---------------------------------------------------------
        // Ban permanent
        // ---------------------------------------------------------

        if let Some((reason,)) = sqlx::query_as::<_, (String,)>(
            r#"
            SELECT raison
            FROM bansperm
            WHERE user_id = ?
            LIMIT 1
            "#
        )
        .bind(user_id)
        .fetch_optional(&self.pool)
        .await?
        {
            return Ok(Some(BanInfo {
                ban_type: BanType::Permanent,
                reason,
                date_deban: None,
            }));
        }

        // ---------------------------------------------------------
        // Ban temporaire
        // ---------------------------------------------------------

        if let Some((reason, date_deban)) =
            sqlx::query_as::<_, (Option<String>, String)>(
                r#"
                SELECT raison, date_deban
                FROM bansferme
                WHERE user_id = ?
                  AND datetime(date_deban) > CURRENT_TIMESTAMP
                LIMIT 1
                "#
            )
            .bind(user_id)
            .fetch_optional(&self.pool)
            .await?
        {
            return Ok(Some(BanInfo {
                ban_type: BanType::Temporary,

                reason: reason.unwrap_or_else(
                    || "Aucune raison fournie".to_string()
                ),

                date_deban: Some(date_deban),
            }));
        }

        Ok(None)
    }
    fn encode_ban_payload(
        ban: &BanInfo,
    ) -> Vec<u8> {

        format!(
            "{}\0{}\0{}",
            ban.ban_type as u8,
            ban.reason,
            ban.date_deban
                .as_deref()
                .unwrap_or("")
        )
        .into_bytes()
    }

    // Encapsulation: setters / getters for previously-private fields
    pub fn set_user_id(&mut self, id: Option<String>) {
        self.user_id = id;
    }

    pub fn user_id(&self) -> Option<&str> {
        self.user_id.as_deref()
    }

    pub fn set_client_id(&mut self, id: Option<i64>) {
        self.client_id = id;
    }

    pub fn client_id(&self) -> Option<i64> {
        self.client_id
    }

    pub fn set_account_id(&mut self, id: Option<i64>) {
        self.account_id = id;
    }

    pub fn account_id(&self) -> Option<i64> {
        self.account_id
    }
pub async fn disconnect(&mut self) {
    if let Err(e) = self.stream.shutdown().await {
        error!(
            "Erreur lors de la déconnexion [{}] : {}",
            self.session_id,
            e
        );
    } else {
        info!(
            "Client déconnecté : {}",
            self.session_id
        );
    }
}

}
