use std::net::TcpStream;
use uuid::Uuid;


use crate::network::packet::{
    receive_packet,
    send_packet,
};
use crate::network::handler::PacketHandler;
pub struct Client {
    stream: TcpStream,
    session_id: String,
    client_id: Option<i64>,

    account_id: Option<i64>,
}
impl Client {
    pub fn new(stream: TcpStream) -> Self {
        Self {
            stream,
            session_id: Uuid::new_v4().to_string(),
            client_id: None,
            account_id: None
        }
    }

    pub fn run(&mut self) {
        println!(
            "Client connecté : {} | Session : {}",
            self.stream.peer_addr().unwrap()
            self.session_id
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
                        &response,
                    ) {

                        println!("Erreur : {}", e);

                        break;

                    }

                }

                Err(e) => {

                            println!(
    "Déconnexion [{}] : {}",
    self.session_id,
    e
);

                    break;

                }

            }

        }

    }

}
