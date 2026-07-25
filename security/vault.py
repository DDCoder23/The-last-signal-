import os
import json
import base64

from cryptography.fernet import Fernet


KEY_FILE = "security/master.key"
VAULT_FILE = "security/vault.enc"


def create_key():
    """
    Crée une clé maître si elle n'existe pas.
    """

    if not os.path.exists(KEY_FILE):

        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as f:
            f.write(key)

        print("Nouvelle clé créée.")


def load_key():

    with open(KEY_FILE, "rb") as f:
        return f.read()


def encrypt_vault(data):

    key = load_key()

    cipher = Fernet(key)

    encrypted = cipher.encrypt(
        json.dumps(data).encode()
    )

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)


def decrypt_vault():

    key = load_key()

    cipher = Fernet(key)

    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()

    decrypted = cipher.decrypt(encrypted)

    return json.loads(decrypted)


def add_secret(name, value):

    if os.path.exists(VAULT_FILE):
        secrets = decrypt_vault()
    else:
        secrets = {}

    secrets[name] = value

    encrypt_vault(secrets)


if __name__ == "__main__":

    create_key()

    
