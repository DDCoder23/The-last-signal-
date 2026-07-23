from ..packet import Packet, PacketType


class ChatPacket(Packet):

    def __init__(self, message):

        self.message = message

        super().__init__(
            PacketType.CHAT,
            message.encode("utf-8")
        )
