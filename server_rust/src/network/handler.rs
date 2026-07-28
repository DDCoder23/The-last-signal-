use crate::network::packet::{
    Packet,
    PacketType,LogLevel,ClientLog,
};
use crate::network::client::Client;
use log::debug;
pub struct PacketHandler;


impl PacketHandler {

    pub async fn handle(
        _client: &mut Client,
        packet: Packet,
    ) -> Packet {

        match packet.packet_type {
            PacketType::Log => {

    let log: ClientLog =
        serde_json::from_slice(&packet.payload)?;

    match log.level {

        LogLevel::Trace =>
            trace!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            ),

        LogLevel::Debug =>
            debug!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            ),

        LogLevel::Info =>
            info!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            ),

        LogLevel::Warn =>
            warn!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            ),

        LogLevel::Error =>
            error!(
                "[CLIENT] [{}:{}] {}",
                log.file,
                log.line,
                log.message
            ),
    }
            }

            PacketType::Ping => {

                debug!("Ping reçu");

                Packet::new(
                    PacketType::Ping,
                    b"PONG".to_vec(),
                )

            }

            PacketType::Login => {

                let username =
                    String::from_utf8_lossy(
                        &packet.payload
                    );

                debug!(
                    "Connexion joueur : {}",
                    username
                );

                // Ici, plus tard :
                // - rechercher le client
                // - rechercher le compte
                // - créer une session
                // - logger la connexion

                Packet::new(
                    PacketType::Login,
                    format!(
                        "Bienvenue {}",
                        username
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


        
