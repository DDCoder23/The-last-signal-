import http.server
import socketserver
import webbrowser
import os


PORT = 8000


def start_server():

    dashboard_path = os.path.join(
        os.getcwd(),
        "scripts/dashboard"
    )

    if not os.path.exists(dashboard_path):
        print("❌ Le dossier dashboard n'existe pas")
        return

    os.chdir(dashboard_path)

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(
        ("", PORT),
        handler
    ) as httpd:

        url = f"http://localhost:{PORT}/index.html"

        print("🚀 Dashboard disponible sur :")
        print(url)

        webbrowser.open(url)

        print("\nCTRL+C pour arrêter le serveur")

        try:
            httpd.serve_forever()

        except KeyboardInterrupt:
            print("\nServeur arrêté")


if __name__ == "__main__":
    start_server()