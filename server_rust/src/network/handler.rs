use crate::network::packet::{
    Packet,
    PacketType,
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


        
