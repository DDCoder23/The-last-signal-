use aes_gcm::{
    aead::{
        Aead,
        AeadCore,
        KeyInit,
        OsRng,
    },
    Aes256Gcm,
    Nonce,
};

use base64::{
    engine::general_purpose,
    Engine as _,
};

use pbkdf2::{
    password_hash::{
        rand_core::RngCore,
        SaltString,
    },
    Pbkdf2,
};

use sha2::{
    Digest,
    Sha256,
};

use crate::utils::save::errors::{
    SaveError,
    SaveResult,
};
use crate::utils::save::config::{
    AES_KEY_SIZE,
    PBKDF2_ITERATIONS,
};


pub struct Encryption;

impl Encryption {

    /// Génère un salt aléatoire.
    pub fn generate_salt() -> SaltString {

        SaltString::generate(&mut OsRng)
    }

    /// Dérive une clé AES-256 depuis un mot de passe.
    pub fn derive_key(
        password: &str,
        salt: &SaltString,
    ) -> SaveResult<[u8; AES_KEY_SIZE]> {

        let mut key = [0u8; AES_KEY_SIZE];

        pbkdf2::pbkdf2_hmac::<Sha256>(
            password.as_bytes(),
            salt.as_str().as_bytes(),
            PBKDF2_ITERATIONS,
            &mut key,
        );

        Ok(key)
    }

    /// Chiffre des données.
    pub fn encrypt(
        key: &[u8; AES_KEY_SIZE],
        data: &[u8],
    ) -> SaveResult<(Vec<u8>, [u8; 12])> {

        let cipher =
            Aes256Gcm::new_from_slice(key)
                .map_err(|e| SaveError::Crypto(e.to_string()))?;

        let nonce =
            Aes256Gcm::generate_nonce(&mut OsRng);

        let ciphertext =
            cipher
                .encrypt(&nonce, data)
                .map_err(|e| SaveError::Crypto(e.to_string()))?;

        let mut nonce_bytes = [0u8; 12];
        nonce_bytes.copy_from_slice(&nonce);

        Ok((ciphertext, nonce_bytes))
    }

    /// Déchiffre des données.
    pub fn decrypt(
        key: &[u8; AES_KEY_SIZE],
        nonce: &[u8; 12],
        data: &[u8],
    ) -> SaveResult<Vec<u8>> {

        let cipher =
            Aes256Gcm::new_from_slice(key)
                .map_err(|e| SaveError::Crypto(e.to_string()))?;

        let plaintext =
            cipher
                .decrypt(
                    Nonce::from_slice(nonce),
                    data,
                )
                .map_err(|_| SaveError::InvalidPassword)?;

        Ok(plaintext)
    }

    /// SHA-256 en hexadécimal.
    pub fn sha256(
        data: &[u8],
    ) -> String {

        let hash =
            Sha256::digest(data);

        hex::encode(hash)
    }

    /// Encode du Base64.
    pub fn encode_base64(
        bytes: &[u8],
    ) -> String {

        general_purpose::STANDARD.encode(bytes)
    }

    /// Décode du Base64.
    pub fn decode_base64(
        text: &str,
    ) -> SaveResult<Vec<u8>> {

        general_purpose::STANDARD
            .decode(text)
            .map_err(|e| SaveError::Crypto(e.to_string()))
    }
    /// Encode un SaltString en Base64.
pub fn encode_salt(
    salt: &SaltString,
) -> String {

    general_purpose::STANDARD.encode(
        salt.as_str().as_bytes(),
    )
}

/// Décode un SaltString depuis du Base64.
pub fn decode_salt(
    text: &str,
) -> SaveResult<SaltString> {

    let bytes =
        general_purpose::STANDARD
            .decode(text)
            .map_err(|e| SaveError::Crypto(e.to_string()))?;

    let text =
        String::from_utf8(bytes)
            .map_err(|e| SaveError::Crypto(e.to_string()))?;

    SaltString::from_b64(&text)
        .map_err(|e| SaveError::Crypto(e.to_string()))
}
}
