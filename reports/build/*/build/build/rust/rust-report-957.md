# Rust Report

Run : 957
Branch : main
Commit : 7570a608c1adb8250db487da90af289bdcef089c
Date : Wed Aug 19 12:32:48 UTC 2026


## Cargo fmt
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:1:
-use std::str::FromStr;
 use std::path::Path;
+use std::str::FromStr;
 
 use sqlx::{
-    sqlite::{SqliteConnectOptions, SqlitePool},
     Error,
+    sqlite::{SqliteConnectOptions, SqlitePool},
 };
 
-
 pub struct DatabaseManager {
     pool: SqlitePool,
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:13:
 
-
 impl DatabaseManager {
     /// Vérifie si une base SQLite existante est corrompue.
     ///
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:19:
     /// - Ok(false) → base valide
     /// - Ok(true)  → base corrompue
     /// - Err(...)  → impossible de vérifier la base
-    pub async fn is_database_corrupted(
-        database_url: &str,
-    ) -> Result<bool, sqlx::Error> {
-        let options = SqliteConnectOptions::from_str(database_url)?
-            .create_if_missing(false);
+    pub async fn is_database_corrupted(database_url: &str) -> Result<bool, sqlx::Error> {
+        let options = SqliteConnectOptions::from_str(database_url)?.create_if_missing(false);
 
         let pool = SqlitePool::connect_with(options).await?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:30:
-        let integrity: String = sqlx::query_scalar(
-            "PRAGMA integrity_check"
-        )
-        .fetch_one(&pool)
-        .await?;
+        let integrity: String = sqlx::query_scalar("PRAGMA integrity_check")
+            .fetch_one(&pool)
+            .await?;
 
         pool.close().await;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:39:
     }
 
     /// Crée ou ouvre la base SQLite.
-    pub async fn create_database(
-        database_url: &str,
-    ) -> Result<SqlitePool, sqlx::Error> {
-        let options = SqliteConnectOptions::from_str(database_url)?
-            .create_if_missing(true);
+    pub async fn create_database(database_url: &str) -> Result<SqlitePool, sqlx::Error> {
+        let options = SqliteConnectOptions::from_str(database_url)?.create_if_missing(true);
 
         let pool = SqlitePool::connect_with(options).await?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:59:
 
     /// Vérifie que PostgreSQL répond.
     pub async fn ping(&self) -> Result<(), sqlx::Error> {
+        sqlx::query("SELECT 1").execute(&self.pool).await?;
 
-        sqlx::query("SELECT 1")
-            .execute(&self.pool)
-            .await?;
-
         Ok(())
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:70:
-    pub async fn new(
-        database_path: &str,
-        database_url: &str,
-    ) -> Result<Self, sqlx::Error> {
+    pub async fn new(database_path: &str, database_url: &str) -> Result<Self, sqlx::Error> {
         // --------------------------------------------------
         // 1. Récupérer le chemin réel de la DB
         // --------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:78:
         let path = database_path
             .strip_prefix("sqlite:")
             .unwrap_or(database_path);
-        let database_file = database_url
-            .strip_prefix("sqlite:")
-            .unwrap_or(database_url);
-        
-       std::fs::create_dir_all(path)
-        .map_err(sqlx::Error::Io)?;
-      let pool =Self::create_database(database_url).await?;
-        
+        let database_file = database_url.strip_prefix("sqlite:").unwrap_or(database_url);
 
-        
-        
-        
+        std::fs::create_dir_all(path).map_err(sqlx::Error::Io)?;
+        let pool = Self::create_database(database_url).await?;
 
         // --------------------------------------------------
         // 3. Vérifier la DB si elle existe déjà
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:103:
                          Suppression et recréation..."
                     );
 
-                    std::fs::remove_file(database_file)
-                        .map_err(sqlx::Error::Io)?;
-                    let pool =Self::create_database(database_url).await?;
-
-
-                    
+                    std::fs::remove_file(database_file).map_err(sqlx::Error::Io)?;
+                    let pool = Self::create_database(database_url).await?;
                 }
 
                 Ok(false) => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:126:
                     return Err(error);
                 }
             }
-        } 
+        }
 
-        
         // --------------------------------------------------
         // 5. Retourner la structure
         // --------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:135:
 
-        Ok(Self {
-            pool,
-        })
+        Ok(Self { pool })
     }
 }
-
-
-    
-
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/migrations.rs:1:
+use crate::utils::password::hash_password;
+use crate::utils::vault::decrypt_vault;
 use log::debug;
-use uuid::Uuid;
 use sqlx::SqlitePool;
-use crate::utils::vault::decrypt_vault;
-use crate::utils::password::hash_password;
+use uuid::Uuid;
 /// Exécute toutes les migrations SQL non encore appliquées.
 pub async fn run(pool: &SqlitePool) -> Result<(), Box<dyn std::error::Error>> {
     sqlx::query(
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/migrations.rs:23:
     let vault = decrypt_vault()?;
 
     let password1 = vault["user1_password"]
-    .as_str()
-    .ok_or("Mot de passe user1 absent")?;
-    let password1_hash = hash_password(password1)
-    .map_err(|e| sqlx::Error::Protocol(e))?;
+        .as_str()
+        .ok_or("Mot de passe user1 absent")?;
+    let password1_hash = hash_password(password1).map_err(|e| sqlx::Error::Protocol(e))?;
 
     let password2 = vault["user2_password"]
-    .as_str()
-    .ok_or("Mot de passe user2 absent")?;
-    let password2_hash = hash_password(password2)
-    .map_err(|e| sqlx::Error::Protocol(e))?;
-    
-    
-    sqlx::migrate!("./migrations")
-        .run(pool)
-        .await?;
+        .as_str()
+        .ok_or("Mot de passe user2 absent")?;
+    let password2_hash = hash_password(password2).map_err(|e| sqlx::Error::Protocol(e))?;
 
+    sqlx::migrate!("./migrations").run(pool).await?;
+
     debug!("Migrations SQLite appliquées.");
-    create_account(
-    pool,
-    "Admin@gmail.com",
-    &password1_hash,
-        "Cyril",
-        "Dev",
-)
-.await?;
+    create_account(pool, "Admin@gmail.com", &password1_hash, "Cyril", "Dev").await?;
 
-create_account(
-    pool,
-    "Superadmin@gmail.com",
-    &password2_hash,
-    "Morgan",
-    "SuperDev",
-)
-.await?;
+    create_account(
+        pool,
+        "Superadmin@gmail.com",
+        &password2_hash,
+        "Morgan",
+        "SuperDev",
+    )
+    .await?;
 
     Ok(())
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/mod.rs:1:
 pub mod database_manager;
 pub mod migrations;
-
-
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/dice.rs:1:
-use rand::{Rng,RngExt};
+use rand::{Rng, RngExt};
 
 pub fn jet_de_des(face: u32, nb: u32) -> u32 {
     let mut rng = rand::rng();
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/dice.rs:5:
 
-    (0..nb)
-        .map(|_| rng.random_range(1..=face))
-        .sum()
+    (0..nb).map(|_| rng.random_range(1..=face)).sum()
 }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/objets.rs:1:
-use serde::{Serialize, Deserialize};
+use serde::{Deserialize, Serialize};
 use std::collections::HashMap;
 
 // Enum pour les types d'objets
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/objets.rs:34:
 }
 
 impl Objet {
-    pub fn new(
-        nom: &str,
-        image: Option<&str>,
-        quantite: u32,
-        type_objet: TypeObjet,
-    ) -> Self {
+    pub fn new(nom: &str, image: Option<&str>, quantite: u32, type_objet: TypeObjet) -> Self {
         Self {
             nom_base: nom.replace(" ", "_"),
             quantite,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/objets.rs:117:
         bonus: i32,
         enchantements: Vec<String>,
     ) -> Self {
-        let  objet = Objet::new(nom, image, quantite, TypeObjet::Equipement);
+        let objet = Objet::new(nom, image, quantite, TypeObjet::Equipement);
         let parts: Vec<&str> = nom.split_whitespace().collect();
         let category = parts.get(0).unwrap_or(&"").to_string();
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/objets.rs:236:
 }
 
 impl Potion {
-    pub fn new(
-        nom: &str,
-        image: Option<&str>,
-        quantite: u32,
-        effet: Option<&str>,
-    ) -> Self {
+    pub fn new(nom: &str, image: Option<&str>, quantite: u32, effet: Option<&str>) -> Self {
         let objet = Objet::new(nom, image, quantite, TypeObjet::Potion);
         Self {
             objet,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:1:
-use rand::{Rng,RngExt};
+use crate::gameplay::dice::jet_de_des;
+use log::debug;
+use rand::{Rng, RngExt};
 use sqlx::SqlitePool;
 use std::collections::HashMap;
-use log::debug;
-use crate::gameplay::dice::jet_de_des;
 
-
 const PA: u32 = 1;
 const PO: u32 = PA * 10;
 const PP: u32 = PO * 10;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:22:
 
 #[derive(Debug, Clone)]
 pub struct Tresor {
-    
     pub loot_par_niveau: HashMap<u32, Loot>,
 
     pub objets_garantis: HashMap<u32, HashMap<String, u32>>,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:32:
     pub seuil_artefact_commun: HashMap<u32, u32>,
     pub seuil_artefact_peu_commun: HashMap<u32, u32>,
     pub sous_loot: HashMap<String, HashMap<String, f64>>,
-    
+
     pub sous_loot_livre_normal: HashMap<String, f64>,
     pub sous_loot_livre_admin: HashMap<String, f64>,
-    
-
-    
 }
 
 impl Tresor {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:148:
         // Niveau 1
         let mut niveau_1 = HashMap::new();
 
-        niveau_1.insert(
-            "argent".to_string(),
-            jet_de_des(6, 2) * PA,
-        );
+        niveau_1.insert("argent".to_string(), jet_de_des(6, 2) * PA);
 
         niveau_1.insert("torche".to_string(), 2);
         niveau_1.insert("sac".to_string(), 3);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:164:
 
         // 17 chances sur 20 : pain
         if jet_de_des(20, 1) >= 4 {
-            niveau_1.insert(
-                "pain".to_string(),
-                rng.random_range(3..=5),
-            );
+            niveau_1.insert("pain".to_string(), rng.random_range(3..=5));
         }
 
         objets_garantis.insert(1, niveau_1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:175:
         // Niveau 2
         let mut niveau_2 = HashMap::new();
 
-        niveau_2.insert(
-            "argent".to_string(),
-            jet_de_des(6, 4) * PA,
-        );
+        niveau_2.insert("argent".to_string(), jet_de_des(6, 4) * PA);
 
         niveau_2.insert("torche".to_string(), 1);
         niveau_2.insert("sac".to_string(), 2);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:193:
         // Niveau 3
         let mut niveau_3 = HashMap::new();
 
-        niveau_3.insert(
-            "argent".to_string(),
-            jet_de_des(6, 1) * 10 * PA,
-        );
+        niveau_3.insert("argent".to_string(), jet_de_des(6, 1) * 10 * PA);
 
         niveau_3.insert("torche".to_string(), 2);
         niveau_3.insert("sac".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:211:
         // Niveau 4
         let mut niveau_4 = HashMap::new();
 
-        niveau_4.insert(
-            "argent".to_string(),
-            jet_de_des(6, 2) * 10 * PA,
-        );
+        niveau_4.insert("argent".to_string(), jet_de_des(6, 2) * 10 * PA);
 
         if jet_de_des(20, 1) >= 12 {
             niveau_4.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:225:
         // Niveau 5
         let mut niveau_5 = HashMap::new();
 
-        niveau_5.insert(
-            "argent".to_string(),
-            jet_de_des(6, 3) * 10 * PA,
-        );
+        niveau_5.insert("argent".to_string(), jet_de_des(6, 3) * 10 * PA);
 
         if jet_de_des(20, 1) >= 10 {
             niveau_5.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:237:
         objets_garantis.insert(5, niveau_5);
         let mut niveau_6 = HashMap::new();
 
-        niveau_6.insert(
-            "argent".to_string(),
-            jet_de_des(6, 4) * 10 * PA,
-        );
+        niveau_6.insert("argent".to_string(), jet_de_des(6, 4) * 10 * PA);
 
         if jet_de_des(20, 1) >= 8 {
             niveau_6.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:249:
         objets_garantis.insert(6, niveau_6);
         let mut niveau_7 = HashMap::new();
 
-        niveau_7.insert(
-            "argent".to_string(),
-            jet_de_des(6, 5) * 10 * PA,
-        );
+        niveau_7.insert("argent".to_string(), jet_de_des(6, 5) * 10 * PA);
 
         if jet_de_des(20, 1) >= 6 {
             niveau_7.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:284:
             "flèches épiques",
             "flèches légendaires",
         ] {
-            quantite_objets.insert(
-                objet.to_string(),
-                rng.random_range(2..=9),
-            );
+            quantite_objets.insert(objet.to_string(), rng.random_range(2..=9));
         }
-        let mut sous_loot: HashMap<String, HashMap<String, f64>> =
-    HashMap::new();
+        let mut sous_loot: HashMap<String, HashMap<String, f64>> = HashMap::new();
         sous_loot.insert(
-    "Artefact commun".to_string(),
-    HashMap::from([
-        ("food".to_string(), 80.0),
-        ("minerais".to_string(), 19.0),
-        ("équi".to_string(), 1.0),
-    ]),
-);
+            "Artefact commun".to_string(),
+            HashMap::from([
+                ("food".to_string(), 80.0),
+                ("minerais".to_string(), 19.0),
+                ("équi".to_string(), 1.0),
+            ]),
+        );
         sous_loot.insert(
-    "Artefact peu commun".to_string(),
-    HashMap::from([
-        ("food".to_string(), 50.0),
-        ("minerais".to_string(), 40.0),
-        ("équi".to_string(), 10.0),
-    ]),
-);
+            "Artefact peu commun".to_string(),
+            HashMap::from([
+                ("food".to_string(), 50.0),
+                ("minerais".to_string(), 40.0),
+                ("équi".to_string(), 10.0),
+            ]),
+        );
         sous_loot.insert(
-    "Artefact rare".to_string(),
-    HashMap::from([
-        ("minerais".to_string(), 50.0),
-        ("équi".to_string(), 25.0),
-        ("potion".to_string(), 25.0),
-    ]),
-);
+            "Artefact rare".to_string(),
+            HashMap::from([
+                ("minerais".to_string(), 50.0),
+                ("équi".to_string(), 25.0),
+                ("potion".to_string(), 25.0),
+            ]),
+        );
         sous_loot.insert(
-    "food".to_string(),
-    HashMap::from([
-        ("viande".to_string(), 10.0),
-        ("pain".to_string(), 70.0),
-        ("fruit et légumes".to_string(), 10.0),
-        ("herbes et racines".to_string(), 10.0),
-    ]),
-);
+            "food".to_string(),
+            HashMap::from([
+                ("viande".to_string(), 10.0),
+                ("pain".to_string(), 70.0),
+                ("fruit et légumes".to_string(), 10.0),
+                ("herbes et racines".to_string(), 10.0),
+            ]),
+        );
         sous_loot.insert(
-    "Artefact super rare".to_string(),
-    HashMap::from([
-        ("potion".to_string(), 50.0),
-        ("équi".to_string(), 40.0),
-        ("minerais".to_string(), 9.9),
-        ("livre enchant".to_string(), 0.1),
-    ]),
-);
+            "Artefact super rare".to_string(),
+            HashMap::from([
+                ("potion".to_string(), 50.0),
+                ("équi".to_string(), 40.0),
+                ("minerais".to_string(), 9.9),
+                ("livre enchant".to_string(), 0.1),
+            ]),
+        );
         sous_loot.insert(
-    "Artefact epique".to_string(),
-    HashMap::from([
-        ("potion".to_string(), 15.0),
-        ("équi".to_string(), 75.0),
-        ("livre enchant".to_string(), 10.0),
-        
-    ]),
-);
+            "Artefact epique".to_string(),
+            HashMap::from([
+                ("potion".to_string(), 15.0),
+                ("équi".to_string(), 75.0),
+                ("livre enchant".to_string(), 10.0),
+            ]),
+        );
         sous_loot.insert(
-    "Artefact legendaire".to_string(),
-    HashMap::from([
-        ("potion".to_string(), 5.0),
-        ("équi".to_string(), 75.0),
-        ("livre enchant".to_string(), 20.0),
-        
-    ]),
-);
+            "Artefact legendaire".to_string(),
+            HashMap::from([
+                ("potion".to_string(), 5.0),
+                ("équi".to_string(), 75.0),
+                ("livre enchant".to_string(), 20.0),
+            ]),
+        );
         sous_loot.insert(
-    "Artefact admin".to_string(),
-    HashMap::from([
-        ("livre enchant".to_string(), 100.0),
-        
-    ]),
-);
-            
+            "Artefact admin".to_string(),
+            HashMap::from([("livre enchant".to_string(), 100.0)]),
+        );
 
-            
-        let seuil_artefact_commun: HashMap<u32, u32> = HashMap::from([
-    (2, 20),
-    (3, 19),
-    (4, 17),
-    (5, 15),
-    (6, 15),
-    (7, 14),       
-]);
-        let seuil_artefact_peu_commun: HashMap<u32, u32> = HashMap::from([
-    (6, 20),
-    (7, 19),
-
-]);
+        let seuil_artefact_commun: HashMap<u32, u32> =
+            HashMap::from([(2, 20), (3, 19), (4, 17), (5, 15), (6, 15), (7, 14)]);
+        let seuil_artefact_peu_commun: HashMap<u32, u32> = HashMap::from([(6, 20), (7, 19)]);
         let sous_loot_livre_normal = HashMap::from([
-    ("livre enchant niv 1".to_string(), 70.0),
-    ("livre enchant niv 2".to_string(), 20.0),
-    ("livre enchant niv 3".to_string(), 5.0),
-    ("livre enchant niv 4".to_string(), 3.0),
-    ("livre enchant niv 5".to_string(), 1.5),
-    ("livre enchant niv 6".to_string(), 0.5),
-]);
+            ("livre enchant niv 1".to_string(), 70.0),
+            ("livre enchant niv 2".to_string(), 20.0),
+            ("livre enchant niv 3".to_string(), 5.0),
+            ("livre enchant niv 4".to_string(), 3.0),
+            ("livre enchant niv 5".to_string(), 1.5),
+            ("livre enchant niv 6".to_string(), 0.5),
+        ]);
 
-let sous_loot_livre_admin = HashMap::from([
-    ("livre enchant niv 1".to_string(), 45.0),
-    ("livre enchant niv 2".to_string(), 15.0),
-    ("livre enchant niv 3".to_string(), 13.0),
-    ("livre enchant niv 4".to_string(), 12.0),
-    ("livre enchant niv 5".to_string(), 8.0),
-    ("livre enchant niv 6".to_string(), 7.0),
-]);
-        
+        let sous_loot_livre_admin = HashMap::from([
+            ("livre enchant niv 1".to_string(), 45.0),
+            ("livre enchant niv 2".to_string(), 15.0),
+            ("livre enchant niv 3".to_string(), 13.0),
+            ("livre enchant niv 4".to_string(), 12.0),
+            ("livre enchant niv 5".to_string(), 8.0),
+            ("livre enchant niv 6".to_string(), 7.0),
+        ]);
 
         Self {
             loot_par_niveau,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:401:
             seuil_artefact_commun,
             seuil_artefact_peu_commun,
             sous_loot_livre_normal,
-            sous_loot_livre_admin, 
-        
+            sous_loot_livre_admin,
         }
     }
-    
-      pub async fn ouvrir(
-    &mut self,
-    pool: &SqlitePool,
-    account_id: i64,
-    niveau: u32,
-    is_admin: bool,
-) -> Result<HashMap<String, u32>, sqlx::Error> {
-    let mut rng = rand::rng();
 
-    let loot = self
-        .loot_par_niveau
-        .get(&niveau)
-        .cloned()
-        .expect("Niveau de coffre invalide");
+    pub async fn ouvrir(
+        &mut self,
+        pool: &SqlitePool,
+        account_id: i64,
+        niveau: u32,
+        is_admin: bool,
+    ) -> Result<HashMap<String, u32>, sqlx::Error> {
+        let mut rng = rand::rng();
 
-    let mut objets = HashMap::new();
+        let loot = self
+            .loot_par_niveau
+            .get(&niveau)
+            .cloned()
+            .expect("Niveau de coffre invalide");
 
-    // ==========================================
-    // OBJETS GARANTIS
-    // ==========================================
+        let mut objets = HashMap::new();
 
-    if let Some(garantis) = self.objets_garantis.get(&niveau) {
-        for (objet, quantite) in garantis {
-            *objets.entry(objet.clone()).or_insert(0) += *quantite;
+        // ==========================================
+        // OBJETS GARANTIS
+        // ==========================================
+
+        if let Some(garantis) = self.objets_garantis.get(&niveau) {
+            for (objet, quantite) in garantis {
+                *objets.entry(objet.clone()).or_insert(0) += *quantite;
+            }
         }
-    }
 
-    // ==========================================
-    // OBJETS COMMUNS
-    // ==========================================
+        // ==========================================
+        // OBJETS COMMUNS
+        // ==========================================
 
-    for _ in 0..loot.commun {
-        let seuil = self
-            .seuil_artefact_commun
-            .get(&niveau)
-            .copied()
-            .unwrap_or(20);
+        for _ in 0..loot.commun {
+            let seuil = self
+                .seuil_artefact_commun
+                .get(&niveau)
+                .copied()
+                .unwrap_or(20);
 
-        let jet = rng.random_range(1..=20);
+            let jet = rng.random_range(1..=20);
 
-        if jet >= seuil {
-            let objet = self
-                .tirer_objet(
-                    pool,
-                    account_id,
-                    "Artefact commun",
-                    &mut rng,
-                    is_admin,
-                )
-                .await?;
+            if jet >= seuil {
+                let objet = self
+                    .tirer_objet(pool, account_id, "Artefact commun", &mut rng, is_admin)
+                    .await?;
 
-            let quantite = self
-                .quantite_objets
-                .get(&objet)
-                .copied()
-                .unwrap_or(1);
+                let quantite = self.quantite_objets.get(&objet).copied().unwrap_or(1);
 
-            *objets.entry(objet).or_insert(0) += quantite;
+                *objets.entry(objet).or_insert(0) += quantite;
+            }
         }
-    }
 
-    // ==========================================
-    // LOOT ADMIN
-    // ==========================================
+        // ==========================================
+        // LOOT ADMIN
+        // ==========================================
 
-    if is_admin {
-        for _ in 0..loot.admin {
-            let objet = self
-                .tirer_objet(
-                    pool,
-                    account_id,
-                    "Artefact admin",
-                    &mut rng,
-                    is_admin,
-                )
-                .await?;
+        if is_admin {
+            for _ in 0..loot.admin {
+                let objet = self
+                    .tirer_objet(pool, account_id, "Artefact admin", &mut rng, is_admin)
+                    .await?;
 
-            let quantite = self
-                .quantite_objets
-                .get(&objet)
-                .copied()
-                .unwrap_or(1);
+                let quantite = self.quantite_objets.get(&objet).copied().unwrap_or(1);
 
-            *objets.entry(objet).or_insert(0) += quantite;
+                *objets.entry(objet).or_insert(0) += quantite;
+            }
         }
+
+        Ok(objets)
     }
 
-    Ok(objets)
-                }  
-            
-        
-            
+    pub fn tirer_pondere(table: &HashMap<String, f64>, rng: &mut impl Rng) -> String {
+        let total: f64 = table.values().sum();
 
-        
+        if total <= 0.0 {
+            panic!("Table de loot vide");
+        }
 
-            
-    
+        let tirage = rng.random_range(0.0..total);
 
-            
-        pub fn tirer_pondere(
-    table: &HashMap<String, f64>,
-    rng: &mut impl Rng,
-) -> String {
-    let total: f64 = table.values().sum();
+        let mut cumul = 0.0;
 
-    if total <= 0.0 {
-        panic!("Table de loot vide");
-    }
+        for (objet, poids) in table {
+            cumul += poids;
 
-    let tirage = rng.random_range(0.0..total);
-
-    let mut cumul = 0.0;
-
-    for (objet, poids) in table {
-        cumul += poids;
-
-        if tirage < cumul {
-            return objet.clone();
+            if tirage < cumul {
+                return objet.clone();
+            }
         }
-    }
 
-    unreachable!("Le tirage n'a trouvé aucun résultat")
-}
-pub fn cle_echec(categorie: &str, objet: &str) -> String {
-    format!("{}::{}", categorie, objet)
-}
+        unreachable!("Le tirage n'a trouvé aucun résultat")
+    }
+    pub fn cle_echec(categorie: &str, objet: &str) -> String {
+        format!("{}::{}", categorie, objet)
+    }
     pub async fn tirer_objet(
-    &mut self,
-    pool: &SqlitePool,
-    account_id: i64,
-    categorie: &str,
-    rng: &mut impl Rng,
-    is_admin: bool,
-) -> Result<String, sqlx::Error> {
+        &mut self,
+        pool: &SqlitePool,
+        account_id: i64,
+        categorie: &str,
+        rng: &mut impl Rng,
+        is_admin: bool,
+    ) -> Result<String, sqlx::Error> {
+        let mut categorie_actuelle = categorie.to_string();
 
-    let mut categorie_actuelle = categorie.to_string();
+        loop {
+            // ==========================================
+            // RÉCUPÉRATION DE LA TABLE
+            // ==========================================
 
-    loop {
-        // ==========================================
-        // RÉCUPÉRATION DE LA TABLE
-        // ==========================================
+            let table_originale = self
+                .sous_loot
+                .get(&categorie_actuelle)
+                .cloned()
+                .unwrap_or_else(|| {
+                    panic!("Catégorie de loot inconnue : {:?}", categorie_actuelle);
+                });
 
-        let table_originale = self
-            .sous_loot
-            .get(&categorie_actuelle)
-            .cloned()
-            .unwrap_or_else(|| {
-                panic!(
-                    "Catégorie de loot inconnue : {:?}",
-                    categorie_actuelle
-                );
-            });
+            let total: f64 = table_originale.values().sum();
 
-        let total: f64 = table_originale.values().sum();
+            if total <= 0.0 {
+                panic!("Table de loot vide");
+            }
 
-        if total <= 0.0 {
-            panic!("Table de loot vide");
-        }
+            // ==========================================
+            // CALCUL DES POIDS AVEC LE PITY SYSTEM
+            // ==========================================
 
-        // ==========================================
-        // CALCUL DES POIDS AVEC LE PITY SYSTEM
-        // ==========================================
+            let mut table_ajustee = HashMap::new();
 
-        let mut table_ajustee = HashMap::new();
+            for (objet, poids) in &table_originale {
+                let probabilite = poids / total;
 
-        for (objet, poids) in &table_originale {
-            let probabilite = poids / total;
-
-            let echecs: i64 = sqlx::query_scalar(
-                r#"
+                let echecs: i64 = sqlx::query_scalar(
+                    r#"
                 SELECT nombre
                 FROM echecs
                 WHERE account_id = ?
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:582:
                   AND categorie = ?
                   AND objet = ?
                 "#,
-            )
-            .bind(account_id)
-            .bind(&categorie_actuelle)
-            .bind(objet)
-            .fetch_optional(pool)
-            .await?
-            .unwrap_or(0);
+                )
+                .bind(account_id)
+                .bind(&categorie_actuelle)
+                .bind(objet)
+                .fetch_optional(pool)
+                .await?
+                .unwrap_or(0);
 
-            /*
-             * PITY :
-             *
-             * Un objet dont la probabilité originale
-             * est strictement inférieure à 3 % bénéficie
-             * du bonus.
-             *
-             * +7,5 % du poids original par échec.
-             */
-            let poids_ajuste = if probabilite < 0.03 {
-                *poids * (1.0 + 0.075 * echecs as f64)
-            } else {
-                *poids
-            };
+                /*
+                 * PITY :
+                 *
+                 * Un objet dont la probabilité originale
+                 * est strictement inférieure à 3 % bénéficie
+                 * du bonus.
+                 *
+                 * +7,5 % du poids original par échec.
+                 */
+                let poids_ajuste = if probabilite < 0.03 {
+                    *poids * (1.0 + 0.075 * echecs as f64)
+                } else {
+                    *poids
+                };
 
