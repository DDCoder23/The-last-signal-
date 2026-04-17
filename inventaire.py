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


class FenetreInventaire(QDialog):
    def __init__(self, inventaire, parent=None):
        super(FenetreInventaire, self).__init__(parent)
        self.setWindowTitle("Inventaire du Joueur")
        self.resize(800, 500)
        self.prix_objets = self.charger_prix_objets()

        # Dossier des images
        self.dossier_images = "assets"
        if not os.path.exists(self.dossier_images):
            os.makedirs(self.dossier_images)

        # Layout principal
        layout = QVBoxLayout(self)

        # Tableau avec 8 colonnes (7 colonnes existantes + 1 pour le bouton Vendre)
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
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


class FenetreBanque(QDialog):
    FICHIER_SAUVEGARDE_BANQUE = "banque_save.json"

    def __init__(self, joueur, horloge_jeu, parent=None):
        super(FenetreBanque, self).__init__(parent)
        self.joueur = joueur
        self.horloge_jeu = horloge_jeu
        self.setWindowTitle("Banque")
        self.resize(400, 200)

        # Initialisation des attributs de la banque
        self.dettes = 0
        self.investissements = {}

        # Charger l'état de la banque si nécessaire
        self.charger_etat_banque()

        layout = QVBoxLayout(self)

        # Boutons pour emprunter et investir
        self.bouton_emprunter = QPushButton("Emprunter de l'argent")
        self.bouton_emprunter.clicked.connect(self.emprunter)

        self.bouton_investir = QPushButton("Investir")
        self.bouton_investir.clicked.connect(self.investir)
        self.bouton_rembourser = QPushButton("Rembourser les dettes")
        self.bouton_rembourser.clicked.connect(self.rembourser)

        layout.addWidget(self.bouton_rembourser)

        layout.addWidget(self.bouton_emprunter)
        layout.addWidget(self.bouton_investir)

        # Enregistrer l'événement de nouveau mois pour gérer les investissements
        self.horloge_jeu.enregistrer_evenement(
            "nouveau_mois", self.verifier_investissements
        )

    def rembourser(self):
        """Permet au joueur de rembourser tout ou partie de ses dettes."""
        if self.dettes <= 0:
            QMessageBox.information(
                self, "Remboursement", "Vous n'avez pas de dettes à rembourser."
            )
            return

        argent_disponible = qtes("argent", self.joueur)
        montant_max = min(argent_disponible, self.dettes)

        montant, ok = QInputDialog.getInt(
            self,
            "Remboursement",
            f"Montant à rembourser (max {montant_max:.2f}):",
            100,
            1,
            montant_max,
            100,
        )
        if ok:
            safe_increment(self.joueur.stuff, "argent", quant=-montant)
            self.dettes -= montant
            self.sauvegarder_etat_banque(s)
            QMessageBox.information(
                self,
                "Remboursement",
                f"Vous avez remboursé {montant:.2f} pièces d'or. Dettes restantes: {self.dettes:.2f}",
            )

    def emprunter(self):
        """Demande la quantité à emprunter et met à jour l'inventaire et les dettes."""
        montant, ok = QInputDialog.getInt(
            self, "Emprunt", "Montant à emprunter:", 100, 1, 1000000, 100
        )
        if ok:
            safe_increment(self.joueur.stuff, "argent", quant=montant)
            self.dettes += montant * 1.10
            self.dettes = round(self.dettes)
            self.sauvegarder_etat_banque(self.joueur)
            QMessageBox.information(
                self,
                "Emprunt",
                f"Vous avez emprunté {montant} pièces d'or. Dettes totales: {self.dettes}",
            )

    def investir(self):
        """Demande le capital et la durée pour investir, calcule l'intérêt composé."""
        argent_disponible = qtes("argent", self.joueur)

        if not self.investissements:
            # Premier investissement
            capital, ok1 = QInputDialog.getInt(
                self,
                "Investissement",
                "Capital à investir:",
                100,
                1,
                argent_disponible,
                1,
            )
            if not ok1:
                return

            if capital > argent_disponible:
                QMessageBox.warning(
                    self,
                    "Investissement",
                    "Vous n'avez pas assez d'argent pour cet investissement.",
                )
                return

            annees, ok2 = QInputDialog.getInt(
                self, "Investissement", "Nombre d'années:", 1, 1, 50, 1
            )
            if not ok2:
                return

            taux_mensuel = 0.05 / 12
            mois = annees * 12
            valeur_future = capital * (1 + taux_mensuel) ** mois
            self.investissements = {
                "capital": capital,
                "valeur_future": valeur_future,
                "mois_total": mois,
                "date_fin": self.horloge_jeu.annees * 12 + self.horloge_jeu.mois + mois,
            }
            safe_increment(self.joueur.stuff, "argent", quant=-capital)
            self.sauvegarder_etat_banque()
            QMessageBox.information(
                self,
                "Investissement",
                f"Investissement de {capital} pièces d'or pour {annees} ans. Valeur future: {valeur_future:.2f}",
            )
        else:
            # Ajout de capital à un investissement existant
            capital_additionnel, ok1 = QInputDialog.getInt(
                self,
                "Ajout d'investissement",
                "Capital supplémentaire à investir:",
                100,
                1,
                argent_disponible,
                1,
            )
            if not ok1:
                return

            if capital_additionnel > argent_disponible:
                QMessageBox.warning(
                    self,
                    "Investissement",
                    "Vous n'avez pas assez d'argent pour ajouter à cet investissement.",
                )
                return

            # Mettre à jour le capital et recalculer la valeur future
            self.investissements["capital"] += capital_additionnel
            taux_mensuel = 0.05 / 12
            mois_restants = self.investissements["date_fin"] - (
                self.horloge_jeu.annees * 12 + self.horloge_jeu.mois
            )
            valeur_future = (
                self.investissements["capital"]
                * (1 + taux_mensuel) ** self.investissements["mois_total"]
            )
            self.investissements["valeur_future"] = valeur_future
            safe_increment(self.joueur.stuff, "argent", quant=-capital_additionnel)
            self.sauvegarder_etat_banque()
            QMessageBox.information(
                self,
                "Investissement",
                f"Ajout de {capital_additionnel} pièces d'or à votre investissement. Nouveau capital: {self.investissements['capital']}. Valeur future: {valeur_future:.2f}",
            )

    def verifier_investissements(self):
        """Vérifie si un investissement est terminé et crédite le joueur."""
        if self.investissements:
            mois_actuel = self.horloge_jeu.annees * 12 + self.horloge_jeu.mois
            if mois_actuel >= self.investissements["date_fin"]:
                safe_increment(
                    self.joueur.stuff,
                    "argent",
                    quant=round(int(self.investissements["valeur_future"])),
                )
                QMessageBox.information(
                    self,
                    "Investissement",
                    f"Votre investissement est arrivé à échéance. {self.investissements['valeur_future']:.2f} pièces d'or ont été ajoutées à votre inventaire.",
                )
                self.investissements = {}
                self.sauvegarder_etat_banque()

    def sauvegarder_etat_banque(self):
        """Sauvegarde l'état actuel de la banque pour ce joueur."""
        data = {}
        if os.path.exists(FenetreBanque.FICHIER_SAUVEGARDE_BANQUE):
            with open(
                FenetreBanque.FICHIER_SAUVEGARDE_BANQUE, "r", encoding="utf-8"
            ) as fichier_json:
                try:
                    data = json.load(fichier_json)
                except json.JSONDecodeError:
                    data = {}

        data[self.joueur.nom] = {
            "dettes": self.dettes,
            "investissements": self.investissements,
        }

        with open(
            FenetreBanque.FICHIER_SAUVEGARDE_BANQUE, "w", encoding="utf-8"
        ) as fichier:
            json.dump(data, fichier, indent=4)

    def afficher_banque(self, **kwargs):
        with open("save.txt", "a", encoding="utf-8") as fichier:
            fichier.write("\ncontinuer")

        self.charger_etat_banque()
        message = f"Dettes: {self.dettes}\n"
        if self.investissements:
            message += (
                f"Investissements: Capital={self.investissements['capital']}, "
                f"Valeur future={self.investissements['valeur_future']:.2f}, "
                f"Mois total={self.investissements['mois_total']},"
                f"échéance={self.investissements['date_fin']}"
            )
        else:
            message += "Aucun investissement en cours."
        if kwargs.get("b", True) == True:
            QMessageBox.information(self, "État de la Banque", message)

    def charger_etat_banque(self):
        """Charge l'état de la banque depuis un fichier JSON si la dernière ligne de save.txt est 'reprise du jeu'."""
        if os.path.exists("save.txt"):
            with open("save.txt", "r", encoding="utf-8") as fichier:
                lignes = fichier.readlines()
                if lignes and lignes[-1].strip() == "reprise du jeu" or "continuer":
                    if os.path.exists(FenetreBanque.FICHIER_SAUVEGARDE_BANQUE):
                        try:
                            with open(
                                FenetreBanque.FICHIER_SAUVEGARDE_BANQUE,
                                "r",
                                encoding="utf-8",
                            ) as fichier_json:
                                data = json.load(fichier_json)
                                player_data = data.get(f"{self.joueur.nom}", {})

                                # Charger les dettes
                                self.dettes = player_data.get("dettes", 0)

                                # Charger les investissements
                                self.investissements = player_data.get(
                                    "investissements", {}
                                )
                        except json.JSONDecodeError:
                            raise json.JSONDecodeError
            with open("save.txt", "a", encoding="utf-8") as fichier:
                fichier.write("\ncontinuer")


def afficher_banque(joueur, horloge_jeu, parent=None, **kwargs):
    b = kwargs.get("b", True)
    dialog = FenetreBanque(joueur, horloge_jeu, parent)
    dialog.afficher_banque(b=b)

    if b == False:
        dialog.hide()
    else:
        dialog.exec()
