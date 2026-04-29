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
dict_enchant={1: {"épée":("Aura de feu I", "Durability I"), "armes à feu":("Rapidity I")}}

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
        objets_enchantes.sort(key=lambda x: x[1].enchant, reverse=True)

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
        self.image = image
        self.quantite = quantite
        self.type_objet = type_objet
        self.image = str(image) if image is not None else ""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def attribut_superieur_a_un(self, nom_attribut: str) -> bool:
        return hasattr(self, nom_attribut) and getattr(self, nom_attribut) > 0

    def nom_affiche(self):
        base = self.nom_base
        if self.attribut_superieur_a_un("enchant"):
            return f"{base} enchanté niv {self.enchant}"
        return base

    @property
    def nom(self):
        return self.nom_affiche()

    def ajouter(self, qte):
        self.quantite += qte

    def retirer(self, qte):
        self.quantite = max(0, self.quantite - qte)

    def __repr__(self):
        return f"{self.quantite:,} "


class equipement(Objet):
    def __init__(
        self, nom, image, quantite=1, type_objet="equipement", enchant=0, bonus=5
    ):
        super().__init__(nom, image, quantite, type_objet)
        self.enchant = enchant
        self.bonus = bonus

    def __repr__(self):

        return f"{self.quantite:,} [Enchant +{self.enchant}| bonus :{self.bonus}  ]"

    def enchanter(self, niv):
        self.enchant += niv
        self.bonus += niv * 5 + self.enchant * 5


class Armes(equipement):
    def __init__(
        self,
        nom,
        image,
        quantite=1,
        type_objet="Armes",
        enchant=0,
        durabilite=100,
        bonus=5,
        enchantements=()
    ):
        super().__init__(nom, image, quantite, type_objet)
        self.durabilite = durabilite
        self.enchant = enchant
        self.bonus = bonus
        self.enchantements=enchantements

    def __repr__(self):

        return f"{self.quantite:,} [Enchant +{self.enchant}| bonus :{self.bonus} | dura : {self.durabilite}]"

    def enchanter(self, niv,enc):
        self.enchant += niv
        self.durabilite += niv * 10 + self.enchant * 5
        self.bonus += niv * 5 + self.enchant * 5
        if niv>0:
            for  en in self.enchantements:
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
    def __init__(self, nom, image, quantite=1, type_objet="livres", **kwargs):
        super().__init__(nom, image, quantite, type_objet)
        self.enchant1=kwargs.get("enchant1",None)
        self.enchant2=kwargs.get("enchant2",None)
        self.enchant3=kwargs.get("enchant3",None)
    def __repr__(self):
        if self.enchant3:
            return f"{self.quantite:,} [{self.enchant1}|{self.enchant2}| {self.enchant3}]"

        elif not self.enchant3 and self.enchant2:
            return f"{self.quantite:,} [{self.enchant1}|{self.enchant2}]"

        elif not self.enchant3 and not self.enchant2:
            return f"{self.quantite:,} [{self.enchant1}]"



        

def nettoyer_stuff_zero(inventaire):
    a_supprimer = []

    async def _nettoyer(invnetaire):

        for nom, obj in inventaire.items():
            if isinstance(obj, Objet):
                if obj.quantite <= 0:
                    a_supprimer.append(nom)

        for nom in a_supprimer:
            del inventaire[nom]

    asyncio.run(_nettoyer(inventaire))


