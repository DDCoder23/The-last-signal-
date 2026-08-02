use std::fs::File;
use std::io::Write;

use zip::{
    ZipWriter,
    write::SimpleFileOptions,
    CompressionMethod,
};
use std::{
    fs,
    path::{Path, PathBuf},
};

use serde_json::{Map, Value};

use crate::utils::save::{
    config::*,
    encryption::Encryption,
    errors::{
        SaveError,
        SaveResult,
    },
    metadata::SaveMetadata,
};

/// Gestionnaire principal des sauvegardes.
pub struct SaveManager;

impl SaveManager {

    /// Crée un nouveau gestionnaire.
    pub fn new() -> Self {
        Self
    }

    /// Sauvegarde des données.
    pub fn save(
    &self,
    profile: &str,
    slot: u8,
    data: &Map<String, Value>,
    password: &str,
) -> SaveResult<()> {

    // Vérifie le slot.
    self.validate_slot(slot)?;

    // Crée le dossier du profil.
    self.create_profile_directory(profile)?;

    // Sérialise les données.
    let json =
        serde_json::to_vec(data)?;

    // Génère le salt.
    let salt =
        Encryption::generate_salt();

    // Dérive la clé AES.
    let key =
        Encryption::derive_key(
            password,
            &salt,
        )?;

    // Chiffrement.
    let (
        encrypted_payload,
        nonce,
    ) =
        Encryption::encrypt(
            &key,
            &json,
        )?;
    // Calcul du checksum.
    let checksum =
    Encryption::sha256(&encrypted_payload);

    // Création des métadonnées.
    let metadata =
    SaveMetadata::new(
        profile.to_string(),
        slot,
        Encryption::encode_base64(
            salt.as_str().as_bytes(),
        ),
        Encryption::encode_base64(&nonce),
        encrypted_payload.len() as u64,
        checksum,
    );

    // Sérialisation des métadonnées.
    let metadata_json =
    serde_json::to_vec_pretty(&metadata)?;

    // Création du fichier .tls.
    let save_file =
    self.save_file(profile, slot);

    let file =
    File::create(&save_file)?;

    let mut zip =
    ZipWriter::new(file);

    let options =
    SimpleFileOptions::default()
        .compression_method(
            CompressionMethod::Deflated,
        );

     // metadata.json
    zip.start_file(
    METADATA_FILE,
    options,
)?;

zip.write_all(&metadata_json)?;

// payload.bin
zip.start_file(
    PAYLOAD_FILE,
    options,
)?;

zip.write_all(&encrypted_payload)?;

// Finalisation de l'archive.
zip.finish()?;

Ok(())

    /// Charge une sauvegarde.
    pub fn load(
        &self,
        profile: &str,
        slot: u8,
        password: &str,
    ) -> SaveResult<Map<String, Value>> {
        todo!()
    }

    /// Vérifie l'intégrité d'une sauvegarde.
    pub fn verify(
        &self,
        profile: &str,
        slot: u8,
    ) -> SaveResult<()> {
        todo!()
    }

    /// Supprime une sauvegarde.
    pub fn delete(
        &self,
        profile: &str,
        slot: u8,
    ) -> SaveResult<()> {
        todo!()
    }

    /// Liste les slots disponibles.
    pub fn list_slots(
        &self,
        profile: &str,
    ) -> SaveResult<Vec<SaveMetadata>> {
        todo!()
    }

    /// Exporte une sauvegarde.
    pub fn export(
        &self,
        profile: &str,
        slot: u8,
        destination: impl AsRef<Path>,
    ) -> SaveResult<()> {
        todo!()
    }

    /// Importe une sauvegarde.
    pub fn import(
        &self,
        source: impl AsRef<Path>,
        profile: &str,
        slot: u8,
    ) -> SaveResult<()> {
        todo!()
    }

    // ===================================================
    // Helpers privés
    // ===================================================

    /// Vérifie qu'un slot est valide.
    fn validate_slot(
        &self,
        slot: u8,
    ) -> SaveResult<()> {

        if slot == 0 || slot > SAVE_SLOT_COUNT {
            return Err(SaveError::InvalidSlot);
        }

        Ok(())
    }

    /// Dossier du profil.
    fn profile_directory(
        &self,
        profile: &str,
    ) -> PathBuf {

        Path::new(SAVE_DIRECTORY)
            .join(profile)
    }

    /// Fichier de sauvegarde.
    fn save_file(
        &self,
        profile: &str,
        slot: u8,
    ) -> PathBuf {

        self.profile_directory(profile)
            .join(format!(
                "slot{}.{}",
                slot,
                SAVE_EXTENSION
            ))
    }

    /// Crée le dossier du profil s'il n'existe pas.
    fn create_profile_directory(
        &self,
        profile: &str,
    ) -> SaveResult<()> {

        fs::create_dir_all(
            self.profile_directory(profile),
        )?;

        Ok(())
    }
}
