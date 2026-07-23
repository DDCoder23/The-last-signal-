use std::net::TcpStream;

use crate::network::packet::{
    receive_packet,
    send_packet,
};

pub struct Client {
    stream: TcpStream,
}

impl Client {
    pub fn new(stream: TcpStream) -> Self {
        Self {
            stream,
        }
    }

    pub fn run(&mut self) {
        println!(
            "Client connecté : {}",
            self.stream.peer_addr().unwrap()
        );

        loop {

            match receive_packet(&mut self.stream) {

                Ok(packet) => {

                    println!(
                        "Type : {:?}",
                        packet.packet_type
                    );

                    println!(
                        "Payload : {}",
                        String::from_utf8_lossy(
                            &packet.payload
                        )
                    );

                    if let Err(e) = send_packet(
                        &mut self.stream,
                        &packet,
                    ) {

                        println!("Erreur : {}", e);

                        break;

                    }

                }

                Err(e) => {

                    println!(
                        "Déconnexion : {}",
                        e
                    );

                    break;

                }

            }

        }

    }

}
