use std::{
    fs::{self, File, OpenOptions},
    io::{self, Read, Write},
    path::{Path, PathBuf},
    sync::{Arc, Mutex},
    thread,
    time::Duration,
};

use aes_gcm::{
    aead::{Aead, KeyInit, OsRng},
    Aes256Gcm, Nonce,
};
use pbkdf2::{
    password_hash::PasswordHasher,
    Pbkdf2,
};
use sha2::Sha256;
use base64::{engine::general_purpose, Engine as _};
use serde_json::{json, Value, Map};
use zip::{write::FileOptions, ZipArchive, ZipWriter};
use chrono::Utc;
use unicode_normalization::UnicodeNormalization;
use tempfile::NamedTempFile;

// --- Constantes ---
const BASE_SAVE_DIR: &str = "saves";
const SLOTS: [u8; 3] = [1, 2, 3];
const KDF_ITERATIONS: u32 = 310_000;
const AES_KEY_SIZE: usize = 32; // 256 bits
const AES_GCM_NONCE_SIZE: usize = 12;
const FORMAT_VERSION: &[u8] = &[0x01];

// --- Fonctions utilitaires ---

/// Normalise le mot de passe (équivalent à `unicodedata.normalize("NFKC", password)`)
fn normalize_password(password: &str) -> String {
    password.nfkc().collect::<String>()
}

/// Dérive une clé AES à partir d'un mot de passe et d'un salt
fn derive_key(password: &str, salt: &[u8]) -> Vec<u8> {
    let password_bytes = normalize_password(password).as_bytes();
    let mut key = vec![0u8; AES_KEY_SIZE];

    // Utilisation de PBKDF2 avec SHA-256
    let hash_result = Pbkdf2
        .hash_password_customized(
            password_bytes,
            None,
            None,
            pbkdf2::Params {
                rounds: KDF_ITERATIONS,
                output_length: AES_KEY_SIZE,
            },
            salt,
        )
        .expect("Échec de la dérivation de la clé");

    key.copy_from_slice(hash_result.hash.unwrap().as_bytes());
    key
}

/// Chiffre des données avec AES-GCM
fn aesgcm_encrypt(aes_key: &[u8], plaintext: &[u8]) -> Vec<u8> {
    let nonce = OsRng.generate_nonce();
    let cipher = Aes256Gcm::new_from_slice(aes_key).expect("Clé AES invalide");
    let ciphertext = cipher
        .encrypt(&nonce, plaintext)
        .expect("Échec du chiffrement");

    let mut result = Vec::new();
    result.extend_from_slice(FORMAT_VERSION);
    result.extend_from_slice(&nonce);
    result.extend_from_slice(&ciphertext);
    result
}

/// Déchiffre des données avec AES-GCM
fn aesgcm_decrypt(aes_key: &[u8], blob: &[u8]) -> Result<Vec<u8>, String> {
    if blob[0] != FORMAT_VERSION[0] {
        return Err("Format inconnu.".to_string());
    }

    let nonce = Nonce::from_slice(&blob[1..1 + AES_GCM_NONCE_SIZE]);
    let ciphertext = &blob[1 + AES_GCM_NONCE_SIZE..];
    let cipher = Aes256Gcm::new_from_slice(aes_key).expect("Clé AES invalide");

    cipher
        .decrypt(nonce, ciphertext)
        .map_err(|_| "Mot de passe incorrect ou fichier corrompu.".to_string())
}

/// Crée le répertoire du profil s'il n'existe pas
fn ensure_profile_dir(profile: &str) -> PathBuf {
    let path = Path::new(BASE_SAVE_DIR).join(profile);
    fs::create_dir_all(&path).expect("Impossible de créer le répertoire de sauvegarde");
    path
}

