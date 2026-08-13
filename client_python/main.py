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
    print(type(response))
    print(response)
    print(response.packet_type)
    print(response.username)
    client.send_packet(
        ChatPacket("Momo dirige le jeu")
  )
    response = client.receive_packet()
    client.send_packet(
        ChatPacket("Le serveur est en rust")
  )
    response = client.receive_packet()
    print(response.message)
    client.send_packet(
        ChatPacket("Le client est en python")
  )
    response = client.receive_packet()
    print(response.message)
    client.send_packet(
        ChatPacket("Tests des trésors en cours...")
  )
    response = client.receive_packet()
    print(response.message)
    client.disconnect()
