from enum import IntEnum
import struct


class PacketType(IntEnum):

    PING = 1
    LOGIN = 2
    CHAT = 3
    MOVE = 4


class Packet:

    def __init__(
        self,
        packet_type,
        payload=b""
    ):

        self.packet_type = PacketType(packet_type)
        self.payload = payload


    def encode(self):

        body = (
            struct.pack(
                "!H",
                self.packet_type
            )
            +
            self.payload
        )

        return (
            struct.pack(
                "!I",
                len(body)
            )
            +
            body
        )


    @staticmethod
    def decode(data):

        packet_type = PacketType(
            struct.unpack(
                "!H",
                data[:2]
            )[0]
        )

        payload = data[2:]


        if packet_type == PacketType.LOGIN:
            from .packets.login import LoginPacket
            return LoginPacket.from_payload(payload)


        if packet_type == PacketType.CHAT:
            from .packets.chat import ChatPacket
            return ChatPacket.from_payload(payload)


        if packet_type == PacketType.MOVE:
            from .packets.move import MovePacket
            return MovePacket.from_payload(payload)


        if packet_type == PacketType.PING:
            from .packets.ping import PingPacket
            return PingPacket()


        return Packet(
            packet_type,
            payload
        )
