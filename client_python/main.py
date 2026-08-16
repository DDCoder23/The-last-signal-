from .client import Client
import time
from .packet import Packet, PacketType
from .packets.chat import ChatPacket
from .packets.login import LoginPacket
from .packets.ping import PingPacket
from .packets.move import MovePacket
from security import vault
def main():
    client = Client()
    client2 = Client()
    client.connect()
    time.sleep(1)
    client2.connect()
    client.send_packet(LoginPacket("Momo"))
    response = client.receive_packet(PacketType.LOGIN)
    
    print(response.username if response != None else "Vide")
    
    
    client.send_packet(
        ChatPacket("Momo dirige le jeu")
  )
    response = client.receive_packet(PacketType.CHAT)
    client.send_packet(
        ChatPacket("Le serveur est en rust")
  )
    response = client.receive_packet(PacketType.CHAT)
    print(response.message if response != None else "Vide")
    client.send_packet(
        ChatPacket("Le client est en python")
  )
    response = client.receive_packet(PacketType.CHAT)
    print(response.message if response != None else "Vide")
    client.send_packet(
        ChatPacket("Tests des trésors en cours...")
  )
    response = client.receive_packet(PacketType.CHAT)
    print(response.message if response != None else "Vide")
    client.disconnect()
