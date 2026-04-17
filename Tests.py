import atexit

import sys


def on_exit():
    print("Nettoyage ou sauvegarde des données avant l'arrêt.")
    ssave = 5
    print("ss")


# Enregistrer la fonction de nettoyage
atexit.register(on_exit)

# Capturer les signaux d'arrêt

try:
    # Votre code principal ici
    print("Le programme est en cours d'exécution...")
    while True:
        pass  # Simule un programme en cours d'exécution
except KeyboardInterrupt:
    print("Interruption clavier capturée.")
finally:
    print("Nettoyage final avant l'arrêt.")

sys.exit(0)
