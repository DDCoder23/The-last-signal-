import os
import pandas as pd
from datetime import datetime
def log_erreur(message):
    """Enregistre un message d'erreur dans un fichier de log."""
    with open("erreurs.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")
def creer_fichier_vide(chemin_fichier):
    """
    Crée un fichier vide s'il n'existe pas.

    Args:
        chemin_fichier (str): Chemin du fichier à créer.
    """
    if not os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'w') as fichier:
            pass  # Crée un fichier vide
        print(f"Fichier créé : {chemin_fichier}")

def calculer_taille_dossier(dossier):
    """Calcule la taille totale d'un dossier en o et compte le nombre de fichiers."""
    taille_totale_octets = 0
    nombre_fichiers = 0

    for chemin, sous_dossiers, fichiers in os.walk(dossier):
        for fichier in fichiers:
            fichier_chemin = os.path.join(chemin, fichier)
            taille_totale_octets += os.path.getsize(fichier_chemin)
            nombre_fichiers += 1

    taille_totale_o = taille_totale_octets 
    return taille_totale_o, nombre_fichiers

def mettre_a_jour_excel_fichiers_et_dossiers(liste_fichiers, liste_dossiers, fichier_excel="inventaire_jeu.xlsx"):
    """
    Met à jour un fichier Excel avec deux feuilles : une pour les fichiers et une pour les dossiers.
    Préserve les autres feuilles existantes.

    Args:
        liste_fichiers (list): Liste des chemins des fichiers à enregistrer.
        liste_dossiers (list): Liste des chemins des dossiers à enregistrer.
        fichier_excel (str): Chemin du fichier Excel à mettre à jour.
    """

    # Préparation des données pour les fichiers
    fichiers_info = []
    for fichier in liste_fichiers:
        if os.path.exists(fichier):
            taille_o = os.path.getsize(fichier)
            fichiers_info.append({
                "Nom": os.path.basename(fichier),
                "Chemin": os.path.abspath(fichier),
                "Taille (o)": taille_o
            })
        else:
            log_erreur(f"Le fichier {fichier} n'existe pas.")

    # Préparation des données pour les dossiers
    dossiers_info = []
    for dossier in liste_dossiers:
        if os.path.exists(dossier) and os.path.isdir(dossier):
            taille_o, nombre_fichiers = calculer_taille_dossier(dossier)
            dossiers_info.append({
                "Nom": os.path.basename(dossier),
                "Chemin": os.path.abspath(dossier),
                "Taille (o)": taille_o,
                "Nombre de fichiers": nombre_fichiers
            })
        else:
            log_erreur(f"⚠️ Le dossier {dossier} n'existe pas ou n'est pas un dossier.")

    # Création des DataFrames
    df_fichiers = pd.DataFrame(fichiers_info)
    print(fichiers_info)
    df_dossiers = pd.DataFrame(dossiers_info)
    print(dossiers_info)
    creer_fichier_vide( fichier_excel)
    

    # Ajouter les feuilles sans écraser les existantes
    try:
        existing_sheets = pd.ExcelFile(fichier_excel).sheet_names
    except FileNotFoundError:
        existing_sheets = []

    with pd.ExcelWriter(fichier_excel, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
        df_fichiers.to_excel(writer, sheet_name="Fichiers", index=False)
        df_dossiers.to_excel(writer, sheet_name="Dossiers", index=False)

    print(f"Fichier Excel mis à jour : {fichier_excel}")


    
    


  
    

