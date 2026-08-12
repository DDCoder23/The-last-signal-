use fernet::Fernet;
use serde_json::Value;
use std::fs;

pub fn decrypt_vault() -> Result<Value, Box<dyn std::error::Error>> {
    const KEY_FILE: &str = "../security/master.key";
    const VAULT_FILE: &str = "../security/vault.enc";

    // Lire la clé Fernet
    let key = fs::read_to_string(KEY_FILE)?;

    let cipher = Fernet::new(key.trim())
        .ok_or("Clé Fernet invalide")?;

    // vault.enc est un token Fernet texte
    let encrypted = fs::read_to_string(VAULT_FILE)?;

    // fernet 0.2.2 retourne directement un Result
    let decrypted = cipher.decrypt(encrypted.trim())?;

    // JSON déchiffré
    let vault: Value = serde_json::from_slice(&decrypted)?;

    Ok(vault)
}
