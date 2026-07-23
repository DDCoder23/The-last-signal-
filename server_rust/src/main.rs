use std::{
    io::{Read, Result},
    net::{TcpListener, TcpStream},
    thread,
};

/// Reçoit exactement `size` octets.
fn recv_exact(stream: &mut TcpStream, size: usize) -> Result<Vec<u8>> {
    let mut buffer = vec![0u8; size];
    stream.read_exact(&mut buffer)?;
    Ok(buffer)
}

/// Reçoit un paquet au format :
/// [4 octets : taille][données]
fn receive_packet(stream: &mut TcpStream) -> Result<Vec<u8>> {
    // Lecture de la taille
    let header = recv_exact(stream, 4)?;

    let size = u32::from_be_bytes([
        header[0],
        header[1],
        header[2],
        header[3],
    ]) as usize;

    // Sécurité
    const MAX_PACKET_SIZE: usize = 10 * 1024 * 1024;

    if size > MAX_PACKET_SIZE {
        panic!("Paquet trop volumineux : {}", size);
    }

    // Lecture des données
    recv_exact(stream, size)
}

/// Gère un client.
fn handle_client(mut stream: TcpStream) {
    println!(
        "Client connecté : {}",
        stream.peer_addr().unwrap()
    );

    loop {
        match receive_packet(&mut stream) {
            Ok(packet) => {
                println!(
                    "Paquet reçu ({} octets)",
                    packet.len()
                );

                println!(
                    "{}",
                    String::from_utf8_lossy(&packet)
                );
            }

            Err(e) => {
                println!("Client déconnecté : {}", e);
                break;
            }
        }
    }
}

fn main() {
    println!("==============================");
    println!("   The Last Signal Server");
    println!("==============================");

    let listener = TcpListener::bind("127.0.0.1:5000")
        .expect("Impossible de démarrer le serveur");

    println!("Listening on 127.0.0.1:5000");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                thread::spawn(move || {
                    handle_client(stream);
                });
            }

            Err(e) => {
                eprintln!("Erreur : {}", e);
            }
        }
    }
                                  }
