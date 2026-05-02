from __future__ import annotations
import random
import Secure_save
import os
import jet_de_des as de
import tresor
from vispy import scene
import numpy as np
from PIL import Image
import generate_map as gemap
import admin_manager
import PySide6.QtWidgets as qt
from PySide6.QtCore import Qt, QTimer
import table_de_conversion as tc
import grade_manager as gr
import configuration as cr
from horloge import HorlogeJeu, arreter_toutes_horloges
import atexit
import logging
from admin_manager import IS_ADMIN
from inventaire import (
    Objet,
    equipement,
    Armes,
    Potion,
    safe_increment,
    liste_armes,
    Livres,
    afficher_magasin,
    liste_outils,
    liste_muni,
    liste_potion,
    ajouter_enchant,
    clefs

)
import sys
import configparser
import json
import dill
from inv import afficher_inventaire
from banque import afficher_banque
import re
from collections import defaultdict
configs = configparser.ConfigParser()
configs.read("config.ini", encoding="utf-8")

mot_de_passe = configs["save"]["password"]
perso= {}

def lister_profils_sauvegardes(base_dir="saves"):
    if not os.path.exists(base_dir):
        print("[SAVE] Aucun dossier de sauvegarde trouvé.")
        return {}
    profils = {}
    for profil in os.listdir(base_dir):
        profil_path = os.path.join(base_dir, profil)
        if not os.path.isdir(profil_path):
            continue
        slots = []
        for i in (1, 2, 3):
            if os.path.exists(os.path.join(profil_path, f"slot{i}.zip")):
                slots.append(i)
        profils[profil] = slots

    return profils


profils = lister_profils_sauvegardes()

ASSETS_DIR = "assets"

# Vérifier que les fichiers de carte existent dans assets/
REQUIRED_MAP_FILES = [
    os.path.join(ASSETS_DIR, "map_height.png"),
    os.path.join(ASSETS_DIR, "map_color.png"),
    os.path.join(ASSETS_DIR, "map_collision.png")
]

# Vérification (optionnelle, pour un message d'erreur clair)
missing_files = [f for f in REQUIRED_MAP_FILES if not os.path.exists(f)]
if missing_files:
    raise FileNotFoundError(
        f"❌ Fichiers de carte manquants dans {ASSETS_DIR}: {missing_files}. "
        "Assurez-vous que les fichiers sont bien présents."
    )
class SaveSelectWidget(qt.QWidget):
    def __init__(self, on_load, on_back, profils):
        super().__init__()

        self.on_load = on_load
        self.on_back = on_back
        self.profils = profils

        layout = qt.QVBoxLayout()

        # Titre
        title = qt.QLabel("💾 Sélection de sauvegarde")
        title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(title)

        # Liste profils / slots
        self.listbox = qt.QListWidget()
        for profil, slots in self.profils.items():
            for slot in slots:
                self.listbox.addItem(f"{profil} — Slot {slot}")
        layout.addWidget(self.listbox)

        # Boutons
        btn_layout = qt.QHBoxLayout()
        btn_load = qt.QPushButton("▶️ Charger")
        btn_back = qt.QPushButton("🔙 Retour")
        btn_layout.addWidget(btn_load)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)

        # Bind événements
        btn_load.clicked.connect(self._charger)
        btn_back.clicked.connect(self.on_back)

        self.setLayout(layout)

    def _charger(self):
        item = self.listbox.currentItem()
        if item is None:
            return

        label = item.text()
        profil, slot = label.split("—")
        profil = profil.strip()
        slot = int(slot.replace("Slot", "").strip())

        self.on_load(profil, slot)


from functools import lru_cache

@lru_cache(maxsize=3)  # Cache les 3 dernières sauvegardes
def reprendre_joueur(nom_profil: str, mot_de_passe: str, slots=(1, 2, 3)):
    if isinstance(slots, int):
        slots = (slots,)

    for slot in slots:
        try:
            print(f"[LOAD] tentative slot {slot}")
            return Secure_save.load_from_slot(nom_profil, slot, mot_de_passe)
        except FileNotFoundError:
            continue
        except ValueError:
            continue

    print("[LOAD] aucune sauvegarde valide trouvée")
    return None
