from __future__ import annotations

import shutil
import socket
import subprocess
import sys
import tempfile
import webbrowser
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import time
import zstandard


HOST = "127.0.0.1"
DEFAULT_PORT = 8000
ARCHIVE_EXTENSION = ".tar.zst"


# ============================================================
# AFFICHAGE
# ============================================================

def print_header(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_error(message: str) -> None:
    print()
    print(f"[ERREUR] {message}")


def print_info(message: str) -> None:
    print(f"[INFO] {message}")


# ============================================================
# GIT
# ============================================================

def find_git_root() -> Path:
    """
    Détecte automatiquement la racine du dépôt Git
    depuis le répertoire courant.
    """

    try:
        result = subprocess.run(
            [
                "git",
                "rev-parse",
                "--show-toplevel",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    except FileNotFoundError:
        raise RuntimeError(
            "Git n'est pas installé ou n'est pas présent dans le PATH."
        )

    except subprocess.CalledProcessError:
        raise RuntimeError(
            "Impossible de trouver la racine Git depuis le répertoire courant."
        )

    root = result.stdout.strip()

    if not root:
        raise RuntimeError("Git n'a retourné aucune racine de dépôt.")

    return Path(root).resolve()


# ============================================================
# RAPPORTS
# ============================================================

def find_project_root() -> Path:
    """
    Détecte automatiquement la racine du projet
    à partir de l'emplacement du script/exécutable.
    """

    if getattr(sys, "frozen", False):
        # Exécution depuis un .exe PyInstaller
        current = Path(sys.executable).resolve().parent
    else:
        # Exécution directe du script Python
        current = Path(__file__).resolve().parent

    # On remonte jusqu'à trouver le dossier reports/
    for directory in [current, *current.parents]:
        if (directory / "reports").is_dir():
            return directory

    raise RuntimeError(
        "Impossible de trouver la racine du projet "
        "(dossier reports introuvable)."
    )

def get_report_types(reports_root: Path) -> list[Path]:
    """
    Détecte automatiquement les types de rapports.

    Exemple :
        reports/python
        reports/build
        reports/security
        reports/integration
    """

    report_types = [
        path
        for path in reports_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    ]

    return sorted(report_types, key=lambda path: path.name.lower())


def choose_report_type(report_types: list[Path]) -> Path:
    """
    Demande à l'utilisateur quel type de rapport ouvrir.
    """

    print_header("TYPES DE RAPPORTS DISPONIBLES")

    for index, report_type in enumerate(report_types, start=1):
        print(f"{index}. {report_type.name}")

    while True:
        try:
            choice = input("\nChoisissez un type de rapport : ").strip()
            index = int(choice)

            if 1 <= index <= len(report_types):
                return report_types[index - 1]

        except ValueError:
            pass

        print("Choix invalide. Entrez le numéro correspondant.")


def ask_report_number() -> int:
    """
    Demande le numéro du rapport.
    """

    while True:
        value = input("\nNuméro du rapport : ").strip()

        try:
            number = int(value)

            if number >= 1:
                return number

        except ValueError:
            pass

        print("Veuillez entrer un numéro de rapport valide.")


def build_report_filename(
    report_type: Path,
    report_number: int,
) -> str:
    """
    Construit le nom du fichier HTML.

    Exemple :
        python-report-3.html
    """

    return f"{report_type.name}-report-{report_number}.html"


# ============================================================
# RECHERCHE DIRECTE
# ============================================================

def find_unarchived_report(
    report_type: Path,
    current_date: str,
    filename: str,
) -> Path | None:
    """
    Recherche d'abord le rapport non archivé.
    """

    report_path = report_type / current_date / filename

    if report_path.is_file():
        return report_path

    return None


# ============================================================
# ARCHIVES
# ============================================================

def find_archive_member(
    archive_path: Path,
    expected_members: list[str],
) -> bytes | None:
    """
    Recherche et extrait uniquement le fichier demandé
    depuis une archive .tar.zst.

    Aucun programme externe zstd/tar n'est nécessaire.
    """

    try:
        with archive_path.open("rb") as compressed_file:

            decompressor = zstandard.ZstdDecompressor()

            with decompressor.stream_reader(compressed_file) as reader:

                import tarfile

                with tarfile.open(
                    fileobj=reader,
                    mode="r|",
                ) as archive:

                    for member in archive:

                        if member.name not in expected_members:
                            continue

                        if not member.isfile():
                            continue

                        extracted = archive.extractfile(member)

                        if extracted is None:
                            return None

                        return extracted.read()

    except Exception as exc:
        print_info(
            f"Impossible de lire {archive_path.name} : {exc}"
        )

    return None

def find_reports_root(git_root: Path) -> Path:
    """
    Trouve le dossier reports du projet.
    """

    reports_root = git_root / "reports"

    if not git_root.is_dir():
        raise RuntimeError(
            f"Le dossier reports est introuvable : {reports_root}"
        )

    return reports_root
def find_archived_report(
    report_type: Path,
    current_date: str,
    filename: str,
    temp_directory: Path,
) -> Path | None:
    """
    Recherche le rapport dans :

    1. l'archive quotidienne :
       YYYY-MM-DD.tar.zst

    2. l'archive mensuelle :
       MM-YYYY.tar.zst

    3. les autres archives en dernier recours.
    """

    month_year = datetime.strptime(
        current_date,
        "%Y-%m-%d",
    ).strftime("%m-%Y")

    daily_archive = report_type / f"{current_date}.tar.zst"
    monthly_archive = report_type / f"{month_year}.tar.zst"

    archives: list[tuple[Path, list[str]]] = []

    # --------------------------------------------------------
    # Archive quotidienne
    # --------------------------------------------------------

    if daily_archive.is_file():
        archives.append(
            (
                daily_archive,
                [
                    f"{current_date}/{filename}",
                    filename,
                ],
            )
        )

    # --------------------------------------------------------
    # Archive mensuelle
    # --------------------------------------------------------

    if monthly_archive.is_file():
        archives.append(
            (
                monthly_archive,
                [
                    f"{month_year}/{current_date}/{filename}",
                    f"{current_date}/{filename}",
                    filename,
                ],
            )
        )

    # --------------------------------------------------------
    # Recherche de secours dans toutes les archives
    # --------------------------------------------------------

    already_checked = {
        archive.resolve()
        for archive, _ in archives
    }

    for archive in sorted(
        report_type.glob(f"*{ARCHIVE_EXTENSION}")
    ):
        if archive.resolve() in already_checked:
            continue

        archives.append(
            (
                archive,
                [
                    f"{current_date}/{filename}",
                    f"{month_year}/{current_date}/{filename}",
                    filename,
                ],
            )
        )

    # --------------------------------------------------------
    # Recherche
    # --------------------------------------------------------

    for archive_path, expected_members in archives:

        print_info(
            f"Recherche dans l'archive : {archive_path.name}"
        )

        data = find_archive_member(
            archive_path,
            expected_members,
        )

        if data is None:
            continue

        output_directory = (
            temp_directory
            / report_type.name
            / current_date
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = output_directory / filename

        output_file.write_bytes(data)

        print_info(
            f"Rapport extrait depuis : {archive_path.name}"
        )

        return output_file

    return None


# ============================================================
# SERVEUR HTTP
# ============================================================

def find_free_port(
    host: str = HOST,
    start_port: int = DEFAULT_PORT,
) -> int:
    """
    Trouve automatiquement un port libre.
    """

    for port in range(start_port, start_port + 100):

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        ) as sock:

            try:
                sock.bind((host, port))
                return port

            except OSError:
                continue

    raise RuntimeError(
        "Impossible de trouver un port libre."
    )


def start_server(
    directory: Path,
) -> None:
    """
    Lance le serveur HTTP local et ouvre le navigateur.
    """

    port = find_free_port()

    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(
        *args,
        directory=str(directory),
        **kwargs,
    )

    server = ThreadingHTTPServer(
        (HOST, port),
        handler,
    )

    url = f"http://{HOST}:{port}/"

    print_header("SERVEUR HTTP")

    print(f"Répertoire : {directory}")
    print(f"Adresse    : {url}")
    print()
    print("Le rapport va être ouvert dans votre navigateur.")
    print("Appuyez sur Ctrl+C pour arrêter le serveur.")

    webbrowser.open(url)

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nArrêt du serveur...")

    finally:
        server.server_close()


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main() -> int:

    print_header("OPEN REPORT")

    # --------------------------------------------------------
    # Date système
    # --------------------------------------------------------

    current_date = datetime.now().strftime("%Y-%m-%d")

    print_info(f"Date système : {current_date}")

    # --------------------------------------------------------
    # Racine Git
    # --------------------------------------------------------

    try:
        git_root = find_project_root()

    except RuntimeError as exc:
        print_error(str(exc))
        time.sleep(30)
        return 1

    print_info(f"Racine : {git_root}")

    # --------------------------------------------------------
    # Dossier reports
    # --------------------------------------------------------

    try:
        reports_root = find_reports_root(git_root)

    except RuntimeError as exc:
        print_error(str(exc))
        return 1

    print_info(f"Dossier reports : {reports_root}")

    # --------------------------------------------------------
    # Types de rapports
    # --------------------------------------------------------

    report_types = get_report_types(
        reports_root
    )

    if not report_types:
        print_error(
            "Aucun type de rapport trouvé dans reports/."
        )
        return 1

    # --------------------------------------------------------
    # Choix du type
    # --------------------------------------------------------

    report_type = choose_report_type(
        report_types
    )

    # --------------------------------------------------------
    # Numéro du rapport
    # --------------------------------------------------------

    report_number = ask_report_number()

    filename = build_report_filename(
        report_type,
        report_number,
    )

    print()
    print_info(f"Rapport demandé : {filename}")

    # --------------------------------------------------------
    # Recherche directe
    # --------------------------------------------------------

    report_path = find_unarchived_report(
        report_type,
        current_date,
        filename,
    )

    temporary_directory: Path | None = None

    if report_path is not None:

        print_info(
            f"Rapport non archivé trouvé : {report_path}"
        )

        server_directory = report_path.parent

    else:

        print_info(
            "Rapport non trouvé dans les fichiers actuels."
        )

        print_info(
            "Recherche dans les archives..."
        )

        # ----------------------------------------------------
        # Répertoire temporaire
        # ----------------------------------------------------

        temporary_directory = Path(
            tempfile.mkdtemp(
                prefix="open-report-"
            )
        )

        report_path = find_archived_report(
            report_type,
            current_date,
            filename,
            temporary_directory,
        )

        if report_path is None:

            print_error(
                f"Rapport introuvable : {filename}"
            )

            print()
            print(
                "Recherche effectuée dans :"
            )
            print(
                f"  {report_type / current_date}"
            )
            print(
                f"  {report_type}/*.tar.zst"
            )

            shutil.rmtree(
                temporary_directory,
                ignore_errors=True,
            )

            return 1

        server_directory = report_path.parent

    # --------------------------------------------------------
    # Serveur
    # --------------------------------------------------------

    try:
        start_server(server_directory)

    finally:

        if temporary_directory is not None:

            shutil.rmtree(
                temporary_directory,
                ignore_errors=True,
            )

            print_info(
                "Répertoire temporaire supprimé."
            )

    return 0


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    sys.exit(main())