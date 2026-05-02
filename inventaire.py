import json
import os
import sys
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QDialog,
    QSpinBox,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import asyncio
import random
from index_manager import mettre_a_jour_index, supprimer_de_l_index
global livres_par_enchantements

livres_par_enchantements = {}
global clefs
clefs={}
def trouver_cles_par_liste_non_ordonnee(dictionnaire, liste_recherchee):
    """Trouve toutes les clés dont la valeur est une liste avec les mêmes éléments (ordre indifférent)."""
    return [
        cle for cle, valeur in dictionnaire.items()
        if set(valeur) == set(liste_recherchee) and len(valeur) == len(liste_recherchee)
    ]


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





liste_armes = [
    "explosifs",
    "armes tranchantes",
    "armes à feu",
    "armes perforantes",
    "armes contendantes",
    "épée de bois",
    "épée de pierre",
    "missiles",
]
liste_outils = ["outils"]
liste_muni = [
    "flèches communes",
    "flèches peu rares",
    "flèches rares",
    "flèches super rares",
    "flèches exotiques",
    "flèches épiques",
    "flèches légendaire",
    "chargeur",
    "carreau d'arbalète",
    "balles",
]
liste_potion = [
    "potion de mana",
    "potion rare",
    "potion de soin léger",
    "potion de soin modéré",
    "potion de délivrance",
]
dict_enchant={1: {"épée":["Aura de feu I","Poison I","Durability I","Putréfaction I","Foudre I", "Critique I"], "armes à feu":["Rapidity I", "Critique I"],"armure":["Respiration I", "Durability I","Vitality I","Protection I", "Renvoie I"]},
             2: {"épée":["Aura de feu II","Poison II", "Durability II","Putréfaction II","Foudre II", "Critique II"], "armes à feu":["Rapidity II", "Critique II"],"armure":["Respiration II", "Durability II","Vitality II","Protection II", "Renvoie II"]},
             3: {"épée":["Aura de feu III","Poison III", "Durability III","Putréfaction III","Foudre III", "Critique III"], "armes à feu":["Rapidity III" "Critique III"],"armure":["Respiration III", "Durability III","Vitality III","Protection III", "Renvoie III"]},
             4: {"épée":["Aura de feu IV","Poison IV", "Durability IV","Putréfaction IV","Foudre IV","Critique IV"], "armes à feu":["Rapidity IV", "Critique IV"],"armure":["Respiration IV", "Durability IV","Vitality IV","Protection IV", "Renvoie IV"]},
             5: {"épée":["Aura de feu V","Poison V", "Durability V","Putréfaction V","Foudre V", "Critique V"], "armes à feu":["Rapidity V", "Critique V"],"armure":["Respiration V", "Durability V","Vitality V","Protection V", "Renvoie V"]},
             6: {"épée":["Aura de feu VI","Poison VI", "Durability VI","Putréfaction VI","Foudre VI", "Critique VI"], "armes à feu":["Rapidity VI", "Critique VI"],"armure":["Respiration VI", "Durability VI","Vitality VI","Protection VI", "Renvoie VI"]},
}
from itertools import combinations


# Cache global pour stocker toutes les combinaisons possibles
cache_enchantements = {}

from itertools import combinations





def pregenerer_cache_enchantements():
    """Pré-génère toutes les combinaisons possibles pour chaque niveau et catégorie,
    en incluant également les enchantements des niveaux inférieurs."""
    global cache_enchantements
    cache_enchantements = {}  # Réinitialiser le cache

    # Parcourir chaque niveau
    for niveau in dict_enchant.keys():
        cache_enchantements[niveau] = {}

        # Collecter tous les enchantements des niveaux <= niveau actuel
        all_enchantements_by_category = {}
        for current_niveau in range(1, niveau + 1):
            if current_niveau in dict_enchant:
                for categorie, enchantements in dict_enchant[current_niveau].items():
                    if categorie not in all_enchantements_by_category:
                        all_enchantements_by_category[categorie] = []
                    all_enchantements_by_category[categorie].extend(enchantements)

        # Générer les combinaisons pour chaque catégorie
        for categorie, enchantements in all_enchantements_by_category.items():
            max_taille = min(niveau, len(enchantements))
            combinaisons = []
            for taille in range(1, max_taille + 1):
                combinaisons.extend(list(combinations(enchantements, taille)))
            cache_enchantements[niveau][categorie] = [list(combo) for combo in combinaisons]
