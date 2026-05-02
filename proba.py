"""
Fichier unique pour calculer les probabilités d'obtenir chaque enchantement via :
1. Les trésors (niveaux 1 à 47, mode normal/admin).
2. Les conversions de livres (1→6, 2→6, etc.).
3. La combinaison des deux.
Toutes les probabilités sont affichées en pourcentages (sans notation scientifique).
"""
from datetime import datetime
import random
from collections import defaultdict

# =============================================================================
# IMPORT DES DONNÉES DEPUIS VOS FICHIERS
# =============================================================================

# Importer les classes et fonctions depuis inventaire.py
from inventaire import (
    Objet, Livres, Armes, equipement, Potion,
    safe_increment, qtes, nettoyer_stuff_zero,
    liste_armes, liste_outils, liste_muni, liste_potion,
    generer_cle_unique, clefs, livres_par_enchantements,
    trouver_cles_par_liste_non_ordonnee, mettre_a_jour_index, supprimer_de_l_index, pregenerer_cache_enchantements, ajouter_enchant
)

# Importer les données depuis table_de_conversion.py
from table_de_conversion import (
    dict_enchant, fusionner_enchantements,
    obtenir_enchantement_superieur, chercher_livre,
    convertir_livres, StatsConversion
)

# Importer la classe tresor depuis tresor.py
from tresor import tresor

# Importer admin_manager
from admin_manager import IS_ADMIN
import json

# Initialiser l'instance de tresor
coffre = tresor()

# =============================================================================
# CONSTANTES
# =============================================================================

# Probabilité qu'un livre ait un enchantement d'une catégorie donnée (70%)
P_CATEGORIE = 1

# Poids des catégories pour les livres enchantés (épée, armes à feu, armure)
POIDS_CATEGORIES = [0.7, 0.2, 0.1]

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def calculer_probabilite_conversion(niveau_depart: int, niveau_cible: int, categorie: str, enchantement_cible: str) -> float:
    """
    Calcule la probabilité d'obtenir un enchantement spécifique (ex: "Poison VI")
    en partant d'un niveau de livre donné (ex: 1) et en remontant jusqu'au niveau cible (ex: 6).
    """
    if niveau_depart >= niveau_cible:
        return 0.0

    if enchantement_cible not in dict_enchant[niveau_cible][categorie]:
        return 0.0

    # Probabilité de base pour un enchantement de la catégorie donnée
    P_ENCHANT_NIV = P_CATEGORIE * POIDS_CATEGORIES[["épée", "armes à feu", "armure"].index(categorie)] / len(dict_enchant[niveau_depart][categorie])

    # Probabilité de réussir toutes les étapes de conversion
    probabilite_totale = 1.0

    for niveau in range(niveau_depart, niveau_cible):
        # Nombre de livres nécessaires pour passer au niveau suivant
        nb_livres_necessaires = niveau + 1  # 2 pour 1→2, 3 pour 2→3, etc.

        # Enchantement actuel à ce niveau (ex: "Poison I" pour niveau 1)
        enchantement_actuel = enchantement_cible.replace(
            f" {['I', 'II', 'III', 'IV', 'V', 'VI'][niveau_cible - 1]}",
            f" {['I', 'II', 'III', 'IV', 'V', 'VI'][niveau - 1]}"
        )

        # Vérifier si l'enchantement actuel existe à ce niveau
        if enchantement_actuel not in dict_enchant[niveau][categorie]:
            return 0.0

        # Probabilité d'avoir au moins 2 livres avec l'enchantement actuel dans nb_livres_necessaires livres
        P_0 = (1 - P_ENCHANT_NIV) ** nb_livres_necessaires
        P_1 = nb_livres_necessaires * P_ENCHANT_NIV * (1 - P_ENCHANT_NIV) ** (nb_livres_necessaires - 1)
        P_au_moins_2 = 1 - P_0 - P_1

        probabilite_totale *= P_au_moins_2

    # Probabilité finale : probabilité d'avoir l'enchantement cible au niveau cible
    P_ENCHANT_CIBLE = P_CATEGORIE * POIDS_CATEGORIES[["épée", "armes à feu", "armure"].index(categorie)] / len(dict_enchant[niveau_cible][categorie])
    probabilite_totale *= P_ENCHANT_CIBLE

    return probabilite_totale

def calculer_toutes_probabilites_conversions() -> dict:
    """Calcule les probabilités pour tous les enchantements via les conversions de livres."""
    resultats = {}

    for niveau_depart in range(1, 6):
        resultats[niveau_depart] = {}
        for niveau_cible in range(niveau_depart + 1, 7):
            resultats[niveau_depart][niveau_cible] = {}
            for categorie in dict_enchant[niveau_cible]:
                resultats[niveau_depart][niveau_cible][categorie] = {}
                for enchantement in dict_enchant[niveau_cible][categorie]:
                    prob = calculer_probabilite_conversion(niveau_depart, niveau_cible, categorie, enchantement)
                    resultats[niveau_depart][niveau_cible][categorie][enchantement] = prob

    return resultats

