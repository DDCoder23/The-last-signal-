use std::net::TcpListener;
use std::thread;

use crate::network::client::Client;

pub struct Server {

    listener: TcpListener,

}

impl Server {

    pub fn new(address: &str) -> Self {

        let listener =
            TcpListener::bind(address)
                .expect("Impossible de démarrer le serveur.");

        Self {

            listener,

        }

    }

    pub fn start(&self) {

        println!("The Last Signal Server");

        println!(
            "Listening on {}",
            self.listener.local_addr().unwrap()
        );

        for stream in self.listener.incoming() {

            match stream {

                Ok(stream) => {

                    thread::spawn(move || {

                        let mut client =
                            Client::new(stream);

                        client.run();

                    });

                }

                Err(e) => {

                    println!("{}", e);

                }

            }

        }

    }

}
