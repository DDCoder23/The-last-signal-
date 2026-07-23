use std::net::TcpStream;

use crate::network::packet::{
    receive_packet,
    send_packet,
};
use crate::network::handler::PacketHandler;
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


                       let response =
                              PacketHandler::handle(packet);

                    if let Err(e) = send_packet(
                        &mut self.stream,
                        &reponse,
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