/// Écrit un fichier ZIP de manière atomique
fn atomic_write_zip<F>(final_path: &Path, write_fn: F) -> io::Result<()>
where
    F: FnOnce(&mut ZipWriter<File>),
{
    let directory = final_path.parent().expect("Le chemin final doit avoir un parent");
    let temp_file = NamedTempFile::new_in(directory)?;
    let temp_path = temp_file.path();

    {
        let file = OpenOptions::new()
            .write(true)
            .truncate(true)
            .open(temp_path)?;
        let mut zip_writer = ZipWriter::new(file);
        write_fn(&mut zip_writer);
        zip_writer.finish()?;
    }

    fs::rename(temp_path, final_path)?;
    Ok(())
}

/// Journalise un événement de sauvegarde
fn log_save_event(profile: &str, slot: u8, status: &str, message: Option<&str>) {
    let base_dir = ensure_profile_dir(profile);
    let log_path = base_dir.join("save.log");

    let timestamp = Utc::now().format("%Y-%m-%dT%H:%M:%SZ").to_string();
    let mut line = format!("[{}] SLOT={} STATUS={}", timestamp, slot, status);

    if let Some(msg) = message {
        line.push_str(&format!(" MESSAGE={}", msg));
    }
    line.push('\n');

    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_path)
        .unwrap_or_else(|_| panic!("Impossible d'ouvrir le fichier de log: {}", log_path.display()));

    file.write_all(line.as_bytes())
        .unwrap_or_else(|_| panic!("Impossible d'écrire dans le fichier de log: {}", log_path.display()));
}

// --- Fonctions principales ---

/// Sauvegarde les données dans un slot donné
pub fn save_to_slot(profile: &str, slot: u8, data: Map<String, Value>, password: &str) -> Result<(), String> {
    if !SLOTS.contains(&slot) {
        return Err("Slot doit être 1, 2 ou 3.".to_string());
    }

    let profile_path = ensure_profile_dir(profile);
    let zip_path = profile_path.join(format!("slot{}.zip", slot));

    let mut payload = data;
    payload.insert(
        "saved_at".to_string(),
        Value::String(Utc::now().format("%Y-%m-%dT%H:%M:%SZ").to_string()),
    );

    let raw = serde_json::to_vec(&payload).map_err(|e| format!("Échec de la sérialisation JSON: {}", e))?;
    let salt = OsRng.generate_nonce();
    let aes_key = derive_key(password, &salt);
    let cipher_blob = aesgcm_encrypt(&aes_key, &raw);

    atomic_write_zip(&zip_path, |zip_writer| {
        let options = FileOptions::default().compression_method(zip::CompressionMethod::Deflated);

        zip_writer
            .start_file("payload.bin", options)
            .expect("Impossible de démarrer le fichier payload.bin");
        zip_writer
            .write_all(&cipher_blob)
            .expect("Impossible d'écrire dans payload.bin");

        let meta = json!({
            "salt": general_purpose::STANDARD.encode(salt),
            "saved_at": payload["saved_at"],
        });

        zip_writer
            .start_file("meta.json", options)
            .expect("Impossible de démarrer le fichier meta.json");
        zip_writer
            .write_all(meta.to_string().as_bytes())
            .expect("Impossible d'écrire dans meta.json");
    })
    .map_err(|e| format!("Erreur lors de l'écriture du ZIP: {}", e))?;

    Ok(())
}

/// Charge les données depuis un slot donné
pub fn load_from_slot(profile: &str, slot: u8, password: &str) -> Result<Map<String, Value>, String> {
    if !SLOTS.contains(&slot) {
        return Err("Slot doit être 1, 2 ou 3.".to_string());
    }

    let zip_path = Path::new(BASE_SAVE_DIR).join(profile).join(format!("slot{}.zip", slot));
    if !zip_path.exists() {
        return Err("Aucune sauvegarde trouvée.".to_string());
    }

    let file = File::open(&zip_path).map_err(|_| "Impossible d'ouvrir le fichier ZIP.".to_string())?;
    let mut archive = ZipArchive::new(file).map_err(|_| "Fichier ZIP corrompu.".to_string())?;

    // Lire payload.bin
    let mut payload = Vec::new();
    let mut payload_file = archive
        .by_name("payload.bin")
        .map_err(|_| "Fichier payload.bin introuvable.")?;
    payload_file
        .read_to_end(&mut payload)
        .map_err(|_| "Impossible de lire payload.bin.")?;

    // Lire meta.json
    let mut meta_json = String::new();
    let mut meta_file = archive
        .by_name("meta.json")
        .map_err(|_| "Fichier meta.json introuvable.")?;
    meta_file
        .read_to_string(&mut meta_json)
        .map_err(|_| "Impossible de lire meta.json.")?;

    let meta: Value = serde_json::from_str(&meta_json).map_err(|_| "meta.json invalide.")?;
    let salt = general_purpose::STANDARD
        .decode(meta["salt"].as_str().unwrap_or_default())
        .map_err(|_| "Salt invalide.")?;
    let aes_key = derive_key(password, &salt);

    let plaintext = aesgcm_decrypt(&aes_key, &payload)?;
    serde_json::from_slice(&plaintext).map_err(|_| "Impossible de désérialiser les données.".to_string())
}

