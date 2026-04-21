from PySide6.QtWidgets import (QVBoxLayout,QMessageBox,QInputDialog,QPushButton,QDialog)
from inventaire import qtes,safe_increment
import json
from horloge import réinitialiser
import os
class FenetreBanque(QDialog):
    FICHIER_SAUVEGARDE_BANQUE = "banque_save.json"
    def __init__(self,joueur,horloge_jeu,horloge2,parent):
        super(FenetreBanque, self).__init__(parent)
        self.joueur = joueur
        self.horloge_jeu = horloge_jeu
        self.horloge2=horloge2
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
        self.verifier_blocage_boutons()

        
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
            self.sauvegarder_etat_banque()
            QMessageBox.information(
                self,
                "Remboursement",
                f"Vous avez remboursé {montant:.2f} pièces d'or. Dettes restantes: {self.dettes:.2f}",
            )
            self.verifier_blocage_boutons()

    def emprunter(self):
        """Demande la quantité à emprunter et met à jour l'inventaire et les dettes."""
        montant, ok = QInputDialog.getInt(
            self, "Emprunt", "Montant à emprunter:", 100, 1, 1000000, 100
        )
        if ok:
            safe_increment(self.joueur.stuff, "argent", quant=montant)
            self.dettes += montant * 1.10
            self.dettes = round(self.dettes)
            self.date_emprunt_mois = self.horloge2.mois
            self.date_emprunt_annees = self.horloge2.annees
            self.sauvegarder_etat_banque()
            QMessageBox.information(
                self,
                "Emprunt",
                f"Vous avez emprunté {montant} pièces d'or. Dettes totales: {self.dettes}",
            )
            self.verifier_blocage_boutons()

    def verifier_blocage_boutons(self):
        if self.dettes > 0:
            # Bloquer le bouton "Investir" dès qu'il y a des dettes
            self.bouton_investir.setEnabled(False)

            # Bloquer le bouton "Emprunter" si les dettes dépassent 100 000
        if self.dettes >= 100000:
            self.bouton_emprunter.setEnabled(False)

            # Vérifier si le délai de remboursement est dépassé
        if hasattr(self, 'date_emprunt_mois') and hasattr(self, 'date_emprunt_annees'):
            # Calculer le nombre de mois écoulés depuis l'emprunt
            mois_ecoules = (self.horloge2.annees - self.date_emprunt_annees) * 12 + (
                        self.horloge2.mois - self.date_emprunt_mois)

            # Si plus d'un an (12 mois) s'est écoulé, appliquer les pénalités
            if mois_ecoules > 12:
                mois_retard = mois_ecoules - 12
                self.dettes += self.dettes * 0.10 * mois_retard
                self.bouton_emprunter.setEnabled(False)
        else:
            # Réactiver les boutons si aucune dette
            self.bouton_emprunter.setEnabled(True)
            self.bouton_investir.setEnabled(True)

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
                réinitialiser(self.horloge_jeu,self.joueur)

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
        "date_emprunt_mois": self.date_emprunt_mois,
        "date_emprunt_annees": self.date_emprunt_annees,
        "investissements": self.investissements,
        }

        with open(
            FenetreBanque.FICHIER_SAUVEGARDE_BANQUE, "w", encoding="utf-8"
        ) as fichier:
            json.dump(data, fichier, indent=4)

    def afficher_banque(self, **kwargs):
        with open("save.txt", "a", encoding="utf-8") as fichier:
            fichier.write("\nbanque")

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
                if lignes and lignes[-1].strip() == "reprise du jeu" or "continuer" or "charge":
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
                                self.date_emprunt_mois = player_data.get("date_emprunt_mois",0)
                                self.date_emprunt_annees = player_data.get("date_emprunt_annees",0)
                                
                        except json.JSONDecodeError:
                            raise json.JSONDecodeError
            with open("save.txt", "a", encoding="utf-8") as fichier:
                fichier.write("\ncharge")

def afficher_banque(joueur,horloge_jeu,horloge2,parent,**kwargs):
    b = kwargs.get("b", True)
    dialog = FenetreBanque(joueur, horloge_jeu,horloge2, parent)
    dialog.afficher_banque(b=b)

    if b == False:
        dialog.hide()
    else:
        dialog.exec()
    dialog.verifier_investissements()
