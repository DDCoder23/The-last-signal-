import struct

from ..packet import Packet, PacketType


class MovePacket(Packet):

    def __init__(self, x, y,z):

        self.x = x
        self.y = y
        self.z = z

        super().__init__(
            PacketType.MOVE,
            struct.pack("!ff", x, y, z)
        )
