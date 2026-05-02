from typing import Dict, Set

# Index global (singleton)
_index_recherche: Dict[str, Set[str]] = {}

def initialiser_index():
    """Initialise l'index global."""
    global _index_recherche
    _index_recherche = {}

def mettre_a_jour_index(inventaire: Dict[str, any]):
    """Met à jour l'index avec le contenu de l'inventaire."""
    global _index_recherche
    _index_recherche = {}
    for cle, objet in inventaire.items():
        _ajouter_objet_au_index(cle, objet)

def _ajouter_objet_au_index(cle: str, objet: any):
    """Ajoute un objet à l'index (méthode interne)."""
    global _index_recherche

    # 1. Nom (sans les numéros de série)
    nom_base = getattr(objet, "nom_base", cle).replace("_", " ").lower()
    _ajouter_mot_cle(nom_base, cle)

    # 2. Type
    type_objet = getattr(objet, "type_objet", "").lower()
    _ajouter_mot_cle(type_objet, cle)

    # 3. Niveau
    niv = getattr(objet, "niv", None)
    if niv is not None:
        if isinstance(niv, str) and niv.isdigit():
            niv = int(niv)
        _ajouter_mot_cle(f"niv{niv}", cle)

    # 4. Enchantements (pour les livres/armes)
    if hasattr(objet, "enchantements") and objet.enchantements:
        for enchant in objet.enchantements:
            _ajouter_mot_cle(enchant.lower(), cle)

    # 5. Effet (pour les potions)
    effet = getattr(objet, "effet", None)
    if effet is not None:
        _ajouter_mot_cle(str(effet).lower(), cle)

def _ajouter_mot_cle(mot_cle: str, cle_objet: str):
    """Ajoute un mot-clé à l'index (méthode interne)."""
    global _index_recherche
    if not mot_cle:
        return
    if mot_cle not in _index_recherche:
        _index_recherche[mot_cle] = set()
    _index_recherche[mot_cle].add(cle_objet)

def rechercher_dans_index(texte: str, inventaire: Dict[str, any]) -> Set[str]:
    """Recherche des clés dans l'index correspondant au texte."""
    global _index_recherche
    if not texte:
        return set(inventaire.keys())

    texte = texte.lower()
    mots_cles = texte.split()

    # Trouver toutes les clés qui correspondent à AU MOINS UN mot-clé
    resultats = set()
    for mot in mots_cles:
        if mot in _index_recherche:
            resultats.update(_index_recherche[mot])

    # Filtrer pour ne garder que les clés existantes dans l'inventaire
    return resultats & set(inventaire.keys())

def supprimer_de_l_index(cle_objet: str):
    """Supprime une clé de l'index."""
    global _index_recherche
    for mot_cle, cles in list(_index_recherche.items()):
        if cle_objet in cles:
            cles.remove(cle_objet)
            if not cles:  # Si plus aucune clé n'est associée à ce mot-clé
                del _index_recherche[mot_cle]