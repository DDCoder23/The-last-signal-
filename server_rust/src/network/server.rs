use tokio::net::TcpListener;
use tokio::task;
use log::{
    info,
    error,
    debug,
};
use crate::database::database_manager::DatabaseManager;
use crate::network::client::Client;

pub struct Server {
    listener: TcpListener,
    database: DatabaseManager,
}

impl Server {
    pub async fn new(
        address: &str,
        database: DatabaseManager,
    ) -> Self {

        let listener = TcpListener::bind(address)
            .await
            .expect(error!(Impossible de démarrer le serveur.));
             

        Self {
            listener,
            database,
        }
    }

    pub async fn start(&self) {

        debug!("==================================");
        debug!("The Last Signal Server");
        debug!("==================================");

        debug!(
            "Listening on {}",
            self.listener.local_addr().unwrap()
        );

        loop {

            match self.listener.accept().await {

                Ok((stream, address)) => {

                    info!("Client connecté : {}", address);

                    let pool = self.database.pool().clone();

                    task::spawn(async move {

                        let mut client =
                            Client::new(stream, pool);

                        client.run().await;

                    });

                }

                Err(e) => {

                error!(
                        "Erreur d'acceptation : {}",
                        e
                    );

                }

            }

        }

    }
}