# =============================================================================
# CALCUL DES PROBABILITÉS POUR LES TRÉSORS
# =============================================================================

def calculer_probabilite_artefact(niveau_tresor: int, type_artefact: str) -> float:
    """Calcule la probabilité de tirer un artefact spécifique à un niveau de trésor donné."""
    if niveau_tresor not in coffre.loot_par_niveau:
        return 0.0

    loot_niveau = coffre.loot_par_niveau[niveau_tresor]
    poids_artefact = loot_niveau.get(type_artefact, 0)
    total_poids = sum(loot_niveau.values())
    P_artefact = poids_artefact / total_poids if total_poids > 0 else 0.0

    # Récupérer le seuil depuis les attributs de coffre
    seuil = 5  # Valeur par défaut
    if type_artefact == "Artefact commun" and hasattr(coffre, 'seuil_artefact_commun') and niveau_tresor in coffre.seuil_artefact_commun:
        seuil = coffre.seuil_artefact_commun[niveau_tresor]
    elif type_artefact == "Artefact peu commun" and hasattr(coffre, 'seuil_artefact_peu_commun') and niveau_tresor in coffre.seuil_artefact_peu_commun:
        seuil = coffre.seuil_artefact_peu_commun[niveau_tresor]
    elif type_artefact == "Artefact rare" and hasattr(coffre, 'seuil_artefact_rare') and niveau_tresor in coffre.seuil_artefact_rare:
        seuil = coffre.seuil_artefact_rare[niveau_tresor]
    elif type_artefact == "Artefact super rare" and hasattr(coffre, 'seuil_artefact_super_rare') and niveau_tresor in coffre.seuil_artefact_super_rare:
        seuil = coffre.seuil_artefact_super_rare[niveau_tresor]
    elif type_artefact == "Artefact épique" and hasattr(coffre, 'seuil_artefact_epique') and niveau_tresor in coffre.seuil_artefact_epique:
        seuil = coffre.seuil_artefact_epique[niveau_tresor]
    elif type_artefact == "Artefact légendaire" and hasattr(coffre, 'seuil_artefact_legendaire') and niveau_tresor in coffre.seuil_artefact_legendaire:
        seuil = coffre.seuil_artefact_legendaire[niveau_tresor]
    elif type_artefact == "Artefact admin":
        seuil = 5  # Valeur par défaut pour admin

    P_seuil = (21 - seuil) / 20  # P(de.jet_de_des(20, 1) >= seuil)
    return P_artefact * P_seuil

def calculer_probabilite_livre_enchant(niveau_tresor: int, is_admin: bool = False) -> dict:
    """Calcule la probabilité d'obtenir chaque niveau de livre enchanté à un niveau de trésor donné."""
    probabilites = {f"livre enchant niv {niv}": 0.0 for niv in range(1, 7)}

    # Utiliser les probabilités de livres depuis coffre.sous_loot
    if is_admin:
        probabilites_livres = coffre.sous_loot["livre enchant"]
    else:
        probabilites_livres = {
            "livre enchant niv 1": 70,
            "livre enchant niv 2": 20,
            "livre enchant niv 3": 5,
            "livre enchant niv 4": 3,
            "livre enchant niv 5": 1.5,
            "livre enchant niv 6": 0.5,
        }

    for type_artefact in ["Artefact super rare", "Artefact épique", "Artefact légendaire", "Artefact admin"]:
        P_artefact = calculer_probabilite_artefact(niveau_tresor, type_artefact)
        if P_artefact == 0.0:
            continue

        # Récupérer la probabilité de livre enchant depuis coffre.sous_loot
        P_livre_enchant = coffre.sous_loot[type_artefact].get("livre enchant", 0) / 100
        P_livre_via_artefact = P_artefact * P_livre_enchant

        for niv_livre in range(1, 7):
            nom_livre = f"livre enchant niv {niv_livre}"
            P_niv_livre = probabilites_livres.get(nom_livre, 0) / 100
            probabilites[nom_livre] += P_livre_via_artefact * P_niv_livre

    return probabilites

def calculer_probabilite_enchantement_par_tresor(niveau_tresor: int, is_admin: bool = False) -> dict:
    """Calcule la probabilité d'obtenir chaque enchantement via un trésor de niveau donné."""
    probas_livres = calculer_probabilite_livre_enchant(niveau_tresor, is_admin)
    resultats = defaultdict(float)

    for niv_livre in range(1, 7):
        nom_livre = f"livre enchant niv {niv_livre}"
        P_livre = probas_livres[nom_livre]

        if P_livre == 0.0:
            continue

        for categorie in dict_enchant[niv_livre]:
            for enchantement in dict_enchant[niv_livre][categorie]:
                P_categorie = P_CATEGORIE * POIDS_CATEGORIES[["épée", "armes à feu", "armure"].index(categorie)]
                P_enchant = P_categorie / len(dict_enchant[niv_livre][categorie])
                resultats[(categorie, enchantement)] += P_livre * P_enchant

    return resultats