-            table_ajustee.insert(
-                objet.clone(),
-                poids_ajuste,
-            );
-        }
+                table_ajustee.insert(objet.clone(), poids_ajuste);
+            }
 
-        // ==========================================
-        // TIRAGE
-        // ==========================================
+            // ==========================================
+            // TIRAGE
+            // ==========================================
 
-        let resultat = Self::tirer_pondere(
-            &table_ajustee,
-            rng,
-        );
+            let resultat = Self::tirer_pondere(&table_ajustee, rng);
 
-        // ==========================================
-        // MISE À JOUR DES ÉCHECS
-        // ==========================================
+            // ==========================================
+            // MISE À JOUR DES ÉCHECS
+            // ==========================================
 
-        for (objet, poids) in &table_originale {
-            let probabilite = poids / total;
+            for (objet, poids) in &table_originale {
+                let probabilite = poids / total;
 
-            // Le pity ne concerne que les objets < 3 %
-            if probabilite >= 0.03 {
-                continue;
-            }
+                // Le pity ne concerne que les objets < 3 %
+                if probabilite >= 0.03 {
+                    continue;
+                }
 
-            if objet == &resultat {
-                // ----------------------------------
-                // OBJET OBTENU → RESET
-                // ----------------------------------
+                if objet == &resultat {
+                    // ----------------------------------
+                    // OBJET OBTENU → RESET
+                    // ----------------------------------
 
-                sqlx::query(
-                    r#"
+                    sqlx::query(
+                        r#"
                     INSERT INTO echecs (
                         account_id,
                         categorie,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:655:
                     DO UPDATE SET
                         nombre = 0
                     "#,
-                )
-                .bind(account_id)
-                .bind(&categorie_actuelle)
-                .bind(objet)
-                .execute(pool)
-                .await?;
+                    )
+                    .bind(account_id)
+                    .bind(&categorie_actuelle)
+                    .bind(objet)
+                    .execute(pool)
+                    .await?;
+                } else {
+                    // ----------------------------------
+                    // OBJET NON OBTENU → +1 ÉCHEC
+                    // ----------------------------------
 
-            } else {
-                // ----------------------------------
-                // OBJET NON OBTENU → +1 ÉCHEC
-                // ----------------------------------
-
-                sqlx::query(
-                    r#"
+                    sqlx::query(
+                        r#"
                     INSERT INTO echecs (
                         account_id,
                         categorie,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:685:
                     DO UPDATE SET
                         nombre = nombre + 1
                     "#,
-                )
-                .bind(account_id)
-                .bind(&categorie_actuelle)
-                .bind(objet)
-                .execute(pool)
-                .await?;
+                    )
+                    .bind(account_id)
+                    .bind(&categorie_actuelle)
+                    .bind(objet)
+                    .execute(pool)
+                    .await?;
+                }
             }
-        }
 
-        // ==========================================
-        // LIVRE ENCHANTÉ
-        // ==========================================
+            // ==========================================
+            // LIVRE ENCHANTÉ
+            // ==========================================
 
-        if resultat == "livre enchant" {
-            return self
-                .tirer_livre(
-                    pool,
-                    account_id,
-                    rng,
-                    is_admin,
-                )
-                .await;
-        }
+            if resultat == "livre enchant" {
+                return self.tirer_livre(pool, account_id, rng, is_admin).await;
+            }
 
-        // ==========================================
-        // SOUS-CATÉGORIE
-        // ==========================================
+            // ==========================================
+            // SOUS-CATÉGORIE
+            // ==========================================
 
-        if self.sous_loot.contains_key(&resultat) {
-            categorie_actuelle = resultat;
-            continue;
-        }
+            if self.sous_loot.contains_key(&resultat) {
+                categorie_actuelle = resultat;
+                continue;
+            }
 
-        // ==========================================
-        // OBJET FINAL
-        // ==========================================
+            // ==========================================
+            // OBJET FINAL
+            // ==========================================
 
-        return Ok(resultat);
+            return Ok(resultat);
+        }
     }
-    }
     pub async fn tirer_livre(
-    &mut self,
-    pool: &SqlitePool,
-    account_id: i64,
-    rng: &mut impl Rng,
-    is_admin: bool,
-) -> Result<String, sqlx::Error> {
+        &mut self,
+        pool: &SqlitePool,
+        account_id: i64,
+        rng: &mut impl Rng,
+        is_admin: bool,
+    ) -> Result<String, sqlx::Error> {
+        let categorie = if is_admin {
+            "livre enchant admin"
+        } else {
+            "livre enchant normal"
+        };
 
-    let categorie = if is_admin {
-        "livre enchant admin"
-    } else {
-        "livre enchant normal"
-    };
+        let table_originale = if is_admin {
+            self.sous_loot_livre_admin.clone()
+        } else {
+            self.sous_loot_livre_normal.clone()
+        };
 
-    let table_originale = if is_admin {
-        self.sous_loot_livre_admin.clone()
-    } else {
-        self.sous_loot_livre_normal.clone()
-    };
+        let total: f64 = table_originale.values().sum();
 
-    let total: f64 = table_originale.values().sum();
+        if total <= 0.0 {
+            panic!("Table de loot des livres vide");
+        }
 
-    if total <= 0.0 {
-        panic!("Table de loot des livres vide");
-    }
+        // ==========================================
+        // CALCUL DES POIDS AVEC PITY
+        // ==========================================
 
-    // ==========================================
-    // CALCUL DES POIDS AVEC PITY
-    // ==========================================
+        let mut table_ajustee = HashMap::new();
 
-    let mut table_ajustee = HashMap::new();
+        for (objet, poids) in &table_originale {
+            let probabilite = poids / total;
 
-    for (objet, poids) in &table_originale {
-        let probabilite = poids / total;
-
-        let echecs: i64 = sqlx::query_scalar(
-            r#"
+            let echecs: i64 = sqlx::query_scalar(
+                r#"
             SELECT nombre
             FROM echecs
             WHERE account_id = ?
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:768:
               AND categorie = ?
               AND objet = ?
             "#,
-        )
-        .bind(account_id)
-        .bind(categorie)
-        .bind(objet)
-        .fetch_optional(pool)
-        .await?
-        .unwrap_or(0);
+            )
+            .bind(account_id)
+            .bind(categorie)
+            .bind(objet)
+            .fetch_optional(pool)
+            .await?
+            .unwrap_or(0);
 
-        /*
-         * Seuls les livres ayant une probabilité
-         * originale < 3 % bénéficient du pity.
-         
-         */
+            /*
+            * Seuls les livres ayant une probabilité
+            * originale < 3 % bénéficient du pity.
 
-        let poids_ajuste = if probabilite < 0.03 {
-            *poids * (1.0 + 0.075 * echecs as f64)
-        } else {
-            *poids
-        };
+            */
 
-        table_ajustee.insert(
-            objet.clone(),
-            poids_ajuste,
-        );
-    }
+            let poids_ajuste = if probabilite < 0.03 {
+                *poids * (1.0 + 0.075 * echecs as f64)
+            } else {
+                *poids
+            };
 
-    // ==========================================
-    // TIRAGE
-    // ==========================================
+            table_ajustee.insert(objet.clone(), poids_ajuste);
+        }
 
-    let resultat = Self::tirer_pondere(
-        &table_ajustee,
-        rng,
-    );
+        // ==========================================
+        // TIRAGE
+        // ==========================================
 
-    // ==========================================
-    // MISE À JOUR DES ÉCHECS
-    // ==========================================
+        let resultat = Self::tirer_pondere(&table_ajustee, rng);
 
-    for (objet, poids) in &table_originale {
-        let probabilite = poids / total;
+        // ==========================================
+        // MISE À JOUR DES ÉCHECS
+        // ==========================================
 
-        // Pas de pity pour les objets >= 1 %
-        if probabilite >= 0.03 {
-            continue;
-        }
+        for (objet, poids) in &table_originale {
+            let probabilite = poids / total;
 
-        if objet == &resultat {
-            // ----------------------------------
-            // OBTENU → RESET
-            // ----------------------------------
+            // Pas de pity pour les objets >= 1 %
+            if probabilite >= 0.03 {
+                continue;
+            }
 
-            sqlx::query(
-                r#"
+            if objet == &resultat {
+                // ----------------------------------
+                // OBTENU → RESET
+                // ----------------------------------
+
+                sqlx::query(
+                    r#"
                 INSERT INTO echecs (
                     account_id,
                     categorie,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:838:
                 DO UPDATE SET
                     nombre = 0
                 "#,
-            )
-            .bind(account_id)
-            .bind(categorie)
-            .bind(objet)
-            .execute(pool)
-            .await?;
+                )
+                .bind(account_id)
+                .bind(categorie)
+                .bind(objet)
+                .execute(pool)
+                .await?;
+            } else {
+                // ----------------------------------
+                // PAS OBTENU → +1
+                // ----------------------------------
 
-        } else {
-            // ----------------------------------
-            // PAS OBTENU → +1
-            // ----------------------------------
-
-            sqlx::query(
-                r#"
+                sqlx::query(
+                    r#"
                 INSERT INTO echecs (
                     account_id,
                     categorie,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:868:
                 DO UPDATE SET
                     nombre = nombre + 1
                 "#,
-            )
-            .bind(account_id)
-            .bind(categorie)
-            .bind(objet)
-            .execute(pool)
-            .await?;
+                )
+                .bind(account_id)
+                .bind(categorie)
+                .bind(objet)
+                .execute(pool)
+                .await?;
+            }
         }
-    }
 
-    Ok(resultat)
+        Ok(resultat)
     }
-
-    
-
-        
-
-    
-    
-        
-    
-      }
+}
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/lib.rs:1:
 pub mod database;
+pub mod gameplay;
 pub mod network;
 pub mod utils;
-pub mod gameplay;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:1:
-use tokio::net::TcpStream;
+use crate::network::handler::PacketHandler;
+use crate::network::packet::{receive_packet, send_packet};
+use log::{debug, error, info};
 use sqlx::SqlitePool;
+use tokio::net::TcpStream;
 use uuid::Uuid;
-use log::{
-    info,
-    debug,
-    error,};
-use crate::network::handler::PacketHandler;
-use crate::network::packet::{
-    receive_packet,
-    send_packet,
-};
 
 pub struct Client {
     stream: TcpStream,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:24:
 }
 
 impl Client {
-
-    pub fn new(
-        stream: TcpStream,
-        pool: SqlitePool,
-    ) -> Self {
-
+    pub fn new(stream: TcpStream, pool: SqlitePool) -> Self {
         Self {
-
             stream,
 
             pool,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:41:
             client_id: None,
 
             account_id: None,
-
         }
-
     }
 
     pub async fn run(&mut self) {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:50:
-
         info!(
             "Client connecté : {} | Session : {}",
             self.stream.peer_addr().unwrap(),
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:55:
         );
 
         loop {
-
             match receive_packet(&mut self.stream).await {
-
                 Ok(packet) => {
+                    debug!("Type : {:?}", packet.packet_type);
 
-                    debug!(
-                        "Type : {:?}",
-                        packet.packet_type
-                    );
+                    debug!("Payload : {}", String::from_utf8_lossy(&packet.payload));
 
-                    debug!(
-                        "Payload : {}",
-                        String::from_utf8_lossy(
-                            &packet.payload
-                        )
-                    );
-
-                    let response =
-                     PacketHandler::handle(self, packet)
-                     .await;
-                    if let Err(e) =
-                        send_packet(
-                            &mut self.stream,
-                            &response,
-                        )
-                        .await
-                    {
-
+                    let response = PacketHandler::handle(self, packet).await;
+                    if let Err(e) = send_packet(&mut self.stream, &response).await {
                         error!("Erreur : {}", e);
 
                         break;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:89:
-
                     }
-
                 }
 
                 Err(e) => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:95:
+                    error!("Déconnexion [{}] : {}", self.session_id, e);
 
-                    error!(
-                        "Déconnexion [{}] : {}",
-                        self.session_id,
-                        e
-                    );
-
                     break;
-
                 }
-
             }
-
         }
-
     }
-
 }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1:
-use crate::network::packet::{
-    Packet,
-    PacketType,LogLevel,ClientLog,
-};
 use crate::network::client::Client;
-use log::{trace, debug, info, warn, error};
+use crate::network::packet::{ClientLog, LogLevel, Packet, PacketType};
+use log::{debug, error, info, trace, warn};
 pub struct PacketHandler;
 
-
 impl PacketHandler {
-
-    pub async fn handle(
-        _client: &mut Client,
-        packet: Packet,
-    ) -> Packet {
-
+    pub async fn handle(_client: &mut Client, packet: Packet) -> Packet {
         match packet.packet_type {
             PacketType::Log => {
+                let log = match serde_json::from_slice::<ClientLog>(&packet.payload) {
+                    Ok(log) => log,
+                    Err(e) => {
+                        error!("Impossible de décoder le paquet LOG : {}", e);
 
-    let log = match serde_json::from_slice::<ClientLog>(&packet.payload) {
-        Ok(log) => log,
-        Err(e) => {
-            error!("Impossible de décoder le paquet LOG : {}", e);
+                        return Packet::new(PacketType::Log, b"INVALID_LOG".to_vec());
+                    }
+                };
 
-            return Packet::new(
-                PacketType::Log,
-                b"INVALID_LOG".to_vec(),
-            );
-        }
-    };
+                match log.level {
+                    LogLevel::TRACE => {
+                        trace!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
+                    }
 
-    match log.level {
-        LogLevel::TRACE => {
-            trace!(
-                "[CLIENT] [{}:{}] {}",
-                log.file,
-                log.line,
-                log.message
-            );
-        }
+                    LogLevel::DEBUG => {
+                        debug!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
+                    }
 
-        LogLevel::DEBUG => {
-            debug!(
-                "[CLIENT] [{}:{}] {}",
-                log.file,
-                log.line,
-                log.message
-            );
-        }
+                    LogLevel::INFO => {
+                        info!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
+                    }
 
-        LogLevel::INFO => {
-            info!(
-                "[CLIENT] [{}:{}] {}",
-                log.file,
-                log.line,
-                log.message
-            );
-        }
+                    LogLevel::WARNING => {
+                        warn!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
+                    }
 
-        LogLevel::WARNING => {
-            warn!(
-                "[CLIENT] [{}:{}] {}",
-                log.file,
-                log.line,
-                log.message
-            );
-        }
+                    LogLevel::ERROR => {
+                        error!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
+                    }
+                }
 
-        LogLevel::ERROR => {
-            error!(
-                "[CLIENT] [{}:{}] {}",
-                log.file,
-                log.line,
-                log.message
-            );
-        }
-    }
-
-    Packet::new(
-        PacketType::Log,
-        b"OK".to_vec(),
-    )
+                Packet::new(PacketType::Log, b"OK".to_vec())
             }
             PacketType::Ping => {
-
                 debug!("Ping reçu");
 
-                Packet::new(
-                    PacketType::Ping,
-                    b"PONG".to_vec(),
-                )
-
+                Packet::new(PacketType::Ping, b"PONG".to_vec())
             }
 
             PacketType::Login => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:96:
+                let username = String::from_utf8_lossy(&packet.payload);
 
-                let username =
-                    String::from_utf8_lossy(
-                        &packet.payload
-                    );
+                debug!("Connexion joueur : {}", username);
 
-                debug!(
-                    "Connexion joueur : {}",
-                    username
-                );
-
                 // Ici, plus tard :
                 // - rechercher le client
                 // - rechercher le compte
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:112:
 
                 Packet::new(
                     PacketType::Login,
-                    format!(
-                        "Bienvenue {}",
-                        username
-                    )
-                    .into_bytes(),
+                    format!("Bienvenue {}", username).into_bytes(),
                 )
-
             }
 
             PacketType::Chat => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:125:
+                debug!("Message : {}", String::from_utf8_lossy(&packet.payload));
 
-                debug!(
-                    "Message : {}",
-                    String::from_utf8_lossy(
-                        &packet.payload
-                    )
-                );
-
-                Packet::new(
-                    PacketType::Chat,
-                    packet.payload,
-                )
-
+                Packet::new(PacketType::Chat, packet.payload)
             }
 
             PacketType::Move => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:141:
-
                 debug!("Déplacement reçu");
 
-                Packet::new(
-                    PacketType::Move,
-                    packet.payload,
-                )
-
+                Packet::new(PacketType::Move, packet.payload)
             }
-
         }
-
     }
-
 }
