use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

/// Version actuelle du format des sauvegardes.
///
/// À incrémenter uniquement lorsqu'une sauvegarde devient
/// incompatible avec les anciennes versions.
pub const SAVE_FORMAT_VERSION: u32 = 1;

/// Métadonnées d'une sauvegarde.
///
/// Ce fichier est stocké en clair dans l'archive afin de
/// pouvoir vérifier la compatibilité avant le déchiffrement.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SaveMetadata {
    /// Version du format de sauvegarde.
    pub format_version: u32,

    /// Version du jeu.
    pub game_version: String,

    /// Nom du profil.
    pub profile: String,

    /// Numéro du slot.
    pub slot: u8,

    /// Date de création.
    pub created_at: DateTime<Utc>,

    /// Salt utilisé pour PBKDF2 (Base64).
    pub salt: String,

    /// Taille des données chiffrées.
    pub payload_size: u64,

    /// Checksum SHA-256 des données chiffrées.
    pub checksum: String,
}

impl SaveMetadata {
    /// Crée de nouvelles métadonnées.
    pub fn new(
        profile: String,
        slot: u8,
        salt: String,
        payload_size: u64,
        checksum: String,
    ) -> Self {
        Self {
            format_version: SAVE_FORMAT_VERSION,
            game_version: env!("CARGO_PKG_VERSION").to_string(),
            profile,
            slot,
            created_at: Utc::now(),
            salt,
            payload_size,
            checksum,
        }
    }

    /// Vérifie que la sauvegarde est compatible.
    pub fn is_compatible(&self) -> bool {
        self.format_version == SAVE_FORMAT_VERSION
    }
}
