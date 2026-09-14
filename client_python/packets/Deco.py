from ..packet import Packet, PacketType

class decoPacket:

  def __init__(
    self,
    deco_type,
    reason,
  ):
    self.packet_type = PacketType.DECO
    self.deco_type = deco_type
    self.reason = reason

@classmethod
def from_payload(cls,payload):

  parts = payload.decode("utf-8").split("\0")

deco_type = int(part[0])
reason = part[1]

return cls(
  ban_type,
  reason,
)
