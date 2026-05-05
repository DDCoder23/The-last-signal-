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
from index_manager import mettre_a_jour_index,rechercher_dans_index
from inventaire import Objet,safe_increment,Potion,Livres, livres_par_enchantements
import math
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
from PySide6.QtCore import Qt, QTimer
from index_manager import mettre_a_jour_index, rechercher_dans_index
from inventaire import Objet, safe_increment, Potion, Livres
import math
import json
import os

def qtes(nom, joueur):
    if nom not in joueur.stuff:
        return 0
    obj = joueur.stuff[nom]
    if isinstance(obj, Objet):
        return obj.quantite
    elif isinstance(obj, (int, float)):
        return obj
    else:
        print(f" Type inattendu pour {nom}: {type(obj)}")
        return 0

class FenetreInventaire(QDialog):
    def __init__(self, inventaire, joueur, parent=None):
        super(FenetreInventaire, self).__init__(parent)
        self.setWindowTitle("Inventaire du Joueur")
        self.resize(800, 500)
        self.prix_objets = self.charger_prix_objets()
        self.joueur = joueur
        self.inventaire = inventaire
        self.inventaire_filtre = self.inventaire.copy()
        mettre_a_jour_index(self.inventaire)

        # Dossier des images
        self.dossier_images = "assets"
        if not os.path.exists(self.dossier_images):
            os.makedirs(self.dossier_images)

        # Layout principal
        layout = QVBoxLayout(self)

        # Tableau avec 10 colonnes
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(10)
        self.table_widget.setHorizontalHeaderLabels(
            [
                "Image",
                "Nom",
                "Quantite",
                "Type",
                "Niveau",
                "Autres infos",
                "Utiliser",
                "Vendre",
                "Tout Vendre",
                "Convertir",
            ]
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table_widget)

        # Barre de recherche
        self.barre_recherche = QLineEdit()
        self.barre_recherche.setPlaceholderText(
            "Rechercher un objet (nom, type, effet...)"
        )
        layout.addWidget(self.barre_recherche)

        # Timer pour débounce (attendre 300ms avant de chercher)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.effectuer_recherche_optimisee)
        self.barre_recherche.textChanged.connect(self.on_search_text_changed)

        self.bouton_rechercher = QPushButton("Rechercher")
        self.bouton_rechercher.clicked.connect(self.effectuer_recherche_optimisee)
        layout.addWidget(self.bouton_rechercher)

        # Cache pour les images et widgets
        self.widget_cache = {}

        # Chargement initial
        self.mettre_a_jour_inventaire_complet()

    def on_search_text_changed(self):
        """Redémarre le timer à chaque changement de texte"""
        self.search_timer.stop()
        self.search_timer.start(300)  # ⏱️ 300ms de délai

    def effectuer_recherche_optimisee(self):
        """Recherche ultra-rapide avec index"""
        texte = self.barre_recherche.text().strip()
        
        if not texte:
            self.inventaire_filtre = self.inventaire.copy()
        else:
            cles_trouvees = rechercher_dans_index(texte, self.inventaire)
            self.inventaire_filtre = {
                cle: self.inventaire[cle]
                for cle in cles_trouvees
            }
        
        self.mettre_a_jour_inventaire_rapide()

    def mettre_a_jour_inventaire_complet(self):
        """Reconstruction complète du tableau (au démarrage uniquement)"""
        mettre_a_jour_index(self.inventaire)
        self.widget_cache = {}
        self.table_widget.setRowCount(len(self.inventaire_filtre))

        for row, (nom, objet) in enumerate(self.inventaire_filtre.items()):
            self._remplir_ligne(row, nom, objet)

        self.table_widget.resizeColumnsToContents()

    def mettre_a_jour_inventaire_rapide(self):
        """Mise à jour rapide du tableau filtré (rechargement uniquement)"""
        self.table_widget.setRowCount(len(self.inventaire_filtre))

        for row, (nom, objet) in enumerate(self.inventaire_filtre.items()):
            self._remplir_ligne(row, nom, objet)

        self.table_widget.resizeColumnsToContents()

    def _remplir_ligne(self, row, nom, objet):
        """Remplit une ligne du tableau"""
        # 1. Image
        image_label = QLabel()

        image_label.setStyleSheet("background-color: lightgray;")  # Fond pour voir le label
        chemin_image = os.path.join(self.dossier_images, getattr(objet, "image", ""))
        chemin_image = os.path.abspath(chemin_image)
        
        if os.path.exists(chemin_image):
            pixmap = QPixmap(chemin_image)
            if not pixmap.isNull():
                image_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                
            else:
                image_label.setText("Erreur image")
        else:
            image_label.setText("Aucune image")
        self.table_widget.setCellWidget(row, 0, image_label)

        # 2. Nom
        self.table_widget.setItem(row, 1, QTableWidgetItem(getattr(objet, "nom", "")))

        # 3. Quantité
        quantite = getattr(objet, "quantite", 0)
        self.table_widget.setItem(row, 2, QTableWidgetItem(str(quantite)))

        # 4. Type
        type_objet = getattr(objet, "type_objet", "de base")
        self.table_widget.setItem(row, 3, QTableWidgetItem(str(type_objet)))

        # 5. Niveau
        niv = getattr(objet, "niv", "Aucun")
        if isinstance(niv, str) and niv.isdigit():
            niv = int(niv)
        self.table_widget.setItem(row, 4, QTableWidgetItem(str(niv)))

        # 6. Autres infos
        if hasattr(objet, "type_objet") and getattr(objet, "type_objet", "").lower() == "potion":
            effet = getattr(objet, "effet", "Aucun effet")
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(effet)))
        elif hasattr(objet, "type_objet") and getattr(objet, "type_objet", "").lower() == "livres":
            enchants = getattr(objet, "enchantements", [])
            enchant_str = ", ".join(enchants) if enchants else "Aucun"
            self.table_widget.setItem(row, 5, QTableWidgetItem(enchant_str))
        else:
            durabilite = getattr(objet, "durabilite", "Indestructible")
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(durabilite)))

        # 7. Bouton Boire (potions uniquement)
        if isinstance(objet, Potion):
            bouton_boire = QPushButton("Boire")
            bouton_boire.clicked.connect(lambda _, r=row, n=nom: self.boire(r, n))
            self.table_widget.setCellWidget(row, 6, bouton_boire)
        else:
            self.table_widget.setCellWidget(row, 6, QLabel(""))

        # 8. Bouton Vendre
        bouton_vendre = QPushButton("Vendre")
        bouton_vendre.clicked.connect(lambda _, r=row, n=nom: self.vendre_objet(r, n))
        self.table_widget.setCellWidget(row, 7, bouton_vendre)

        # 9. Bouton Tout Vendre
        bouton_tout_vendre = QPushButton("Tout Vendre")
        bouton_tout_vendre.setStyleSheet("background-color: #ff6b6b; color: white; font-weight: bold;")
        bouton_tout_vendre.clicked.connect(
    lambda _, obj=objet: self.vendre_tous_meme_nom(obj)
)
        self.table_widget.setCellWidget(row, 8, bouton_tout_vendre)

        # 10. Bouton Convertir (livres uniquement)
        if isinstance(objet, Livres):
            niv = getattr(objet, "niv", 0)
            if isinstance(niv, str) and niv.isdigit():
                niv = int(niv)
            if int(niv) < 6:
                bouton_convertir = QPushButton("Convertir")
                bouton_convertir.clicked.connect(lambda _, r=row, n=nom: self.demander_quantite_conversion(r, n))
                self.table_widget.setCellWidget(row, 9, bouton_convertir)
            else:
                self.table_widget.setCellWidget(row, 9, QLabel(""))
        else:
            self.table_widget.setCellWidget(row, 9, QLabel(""))



    def demander_quantite_conversion(self, row, nom):
        """Demander la quantité de livres à convertir."""
        objet = self.inventaire_filtre[nom]
        if "1" in nom:
            quantite_max = getattr(objet, "quantite", 0)/2
        elif "2" in nom:
            quantite_max = getattr(objet, "quantite", 0)/3
        elif "3" in nom:
            quantite_max = getattr(objet, "quantite", 0)/4
        elif "4" in nom:
            quantite_max = getattr(objet, "quantite", 0)/5
        elif "5" in nom:
            quantite_max = getattr(objet, "quantite", 0)/6
        quantite_max = math.floor(quantite_max)
        




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
        parts = nom.split()
        for part in parts:
            if part.isdigit():  # ✅ Cherche le premier nombre dans le nom
                niveau_actuel= int(part)
          
        niveau_cible = niveau_actuel + 1

        if niveau_cible >6:  # Niveau max = 6
            QMessageBox.warning(self, "Erreur", "Niveau maximal atteint (6).")
            return

       
        stats = convertir_livres(self.joueur, niv=niveau_cible, nb=quantite) 
        # Mettre à jour l'affichage
        self.mettre_a_jour_inventaire_rapide()
        QMessageBox.information(
            self,
            "Succès",
            f"{quantite} {nom}(s) converti(s) en niveau {niveau_cible} !\nStatistiques: {stats}"
        )
        self.mettre_a_jour_inventaire_complet()

    def _calculer_prix_unitaire(self, objet):

        type_objet = getattr(objet, "type_objet", "").lower()
        nom_recherche = getattr(objet, "nom_base", getattr(objet, "nom", "inconnu")).replace("_", " ")

        if type_objet in ["potion", "de base", "livres"]:
            prix_base = self.prix_objets.get(nom_recherche, 10)
            return round(prix_base * 0.75)
        elif type_objet in ["equipement", "armes"]:
            prix_base = self.prix_objets.get(nom_recherche, 10)
            niv = getattr(objet, "niv", 0)
            return round(prix_base * 0.75 + niv * 1000)
        else:
            return 10  # Prix par défaut

    def _vendre_objet_interne(self, nom, quantite):
   
        if nom.lower() == "argent":
            raise ValueError("Impossible de vendre de l'argent.")

        objet = self.inventaire_filtre[nom]
        if quantite > objet.quantite:
            raise ValueError(f"Quantité demandée ({quantite}) > quantité disponible ({objet.quantite}).")

        prix_unitaire = self._calculer_prix_unitaire(objet)
        prix_total = quantite * prix_unitaire

        objet.retirer(quantite)
        if objet.quantite <= 0:
            del self.inventaire_filtre[nom]
        if nom in self.inventaire:
            del self.inventaire[nom]

        safe_increment(self.inventaire, "argent", quant=prix_total)
        return prix_total
    def vendre_objet(self, row, nom):
        
        self.mettre_a_jour_inventaire_complet()
        noms = list(self.inventaire_filtre.keys())
        if row < 0 or row >= len(noms):
            return

        objet = self.inventaire_filtre[nom]
        quantite, ok = QInputDialog.getInt(
        self,
        "Vendre un objet",
        f"Quantité de {objet.nom} à vendre (max: {objet.quantite}):",
        1, 1, objet.quantite,
    )

        if ok:
            try:
                prix_total = self._vendre_objet_interne(nom, quantite)
                QMessageBox.information(
                self, "Vente",
                f"Vous avez vendu {quantite} {objet.nom}(s) pour {prix_total} pièces d'or!"
            )
                self.mettre_a_jour_inventaire_complet()
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))

    def vendre_tous_meme_nom(self, objet):
        """Vend tous les objets du même type (même nom_base)."""
        self.mettre_a_jour_inventaire_complet()

        # Trouver le nom_base de l'objet
        nom_base = getattr(objet, "nom_base", None)
        if not nom_base:
            QMessageBox.warning(self, "Erreur", "Impossible de déterminer le type de l'objet.")
            return

        # Trouver tous les objets avec le même nom_base dans l'inventaire COMPLET
        objets_similaires = [
            (nom_key, obj)
            for nom_key, obj in self.inventaire.items()
            if getattr(obj, "nom_base", nom_key) == nom_base and obj.quantite > 0
        ]

        if not objets_similaires:
            QMessageBox.warning(self, "Erreur", "Aucun objet trouvé.")
            return

        # Calculer quantité totale et prix total
        quantite_totale = sum(obj.quantite for _, obj in objets_similaires)
        prix_total = sum(
            self._calculer_prix_unitaire(obj) * obj.quantite
            for _, obj in objets_similaires
        )

        # Confirmation
        confirm = QMessageBox.question(
            self,
            "Confirmation de vente",
            f"Vendre tous les '{nom_base}' ?\n"
            f"- Nombre d'objets : {quantite_totale}\n"
            f"- Prix total : {prix_total} pièces d'or\n"
            f"- Objets concernés : {len(objets_similaires)}",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            try:
                # Supprimer chaque objet de l'inventaire et de l'index
                for nom_key, obj in objets_similaires:
                    if isinstance(obj, Livres):
                        # Supprimer de livres_par_enchantements
                        cle_enchantements = tuple(obj.enchantements)
                        if cle_enchantements in livres_par_enchantements:
                            del livres_par_enchantements[cle_enchantements]
                    # Supprimer de l'inventaire
                    del self.inventaire[nom_key]

                # Ajouter l'argent
                safe_increment(self.inventaire, "argent", quant=prix_total)

                # Mettre à jour l'index et l'interface
                mettre_a_jour_index(self.inventaire)
                self.mettre_a_jour_inventaire_complet()

                QMessageBox.information(
                    self,
                    "Vente réussie",
                    f"{quantite_totale} objet(s) vendu(s) pour {prix_total} pièces d'or !"
                )
                self.mettre_a_jour_inventaire_complet()
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Une erreur est survenue : {str(e)}")
    def boire(self, row, nom):
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

        self.mettre_a_jour_inventaire_rapide()

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
                "Le fichier objet_dispo.json n'est pas un fichiAer JSON valide.",
            )
            return {}

    def effectuer_recherche(self):
        """Effectue la recherche en fonction du texte saisi."""
        texte = self.barre_recherche.text()
        self.filtrer_inventaire(texte)

    def filtrer_inventaire(self, texte):

    # ✅ 1. Met à jour l'index avant la recherche
        mettre_a_jour_index(self.inventaire)

    # ✅ 2. Effectue la recherche dans l'index
        cles_trouvees = rechercher_dans_index(texte, self.inventaire)

    # ✅ 3. Met à jour l'inventaire filtré
        self.inventaire_filtre = {
        cle: self.inventaire[cle]
        for cle in cles_trouvees
    }

def afficher_inventaire(inventaire, joueur, parent=None):
    dialog = FenetreInventaire(inventaire, joueur, parent)
    dialog.exec()  # Utilisez exec() pour une boîte de dialogue modale
    # Ou utilisez dialog.show() pour une fenêtre non-modale
