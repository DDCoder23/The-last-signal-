import socket
import struct
import sys


HOST = "127.0.0.1"
PORT = 5000


PAYLOADS = [
    "'",
    '"',
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1 --",
    '" OR 1=1 --',
    "'; DROP TABLE users; --",
    "'; DROP TABLE accounts; --",
    "admin'--",
    "admin' OR '1'='1",
    "' UNION SELECT NULL --",
    "' UNION SELECT * FROM users --",
]


def create_login_packet(username: str) -> bytes:

    payload = username.encode("utf-8")

    body = (
        struct.pack("!H", 2)
        + payload
    )

    return (
        struct.pack("!I", len(body))
        + body
    )


def receive_packet(sock):

    header = sock.recv(4)

    if len(header) != 4:
        return None

    size = struct.unpack("!I", header)[0]

    data = b""

    while len(data) < size:

        chunk = sock.recv(size - len(data))

        if not chunk:
            return None

        data += chunk

    return data


def test_payload(payload):

    try:

        with socket.create_connection(
            (HOST, PORT),
            timeout=5,
        ) as sock:

            sock.sendall(
                create_login_packet(payload)
            )

            response = receive_packet(sock)

            if response is None:
                return False, "Connexion fermée"

            if len(response) < 2:
                return False, "Réponse invalide"

            packet_type = struct.unpack(
                "!H",
                response[:2]
            )[0]

            response_payload = response[2:]

            return True, (
                f"PacketType={packet_type}, "
                f"payload={response_payload!r}"
            )

    except Exception as error:

        return False, repr(error)


def main():

    print("# SQL Injection Security Test")
    print()

    print(
        "> Ces tests vérifient actuellement la robustesse "
        "du protocole LOGIN."
    )
    print(
        "> Le handler LOGIN actuel n'effectue pas encore "
        "de requête SQL."
    )
    print()

    failures = 0

    print("| Payload | Résultat |")
    print("|---|---|")

    for payload in PAYLOADS:

        success, result = test_payload(payload)

        if success:
            status = "✅ Serveur stable"
        else:
            status = f"❌ {result}"
            failures += 1

        print(
            f"| `{payload}` | {status} |"
        )

    print()
    print(f"Tests effectués : {len(PAYLOADS)}")
    print(f"Échecs : {failures}")

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
