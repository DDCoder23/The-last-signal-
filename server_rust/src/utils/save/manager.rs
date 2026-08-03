use std::fs::File;
use std::io::{Write,Read};
use log::error;
use zip::{
    ZipWriter,
    ZipArchive,
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
pub struct SaveManager {
    profile_manager: ProfileManager,
}

impl SaveManager {

    /// Crée un nouveau gestionnaire.
    pub fn new() -> Self {
    Self {
        profile_manager: ProfileManager::new(),
    }
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
        Encryption::encode_salt(
    &salt),
        Encryption::encode_nonce(&nonce),
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
    }

    /// Charge une sauvegarde.
pub fn load(
    &self,
    profile: &str,
    slot: u8,
    password: &str,
) -> SaveResult<Map<String, Value>> {

    // Vérification du slot.
    self.validate_slot(slot)?;

    // Chemin de la sauvegarde.
    let save_path =
        self.save_file(profile, slot);

    if !save_path.exists() {
        error!("Sauvegarde abscbente");
        return Err(
            SaveError::SaveNotFound,
        );
    }

    // Ouverture du fichier.
    let file =
        File::open(save_path)?;

    let mut archive =
        ZipArchive::new(file)?;

    // ============================
    // Lecture des métadonnées
    // ============================

    let metadata: SaveMetadata = {

        let mut file =
            archive.by_name(
                METADATA_FILE,
            )?;

        let mut json =
            String::new();

        file.read_to_string(
            &mut json,
        )?;

        serde_json::from_str(&json)?
    };

    // Vérification de la version.
    if !metadata.is_compatible() {
        error!("format incompatible");

        return Err(
            SaveError::InvalidFormat,
        );

    }

    // ============================
    // Lecture du payload
    // ============================

    let encrypted_payload = {

        let mut file =
            archive.by_name(
                PAYLOAD_FILE,
            )?;

        let mut payload =
            Vec::new();

        file.read_to_end(
            &mut payload,
        )?;

        payload
    };

    // Vérification de la taille.
    if encrypted_payload.len() as u64
        != metadata.payload_size
    {   error!("sauvegarde corrompue");

        return Err(
            SaveError::CorruptedSave,
        );

    }

    // Vérification du checksum.
    let checksum =
        Encryption::sha256(
            &encrypted_payload,
        );

    if checksum != metadata.checksum {
        error!("sauvegarde corompue");

        return Err(
            SaveError::CorruptedSave,
        );

    }

    // Reconstruction du salt.
    let salt =
        Encryption::decode_salt(
            &metadata.salt,
        )?;

    // Reconstruction du nonce.
    let nonce_bytes =
    Encryption::decode_nonce(
        &metadata.nonce,
    )?;

    if nonce_bytes.len()
        != AES_NONCE_SIZE
    {
        error!("sauvegarde corompue");
        return Err(
            SaveError::CorruptedSave,
        );

    }

    let mut nonce =
        [0u8; AES_NONCE_SIZE];

    nonce.copy_from_slice(
        &nonce_bytes,
    );

    // Dérivation de la clé.
    let key =
        Encryption::derive_key(
            password,
            &salt,
        )?;

    // Déchiffrement.
    let plaintext =
        Encryption::decrypt(
            &key,
            &nonce,
            &encrypted_payload,
        )?;

    // Désérialisation.
    let data =
        serde_json::from_slice::<
            Map<String, Value>,
        >(
            &plaintext,
        )?;

    Ok(data)
}

    /// Vérifie l'intégrité d'une sauvegarde.
    pub fn verify(
    &self,
    profile: &str,
    slot: u8,
) -> SaveResult<()> {

    self.validate_slot(slot)?;

    let save_path =
        self.save_file(profile, slot);

    if !save_path.exists() {
        error!("sauvegarde abscente");
        return Err(
            SaveError::SaveNotFound,
        );
    }

    let file =
        File::open(save_path)?;

    let mut archive =
        ZipArchive::new(file)?;

    // Lecture des métadonnées
    let metadata: SaveMetadata = {

        let mut file =
            archive.by_name(
                METADATA_FILE,
            )?;

        let mut json =
            String::new();

        file.read_to_string(
            &mut json,
        )?;

        serde_json::from_str(&json)?
    };

    if !metadata.is_compatible() {
        error!("sauvegarde invalide");

        return Err(
            SaveError::InvalidFormat,
        );

    }

    // Lecture du payload
    let payload = {

        let mut file =
            archive.by_name(
                PAYLOAD_FILE,
            )?;

        let mut payload =
            Vec::new();

        file.read_to_end(
            &mut payload,
        )?;

        payload
    };

    if payload.len() as u64
        != metadata.payload_size
    {    error!("sauvegarde corompue");

        return Err(
            SaveError::CorruptedSave,
        );

    }

    let checksum =
        Encryption::sha256(
            &payload,
        );

    if checksum != metadata.checksum {
        error!("sauvegarde corompue");

        return Err(
            SaveError::CorruptedSave,
        );

    }

    Ok(())
    }

    /// Supprime une sauvegarde.
    pub fn delete(
    &self,
    profile: &str,
    slot: u8,
) -> SaveResult<()> {

    self.validate_slot(slot)?;

    let save =
        self.save_file(profile, slot);

    if !save.exists() {
        error!("sauvegarde abscente");
        return Err(
            SaveError::SaveNotFound,
        );
    }

    std::fs::remove_file(save)?;

    Ok(())
    }

    /// Liste les slots disponibles.
    pub fn list_slots(
    &self,
    profile: &str,
) -> SaveResult<Vec<SaveMetadata>> {

    let mut saves = Vec::new();

    for slot in 1..=SAVE_SLOT_COUNT {

        let save =
            self.save_file(
                profile,
                slot,
            );

        if !save.exists() {
            continue;
        }

        let file =
            File::open(save)?;

        let mut archive =
            ZipArchive::new(file)?;

        let mut metadata_file =
            archive.by_name(
                METADATA_FILE,
            )?;

        let mut json =
            String::new();

        metadata_file
            .read_to_string(
                &mut json,
            )?;

        let metadata: SaveMetadata =
            serde_json::from_str(
                &json,
            )?;

        saves.push(metadata);
    }

    Ok(saves)
    }
    /// Exporte une sauvegarde.
    pub fn export(
    &self,
    profile: &str,
    slot: u8,
    destination: impl AsRef<Path>,
) -> SaveResult<()> {

    self.validate_slot(slot)?;

    let source =
        self.save_file(
            profile,
            slot,
        );

    if !source.exists() {

        return Err(
            SaveError::SaveNotFound,
        );

    }

    fs::copy(
        source,
        destination,
    )?;

    Ok(())
    }

    /// Importe une sauvegarde.
    pub fn import(
    &self,
    source: impl AsRef<Path>,
    profile: &str,
    slot: u8,
) -> SaveResult<()> {

    self.validate_slot(slot)?;

    let source =
        source.as_ref();

    if !source.exists() {

        return Err(
            SaveError::SaveNotFound,
        );

    }

    self.profile_manager.create_profile_directory(
        profile,
    )?;

    fs::copy(
        source,
        self.save_file(
            profile,
            slot,
        ),
    )?;

    Ok(())
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
    
    /// Fichier de sauvegarde.
    fn save_file(
        &self,
        profile: &str,
        slot: u8,
    ) -> PathBuf {

        self.profile_manager
    .profile_directory(profile)
            .join(format!(
                "slot{}.{}",
                slot,
                SAVE_EXTENSION
            ))
    }

    
    
}
