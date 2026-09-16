import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest


HOST = "127.0.0.1"
PORT = 5000

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

# Une réponse >= 600 secondes = 10 minutes.
RESPONSE_LIMIT = 600.0

# Temps maximal pendant lequel chaque client reste connecté
# avant la fin normale d'une étape.
TEST_DURATION = 30.0

# Temps entre deux PING d'un même client.
PING_INTERVAL = 1.0

# Timeout utilisé uniquement pour établir la connexion TCP.
CONNECT_TIMEOUT = 10.0

# Nombre initial de connexions.
INITIAL_CONNECTIONS = 10

# Augmentation entre deux étapes.
CONNECTION_STEP = 10

# Protection contre une charge accidentelle illimitée.
MAX_CONNECTIONS = 10_000

# Nombre maximal de workers utilisés pour le générateur.
MAX_WORKERS = 2_000


# ------------------------------------------------------------
# Protocole
# ------------------------------------------------------------

PACKET_TYPE_PING = b"\x00\x01"


def build_ping_packet():
    """
    Construit un paquet compatible avec le protocole actuel :

        4 octets : taille du body, big-endian
        2 octets : PacketType::PING
    """

    body = PACKET_TYPE_PING

    return (
        len(body).to_bytes(4, "big")
        + body
    )


PING_PACKET = build_ping_packet()


def receive_packet(sock):
    """
    Reçoit un paquet selon le protocole :

        4 octets : longueur
        N octets : body
    """

    header = b""

    while len(header) < 4:
        chunk = sock.recv(4 - len(header))

        if not chunk:
            raise ConnectionError(
                "Connexion fermée pendant le header"
            )

        header += chunk

    size = int.from_bytes(header, "big")

    if size < 2:
        raise ValueError(
            f"Taille de paquet invalide : {size}"
        )

    # Protection contre un serveur qui annoncerait
    # une taille aberrante.
    if size > 10 * 1024 * 1024:
        raise ValueError(
            f"Paquet trop grand : {size} octets"
        )

    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError(
                "Connexion fermée pendant le paquet"
            )

        data += chunk

    return data


# ------------------------------------------------------------
# Résultat d'un client
# ------------------------------------------------------------

class ClientResult:
    def __init__(self):
        self.connected = False
        self.failed = False
        self.responses = 0
        self.errors = 0
        self.max_latency = 0.0
        self.total_latency = 0.0
        self.slow_response = False


# ------------------------------------------------------------
# Client persistant
# ------------------------------------------------------------

def persistent_client(stop_event):
    """
    Maintient une connexion TCP ouverte et envoie
    régulièrement des PING.

    Le client s'arrête lorsque :

    - stop_event est activé ;
    - le serveur ferme la connexion ;
    - une erreur survient ;
    - une réponse dépasse RESPONSE_LIMIT.
    """

    result = ClientResult()

    try:
        with socket.create_connection(
            (HOST, PORT),
            timeout=CONNECT_TIMEOUT,
        ) as sock:

            result.connected = True

            # Après la connexion, on enlève le timeout.
            # Le serveur peut donc réellement mettre
            # plusieurs minutes à répondre.
            sock.settimeout(None)

            while not stop_event.is_set():

                start = time.perf_counter()

                sock.sendall(PING_PACKET)

                try:
                    receive_packet(sock)

                except Exception:
                    result.errors += 1
                    result.failed = True
                    break

                elapsed = (
                    time.perf_counter() - start
                )

                result.responses += 1
                result.total_latency += elapsed

                if elapsed > result.max_latency:
                    result.max_latency = elapsed

                if elapsed >= RESPONSE_LIMIT:
                    result.slow_response = True
                    stop_event.set()
                    break

                # Attente sans bloquer trop longtemps
                # l'arrêt global.
                stop_event.wait(PING_INTERVAL)

    except Exception:
        result.failed = True

    return result


# ------------------------------------------------------------
# Une étape de charge
# ------------------------------------------------------------

