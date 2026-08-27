from .client import Client
import time
from .packet import Packet, PacketType
from .packets.chat import ChatPacket
from .packets.login import LoginPacket
from .packets.ping import PingPacket
from .packets.move import MovePacket
from .packets.singup import SingupPacket

def main():
    client = Client()
    client2 = Client()
    client.connect()
    time.sleep(1)
    client2.connect()
    client.send_packet(SingupPacket("Modo@gmail.com","fhfjf6384"))
    response = client.receive_packet(PacketType.SignUpResponse)
    
    if response is None:
        print("❌ Serveur déconnecté")
    else:
        print("📥 Serveur → client")
        print(f"Type : {response.packet_type}")
        print(f"Payload : {response.payload!r}")
        print(
        f"Message : {response.payload.decode('utf-8', errors='replace')}"
         )
    
    
    
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
    for i in range(0,3):
        client2.send_packet(LoginPacket("Modo@gmail.com","fhfjfdsalkjslf"))
        response = client2.receive_packet(PacketType.LoginResponse)
        if response is None:
            print("❌ Serveur déconnecté")
        else:
            print("📥 Serveur → client")
            print(f"Type : {response.packet_type}")
            print(f"Payload : {response.payload!r}")
            print(
                  f"Message : {response.payload.decode('utf-8', errors='replace')}"
                )
    for i in range (0,602):
            time.sleep(1)
            print(f'ban restant : {601-i} secondes')
    
    client2.connect()
    client2.send_packet(LoginPacket("Modo@gmail.com","fhfjf6384"))
    response = client2.receive_packet(PacketType.LoginResponse)
    client2.disconnect()
    
