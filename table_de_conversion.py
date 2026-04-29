from inventaire import safe_increment, Objet

from dataclasses import dataclass, asdict


@dataclass
class StatsConversion:
    livres_achetes: int = 0
    livres_convertis: int = 0
    gemmes_utilisees: int = 0


# Variables globales pour le suivi des conversions


def qtes(nom, joueur):

    if nom not in joueur.stuff:
        return 0

    obj = joueur.stuff[nom]

    # Cas 1 : C'est un objet de type Objet
    if isinstance(obj, Objet):
        return obj.quantite

    # Cas 2: C'est un nombre (int ou float)
    elif isinstance(obj, (int, float)):
        return obj

    # Cas 3 : Autre type (ne devrait pas arriver)
    else:
        print(f" Type inattendu pour {nom}: {type(obj)}")
        return 0


def l1_l2(joueur, nb2=2):

    manque = nb2 - qtes("livre enchant niv 2", joueur)
    if manque <= 0:
        return True

    if qtes("livre enchant niv 1", joueur) >= 2 * manque and manque == 1:
        safe_increment(
            joueur.stuff,
            "livre enchant niv 1",
            quant=-2,
        )
        safe_increment(joueur.stuff, "livre enchant niv 2", quant=1)
        stats["livres_convertis"] += 2
        print(f"Conversion réussie : 2 livres niv 1 → {manque} livres niv 2.")

        return True

    elif qtes("livre enchant niv 1", joueur) >= 2 * manque and manque == 2:
        safe_increment(
            joueur.stuff,
            "livre enchant niv 1",
            quant=-4,
        )
        safe_increment(joueur.stuff, "livre enchant niv 2", quant=2)

        stats["livres_convertis"] += 4
        print(f"Conversion réussie : 4 livres niv 1 → {manque} livres niv 2.")

        return True


def l2_l3(joueur):
    if qtes("livre enchant niv 3", joueur) >= 3:
        return True

    else:
        while qtes("livre enchant niv 3", joueur) < 3:
            if qtes("livre enchant niv 2", joueur) // 3 < 1:
                while qtes("livre enchant niv 2", joueur) < 3:
                    if qtes("livre enchant niv 1", joueur) >= 2:
                        safe_increment(joueur.stuff, "livre enchant niv 1", quant=-2)
                        safe_increment(joueur.stuff, "livre enchant niv 2", quant=1)
                        stats["livres_convertis"] += 2
                    else:
                        return False

            safe_increment(joueur.stuff, "livre enchant niv 2", quant=-3)
            safe_increment(joueur.stuff, "livre enchant niv 3", quant=1)
            stats["livres_convertis"] += 3

        print("conversion niv 2=> 3 réussie")
        return True


def l3_l4(joueur):
    if qtes("livre enchant niv 4", joueur) >= 4:
        return True

    else:
        while qtes("livre enchant niv 4", joueur) < 4:
            if qtes("livre enchant niv 3", joueur) // 4 < 1:
                while qtes("livre enchant niv 3", joueur) < 4:
                    if qtes("livre enchant niv 2", joueur) // 3 < 1:
                        while qtes("livre enchant niv 2", joueur) < 3:
                            safe_increment(
                                joueur.stuff, "livre enchant niv 1", quant=-2
                            )
                            safe_increment(joueur.stuff, "livre enchant niv 2", quant=1)
                            stats["livres_convertis"] += 2

                    else:
                        return False
                    safe_increment(joueur.stuff, "livre enchant niv 2", quant=-3)
                    safe_increment(joueur.stuff, "livre enchant niv 3", quant=1)
                    stats["livres_convertis"] += 3

            safe_increment(joueur.stuff, "livre enchant niv 3", quant=-4)
            safe_increment(joueur.stuff, "livre enchant niv 4", quant=1)
            stats["livres_convertis"] += 3

        print("conversion niv 3=> 4 réussie")
        return True


def l4_l5(joueur):
    pass


def l5_l6(joueur):
    pass
def l1_l2inf(joueur, nb2=2):
    if qtes("livre enchant niv 1", joueur) >= 2 *nb2:
        safe_increment(
            joueur.stuff,
            "livre enchant niv 1",
            quant=-2*nb2,
        )
        safe_increment(joueur.stuff, "livre enchant niv 2", quant=nb2)
        stats["livres_convertis"] += nb2*2
        print(f"Conversion réussie : {2*nb2} livres niv 1 → {nb2} livres niv 2.")

        return True


def l2_l3inf(joueur,nb3):
    pass
def l3_l4inf(joueur,nb4):
    pass

def l4_l5inf(joueur,nb5):
    pass


def l5_l6inf(joueur,nb6):
    pass
def convertir_livres(niveau_cible, nb, joueur,inf=False):
    print(joueur.stuff)
    sta = StatsConversion()
    global stats
    stats = asdict(sta)

    if 1 < niveau_cible < 7 and not inf:
        if niveau_cible == 2:
            l1_l2(joueur)
        elif niveau_cible == 3:
            l2_l3(joueur)

        elif niveau_cible == 4:
            l3_l4(joueur)

        elif niveau_cible == 5:
            l4_l5(joueur)

        else:
            l5_l6(joueur)
    if 1 < niveau_cible < 7 and inf:
        if niveau_cible == 2:
            l1_l2inf(joueur,nb)
        elif niveau_cible == 3:
            l2_l3inf(joueur,nb)

        elif niveau_cible == 4:
            l3_l4inf(joueur,nb)

        elif niveau_cible == 5:
            l4_l5inf(joueur,nb)

        else:
            l5_l6inf(joueur,nb)

    stat = stats
    return stat
