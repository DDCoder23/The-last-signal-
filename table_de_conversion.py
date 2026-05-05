
from index_manager import mettre_a_jour_index
from inventaire import safe_increment, Objet, Livres, dict_enchant,nettoyer_stuff_zero,clefs
import random
from dataclasses import dataclass, asdict
lvs=[]

@dataclass
class StatsConversion:
    
    livres_utilises = 0
    livres_crees=0
def qtes(nom: str, joueur: 'joueur') :
    """Retourne la quantité et la catégorie d'un objet dans l'inventaire du joueur."""
    if nom not in joueur.stuff:
        return 0, None
    obj = joueur.stuff[nom]
    if isinstance(obj, Livres):
        return obj.quantite, obj.category
    if isinstance(obj, Objet):
        return obj.quantite, None
    if isinstance(obj, (int, float)):
        return obj, None
    print(f"Type inattendu pour {nom}: {type(obj)}")
    return 0, None
def chercher_livre(nb, dict_livre,lv1,clef1,joueur):
    lvs=[]
    for i in range(1,nb+1):
        for cle in dict_livre[1:]:
            lv_temp = joueur.stuff[cle]
            if lv_temp.category == lv1.category and lv_temp.enchantements:
                lvs.append(cle)
                
                break

            # Si pas de 2e livre trouvé avec la même catégorie
        if len(lvs)<i:
            
            lvs.append(clef1)
    return lvs[:nb]


def fusionner_enchantements(niv: int, *listes: list) -> list:
    """
    Fusionne jusqu'à 6 listes d'enchantements en :
    - Supprimant les enchantements de niveau inférieur si un niveau supérieur existe.
    - Limitant le résultat à `niv` enchantements.
    - Conservant les enchantements de niveau supérieur.
    """
    niveaux_romains = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
    # Dictionnaire pour suivre le niveau maximal de chaque enchantement
    enchantements_max = {}
    def niveau_to_romain(n: int) -> str:
        romains = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
        return romains.get(n, "I")
    # Fonction pour extraire le niveau d'un enchantement (ex: "Poison VI" -> 6)
    def get_niveau(enchant: str) -> int:
        niveaux_romains = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
        parts = enchant.split()
        if len(parts) < 2:
            return 0
        niveau_str = parts[-1]
        return niveaux_romains.get(niveau_str, 0)

    # Fonction pour extraire le nom de l'enchantement (ex: "Poison VI" -> "Poison")
    def get_nom(enchant: str) -> str:
        parts = enchant.split()
        return " ".join(parts[:-1]) if len(parts) > 1 else enchant

    # Traiter chaque liste
    for liste in listes:
        for enchant in liste:
            nom = get_nom(enchant)
            niveau = get_niveau(enchant)

            # Si l'enchantement n'est pas encore présent ou si le nouveau niveau est supérieur
            if nom not in enchantements_max or niveau > enchantements_max[nom]:
                enchantements_max[nom] = niveau

    # Reconstruire la liste des enchantements avec leur niveau maximal
    liste_fusionnee = [f"{nom} {niveau_to_romain(niveau)}" for nom, niveau in enchantements_max.items()]

    # Fonction pour convertir un niveau en chiffres romains


    # Trier par niveau décroissant
    liste_fusionnee.sort(key=lambda x: get_niveau(x), reverse=True)

    # Limiter à `niv` enchantements
    if len(liste_fusionnee) > niv:
        liste_fusionnee = liste_fusionnee[:niv]

    return liste_fusionnee
def obtenir_enchantement_superieur(enchantement: str) -> str:
    """
    Retourne l'enchantement de niveau supérieur pour un enchantement donné.
    Exemple : "Poison I" → "Poison II"
    """
    # Extraire le nom et le niveau de l'enchantement
    parts = enchantement.split()
    if len(parts) < 2:
        return enchantement  # Si pas de niveau, retourne l'enchantement tel quel

    nom = " ".join(parts[:-1])  # Ex: "Poison"
    niveau_str = parts[-1]    # Ex: "I"

    # Trouver le niveau actuel (I=1, II=2, etc.)
    niveau_actuel = 0
    if niveau_str == "I":
        niveau_actuel = 1
    elif niveau_str == "II":
        niveau_actuel = 2
    elif niveau_str == "III":
        niveau_actuel = 3
    elif niveau_str == "IV":
        niveau_actuel = 4
    elif niveau_str == "V":
        niveau_actuel = 5
    elif niveau_str == "VI":
        niveau_actuel = 6
    else:
        return enchantement  # Si le niveau n'est pas reconnu, retourne l'enchantement tel quel

    # Trouver l'enchantement de niveau supérieur
    if niveau_actuel < 6:
        niveau_superieur = niveau_actuel + 1
        niveau_romain = ["I", "II", "III", "IV", "V", "VI"][niveau_superieur - 1]
        return f"{nom} {niveau_romain}"
    else:
        return enchantement  # Si déjà au niveau max, retourne l'enchantement tel quel
