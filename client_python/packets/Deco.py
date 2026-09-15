from ..packet import Packet, PacketType

class decoPacket:

  def __init__(
    self,
    
    reason,
  ):
    
    self.reason = reason

@classmethod
def from_payload(cls, payload):
  return cls(
            payload.decode("utf-8")
        )
