use crate::network::packet::{
    Packet,
    PacketType,
};


pub struct PacketHandler;


impl PacketHandler {

    pub fn handle(packet: Packet) -> Packet {

        match packet.packet_type {

            PacketType::Ping => {

                println!("Ping reçu");

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

                println!(
                    "Connexion joueur : {}",
                    username
                );


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

                let message =
                    String::from_utf8_lossy(
                        &packet.payload
                    );


                println!(
                    "Message : {}",
                    message
                );


                Packet::new(
                    PacketType::Chat,
                    packet.payload,
                )

            }


            PacketType::Move => {

                println!("Déplacement reçu");


                Packet::new(
                    PacketType::Move,
                    packet.payload,
                )

            }

        }

    }

}