// --- AutoSaver ---
pub struct AutoSaver<F> {
    provider: F,
    profile: String,
    slot: u8,
    password: String,
    interval: u64, // en secondes
    stop: Arc<Mutex<bool>>,
    thread: Option<thread::JoinHandle<()>>,
}

impl<F> AutoSaver<F>
where
    F: Fn() -> Map<String, Value> + Send + 'static,
{
    /// Crée un nouveau AutoSaver
    pub fn new(provider: F, profile: String, slot: u8, password: String, interval: u64) -> Self {
        Self {
            provider,
            profile,
            slot,
            password,
            interval,
            stop: Arc::new(Mutex::new(false)),
            thread: None,
        }
    }

    /// Boucle de sauvegarde automatique
    fn loop_save(&self) {
        let stop = self.stop.clone();
        let profile = self.profile.clone();
        let password = self.password.clone();
        let provider = self.provider;
        let mut current_slot = self.slot;

        while !*stop.lock().unwrap() {
            let data = (provider)();

            match save_to_slot(&profile, current_slot, data, &password) {
                Ok(_) => {
                    log_save_event(&profile, current_slot, "OK", None);
                    // Rotation des slots: 1 → 2 → 3 → 1
                    current_slot = if current_slot == 3 { 1 } else { current_slot + 1 };
                }
                Err(e) => {
                    log_save_event(&profile, current_slot, "ERROR", Some(&e));
                }
            }

            // Attendre l'intervalle (en vérifiant `stop` toutes les 0.5 secondes)
            for _ in 0..(self.interval * 2) {
                if *stop.lock().unwrap() {
                    break;
                }
                thread::sleep(Duration::from_millis(500));
            }
        }
    }

    /// Démarre la sauvegarde automatique
    pub fn start(&mut self) {
        if let Some(thread) = &self.thread {
            if thread.is_finished() == false {
                return; // Le thread est déjà en cours d'exécution
            }
        }

        *self.stop.lock().unwrap() = false;
        let stop = self.stop.clone();
        let profile = self.profile.clone();
        let password = self.password.clone();
        let slot = self.slot;
        let interval = self.interval;
        let provider = self.provider.clone();

        self.thread = Some(thread::spawn(move || {
            let saver = AutoSaver {
                provider,
                profile,
                slot,
                password,
                interval,
                stop,
                thread: None,
            };
            saver.loop_save();
        }));
    }

    /// Arrête la sauvegarde automatique
    pub fn stop(&mut self) {
        *self.stop.lock().unwrap() = true;
        if let Some(thread) = self.thread.take() {
            thread.join().unwrap_or_else(|_| panic!("Impossible de joindre le thread de sauvegarde"));
        }
    }
}

// Clonage de la closure pour AutoSaver
impl<F> Clone for AutoSaver<F>
where
    F: Fn() -> Map<String, Value> + Send + Clone + 'static,
{
    fn clone(&self) -> Self {
        Self {
            provider: self.provider.clone(),
            profile: self.profile.clone(),
            slot: self.slot,
            password: self.password.clone(),
            interval: self.interval,
            stop: self.stop.clone(),
            thread: None, // On ne clone pas le thread
        }
    }
}
