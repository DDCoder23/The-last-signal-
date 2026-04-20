import traceback
from debugger import debug
import PySide6.QtWidgets as qt
from PySide6.QtCore import Qt, QTimer
from functools import wraps
import json
from table_de_conversion import qtes
from inventaire import safe_increment, Objet, trier
import re
import configparser
from PySide6.QtWidgets import QMessageBox
import dill

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

mot_de_passe = config["Admin"]["password"]

IS_ADMIN = False
_console = None
_current_joueur = None

IS_ADMIN = False

_console_frame = None

def calculer_distance_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return calculer_distance_levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def trouver_commandes_similaires(commande_saisie, commandes_disponibles, seuil=0.6):
    similitudes = []
    for cmd in commandes_disponibles:
        distance = calculer_distance_levenshtein(commande_saisie, cmd)
        max_len = max(len(commande_saisie), len(cmd))
        similarite = 1 - (distance / max_len) if max_len > 0 else 0
        if similarite >= seuil:
            similitudes.append((cmd, similarite))
    similitudes.sort(key=lambda x: x[1], reverse=True)
    return [cmd for cmd, similarite in similitudes]


def admin_only(func):
    def wrapper(*args, **kwargs):
        if not IS_ADMIN:
            print(f"[ADMIN] Accès refusé : {func.__name__}")
            return None
        return func(*args, **kwargs)

    return wrapper