def ajouter_enchant(niveau: int) -> tuple[list[str], str]:
    """
    Retourne une combinaison aléatoire parmi toutes les possibles pour un niveau donné.
    """
    if niveau not in cache_enchantements:
        pregenerer_cache_enchantements()


    categories = list(cache_enchantements[niveau].keys())
    poids = [0.7, 0.05,0.25]
    categorie = random.choices(categories, weights=poids, k=1)[0]

    # Choisir une combinaison aléatoire parmi celles possibles pour cette catégorie
    combinaisons = cache_enchantements[niveau][categorie]
    en = random.choice(combinaisons)
    return en,categorie


def trier(inventaire):
    """Trie l'inventaire selon les règles définies."""
    prioritaires = ["argent", "gemmes"]
    livres_enchant = []
    objets_enchantes = []
    autres_objets = []
    inv = inventaire

    async def _trier(inventaire):
        for nom, obj in inv.items():
            if nom in prioritaires:
                continue  # Déjà en tête
            elif nom.startswith("livre enchant niv"):
                livres_enchant.append((nom, obj))
            if isinstance(obj, Armes) or isinstance(obj, equipement):
                objets_enchantes.append((nom, obj))
            else:
                autres_objets.append((nom, obj))

        # Tri des livres d'enchant par niveau décroissant
        livres_enchant.sort(key=lambda x: int(x[0].split()[-1]), reverse=True)

        # Tri des objets enchantés par niveau décroissant
        objets_enchantes.sort(key=lambda x: x[1].niv, reverse=True)

        # Tri des autres objets par ordre alphabétique
        autres_objets.sort(key=lambda x: x[0])

        # Construction de l'inventaire trié
        inventaire = {nom: inv[nom] for nom in prioritaires if nom in inv}
        inventaire.update({nom: obj for nom, obj in livres_enchant})
        inventaire.update({nom: obj for nom, obj in objets_enchantes})
        inventaire.update({nom: obj for nom, obj in autres_objets})

        return inventaire

    asyncio.run(_trier(inventaire))


class Objet:
    def __init__(self, nom, image=None, quantite=1, type_objet="de base", **kwargs):
        self.nom_base = nom.replace(" ", "_")
        self.quantite = quantite
        self.type_objet = type_objet
        self.nom_image=image
        for key, value in kwargs.items():
            setattr(self, key, value)

    def attribut_superieur_a_un(self, nom_attribut: str) -> bool:
        return hasattr(self, nom_attribut) and getattr(self, nom_attribut) != []

    def nom_affiche(self):
        base = self.nom_base
        if self.attribut_superieur_a_un("enchantements") and self.type_objet!="livres":
            return f"{base} enchanté(e)"
        return base

    @property
    def nom(self):
        return self.nom_affiche()
    @property
    def image(self):
       return self.nom_image +".png" if self.nom_image!= None else " "

    def ajouter(self, qte):
        self.quantite += qte

    def retirer(self, qte):
        self.quantite = max(0, self.quantite - qte)

    def __repr__(self):
        return f"{self.quantite:,} "


class equipement(Objet):
    def __init__(
        self, nom, image, quantite=1, type_objet="equipement", niv=1, bonus=5,enchantements=[]
    ):
        
        super().__init__(nom, image, quantite, type_objet)
        self.parts=self.nom.split()
        self.niv = niv
        self.bonus = bonus
        self.category=self.parts[0]
        self.enchantements=enchantements 

    def __repr__(self):
        
        enchants = self.enchantements if self.enchantements else []
        return f"{self.quantite:,} [Niveau{self.niv}| bonus :{self.bonus}| enchantements : {enchants}]"

    def enchanter(self,enc):
        for en in self.enchantements:
            for e in enc:
                if e.startswith==en:
                    del self.enchantements[e]
                self.enchantements.append(enc)


