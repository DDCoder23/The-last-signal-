use fernet::Fernet;
use serde_json::Value;
use std::fs;

pub fn decrypt_vault() -> Result<Value, Box<dyn std::error::Error>> {
    const KEY_FILE: &str = "security/master.key";
    const VAULT_FILE: &str = "security/vault.enc";

    let key = fs::read_to_string(KEY_FILE)?;
    let cipher = Fernet::new(key.trim())
        .ok_or("Clé Fernet invalide")?;

    let encrypted = fs::read(VAULT_FILE)?;

    let decrypted = cipher
        .decrypt(&encrypted)
        .ok_or("Impossible de déchiffrer vault.enc")?;

    let vault: Value = serde_json::from_slice(&decrypted)?;

    Ok(vault)
}
