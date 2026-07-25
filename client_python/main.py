from .client import Client
import time
from .packets.chat import ChatPacket
from .packets.login import LoginPacket
from .packets.ping import PingPacket
from .packets.move import MovePacket
def main():
    client = Client()
    client2 = Client()
    client.connect()
    time.sleep(1)
    client2.connect()
    client.send_packet(LoginPacket("Momo"))
    response = client.receive_packet()
    print(response.username)
    client.send_packet(
        ChatPacket("Momo dirige le jeu")
  )
    response = client.receive_packet()
    print(response.message)
    client.disconnect()
