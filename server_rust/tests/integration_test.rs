use the_last_signal_server::packet::PacketType;

#[test]
fn test_packet_login() {
    assert_eq!(PacketType::Login as u8, 2);
}
