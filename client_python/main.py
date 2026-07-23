from .client import Client
import time
def main():
  client = Client()
  client.connect()
  time.sleep(1)
  client.send_packet(
        "Bonjour serveur".encode("utf-8")
  )
  client.disconnect()