class Armes(equipement):
    def __init__(
        self,
        nom,
        image,
        quantite=1,
        type_objet="Armes",
        niv=1,
        durabilite=100,
        bonus=5,
        enchantements=[]
    ):
        
        super().__init__(nom, image, quantite, type_objet)
        self.durabilite = durabilite
        self.durabilite_max=durabilite
        self.niv= niv
        self.bonus = bonus
        self.parts=self.nom.split()
        self.category=self.parts[0]
        self.enchantements=enchantements

    def __repr__(self):
        enchants = self.enchantements if self.enchantements else []
        return f"{self.quantite:,} [Niveau{self.niv}| bonus :{self.bonus}| enchantements : {enchants} | dura : {self.durabilite}/{self.durabilite_max} ]"
    @property
    def taux_de_critique(self):
        return self.bonus/100

        
    def enchanter(self,enc):
        for en in self.enchantements:
            for e in enc:
                if e.startswith==en:
                    del self.enchantements[e]
                self.enchantements.append(enc)


class Potion(Objet):
    def __init__(self, nom, image, quantite=1, type_objet="potion", **kwargs):
        super().__init__(nom, image, quantite, type_objet)
        self.effet=kwargs.get("effet",None)

    def appliquer_effet(self):
        pass
class Livres(Objet):
    def __init__(self, nom, image, quantite=1, type_objet="livres",category=None,enchantements=None,niv=1, **kwargs):

        super().__init__(nom, image, quantite, type_objet)
        
        self.enchantements=enchantements
        self.category=category
        self.niv=niv
    def __repr__(self):
       enchants_str = "|".join(self.enchantements) if self.enchantements else "Aucun"
       return f"{self.quantite:,} [Niveau {self.niv} | {enchants_str}]"

        
    



        
def nettoyer_stuff_zero(inventaire):
    a_supprimer = []

    async def _nettoyer(inventaire):
        for nom, obj in inventaire.items():
            if isinstance(obj, Objet):
                if obj.quantite <= 0:
                    a_supprimer.append(nom)

        for nom in a_supprimer:
            if nom in inventaire:
                obj = inventaire[nom]
                if isinstance(obj, Livres):
                    # ✅ Supprime de l'index livres_par_enchantements
                    cle_enchantements = tuple(obj.enchantements)
                    if cle_enchantements in livres_par_enchantements:
                        del livres_par_enchantements[cle_enchantements]
                supprimer_de_l_index(nom)
                del inventaire[nom]
        mettre_a_jour_index(inventaire)


    asyncio.run(_nettoyer(inventaire))
def generer_cle_unique(inventaire, nom_base):
    """Génère une clé unique pour un objet dans l'inventaire."""
    if nom_base not in clefs:
        return f"{nom_base} n°1",1
    else:
        return f'{nom_base} n°{clefs[nom_base] +1}',clefs[nom_base]+1



