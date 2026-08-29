from .client import Client
import time
from .packet import Packet, PacketType
from .packets.chat import ChatPacket
from .packets.login import LoginPacket
from .packets.ping import PingPacket
from .packets.move import MovePacket
from .packets.singup import SingupPacket
import sys
import atexit
import random
def main():
    client = Client()
    def on_exit():
        client.disconnect()
    atexit.register(on_exit)
    client.connect()
    while True:
        
        
        a = random.choice(["Chat", "Login", "Ping", "Move","Singup"])
        message = [
                    "Le serveur est en rust",
                    "Le client est en python",
                    "Momo dirige le jeu"
                  ]
        personne = [
                    "Admin",
                    "Dev",
                    "Momo",
                    "Modo"
                  ]
        password_cara = "sfdqmjlsdlj@sqghl}^=)à)=à{¹~#fsdjfqsmkdfsdfj€"
        password = "d"
        for i in range (0,random.randint(1,101)):
            password += password_cara[random.randint(0,len(password_cara)-1)]
        email = f'{random.choice(personne)}@gmail.com'
        
        if a == "Chat":
            client.send_packet(ChatPacket(random.choice(message)))
            print("chat")
        elif a == "Login":
            client.send_packet(LoginPacket(email, password))
            print("login")
        elif a == "Singup":
            client.send_packet(SingupPacket(email, password))
            print("singup")
        elif a == "Ping":
            client.send_packet(PingPacket())
            print("ping")
        elif a == "Move":
            client.send_packet(MovePacket(random.randint(0,8096),random.randint(0,8096),random.randint(0,100)))
            print("move")
        client.receive_packet()

        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("arrêt du programme.")

    except SystemExit:
        print("arrêt du programme.")
    except Exception as e:
        print(f"il y a une erreur : {e}")
    finally:
        
        print("Le jeu s'arrête....")

        sys.exit(0)
    
