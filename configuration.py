from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
)
from PySide6.QtCore import Qt


class ModeDeJeuDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurer la partie")
        self.setModal(True)

        # Variables pour stocker les choix
        self.mode = None
        self.difficulte = None
        self.type_armee = None

        # Layout principal
        layout = QVBoxLayout(self)

        # Titre
        label_titre = QLabel("Configurer votre partie :")
        label_titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_titre)

        # Sélection du mode de jeu
        mode_layout = QHBoxLayout()
        label_mode = QLabel("Mode de jeu :")
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["Aventure", "Militaire"])
        self.combo_mode.currentTextChanged.connect(self._mettre_a_jour_affichage)
        mode_layout.addWidget(label_mode)
        mode_layout.addWidget(self.combo_mode)
        layout.addLayout(mode_layout)

        # Sélection de la difficulté
        difficulte_layout = QHBoxLayout()
        label_difficulte = QLabel("Difficulté :")
        self.combo_difficulte = QComboBox()
        self.combo_difficulte.addItems(["Facile", "Moyen", "Difficile"])
        difficulte_layout.addWidget(label_difficulte)
        difficulte_layout.addWidget(self.combo_difficulte)
        layout.addLayout(difficulte_layout)

        # Sélection du type d'armée (masqué par défaut)
        self.group_armee = QGroupBox("Type d'armée :")
        self.armee_layout = QHBoxLayout()
        self.combo_armee = QComboBox()
        self.combo_armee.addItems(["Terre", "Air", "Marine", "Gendarmerie"])
        self.armee_layout.addWidget(self.combo_armee)
        self.group_armee.setLayout(self.armee_layout)
        self.group_armee.hide()  # Masqué par défaut
        layout.addWidget(self.group_armee)

        # Boutons de validation
        boutons_layout = QHBoxLayout()
        bouton_valider = QPushButton("Valider")
        bouton_valider.clicked.connect(self._valider_choix)
        bouton_annuler = QPushButton("Annuler")
        bouton_annuler.clicked.connect(self.reject)
        boutons_layout.addWidget(bouton_valider)
        boutons_layout.addWidget(bouton_annuler)
        layout.addLayout(boutons_layout)

    def _mettre_a_jour_affichage(self, mode):
        """Affiche ou masque le choix du type d'armée selon le mode."""
        if mode == "Militaire":
            self.group_armee.show()
        else:
            self.group_armee.hide()

    def _valider_choix(self):
        """Stocke les choix et ferme la boîte de dialogue."""
        self.mode = self.combo_mode.currentText()
        self.difficulte = self.combo_difficulte.currentText()
        if self.mode == "Militaire":
            self.type_armee = self.combo_armee.currentText()
        self.accept()


def demander_configuration_jeu(parent=None):
    """
    Affiche la boîte de dialogue de configuration et retourne un dictionnaire avec :
    - "mode" : "Aventure" ou "Militaire"
    - "difficulte" : "Facile", "Moyen" ou "Difficile"
    - "type_armee" : "Marine", "Air" ou "Terre" (si mode Militaire)
    Retourne None si annulé.
    """
    dialog = ModeDeJeuDialog(parent)
    if dialog.exec_() == QDialog.Accepted:
        result = {
            "mode": dialog.mode,
            "difficulte": dialog.difficulte,
        }
        if dialog.mode == "Militaire":
            result["type_armee"] = dialog.type_armee
        return result
    else:
        return None
