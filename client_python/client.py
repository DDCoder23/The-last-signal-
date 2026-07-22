import socket


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
            print("Déjà connecté.")
            return

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            self.socket.connect((self.host, self.port))

            self.connected = True

            print(f"Connexion au serveur {self.host}:{self.port}")

        except Exception as e:

            print("Impossible de se connecter.")

            print(e)

            self.connected = False

    def send_packet(self, packet):
        """
        Envoie des données au serveur.
        """

        if not self.connected:
            print("Client non connecté.")
            return

        try:

            self.socket.sendall(packet)

        except Exception as e:

            print("Erreur d'envoi")

            print(e)

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

            print("Erreur de réception")

            print(e)

            return None

    def disconnect(self):
        """
        Ferme la connexion.
        """

        if self.socket:

            self.socket.close()

        self.connected = False

        print("Déconnecté.")
