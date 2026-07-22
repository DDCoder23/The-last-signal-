'''
Ce module permet d'encrypter
les sauvegardes du jeu
'''
import os
import json
import zipfile
import threading
import time
from datetime import datetime
import base64
import secrets
import unicodedata
import tempfile
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from typing import Callable


BASE_SAVE_DIR = "saves"
SLOTS = [1, 2, 3]

KDF_ITERATIONS = 310_000
AES_KEY_SIZE = 32
AES_GCM_NONCE_SIZE = 12
FORMAT_VERSION = b"\x01"


def log_save_event(profile: str, slot: int, status: str, message: str = "")-> None:
    """
    Journalise un événement de sauvegarde.

    status : "OK" | "ERROR"
    """
    
    try:
        base_dir = os.path.join("saves", profile)
        os.makedirs(base_dir, exist_ok=True)

        log_path = os.path.join(base_dir, "save.log")
        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"

        line = f"[{timestamp}] SLOT={slot} STATUS={status}"
        if message:
            line += f" MESSAGE={message}"
        line += "\n"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)

    except Exception:
        # Le journal ne doit JAMAIS faire planter le jeu
        pass


def normalize_password(password: str) -> str:
    """
    Cette fonction normalise 
    le mot de passe de sauvegarde 
    """
    return unicodedata.normalize("NFKC", password)


def derive_key(password: str, salt: bytes):
    password = normalize_password(password).encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=AES_KEY_SIZE,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password)


def aesgcm_encrypt(aes_key: bytes, plaintext: bytes) -> bytes:
    """
    Encrypte le mot de passe
    """
    nonce = secrets.token_bytes(AES_GCM_NONCE_SIZE)
    aes = AESGCM(aes_key)
    ct = aes.encrypt(nonce, plaintext, None)
    return FORMAT_VERSION + nonce + ct


def aesgcm_decrypt(aes_key: bytes, blob: bytes) -> bytes:
    """
    Décrypte le mot de passe
    """
    if blob[0:1] != FORMAT_VERSION:
        raise ValueError("Format inconnu.")
    nonce = blob[1 : 1 + AES_GCM_NONCE_SIZE]
    ct = blob[1 + AES_GCM_NONCE_SIZE :]
    aes = AESGCM(aes_key)
    return aes.decrypt(nonce, ct, None)


def ensure_profile_dir(profile: str) -> str:
    path = os.path.join(BASE_SAVE_DIR, profile)
    os.makedirs(path, exist_ok=True)
    return path


def atomic_write_zip(
    final_path: str,
    write_fn: Callable[[str], None]
) -> None:
    directory = os.path.dirname(final_path)
    fd, tmp_path = tempfile.mkstemp(prefix=".tmp_", dir=directory)
    os.close(fd)
    try:
        write_fn(tmp_path)
        os.replace(tmp_path, final_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def save_to_slot(profile: str, slot: int, data: dict, password: str)-> "Zip":
    if slot not in SLOTS:
        raise ValueError("Slot doit être 1, 2 ou 3.")

    profile_path = ensure_profile_dir(profile)
    zip_path = os.path.join(profile_path, f"slot{slot}.zip")

    payload = dict(data)
    payload["saved_at"] = datetime.utcnow().isoformat() + "Z"
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    salt = secrets.token_bytes(16)
    aes_key = derive_key(password, salt)
    cipher_blob = aesgcm_encrypt(aes_key, raw)

    def write_zip(path):
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("payload.bin", cipher_blob)
            z.writestr(
                "meta.json",
                json.dumps(
                    {
                        "salt": base64.b64encode(salt).decode(),
                        "saved_at": payload["saved_at"],
                    },
                    indent=2,
                ),
            )

    atomic_write_zip(zip_path, write_zip)


def load_from_slot(profile: str, slot: int, password: str) -> dict:
    if slot not in SLOTS:
        raise ValueError("Slot doit être 1, 2 ou 3.")

    zip_path = os.path.join(BASE_SAVE_DIR, profile, f"slot{slot}.zip")
    if not os.path.exists(zip_path):
        raise FileNotFoundError("Aucune sauvegarde trouvée.")

    with zipfile.ZipFile(zip_path, "r") as z:
        payload = z.read("payload.bin")
        meta = json.loads(z.read("meta.json").decode("utf-8"))

    salt = base64.b64decode(meta["salt"])
    aes_key = derive_key(password, salt)

    try:
        plaintext = aesgcm_decrypt(aes_key, payload)
    except InvalidTag:
        raise ValueError("Mot de passe incorrect ou fichier corrompu.")

    return json.loads(plaintext.decode("utf-8"))


class AutoSaver:
    def __init__(self, provider, profile, slot, password, interval=30):
        self.provider = provider
        self.profile = profile
        self.slot = slot
        self.password = password
        self.interval = interval
        self._stop = threading.Event()
        self._thread = None

    def _loop(self):
        while not self._stop.is_set():
            try:
                data = self.provider()
                save_to_slot(self.profile, self.slot, data, self.password)

                log_save_event(profile=self.profile, slot=self.slot, status="OK")

                # rotation réelle des slots
                self.slot = 1 if self.slot == 3 else self.slot + 1

            except Exception as e:
                log_save_event(
                    profile=self.profile, slot=self.slot, status="ERROR", message=str(e)
                )

            for _ in range(int(self.interval * 2)):
                if self._stop.is_set():
                    break
                time.sleep(0.5)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join()