def run_load_test(connection_count):
    """
    Lance connection_count clients persistants.
    """

    stop_event = threading.Event()

    workers = min(
        connection_count,
        MAX_WORKERS,
    )

    results = []

    start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        futures = [
            executor.submit(
                persistent_client,
                stop_event,
            )
            for _ in range(connection_count)
        ]

        # On laisse le test tourner pendant TEST_DURATION.
        while (
            time.perf_counter() - start
            < TEST_DURATION
        ):
            if stop_event.is_set():
                break

            time.sleep(0.25)

        # Arrêt propre des clients.
        stop_event.set()

        for future in futures:
            try:
                results.append(
                    future.result(
                        timeout=RESPONSE_LIMIT + 5
                    )
                )
            except Exception:
                results.append(
                    ClientResult()
                )

    elapsed_test = (
        time.perf_counter() - start
    )

    return results, elapsed_test


# ------------------------------------------------------------
# Analyse
# ------------------------------------------------------------

def analyse_results(results):
    connected = sum(
        result.connected
        for result in results
    )

    failed = sum(
        result.failed
        for result in results
    )

    responses = sum(
        result.responses
        for result in results
    )

    errors = sum(
        result.errors
        for result in results
    )

    latencies = []

    for result in results:

        if result.responses > 0:

            # Latence moyenne de ce client.
            average = (
                result.total_latency
                / result.responses
            )

            latencies.append(average)

    average_latency = (
        sum(latencies) / len(latencies)
        if latencies
        else 0.0
    )

    maximum_latency = max(
        (
            result.max_latency
            for result in results
        ),
        default=0.0,
    )

    slow_response = any(
        result.slow_response
        for result in results
    )

    return {
        "connected": connected,
        "failed": failed,
        "responses": responses,
        "errors": errors,
        "average_latency": average_latency,
        "maximum_latency": maximum_latency,
        "slow_response": slow_response,
    }


# ------------------------------------------------------------
# Test principal
# ------------------------------------------------------------

@pytest.mark.security
def test_main():

    print("# Persistent Server Load Test")
    print()

    print(
        f"Serveur : {HOST}:{PORT}"
    )

    print(
        f"Seuil : {RESPONSE_LIMIT / 60:.0f} minutes"
    )

    print(
        f"Durée par étape : {TEST_DURATION:.0f}s"
    )

    print()

    print(
        "| Connexions | Connectées | "
        "Échecs | Réponses | Erreurs | "
        "Moyenne | Maximum |"
    )

    print(
        "|---:|---:|---:|---:|---:|---:|---:|"
    )

    connection_count = INITIAL_CONNECTIONS

    while connection_count <= MAX_CONNECTIONS:

        print(
            f"\n🔎 Test avec "
            f"{connection_count} connexions persistantes..."
        )

        results, _ = run_load_test(
            connection_count
        )

        stats = analyse_results(results)

        print(
            f"| {connection_count} | "
            f"{stats['connected']} | "
            f"{stats['failed']} | "
            f"{stats['responses']} | "
            f"{stats['errors']} | "
            f"{stats['average_latency']:.4f}s | "
            f"{stats['maximum_latency']:.4f}s |"
        )

        # ----------------------------------------------------
        # Seuil de 10 minutes
        # ----------------------------------------------------

        if stats["slow_response"]:

            print()
            print(
                "🚨 SEUIL DE 10 MINUTES ATTEINT"
            )

            print(
                f"Une réponse a dépassé "
                f"{RESPONSE_LIMIT / 60:.0f} minutes "
                f"avec {connection_count} connexions."
            )

            break

        # ----------------------------------------------------
        # Échecs
        # ----------------------------------------------------

        if stats["failed"] > 0:

            print()
            print(
                "⚠️ Des connexions ont échoué."
            )

            print(
                "Le test s'arrête afin de ne pas "
                "continuer à augmenter la charge."
            )

            break

        # ----------------------------------------------------
        # Étape suivante
        # ----------------------------------------------------

        connection_count += CONNECTION_STEP

        time.sleep(1)

    else:

        print()
        print(
            "ℹ️ Le seuil de 10 minutes n'a pas "
            "été atteint."
        )

        print(
            f"Maximum testé : {MAX_CONNECTIONS} "
            "connexions persistantes."
        )

    print()


if __name__ == "__main__":
    sys.exit(
        pytest.main(
            [__file__, "-s"]
        )
    )
    