def reconstruire_stuff(etat_charge):
    stuff_reconstruit = {}

    for nom_obj, data in etat_charge.get("stuff", {}).items():

        if isinstance(data, dict):

            niv = data.get("niv")
            durabilite = data.get("durabilite")
            effet=data.get("effet")
            enchants=data.get("enchants")            

            #  ARME 
            if isinstance(durabilite, int):
                stuff_reconstruit[nom_obj] = Armes(
                    nom=data.get("nom", nom_obj),
                    image=data.get("image", ""),
                    quantite=data.get("quantite", 1),
                    niv=niv or 1,
                    durabilite=durabilite,
                )

            # ÉQUIPEMENT
            elif isinstance(niv, int):
                stuff_reconstruit[nom_obj] = equipement(
                    nom=data.get("nom", nom_obj),
                    image=data.get("image", ""),
                    quantite=data.get("quantite", 1),
                    niv=niv or 1,
                )
            #Potion
            elif isinstance(effet, str) or effet is None:
                stuff_reconstruit[nom_obj] = Potion(
                    nom=data.get("nom", nom_obj),
                    image=data.get("image", ""),
                    quantite=data.get("quantite", 1),
                    effet=effet,
                )
            #Livres

            elif isinstance(enchants, list) or enchants is None:
                stuff_reconstruit[nom_obj] = Livres(
                    nom=data.get("nom", nom_obj),
                    image=data.get("image", ""),
                    quantite=data.get("quantite", 1),
                    category=data.get("category"),
                    echants=enchants


                )

            # OBJET SIMPLE
            else:
                stuff_reconstruit[nom_obj] = Objet(
                    nom=data.get("nom", nom_obj),
                    image=data.get("image", ""),
                    quantite=data.get("quantite", 1),
                )

        else:
            stuff_reconstruit[nom_obj] = data

    return stuff_reconstruit


class Jeu:
    pass


