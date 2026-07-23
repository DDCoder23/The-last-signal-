from ..packet import Packet, PacketType


class LoginPacket(Packet):

    def __init__(self, username):

        self.username = username

        super().__init__(
            PacketType.LOGIN,
            username.encode("utf-8")
        )
    @classmethod
    def from_payload(cls, payload):

        username = payload.decode(
            "utf-8"
        )

        return cls(username)
