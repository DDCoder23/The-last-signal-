import sys

from PySide6.QtWidgets import QApplication

from .game import Game
from .client import Client


def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    client = Client()

    try:
        client.connect()

        game = Game(client)
        game.show()

        return app.exec()
    finally:
        client.disconnect("Arrêt normal")


if __name__ == "__main__":
    sys.exit(main())
