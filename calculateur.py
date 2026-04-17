
import os
import asyncio
import pandas as pd
from datetime import datetime
import gestionnaire_de_fichiers as gf






async def log_erreur_async(message):
    """Enregistre un message d'erreur dans un fichier de log (version asynchrone)."""

    def _ecrire_log():
        with open("erreurs.log", "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")

    # Exécute l'opération bloquante dans un thread séparé
    await asyncio.get_event_loop().run_in_executor(None, _ecrire_log)
async def creer_fichier_vide_async(chemin_fichier):
    """
    Crée un fichier Excel vide s'il n'existe pas (version asynchrone).
    """
    if not os.path.exists(chemin_fichier):
        async with asyncio.Lock():
            with open(chemin_fichier, 'w') as fichier:
                df = pd.DataFrame(columns=["Nom", "Type", "Quantité", "Niveau"])
                df.to_excel(chemin_fichier, index=False, engine='openpyxl')
            print(f"Fichier créé : {chemin_fichier}")

async def calculer_taille_dossier_async(dossier):
    
    a={}

    def _calculer_taille():
        taille_totale_octets = 0
        nombre_fichiers = 0
  
        for chemin, sous_dossiers, fichiers in os.walk(dossier):
            for fichier in fichiers:
                try:
                    fichier_chemin = os.path.join(chemin, fichier)
                    taille_totale_octets += os.path.getsize(fichier_chemin)
                    nombre_fichiers += 1
                except FileNotFoundError:
                    a[fichier]=FileNotFoundError
                     
                     
                except Exception as e:
                    a[fichier]=e
        
                    
        return taille_totale_octets, nombre_fichiers
    for values,keys in a:
             await log_erreur_async(f"{keys} a levé cette erreur {a[fichier]}.")



    # Exécute la fonction bloquante dans un thread séparé
    return await asyncio.get_event_loop().run_in_executor(None, _calculer_taille)
async def mettre_a_jour_excel_fichiers_et_dossiers(liste_fichiers, liste_dossiers, fichier_excel=r"E:\Projetpython\Gestion\fichiersduJeu.xlsx"):
    """
    Met à jour un fichier Excel avec deux feuilles : une pour les fichiers et une pour les dossiers (version asynchrone).
    Préserve les autres feuilles existantes.
    """
    # Préparation des données pour les fichiers
    fichiers_info = []
    for fichier in liste_fichiers:
        if os.path.exists(fichier):
            taille_o = os.path.getsize(fichier)
            nom_fichier = os.path.basename(fichier)
            extension = os.path.splitext(nom_fichier)[1]
            fichiers_info.append({
                "Nom": nom_fichier,
                "Extension": extension, 
                "Chemin": os.path.abspath(fichier),
                "Taille (o)": taille_o
            })
        else:
            await log_erreur_async(f" Le fichier {fichier} n'existe pas.")

    # Préparation des données pour les dossiers
    dossiers_info = []
    for dossier in liste_dossiers:
        if os.path.exists(dossier) and os.path.isdir(dossier):
            taille_o, nombre_fichiers = await calculer_taille_dossier_async(dossier)
            dossiers_info.append({
                "Nom": os.path.basename(dossier),
                "Chemin": os.path.abspath(dossier),
                "Taille (o)": taille_o,
                "Nombre de fichiers": nombre_fichiers
            })
        else:
            await log_erreur_async(f"Le dossier {dossier} n'existe pas ou n'est pas un dossier.")

    # Création des DataFrames
    df_fichiers = pd.DataFrame(fichiers_info)
    df_dossiers = pd.DataFrame(dossiers_info)

    # Crée le fichier Excel s'il n'existe pas
    await creer_fichier_vide_async(fichier_excel)

    # Ajoute les feuilles sans écraser les existantes
    try:
        existing_sheets = pd.ExcelFile(fichier_excel, engine='openpyxl').sheet_names
    except FileNotFoundError:
        existing_sheets = []

    with pd.ExcelWriter(fichier_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df_fichiers.to_excel(writer, sheet_name="Fichiers", index=False)
        df_dossiers.to_excel(writer, sheet_name="Dossiers", index=False)

    print(f"Fichier Excel mis à jour : {fichier_excel}")