def safe_increment(
    inventaire, nom, image=None, quant=1, type_objet="base", ajouter=True, **kwargs
):
    image = (
        f"{nom}.png" if os.path.exists(os.path.join("asset", f"{nom}.png")) else None
    )

    trier(inventaire)
    if type_objet == "armes":
        for _ in range(quant):
            cle = nom
            i = 1
            while cle in inventaire:
                i += 1
                cle = f"{nom}n°{i}"

            inventaire[cle] = Armes(
                nom=nom,
                image=image,
                quantite=1,
                enchant=kwargs.get("enchant", 0),
                durabilite=kwargs.get("durabilite", 100),
            )
        return
    if type_objet == "équipement":
        for _ in range(quant):
            cle = nom
            i = 1
            while cle in inventaire:
                i += 1
                cle = f"{nom}n°{i}"

            inventaire[cle] = equipement(
                nom=nom,
                image=image,
                quantite=1,
                enchant=kwargs.get("enchant", 0),
            )
            return
    if type_objet == "livres":
        for _ in range(quant):
            for key in inventaire:
                if isinstance(nom,Livres):
                    if (key.enchant1==kwargs.get("enchant1", None) or key.enchant2==kwargs.get("enchant2", None) or key.enchant3==kwargs.get("enchant3", None)):
                        globals()[nom] = inventaire[nom]
                        obj = inventaire[nom]
                        if isinstance(obj, Objet):
                            obj.ajouter(quant)
                        nettoyer_stuff_zero(inventaire)
                        return
                        

                

            inventaire[nom] = Livres(
                nom=nom,
                image=image,
                quantite=1,
                enchant1=kwargs.get("enchant1", None),
enchant2=kwargs.get("enchant2", None),
enchant3=kwargs.get("enchant3", None),

            )
            nettoyer_stuff_zero(inventaire)
            return
  

    # 1️⃣ L’objet existe déjà
    if nom in inventaire.keys():
        globals()[nom] = inventaire[nom]
        obj = inventaire[nom]
        if isinstance(obj, Objet):

            if ajouter == True:
                obj.ajouter(quant)

                nettoyer_stuff_zero(inventaire)
                trier(inventaire)
                return

            elif ajouter == False:
                obj.retirer(quant)

                nettoyer_stuff_zero(inventaire)
                trier(inventaire)
                return

        else:
            if ajouter == True:
                inventaire[nom] += quant
                nettoyer_stuff_zero(inventaire)
                trier(inventaire)
            elif ajouter == False:
                inventaire[nom] += quant
                nettoyer_stuff_zero(inventaire)
                trier(inventaire)

    if type_objet == "armes":
        inventaire[nom] = Armes(
            nom,
            image,
            quant,
            type_objet=type_objet,
            enchant=kwargs.get("enchant", 0),
            durabilite=kwargs.get("durabilite", 100),
        )

    elif type_objet == "équipement":
        inventaire[nom] = equipement(
            nom, image, quant, type_objet=type_objet, enchant=kwargs.get("enchant", 0)
        )
    elif type_objet == "potion":
        inventaire[nom] = Potion(
            nom, image, quant, type_objet=type_objet, effet=kwargs.get("effet", None)
        )

    elif type_objet == "livres":
        inventaire[nom] = Livre(nom, image, quant,type_objet=type_objet,enchant1=kwargs.get("enchant1", None), enchant2=kwargs.get("enchant2", None), enchant3=kwargs.get("enchant3", None) )

    elif type_objet == "de base" or type_objet == "base":
        inventaire[nom] = Objet(nom, image, quant)
    nettoyer_stuff_zero(inventaire)
    trier(inventaire)


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
                "Enchantement",
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
                row, 3, QTableWidgetItem(objet.get("type", "de base"))
            )

            # 5. Enchantement
            self.table_widget.setItem(
                row, 4, QTableWidgetItem(str(objet.get("enchant", "Aucun")))
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
            if objet.get("type") == "de base":
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet=objet.get("type"),
                )
                print("ajouté")
            elif objet.get("type").lower() == "potion":
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet=objet.get("type"),
                    effet=objet.get("effet", ""),
                )
                print("ajouté")
            elif (
                objet.get("type").lower() == "equipement"
                or objet.get("type").lower() == "équipement"
            ):
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet="équipement",
                    durabilite=100,
                )
                print("ajouté")
            elif objet.get("type").lower() == "armes":
                safe_increment(
                    self.inventaire,
                    objet["nom"],
                    quant=quantite,
                    type_objet="armes",
                    durabilite=100,
                    enchant=0,
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


