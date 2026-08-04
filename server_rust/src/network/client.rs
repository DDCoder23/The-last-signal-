use tokio::net::TcpStream;
use sqlx::Pool;
use uuid::Uuid;
use log::{
    info,
    debug,
    error,};
use crate::network::handler::PacketHandler;
use crate::network::packet::{
    receive_packet,
    send_packet,
};

pub struct Client {
    stream: TcpStream,

    pool: Pool,

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

            session_id: Uuid::new_v4(),

            client_id: None,

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

            match receive_packet(&mut self.stream).await {

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

                        error!("Erreur : {}", e);

                        break;

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

    }

}
