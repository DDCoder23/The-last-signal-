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
    print(response)
    client.send_packet(
    Packet(
        PacketType.CHAT,
        b"Momo dirige le jeu"
    )
  )
    response = client.receive_packet()
    print(response)
    client.disconnect()
