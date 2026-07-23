import socket
import traceback

from .logger import logger
from .packet import Packet


class Client:
    """
    Client réseau de The Last Signal.
    """

    def __init__(
        self,
        host="127.0.0.1",
        port=5000,
    ):

        self.host = host
        self.port = port

        self.socket = None

        self.connected = False

    def connect(self):

        if self.connected:
            logger.warning("Déjà connecté.")
            return

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            self.socket.connect(
                (self.host, self.port)
            )

            self.connected = True

            logger.info(
                f"Connexion au serveur {self.host}:{self.port}"
            )

        except Exception:

            logger.error(
                f"Impossible de se connecter : {traceback.format_exc()}"
            )

            self.connected = False

    def send_packet(self, packet):
        """
        Envoie un Packet.
        """

        if not self.connected:
            logger.warning("Client non connecté.")
            return

        try:

            self.socket.sendall(
                Packet.encode()
            )
            logger.info("Paquet envoyé avec succès") 

        except Exception:

            logger.error(
                f"Erreur d'envoi : {traceback.format_exc()}"
            )

    def receive_packet(self):
        """
        Attend un Packet.
        """

        if not self.connected:
            return None

        try:

            header = self._recv_exact(4)

            if header is None:
                return None

            size = int.from_bytes(
                header,
                "big"
            )

            data = self._recv_exact(size)

            if data is None:
                return None

            return Packet.decode(data)

        except Exception:

            logger.error(
                f"Erreur de réception : {traceback.format_exc()}"
            )

            return None

    def _recv_exact(self, size):

        if not self.connected:
            return None

        data = bytearray()

        try:

            while len(data) < size:

                chunk = self.socket.recv(
                    size - len(data)
                )

                if not chunk:

                    logger.warning(
                        "Connexion fermée."
                    )

                    self.connected = False

                    return None

                data.extend(chunk)

            return bytes(data)

        except Exception:

            logger.error(
                f"Erreur : {traceback.format_exc()}"
            )

            self.connected = False

            return None

    def disconnect(self):

        if self.socket:

            self.socket.close()

        self.connected = False

        logger.info("Déconnecté.")
