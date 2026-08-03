use std::{
    fs,
    path::{Path, PathBuf},
};

use crate::utils::save::{
    config::SAVE_DIRECTORY,
    errors::SaveResult,
};

pub struct ProfileManager;

impl ProfileManager {

    pub fn new() -> Self {
        Self
    }

    /// Retourne le dossier d'un profil.
    pub fn profile_directory(
        &self,
        profile: &str,
    ) -> PathBuf {

        Path::new(SAVE_DIRECTORY)
            .join(profile)
    }

    /// Crée le dossier d'un profil.
    pub fn create_profile_directory(
        &self,
        profile: &str,
    ) -> SaveResult<()> {

        fs::create_dir_all(
            self.profile_directory(profile),
        )?;

        Ok(())
    }

    /// Vérifie si un profil existe.
    pub fn profile_exists(
        &self,
        profile: &str,
    ) -> bool {

        self.profile_directory(profile)
            .exists()
    }

    /// Supprime complètement un profil.
    pub fn delete_profile(
        &self,
        profile: &str,
    ) -> SaveResult<()> {

        let directory =
            self.profile_directory(profile);

        if directory.exists() {
            fs::remove_dir_all(directory)?;
        }

        Ok(())
    }

    /// Renomme un profil.
    pub fn rename_profile(
        &self,
        old_name: &str,
        new_name: &str,
    ) -> SaveResult<()> {

        fs::rename(
            self.profile_directory(old_name),
            self.profile_directory(new_name),
        )?;

        Ok(())
    }

    /// Liste tous les profils.
    pub fn list_profiles(
        &self,
    ) -> SaveResult<Vec<String>> {

        let mut profiles = Vec::new();

        if !Path::new(SAVE_DIRECTORY).exists() {
            return Ok(profiles);
        }

        for entry in fs::read_dir(SAVE_DIRECTORY)? {

            let entry = entry?;

            if entry.path().is_dir() {

                if let Some(name) =
                    entry.file_name().to_str()
                {
                    profiles.push(
                        name.to_string(),
                    );
                }
            }
        }

        profiles.sort();

        Ok(profiles)
    }
}