def convertir_livres(joueur, niv, nb):
    stats = StatsConversion()
    
  

    if 1 < niv < 7 :
        if niv == 2:
            l1_l2(joueur,nb,stats)
        elif niv == 3:
            l2_l3(joueur,nb,stats)

        elif niv== 4:
            l3_l4(joueur,nb,stats)

        elif niv == 5:
            l4_l5(joueur,nb,stats)

        else:
            l5_l6(joueur,nb,stats)
        mettre_a_jour_index(joueur.stuff)
    return {"livres_utilises" : stats.livres_utilises,"livres_crees" : stats.livres_crees}
    print(asdict(stats))
    return asdict(stats) 
def l1_l2(joueur,nb,stats):
    for i in range(nb):
        livres_niv1 = [
        cle for cle, obj in joueur.stuff.items()
        if isinstance(obj, Livres) and obj.niv == 1 and obj.quantite > 0
    ]

        
    for _ in range(nb):
        
        random.shuffle(livres_niv1)

        
        clef1 = livres_niv1[0]
        lv1 = joueur.stuff[clef1]
        clef2=None
        clef2=chercher_livre(1, livres_niv1,lv1,clef1,joueur)[0]
        

            

        
        lv2 = joueur.stuff[clef2]

        if (lv1.category == lv2.category and
            lv1.enchantements and lv2.enchantements):
            enchantements=fusionner_enchantements(2,lv1.enchantements, lv2.enchantements)
            print(enchantements)
            category=lv1.category
            safe_increment(joueur.stuff, lv1, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv2, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, "livre enchant niv 2", quant=1, type_objet="livres",enchantements=enchantements,category=category)
            stats.livres_utilises += 2
            stats.livres_crees +=1
            
        else:
            print(f"Catégories différentes ou pas d'enchantements pour {clef1} et {clef2}")
def l2_l3(joueur,nb,stats):
    for i in range(nb):
        livres_niv2 = [
        cle for cle, obj in joueur.stuff.items()
        if isinstance(obj, Livres) and obj.niv == 2 and obj.quantite > 0
    ]

        
    for _ in range(nb):
        
        random.shuffle(livres_niv2)

        
        clef1 = livres_niv2[0]
        lv1 = joueur.stuff[clef1]
        clef2=None
        clef3=None
        clefs_lv=chercher_livre(2, livres_niv2,lv1,clef1,joueur)
        clef2=clefs_lv[0]
        clef3=clefs_lv[1]
        lv2 = joueur.stuff[clef2]
        lv3 = joueur.stuff[clef3]

        if (lv1.category == lv2.category==lv3.category and
            lv1.enchantements and lv2.enchantements and lv3.enchantements):
            enchantements=fusionner_enchantements(3,lv1.enchantements, lv2.enchantements, lv3.enchantements)
            print(enchantements)
            category=lv1.category
            safe_increment(joueur.stuff, lv1, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv2, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv3, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, "livre enchant niv 3", quant=1, type_objet="livres",enchantements=enchantements,category=category)
            stats.livres_utilises += 3
            stats.livres_crees +=1
            
        else:
            print(f"Catégories différentes ou pas d'enchantements pour {clef1} et {clef2} et {clef3}")
def l3_l4(joueur,nb,stats):
    for i in range(nb):
        livres_niv3 = [
        cle for cle, obj in joueur.stuff.items()
        if isinstance(obj, Livres) and obj.niv == 3 and obj.quantite > 0
    ]

        
    for _ in range(nb):
        
        random.shuffle(livres_niv3)

        
        clef1 = livres_niv3[0]
        lv1 = joueur.stuff[clef1]
        clef2=None
        clef3=None
        clef4=None
        clefs_lv=chercher_livre(3, livres_niv3,lv1,clef1,joueur)
        clef2=clefs_lv[0]
        clef3=clefs_lv[1]
        clef4=clefs_lv[2]
        lv2 = joueur.stuff[clef2]
        lv3 = joueur.stuff[clef3]
        lv4 = joueur.stuff[clef4]

        if (lv1.category == lv2.category==lv3.category==lv4.category and
            lv1.enchantements and lv2.enchantements and lv3.enchantements and lv4.enchantements):
            enchantements=fusionner_enchantements(4,lv1.enchantements, lv2.enchantements, lv3.enchantements,lv4.enchantements)
            print(enchantements)
            category=lv1.category
            safe_increment(joueur.stuff, lv1, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv2, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv3, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv4, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, "livre enchant niv 4", quant=1, type_objet="livres",enchantements=enchantements,category=category)
            stats.livres_utilises += 4
            stats.livres_crees +=1
            
        else:
            print(f"Catégories différentes ou pas d'enchantements pour {clef1} et {clef2} et {clef3} et {clef4}")
            
