//! Configuration du système de sauvegarde.

/// Version du format des sauvegardes.
pub const SAVE_FORMAT_VERSION: u32 = 1;

/// Version interne du chiffrement.
pub const ENCRYPTION_VERSION: u8 = 1;

/// Nombre de slots disponibles.
pub const SAVE_SLOT_COUNT: u8 = 3;

/// Dossier contenant toutes les sauvegardes.
pub const SAVE_DIRECTORY: &str = "saves";

/// Extension des fichiers de sauvegarde.
pub const SAVE_EXTENSION: &str = "tls";

/// Nom du fichier contenant les métadonnées.
pub const METADATA_FILE: &str = "metadata.json";

/// Nom du fichier contenant les données chiffrées.
pub const PAYLOAD_FILE: &str = "payload.bin";

/// Taille de la clé AES-256.
pub const AES_KEY_SIZE: usize = 32;

/// Taille du nonce AES-GCM.
pub const AES_NONCE_SIZE: usize = 12;

/// Taille du sel PBKDF2.
pub const SALT_SIZE: usize = 32;

/// Nombre d'itérations PBKDF2.
pub const PBKDF2_ITERATIONS: u32 = 310_000;

/// Algorithme utilisé.
pub const HASH_ALGORITHM: &str = "SHA-256";

/// Compression ZIP utilisée.
pub const ZIP_COMPRESSION_LEVEL: i64 = 9;
/// Nombre maximum de profils locaux.
pub const MAX_PROFILES: usize = 16;

/// Taille maximale d'une sauvegarde (100 Mo).
pub const MAX_SAVE_SIZE: u64 = 100 * 1024 * 1024;

/// Version minimale compatible.
pub const MIN_SUPPORTED_FORMAT: u32 = 1;

/// Version maximale compatible.
pub const MAX_SUPPORTED_FORMAT: u32 = SAVE_FORMAT_VERSION;
