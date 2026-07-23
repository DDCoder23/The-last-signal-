use std::io::{self, Read, Write};
use std::net::TcpStream;

pub const MAX_PACKET_SIZE: usize = 10 * 1024 * 1024;

/// Types de paquets.
#[repr(u16)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PacketType {
    Ping = 1,
    Login = 2,
    Chat = 3,
    Move = 4,
}

impl PacketType {
    pub fn from_u16(value: u16) -> Option<Self> {
        match value {
            1 => Some(PacketType::Ping),
            2 => Some(PacketType::Login),
            3 => Some(PacketType::Chat),
            4 => Some(PacketType::Move),
            _ => None,
        }
    }
}

/// Un paquet réseau.
#[derive(Debug, Clone)]
pub struct Packet {
    pub packet_type: PacketType,
    pub payload: Vec<u8>,
}

impl Packet {
    pub fn new(
        packet_type: PacketType,
        payload: Vec<u8>,
    ) -> Self {
        Self {
            packet_type,
            payload,
        }
    }
}

/// Envoie un paquet.
pub fn send_packet(
    stream: &mut TcpStream,
    packet: &Packet,
) -> io::Result<()> {

    let payload_size = 2 + packet.payload.len();

    if payload_size > MAX_PACKET_SIZE {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "Paquet trop volumineux.",
        ));
    }

    let size = (payload_size as u32).to_be_bytes();

    stream.write_all(&size)?;

    let packet_type =
        (packet.packet_type as u16).to_be_bytes();

    stream.write_all(&packet_type)?;

    stream.write_all(&packet.payload)?;

    Ok(())
}

/// Reçoit exactement `size` octets.
fn recv_exact(
    stream: &mut TcpStream,
    size: usize,
) -> io::Result<Vec<u8>> {

    let mut buffer = vec![0u8; size];

    stream.read_exact(&mut buffer)?;

    Ok(buffer)
}

/// Reçoit un paquet.
pub fn receive_packet(
    stream: &mut TcpStream,
) -> io::Result<Packet> {

    // Taille
    let header = recv_exact(stream, 4)?;

    let size = u32::from_be_bytes([
        header[0],
        header[1],
        header[2],
        header[3],
    ]) as usize;

    if size < 2 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "Paquet invalide.",
        ));
    }

    if size > MAX_PACKET_SIZE {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "Paquet trop volumineux.",
        ));
    }

    // Corps du paquet
    let data = recv_exact(stream, size)?;

    // Type
    let packet_type =
        u16::from_be_bytes([data[0], data[1]]);

    let packet_type =
        PacketType::from_u16(packet_type)
            .ok_or_else(|| {
                io::Error::new(
                    io::ErrorKind::InvalidData,
                    "Type de paquet inconnu.",
                )
            })?;

    // Payload
    let payload = data[2..].to_vec();

    Ok(Packet {
        packet_type,
        payload,
    })
}
