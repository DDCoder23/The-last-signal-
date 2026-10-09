from __future__ import annotations

import queue
import struct
import threading
import uuid
from pathlib import Path

import numpy as np
from PIL import Image
from vispy import app, scene
from vispy.scene import visuals

from .client import Client
from .packet import PacketType
from .packets.move import MovePacket


class Game(scene.SceneCanvas):
    """Client 3D de The Last Signal avec terrain découpé en chunks."""

    # ==============================================================
    # WORLD
    # ==============================================================

    WORLD_WIDTH = 1000.0
    WORLD_DEPTH = 1000.0
    WORLD_HEIGHT = 120.0

    # Taille maximale de la heightmap après réduction.
    MAX_TERRAIN_SIZE = 512

    # Taille d'un chunk en unités du monde.
    CHUNK_SIZE = 64.0

    # Nombre de chunks dans chaque direction autour du joueur.
    # 2 = jusqu'à 25 chunks actifs.
    RENDER_DISTANCE = 2

    # Caméra et joueur.
    PLAYER_HEIGHT = 2.0
    PLAYER_SPEED = 5.0

    # Réseau.
    NETWORK_QUEUE_LIMIT = 100

    # Joueurs distants.
    REMOTE_PLAYER_RADIUS = 2.0
    REMOTE_PLAYER_SIZE = 14

    # ==============================================================
    # INITIALIZATION
    # ==============================================================

    def __init__(self, client: Client):
        super().__init__(
            keys="interactive",
            title="The Last Signal",
            size=(1280, 720),
            bgcolor="black",
        )

        self.unfreeze()

        self.client = client
        self.running = True

        # Position initiale côté serveur.
        self.local_x = 100.0
        self.local_y = 100.0
        self.local_z = 0.0

        # Joueurs distants.
        self.remote_players: dict[
            uuid.UUID, tuple[int, int, int]
        ] = {}

        self.remote_visuals: dict[
            uuid.UUID, visuals.Markers
        ] = {}

        # ==========================================================
        # NETWORK
        # ==========================================================

        self.network_queue: queue.Queue = queue.Queue(
            maxsize=self.NETWORK_QUEUE_LIMIT
        )

        self.network_thread = threading.Thread(
            target=self._network_loop,
            name="GameNetworkThread",
            daemon=True,
        )

        # ==========================================================
        # SCENE AND CAMERA
        # ==============================================================

        self.view = self.central_widget.add_view()

        self.view.camera = scene.cameras.FlyCamera(
            fov=70.0,
            up="y",
            parent=self.view.scene,
        )

        self.camera = self.view.camera
        self.camera.scale_factor = self.PLAYER_SPEED
        self.camera.auto_roll = False

        # ==========================================================
        # TERRAIN DATA
        # ==============================================================

        self.heightmap: np.ndarray | None = None
        self.color_map: np.ndarray | None = None

        # (chunk_x, chunk_z) -> maillage VisPy.
        self.terrain_chunks: dict[
            tuple[int, int], visuals.Mesh
        ] = {}

        self._last_chunk_center: tuple[int, int] | None = None

        self._load_terrain()
        self._place_camera_initially()
        self._update_terrain_chunks()

        # ==========================================================
        # TIMER
        # ==============================================================

        self.timer = app.Timer(
            interval=1.0 / 60.0,
            connect=self._update,
            start=True,
        )

        # ==========================================================
        # EVENTS
        # ==============================================================

        self.events.key_press.connect(self._on_key_press)
        self.events.key_release.connect(self._on_key_release)
        self.events.mouse_press.connect(self._on_mouse_press)

        # ==========================================================
        # NETWORK THREAD
        # ==============================================================

        self.network_thread.start()

    # ==============================================================
    # ASSETS
    # ==============================================================

    def _assets_directory(self) -> Path:
        """Retourne le dossier assets du projet."""

        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent

        assets = project_root / "assets"

        if assets.is_dir():
            return assets

        fallback = Path("assets")

        if fallback.is_dir():
            return fallback

        raise FileNotFoundError(
            "Dossier assets introuvable. "
            f"Chemin recherché : {assets}"
        )

    # ==============================================================
    # TERRAIN DATA
    # ==============================================================

    def _load_terrain(self) -> None:
        """
        Charge les données du terrain en mémoire.

        Aucun maillage global n'est créé ici. Les maillages seront
        construits uniquement pour les chunks proches du joueur.
        """

        assets = self._assets_directory()

        height_path = assets / "map_height.png"
        color_path = assets / "map_color.png"

        if not height_path.is_file():
            raise FileNotFoundError(
                f"Heightmap introuvable : {height_path}"
            )

        print(f"[GAME] Chargement heightmap : {height_path}")

        with Image.open(height_path) as image:
            height_image = image.convert("L")
            height = np.asarray(
                height_image,
                dtype=np.float32,
            ).copy()

        if height.ndim != 2 or min(height.shape) < 2:
            raise ValueError(
                "map_height.png doit être une image "
                "en niveaux de gris d'au moins 2 x 2 pixels."
            )

        # Normalisation entre 0 et 1.
        height_min = float(height.min())
        height_max = float(height.max())

        if height_max > height_min:
            height = (
                (height - height_min)
                / (height_max - height_min)
            )
        else:
            height.fill(0.0)

        # Réduction facultative de la résolution.
        height = self._downsample_height(height)

        self.heightmap = height

        terrain_height, terrain_width = height.shape

        # Chargement des couleurs à la même résolution.
        if color_path.is_file():
            print(f"[GAME] Chargement couleurs : {color_path}")

            with Image.open(color_path) as image:
                color_image = image.convert("RGB")
                color_image = color_image.resize(
                    (terrain_width, terrain_height),
                    Image.Resampling.BILINEAR,
                )

                self.color_map = (
                    np.asarray(
                        color_image,
                        dtype=np.float32,
                    )
                    / 255.0
                )
        else:
            self.color_map = None

            print(
                "[GAME] map_color.png absent : "
                "couleur verte par défaut."
            )

        print(
            f"[GAME] Données terrain : "
            f"{terrain_width} x {terrain_height}"
        )

        print(
            f"[GAME] Taille des chunks : "
            f"{self.CHUNK_SIZE:.0f} x "
            f"{self.CHUNK_SIZE:.0f}"
        )

    def _downsample_height(
        self,
        height: np.ndarray,
    ) -> np.ndarray:
        """Réduit la résolution si la heightmap est trop grande."""

        h, w = height.shape

        if max(h, w) <= self.MAX_TERRAIN_SIZE:
            return height

        scale = max(h, w) / self.MAX_TERRAIN_SIZE

        new_w = max(2, int(round(w / scale)))
        new_h = max(2, int(round(h / scale)))

        image = Image.fromarray(
            np.uint8(np.clip(height, 0.0, 1.0) * 255.0),
        )

        image = image.resize(
            (new_w, new_h),
            Image.Resampling.BILINEAR,
        )

        return (
            np.asarray(image, dtype=np.float32)
            / 255.0
        )

    # ==============================================================
    # MESH HELPERS
    # ==============================================================

    @staticmethod
    def _build_faces(
        width: int,
        height: int,
    ) -> np.ndarray:
        """Construit deux triangles pour chaque cellule du maillage."""

        if width < 2 or height < 2:
            return np.empty((0, 3), dtype=np.uint32)

        grid = np.arange(
            width * height,
            dtype=np.uint32,
        ).reshape(height, width)

        a = grid[:-1, :-1].ravel()
        b = grid[:-1, 1:].ravel()
        c = grid[1:, :-1].ravel()
        d = grid[1:, 1:].ravel()

        faces = np.empty(
            (a.size * 2, 3),
            dtype=np.uint32,
        )

        faces[0::2] = np.column_stack((a, b, c))
        faces[1::2] = np.column_stack((b, d, c))

        return faces

    def _chunk_counts(self) -> tuple[int, int]:
        """Nombre de chunks sur les axes X et Z."""

        count_x = int(
            np.ceil(self.WORLD_WIDTH / self.CHUNK_SIZE)
        )

        count_z = int(
            np.ceil(self.WORLD_DEPTH / self.CHUNK_SIZE)
        )

        return count_x, count_z

    def _chunk_coordinates(
        self,
        world_x: float,
        world_z: float,
    ) -> tuple[int, int]:
        """Convertit une position du monde en coordonnées de chunk."""

        count_x, count_z = self._chunk_counts()

        chunk_x = int(
            np.floor(
                (world_x + self.WORLD_WIDTH / 2.0)
                / self.CHUNK_SIZE
            )
        )

        chunk_z = int(
            np.floor(
                (world_z + self.WORLD_DEPTH / 2.0)
                / self.CHUNK_SIZE
            )
        )

        return (
            int(np.clip(chunk_x, 0, count_x - 1)),
            int(np.clip(chunk_z, 0, count_z - 1)),
        )

    # ==============================================================
    # CHUNK MESH CREATION
    # ==============================================================

    def _create_terrain_chunk(
        self,
        chunk_x: int,
        chunk_z: int,
    ) -> visuals.Mesh | None:
        """Construit un seul chunk du terrain."""

        if self.heightmap is None:
            return None

        heightmap = self.heightmap
        map_height, map_width = heightmap.shape

        # Limites mondiales du chunk.
        world_x0 = (
            -self.WORLD_WIDTH / 2.0
            + chunk_x * self.CHUNK_SIZE
        )

        world_z0 = (
            -self.WORLD_DEPTH / 2.0
            + chunk_z * self.CHUNK_SIZE
        )

        world_x1 = min(
            world_x0 + self.CHUNK_SIZE,
            self.WORLD_WIDTH / 2.0,
        )

        world_z1 = min(
            world_z0 + self.CHUNK_SIZE,
            self.WORLD_DEPTH / 2.0,
        )

        # Conversion des limites mondiales en indices de heightmap.
        col0 = int(round(
            (world_x0 + self.WORLD_WIDTH / 2.0)
            / self.WORLD_WIDTH
            * (map_width - 1)
        ))

        col1 = int(round(
            (world_x1 + self.WORLD_WIDTH / 2.0)
            / self.WORLD_WIDTH
            * (map_width - 1)
        ))

        row0 = int(round(
            (world_z0 + self.WORLD_DEPTH / 2.0)
            / self.WORLD_DEPTH
            * (map_height - 1)
        ))

        row1 = int(round(
            (world_z1 + self.WORLD_DEPTH / 2.0)
            / self.WORLD_DEPTH
            * (map_height - 1)
        ))

        col0 = int(np.clip(col0, 0, map_width - 2))
        col1 = int(np.clip(col1, col0 + 1, map_width - 1))

        row0 = int(np.clip(row0, 0, map_height - 2))
        row1 = int(np.clip(row1, row0 + 1, map_height - 1))

        heights = heightmap[
            row0:row1 + 1,
            col0:col1 + 1,
        ]

        rows, cols = heights.shape

        # Coordonnées calculées à partir des indices réels :
        # les sommets des chunks voisins coïncident exactement.
        x = (
            -self.WORLD_WIDTH / 2.0
            + np.arange(col0, col1 + 1, dtype=np.float32)
            / (map_width - 1)
            * self.WORLD_WIDTH
        )

        z = (
            -self.WORLD_DEPTH / 2.0
            + np.arange(row0, row1 + 1, dtype=np.float32)
            / (map_height - 1)
            * self.WORLD_DEPTH
        )

        xx, zz = np.meshgrid(x, z)
        yy = heights * self.WORLD_HEIGHT

        vertices = np.column_stack((
            xx.ravel(),
            yy.ravel(),
            zz.ravel(),
        )).astype(np.float32)

        faces = self._build_faces(cols, rows)

        # Couleurs du chunk.
        if self.color_map is not None:
            rgb = self.color_map[
                row0:row1 + 1,
                col0:col1 + 1,
            ].reshape(-1, 3)

            alpha = np.ones(
                (rgb.shape[0], 1),
                dtype=np.float32,
            )

            colors = np.concatenate(
                (rgb, alpha),
                axis=1,
            )
        else:
            colors = np.empty(
                (rows * cols, 4),
                dtype=np.float32,
            )

            colors[:, 0] = 0.25
            colors[:, 1] = 0.55
            colors[:, 2] = 0.25
            colors[:, 3] = 1.0

        return visuals.Mesh(
            vertices=vertices,
            faces=faces,
            vertex_colors=colors,
            shading="smooth",
            parent=self.view.scene,
        )

    # ==============================================================
    # CHUNK STREAMING
    # ==============================================================

    def _update_terrain_chunks(self) -> None:
        """Charge les chunks proches et décharge les autres."""

        if self.heightmap is None:
            return

        center = self.camera.center

        if center is None:
            return

        try:
            world_x = float(center[0])
            world_z = float(center[2])
        except (TypeError, ValueError, IndexError):
            return

        center_chunk = self._chunk_coordinates(
            world_x,
            world_z,
        )

        # Inutile de recalculer la zone si le joueur n'a pas
        # changé de chunk.
        if center_chunk == self._last_chunk_center:
            return

        self._last_chunk_center = center_chunk

        cx, cz = center_chunk
        count_x, count_z = self._chunk_counts()

        wanted: set[tuple[int, int]] = set()

        for dx in range(
            -self.RENDER_DISTANCE,
            self.RENDER_DISTANCE + 1,
        ):
            for dz in range(
                -self.RENDER_DISTANCE,
                self.RENDER_DISTANCE + 1,
            ):
                x = cx + dx
                z = cz + dz

                if 0 <= x < count_x and 0 <= z < count_z:
                    wanted.add((x, z))

        # Décharger les chunks éloignés.
        for key in list(self.terrain_chunks):
            if key not in wanted:
                mesh = self.terrain_chunks.pop(key)
                mesh.parent = None

        # Charger les chunks manquants.
        for key in sorted(wanted):
            if key in self.terrain_chunks:
                continue

            mesh = self._create_terrain_chunk(*key)

            if mesh is not None:
                self.terrain_chunks[key] = mesh

        print(
            f"[GAME] Chunk central : {center_chunk} | "
            f"Chunks actifs : {len(self.terrain_chunks)}"
        )

    # ==============================================================
    # CAMERA
    # ==============================================================

    def _place_camera_initially(self) -> None:
        """Positionne initialement la caméra au-dessus du terrain."""

        world_x = self._server_x_to_world(self.local_x)
        world_z = self._server_y_to_world(self.local_y)

        terrain_y = self._terrain_height_at(
            world_x,
            world_z,
        )

        self.camera.center = (
            world_x,
            terrain_y + self.PLAYER_HEIGHT,
            world_z,
        )

        print(
            "[GAME] Position initiale : "
            f"({world_x:.1f}, "
            f"{terrain_y + self.PLAYER_HEIGHT:.1f}, "
            f"{world_z:.1f})"
        )

    def _update_camera_position(self) -> None:
        """Maintient le point central de la caméra au-dessus du terrain."""

        center = self.camera.center

        if center is None:
            return

        try:
            x = float(center[0])
            z = float(center[2])
        except (TypeError, ValueError, IndexError):
            return

        terrain_y = self._terrain_height_at(x, z)

        self.camera.center = (
            x,
            terrain_y + self.PLAYER_HEIGHT,
            z,
        )

    def _terrain_height_at(
        self,
        world_x: float,
        world_z: float,
    ) -> float:
        """Interpole la hauteur du terrain à une position mondiale."""

        if self.heightmap is None:
            return 0.0

        height, width = self.heightmap.shape

        normalized_x = float(np.clip(
            (world_x + self.WORLD_WIDTH / 2.0)
            / self.WORLD_WIDTH,
            0.0,
            1.0,
        ))

        normalized_z = float(np.clip(
            (world_z + self.WORLD_DEPTH / 2.0)
            / self.WORLD_DEPTH,
            0.0,
            1.0,
        ))

        px = normalized_x * (width - 1)
        pz = normalized_z * (height - 1)

        x0 = int(np.floor(px))
        z0 = int(np.floor(pz))

        x1 = min(x0 + 1, width - 1)
        z1 = min(z0 + 1, height - 1)

        fx = px - x0
        fz = pz - z0

        h00 = float(self.heightmap[z0, x0])
        h10 = float(self.heightmap[z0, x1])
        h01 = float(self.heightmap[z1, x0])
        h11 = float(self.heightmap[z1, x1])

        h0 = h00 * (1.0 - fx) + h10 * fx
        h1 = h01 * (1.0 - fx) + h11 * fx

        value = h0 * (1.0 - fz) + h1 * fz

        return value * self.WORLD_HEIGHT

    # ==============================================================
    # COORDINATE CONVERSION
    # ==============================================================

    def _server_x_to_world(self, x: float) -> float:
        """Serveur X -> VisPy X."""

        return x - self.WORLD_WIDTH / 2.0

    def _server_y_to_world(self, y: float) -> float:
        """Serveur Y horizontal -> VisPy Z."""

        return y - self.WORLD_DEPTH / 2.0

    def _world_x_to_server(self, x: float) -> int:
        return int(round(x + self.WORLD_WIDTH / 2.0))

    def _world_z_to_server(self, z: float) -> int:
        return int(round(z + self.WORLD_DEPTH / 2.0))

    # ==============================================================
    # NETWORK RECEIVE THREAD
    # ==============================================================

    def _network_loop(self) -> None:
        """Reçoit les paquets sans bloquer la boucle graphique."""

        try:
            print("[GAME] Connexion au serveur...")
            self.client.connect()
            print("[GAME] Connecté au serveur.")
        except Exception as exc:
            if self.running:
                print(f"[GAME] Connexion impossible : {exc}")
            return

        while self.running:
            try:
                if not self.client.connected:
                    break

                packet = self.client.receive_packet()

                if packet is None:
                    continue

                try:
                    self.network_queue.put_nowait(packet)
                except queue.Full:
                    # La file est pleine : supprimer le paquet le
                    # plus ancien pour garder les données récentes.
                    try:
                        self.network_queue.get_nowait()
                    except queue.Empty:
                        pass

                    try:
                        self.network_queue.put_nowait(packet)
                    except queue.Full:
                        pass

            except Exception as exc:
                if self.running:
                    print(f"[GAME] Erreur réseau : {exc}")
                break

    # ==============================================================
    # NETWORK PACKET PROCESSING
    # ==============================================================

    def _process_network_queue(self) -> None:
        """Traite les paquets sur le thread graphique."""

        for _ in range(100):
            try:
                packet = self.network_queue.get_nowait()
            except queue.Empty:
                break

            try:
                self._handle_packet(packet)
            except Exception as exc:
                print(f"[GAME] Erreur de traitement réseau : {exc}")

    def _handle_packet(self, packet) -> None:
        """Distribue les paquets selon leur type."""

        packet_type = getattr(packet, "packet_type", None)
        payload = getattr(packet, "payload", b"")

        if packet_type is None:
            packet_type = getattr(packet, "type", None)

        if packet_type == PacketType.SESSION:
            self._handle_session(payload)

        elif packet_type == PacketType.PLAYER_STATE:
            self._handle_player_state(payload)

        elif packet_type == PacketType.PLAYER_REMOVE:
            self._handle_player_remove(payload)

    def _handle_session(self, payload: bytes) -> None:
        """Traite le paquet SESSION contenant un UUID de 16 octets."""

        if len(payload) != 16:
            print(
                f"[GAME] SESSION invalide : {len(payload)} octets"
            )
            return

        try:
            session_id = uuid.UUID(bytes=payload)
            self.client.session_id = session_id
            print(f"[GAME] Session : {session_id}")
        except (ValueError, AttributeError, TypeError) as exc:
            print(f"[GAME] SESSION invalide : {exc}")

    def _handle_player_state(self, payload: bytes) -> None:
        """Traite UUID + x/y/z sous forme de trois entiers signés."""

        if len(payload) != 28:
            print(
                "[GAME] PLAYER_STATE invalide : "
                f"{len(payload)} octets"
            )
            return

        try:
            player_id = uuid.UUID(bytes=payload[:16])
            x, y, z = struct.unpack("!iii", payload[16:28])
        except (ValueError, struct.error):
            print("[GAME] PLAYER_STATE invalide.")
            return

        local_id = self._get_local_player_id()

        if local_id is not None and player_id == local_id:
            self.local_x = float(x)
            self.local_y = float(y)
            self.local_z = float(z)
            return

        self.remote_players[player_id] = (x, y, z)

        self._create_or_update_remote_player(
            player_id,
            x,
            y,
            z,
        )

    def _handle_player_remove(self, payload: bytes) -> None:
        """Supprime un joueur distant."""

        if len(payload) != 16:
            print(
                "[GAME] PLAYER_REMOVE invalide : "
                f"{len(payload)} octets"
            )
            return

        try:
            player_id = uuid.UUID(bytes=payload)
        except ValueError:
            print("[GAME] UUID PLAYER_REMOVE invalide.")
            return

        self.remote_players.pop(player_id, None)

        visual = self.remote_visuals.pop(player_id, None)

        if visual is not None:
            visual.parent = None

        print(f"[GAME] Joueur supprimé : {player_id}")

    def _get_local_player_id(self) -> uuid.UUID | None:
        """Retourne l'identifiant de session local."""

        session_id = getattr(self.client, "session_id", None)

        if session_id is None:
            return None

        if isinstance(session_id, uuid.UUID):
            return session_id

        try:
            return uuid.UUID(str(session_id))
        except (ValueError, TypeError, AttributeError):
            return None

    # ==============================================================
    # REMOTE PLAYERS
    # ==============================================================

    def _create_or_update_remote_player(
        self,
        player_id: uuid.UUID,
        x: int,
        y: int,
        z: int,
    ) -> None:
        """Crée ou met à jour le marqueur d'un joueur distant."""

        world_x = self._server_x_to_world(x)
        world_z = self._server_y_to_world(y)

        terrain_y = self._terrain_height_at(
            world_x,
            world_z,
        )

        # Le serveur reste la source de la position verticale.
        # Le terrain sert de solution de repli si Z vaut zéro.
        world_y = (
            float(z)
            if z != 0
            else terrain_y + self.REMOTE_PLAYER_RADIUS
        )

        position = np.array(
            [[world_x, world_y, world_z]],
            dtype=np.float32,
        )

        visual = self.remote_visuals.get(player_id)

        if visual is None:
            visual = visuals.Markers(
                pos=position,
                size=self.REMOTE_PLAYER_SIZE,
                face_color="red",
                edge_color="white",
                parent=self.view.scene,
            )

            self.remote_visuals[player_id] = visual
        else:
            visual.set_data(
                pos=position,
                size=self.REMOTE_PLAYER_SIZE,
                face_color="red",
                edge_color="white",
            )

    # ==============================================================
    # MOVEMENT AND SERVER SYNCHRONIZATION
    # ==============================================================

    def _sync_camera_to_server(self) -> None:
        """Envoie les changements de position au serveur."""

        center = self.camera.center

        if center is None:
            return

        try:
            world_x = float(center[0])
            world_z = float(center[2])
        except (TypeError, ValueError, IndexError):
            return

        server_x = self._world_x_to_server(world_x)
        server_y = self._world_z_to_server(world_z)

        server_x = max(
            0,
            min(int(self.WORLD_WIDTH), server_x),
        )

        server_y = max(
            0,
            min(int(self.WORLD_DEPTH), server_y),
        )

        if (
            server_x == int(self.local_x)
            and server_y == int(self.local_y)
        ):
            return

        self.local_x = float(server_x)
        self.local_y = float(server_y)

        self._send_position_to_server(
            server_x,
            server_y,
            int(self.local_z),
        )

    def _send_position_to_server(
        self,
        x: int,
        y: int,
        z: int,
    ) -> None:
        """Envoie un paquet MOVE."""

        try:
            if not self.client.connected:
                return

            packet = MovePacket(
                int(x),
                int(y),
                int(z),
            )

            self.client.send_packet(packet)

        except Exception as exc:
            print(f"[GAME] Impossible d'envoyer MOVE : {exc}")

    # ==============================================================
    # GAME LOOP
    # ==============================================================

    def _update(self, event) -> None:
        """Boucle principale exécutée sur le thread VisPy."""

        if not self.running:
            return

        self._process_network_queue()
        self._update_camera_position()
        self._update_terrain_chunks()
        self._sync_camera_to_server()

        self.update()

    # ==============================================================
    # INPUT
    # ==============================================================

    def _on_key_press(self, event) -> None:
        """Traite les touches supplémentaires."""

        key = getattr(event, "key", None)

        if key is None:
            return

        key_name = str(
            getattr(key, "name", key)
        ).lower()

        if key_name == "escape":
            self.close()

    def _on_key_release(self, event) -> None:
        """Réservé aux contrôles personnalisés."""

        pass

    def _on_mouse_press(self, event) -> None:
        """La caméra gère les interactions souris."""

        pass

    # ==============================================================
    # SHUTDOWN
    # ==============================================================

    def on_close(self, event) -> None:
        """Arrête proprement le client et son thread réseau."""

        if not self.running:
            return

        self.running = False

        print("[GAME] Arrêt du client 3D...")

        try:
            self.timer.stop()
        except Exception:
            pass

        # Déconnecter le client débloque normalement la réception.
        try:
            if self.client.connected:
                self.client.disconnect("Arrêt normal")
        except Exception as exc:
            print(f"[GAME] Erreur déconnexion : {exc}")

        if (
            self.network_thread.is_alive()
            and threading.current_thread() is not self.network_thread
        ):
            self.network_thread.join(timeout=1.0)

        print("[GAME] Client 3D arrêté.")


def run_game(client: Client | None = None) -> None:
    """Lance le client 3D."""

    if client is None:
        client = Client()

    game = Game(client)
    game.show()

    app.run()