# =============================
# CONSOLE ADMIN wx (SIMPLE, STABLE)
# =============================
class ConsoleAdmin(qt.QWidget):
    def __init__(self, joueur, parent=None):
        super().__init__(parent)

        self.joueur = joueur
        self.contexte = {
            "joueur": joueur,
            "stuff": joueur.stuff,
        }

        self.setWindowTitle("Console Admin")
        self.resize(700, 450)
        self.setWindowFlag(Qt.Window)

        layout = qt.QVBoxLayout(self)

        self.sortie = qt.QTextEdit()
        self.sortie.setReadOnly(True)

        self.entree = qt.QLineEdit()
        self.entree.returnPressed.connect(self.executer)

        layout.addWidget(self.sortie)
        layout.addWidget(self.entree)

        self.log("[ADMIN] Console prête.\n")

        self.show()
        self.raise_()
        self.activateWindow()

    def log(self, txt):
        self.sortie.append(str(txt))

    def executer(self):
        cmd = self.entree.text().strip()
        self.entree.clear()

        if not cmd:
            return

        self.log(f">>> {cmd}")

        if cmd.startswith("/"):
            self.executer_commande(cmd[1:])
            return

        try:
            try:
                result = eval(cmd, self.contexte)
                if result is not None:
                    self.log(result)
            except SyntaxError:
                exec(cmd, self.contexte)
        except Exception:
            self.log(traceback.format_exc())

    @admin_only
    def executer_commande(self, cmd):
        parts = cmd.split()
        if not parts:
            return

        nom = parts[0]
        commandes_disponibles = [
            "help", "exit", "ban", "close", "inv", "kill", "setstat",
            "give", "gold", "clear", "tp"
        ]

        if nom == "help":
            self._cmd_help()
        elif nom == "exit":
            self._cmd_exit()
        elif nom=="ban":
            self._cmd_ban(parts[1:])
        elif nom == "close":
            self._cmd_close()
        elif nom == "inv":
            self._cmd_inv()
        elif nom == "kill":
            self._cmd_kill()
        elif nom == "setstat":
            self._cmd_setstat(parts[1:])
        elif nom == "give":
            self._cmd_give(parts[1:])
        elif nom == "gold":
            self._cmd_gold(parts[1:])
        elif nom == "clear":
            self._cmd_clear(parts[1:])

        else:
            similitudes = trouver_commandes_similaires(nom, commandes_disponibles)
            if similitudes:
                self.log(f"[ADMIN] Commande inconnue. Peut-être vouliez-vous dire : {', '.join(similitudes)}")
            else:
                self.log(f"[ADMIN] Commande inconnue : {nom}")

    def _cmd_exit(self):
        self.destroy()  # Détruit la console admin
        self.log("[ADMIN] Console détruite.")

    def _cmd_close(self):
        self.close()  # Ferme la console admin
        self.log("[ADMIN] Console fermée.")

    def _cmd_give(self, args):
        if not args:
            self.log("Usage : /give <objet> (qte)")
            return

        # Extraction de la quantité
        qty = 1
        nom_objet_avec_qty = " ".join(args)
        m = re.search(r"\((\d+)\)$", nom_objet_avec_qty)
        if m:
            qty = int(m.group(1))
            nom_objet = re.sub(r"\s*\(\d+\)$", "", nom_objet_avec_qty).strip()
        else:
            nom_objet = nom_objet_avec_qty

        # Chargement des objets disponibles
        try:
            with open("objet_dispo.json", "r", encoding="utf-8") as fichier:
                objets = json.load(fichier)
        except FileNotFoundError:
            QMessageBox.warning(
                self, "Erreur", "Le fichier objet_dispo.json est introuvable."
            )
            return
        except json.JSONDecodeError:
            QMessageBox.warning(
                self,
                "Erreur",
                "Le fichier objet_dispo.json n'est pas un fichier JSON valide.",
            )
            return

        # Extraction des noms des objets disponibles
        liste_objets = [objet["nom"] for objet in objets]

        # Vérification de l'existence de l'objet
        if nom_objet not in liste_objets:
            self.log(
                f"[ADMIN] Objet inconnu : '{nom_objet}'. Voici la liste des objets disponibles :"
            )
            for objet in liste_objets:
                self.log(f"- {objet}")
            return

        # Ajout de l'objet à l'inventaire
        safe_increment(self.joueur.stuff, nom_objet, quant=qty)
        self.log(f"[ADMIN] {nom_objet} x{qty} ajouté à l'inventaire.")

    def _cmd_gold(self, args):
        if not args:
            self.log("Usage : /gold <qte>")
            return
        try:
            qte = int(args[0])
            safe_increment(self.joueur.stuff, "argent", quant=qte)

            self.log(f"[ADMIN] Argent +{qte} ")
        except ValueError:
            self.log("Quantité invalide")
    def _cmd_ban(self,args):
        self.log(f"[ADMIN] {args[0]} a été banni pour {args[1]} {args[2]}")

    def _cmd_help(self):
        self.log(
            """
    === COMMANDES ADMIN ===

    /help
      Affiche cette aide.
    
    /ban <user> <temps> <unit>
    Banni le joueur pour une durée donnée.

    /give <objet> (qte)
      Donne un objet.

    /gold <qte>
      Ajoute de l'argent.

    /tp <user> <x> <y> 
      Téléporte le joueur.

    /stats
      Affiche les statistiques du joueur.

    /inv
      Affiche l'inventaire.
    /kill 
      Tue le joueur.
    /setstat
       Modifie une statistique

    Exemples :
      /give livre enchant 1 (1)
      /tp user 64 64 
      /inv

    ========================
    """
        )

    def _cmd_tp(self, args):
        with open(
               "joueurs.dill", "rb"
        ) as fichier:
            try:
                data = dill.load(fichier)
            except :
                data = {}
        user=args[0]
        if user=="@s":
            user=data[self.joueur.nom]
        else:
            try:
                user=data[str(user)]
            except KeyError:
                self.log("Ce joueur n'existe pas")

        if isinstance(user, object) and not isinstance(user, (int, float, str, list, dict, tuple, set, bool)):
            if hasattr(user, "x"):
                if len(args) != 3:
                    self.log("Usage : /tp <user> <x> <y> ")
                    return
                try:
                    x = float(args[1])
                    y = float(args[2])

                except ValueError:
                    self.log("Coordonnées invalides")
                    return
                user = args[0]
                if user == "@s":
                    user = self.joueur.nom
                user.x=x
                user.y=y




        # recalcul Z si possible
        parent = self.parent()
        if parent and hasattr(parent, "map"):
            user.z = parent.map.get_height(x, y)
        self.log(f" [ADMIN] {user} a été téléporté  en ({x:.2f}, {y:.2f})")



    def _cmd_inv(self):

        self.log("=== INVENTAIRE ===")
        trier(self.joueur.stuff)
        self.log(f"Argent : {qtes("argent",self.joueur)}")

        for nom, obj in self.joueur.stuff.items():
            if nom == "argent":
                continue
            if hasattr(obj, "quantite"):
                extra = ""
                if hasattr(obj, "enchant"):
                    extra += f" | enchant +{obj.enchant}"
                if hasattr(obj, "durabilite"):
                    extra += f" | dura {obj.durabilite}"
                self.log(f"{nom} x{obj.quantite}{extra}")
            else:
                self.log(f"{nom} : {obj}")
        self.log("==================")

    def _cmd_kill(self):
        self.joueur.stats["PV"] = 0
        self.joueur.vivant = False
        self.log("[ADMIN] Joueur tué 💀")
    def _cmd_clear(self,args):
        with open(
               "joueurs.dill", "rb"
        ) as fichier:
            try:
                data = dill.load(fichier)
            except :
                data = {}
        user=args[0]
        if user=="@a":
            for perso in data:
                user= []
                user.append(data[perso])

        else:
            try:
                user=data[str(user)]
            except KeyError:
                self.log("Ce joueur n'existe pas")
        for users in user:

            if isinstance(users, object) and not isinstance(users, (int, float, str, list, dict, tuple, set, bool)):
                if hasattr(users, "stuff"):
                    users.stuff={}
                self.log(f" {user} a été clear")
    def _cmd_setstat(self, args):
        if len(args) != 2:
            self.log("Usage : /setstat <STAT> <valeur>")
            return

        stat = args[0].upper()

        try:
            valeur = int(args[1])
        except ValueError:
            self.log("Valeur invalide (doit être un entier)")
            return

        if stat not in self.joueur.stats:
            self.log(f"[ADMIN] Stat inconnue : {stat}")
            return

        self.joueur.stats[stat] = valeur
        self.log(f"[ADMIN] {stat} défini à {valeur}")

        # 🔁 Recalcul des modificateurs si stat primaire
        if stat in ("FOR", "DEX", "CON", "INT", "SAG", "CHA"):
            mod = self.joueur.get_modifier(valeur)
            self.joueur.stats[f"MOD_{stat}"] = mod
            self.log(f"[ADMIN] MOD_{stat} recalculé → {mod}")

        # 🔁 Ajustement PV si CON modifiée
        if stat == "CON":
            pv_max = (valeur // 2) + 12
            self.joueur.stats["PV_MAX"] = pv_max
            self.joueur.stats["PV"] = min(self.joueur.stats["PV"], pv_max)
            self.log(f"[ADMIN] PV_MAX recalculé → {pv_max}")


# =============================
# ACTIVATION MODE ADMIN
# =============================
def activer_admin(joueur, parent=None):
    global IS_ADMIN, _console

    if IS_ADMIN:
        return

    if joueur is None:
        print("[ADMIN] Impossible : joueur non créé")
        return

    IS_ADMIN = True
    debug()

    _console = ConsoleAdmin(joueur, parent)
    print("[ADMIN] Mode admin activé")


# =============================
# MENU ADMIN
# =============================
def installer_raccourci_admin(widget, joueur):
    def keyPressEvent(event):
        if (
            event.modifiers() & Qt.ControlModifier
            and event.modifiers() & Qt.ShiftModifier
            and event.key() == Qt.Key_A
        ):
            if not IS_ADMIN:
                demander_mot_de_passe(widget, joueur)
            return
        super(widget.__class__, widget).keyPressEvent(event)

    widget.keyPressEvent = keyPressEvent


# =============================
# RACCOURCI CLAVIER
# =============================


# =============================
# MOT DE PASSE ADMIN
# =============================
def demander_mot_de_passe(joueur, parent):

    dlg = qt.QInputDialog(parent)
    dlg.setTextEchoMode(qt.QLineEdit.Password)
    dlg.setLabelText("Mot de passe admin :")

    if dlg.exec() == qt.QDialog.Accepted:
        if dlg.textValue() == mot_de_passe:
            activer_admin(joueur, parent)
        else:
            print("[ADMIN] Mot de passe incorrect")


# admin_decorator.py


def admin_mode_decorator(func):
    """
    Décorateur qui active :
      - RAMMonitor
      - Debugger unifié (SoftDebugger)
    uniquement si IS_ADMIN est True.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if IS_ADMIN:
            print("[ADMIN] Mode admin activé : RAMMonitor et Debugger activés")

            dbg = debug()
            wrapped_func = dbg.wrap(func)  # wrappe la fonction principale
            try:
                result = wrapped_func(*args, **kwargs)
            finally:
                pass  # Arrêter le RAMMonitor à la fin
            return result
        else:
            # Mode normal : exécution classique
            return func(*args, **kwargs)

    return wrapper
