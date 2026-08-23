use tokio::net::TcpStream;
use sqlx::SqlitePool;
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

                    if let Some(response) =
                     PacketHandler::handle(self, packet,self.pool.clone())
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

}
