from pathlib import Path
import asyncio
from functools import lru_cache



async def trouver_chemins_par_type(noms, repertoire_depart="E:\\"):
    noms = [nom.lower() for nom in noms]  # Recherche insensible à la casse
    repertoire = Path(repertoire_depart)
    chemins_fichiers = []
    chemins_dossiers = []

    @lru_cache(maxsize=32)
    def _rechercher():
        for chemin in repertoire.rglob("*"):
            chemin_str = str(chemin).lower()
            nom_actuel = chemin.name.lower()  
            if nom_actuel in noms:
                if chemin.is_dir():
                    chemins_dossiers.append(str(chemin.resolve()))
                elif chemin.is_file():
                    chemins_fichiers.append(str(chemin.resolve()))

    # Exécute la recherche dans un thread séparé pour éviter de bloquer l'event loop
    await asyncio.get_event_loop().run_in_executor(None, _rechercher)

    return chemins_fichiers, chemins_dossiers