def safe_increment(
    inventaire, nom, image=None, quant=1, type_objet="base", ajouter=True, **kwargs
):
  
    
    # Mettre à jour le compteur global pour ce type d'objet
    if nom not in clefs:
        clefs[nom] = 0


    # --- Cas 1 : Armes ---
    if type_objet.lower() == "armes" and ajouter:
        for _ in range(quant):
            cle, i = generer_cle_unique(inventaire, nom)
            inventaire[cle] = Armes(
                nom=nom,
                image=image,
                quantite=1,  # ✅ 1 par objet
                niv=kwargs.get("niv", 1),
                durabilite=kwargs.get("durabilite", 100),
                enchantements=kwargs.get("enchantements", []),
            )
        clefs[nom] += 1
        mettre_a_jour_index(inventaire)
        return

    # --- Cas 2 : Équipement ---
    if type_objet.lower() == "équipement" and ajouter:
        for _ in range(quant):
            cle, i = generer_cle_unique(inventaire, nom)
            inventaire[cle] = equipement(
                nom=nom,
                image=image,
                quantite=1,  # ✅ 1 par objet
                niv=kwargs.get("niv", 1),
                enchantements=kwargs.get("enchantements", []),
            )
            clefs[nom] += 1
        mettre_a_jour_index(inventaire)
        return

    # --- Cas 3 : Livres ---
    if type_objet.lower() == "livres" and ajouter:
        

        for _ in range(quant):
            enchantements = kwargs.get("enchantements", [])
            cles_trouvees = trouver_cles_par_liste_non_ordonnee(livres_par_enchantements, enchantements)
            if cles_trouvees:
                inventaire[cles_trouvees[0]].ajouter(quant)
                mettre_a_jour_index(inventaire)
                return
            else:
                cle, i = generer_cle_unique(inventaire, nom)
                inventaire[cle] = Livres(
                nom=nom,
                image=image,
                quantite=1,
                enchantements=kwargs.get("enchantements"),
                category=kwargs.get("category", None),
                niv=kwargs.get("niv",1)
            )

                clefs[nom] += 1
                livres_par_enchantements[cle]=kwargs.get("enchantements")
        mettre_a_jour_index(inventaire)
        return

    # --- Cas 4 : Objet existant (non-Armes/Équipement/Livres) ---
    if nom in inventaire:
        obj = inventaire[nom]
        if isinstance(obj, Objet):
            if ajouter:
                obj.ajouter(quant)
            else:
                obj.retirer(quant)
                if obj.quantite <= 0:
                    # Supprimer de l'index si c'est un livre
                    if isinstance(obj, Livres):
                        cle_enchantements = (tuple(obj.enchantements), obj.category)
                        if cle_enchantements in livres_par_enchantements:
                            del livres_par_enchantements[cle_enchantements]
                    del inventaire[nom]
        else:
            # Cas où l'objet est un nombre (int/float)
            inventaire[nom] += quant if ajouter else -quant
        nettoyer_stuff_zero(inventaire)
        mettre_a_jour_index(inventaire)
        return

    # --- Cas 5 : Nouvel objet (non-Armes/Équipement/Livres) ---
    if type_objet == "potion":
        inventaire[nom] = Potion(
            nom, image, quant, type_objet=type_objet, effet=kwargs.get("effet", None)
        )
    elif type_objet == "de base" or type_objet == "base":
        inventaire[nom] = Objet(nom, image, quant)
    nettoyer_stuff_zero(inventaire)
    mettre_a_jour_index(inventaire)


