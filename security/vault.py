import os
import json
import base64

from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


VAULT_FILE = "vault.enc"


def generate_key(password: str, salt: bytes):
    """
    Transforme le mot de passe maître en clé AES.
    """

    return hash_secret_raw(
        password.encode(),
        salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID
    )


def encrypt_vault(data, password):
    
    salt = os.urandom(16)
    key = generate_key(password, salt)

    aes = AESGCM(key)

    nonce = os.urandom(12)

    encrypted = aes.encrypt(
        nonce,
        json.dumps(data).encode(),
        None
    )

    vault = {
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "data": base64.b64encode(encrypted).decode()
    }

    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)


def decrypt_vault(password):

    with open(VAULT_FILE) as f:
        vault = json.load(f)

    salt = base64.b64decode(vault["salt"])
    nonce = base64.b64decode(vault["nonce"])
    encrypted = base64.b64decode(vault["data"])

    key = generate_key(password, salt)

    aes = AESGCM(key)

    decrypted = aes.decrypt(
        nonce,
        encrypted,
        None
    )

    return json.loads(decrypted)


def add_secret():

    password = input("Mot de passe maître : ")

    if os.path.exists(VAULT_FILE):
        secrets = decrypt_vault(password)
    else:
        secrets = {}

    name = input("Nom du secret : ")
    value = input("Valeur : ")

    secrets[name] = value

    encrypt_vault(secrets, password)

    print("Secret ajouté.")


def show_secrets():

    password = input("Mot de passe maître : ")

    secrets = decrypt_vault(password)

    for name, value in secrets.items():
        print(f"{name} = {value}")


if __name__ == "__main__":

    print("""
1 - Ajouter un secret
2 - Voir les secrets
""")

    choix = input("> ")

    if choix == "1":
        add_secret()

    elif choix == "2":
        show_secrets()
