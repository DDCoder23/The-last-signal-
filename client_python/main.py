from .client import Client
import time
from .packet import Packet, PacketType
def main():
    client = Client()
    client.connect()
    time.sleep(1)
    client.send_packet(
    Packet(
        PacketType.LOGIN,
        b"Momo"
    )
  )
    response = client.receive_packet()

    try:
        print(response.payload.decode("utf-8"))
    except UnicodeDecodeError:
        print(response.payload)
    client.disconnect()
