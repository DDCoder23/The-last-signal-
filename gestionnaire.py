import calculateur as cl
import gestionnaire_de_fichiers as gf
import asyncio


async def main():
    # Liste des noms à rechercher
    noms_a_rechercher = [
        "launch.bat",
        "PyCharmCommunity",
        "Winpython",
        "argent.xlsx",
        "fichiersduJeu.xlsx",
        "tableauThe last signal.pdf",
        "tableauThe last signal.xmind",
        "map_height.png",
        "map_color.png",
        "map_collision.png",
    ]

    # Recherche asynchrone des fichiers et dossiers
    fichiers_trouves, dossiers_trouves = await gf.trouver_chemins_par_type(
        noms_a_rechercher
    )
    print("Noms recherchés :", noms_a_rechercher)
    print("Fichiers trouvés :", fichiers_trouves)
    print("Dossiers trouvés :", dossiers_trouves)

    # Liste complète des fichiers et dossiers
    fichiers = [
        "jet_de_des.py",
        "debugger.py",
        "main.py",
        "Secure_save.py",
        "debug.log",
        "idée.txt",
        "generate_map.py",
        "Tests.py",
        "table_de_conversion.py",
        "echecs.json",
        "fuseaux_horaires.json",
        "indicateurs_telephoniques.json",
        "localisation.py",
        "heure_locale.py",
        "configuration.py",
        "inventaire.py",
        "erreurs.log",
        "admin_manager.py",
        "véhicules.txt",
        "tresor.py",
        "config.ini",
        "grade_manager.py",
        "gestionnaire_de_fichiers.py",
        "gestionnaire.py",
        "objet_dispo.json",
        "horloge.py",
        "horloge_jeu.json",
        "save.txt",
        "banque_save.json",
        *fichiers_trouves,
    ]
    dossiers = [
        "saves",
        ".venv",
        "__pycache__",
        ".idea",
        *dossiers_trouves,
    ]
    print(fichiers, dossiers)

    # Mise à jour du fichier Excel
    await cl.mettre_a_jour_excel_fichiers_et_dossiers(fichiers, dossiers)

def ecrire():
    asyncio.run(main())
