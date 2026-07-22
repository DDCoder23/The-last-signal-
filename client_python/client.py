import socket

HOST = "127.0.0.1"
PORT = 5000
def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((HOST, PORT))
  print("Connecté au serveur")
  client.close()
