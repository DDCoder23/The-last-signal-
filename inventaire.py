import json
import os
import sys
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QInputDialog,
    QLineEdit,
    QPushButton,
    QDialog,
    QSpinBox,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
import asyncio
import threading

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
from horloge import réinitialiser

class FenetreInventaire(QDialog):
    

    def __init__(self, inventaire, parent=None):
        super(FenetreInventaire, self).__init__(parent)
        self.setWindowTitle("Inventaire du Joueur")
        self.resize(800, 500)
        self.prix_objets =self.charger_prix_objets()

        # Dossier des images
        self.dossier_images = "assets"
        if not os.path.exists(self.dossier_images):
            os.makedirs(self.dossier_images)

        # Layout principal
        layout = QVBoxLayout(self)

        # Tableau avec 9 colonnes (8 colonnes existantes + 1 pour le bouton Tout Vendre)
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)  # ← CHANGÉ DE 8 À 9
        self.table_widget.setHorizontalHeaderLabels(
            [
                "Image",
                "Nom",
                "Quantite",
                "Type",
                "Enchantement",
                "Durabilite/Effet",
                "Utiliser",
                "Vendre",
                "Tout Vendre",  # ← NOUVELLE COLONNE
            ]
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ajout du tableau au layout
        layout.addWidget(self.table_widget)

        # Barre de recherche
        self.barre_recherche = QLineEdit()
        self.barre_recherche.setPlaceholderText(
            "Rechercher un objet (nom, type, effet...)"
        )
        layout.addWidget(self.barre_recherche)

        self.bouton_rechercher = QPushButton("Rechercher")
        self.bouton_rechercher.clicked.connect(self.effectuer_recherche)
        layout.addWidget(self.bouton_rechercher)

        # Chargement initial
        self.inventaire = inventaire
        self.inventaire_filtre = self.inventaire
        self.mettre_a_jour_inventaire()

    def mettre_a_jour_inventaire(self):
        
        """Met à jour le tableau avec les données actuelles de l'inventaire."""
        self.table_widget.setRowCount(len(self.inventaire_filtre))

        for row, (nom, objet) in enumerate(self.inventaire_filtre.items()):
            # 1. Image
            image_label = QLabel()
            chemin_image = os.path.join(
                self.dossier_images, getattr(objet, "image", "")
            )
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
            self.table_widget.setItem(
                row, 1, QTableWidgetItem(getattr(objet, "nom", ""))
            )

            # 3. Quantité
            quantite = getattr(objet, "quantite", 0)
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(quantite)))

            # 4. Type
            type_objet = getattr(objet, "type_objet", "de base")
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(type_objet)))

            # 5. Enchantement
            enchantement = getattr(objet, "enchant", "Aucun")
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(enchantement)))

            # 6. Durabilité/Effet
            if (
                hasattr(objet, "type_objet")
                and getattr(objet, "type_objet", "").lower() == "potion"
            ):
                effet = getattr(objet, "effet", "Aucun effet")
                self.table_widget.setItem(row, 5, QTableWidgetItem(str(effet)))
            else:
                durabilite = getattr(objet, "durabilite", "Indestructible")
                self.table_widget.setItem(row, 5, QTableWidgetItem(str(durabilite)))

            # 7. Bouton Utiliser
            bouton_utiliser = QPushButton("Utiliser")
            bouton_utiliser.clicked.connect(
                lambda _, r=row, n=nom: self.utiliser_objet(r, n)
            )
            self.table_widget.setCellWidget(row, 6, bouton_utiliser)

            # 8. Bouton Vendre
            bouton_vendre = QPushButton("Vendre")
            bouton_vendre.clicked.connect(
                lambda _, r=row, n=nom: self.vendre_objet(r, n)
            )
            self.table_widget.setCellWidget(row, 7, bouton_vendre)

            bouton_tout_vendre = QPushButton("Tout Vendre")
            bouton_tout_vendre.setStyleSheet("background-color: #ff6b6b; color: white; font-weight: bold;")
            bouton_tout_vendre.clicked.connect(
                    lambda _, r=row, n=nom: self.vendre_tous_meme_nom(r, n)
                )
            self.table_widget.setCellWidget(row, 8, bouton_tout_vendre)

            self.table_widget.resizeColumnsToContents()

    def vendre_objet(self, row, nom):
        """Vendre l'objet sélectionné."""
        noms = list(self.inventaire_filtre.keys())
        if row < 0 or row >= len(noms):
            return

        objet = self.inventaire_filtre[nom]
        if nom.lower() == "argent":
            QMessageBox.warning(
                self, "Erreur", "Vous ne pouvez pas vendre de l'argent."
            )
            return

        # Demander la quantité à vendre
        quantite, ok = QInputDialog.getInt(
            self,
            "Vendre un objet",
            f"Quantité de {objet.nom} à vendre (max: {objet.quantite}):",
            1,
            1,
            objet.quantite,
        )

        if ok:
            if (
                objet.type_objet.lower() == "potion"
                or objet.type_objet.lower() == "de base"
            ) and not objet == "gemmes":
                prix_unitaire = (
                    self.prix_objets.get(objet.nom.replace("_", " "), 10) * 0.75
                )
                prix_unitaire = round(prix_unitaire)
            elif (
                objet.type_objet.lower() == "equipement"
                or objet.type_objet.lower() == "armes"
            ):
                prix_unitaire = (
                    self.prix_objets.get(objet.nom_base.replace("_", " "), 10) * 0.75
                    + objet.enchant * 1000
                )
                prix_unitaire = round(prix_unitaire)
            prix_total = quantite * prix_unitaire

            # Mettre à jour la quantité de l'objet
            objet.retirer(quantite)

            # Si la quantité est à zéro, retirer l'objet de l'inventaire
            if objet.quantite <= 0:
                del self.inventaire_filtre[nom]

            QMessageBox.information(
                self,
                "Vente",
                f"Vous avez vendu {quantite} {objet.nom}(s) pour {prix_total} pièces d'or!",
            )
            safe_increment(self.inventaire, "argent", quant=prix_total)
            # Mettre à jour l'affichage de l'inventaire
            self.mettre_a_jour_inventaire()

    
    def vendre_tous_meme_nom(self, row, nom):
        
        objet = self.inventaire_filtre[nom]
        objets_similaires = []
        prix_total = 0
        quantite_totale = 0
        if nom.lower() == "argent":
            QMessageBox.warning(
                self, "Erreur", "Vous ne pouvez pas vendre de l'argent."
            )
            return



        # Trouver tous les objets avec le même nom_base
        nom_base = getattr(objet, "nom_base", nom)
        for nom_key, obj in list(self.inventaire_filtre.items()):
            obj_nom_base = getattr(obj, "nom_base", nom_key)
            if obj_nom_base == nom_base:
                objets_similaires.append((nom_key, obj))

        # Calculer le prix et quantité totale
        for nom_key, obj in objets_similaires:
            quantite_totale += obj.quantite
            # Calculer prix unitaire
            if (obj.type_objet.lower() == "potion" or obj.type_objet.lower() == "de base") and nom_key != "gemmes":
                prix_unitaire = self.prix_objets.get(obj.nom.replace("_", " "), 10) * 0.75
            elif obj.type_objet.lower() in ["equipement", "armes"]:
                prix_unitaire = self.prix_objets.get(obj.nom_base.replace("_", " "), 10) * 0.75 + getattr(obj, "enchant", 0) * 1000
            else:
                prix_unitaire = 10
            prix_total += obj.quantite * round(prix_unitaire)

        # Confirmation
        confirm = QMessageBox.question(
            self,
            "Confirmation de vente",
            f"Vendre tous les '{nom_base}' ({len(objets_similaires)} ligne(s), {quantite_totale} objet(s)) pour {prix_total} pièces d'or ?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            # Vendre tous les objets
            for nom_key, obj in objets_similaires:
                obj.retirer(obj.quantite)
                if obj.quantite <= 0:
                    del self.inventaire_filtre[nom_key]
                    if nom_key in self.inventaire:
                        del self.inventaire[nom_key]

            safe_increment(self.inventaire, "argent", quant=prix_total)
            QMessageBox.information(
                self,
                "Vente réussie",
                f"{quantite_totale} objet(s) vendu(s) pour {prix_total} pièces d'or !",
            )
            self.mettre_a_jour_inventaire()

    def utiliser_objet(self, row, nom):
        """Utilise l'objet sélectionné (ex : boire une potion)."""
        noms = list(self.inventaire_filtre.keys())
        if row < 0 or row >= len(noms):
            return

        objet = self.inventaire_filtre[nom]
        if (
            hasattr(objet, "type_objet")
            and getattr(objet, "type_objet", "").lower() == "potion"
        ):
            objet.retirer(1)
            QMessageBox.information(
                self,
                "Utilisation",
                f"Vous avez utilisé {objet.nom} ! Effet : {getattr(objet, 'effet', 'Aucun')}",
            )
            if objet.quantite <= 0:
                del self.inventaire_filtre[nom]
        else:
            QMessageBox.warning(
                self, "Erreur", "Seules les potions peuvent être utilisées directement."
            )

        self.mettre_a_jour_inventaire()

    def charger_prix_objets(self):

        try:
            with open("objet_dispo.json", "r", encoding="utf-8") as fichier:
                objets = json.load(fichier)
            prix_objets = {objet["nom"]: objet["prix"] for objet in objets}
            return prix_objets
        except FileNotFoundError:
            QMessageBox.warning(
                self, "Erreur", "Le fichier objet_dispo.json est introuvable."
            )
            return {}
        except json.JSONDecodeError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Le fichier objet_dispo.json n'est pas un fichier JSON valide.",
            )
            return {}

    def effectuer_recherche(self):
        """Effectue la recherche en fonction du texte saisi."""
        texte = self.barre_recherche.text()
        self.filtrer_inventaire(texte)

    def filtrer_inventaire(self, texte):
        if not texte:
            self.inventaire_filtre = self.inventaire.copy()
        else:
            texte = texte.lower()
            self.inventaire_filtre = {
                nom: objet
                for nom, objet in self.inventaire.items()
                if (
                    texte in getattr(objet, "nom", "").lower()
                    or texte in getattr(objet, "type_objet", "").lower()
                    or texte in str(getattr(objet, "effet", "")).lower()
                    or texte in str(getattr(objet, "enchant", "")).lower()
                )
            }
        self.mettre_a_jour_inventaire()

        
def afficher_inventaire(inventaire, parent=None):
    dialog = FenetreInventaire(inventaire, parent)
    dialog.exec()  # Utilisez exec() pour une boîte de dialogue modale
    # Ou utilisez dialog.show() pour une fenêtre non-modale


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
    ):
        super().__init__(nom, image, quantite, type_objet)
        self.durabilite = durabilite
        self.enchant = enchant
        self.bonus = bonus

    def __repr__(self):

        return f"{self.quantite:,} [Enchant +{self.enchant}| bonus :{self.bonus} ]"

    def enchanter(self, niv):
        self.enchant += niv
        self.durabilite += niv * 10 + self.enchant * 5
        self.bonus += niv * 5 + self.enchant * 5


class Potion(Objet):
    def __init__(self, nom, image, quantite=1, type_objet="potion", **kwargs):
        super().__init__(nom, image, quantite, type_objet)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def appliquer_effet(self):
        pass


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