# =============================================================================
# COMBINAISON DES PROBABILITÉS (TRÉSORS + CONVERSIONS)
# =============================================================================

def calculer_probabilite_totale(niveau_tresor: int, is_admin: bool = False) -> dict:
    """
    Calcule la probabilité totale d'obtenir chaque enchantement via :
    1. Les trésors (directement).
    2. Les conversions de livres (en partant des livres obtenus via les trésors).
    """
    # 1. Probabilités via les trésors
    probas_tresors = calculer_probabilite_enchantement_par_tresor(niveau_tresor, is_admin)

    # 2. Probabilités via les conversions
    probas_conversions = calculer_toutes_probabilites_conversions()

    # 3. Combinaison des deux
    resultats = defaultdict(float)

    # Ajouter les probabilités directes des trésors
    for (categorie, enchantement), prob in probas_tresors.items():
        resultats[(categorie, enchantement, "Trésor")] = prob

    # Ajouter les probabilités via les conversions
    for niveau_depart in range(1, 6):
        for niveau_cible in range(niveau_depart + 1, 7):
            for categorie in probas_conversions[niveau_depart][niveau_cible]:
                for enchantement, prob in probas_conversions[niveau_depart][niveau_cible][categorie].items():
                    # Probabilité d'obtenir un livre de niveau_depart via les trésors
                    P_livre_depart = calculer_probabilite_livre_enchant(niveau_tresor, is_admin).get(f"livre enchant niv {niveau_depart}", 0.0)
                    # Probabilité totale = P(livre_depart) * P(conversion de niveau_depart à niveau_cible avec enchantement)
                    resultats[(categorie, enchantement, f"Conversion {niveau_depart}→{niveau_cible}")] += P_livre_depart * prob

    return resultats

# =============================================================================
# AFFICHAGE DES RÉSULTATS (EN POURCENTAGES UNIQUEMENT)
# =============================================================================

def afficher_probabilites_conversions():
    """Affiche les probabilités d'obtenir chaque enchantement via les conversions de livres (en %)."""
    probas = calculer_toutes_probabilites_conversions()

    print("\n" + "=" * 120)
    print("PROBABILITÉS D'OBTENIR CHAQUE ENCHANTEMENT VIA LES CONVERSIONS (EN %)".center(120))
    print("=" * 120)

    for niveau_depart in range(1, 6):
        for niveau_cible in range(niveau_depart + 1, 7):
            print(f"\n📖 Conversion {niveau_depart} → {niveau_cible} :")
            for categorie in probas[niveau_depart][niveau_cible]:
                for enchantement, prob in probas[niveau_depart][niveau_cible][categorie].items():
                    if prob > 0:
                        print(f"  🗡️ {categorie} - {enchantement}: {prob * 100:.6f}%")

def afficher_probabilites_tresor(niveau_tresor: int, is_admin: bool = False):
    """Affiche les probabilités d'obtenir chaque enchantement pour un niveau de trésor donné (en %)."""
    probas = calculer_probabilite_enchantement_par_tresor(niveau_tresor, is_admin)
    mode = "ADMIN" if is_admin else "NORMAL"

    print("\n" + "=" * 120)
    print(f"PROBABILITÉS VIA LES TRÉSORS (NIVEAU {niveau_tresor}, MODE {mode}) - EN %".center(120))
    print("=" * 120)

    for (categorie, enchantement), prob in sorted(probas.items(), key=lambda x: x[1], reverse=True):
        if prob > 0:
            print(f"  🗡️ {categorie} - {enchantement}: {prob * 100:.6f}%")

def afficher_probabilites_totales(niveau_tresor: int, is_admin: bool = False):
    """Affiche les probabilités totales (trésors + conversions) pour un niveau de trésor donné (en %)."""
    probas = calculer_probabilite_totale(niveau_tresor, is_admin)
    mode = "ADMIN" if is_admin else "NORMAL"

    print("\n" + "=" * 120)
    print(f"PROBABILITÉS TOTALES (TRÉSORS + CONVERSIONS) POUR LE NIVEAU {niveau_tresor} (MODE {mode}) - EN %".center(120))
    print("=" * 120)

    # Regrouper les probabilités par enchantement
    probas_par_enchantement = defaultdict(float)
    for (categorie, enchantement, source), prob in probas.items():
        probas_par_enchantement[(categorie, enchantement)] += prob

    for (categorie, enchantement), prob in sorted(probas_par_enchantement.items(), key=lambda x: x[1], reverse=True):
        if prob > 0:
            print(f"  🗡️ {categorie} - {enchantement}: {prob * 100:.6f}%")
