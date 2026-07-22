use std::net::TcpListener;

fn main() {

    let listener = TcpListener::bind("127.0.0.1:5000")
        .expect("Impossible de démarrer le serveur");

    println!("The Last Signal Server");
    println!("Listening on 127.0.0.1:5000");

    for stream in listener.incoming() {

        match stream {

            Ok(_) => {

                println!("Client connecté");

            }

            Err(e) => {

                println!("Erreur : {}", e);

            }

        }

    }

}
