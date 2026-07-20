from __future__ import annotations
from vispy import scene
import numpy as np
import PySide6.QtWidgets as qt
from PySide6.QtCore import Qt, QTimer
import atexit
import sys


class Joueur():
    def __init__(
        self, image, jeu=None, 
        nom="Player 1", 
        recommencer=True, 
        grade=None, config=None,stats={}
    ):
        super().__init__(image,  jeu)
        self.nom = nom
        self.stats=stats
        self.vivant = True
        self.stuff = {}
        self.index_arme_selectionnee = 0
        self.grade = grade
        self.config = config
        self._initialiser_stats(self.stats)

    def _initialiser_stats(self,stats:dict):
        self.stats["MANA_max"] = 100
        self.stats["MANA"] = self.stats["MANA_max"]
        self.stats["XP"] = 0
        self.stats["niv"] = 1
        self.stats["bouff_max"] = self.stats["niv"] * 10
        self.stats["bouff"] = self.stats["bouff_max"]
        
        
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
            pass
        elif key == Qt.Key_E:
            pass
        elif key == Qt.Key_I:
            pass
        elif key == Qt.Key_S:
            pass
        elif key == Qt.Key_B:
            pass

        elif key == Qt.Key_A and ctrl:
            pass
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

       
        

        
        

        self.current_widget = None
        self.show_menu()
      
    
    

    
       

    
        
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
    def start_game(self, player_name, recommencer=False,
    grade=None,
    configuration=None,
):
        
        self.clear_layout(self.layout_central)

        jeu = Jeu()

        joueur = Joueur(
            "image_joueur.jpg",
            jeu,
            grade=kwargs.get("grade", None),
            nom=player_name,
            config=kwargs.get("configuration", None),
        )
        
         
                
        

        self.current_widget = VispyWidget(self, joueur)
        self.layout_central.addWidget(self.current_widget)

        QTimer.singleShot(0, lambda: self.current_widget.canvas.native.setFocus())
        

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



def main():

    def on_exit():
        pass

    # Enregistrer la fonction de nettoyage
    atexit.register(on_exit)
    global window
    app = qt.QApplication([])
    window = MainFrame()
    window.show()
    sys.exit(app.exec())



       
