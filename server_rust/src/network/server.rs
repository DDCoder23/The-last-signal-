use tokio::net::TcpListener;
use tokio::task;

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
            .expect("Impossible de démarrer le serveur.");

        Self {
            listener,
            database,
        }
    }

    pub async fn start(&self) {

        println!("==================================");
        println!("The Last Signal Server");
        println!("==================================");

        println!(
            "Listening on {}",
            self.listener.local_addr().unwrap()
        );

        loop {

            match self.listener.accept().await {

                Ok((stream, address)) => {

                    println!("Client connecté : {}", address);

                    let pool = self.database.pool.clone();

                    task::spawn(async move {

                        let mut client =
                            Client::new(stream, pool);

                        client.run().await;

                    });

                }

                Err(e) => {

                    eprintln!(
                        "Erreur d'acceptation : {}",
                        e
                    );

                }

            }

        }

    }
}
