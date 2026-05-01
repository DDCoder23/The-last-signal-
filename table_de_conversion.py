from inventaire import safe_increment, Objet,Livres,dict_enchant
import random
from dataclasses import dataclass, asdict


@dataclass
class StatsConversion:
    
    livres_convertis: int = 0
    



def vérifier(category,*args):
    en=[]
    liste1=[]
    liste2=[]
    liste3=[]
    liste4=[]
    liste5=[]
    liste6=[]
    if len(args)<2:
        return
    for lv in args:
        if not isinstance(lv,Livres):
            return
        if not liste1:
            liste1=lv.enchantements
        elif not liste2:
            liste2=lv.enchantements
        elif not liste3:
            liste3=lv.enchantements
        elif not liste4:
            liste4=lv.enchantements
        elif not liste5:
            liste5=lv.enchantements
        elif not liste6:
            liste6=lv.enchantements




        while len(en)!= len(args):
            for ele in liste1:
                if ele in liste2:
                    ind=dict_enchant[len(args)-1][category].index(ele)
                    en.append(dict_enchant[len(args)][category][ind])
                elif ele in liste3:
                    ind=dict_enchant[len(args)-1][category].index(ele)
                    en.append(dict_enchant[len(args)][category][ind])
                elif ele in liste4:
                    ind=dict_enchant[len(args)-1][category].index(ele)
                    en.append(dict_enchant[len(args)][category][ind])
                elif ele in liste5:
                    ind=dict_enchant[len(args)-1][category].index(ele)
                    en.append(dict_enchant[len(args)][category][ind])
                                         
                elif ele in liste6:
                    ind=dict_enchant[len(args)-1][category].index(ele)
                    en.append(dict_enchant[len(args)][category][ind])
                en=list(filter(lambda x: x is not None, en))
            if len(args)>2:
                for i in range( len(args)-2):
                    for ele in en:
                        if ele in liste1:
                            ind=dict_enchant[len(args)-1][category].index(ele)
                            en.append(dict_enchant[len(args)][category][ind])
                        elif ele in liste2:
                            ind=dict_enchant[len(args)-1][category].index(ele)
                            en.append(dict_enchant[len(args)][category][ind])
                        elif ele in liste3:
                            ind=dict_enchant[len(args)-1][category].index(ele)
                            en.append(dict_enchant[len(args)][category][ind])
                        elif ele in liste4:
                            ind=dict_enchant[len(args)-1][category].index(ele)
                            en.append(dict_enchant[len(args)][category][ind])
                        elif ele in liste5:
                            ind=dict_enchant[len(args)-1][category].index(ele)
                            en.append(dict_enchant[len(args)][category][ind])
                        elif ele in liste6:
                            ind=dict_enchant[len(args)-1][category].index(ele)
                            en.append(dict_enchant[len(args)][category][ind])
            en=list(filter(lambda x: x is not None, en))
            set(en)
            if len(en)!= len(args):
                en.append(random.choice(dict_enchant[len(args)-1][category]))
    return en






            
            

def qtes(nom, joueur):

    if nom not in joueur.stuff:
        return 0

    obj = joueur.stuff[nom]
    if isinstance(obj, Livres):
        return obj.quantite,obj.category
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
    l,i= qtes("livre enchant niv 1", joueur)
    if  l >= 2 *nb2:
        for i in range (nb2):
            a=vérifier(i,"livre enchant niv 1","livre enchant niv 1")
            safe_increment(
            joueur.stuff,
            "livre enchant niv 1",
            quant=-2,
        )
            safe_increment(joueur.stuff, "livre enchant niv 2", quant=1,enchantements=a,)
        stats["livres_convertis"] += nb2*2
        print(f"Conversion réussie : {2*nb2} livres niv 1 → {nb2} livres niv 2.")

        return True


def l2_l3(joueur,nb3):
    pass
def l3_l4(joueur,nb4):
    pass

def l4_l5(joueur,nb5):
    pass


def l5_l6(joueur,nb6):
    pass
def convertir_livres(niveau_cible, nb, joueur):
    print(joueur.stuff)
    sta = StatsConversion()
    global stats
    stats = asdict(sta)

  

    if 1 < niveau_cible < 7 :
        if niveau_cible == 2:
            l1_l2(joueur,nb)
        elif niveau_cible == 3:
            l2_l3(joueur,nb)

        elif niveau_cible == 4:
            l3_l4(joueur,nb)

        elif niveau_cible == 5:
            l4_l5(joueur,nb)

        else:
            l5_l6(joueur,nb)

    stat = stats
    return stat