class PersoCore:
    """Modèle de personnage (logique métier uniquement)."""

    STATS = ["FOR", "DEX", "CON", "INT", "SAG", "CHA"]

    @staticmethod
    def get_modifier(value):
        modifiers = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        index = (value - 1) // 2
        return modifiers[index] if 0 <= index < len(modifiers) else 0

    @classmethod
    def generer_stats(cls, jeu: Jeu):
        valeurs = [
            sum(sorted([de.jet_de_des(6, 4)], reverse=True)[:3]) for _ in range(6)
        ]
        stats = dict(zip(cls.STATS, valeurs))
        for n in cls.STATS:
            stats[f"MOD_{n}"] = cls.get_modifier(stats[n])
        stats["PV_MAX"] = (stats["CON"] // 2) + 12
        stats["PV"] = stats["PV_MAX"]
        stats["DEF"] = 10 + stats["MOD_DEX"]
        return stats


class Lutin:
    def __init__(self, image, largeur=200, hauteur=200, z=0):
        self.image = image
        self.largeur = largeur
        self.hauteur = hauteur
        self.x = 0
        self.y = 0
        self.z = z


    @property
    def position(self):
        return (self.x, self.y, self.z)

    def set_position(self, x, y):
        self.x = x
        self.y = y


class Perso(Lutin):

    def __init__(self, image, jeu: Jeu):
        super().__init__(image)
        self.stats = PersoCore.generer_stats(jeu)
        self.nom = "Inconnu"
        self.vivant = True
        self.vitesse = 0.4

    def deplacer(self, dx, dy, game_map):
        if not self.vivant:
            return

        self.x = np.clip(self.x + dx, 0, game_map.width - 1)
        self.y = np.clip(self.y + dy, 0, game_map.height - 1)

        self.z = game_map.get_height(self.x, self.y)

    def subir_degats(self, degats: int):
        self.stats["PV"] -= max(0, degats)
        if self.stats["PV"] <= 0:
            self.stats["PV"] = 0
            self.vivant = False
    def liste(self):
        perso[self.nom]=self
        with open(
            "joueurs.dill", "wb"
        ) as fichier:
            dill.dump(perso, fichier)
    @staticmethod
    def jet_attaque(attaquant: Perso, defenseur: Perso) -> bool:
        jet = de.jet_de_des(20, 1) + attaquant.stats["MOD_FOR"]
        return jet >= defenseur.stats["DEF"]

    @staticmethod
    def calcul_degats(attaquant: Perso) -> int:
        return max(1, de.jet_de_des(20, 1) + attaquant.stats["MOD_FOR"])


class Joueur(Perso):
    def __init__(
        self, image, jeu: Jeu, nom="Player 1", recommencer=True, grade=None, config=None
    ):
        super().__init__(image, jeu)
        self.nom = nom
        self.vivant = True
        self.stats["MANA_max"] = 100
        self.stats["MANA"] = self.stats["MANA_max"]
        self.stats["XP"] = 0
        self.stats["niv"] = 1
        self.stats["bouff_max"] = self.stats["niv"] * 10
        self.stats["bouff"] = self.stats["bouff_max"]
        self.stuff = {}
        self.index_arme_selectionnee = 0
        self.grade = grade
        self.config = config
        

        if recommencer == False:
            etat_charge = reprendre_joueur(self.nom, mot_de_passe)
            if etat_charge:
                self.stuff = reconstruire_stuff(etat_charge)
                clefs=etat_charge.get("clefs",{})
        else:
            self.stuff = {}
            safe_increment(self.stuff, "corde", quant=1)
            safe_increment(self.stuff, "torche", quant=2)
            safe_increment(self.stuff, "argent", quant=100)
            safe_increment(self.stuff, "sac", quant=2)
            safe_increment(
                self.stuff,
                "épée de bois",
                quant=2,
                type_objet="armes",
                durabilite=100,
            )

    def save(self):
        autosave = Secure_save.AutoSaver(
            provider=autosave_provider_factory(self),
            profile=self.nom,
            slot=1,
            password=mot_de_passe,
            interval=5,
        )
        autosave.start()

    def to_dict(self):
        stuff_serializable = {}
        for k, v in self.stuff.items():
            if isinstance(v, Objet):
                stuff_serializable[k] = {
                    "nom": v.nom_base,
                    "quantite": v.quantite,
                    "durabilite": getattr(v, "durabilite", None),
                    "niv": getattr(v, "niv", None),
                    "effet":getattr(v,"effet",None),
                    "category":getattr(v,"category",None),
                    "enchantements":getattr(v,"enchantements",None),
                                        
                }
            else:
                stuff_serializable[k] = v
        config_dict = {}
        if hasattr(self.config, "sections"):
            for section in self.config.sections():
                config_dict[section] = {}
                for key, value in self.config.items(section):
                    config_dict[section][key] = value
        elif isinstance(self.config, dict):
            config_dict = self.config.copy()

        return {
            "image": self.image,
            "position": self.position,
            "stats": self.stats,
            "stuff": stuff_serializable,
            "grade": self.grade,
            "config": config_dict,
            "clefs" : clefs
        }

   



class Adversaire(Perso):
    def __init__(self, image, jeu: Jeu, nom="Monstre"):
        super().__init__(image, jeu)
        self.nom = nom
        self.vivant = True

    def cara_sup(self, NC, Mod_cre):
        self.stats["NC"] = NC
        self.stats["Mod_cre"] = Mod_cre
        self.stats["NIvtr"] = (
            self.stats["NC"] + self.stats["Mod_cre"] + self.stats["MOD_INT"]
        )


class Combat:
    @staticmethod
    def attaquer(attaquant: Perso, defenseur: Perso) -> bool:
        if not attaquant.vivant or not defenseur.vivant:
            return False

        touche = Perso.jet_attaque(attaquant, defenseur)
        if touche:
            degats = Perso.calcul_degats(attaquant)
            defenseur.subir_degats(degats)
        return touche


def autosave_provider_factory(joueur):
    slot = 1

    def provider():
        nonlocal slot

        data = joueur.to_dict()

        data["_slot_used"] = slot
        slot = 1 if slot == 3 else slot + 1

        return data

    return provider


class Map3D:
    def __init__(self, image_path, scale_z=5.0):
        self.img = Image.open(image_path).convert("L")  # grayscale
        self.width, self.height = self.img.size
        self.pixels = np.zeros((self.height, self.width))
        self.scale_z = scale_z

    def get_height(self, x, y):
        ix = int(np.clip(x, 0, self.width - 1))
        iy = int(np.clip(y, 0, self.height - 1))
        return self.pixels[iy, ix] * self.scale_z


class VispyWidget(qt.QWidget):
    def __init__(self, parent, joueur_obj):
        super().__init__(parent)

        self.joueur = joueur_obj
        self.open_tresors = []

        # Layout principal
        layout = qt.QVBoxLayout()
        self.setLayout(layout)

        # ==========================
        # CANVAS VISPY
        # ==========================
        self.canvas = scene.SceneCanvas(keys="interactive", show=True)
        layout.addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.cameras.TurntableCamera(
            elevation=45, azimuth=45, distance=150, fov=70.0
        )

        # ==========================
        # MAP 3D (IMAGE HEIGHTMAP)
        # ==========================
        self.map = Map3D(r".\assets\map_height.png", scale_z=12)
        self.view.camera.center = (
            self.map.width // 2,
            self.map.height // 2,
            0,
        )  # Centre du terrain

        self.view.camera.position = (
            self.map.width // 2,
            self.map.height // 2,
            10,
        )  # Position de la caméra en hauteur
        self.view.camera.position = (
            self.joueur.x,
            self.joueur.y,
            self.joueur.z - 5,
        )  # Hauteur des yeux

        self.view.bgcolor = (0.1, 0.3, 0.8, 1)
        self.camera_angle = 0  # Bleu ciel (RGBA)
        self.view.camera.elevation = 25

        self.view.camera.distance = 50

        w, h = self.map.width, self.map.height
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        z = np.zeros_like(x)

        vertices = np.c_[x.flatten(), y.flatten(), z.flatten()].astype(np.float32)

        faces = []
        for j in range(h - 1):
            for i in range(w - 1):
                idx = j * w + i
                faces.append([idx, idx + 1, idx + w])
                faces.append([idx + 1, idx + w + 1, idx + w])
        faces = np.array(faces, dtype=np.uint32)

        self.terrain = scene.visuals.Mesh(
            vertices=vertices,
            faces=faces,
            shading=None,
            color=(0.35, 0.75, 0.35, 1),
        )
        self.view.add(self.terrain)

        # ==========================
        # POSITION INITIALE JOUEUR
        # ==========================
        self.joueur.x = w // 2
        self.joueur.y = h // 2
        self.joueur.z = self.map.get_height(self.joueur.x, self.joueur.y)

        # ==========================
        # MARKER JOUEUR
        # ==========================
        self.joueur_marker = scene.visuals.Markers()
        self.joueur_marker.set_data(
            np.array([[self.joueur.x, self.joueur.y, self.joueur.z + 0.5]]),
            face_color=(1, 0, 0, 1),
            size=14,
        )
        self.view.add(self.joueur_marker)

        # ==========================
        # UI TEXTE
        # ==========================
        self.info_text = qt.QTextEdit()
        self.info_text.setReadOnly(True)
        layout.addWidget(self.info_text)

        # ==========================
        # EVENTS
        # ==========================
        self.canvas.events.key_press.connect(self.on_key_vispy)
        self.canvas.native.setFocus()

        self.update_info()

    def on_key_vispy(self, event):
        key = event.native.key()
        mods = event.modifiers
        ctrl = "Control" in mods

        # Calculer le déplacement en fonction de l'angle de la caméra
        dx, dy = 0, 0
        if key == Qt.Key_Up:
            dy = 1
        elif key == Qt.Key_Down:
            dy = -1
        elif key == Qt.Key_Left:
            dx = -1
        elif key == Qt.Key_Right:
            dx = 1
        elif key == Qt.Key_T:
            self.afficher_tresor(47)
        elif key == Qt.Key_E:
            self.joueur.enchanter_arme(MAX_NIV=6, parent_widget=self)
        elif key == Qt.Key_I:
            print(self.joueur.stuff)
            afficher_inventaire(self.joueur.stuff,self.joueur, parent=self)
        elif key == Qt.Key_S:
            afficher_magasin(
                self.joueur.stuff, self.joueur.stuff["argent"].quantite, parent=self
            )
        elif key == Qt.Key_B:
            horloge2 = HorlogeJeu(2, self.joueur.nom)
            horloge3 = HorlogeJeu(3, self.joueur.nom)
            with open("save.txt", "r", encoding="utf-8") as fichier:
                lignes = fichier.readlines()
                print(lignes)
                for ligne in reversed(lignes):
                    if ligne.strip()=="----Nouvelle partie----" or "init":
                        horloge2.demarrer(recommencer=True)
                        
                        break
                    elif ligne.strip()=="reprise du jeu":
                        horloge2.demarrer()
                        

                        break
                    else: 
                        continue
            afficher_banque(self.joueur, horloge2,horloge3, parent=self)

        elif key == Qt.Key_A and ctrl:
            if admin_manager.IS_ADMIN:
                _console = admin_manager.ConsoleAdmin(self.joueur, self)
                # Mettre à jour l'angle de la caméra en fonction des touches Left/Right (rotation)
        if key == Qt.Key_Left:
            self.camera_angle -= 0.1  # Tourner à gauche
        elif key == Qt.Key_Right:
            self.camera_angle += 0.1  # Tourner à droite

            # Calculer le déplacement en fonction de l'angle actuel
        if dx != 0 or dy != 0:
            # Convertir l'angle en vecteur de direction
            rad = self.camera_angle
            move_x = dx * np.cos(rad) - dy * np.sin(rad)
            move_y = dx * np.sin(rad) + dy * np.cos(rad)

            # Normaliser le mouvement
            norm = np.sqrt(move_x**2 + move_y**2)
            if norm > 0:
                move_x /= norm
                move_y /= norm

            # Déplacer le joueur
            self.joueur.deplacer(move_x, move_y, self.map)

        self.refresh_joueur()

    def refresh_joueur(self):
        pos = np.array([[self.joueur.x, self.joueur.y, self.joueur.z + 0.5]])
        self.joueur_marker.set_data(pos)
        cam_x = self.joueur.x + 0.5 * np.sin(self.camera_angle)
        cam_y = self.joueur.y + 0.5 * np.cos(self.camera_angle)

        # Mettre à jour la caméra pour suivre le joueur et regarder dans la bonne direction
        self.view.camera.center = (self.joueur.x, self.joueur.y, self.joueur.z)
        self.view.camera.position = (cam_x, cam_y, self.joueur.z + 1.7)

        # Ajuster l'azimut de la caméra pour qu'elle regarde dans la direction du joueur
        self.view.camera.azimuth = np.degrees(-self.camera_angle)
        self.update_info()

    def update_info(self):
        txt = (
            (
                f"Nom : {self.joueur.nom}\n"
                f"PV : {self.joueur.stats['PV']} / {self.joueur.stats['PV_MAX']}\n"
                f"Grade :{self.joueur.grade}\n"
                f"Position : ({self.joueur.x:.2f}, {self.joueur.y:.2f})"
            )
            if self.joueur.grade != None
            else (
                f"Nom : {self.joueur.nom}\n"
                f"PV : {self.joueur.stats['PV']} / {self.joueur.stats['PV_MAX']}\n"
                f"Position : ({self.joueur.x:.2f}, {self.joueur.y:.2f})"
            )
        )
        self.info_text.setText(txt)

    @gr.manage(lambda self: self.joueur)
    def afficher_tresor(self, niveau):
        te = tresor.create_tresor(niveau)
        dlg = TresorDialogQt(self, te, self.joueur)
        self.open_tresors.append(dlg)

  

# -----------------------------
# DIALOGUE TRESOR NON BLOQUANT
# -----------------------------


class TresorDialogQt(qt.QDialog):
    def __init__(self, parent, tresor_data, joueur):
        super().__init__(parent)

        self.tresor = tresor_data
        self.joueur = joueur
        self.parent_widget = parent  # VispyWidget

        self.setWindowTitle("🎁 Trésor découvert")
        self.resize(400, 400)
        self.setModal(False)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # ==========================
        # LAYOUT
        # ==========================
        layout = qt.QVBoxLayout(self)

        titre = qt.QLabel("Vous avez trouvé :")
        titre.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(titre)

        # Liste des objets
        self.listbox = qt.QListWidget()
        for nom, qte in self.tresor.items():
            self.listbox.addItem(f"{nom} x{qte}")
        layout.addWidget(self.listbox)

        # Boutons
        btn_layout = qt.QHBoxLayout()
        btn_take = qt.QPushButton("Récupérer")
        btn_close = qt.QPushButton("Fermer")
        btn_layout.addWidget(btn_take)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

        btn_take.clicked.connect(self.on_take)
        btn_close.clicked.connect(self.close)

        self.show()

    # ==========================
    # ACTIONS
    # ==========================
    global TYPE_OBJETS
    TYPE_OBJETS = {
    **{nom: "armes" for nom in liste_armes},
    **{nom: "équipement" for nom in liste_muni + liste_outils},
    **{nom: "potion" for nom in liste_potion},
}





    def on_take(self):
        for nom, qte in self.tresor.items():
            

            if "livre enchant" in nom:
                print(qte)
                try:
                    niveau = int(nom.split()[-1])  # Récupère le dernier mot et le convertit en int
                except ValueError:
                    niveau=1
                finally:
                    for i in range(qte):
                        if 1 <= niveau <= 6:
                            enchantements, category = ajouter_enchant(niveau)
                            print(enchantements)
                            safe_increment(
                        self.joueur.stuff,
                        nom,"livre enchant",
                        quant=1,
                        type_objet="livres",
                        category=category,
                        enchantements=enchantements,
                        niv=niveau
                    )


            else:
                type_objet = TYPE_OBJETS.get(nom, "de base")
                kwargs = {}

                if type_objet == "armes":
                    kwargs.update({"niv": 1, "durabilite": 100})
                elif type_objet == "potion":
                    kwargs.update({"effect": None})

                safe_increment(
            self.joueur.stuff,
            nom,
            quant=qte,
            type_objet=type_objet,
            **kwargs
        )

    # ⚡ Tri UNIQUEMENT à la fin
        self.close()

       

    # ==========================
    # FOCUS (LE POINT VITAL)
    # ==========================
    def closeEvent(self, event):
        super().closeEvent(event)

        # 🔑 RENDRE LE FOCUS AU CANVAS VISPY
        if hasattr(self.parent_widget, "canvas"):
            QTimer.singleShot(
                0,
                lambda: self.parent_widget.canvas.native.setFocus(),
            )


class MainMenuWidget(qt.QWidget):
    def __init__(self, on_new_game, on_load_game):
        super().__init__()

        self.on_new_game = on_new_game
        self.on_load_game = on_load_game

        layout = qt.QVBoxLayout()

        title = qt.QLabel("The last signal")
        title.setStyleSheet("font-size: 18pt; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Nom du joueur
        layout.addWidget(qt.QLabel("Nom du personnage"))
        self.name_edit = qt.QLineEdit()
        self.name_edit.setText("Player1")
        layout.addWidget(self.name_edit)

        # Boutons
        btn_new = qt.QPushButton("🆕 Nouvelle partie")
        btn_load = qt.QPushButton("📂 Charger partie")
        layout.addWidget(btn_new)
        layout.addWidget(btn_load)

        # Bind
        btn_new.clicked.connect(self._new_game)
        btn_load.clicked.connect(self._load_game)

        self.setLayout(layout)

    def _new_game(self):
        name = self.name_edit.text().strip() or "Player1"
        self.on_new_game(name)

    def _load_game(self):
        name = self.name_edit.text().strip() or "Player1"
        self.on_load_game(name)


class EmptyWidget(qt.QWidget):
    def __init__(self):
        super().__init__()
        layout = qt.QVBoxLayout(self)
        layout.addStretch()


class MainFrame(qt.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("The last signal")
        self.resize(900, 900)

        # Initialiser l'horloge du jeu
        self.horloge = HorlogeJeu(1)

        # Créer une étiquette pour afficher l'heure du jeu
        self.etiquette_horloge = qt.QLabel()
        self.etiquette_horloge.setAlignment(Qt.AlignCenter)
        self.etiquette_horloge.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                background-color: #333;
                color: white;
                padding: 8px;
            }
        """
        )

        # Créer un widget pour contenir l'étiquette de l'horloge
        self.widget_horloge = qt.QWidget()
        self.layout_horloge = qt.QVBoxLayout(self.widget_horloge)
        self.layout_horloge.setContentsMargins(0, 0, 0, 0)
        self.layout_horloge.addWidget(self.etiquette_horloge)

        # Créer un widget central principal
        self.widget_central = qt.QWidget()
        self.layout_central = qt.QVBoxLayout(self.widget_central)
        self.layout_central.setContentsMargins(0, 0, 0, 0)
        self.layout_central.setSpacing(0)

        # Créer un widget principal qui contiendra l'horloge et le contenu
        self.widget_principal = qt.QWidget()
        self.layout_principal = qt.QVBoxLayout(self.widget_principal)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        self.layout_principal.addWidget(self.widget_horloge)

        # Ajouter le widget central au layout principal
        self.layout_principal.addWidget(self.widget_central)

        # Définir le widget principal comme widget central de la fenêtre
        self.setCentralWidget(self.widget_principal)

        # Créer un timer pour mettre à jour l'affichage de l'horloge
        self.timer_horloge = QTimer(self)
        self.timer_horloge.timeout.connect(self.mettre_a_jour_horloge)
        self.timer_horloge.start(100)  # Mettre à jour toutes les 100ms

        # Enregistrer les callbacks pour les événements de l'horloge
        self.horloge.enregistrer_evenement("nouveau_jour", self.nouveau_jour)
        self.horloge.enregistrer_evenement("nouvelle_semaine", self.nouvelle_semaine)
        self.horloge.enregistrer_evenement("nouveau_mois", self.nouveau_mois)
        self.horloge.enregistrer_evenement("nouvelle_annee", self.nouvelle_annee)

        self.current_widget = None
        self.show_menu()
      
    
    def mettre_a_jour_horloge(self):
        """Met à jour l'affichage de l'horloge."""
        heure_formatee = self.horloge.obtenir_heure_formatee()
        self.etiquette_horloge.setText(f"⏰ Temps du jeu: {heure_formatee}")

    def nouveau_jour(self):
        """Callback pour un nouveau jour dans le jeu."""
        print("🌅 Un nouveau jour commence dans le jeu !")
        

    def nouvelle_semaine(self):
        """Callback pour une nouvelle semaine dans le jeu."""
        print("📅 Une nouvelle semaine commence dans le jeu !")
       
    def nouveau_mois(self):
        """Callback pour un nouveau mois dans le jeu."""
        print("📆 Un nouveau mois commence dans le jeu !")
       

    def nouvelle_annee(self):
        """Callback pour une nouvelle année dans le jeu."""
        print("🎉 Une nouvelle année commence dans le jeu !")
        
    def show_menu(self):
        if hasattr(self, "current_widget") and self.current_widget:
            self.current_widget.deleteLater()

        self.current_widget = MainMenuWidget(
            on_new_game=self.start_new_game, on_load_game=self.start_load_game
        )
        self.layout_central.addWidget(self.current_widget)
        self.layout()

    def start_new_game(self, player_name):
        self.show_empty()
        with open("save.txt", "a", encoding="utf-8") as fichier:
            fichier.write("\n----Nouvelle partie----")
        data = {}

        with open("banque_save.json", "r", encoding="utf-8") as fichier_json:
            try:
                data = json.load(fichier_json)
            except json.JSONDecodeError:
                data = {}

        data[player_name] = {
            "dettes": 0,
            "investissements": {},
        }

        with open("banque_save.json", "w", encoding="utf-8") as fichier:
            json.dump(data, fichier, indent=4)
        config = cr.demander_configuration_jeu(self)
        grade = None
        if config:
            print(f"Mode: {config['mode']}, Difficulté: {config['difficulte']}")
            if config["mode"] == "Militaire":
                print(f"Type d'armée: {config['type_armee']}")
                if config["type_armee"] == "Terre":
                    grade = "soldat"
                elif config["type_armee"] == "Marine":
                    grade = "mousse"
                elif config["type_armee"] == "Air":
                    grade = "aviateur"
                elif config["type_armee"] == "Gendarmerie":
                    grade = "gendarme adjoint 2e classe"

        MainFrame.start_game(
            self, player_name, recommencer=True, grade=grade, configuration=config
        )

    def start_load_game(self, player_name=None):
        self.show_empty()

        self.show_save_select(player_name)

    def show_empty(self):
        """
        Affiche un widget vide (EmptyWidget) tout en conservant l'affichage de l'horloge.
        """
        if hasattr(self, "current_widget") and self.current_widget:
            self.layout_central.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
            self.current_widget.destroy()

        # Créer un widget vide
        self.current_widget = EmptyWidget()
        self.layout_central.addWidget(self.current_widget)

        # Mettre à jour le layout
        self.layout()

    def clear_layout(self, layout):
        """Supprime tous les widgets d'un layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    @staticmethod
    def start_game(self, player_name, recommencer=False, **kwargs):
        j = kwargs.get("joueur")
        if isinstance(j, Joueur):
            print("")
        self.clear_layout(self.layout_central)

        jeu = Jeu()

        joueur = Joueur(
            "image_joueur.jpg",
            jeu,
            grade=kwargs.get("grade", None),
            nom=player_name,
            config=kwargs.get("configuration", None),
        )
        joueur.liste()
        self.horloge.joueur = joueur.nom
        print(self.horloge.joueur)
        self.horloge.demarrer(recommencer=recommencer)
        horloge2 = HorlogeJeu(2, joueur.nom)
        horloge3 = HorlogeJeu(3, joueur.nom)
        with open("save.txt", "r", encoding="utf-8") as fichier:
            lignes = fichier.readlines()
        if (lignes and lignes[-1].strip() == "reprise du jeu") or (
            lignes
            and (
                lignes[-2].strip() == "reprise du jeu"
                and lignes[-2].strip() == "continuer"
            )
        ):
            horloge2.demarrer()
        afficher_banque(joueur, horloge2,horloge3, parent=self, b=False)
        print(recommencer)
        if not recommencer:
            slot = kwargs.get("slot", 1)
            etat = reprendre_joueur(player_name, mot_de_passe, slots=slot)
            print(etat)
            if etat:
                joueur.stuff = reconstruire_stuff(etat)
                joueur.stats = etat.get("stats", {})
                joueur.config = etat.get("config", {})
                joueur.x, joueur.y, joueur.z = etat.get(
                    "position", {"x": 0, "y": 0, "z": 0}
                )
                joueur.grade = etat.get("grade", None)
                print(joueur.grade)
        joueur.save()

        self.current_widget = VispyWidget(self, joueur)
        self.layout_central.addWidget(self.current_widget)

        QTimer.singleShot(0, lambda: self.current_widget.canvas.native.setFocus())
        admin_manager.demander_mot_de_passe(joueur, self)

        admin_manager.installer_raccourci_admin(self.current_widget, joueur)

    def load_game_from_slot(self, profil, slot):
        with open("save.txt", "a", encoding="utf-8") as fichier:
            fichier.write("\nreprise du jeu")

        self.clear_layout(self.layout_central)
        MainFrame.start_game(self, profil, slot=slot)

    def show_save_select(self, player_name=None):
        if hasattr(self, "current_widget") and self.current_widget:
            self.current_widget.deleteLater()

        self.current_widget = SaveSelectWidget(
            on_load=self.load_game_from_slot, on_back=self.show_menu, profils=profils
        )
        self.layout_central.addWidget(self.current_widget)

        self.layout()

    def layout(self):
        """Met à jour le layout de la fenêtre."""
        if hasattr(self, "current_widget") and self.current_widget:
            self.current_widget.setSizePolicy(
                qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding
            )
            self.layout_central.update()

    def closeEvent(self, event):

        self.horloge.arreter()
        event.accept()


@admin_manager.admin_mode_decorator
def main():

    def on_exit():
        print("Arrêt en cours....")
        arreter_toutes_horloges()

    # Enregistrer la fonction de nettoyage
    atexit.register(on_exit)
    global window
    app = qt.QApplication([])
    window = MainFrame()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Nettoyage avant l'arrêt du programme.")

    except SystemExit:
        print("Nettoyage avant l'arrêt du programme.")
    except Exception as e:
        print(f"il y a une erreur : {e}")
    finally:
        arreter_toutes_horloges()
        print("Le jeu s'arrête....")

        sys.exit(0)
