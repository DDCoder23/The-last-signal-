use std::io::{Read, Result, Write};
use std::net::TcpStream;

/// Taille maximale d'un paquet (10 Mo)
pub const MAX_PACKET_SIZE: usize = 10 * 1024 * 1024;

/// Reçoit exactement `size` octets.
pub fn recv_exact(
    stream: &mut TcpStream,
    size: usize,
) -> Result<Vec<u8>> {

    let mut buffer = vec![0u8; size];

    stream.read_exact(&mut buffer)?;

    Ok(buffer)
}

/// Reçoit un paquet.
///
/// Format :
///
/// [4 octets : taille]
/// [données]
pub fn receive_packet(
    stream: &mut TcpStream,
) -> Result<Vec<u8>> {

    let header = recv_exact(stream, 4)?;

    let size = u32::from_be_bytes([
        header[0],
        header[1],
        header[2],
        header[3],
    ]) as usize;

    if size > MAX_PACKET_SIZE {
        panic!("Paquet trop volumineux.");
    }

    recv_exact(stream, size)
}

/// Envoie un paquet.
pub fn send_packet(
    stream: &mut TcpStream,
    packet: &[u8],
) -> Result<()> {

    let size =
        (packet.len() as u32).to_be_bytes();

    stream.write_all(&size)?;

    stream.write_all(packet)?;

    Ok(())
}
