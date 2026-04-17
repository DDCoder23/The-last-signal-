import threading
import time
import json
import os
from typing import Optional, Dict, Any

horloges = []


class HorlogeJeu:
    """
    Une horloge pour le jeu où 1 minute dans le jeu = 1 seconde en réalité.
    Gère les conversions en jours, semaines, mois et années.
    """

    FICHIER_SAUVEGARDE = "horloge_jeu.json"  # Nom du fichier de sauvegarde

    def __init__(self, id: int, joueur="Unknown Player"):
        """
        Initialise l'horloge du jeu.
        """
        self.id = id
        self.joueur = joueur
        self.heures = 0
        self.minutes = 0
        self.jours = 0
        self.semaines = 0
        self.mois = 0
        self.annees = 0
        self.en_cours = False
        self.thread = threading.Thread(target=self._mettre_a_jour_horloge, daemon=True)
        self.verrou = threading.Lock()
        self.evenements = {
            "nouveau_jour": [],
            "nouvelle_semaine": [],
            "nouveau_mois": [],
            "nouvelle_annee": [],
        }
        horloges.append(self)

    def demarrer(self, **kwargs):
        """
        Démarre l'horloge du jeu.
        """
        if not self.en_cours:
            print(f"horloge{self.id} démarée")
            self.en_cours = True
            if kwargs.get("recommencer", False) == False:
                print("chargée")
                self.charger_depuis_json()
            self.thread.start()

    def arreter(self) -> None:
        """
        Arrête l'horloge du jeu.
        """

        self.sauvegarder_dans_json()
        self.en_cours = False  # Sauvegarder une dernière fois avant de quitter

    def _mettre_a_jour_horloge(self) -> None:
        while self.en_cours:
            self.sauvegarder_dans_json()
            time.sleep(1)  # 1 seconde en réalité = 1 minute en jeu

            with self.verrou:
                self.minutes += 1
                # Sauvegarder à chaque mise à jour

                # Conversion des minutes en heures
                if self.minutes >= 60:
                    self.minutes = 0
                    self.heures += 1
                    # Sauvegarder après chaque conversion

                    # Conversion des heures en jours
                    if self.heures >= 24:
                        self.heures = 0
                        self.jours += 1
                        self._declencher_evenement("nouveau_jour")
                        # Sauvegarder après chaque conversion

                        # Conversion des jours en semaines
                        if self.jours >= 7:
                            self.jours = 0
                            self.semaines += 1
                            self._declencher_evenement("nouvelle_semaine")
                            # Sauvegarder après chaque conversion

                            # Conversion des semaines en mois
                            if self.semaines >= 4:
                                self.semaines = 0
                                self.mois += 1
                                self._declencher_evenement("nouveau_mois")
                                # Sauvegarder après chaque conversion

                                # Conversion des mois en années
                                if self.mois >= 12:
                                    self.mois = 0
                                    self.annees += 1
                                    self._declencher_evenement("nouvelle_annee")
                                    # Sauvegarder après chaque conversion

    def _declencher_evenement(self, type_evenement: str) -> None:
        """
        Déclenche les callbacks enregistrés pour un type d'événement donné.
        """
        for callback in self.evenements[type_evenement]:
            callback()

    def enregistrer_evenement(self, type_evenement: str, callback: callable) -> None:
        """
        Enregistre un callback pour un type d'événement donné.
        """
        if type_evenement in self.evenements:
            self.evenements[type_evenement].append(callback)
        else:
            raise ValueError(f"Type d'événement inconnu : {type_evenement}")

    def obtenir_heure(self) -> Dict[str, int]:
        """
        Retourne l'heure actuelle du jeu sous forme de dictionnaire.
        """
        with self.verrou:
            return {
                "minutes": self.minutes,
                "heures": self.heures,
                "jours": self.jours,
                "semaines": self.semaines,
                "mois": self.mois,
                "annees": self.annees,
            }

    def obtenir_heure_formatee(self) -> str:
        """
        Retourne l'heure actuelle du jeu sous forme de chaîne formatée.
        """
        with self.verrou:
            return (
                f"{self.annees}a {self.mois}m {self.semaines}s {self.jours}j "
                f"{self.heures:02d}:{self.minutes:02d}"
            )

    def sauvegarder_dans_json(self) -> None:
        """
        Sauvegarde l'état actuel de l'horloge dans un fichier JSON.
        """
        data = {}
        if os.path.exists(HorlogeJeu.FICHIER_SAUVEGARDE):
            with open(HorlogeJeu.FICHIER_SAUVEGARDE, "r", encoding="utf-8") as fichier:
                try:
                    data = json.load(fichier)
                except json.JSONDecodeError:
                    data = {}

        with self.verrou:

            data[self.joueur + " : " + str(self.id)] = {
                "id": self.id,
                "minutes": self.minutes,
                "heures": self.heures,
                "jours": self.jours,
                "semaines": self.semaines,
                "mois": self.mois,
                "annees": self.annees,
            }

        with open(HorlogeJeu.FICHIER_SAUVEGARDE, "w", encoding="utf-8") as fichier:
            json.dump(data, fichier, indent=4)

    def charger_depuis_json(self) -> None:
        if os.path.exists(HorlogeJeu.FICHIER_SAUVEGARDE):
            try:
                with open(
                    HorlogeJeu.FICHIER_SAUVEGARDE, "r", encoding="utf-8"
                ) as fichier:
                    contenu = fichier.read().strip()
                    if contenu:
                        data = json.loads(contenu)
                        horloge_data = data.get(self.joueur + " : " + str(self.id), {})
                        print(horloge_data)

                        with self.verrou:
                            self.id = horloge_data.get("id", self.id)
                            self.heures = horloge_data.get("heures", self.heures)
                            self.minutes = horloge_data.get("minutes", self.minutes)
                            self.jours = horloge_data.get("jours", self.jours)
                            self.semaines = horloge_data.get("semaines", self.semaines)
                            self.mois = horloge_data.get("mois", self.mois)
                            self.annees = horloge_data.get("annees", self.annees)
                    else:
                        print(
                            f"[HORLOGE] Le fichier {HorlogeJeu.FICHIER_SAUVEGARDE} est vide. Initialisation avec des valeurs par défaut."
                        )
                        self.sauvegarder_dans_json()
            except json.JSONDecodeError:
                print(
                    f"[HORLOGE] Le fichier {HorlogeJeu.FICHIER_SAUVEGARDE} est mal formé. Initialisation avec des valeurs par défaut."
                )
                self.sauvegarder_dans_json()
            except Exception as e:
                print(f"[HORLOGE] Erreur lors de la lecture du fichier : {e}")
        else:
            print(
                f"[HORLOGE] Le fichier {HorlogeJeu.FICHIER_SAUVEGARDE} n'existe pas. Initialisation avec des valeurs par défaut."
            )
            self.sauvegarder_dans_json()


def arreter_toutes_horloges():
    """Arrête tous les threads des horloges."""
    for horloge in horloges:
        horloge.sauvegarder_dans_json()
        horloge.arreter()
    print("Toutes les horloges ont été arrêtées.")