def l4_l5(joueur,nb,stats):
    for i in range(nb):
        livres_niv4 = [
        cle for cle, obj in joueur.stuff.items()
        if isinstance(obj, Livres) and obj.niv == 4 and obj.quantite > 0
    ]

        
    for _ in range(nb):
        
        random.shuffle(livres_niv4)

        
        clef1 = livres_niv4[0]
        lv1 = joueur.stuff[clef1]
        clef2=None
        clef3=None
        clef4=None
        clef5= None
        clefs_lv=chercher_livre(4, livres_niv4,lv1,clef1,joueur)
        clef2=clefs_lv[0]
        clef3=clefs_lv[1]
        clef4=clefs_lv[2]
        clef5=clefs_lv[3]
        lv2 = joueur.stuff[clef2]
        lv3 = joueur.stuff[clef3]
        lv4 = joueur.stuff[clef4]
        lv5= joueur.stuff[clef5]


        if (lv1.category == lv2.category==lv3.category==lv4.category==lv5.category and
            lv1.enchantements and lv2.enchantements and lv3.enchantements and lv4.enchantements and lv5.enchantements):

            enchantements=fusionner_enchantements(5,lv1.enchantements, lv2.enchantements, lv3.enchantements,lv4.enchantements,lv5.enchantements)
            print(enchantements)
            category=lv1.category
            safe_increment(joueur.stuff, lv1, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv2, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv3, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv4, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv5, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, "livre enchant niv 5", quant=1, type_objet="livres",enchantements=enchantements,category=category)
            stats.livres_utilises += 5
            stats.livres_crees +=1
            
        else:
            print(f"Catégories différentes ou pas d'enchantements pour {clef1} et {clef2} et {clef3} et {clef4} et {clef5}")

def l5_l6(joueur,nb,stats):
    for i in range(nb):
        livres_niv5 = [
        cle for cle, obj in joueur.stuff.items()
        if isinstance(obj, Livres) and obj.niv == 5 and obj.quantite > 0
    ]

        
    for _ in range(nb):
        
        random.shuffle(livres_niv5)

        
        clef1 = livres_niv5[0]
        lv1 = joueur.stuff[clef1]
        clef2=None
        clef3=None
        clef4=None
        clef5= None
        clef6=None
        clefs_lv=chercher_livre(5, livres_niv5,lv1,clef1,joueur)
        clef2=clefs_lv[0]
        clef3=clefs_lv[1]
        clef4=clefs_lv[2]
        clef5=clefs_lv[3]
        clef6=clefs_lv[4]
        lv2 = joueur.stuff[clef2]
        lv3 = joueur.stuff[clef3]
        lv4 = joueur.stuff[clef4]
        lv5= joueur.stuff[clef5]
        lv6= joueur.stuff[clef6]


        if (lv1.category == lv2.category==lv3.category==lv4.category==lv5.category ==lv6.category and
            lv1.enchantements and lv2.enchantements and lv3.enchantements and lv4.enchantements and lv5.enchantements,lv6.enchantements):
            enchantements=fusionner_enchantements(6,lv1.enchantements, lv2.enchantements, lv3.enchantements,lv4.enchantements,lv5.enchantements,lv6.enchantements)
            print(enchantements)
            category=lv1.category
            safe_increment(joueur.stuff, lv1, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv2, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv3, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv4, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv5, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, lv6, quant=-1, type_objet="livres", ajouter=False)
            safe_increment(joueur.stuff, "livre enchant niv 6", quant=1, type_objet="livres",enchantements=enchantements,category=category)
            stats.livres_utilises += 6
            stats.livres_crees +=1
            
        else:
            print(f"Catégories différentes ou pas d'enchantements pour {clef1} et {clef2} et {clef3} et {clef4} et {clef5} et {clef6} ")




          
  








            
            