-
-
-        
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/mod.rs:1:
-pub mod packet;
 pub mod client;
-pub mod server;
 pub mod handler;
-
-
+pub mod packet;
+pub mod server;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:1:
 use log::error;
 use std::io;
 
-use tokio::io::{
-    AsyncReadExt,
-    AsyncWriteExt,
-};
-use tokio::net::TcpStream;
 use serde::{Deserialize, Serialize};
+use tokio::io::{AsyncReadExt, AsyncWriteExt};
+use tokio::net::TcpStream;
 
-
 pub const MAX_PACKET_SIZE: usize = 10 * 1024 * 1024;
 
 /// Types de paquets.
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:22:
     Log = 5,
 }
 
-
 #[derive(Debug, Serialize, Deserialize)]
 pub enum LogLevel {
     TRACE,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:32:
     ERROR,
 }
 
-
 #[derive(Debug, Serialize, Deserialize)]
 pub struct ClientLog {
     pub level: LogLevel,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:62:
 }
 
 impl Packet {
-    pub fn new(
-        packet_type: PacketType,
-        payload: Vec<u8>,
-    ) -> Self {
+    pub fn new(packet_type: PacketType, payload: Vec<u8>) -> Self {
         Self {
             packet_type,
             payload,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:74:
 }
 
 /// Envoie un paquet.
-pub async fn send_packet(
-    stream: &mut TcpStream,
-    packet: &Packet,
-) -> io::Result<()> {
-
+pub async fn send_packet(stream: &mut TcpStream, packet: &Packet) -> io::Result<()> {
     let payload_size = 2 + packet.payload.len();
 
     if payload_size > MAX_PACKET_SIZE {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:93:
 
     stream.write_all(&size).await?;
 
-    let packet_type =
-        (packet.packet_type as u16).to_be_bytes();
+    let packet_type = (packet.packet_type as u16).to_be_bytes();
 
     stream.write_all(&packet_type).await?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:104:
 }
 
 /// Reçoit exactement `size` octets.
-async fn recv_exact(
-    stream: &mut TcpStream,
-    size: usize,
-) -> io::Result<Vec<u8>> {
-
+async fn recv_exact(stream: &mut TcpStream, size: usize) -> io::Result<Vec<u8>> {
     let mut buffer = vec![0u8; size];
 
     stream.read_exact(&mut buffer).await?;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:117:
 }
 
 /// Reçoit un paquet.
-pub async fn receive_packet(
-    stream: &mut TcpStream,
-) -> io::Result<Packet> {
-
+pub async fn receive_packet(stream: &mut TcpStream) -> io::Result<Packet> {
     // Taille
     let header = recv_exact(stream, 4).await?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:127:
-    let size = u32::from_be_bytes([
-        header[0],
-        header[1],
-        header[2],
-        header[3],
-    ]) as usize;
+    let size = u32::from_be_bytes([header[0], header[1], header[2], header[3]]) as usize;
 
     if size < 2 {
         error!("paquet invalide");
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:151:
     let data = recv_exact(stream, size).await?;
 
     // Type
-    let packet_type =
-        u16::from_be_bytes([data[0], data[1]]);
+    let packet_type = u16::from_be_bytes([data[0], data[1]]);
 
-    let packet_type =
-        PacketType::from_u16(packet_type)
-            .ok_or_else(|| {
-                error!("Type de paquet inconnu");
-                io::Error::new(
-                    io::ErrorKind::InvalidData,
-                    "Type de paquet inconnu.",
-                )
-            })?;
+    let packet_type = PacketType::from_u16(packet_type).ok_or_else(|| {
+        error!("Type de paquet inconnu");
+        io::Error::new(io::ErrorKind::InvalidData, "Type de paquet inconnu.")
+    })?;
 
     // Payload
     let payload = data[2..].to_vec();
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/server.rs:1:
-use tokio::net::TcpListener;
-use tokio::task;
-use log::{
-    info,
-    error,
-    debug,
-};
 use crate::database::database_manager::DatabaseManager;
 use crate::network::client::Client;
+use log::{debug, error, info};
+use tokio::net::TcpListener;
+use tokio::task;
 
 pub struct Server {
     listener: TcpListener,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/server.rs:14:
 }
 
 impl Server {
-    pub async fn new(
-        address: &str,
-        database: DatabaseManager,
-    ) -> std::io::Result<Self>  {
-
+    pub async fn new(address: &str, database: DatabaseManager) -> std::io::Result<Self> {
         let listener = TcpListener::bind(address)
-    .await
-    .inspect_err(|e| error!("Impossible de démarrer le serveur : {}", e))?;
+            .await
+            .inspect_err(|e| error!("Impossible de démarrer le serveur : {}", e))?;
 
-        Ok(Self {
-        listener,
-        database,
-    })
+        Ok(Self { listener, database })
     }
 
     pub async fn start(&self) {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/server.rs:33:
-
         debug!("==================================");
         debug!("The Last Signal Server");
         debug!("==================================");
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/server.rs:37:
 
-        debug!(
-            "Listening on {}",
-            self.listener.local_addr().unwrap()
-        );
+        debug!("Listening on {}", self.listener.local_addr().unwrap());
 
         loop {
-
             match self.listener.accept().await {
-
                 Ok((stream, address)) => {
-
                     info!("Client connecté : {}", address);
 
                     let pool = self.database.pool().clone();
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/server.rs:52:
 
                     task::spawn(async move {
+                        let mut client = Client::new(stream, pool);
 
-                        let mut client =
-                            Client::new(stream, pool);
-
                         client.run().await;
-
                     });
-
                 }
 
                 Err(e) => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/server.rs:65:
-
-                error!(
-                        "Erreur d'acceptation : {}",
-                        e
-                    );
-
+                    error!("Erreur d'acceptation : {}", e);
                 }
-
             }
-
         }
-
     }
 }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:1:
-use flate2::{
-    write::GzEncoder,
-    Compression,
-};
+use flate2::{Compression, write::GzEncoder};
 use log::info;
 
-
 use std::{
     fs::{self, File},
     io::{self, BufReader},
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:20:
         log_directory: P,
         keep_latest: usize,
     ) -> io::Result<()> {
-
         let log_directory = log_directory.as_ref();
 
         if !log_directory.exists() {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:38:
         });
 
         for file in log_files.into_iter().skip(keep_latest) {
+            let compressed = file.with_extension("log.gz");
 
-            let compressed =
-                file.with_extension("log.gz");
-
             // Déjà compressé
             if compressed.exists() {
                 continue;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:48:
             }
 
-            info!(
-                "[LOGGER] Compression : {}",
-                file.display()
-            );
+            info!("[LOGGER] Compression : {}", file.display());
 
             Self::compress_file(&file, &compressed)?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:60:
         Ok(())
     }
 
-    fn collect_logs(
-        directory: &Path,
-    ) -> io::Result<Vec<PathBuf>> {
-
+    fn collect_logs(directory: &Path) -> io::Result<Vec<PathBuf>> {
         let mut files = Vec::new();
 
         for entry in fs::read_dir(directory)? {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:70:
-
             let entry = entry?;
 
             let path = entry.path();
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:76:
                 continue;
             }
 
-            let Some(name) =
-                path.file_name().and_then(|n| n.to_str())
-            else {
+            let Some(name) = path.file_name().and_then(|n| n.to_str()) else {
                 continue;
             };
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:95:
         Ok(files)
     }
 
-    fn compress_file(
-        input: &Path,
-        output: &Path,
-    ) -> io::Result<()> {
-
+    fn compress_file(input: &Path, output: &Path) -> io::Result<()> {
         let input_file = File::open(input)?;
 
         let output_file = File::create(output)?;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:106:
 
-        let mut encoder =
-            GzEncoder::new(
-                output_file,
-                Compression::default(),
-            );
+        let mut encoder = GzEncoder::new(output_file, Compression::default());
 
-        let mut reader =
-            BufReader::new(input_file);
+        let mut reader = BufReader::new(input_file);
 
-        io::copy(
-            &mut reader,
-            &mut encoder,
-        )?;
+        io::copy(&mut reader, &mut encoder)?;
 
         encoder.finish()?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/compressor.rs:123:
         Ok(())
     }
 
-    fn modified(
-        path: &Path,
-    ) -> std::time::SystemTime {
-
+    fn modified(path: &Path) -> std::time::SystemTime {
         fs::metadata(path)
             .and_then(|m| m.modified())
             .unwrap_or(std::time::UNIX_EPOCH)
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:1:
 use flexi_logger::{
-    Cleanup,
-    Criterion,
-    DeferredNow,
-    Duplicate,
-    FileSpec,
-    Logger,
-    Naming,
-    Record,
+    Cleanup, Criterion, DeferredNow, Duplicate, FileSpec, Logger, Naming, Record,
     writers::LogWriter,
 };
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:13:
-
-
 use sqlx::SqlitePool;
 
 use std::io::Write;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:22:
 
 use crate::utils::logger::compressor::LogCompressor;
 
-
 // ============================================================
 // LOG DESTINÉ À SQLITE
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:34:
     message: String,
 }
 
-
 // ============================================================
 // COMMANDES DU WORKER DATABASE
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:44:
     Log(DatabaseLog),
 }
 
-
 // ============================================================
 // WRITER SQLITE
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:54:
 }
 
 impl DatabaseWriter {
-    fn new(
-        sender: mpsc::UnboundedSender<DatabaseCommand>,
-    ) -> Self {
+    fn new(sender: mpsc::UnboundedSender<DatabaseCommand>) -> Self {
         Self { sender }
     }
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:63:
 
 impl LogWriter for DatabaseWriter {
-
-    fn write(
-        &self,
-        _now: &mut DeferredNow,
-        record: &Record<'_>,
-    ) -> std::io::Result<()> {
-
+    fn write(&self, _now: &mut DeferredNow, record: &Record<'_>) -> std::io::Result<()> {
         let module = record
             .module_path()
             .unwrap_or_else(|| record.target())
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:83:
         // On envoie le log au worker SQLite.
         //
         // Le logger ne bloque donc pas en attendant SQLite.
-        let _ = self.sender.send(
-            DatabaseCommand::Log(log)
-        );
+        let _ = self.sender.send(DatabaseCommand::Log(log));
 
         Ok(())
     }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:95:
     }
 }
 
-
 // ============================================================
 // FORMAT DU FICHIER LOG
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:105:
     now: &mut DeferredNow,
     record: &Record<'_>,
 ) -> std::io::Result<()> {
-
     let file = record
         .file()
         .and_then(|f| Path::new(f).file_name())
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:123:
     )
 }
 
-
 // ============================================================
 // LOGGER
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:131:
 pub struct ServerLogger;
 
 impl ServerLogger {
-
     // ========================================================
     // INITIALISATION
     // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:138:
 
     pub fn init() {
-
         let log_dir = PathBuf::from("../logs");
 
         // ----------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:144:
         // Canal entre flexi_logger et le worker SQLite
         // ----------------------------------------------------
 
-        let (sender, mut receiver) =
-            mpsc::unbounded_channel::<DatabaseCommand>();
+        let (sender, mut receiver) = mpsc::unbounded_channel::<DatabaseCommand>();
 
-
         // ----------------------------------------------------
         // Worker SQLite
         // ----------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:154:
 
         tokio::spawn(async move {
-
             let mut pool: Option<SqlitePool> = None;
 
             // Logs produits avant que la DB soit disponible.
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:165:
             // mémoire infinie si la DB ne devient jamais disponible.
             const MAX_PENDING_LOGS: usize = 1000;
 
-
             while let Some(command) = receiver.recv().await {
-
                 match command {
-
                     // ----------------------------------------
                     // Base de données disponible
                     // ----------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:176:
-
                     DatabaseCommand::SetPool(new_pool) => {
-
                         pool = Some(new_pool);
 
-
                         // ------------------------------------
                         // Écriture des logs en attente
                         // ------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:185:
 
                         if let Some(pool) = &pool {
-
                             for log in pending_logs.drain(..) {
-
-                                if let Err(error) =
-                                    Self::insert_log(
-                                        pool,
-                                        &log,
-                                    )
-                                    .await
-                                {
-                                    eprintln!(
-                                        "Erreur écriture log SQLite : {}",
-                                        error
-                                    );
+                                if let Err(error) = Self::insert_log(pool, &log).await {
+                                    eprintln!("Erreur écriture log SQLite : {}", error);
                                 }
                             }
                         }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:204:
                     }
 
-
                     // ----------------------------------------
                     // Nouveau log
                     // ----------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:210:
-
                     DatabaseCommand::Log(log) => {
-
                         match &pool {
-
                             // DB disponible
                             Some(pool) => {
-
-                                if let Err(error) =
-                                    Self::insert_log(
-                                        pool,
-                                        &log,
-                                    )
-                                    .await
-                                {
-                                    eprintln!(
-                                        "Erreur écriture log SQLite : {}",
-                                        error
-                                    );
+                                if let Err(error) = Self::insert_log(pool, &log).await {
+                                    eprintln!("Erreur écriture log SQLite : {}", error);
                                 }
                             }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:232:
-
                             // DB pas encore disponible
                             None => {
-
-                                if pending_logs.len()
-                                    >= MAX_PENDING_LOGS
-                                {
+                                if pending_logs.len() >= MAX_PENDING_LOGS {
                                     // On supprime le plus ancien
                                     // pour éviter une croissance
                                     // infinie.
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:250:
             }
         });
 
-
         // ----------------------------------------------------
         // Writer SQLite
         // ----------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:257:
 
-        let database_writer =
-            DatabaseWriter::new(sender.clone());
+        let database_writer = DatabaseWriter::new(sender.clone());
 
-
         // ----------------------------------------------------
         // Flexi logger
         // ----------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:265:
 
         Logger::try_with_str("trace,sqlx=warn")
             .unwrap()
-
             // Fichier + SQLite
             .log_to_file_and_writer(
                 FileSpec::default()
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:272:
                     .directory(log_dir)
                     .basename("the_last_signal"),
-
                 Box::new(database_writer),
             )
-
             // stdout
             .duplicate_to_stdout(Duplicate::All)
-
             // Format du fichier
             .format(log_format)
-
             // Rotation à 10 MB
             .rotate(
                 Criterion::Size(10_000_000),
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:287:
                 Naming::Numbers,
                 Cleanup::KeepLogFiles(100),
             )
-
             // Ajouter aux fichiers existants
             .append()
-
             // Démarrage
             .start()
             .unwrap();
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:297:
 
-
         // ----------------------------------------------------
         // Compression
         // ----------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:302:
 
         Self::compress();
 
-
         // ----------------------------------------------------
         // Stockage du sender
         // ----------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:314:
         DatabaseSender::set(sender);
     }
 
-
     // ========================================================
     // CONNEXION À LA DATABASE
     // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:321:
 
-    pub fn set_database(
-        pool: SqlitePool,
-    ) {
-
-        if let Some(sender) =
-            DatabaseSender::get()
-        {
-            let _ = sender.send(
-                DatabaseCommand::SetPool(pool)
-            );
-        }
-        else {
-
+    pub fn set_database(pool: SqlitePool) {
+        if let Some(sender) = DatabaseSender::get() {
+            let _ = sender.send(DatabaseCommand::SetPool(pool));
+        } else {
             eprintln!(
                 "Impossible de connecter le logger à SQLite : \
                  ServerLogger::init() n'a pas été appelé."
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:339:
         }
     }
 
-
     // ========================================================
     // INSERTION SQLITE
     // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:346:
 
-    async fn insert_log(
-        pool: &SqlitePool,
-        log: &DatabaseLog,
-    ) -> Result<(), sqlx::Error> {
-
+    async fn insert_log(pool: &SqlitePool, log: &DatabaseLog) -> Result<(), sqlx::Error> {
         sqlx::query(
             r#"
             INSERT INTO logs (
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:368:
         Ok(())
     }
 
-
     // ========================================================
     // COMPRESSION
     // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:375:
 
     pub fn compress() {
-
-        if let Err(error) =
-            LogCompressor::compress_old_logs(
-                "logs",
-                10,
-            )
-        {
-            eprintln!(
-                "Compression impossible : {}",
-                error
-            );
+        if let Err(error) = LogCompressor::compress_old_logs("logs", 10) {
+            eprintln!("Compression impossible : {}", error);
         }
     }
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:391:
 
-
 // ============================================================
 // STOCKAGE GLOBAL DU SENDER
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:396:
 
 struct DatabaseSender;
 
-static SENDER:
-    std::sync::OnceLock<
-        Arc<RwLock<
-            Option<mpsc::UnboundedSender<DatabaseCommand>>
-        >>
-    >
-    = std::sync::OnceLock::new();
+static SENDER: std::sync::OnceLock<Arc<RwLock<Option<mpsc::UnboundedSender<DatabaseCommand>>>>> =
+    std::sync::OnceLock::new();
 
-
 impl DatabaseSender {
+    fn set(sender: mpsc::UnboundedSender<DatabaseCommand>) {
+        let storage = Arc::new(RwLock::new(Some(sender)));
 
-    fn set(
-        sender: mpsc::UnboundedSender<DatabaseCommand>,
-    ) {
-
-        let storage =
-            Arc::new(
-                RwLock::new(Some(sender))
-            );
-
         let _ = SENDER.set(storage);
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/logger.rs:422:
-
-    fn get()
-        -> Option<
-            mpsc::UnboundedSender<DatabaseCommand>
-        >
-    {
+    fn get() -> Option<mpsc::UnboundedSender<DatabaseCommand>> {
         SENDER
             .get()
-            .and_then(|storage| {
-                storage
-                    .read()
-                    .ok()
-                    .and_then(|guard| guard.clone())
-            })
+            .and_then(|storage| storage.read().ok().and_then(|guard| guard.clone()))
     }
-            }
+}
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/logger/mod.rs:1:
-pub mod logger;
-pub mod context;
 pub mod compressor;
+pub mod context;
+pub mod logger;
 pub mod macros;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/mod.rs:1:
-pub mod save;
 pub mod logger;
-pub mod vault;
 pub mod password;
+pub mod save;
+pub mod vault;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/password.rs:1:
 use argon2::{
-    password_hash::{
-        rand_core::OsRng,
-        PasswordHash,
-        PasswordHasher,
-        PasswordVerifier,
-        SaltString,
-    },
     Argon2,
+    password_hash::{PasswordHash, PasswordHasher, PasswordVerifier, SaltString, rand_core::OsRng},
 };
 
 /// Hash un mot de passe.
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/password.rs:23:
 }
 
 /// Vérifie un mot de passe avec un hash existant.
-pub fn verify_password(
-    password: &str,
-    password_hash: &str,
-) -> bool {
+pub fn verify_password(password: &str, password_hash: &str) -> bool {
     let parsed_hash = match PasswordHash::new(password_hash) {
         Ok(hash) => hash,
         Err(_) => return false,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/vault.rs:8:
         Err(_) => fs::read_to_string("../security/master.key")?,
     };
 
-    let cipher = Fernet::new(key.trim())
-        .ok_or("Clé Fernet invalide")?;
+    let cipher = Fernet::new(key.trim()).ok_or("Clé Fernet invalide")?;
 
     let encrypted = fs::read_to_string("../security/vault.enc")?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:1:
+use log::{debug, info};
+use the_last_signal_server::database::{database_manager::DatabaseManager, migrations};
 use the_last_signal_server::network::packet::PacketType;
-use the_last_signal_server::database::{
-    database_manager::DatabaseManager,
-    migrations,
-};
-use log::{debug,info};
 use the_last_signal_server::network::server::Server;
 use the_last_signal_server::utils::logger::logger::ServerLogger;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:10:
 #[tokio::main]
 async fn main() -> Result<(), Box<dyn std::error::Error>> {
     let _guard = ServerLogger::init();
-    
-    
-    let database_url = 
-        std::env::var("DATABASE_URL")?;
-    let database_path =
-        std::env::var("DATABASE_PATH")?;
 
-    let database =
-        DatabaseManager::new(&database_path,& database_url)
-            .await?;
+    let database_url = std::env::var("DATABASE_URL")?;
+    let database_path = std::env::var("DATABASE_PATH")?;
 
+    let database = DatabaseManager::new(&database_path, &database_url).await?;
+
     database.ping().await?;
 
-    migrations::run(&database.pool())
-        .await?;
+    migrations::run(&database.pool()).await?;
 
     info!("Base SQLite prête.");
     ServerLogger::set_database(database.pool().clone());
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:31:
-    
 
-    let server =
-        Server::new(
-            "127.0.0.1:5000",
-            database,
-        )
-        .await?;
+    let server = Server::new("127.0.0.1:5000", database).await?;
 
-
     server.start().await;
-    
 
     Ok(())
 }
⚠️ cargo fmt --check failed

## Cargo clippy

## Cargo test
   Compiling libc v0.2.189
   Compiling cfg-if v1.0.4
   Compiling typenum v1.20.1
   Compiling rand_core v0.10.1
   Compiling zerofrom v0.1.8
   Compiling stable_deref_trait v1.2.1
   Compiling smallvec v1.15.2
   Compiling yoke v0.8.3
   Compiling zerovec v0.11.7
   Compiling pin-project-lite v0.2.17
   Compiling memchr v2.8.3
   Compiling tinystr v0.8.4
   Compiling hybrid-array v0.4.14
   Compiling jobserver v0.1.35
   Compiling getrandom v0.4.3
   Compiling futures-core v0.3.34
   Compiling cc v1.4.3
   Compiling writeable v0.6.4
   Compiling once_cell v1.21.4
   Compiling scopeguard v1.2.0
   Compiling litemap v0.8.3
   Compiling lock_api v0.4.14
   Compiling crypto-common v0.2.2
   Compiling icu_locale_core v2.3.0
   Compiling zeroize v1.9.0
   Compiling potential_utf v0.1.6
   Compiling zerotrie v0.2.5
   Compiling utf8_iter v1.0.4
   Compiling icu_collections v2.3.0
   Compiling icu_provider v2.3.0
   Compiling serde_core v1.0.229
   Compiling cmov v0.5.4
   Compiling num-traits v0.2.19
   Compiling ctutils v0.4.2
   Compiling icu_properties_data v2.3.0
   Compiling parking_lot_core v0.9.12
   Compiling icu_normalizer_data v2.3.0
   Compiling block-buffer v0.12.1
   Compiling socket2 v0.6.5
   Compiling mio v1.2.2
   Compiling bytes v1.12.1
   Compiling futures-sink v0.3.34
   Compiling equivalent v1.0.2
   Compiling parking_lot v0.12.5
   Compiling icu_normalizer v2.3.0
   Compiling icu_properties v2.3.0
   Compiling cpufeatures v0.3.0
   Compiling iana-time-zone v0.1.65
   Compiling cpufeatures v0.2.17
   Compiling generic-array v0.14.7
   Compiling slab v0.4.12
   Compiling percent-encoding v2.3.2
   Compiling serde v1.0.229
   Compiling hashbrown v0.17.1
   Compiling futures-task v0.3.34
   Compiling futures-io v0.3.34
   Compiling idna_adapter v1.2.2
   Compiling subtle v2.6.1
   Compiling allocator-api2 v0.2.21
   Compiling log v0.4.33
   Compiling foldhash v0.2.0
   Compiling indexmap v2.14.0
   Compiling idna v1.1.0
   Compiling futures-util v0.3.34
   Compiling hashbrown v0.16.1
   Compiling form_urlencoded v1.2.2
   Compiling zmij v1.0.23
   Compiling crossbeam-utils v0.8.22
   Compiling crc-catalog v2.5.0
   Compiling parking v2.2.1
   Compiling itoa v1.0.18
   Compiling serde_json v1.0.151
   Compiling event-listener v5.4.2
   Compiling crossbeam-queue v0.3.13
   Compiling crc v3.4.0
   Compiling url v2.5.8
   Compiling hashlink v0.11.1
   Compiling either v1.17.0
   Compiling block-buffer v0.10.4
   Compiling crypto-common v0.1.7
   Compiling futures-intrusive v0.5.0
   Compiling const-oid v0.10.2
   Compiling digest v0.11.3
   Compiling digest v0.10.7
   Compiling tokio v1.53.1
   Compiling libsqlite3-sys v0.37.0
   Compiling zstd-sys v2.0.16+zstd.1.5.7
   Compiling spin v0.9.9
   Compiling inout v0.2.2
   Compiling tracing-core v0.1.36
   Compiling errno v0.3.14
   Compiling signal-hook-registry v1.4.8
   Compiling tracing v0.1.44
   Compiling flume v0.12.0
   Compiling sha2 v0.10.9
   Compiling futures-executor v0.3.34
   Compiling chrono v0.4.45
   Compiling futures-channel v0.3.34
   Compiling atoi v2.0.0
   Compiling openssl-sys v0.9.117
   Compiling tokio-stream v0.1.19
   Compiling aho-corasick v1.1.5
   Compiling regex-syntax v0.8.11
   Compiling cpubits v0.1.1
   Compiling regex-automata v0.4.18
   Compiling sqlx-core v0.9.0
   Compiling thiserror v2.0.20
   Compiling cipher v0.5.2
   Compiling getrandom v0.2.17
   Compiling simd-adler32 v0.3.10
   Compiling base64 v0.22.1
   Compiling bitflags v2.13.1
   Compiling zstd-safe v7.2.4
   Compiling sqlx-sqlite v0.9.0
   Compiling crc32fast v1.5.0
   Compiling universal-hash v0.6.1
   Compiling uuid v1.24.1
   Compiling foreign-types-shared v0.1.1
   Compiling hex v0.4.3
   Compiling adler2 v2.0.1
   Compiling sqlx-macros-core v0.9.0
   Compiling miniz_oxide v0.8.9
   Compiling openssl v0.10.81
   Compiling foreign-types v0.3.2
   Compiling polyval v0.7.3
   Compiling rand_core v0.6.4
   Compiling aes v0.9.2
   Compiling sha2 v0.11.0
   Compiling hmac v0.13.0
   Compiling base64ct v1.8.3
   Compiling num-conv v0.2.2
   Compiling tinyvec_macros v0.1.1
   Compiling deranged v0.5.8
   Compiling bumpalo v3.20.3
   Compiling nu-ansi-term v0.50.3
   Compiling powerfmt v0.2.0
   Compiling libbz2-rs-sys v0.2.5
   Compiling zlib-rs v0.6.7
   Compiling linux-raw-sys v0.12.1
   Compiling time-core v0.1.9
   Compiling lazy_static v1.5.0
   Compiling sharded-slab v0.1.7
   Compiling time v0.3.55
   Compiling rustix v1.1.4
   Compiling bzip2 v0.6.1
   Compiling zopfli v0.8.3
   Compiling lzma-rust2 v0.16.5
   Compiling tinyvec v1.12.0
   Compiling password-hash v0.5.0
   Compiling flate2 v1.1.9
   Compiling pbkdf2 v0.13.0
   Compiling zstd v0.13.3
   Compiling sqlx-macros v0.9.0
   Compiling ghash v0.6.0
   Compiling ctr v0.10.1
   Compiling matchers v0.2.0
   Compiling regex v1.13.1
   Compiling tracing-log v0.2.0
   Compiling aead v0.6.1
   Compiling blake2 v0.10.6
   Compiling sha1 v0.11.0
   Compiling chacha20 v0.10.1
   Compiling thread_local v1.1.10
   Compiling same-file v1.0.6
   Compiling ppmd-rust v1.4.0
   Compiling fastrand v2.5.0
   Compiling deflate64 v0.1.12
   Compiling typed-path v0.12.3
   Compiling constant_time_eq v0.4.2
   Compiling byteorder v1.5.0
   Compiling tempfile v3.27.0
   Compiling tracing-subscriber v0.3.23
   Compiling walkdir v2.5.0
   Compiling zip v8.6.0
   Compiling fernet v0.2.2
   Compiling rand v0.10.2
   Compiling argon2 v0.5.3
   Compiling aes-gcm v0.11.0
   Compiling sqlx v0.9.0
   Compiling flexi_logger v0.31.10
   Compiling unicode-normalization v0.1.25
   Compiling anyhow v1.0.104
   Compiling base64 v0.23.1
   Compiling the-last-signal-server v0.1.0 (/home/runner/work/The-last-signal-/The-last-signal-/server_rust)
warning: unused import: `Error`
 --> src/database/database_manager.rs:6:5
  |
6 |     Error,
  |     ^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: unused import: `Rng`
 --> src/gameplay/dice.rs:1:12
  |
1 | use rand::{Rng,RngExt};
  |            ^^^

warning: unused import: `log::debug`
 --> src/gameplay/tresor.rs:4:5
  |
4 | use log::debug;
  |     ^^^^^^^^^^

warning: unused variable: `pool`
   --> src/database/database_manager.rs:108:25
    |
108 |                     let pool =Self::create_database(database_url).await?;
    |                         ^^^^ help: if this is intentional, prefix it with an underscore: `_pool`
    |
    = note: `#[warn(unused_variables)]` (part of `#[warn(unused)]`) on by default

warning: fields `pool`, `client_id`, and `account_id` are never read
  --> src/network/client.rs:17:5
   |
14 | pub struct Client {
   |            ------ fields in this struct
...
17 |     pool: SqlitePool,
   |     ^^^^
...
21 |     client_id: Option<i64>,
   |     ^^^^^^^^^
22 |
23 |     account_id: Option<Uuid>,
   |     ^^^^^^^^^^
   |
   = note: `#[warn(dead_code)]` (part of `#[warn(unused)]`) on by default

warning: constant `PO` is never used
 --> src/gameplay/tresor.rs:9:7
  |
9 | const PO: u32 = PA * 10;
  |       ^^

warning: constant `PP` is never used
  --> src/gameplay/tresor.rs:10:7
   |
10 | const PP: u32 = PO * 10;
   |       ^^

warning: `the-last-signal-server` (lib) generated 7 warnings (run `cargo fix --lib -p the-last-signal-server` to apply 4 suggestions)
warning: unused import: `the_last_signal_server::network::packet::PacketType`
 --> src/main.rs:1:5
  |
1 | use the_last_signal_server::network::packet::PacketType;
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: unused import: `debug`
 --> src/main.rs:6:11
  |
6 | use log::{debug,info};
  |           ^^^^^

warning: `the-last-signal-server` (bin "the-last-signal-server" test) generated 2 warnings (1 duplicate) (run `cargo fix --bin "the-last-signal-server" -p the-last-signal-server --tests` to apply 1 suggestion)
warning: `the-last-signal-server` (lib test) generated 7 warnings (7 duplicates)
warning: `the-last-signal-server` (bin "the-last-signal-server") generated 2 warnings (1 duplicate) (run `cargo fix --bin "the-last-signal-server" -p the-last-signal-server` to apply 1 suggestion)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 33.77s
     Running unittests src/lib.rs (server_rust/target/debug/deps/the_last_signal_server-5b4e47ab932b9cea)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (server_rust/target/debug/deps/the_last_signal_server-17c87c6de774b290)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/integration_test.rs (server_rust/target/debug/deps/integration_test-7edf23c0e7a3275d)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests the_last_signal_server

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

