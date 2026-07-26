use tokio::net::TcpStream;
use sqlx::PgPool;
use uuid::Uuid;

use crate::network::handler::PacketHandler;
use crate::network::packet::{
    receive_packet,
    send_packet,
};

pub struct Client {
    stream: TcpStream,

    pool: PgPool,

    session_id: Uuid,

    client_id: Option<i64>,

    account_id: Option<Uuid>,
}

impl Client {

    pub fn new(
        stream: TcpStream,
        pool: PgPool,
    ) -> Self {

        Self {

            stream,

            pool,

            session_id: Uuid::new_v4().to_string(),

            client_id: None,

            account_id: None,

        }

    }

    pub async fn run(&mut self) {

        println!(
            "Client connecté : {} | Session : {}",
            self.stream.peer_addr().unwrap(),
            self.session_id,
        );

        loop {

            match receive_packet(&mut self.stream).await {

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
                     PacketHandler::handle(self, packet)
                     .await;
                    if let Err(e) =
                        send_packet(
                            &mut self.stream,
                            &response,
                        )
                        .await
                    {

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
