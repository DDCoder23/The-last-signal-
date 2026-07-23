from enum import IntEnum
import struct


class PacketType(IntEnum):
    PING = 1
    LOGIN = 2
    CHAT = 3
    MOVE = 4


class Packet:
    """
    Classe de base de tous les paquets.
    """

    def __init__(self, packet_type, payload=b""):

        self.packet_type = PacketType(packet_type)
        self.payload = payload
    @classmethod
    def encode(self):
        """
        Encode le paquet.

        Format :
            [4 octets : taille]
            [2 octets : type]
            [payload]
        """

        body = (
            struct.pack("!H", self.Packet_type)
            + self.payload
        )

        header = struct.pack(
            "!I",
            len(body)
        )

        return header + body

    @classmethod
    def decode(cls, data):

        packet_type = PacketType(
            struct.unpack(
                "!H",
                data[:2]
            )[0]
        )

        payload = data[2:]

        return cls(
            packet_type,
            payload
        )

    def __repr__(self):

        return (
            f"{self.__class__.__name__}"
            f"(type={self.packet_type.name}, "
            f"payload={self.payload!r})"
        )
