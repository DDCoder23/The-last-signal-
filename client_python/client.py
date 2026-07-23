import socket
from .logger import logger
import traceback
import struct
class Client:
    """
    Client réseau de The Last Signal.
    Gère la connexion avec le serveur.
    """

    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port

        self.socket = None

        self.connected = False

    def connect(self):
        """
        Connexion au serveur.
        """

        if self.connected:
            logger.warning("Déjà connecté.")
            return

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            self.socket.connect((self.host, self.port))

            self.connected = True

            logger.info(
    f"Connexion au serveur {self.host}:{self.port}"
)

        except Exception as e:

            logger.error(
    f"Impossible de se connecter : {traceback.format_exc()}"
)

            self.connected = False

    def send_packet(self, packet):
        """
        Envoie des données au serveur.
        """

        if not self.connected:
            logger.warning("Client non connecté.")
            return

        try:

            size = struct.pack("!I", len(packet))
            self.socket.sendall(size + packet)

        except Exception as e:

            logger.error(
    f"Erreur d'envoi : {traceback.format_exc()}"
)

    def receive_packet(self, size=4096):
        """
        Attend un paquet du serveur.
        """

        if not self.connected:
            return None

        try:

            data = self.socket.recv(size)

            return data

        except Exception as e:

            logger.error(
    f"Erreur de réception : {traceback.format_exc()}"
)

            return None

    def disconnect(self):
        """
        Ferme la connexion.
        """

        if self.socket:

            self.socket.close()

        self.connected = False

        logger.info("Déconnecté.")
