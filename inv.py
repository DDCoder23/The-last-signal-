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
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from inventaire import Objet,safe_increment

import json
import os
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

    def __init__(self, inventaire, joueur, parent=None):
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

        # Tableau avec 9 colonnes (8 colonnes existantes + 1 pour le bouton Tout Vendre)
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(10)  # ← CHANGÉ DE 9 À 10
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
                "Tout Vendre",
                "Convertir",  # ← NOUVELLE COLONNE
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
            # 9. Bouton Convertir (UNIQUEMENT POUR LES LIVRES)
            if getattr(objet, "type_objet", "").lower() == "livres":
                bouton_convertir = QPushButton("Convertir")
                bouton_convertir.clicked.connect(
                    lambda _, r=row, n=nom: self.demander_quantite_conversion(r, n)
                )
                self.table_widget.setCellWidget(row, 9, bouton_convertir)  # ← COLONNE 9
            else:
                self.table_widget.setCellWidget(row, 9, QLabel(""))  # Cellule vide

    def demander_quantite_conversion(self, row, nom):
        """Demander la quantité de livres à convertir."""
        objet = self.inventaire_filtre[nom]
        quantite_max = getattr(objet, "quantite", 0)

        if quantite_max <= 0:
            QMessageBox.warning(self, "Erreur", "Aucun livre disponible à convertir.")
            return

        # Demander la quantité à convertir
        quantite, ok = QInputDialog.getInt(
            self,
            "Convertir des livres",
            f"Quantité de {nom} à convertir (max: {quantite_max}):",
            1,  # Valeur par défaut
            1,  # Minimum
            quantite_max,  # Maximum
        )

        if ok:
            self.convertir_livre(row, nom, quantite)

    def convertir_livre(self, row, nom, quantite):
        """Convertir une quantité de livres en un niveau supérieur."""
        from table_de_conversion import convertir_livres

        # Vérifier si c'est un livre enchanté
        if "livre enchant" not in nom:
            QMessageBox.warning(self, "Erreur", "Seuls les livres enchantés peuvent être convertis.")
            return

        # Extraire le niveau actuel
        niveau_actuel = int(nom.split("niv ")[1]) if "niv" in nom else 1
        niveau_cible = niveau_actuel + 1

        if niveau_cible > 6:  # Niveau max = 6
            QMessageBox.warning(self, "Erreur", "Niveau maximal atteint (6).")
            return

        # Appeler la fonction de conversion
        stats = convertir_livres(niveau_cible, quantite, self.joueur)

        # Mettre à jour l'affichage
        self.mettre_a_jour_inventaire()
        QMessageBox.information(
            self,
            "Succès",
            f"{quantite} {nom}(s) converti(s) en niveau {niveau_cible} !\nStatistiques: {stats}"
        )

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
                    or objet.type_objet.lower() == "de base" or objet.type_objet.lower() == "livres"
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
                prix_unitaire = self.prix_objets.get(obj.nom_base.replace("_", " "), 10) * 0.75 + getattr(obj,
                                                                                                          "enchant",
                                                                                                          0) * 1000
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


def afficher_inventaire(inventaire, joueur, parent=None):
    dialog = FenetreInventaire(inventaire, joueur, parent)
    dialog.exec()  # Utilisez exec() pour une boîte de dialogue modale
    # Ou utilisez dialog.show() pour une fenêtre non-modale