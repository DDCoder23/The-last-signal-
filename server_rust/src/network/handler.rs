use crate::network::packet::{
    Packet,
    PacketType,LogLevel,ClientLog,
};
use crate::network::client::Client;
use crate:: network::client::parser::parse_login_payload;
use log::{trace, debug, info, warn, error};
pub struct PacketHandler;


impl PacketHandler {

    pub async fn handle(
        _client: &mut Client,
        packet: Packet,
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

    let (email, _password) =
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

    debug!(
        "Tentative de connexion : {}",
        email
    );

    Packet::new(
        PacketType::Login,
        format!(
            "Bienvenue {}",
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


        