class QuantiteDialog(QDialog):
    def __init__(self, nom_objet, prix, argent_joueur, parent=None):
        super(QuantiteDialog, self).__init__(parent)
        self.setWindowTitle(f"Acheter {nom_objet}")
        self.setMinimumWidth(300)

        # Layout principal
        layout = QVBoxLayout(self)

        # Label pour le nom de l'objet
        self.label_nom = QLabel(f"Objet: {nom_objet}")
        layout.addWidget(self.label_nom)

        # Label pour le prix
        self.label_prix = QLabel(f"Prix unitaire: {prix} pièces d'or")
        layout.addWidget(self.label_prix)

        # Label pour l'argent du joueur
        self.label_argent = QLabel(f"Votre argent: {argent_joueur} pièces d'or")
        layout.addWidget(self.label_argent)

        # Layout horizontal pour les boutons et le champ de quantité
        quantite_layout = QHBoxLayout()

        # Bouton -
        self.bouton_moins = QPushButton("-")
        self.bouton_moins.clicked.connect(self.diminuer_quantite)

        # Champ de quantité
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(1000)
        self.spin_box.setValue(1)

        # Bouton +
        self.bouton_plus = QPushButton("+")
        self.bouton_plus.clicked.connect(self.augmenter_quantite)

        # Ajout des widgets au layout horizontal
        quantite_layout.addWidget(self.bouton_moins)
        quantite_layout.addWidget(self.spin_box)
        quantite_layout.addWidget(self.bouton_plus)

        # Ajout du layout horizontal au layout principal
        layout.addLayout(quantite_layout)

        # Label pour le prix total
        self.label_prix_total = QLabel(f"Prix total: {prix} pièces d'or")
        layout.addWidget(self.label_prix_total)

        # Boutons OK et Annuler
        self.bouton_ok = QPushButton("OK")
        self.bouton_ok.clicked.connect(self.accept)
        self.bouton_annuler = QPushButton("Annuler")
        self.bouton_annuler.clicked.connect(self.reject)

        # Layout horizontal pour les boutons OK et Annuler
        boutons_layout = QHBoxLayout()
        boutons_layout.addWidget(self.bouton_ok)
        boutons_layout.addWidget(self.bouton_annuler)

        # Ajout du layout horizontal au layout principal
        layout.addLayout(boutons_layout)

        # Stocker les informations de l'objet
        self.nom_objet = nom_objet
        self.prix = prix
        self.argent_joueur = argent_joueur
        self.max_quantite = argent_joueur // prix if prix != 0 else 100
        self.max_quantite = min(self.max_quantite, 1000)
        self.spin_box.setMaximum(self.max_quantite)

        # Mettre à jour le prix total
        self.spin_box.valueChanged.connect(self.mettre_a_jour_prix_total)

    def diminuer_quantite(self):
        """Diminue la quantité."""
        self.spin_box.setValue(self.spin_box.value() - 1)

    def augmenter_quantite(self):
        """Augmente la quantité."""
        self.spin_box.setValue(self.spin_box.value() + 1)

    def mettre_a_jour_prix_total(self, quantite):
        """Met à jour le prix total en fonction de la quantité."""
        prix_total = quantite * self.prix
        self.label_prix_total.setText(f"Prix total: {prix_total} pièces d'or")

    def get_quantite(self):
        """Retourne la quantité sélectionnée."""
        return self.spin_box.value()


