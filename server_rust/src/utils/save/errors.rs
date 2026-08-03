use std::{fmt, io};

use serde_json;
use zip::result::ZipError;

/// Type de retour utilisé dans tout le système de sauvegarde.
pub type SaveResult<T> = Result<T, SaveError>;

#[derive(Debug)]
pub enum SaveError {
    /// Slot invalide.
    InvalidSlot,

    /// Profil inexistant.
    ProfileNotFound,

    /// Sauvegarde inexistante.
    SaveNotFound,

    /// Mot de passe incorrect.
    InvalidPassword,

    /// Sauvegarde corrompue.
    CorruptedSave,

    /// Version du format inconnue.
    InvalidFormat,

    /// Erreur cryptographique.
    Crypto(String),

    /// Erreur d'entrée/sortie.
    Io(io::Error),

    /// Erreur JSON.
    Json(serde_json::Error),

    /// Erreur ZIP.
    Zip(ZipError),
    InvalidNonce,

    /// Toute autre erreur.
    Other(String),
}

impl fmt::Display for SaveError {
    fn fmt(
        &self,
        f: &mut fmt::Formatter<'_>,
    ) -> fmt::Result {

        match self { 
            SaveError::InvalidNonce => write!(f,"Nonce invalide"),

            SaveError::InvalidSlot =>
                write!(f, "Le slot est invalide."),

            SaveError::ProfileNotFound =>
                write!(f, "Le profil est introuvable."),

            SaveError::SaveNotFound =>
                write!(f, "La sauvegarde est introuvable."),

            SaveError::InvalidPassword =>
                write!(f, "Mot de passe incorrect."),

            SaveError::CorruptedSave =>
                write!(f, "La sauvegarde est corrompue."),

            SaveError::InvalidFormat =>
                write!(f, "Version du format de sauvegarde inconnue."),

            SaveError::Crypto(msg) =>
                write!(f, "Erreur cryptographique : {}", msg),

            SaveError::Io(err) =>
                write!(f, "Erreur IO : {}", err),

            SaveError::Json(err) =>
                write!(f, "Erreur JSON : {}", err),

            SaveError::Zip(err) =>
                write!(f, "Erreur ZIP : {}", err),

            SaveError::Other(msg) =>
                write!(f, "{}", msg),
        }
    }
}

impl std::error::Error for SaveError {}

impl From<io::Error> for SaveError {
    fn from(err: io::Error) -> Self {
        SaveError::Io(err)
    }
}

impl From<serde_json::Error> for SaveError {
    fn from(err: serde_json::Error) -> Self {
        SaveError::Json(err)
    }
}

impl From<ZipError> for SaveError {
    fn from(err: ZipError) -> Self {
        SaveError::Zip(err)
    }
}

impl From<String> for SaveError {
    fn from(err: String) -> Self {
        SaveError::Other(err)
    }
}

impl From<&str> for SaveError {
    fn from(err: &str) -> Self {
        SaveError::Other(err.to_string())
    }
}