# =============================================================================
# CALCUL DES PROBABILITÉS POUR TOUS LES NIVEAUX DE CONVERSION
# =============================================================================


# Exécuter l'affichage
def sauvegarder_probabilites_dans_json():
    """Calcule et sauvegarde toutes les probabilités dans un fichier JSON."""
    # Dossier pour sauvegarder les fichiers JSON
    dossier_sauvegarde = "probabilites"
    if not os.path.exists(dossier_sauvegarde):
        os.makedirs(dossier_sauvegarde)

    # Date et heure pour le nom du fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = os.path.join(dossier_sauvegarde, f"probabilites_{timestamp}.json")

    # Calculer toutes les données à sauvegarder
    données = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "description": "Probabilités d'obtenir chaque enchantement via les trésors et les conversions de livres.",
            "mode_admin": IS_ADMIN,
        },
        "probabilites_conversions": {},
        "probabilites_tresors": {},
        "probabilites_totales": {}
    }

    # 1. Sauvegarder les probabilités de conversion
    probas_conversions = calculer_toutes_probabilites_conversions()
    for niveau_depart in probas_conversions:
        données["probabilites_conversions"][f"{niveau_depart}→{niveau_depart+1}"] = {
            categorie: {
                enchantement: f"{prob * 100:.6f}%"
                for enchantement, prob in probas_conversions[niveau_depart][niveau_depart+1][categorie].items()
                if prob > 0
            }
            for categorie in probas_conversions[niveau_depart][niveau_depart+1]
        }

    # 2. Sauvegarder les probabilités pour chaque niveau de trésor (1 à 47)
    for niveau_tresor in range(1, 48):
        données["probabilites_tresors"][f"niveau_{niveau_tresor}"] = {
            "normal": {
                f"{categorie} - {enchantement}": f"{prob * 100:.6f}%"
                for (categorie, enchantement), prob in calculer_probabilite_enchantement_par_tresor(niveau_tresor, False).items()
                if prob > 0
            },
            "admin": {
                f"{categorie} - {enchantement}": f"{prob * 100:.6f}%"
                for (categorie, enchantement), prob in calculer_probabilite_enchantement_par_tresor(niveau_tresor, True).items()
                if prob > 0
            }
        }

    # 3. Sauvegarder les probabilités totales (trésors + conversions) pour chaque niveau de trésor
    for niveau_tresor in range(1, 48):
        probas_totales = calculer_probabilite_totale(niveau_tresor, False)
        probas_par_enchantement = defaultdict(float)
        for (categorie, enchantement, source), prob in probas_totales.items():
            probas_par_enchantement[(categorie, enchantement)] += prob

        données["probabilites_totales"][f"niveau_{niveau_tresor}_normal"] = {
            f"{categorie} - {enchantement}": f"{prob * 100:.6f}%"
            for (categorie, enchantement), prob in probas_par_enchantement.items()
            if prob > 0
        }

        # Mode admin
        probas_totales_admin = calculer_probabilite_totale(niveau_tresor, True)
        probas_par_enchantement_admin = defaultdict(float)
        for (categorie, enchantement, source), prob in probas_totales_admin.items():
            probas_par_enchantement_admin[(categorie, enchantement)] += prob

        données["probabilites_totales"][f"niveau_{niveau_tresor}_admin"] = {
            f"{categorie} - {enchantement}": f"{prob * 100:.6f}%"
            for (categorie, enchantement), prob in probas_par_enchantement_admin.items()
            if prob > 0
        }

    # Sauvegarder dans le fichier JSON
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        json.dump(données, fichier, indent=4, ensure_ascii=False)

    print(f"\n✅ Les probabilités ont été sauvegardées dans : {nom_fichier}")
    return nom_fichier



# =============================================================================
# EXÉCUTION
# =============================================================================

if __name__ == "__main__":
    import os
    import sys

    # 1. Sauvegarder toutes les probabilités dans un fichier JSON
    fichier_json = sauvegarder_probabilites_dans_json()

    # 2. Afficher un résumé des probabilités
    print("\n" + "=" * 120)
    print("RÉSUMÉ DES PROBABILITÉS (EN %)".center(120))
    print("=" * 120)

    # Afficher les probabilités de conversion
    afficher_probabilites_conversions()

    # Afficher les probabilités pour le trésor niveau 47 en mode normal
    afficher_probabilites_tresor(47, is_admin=False)

    # Afficher les probabilités pour le trésor niveau 47 en mode admin
    afficher_probabilites_tresor(47, is_admin=True)

    # Afficher les probabilités totales pour le trésor niveau 47 en mode admin
    afficher_probabilites_totales(47, is_admin=True)


