class FenetreMagasin(QDialog):
    def __init__(self, inventaire, argent_joueur, parent=None):
        super(FenetreMagasin, self).__init__(parent)
        self.inventaire = inventaire
        self.argent_joueur = argent_joueur
        self.setWindowTitle("Magasin")
        self.resize(800, 500)

        # Dossier des images
        self.dossier_images = "assets"
        if not os.path.exists(self.dossier_images):
            os.makedirs(self.dossier_images)

        # Layout principal
        layout = QVBoxLayout(self)

        # Tableau avec 7 colonnes
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            [
                "Image",
                "Nom",
                "Prix",
                "Type",
                "Niveau",
                "Durabilité/Effet",
                "Acheter",
            ]
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ajout du tableau au layout
        layout.addWidget(self.table_widget)

        # Chargement des objets disponibles
        self.objets_dispo = self.charger_objets_dispo()
        for index, objet in enumerate(self.objets_dispo):
            if objet.get("nom").lower() == "gemmes":
                del self.objets_dispo[index]
                break
        self.mettre_a_jour_magasin()

    def charger_objets_dispo(self):
        """Charge les objets disponibles depuis le fichier JSON."""
        try:
            with open("objet_dispo.json", "r", encoding="utf-8") as fichier:
                objets = json.load(fichier)
            return objets
        except FileNotFoundError:
            QMessageBox.warning(
                self, "Erreur", "Le fichier objet_dispo.json est introuvable."
            )
            return []
        except json.JSONDecodeError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Le fichier objet_dispo.json n'est pas un fichier JSON valide.",
            )
            return []

    def mettre_a_jour_magasin(self):
        """Met à jour le tableau avec les objets disponibles dans le magasin."""
        self.table_widget.setRowCount(len(self.objets_dispo))

        for row, objet in enumerate(self.objets_dispo):
            # 1. Image
            image_label = QLabel()
            chemin_image = os.path.join(self.dossier_images, objet.get("image", ""))
            if os.path.exists(chemin_image):
                pixmap = QPixmap(chemin_image)
                if not pixmap.isNull():
                    image_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
                else:
                    image_label.setText("Erreur image")
            else:
                image_label.setText("Aucune image")
            self.table_widget.setCellWidget(row, 0, image_label)

            # 2. Nom
            self.table_widget.setItem(row, 1, QTableWidgetItem(objet.get("nom", "")))

            # 3. Prix
            self.table_widget.setItem(
                row, 2, QTableWidgetItem(str(objet.get("prix", 0)))
            )

            # 4. Type
            self.table_widget.setItem(
                row, 3, QTableWidgetItem(objet.get("type_objet", "de base"))
            )

            # 5. Enchantement
            self.table_widget.setItem(
                row, 4, QTableWidgetItem(str(objet.get("niv", "Aucun")))
            )

            # 6. Durabilité/Effet
            if objet.get("type", "").lower() == "potion":
                effet = objet.get("effet", "Aucun effet")
                self.table_widget.setItem(row, 5, QTableWidgetItem(str(effet)))
            else:
                durabilite = objet.get("durabilite", "Indestructible")
                self.table_widget.setItem(row, 5, QTableWidgetItem(str(durabilite)))

            # 7. Bouton Acheter
            bouton_acheter = QPushButton("Acheter")
            bouton_acheter.clicked.connect(lambda _, r=row: self.acheter_objet(r))
            self.table_widget.setCellWidget(row, 6, bouton_acheter)

        self.table_widget.resizeColumnsToContents()

    def acheter_objet(self, row):
        """Acheter l'objet sélectionné."""
        objet = self.objets_dispo[row]
        dialog = QuantiteDialog(objet["nom"], objet["prix"], self.argent_joueur, self)
        if dialog.exec():
            quantite = dialog.get_quantite()
            prix_total = quantite * objet["prix"]

            if prix_total > self.argent_joueur:
                QMessageBox.warning(
                    self, "Erreur", "Vous n'avez pas assez d'argent pour cet achat."
                )
                return

            # Mettre à jour l'argent du joueur
            self.argent_joueur -= prix_total
            safe_increment(self.inventaire, "argent", quant=-prix_total)
            # Ajouter l'objet à l'inventaire
            print(f"Argent restant: {self.argent_joueur}")
            if objet.get("type_objet") == "de base":
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet=objet.get("type_objet"),
                )
                print("ajouté")
            elif objet.get("type_objet").lower() == "potion":
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet=objet.get("type_objet"),
                    effet=objet.get("effet", ""),
                )
                print("ajouté")
            elif (
                objet.get("type_objet").lower() == "equipement"
                or objet.get("type_objet").lower() == "équipement"
            ):
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet="équipement",
                    durabilite=100,
                )
                print("ajouté")
            elif objet.get("type_objet").lower() == "armes":
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet="armes",
                    durabilite=100,
                    enchant=0,
                )
                print("ajouté")

            elif objet.get("type_objet").lower() == "livres":
                niveau = int(objet["nom"][-1])  # ✅ Extrait le niveau
                enchantements, category = ajouter_enchant(niveau)  # ✅ Récupère les enchantements

                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    category=category,
                    type_objet="livres",enchantements=enchantements
                    
                )
                print("ajouté")

            QMessageBox.information(
                self,
                "Achat",
                f"Vous avez acheté {quantite} {objet['nom']}(s) pour {prix_total} pièces d'or! Il vous reste {self.argent_joueur} pièces d'or.",
            )


def afficher_magasin(inventaire, argent_joueur, parent=None):
    dialog = FenetreMagasin(inventaire, argent_joueur, parent)
    dialog.exec()
