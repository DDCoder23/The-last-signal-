import argparse
import sqlite3

DEFAULT_DATABASE = "database.db"
DEFAULT_TABLE = "logs"
DEFAULT_RECHERCHE = ""

def rechercher(database, table, recherche):
    """Recherche dans toutes les colonnes de la table."""

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table})")
    colonnes = [col[1] for col in cursor.fetchall()]

    resultats = []

    for colonne in colonnes:
        try:
            cursor.execute(
                f"SELECT rowid, * FROM {table} "
                f"WHERE CAST({colonne} AS TEXT) LIKE ?",
                (f"%{recherche}%",)
            )

            for ligne in cursor.fetchall():
                texte = f"[{colonne}] {ligne}"
                print(texte)
                resultats.append(texte)

        except sqlite3.Error:
            continue

    conn.close()
    return resultats


def ecrire_fichier(resultats, fichier):
    """Écrit les résultats dans un fichier texte."""

    with open(fichier, "w", encoding="utf-8") as f:
        if resultats:
            f.write("\n".join(resultats))
        else:
            f.write("Aucun résultat trouvé.\n")

    print(f"\nRésultats enregistrés dans : {fichier}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("database", nargs="?")
    parser.add_argument("table", nargs="?")
    parser.add_argument("recherche", nargs="?")
    parser.add_argument(
        "-o",
        "--output",
        help="Fichier dans lequel enregistrer les résultats."
    )
    args = parser.parse_args()
  
    if args.database and args.table and args.recherche:
        database = args.database
        table = args.table
        recherche = args.recherche
        output = args.output
    else:
        database = input("Database : ")
        table = input("Table : ")
        recherche = input("Recherche : ")
        output = input("Fichier de sortie (laisser vide pour aucun) : ").strip()

        if output == "":
            output = None

  
        if not (database and table and recherche):
            database=DEFAULT_DATABASE if not database
            table=DEFAULT_TABLE  if not table
            recherche=DEFAULT_RECHERCHE if not recherche

        resultats = rechercher(database, table, recherche)
        if output:
            ecrire_fichier(resultats, output)
        else:
            print(resultat)
        


if __name__ == "__main__":
    main()
