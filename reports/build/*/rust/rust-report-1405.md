# Rust Report

Run : 1405
Branch : main
Commit : 87656f7533283896461efd9b589ab03e57abbe53
Date : Sun Aug 30 20:04:12 UTC 2026


## Cargo fmt
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:1:
-use std::str::FromStr;
 use std::path::Path;
+use std::str::FromStr;
 
 use sqlx::{
-    sqlite::{SqliteConnectOptions, SqlitePool, SqlitePoolOptions},
     Error,
+    sqlite::{SqliteConnectOptions, SqlitePool, SqlitePoolOptions},
 };
 
-
-
 pub struct DatabaseManager {
     pool: SqlitePool,
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:14:
 
-
 impl DatabaseManager {
     /// Vérifie si une base SQLite existante est corrompue.
     ///
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:20:
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
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:31:
-        let integrity: String = sqlx::query_scalar(
-            "PRAGMA integrity_check"
-        )
-        .fetch_one(&pool)
-        .await?;
+        let integrity: String = sqlx::query_scalar("PRAGMA integrity_check")
+            .fetch_one(&pool)
+            .await?;
 
         pool.close().await;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:40:
     }
 
     /// Crée ou ouvre la base SQLite.
-    pub async fn create_database(
-        database_url: &str,
-    ) -> Result<SqlitePool, sqlx::Error> {
-        let options = SqliteConnectOptions::from_str(database_url)?
-            .create_if_missing(true);
+    pub async fn create_database(database_url: &str) -> Result<SqlitePool, sqlx::Error> {
+        let options = SqliteConnectOptions::from_str(database_url)?.create_if_missing(true);
 
         // Use SqlitePoolOptions to limit concurrent connections for SQLite.
         // SQLite supports a single writer at a time; limiting the pool helps
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:58:
         sqlx::query("PRAGMA journal_mode = WAL;")
             .execute(&pool)
             .await?;
-        
-        sqlx::query("PRAGMA busy_timeout = 30000")  // 30 secondes
+
+        sqlx::query("PRAGMA busy_timeout = 30000") // 30 secondes
             .execute(&pool)
             .await?;
-        
-        sqlx::query("PRAGMA synchronous = NORMAL")  // Plus rapide
+
+        sqlx::query("PRAGMA synchronous = NORMAL") // Plus rapide
             .execute(&pool)
             .await?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:77:
         &self.pool
     }
     pub async fn ping(&self) -> Result<(), sqlx::Error> {
+        sqlx::query("SELECT 1").execute(&self.pool).await?;
 
-        sqlx::query("SELECT 1")
-            .execute(&self.pool)
-            .await?;
-
         Ok(())
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:88:
-
-
-    
-
-    pub async fn new(
-        database_path: &str,
-        database_url: &str,
-    ) -> Result<Self, sqlx::Error> {
+    pub async fn new(database_path: &str, database_url: &str) -> Result<Self, sqlx::Error> {
         // --------------------------------------------------
         // 1. Récupérer le chemin réel de la DB
         // --------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:100:
         let path = database_path
             .strip_prefix("sqlite:")
             .unwrap_or(database_path);
-        let database_file = database_url
-            .strip_prefix("sqlite:")
-            .unwrap_or(database_url);
-        
-       std::fs::create_dir_all(path)
-        .map_err(sqlx::Error::Io)?;
-      let mut pool =Self::create_database(database_url).await?;
-        
+        let database_file = database_url.strip_prefix("sqlite:").unwrap_or(database_url);
 
-        
-        
-        
+        std::fs::create_dir_all(path).map_err(sqlx::Error::Io)?;
+        let mut pool = Self::create_database(database_url).await?;
 
         // --------------------------------------------------
         // 3. Vérifier la DB si elle existe déjà
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:125:
                          Suppression et recréation..."
                     );
 
-                    std::fs::remove_file(database_file)
-                        .map_err(sqlx::Error::Io)?;
-                    pool =Self::create_database(database_url).await?;
-
-
-                    
+                    std::fs::remove_file(database_file).map_err(sqlx::Error::Io)?;
+                    pool = Self::create_database(database_url).await?;
                 }
 
                 Ok(false) => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:148:
                     return Err(error);
                 }
             }
-        } 
+        }
 
-        
         // --------------------------------------------------
         // 5. Retourner la structure
         // --------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/database_manager.rs:157:
 
-        Ok(Self {
-            pool,
-        })
+        Ok(Self { pool })
     }
 }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/migrations.rs:1:
+use crate::utils::account_creator::create_account;
+use crate::utils::password::hash_password;
+use crate::utils::vault::decrypt_vault;
 use log::debug;
 use sqlx::SqlitePool;
-use crate::utils::vault::decrypt_vault;
-use crate::utils::password::hash_password;
-use crate::utils::account_creator::create_account;
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
     create_account(
-    pool,
-    "Admin@gmail.com",
-    &password1_hash,
+        pool,
+        "Admin@gmail.com",
+        &password1_hash,
         "Cyril",
         "Dev",
         Some("DISCONNECTED"),
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/migrations.rs:50:
-)
-.await?;
+    )
+    .await?;
 
-create_account(
-    pool,
-    "Superadmin@gmail.com",
-    &password2_hash,
-    "Morgan",
-    "SuperDev",
-    Some("DISCONNECTED"),
-)
-.await?;
+    create_account(
+        pool,
+        "Superadmin@gmail.com",
+        &password2_hash,
+        "Morgan",
+        "SuperDev",
+        Some("DISCONNECTED"),
+    )
+    .await?;
 
     Ok(())
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/migrations.rs:65:
-
-
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/database/mod.rs:1:
 pub mod database_manager;
 pub mod migrations;
-
-
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/dice.rs:3:
 pub fn jet_de_des(face: u32, nb: u32) -> u32 {
     let mut rng = rand::rng();
 
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
+use rand::{Rng, RngExt};
 use sqlx::SqlitePool;
 use std::collections::HashMap;
-use crate::gameplay::dice::jet_de_des;
 
-
 const PA: u32 = 1;
 const PO: u32 = PA * 10;
 const PP: u32 = PO * 10;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:21:
 
 #[derive(Debug, Clone)]
 pub struct Tresor {
-    
     pub loot_par_niveau: HashMap<u32, Loot>,
 
     pub objets_garantis: HashMap<u32, HashMap<String, u32>>,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:31:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:147:
         // Niveau 1
         let mut niveau_1 = HashMap::new();
 
-        niveau_1.insert(
-            "argent".to_string(),
-            jet_de_des(6, 2) * PA,
-        );
+        niveau_1.insert("argent".to_string(), jet_de_des(6, 2) * PA);
 
         niveau_1.insert("torche".to_string(), 2);
         niveau_1.insert("sac".to_string(), 3);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:163:
 
         // 17 chances sur 20 : pain
         if jet_de_des(20, 1) >= 4 {
-            niveau_1.insert(
-                "pain".to_string(),
-                rng.random_range(3..=5),
-            );
+            niveau_1.insert("pain".to_string(), rng.random_range(3..=5));
         }
 
         objets_garantis.insert(1, niveau_1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:174:
         // Niveau 2
         let mut niveau_2 = HashMap::new();
 
-        niveau_2.insert(
-            "argent".to_string(),
-            jet_de_des(6, 4) * PA,
-        );
+        niveau_2.insert("argent".to_string(), jet_de_des(6, 4) * PA);
 
         niveau_2.insert("torche".to_string(), 1);
         niveau_2.insert("sac".to_string(), 2);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:192:
         // Niveau 3
         let mut niveau_3 = HashMap::new();
 
-        niveau_3.insert(
-            "argent".to_string(),
-            jet_de_des(6, 1) * 10 * PA,
-        );
+        niveau_3.insert("argent".to_string(), jet_de_des(6, 1) * 10 * PA);
 
         niveau_3.insert("torche".to_string(), 2);
         niveau_3.insert("sac".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:210:
         // Niveau 4
         let mut niveau_4 = HashMap::new();
 
-        niveau_4.insert(
-            "argent".to_string(),
-            jet_de_des(6, 2) * 10 * PA,
-        );
+        niveau_4.insert("argent".to_string(), jet_de_des(6, 2) * 10 * PA);
 
         if jet_de_des(20, 1) >= 12 {
             niveau_4.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:224:
         // Niveau 5
         let mut niveau_5 = HashMap::new();
 
-        niveau_5.insert(
-            "argent".to_string(),
-            jet_de_des(6, 3) * 10 * PA,
-        );
+        niveau_5.insert("argent".to_string(), jet_de_des(6, 3) * 10 * PA);
 
         if jet_de_des(20, 1) >= 10 {
             niveau_5.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:236:
         objets_garantis.insert(5, niveau_5);
         let mut niveau_6 = HashMap::new();
 
-        niveau_6.insert(
-            "argent".to_string(),
-            jet_de_des(6, 4) * 10 * PA,
-        );
+        niveau_6.insert("argent".to_string(), jet_de_des(6, 4) * 10 * PA);
 
         if jet_de_des(20, 1) >= 8 {
             niveau_6.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:248:
         objets_garantis.insert(6, niveau_6);
         let mut niveau_7 = HashMap::new();
 
-        niveau_7.insert(
-            "argent".to_string(),
-            jet_de_des(6, 5) * 10 * PA,
-        );
+        niveau_7.insert("argent".to_string(), jet_de_des(6, 5) * 10 * PA);
 
         if jet_de_des(20, 1) >= 6 {
             niveau_7.insert("gemmes".to_string(), 1);
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:283:
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
+            "Artefact admin".to_string(),
+            HashMap::from([("livre enchant".to_string(), 100.0)]),
+        );
         sous_loot.insert(
-    "équi".to_string(),
-    HashMap::from([
-        ("armes".to_string(), 20.0),
-        ("outils".to_string(), 20.0),
-        ("armure".to_string(), 20.0),
-        ("véhicules".to_string(), 20.0),
-        ("batiments".to_string(), 20.0),
-        
-        
-    ]),
-);
-            
+            "équi".to_string(),
+            HashMap::from([
+                ("armes".to_string(), 20.0),
+                ("outils".to_string(), 20.0),
+                ("armure".to_string(), 20.0),
+                ("véhicules".to_string(), 20.0),
+                ("batiments".to_string(), 20.0),
+            ]),
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:412:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:593:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:666:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:696:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:779:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:849:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/tresor.rs:879:
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
 use tokio::{
     io::AsyncWriteExt,
     net::TcpStream,
-    time::{interval, Duration},
+    time::{Duration, interval},
 };
 
 use sqlx::SqlitePool;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:8:
 use uuid::Uuid;
 
-use log::{
-    debug,
-    error,
-    info,
-};
+use log::{debug, error, info};
 
 use crate::network::handler::PacketHandler;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:18:
-use crate::network::packet::{
-    receive_packet,
-    send_packet,
-    BanInfo,
-    BanType,
-    Packet,
-    PacketType,
-};
+use crate::network::packet::{BanInfo, BanType, Packet, PacketType, receive_packet, send_packet};
 
-
 pub struct Client {
-
     stream: TcpStream,
 
     pool: SqlitePool,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:40:
     account_id: Option<i64>,
 }
 
-
 impl Client {
-
     // ============================================================
     // CONSTRUCTEUR
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:49:
 
-    pub fn new(
-        stream: TcpStream,
-        pool: SqlitePool,
-    ) -> Self {
-
+    pub fn new(stream: TcpStream, pool: SqlitePool) -> Self {
         Self {
             stream,
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:67:
         }
     }
 
-
     // ============================================================
     // BOUCLE PRINCIPALE
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:74:
 
     pub async fn run(&mut self) {
-
         let peer = self
             .stream
             .peer_addr()
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:80:
             .map(|addr| addr.to_string())
             .unwrap_or_else(|_| "adresse inconnue".to_string());
 
+        info!("Client connecté : {} | Session : {}", peer, self.session_id);
 
-        info!(
-            "Client connecté : {} | Session : {}",
-            peer,
-            self.session_id
-        );
-
-
         // --------------------------------------------------------
         // Timer de vérification du ban
         // --------------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:94:
 
-        let mut ban_checker =
-            interval(Duration::from_secs(1));
+        let mut ban_checker = interval(Duration::from_secs(1));
 
-
         // interval() déclenche immédiatement son premier tick.
         //
         // On le consomme donc ici pour que la première véritable
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:102:
         // vérification ait lieu après 1 seconde.
         ban_checker.tick().await;
 
-
         // ========================================================
         // BOUCLE
         // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:109:
 
         loop {
-
             tokio::select! {
 
                 // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:313:
             }
         }
 
-
         // ========================================================
         // FIN DE SESSION
         // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:320:
 
         self.mark_disconnected().await;
 
-
-        info!(
-            "Fin de session : {}",
-            self.session_id
-        );
+        info!("Fin de session : {}", self.session_id);
     }
 
-
     // ============================================================
     // RÉCUPÉRATION DES INFORMATIONS DE BAN
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:334:
 
-    pub async fn get_ban_info(
-        &self,
-    ) -> Result<Option<BanInfo>, sqlx::Error> {
+    pub async fn get_ban_info(&self) -> Result<Option<BanInfo>, sqlx::Error> {
+        let user_id = match self.user_id() {
+            Some(id) => id,
 
-        let user_id =
-            match self.user_id() {
+            None => {
+                return Ok(None);
+            }
+        };
 
-                Some(id) => id,
-
-                None => {
-                    return Ok(None);
-                }
-            };
-
-
         // ========================================================
         // BAN PERMANENT
         // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:353:
 
-        if let Some((reason,)) =
-            sqlx::query_as::<_, (Option<String>,)>(
-                r#"
+        if let Some((reason,)) = sqlx::query_as::<_, (Option<String>,)>(
+            r#"
                 SELECT raison
                 FROM bansperm
                 WHERE user_id = ?
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:360:
                 LIMIT 1
-                "#
-            )
-            .bind(user_id)
-            .fetch_optional(&self.pool)
-            .await?
+                "#,
+        )
+        .bind(user_id)
+        .fetch_optional(&self.pool)
+        .await?
         {
+            return Ok(Some(BanInfo {
+                ban_type: BanType::Permanent,
 
-            return Ok(Some(
-                BanInfo {
+                reason: reason.unwrap_or_else(|| "Aucune raison fournie".to_string()),
 
-                    ban_type:
-                        BanType::Permanent,
-
-                    reason:
-                        reason.unwrap_or_else(
-                            || "Aucune raison fournie".to_string()
-                        ),
-
-                    date_deban:
-                        None,
-                }
-            ));
+                date_deban: None,
+            }));
         }
 
-
         // ========================================================
         // BAN TEMPORAIRE
         // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:389:
 
-        if let Some((reason, date_deban)) =
-            sqlx::query_as::<_, (Option<String>, String)>(
-                r#"
+        if let Some((reason, date_deban)) = sqlx::query_as::<_, (Option<String>, String)>(
+            r#"
                 SELECT
                     raison,
                     date_deban
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:402:
                       > CURRENT_TIMESTAMP
 
                 LIMIT 1
-                "#
-            )
-            .bind(user_id)
-            .fetch_optional(&self.pool)
-            .await?
+                "#,
+        )
+        .bind(user_id)
+        .fetch_optional(&self.pool)
+        .await?
         {
+            return Ok(Some(BanInfo {
+                ban_type: BanType::Temporary,
 
-            return Ok(Some(
-                BanInfo {
+                reason: reason.unwrap_or_else(|| "Aucune raison fournie".to_string()),
 
-                    ban_type:
-                        BanType::Temporary,
-
-                    reason:
-                        reason.unwrap_or_else(
-                            || "Aucune raison fournie".to_string()
-                        ),
-
-                    date_deban:
-                        Some(date_deban),
-                }
-            ));
+                date_deban: Some(date_deban),
+            }));
         }
 
-
         // ========================================================
         // PAS DE BAN
         // ========================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:434:
         Ok(None)
     }
 
-
     // ============================================================
     // ENCODAGE DU PAQUET BAN
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:441:
 
-    fn encode_ban_payload(
-        ban: &BanInfo,
-    ) -> Vec<u8> {
-
+    fn encode_ban_payload(ban: &BanInfo) -> Vec<u8> {
         format!(
             "{}\0{}\0{}",
             ban.ban_type as u8,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:449:
-
             ban.reason,
-
-            ban.date_deban
-                .as_deref()
-                .unwrap_or("")
+            ban.date_deban.as_deref().unwrap_or("")
         )
         .into_bytes()
     }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:458:
 
-
     // ============================================================
     // MARQUER COMME DÉCONNECTÉ
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:463:
 
-    async fn mark_disconnected(
-        &self,
-    ) {
+    async fn mark_disconnected(&self) {
+        let user_id = match self.user_id() {
+            Some(id) => id,
 
-        let user_id =
-            match self.user_id() {
+            None => return,
+        };
 
-                Some(id) => id,
-
-                None => return,
-            };
-
-
-        if let Err(e) =
-            sqlx::query(
-                r#"
+        if let Err(e) = sqlx::query(
+            r#"
                 UPDATE users
 
                 SET status = 'DISCONNECTED'
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:484:
                 WHERE user_id = ?
 
                   AND status = 'CONNECTED'
-                "#
-            )
-            .bind(user_id)
-            .execute(&self.pool)
-            .await
+                "#,
+        )
+        .bind(user_id)
+        .execute(&self.pool)
+        .await
         {
-
             error!(
                 "Impossible de mettre le joueur {} en DISCONNECTED [{}] : {}",
-                user_id,
-                self.session_id,
-                e
+                user_id, self.session_id, e
             );
 
             return;
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:502:
         }
 
-
         debug!(
             "Utilisateur {} marqué comme DISCONNECTED [{}]",
-            user_id,
-            self.session_id
+            user_id, self.session_id
         );
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:512:
-
     // ============================================================
     // SET USER ID
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:516:
 
-    pub fn set_user_id(
-        &mut self,
-        id: Option<String>,
-    ) {
-
+    pub fn set_user_id(&mut self, id: Option<String>) {
         self.user_id = id;
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:525:
-
     // ============================================================
     // GET USER ID
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:529:
 
-    pub fn user_id(
-        &self,
-    ) -> Option<&str> {
-
-        self.user_id
-            .as_deref()
+    pub fn user_id(&self) -> Option<&str> {
+        self.user_id.as_deref()
     }
 
-
     // ============================================================
     // SET CLIENT ID
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:542:
 
-    pub fn set_client_id(
-        &mut self,
-        id: Option<i64>,
-    ) {
-
+    pub fn set_client_id(&mut self, id: Option<i64>) {
         self.client_id = id;
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:551:
-
     // ============================================================
     // GET CLIENT ID
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:555:
 
-    pub fn client_id(
-        &self,
-    ) -> Option<i64> {
-
+    pub fn client_id(&self) -> Option<i64> {
         self.client_id
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:563:
-
     // ============================================================
     // SET ACCOUNT ID
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:567:
 
-    pub fn set_account_id(
-        &mut self,
-        id: Option<i64>,
-    ) {
-
+    pub fn set_account_id(&mut self, id: Option<i64>) {
         self.account_id = id;
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:576:
-
     // ============================================================
     // GET ACCOUNT ID
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:580:
 
-    pub fn account_id(
-        &self,
-    ) -> Option<i64> {
-
+    pub fn account_id(&self) -> Option<i64> {
         self.account_id
     }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:588:
-
     // ============================================================
     // DÉCONNEXION
     // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:592:
 
-    pub async fn disconnect(
-        &mut self,
-    ) {
-
+    pub async fn disconnect(&mut self) {
         // --------------------------------------------------------
         // Mettre le compte hors ligne AVANT de fermer le socket
         // --------------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:600:
 
         self.mark_disconnected().await;
 
-
         // --------------------------------------------------------
         // Fermeture du socket
         // --------------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:607:
 
-        if let Err(e) =
-            self.stream.shutdown().await
-        {
-
+        if let Err(e) = self.stream.shutdown().await {
             error!(
                 "Erreur lors de la déconnexion [{}] : {}",
-                self.session_id,
-                e
+                self.session_id, e
             );
-        }
-        else {
-
-            info!(
-                "Client déconnecté : {}",
-                self.session_id
-            );
+        } else {
+            info!("Client déconnecté : {}", self.session_id);
         }
     }
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:627:
+
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1:
-use crate::network::packet::{
-    Packet,
-    PacketType,
-    LogLevel,
-    ClientLog,
-};
+use crate::network::packet::{ClientLog, LogLevel, Packet, PacketType};
 
 use crate::network::client::Client;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:10:
-use crate::network::parser::{
-    parse_login_payload,
-    parse_signup_payload,
-};
+use crate::network::parser::{parse_login_payload, parse_signup_payload};
 
-use crate::utils::password::{
-    verify_password,
-    hash_password,
-};
+use crate::utils::password::{hash_password, verify_password};
 
-use log::{
-    trace,
-    debug,
-    info,
-    warn,
-    error,
-};
+use log::{debug, error, info, trace, warn};
 
-use sqlx::{
-    SqlitePool,
-    Row,
-};
+use sqlx::{Row, SqlitePool};
 
 use uuid::Uuid;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:35:
-
 // ============================================================
 // Structures
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:42:
     password_hash: String,
 }
 
-
 struct LoginData {
     user_id: String,
     password_hash: String,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:50:
     is_banned_temp: bool,
 }
 
-
 pub struct PacketHandler;
 
-
 // ============================================================
 // Packet Handler
 // ============================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:60:
 
 impl PacketHandler {
-
-    pub async fn handle(
-        client: &mut Client,
-        packet: Packet,
-        pool: SqlitePool,
-    ) -> Option<Packet> {
-
+    pub async fn handle(client: &mut Client, packet: Packet, pool: SqlitePool) -> Option<Packet> {
         match packet.packet_type {
-
             // =================================================
             // LOG
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:74:
-
             PacketType::Log => {
+                let log = match serde_json::from_slice::<ClientLog>(&packet.payload) {
+                    Ok(log) => log,
 
-                let log =
-                    match serde_json::from_slice::<ClientLog>(
-                        &packet.payload
-                    ) {
+                    Err(e) => {
+                        error!("Impossible de décoder le paquet LOG : {}", e);
 
-                        Ok(log) => log,
+                        return None;
+                    }
+                };
 
-                        Err(e) => {
-
-                            error!(
-                                "Impossible de décoder le paquet LOG : {}",
-                                e
-                            );
-
-                            return None;
-                        }
-                    };
-
-
                 match log.level {
-
                     LogLevel::TRACE => {
-                        trace!(
-                            "[CLIENT] [{}:{}] {}",
-                            log.file,
-                            log.line,
-                            log.message
-                        );
+                        trace!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                     }
 
                     LogLevel::DEBUG => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:108:
-                        debug!(
-                            "[CLIENT] [{}:{}] {}",
-                            log.file,
-                            log.line,
-                            log.message
-                        );
+                        debug!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                     }
 
                     LogLevel::INFO => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:117:
-                        info!(
-                            "[CLIENT] [{}:{}] {}",
-                            log.file,
-                            log.line,
-                            log.message
-                        );
+                        info!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                     }
 
                     LogLevel::WARNING => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:126:
-                        warn!(
-                            "[CLIENT] [{}:{}] {}",
-                            log.file,
-                            log.line,
-                            log.message
-                        );
+                        warn!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                     }
 
                     LogLevel::ERROR => {
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:135:
-                        error!(
-                            "[CLIENT] [{}:{}] {}",
-                            log.file,
-                            log.line,
-                            log.message
-                        );
+                        error!("[CLIENT] [{}:{}] {}", log.file, log.line, log.message);
                     }
                 }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:144:
-
                 None
             }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:148:
-
             // =================================================
             // PING
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:152:
-
             PacketType::Ping => {
-
                 debug!("Ping reçu");
 
-                Some(
-                    Packet::new(
-                        PacketType::Ping,
-                        b"PONG".to_vec(),
-                    )
-                )
+                Some(Packet::new(PacketType::Ping, b"PONG".to_vec()))
             }
 
-
             // =================================================
             // BAN
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:169:
-
             PacketType::BAN => {
+                debug!("Packet BAN reçu depuis le client : ignoré");
 
-                debug!(
-                    "Packet BAN reçu depuis le client : ignoré"
-                );
-
                 None
             }
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:179:
-
             // =================================================
             // SIGN UP
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:183:
-
             PacketType::SignUp => {
-
                 // ------------------------------------------------
                 // Parser
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:189:
 
-                let (email, password) =
-                    match parse_signup_payload(
-                        &packet.payload
-                    ) {
+                let (email, password) = match parse_signup_payload(&packet.payload) {
+                    Ok(signup) => signup,
 
-                        Ok(signup) => signup,
+                    Err(error) => {
+                        debug!("SIGN_UP invalide : {}", error);
 
-                        Err(error) => {
+                        return Some(Packet::new(
+                            PacketType::SignUpResponse,
+                            b"SIGN_UP invalide".to_vec(),
+                        ));
+                    }
+                };
 
-                            debug!(
-                                "SIGN_UP invalide : {}",
-                                error
-                            );
-
-                            return Some(
-                                Packet::new(
-                                    PacketType::SignUpResponse,
-                                    b"SIGN_UP invalide".to_vec(),
-                                )
-                            );
-                        }
-                    };
-
-
                 // ------------------------------------------------
                 // Hash Argon2
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:217:
 
-                let password_hash =
-                    match hash_password(&password) {
+                let password_hash = match hash_password(&password) {
+                    Ok(hash) => hash,
 
-                        Ok(hash) => hash,
+                    Err(error) => {
+                        error!("Erreur lors du hash du mot de passe : {}", error);
 
-                        Err(error) => {
+                        return Some(Packet::new(
+                            PacketType::SignUpResponse,
+                            b"Erreur serveur".to_vec(),
+                        ));
+                    }
+                };
 
-                            error!(
-                                "Erreur lors du hash du mot de passe : {}",
-                                error
-                            );
-
-                            return Some(
-                                Packet::new(
-                                    PacketType::SignUpResponse,
-                                    b"Erreur serveur".to_vec(),
-                                )
-                            );
-                        }
-                    };
-
-
                 // ------------------------------------------------
                 // UUID
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:243:
 
-                let user_id =
-                    Uuid::new_v4().to_string();
+                let user_id = Uuid::new_v4().to_string();
 
-
                 // ------------------------------------------------
                 // Création utilisateur
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:265:
                 .execute(&pool)
                 .await
                 {
-
                     Ok(_) => {
+                        debug!("Nouvel utilisateur créé : {}", email);
 
-                        debug!(
-                            "Nouvel utilisateur créé : {}",
-                            email
-                        );
+                        client.set_user_id(Some(user_id.clone()));
 
-                        client.set_user_id(
-                            Some(user_id.clone())
-                        );
-
-                        Some(
-                            Packet::new(
-                                PacketType::SignUpResponse,
-                                b"Utilisateur cree avec succes".to_vec(),
-                            )
-                        )
+                        Some(Packet::new(
+                            PacketType::SignUpResponse,
+                            b"Utilisateur cree avec succes".to_vec(),
+                        ))
                     }
 
-
                     Err(error) => {
+                        let error_msg = error.to_string();
 
-                        let error_msg =
-                            error.to_string();
+                        if error_msg.contains("UNIQUE constraint failed") {
+                            debug!("SIGN_UP refusé : email déjà utilisé");
 
-
-                        if error_msg.contains(
-                            "UNIQUE constraint failed"
-                        ) {
-
-                            debug!(
-                                "SIGN_UP refusé : email déjà utilisé"
-                            );
-
-                            Some(
-                                Packet::new(
-                                    PacketType::SignUpResponse,
-                                    b"Email deja utilise".to_vec(),
-                                )
-                            )
-
+                            Some(Packet::new(
+                                PacketType::SignUpResponse,
+                                b"Email deja utilise".to_vec(),
+                            ))
                         } else {
+                            error!("Erreur lors de la création du user : {}", error);
 
-                            error!(
-                                "Erreur lors de la création du user : {}",
-                                error
-                            );
-
-                            Some(
-                                Packet::new(
-                                    PacketType::SignUpResponse,
-                                    b"Erreur serveur".to_vec(),
-                                )
-                            )
+                            Some(Packet::new(
+                                PacketType::SignUpResponse,
+                                b"Erreur serveur".to_vec(),
+                            ))
                         }
                     }
                 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:326:
             }
 
-
             // =================================================
             // LOGIN
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:332:
-
             PacketType::Login => {
-
                 // ------------------------------------------------
                 // Parser LOGIN
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:338:
 
-                let (email, password) =
-                    match parse_login_payload(
-                        &packet.payload
-                    ) {
+                let (email, password) = match parse_login_payload(&packet.payload) {
+                    Ok(login) => login,
 
-                        Ok(login) => login,
+                    Err(error) => {
+                        debug!("LOGIN invalide : {}", error);
 
-                        Err(error) => {
+                        return Some(Packet::new(
+                            PacketType::LoginResponse,
+                            b"LOGIN invalide".to_vec(),
+                        ));
+                    }
+                };
 
-                            debug!(
-                                "LOGIN invalide : {}",
-                                error
-                            );
-
-                            return Some(
-                                Packet::new(
-                                    PacketType::LoginResponse,
-                                    b"LOGIN invalide".to_vec(),
-                                )
-                            );
-                        }
-                    };
-
-
                 // ------------------------------------------------
                 // Récupération utilisateur + bans
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:366:
 
-                let login_data =
-                    match sqlx::query(
-                        r#"
+                let login_data = match sqlx::query(
+                    r#"
                         SELECT
                             u.user_id,
                             u.password_hash,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:399:
 
                         WHERE u.email = ?
                         "#,
-                    )
-                    .bind(&email)
-                    .fetch_optional(&pool)
-                    .await
-                    {
+                )
+                .bind(&email)
+                .fetch_optional(&pool)
+                .await
+                {
+                    Ok(Some(row)) => LoginData {
+                        user_id: row.get::<String, _>("user_id"),
 
-                        Ok(Some(row)) => {
+                        password_hash: row.get::<String, _>("password_hash"),
 
-                            LoginData {
+                        is_banned_perm: row.get::<i64, _>("is_banned_perm") != 0,
 
-                                user_id:
-                                    row.get::<String, _>(
-                                        "user_id"
-                                    ),
+                        is_banned_temp: row.get::<i64, _>("is_banned_temp") != 0,
+                    },
 
-                                password_hash:
-                                    row.get::<String, _>(
-                                        "password_hash"
-                                    ),
+                    Ok(None) => {
+                        debug!("Tentative de connexion avec un utilisateur inexistant");
 
-                                is_banned_perm:
-                                    row.get::<i64, _>(
-                                        "is_banned_perm"
-                                    ) != 0,
+                        return Some(Packet::new(
+                            PacketType::LoginResponse,
+                            b"Identifiants invalides".to_vec(),
+                        ));
+                    }
 
-                                is_banned_temp:
-                                    row.get::<i64, _>(
-                                        "is_banned_temp"
-                                    ) != 0,
-                            }
-                        }
+                    Err(error) => {
+                        error!("Erreur lors de la recherche de l'utilisateur : {}", error);
 
+                        return Some(Packet::new(
+                            PacketType::LoginResponse,
+                            b"Erreur serveur".to_vec(),
+                        ));
+                    }
+                };
 
-                        Ok(None) => {
-
-                            debug!(
-                                "Tentative de connexion avec un utilisateur inexistant"
-                            );
-
-                            return Some(
-                                Packet::new(
-                                    PacketType::LoginResponse,
-                                    b"Identifiants invalides".to_vec(),
-                                )
-                            );
-                        }
-
-
-                        Err(error) => {
-
-                            error!(
-                                "Erreur lors de la recherche de l'utilisateur : {}",
-                                error
-                            );
-
-                            return Some(
-                                Packet::new(
-                                    PacketType::LoginResponse,
-                                    b"Erreur serveur".to_vec(),
-                                )
-                            );
-                        }
-                    };
-
-
                 // ------------------------------------------------
                 // BAN PERMANENT
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:470:
 
                 if login_data.is_banned_perm {
+                    debug!("Connexion refusée : utilisateur banni définitivement");
 
-                    debug!(
-                        "Connexion refusée : utilisateur banni définitivement"
-                    );
-
-                    return Some(
-                        Packet::new(
-                            PacketType::LoginResponse,
-                            b"Compte banni definitivement".to_vec(),
-                        )
-                    );
+                    return Some(Packet::new(
+                        PacketType::LoginResponse,
+                        b"Compte banni definitivement".to_vec(),
+                    ));
                 }
 
-
                 // ------------------------------------------------
                 // BAN FERME
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:489:
 
                 if login_data.is_banned_temp {
+                    debug!("Connexion refusée : utilisateur temporairement banni");
 
-                    debug!(
-                        "Connexion refusée : utilisateur temporairement banni"
-                    );
-
-                    return Some(
-                        Packet::new(
-                            PacketType::LoginResponse,
-                            b"Compte temporairement banni".to_vec(),
-                        )
-                    );
+                    return Some(Packet::new(
+                        PacketType::LoginResponse,
+                        b"Compte temporairement banni".to_vec(),
+                    ));
                 }
 
-
                 // ------------------------------------------------
                 // Vérification mot de passe
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:508:
 
-                let password_valid =
-                    verify_password(
-                        &password,
-                        &login_data.password_hash,
-                    );
+                let password_valid = verify_password(&password, &login_data.password_hash);
 
-
                 // =================================================
                 // MOT DE PASSE INCORRECT
                 // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:519:
 
                 if !password_valid {
-
                     // --------------------------------------------
                     // Compteur de tentatives
                     // --------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:525:
 
-                    let attempts =
-                        match sqlx::query_scalar::<_, i64>(
-                            r#"
+                    let attempts = match sqlx::query_scalar::<_, i64>(
+                        r#"
                             INSERT INTO login_attempts (
                                 user_id,
                                 failed_attempts,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:548:
 
                             RETURNING failed_attempts
                             "#,
-                        )
-                        .bind(&login_data.user_id)
-                        .fetch_one(&pool)
-                        .await
-                        {
+                    )
+                    .bind(&login_data.user_id)
+                    .fetch_one(&pool)
+                    .await
+                    {
+                        Ok(value) => value,
 
-                            Ok(value) => value,
+                        Err(error) => {
+                            error!(
+                                "Erreur lors de l'enregistrement de la tentative : {}",
+                                error
+                            );
 
-                            Err(error) => {
+                            return Some(Packet::new(
+                                PacketType::LoginResponse,
+                                b"Erreur serveur".to_vec(),
+                            ));
+                        }
+                    };
 
-                                error!(
-                                    "Erreur lors de l'enregistrement de la tentative : {}",
-                                    error
-                                );
-
-                                return Some(
-                                    Packet::new(
-                                        PacketType::LoginResponse,
-                                        b"Erreur serveur".to_vec(),
-                                    )
-                                );
-                            }
-                        };
-
-
                     debug!(
                         "Mot de passe incorrect pour {} : tentative {}",
-                        email,
-                        attempts
+                        email, attempts
                     );
 
-
                     // =================================================
                     // 3 ÉCHECS
                     // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:586:
-                    
-                    if attempts >= 3 {
 
+                    if attempts >= 3 {
                         // --------------------------------------------
                         // Recherche du sursis
                         // --------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:592:
                         debug!(
-    "DEBUG BAN : création du ban pour user_id={}, tentatives={}",
-    login_data.user_id,
-    attempts
-);
-                        let sursis_jours =
-                            match sqlx::query_scalar::<_, i64>(
-                                r#"
+                            "DEBUG BAN : création du ban pour user_id={}, tentatives={}",
+                            login_data.user_id, attempts
+                        );
+                        let sursis_jours = match sqlx::query_scalar::<_, i64>(
+                            r#"
                                 SELECT sursis
 
                                 FROM banssursis
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:605:
 
                                 LIMIT 1
                                 "#,
-                            )
-                            .bind(&login_data.user_id)
-                            .fetch_optional(&pool)
-                            .await
-                            {
+                        )
+                        .bind(&login_data.user_id)
+                        .fetch_optional(&pool)
+                        .await
+                        {
+                            Ok(value) => value,
 
-                                Ok(value) => value,
+                            Err(error) => {
+                                error!("Erreur lors de la vérification du sursis : {}", error);
 
-                                Err(error) => {
+                                return Some(Packet::new(
+                                    PacketType::LoginResponse,
+                                    b"Erreur serveur".to_vec(),
+                                ));
+                            }
+                        };
 
-                                    error!(
-                                        "Erreur lors de la vérification du sursis : {}",
-                                        error
-                                    );
-
-                                    return Some(
-                                        Packet::new(
-                                            PacketType::LoginResponse,
-                                            b"Erreur serveur".to_vec(),
-                                        )
-                                    );
-                                }
-                            };
-
-
                         // =================================================
                         // SURsis EXISTANT
                         // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:636:
 
-                        if let Some(jours) =
-                            sursis_jours
-                        {
-
+                        if let Some(jours) = sursis_jours {
                             // ----------------------------------------
                             // Validation
                             // ----------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:644:
 
                             if jours <= 0 {
+                                error!("Sursis invalide pour {} : {} jour(s)", email, jours);
 
-                                error!(
-                                    "Sursis invalide pour {} : {} jour(s)",
-                                    email,
-                                    jours
-                                );
-
-                                return Some(
-                                    Packet::new(
-                                        PacketType::LoginResponse,
-                                        b"Erreur serveur".to_vec(),
-                                    )
-                                );
+                                return Some(Packet::new(
+                                    PacketType::LoginResponse,
+                                    b"Erreur serveur".to_vec(),
+                                ));
                             }
 
+                            debug!("Activation du sursis pour {} : {} jour(s)", email, jours);
 
-                            debug!(
-                                "Activation du sursis pour {} : {} jour(s)",
-                                email,
-                                jours
-                            );
-
-
                             // ----------------------------------------
                             // Ajouter le sursis au ban ferme
                             //
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:685:
                             // ----------------------------------------
 
                             let result = sqlx::query(
-    r#"
+                                r#"
     INSERT INTO bansferme (
         user_id,
         auteur,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:738:
             )
         END
     "#,
-)
-.bind(&login_data.user_id)
-.bind(jours)
-.bind(jours)
-.bind(jours)
-.execute(&pool)
-.await;
+                            )
+                            .bind(&login_data.user_id)
+                            .bind(jours)
+                            .bind(jours)
+                            .bind(jours)
+                            .execute(&pool)
+                            .await;
 
-                            if let Err(error) =
-                                result
-                            {
+                            if let Err(error) = result {
+                                error!("Impossible d'activer le sursis pour {} : {}", email, error);
 
-                                error!(
-                                    "Impossible d'activer le sursis pour {} : {}",
-                                    email,
-                                    error
-                                );
-
-                                return Some(
-                                    Packet::new(
-                                        PacketType::LoginResponse,
-                                        b"Erreur serveur".to_vec(),
-                                    )
-                                );
+                                return Some(Packet::new(
+                                    PacketType::LoginResponse,
+                                    b"Erreur serveur".to_vec(),
+                                ));
                             }
 
-
                             // ----------------------------------------
                             // Supprimer le sursis consommé
                             // ----------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:771:
 
-                            if let Err(error) =
-                                sqlx::query(
-                                    r#"
+                            if let Err(error) = sqlx::query(
+                                r#"
                                     DELETE FROM banssursis
 
                                     WHERE user_id = ?
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:778:
                                     "#,
-                                )
-                                .bind(&login_data.user_id)
-                                .execute(&pool)
-                                .await
+                            )
+                            .bind(&login_data.user_id)
+                            .execute(&pool)
+                            .await
                             {
+                                error!("Impossible de supprimer le sursis consommé : {}", error);
 
-                                error!(
-                                    "Impossible de supprimer le sursis consommé : {}",
-                                    error
-                                );
-
-                                return Some(
-                                    Packet::new(
-                                        PacketType::LoginResponse,
-                                        b"Erreur serveur".to_vec(),
-                                    )
-                                );
+                                return Some(Packet::new(
+                                    PacketType::LoginResponse,
+                                    b"Erreur serveur".to_vec(),
+                                ));
                             }
 
-
-                            debug!(
-                                "Sursis de {} jour(s) activé pour {}",
-                                jours,
-                                email
-                            );
+                            debug!("Sursis de {} jour(s) activé pour {}", jours, email);
                         }
-
-
                         // =================================================
                         // PAS DE SURsis
                         // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:810:
-
                         else {
+                            debug!("Aucun sursis pour {}", email);
 
-                            debug!(
-                                "Aucun sursis pour {}",
-                                email
-                            );
-
-
                             // --------------------------------------------
                             // Ban automatique de 10 minutes
                             // --------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:943:
                                 .execute(&pool)
                                 .await;
 
+                            if let Err(error) = result {
+                                error!("Impossible de créer le ban temporaire : {}", error);
 
-                            if let Err(error) =
-                                result
-                            {
-
-                                error!(
-                                    "Impossible de créer le ban temporaire : {}",
-                                    error
-                                );
-
-                                return Some(
-                                    Packet::new(
-                                        PacketType::LoginResponse,
-                                        b"Erreur serveur".to_vec(),
-                                    )
-                                );
+                                return Some(Packet::new(
+                                    PacketType::LoginResponse,
+                                    b"Erreur serveur".to_vec(),
+                                ));
                             }
                         }
-                        debug!(
-    "DEBUG BAN : INSERT terminé pour {}",
-    login_data.user_id
-);
+                        debug!("DEBUG BAN : INSERT terminé pour {}", login_data.user_id);
 
                         // =================================================
                         // RESET DES TENTATIVES
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:971:
                         // =================================================
 
-                        if let Err(error) =
-                            sqlx::query(
-                                r#"
+                        if let Err(error) = sqlx::query(
+                            r#"
                                 DELETE FROM login_attempts
 
                                 WHERE user_id = ?
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:979:
                                 "#,
-                            )
-                            .bind(&login_data.user_id)
-                            .execute(&pool)
-                            .await
+                        )
+                        .bind(&login_data.user_id)
+                        .execute(&pool)
+                        .await
                         {
+                            error!("Impossible de supprimer le compteur : {}", error);
 
-                            error!(
-                                "Impossible de supprimer le compteur : {}",
-                                error
-                            );
-
-                            return Some(
-                                Packet::new(
-                                    PacketType::LoginResponse,
-                                    b"Erreur serveur".to_vec(),
-                                )
-                            );
+                            return Some(Packet::new(
+                                PacketType::LoginResponse,
+                                b"Erreur serveur".to_vec(),
+                            ));
                         }
 
-
                         // =================================================
                         // RÉPONSE
                         // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1003:
                         info!("Utilisateur banni");
-                        return Some(
-                            Packet::new(
-                                PacketType::LoginResponse,
-                                b"Trop de tentatives. Compte bloque temporairement.".to_vec(),
-                            )
-                        );
+                        return Some(Packet::new(
+                            PacketType::LoginResponse,
+                            b"Trop de tentatives. Compte bloque temporairement.".to_vec(),
+                        ));
                     }
 
-
                     // ------------------------------------------------
                     // Moins de 3 tentatives
                     // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1016:
 
-                    return Some(
-                        Packet::new(
-                            PacketType::LoginResponse,
-                            b"Identifiants invalides".to_vec(),
-                        )
-                    );
+                    return Some(Packet::new(
+                        PacketType::LoginResponse,
+                        b"Identifiants invalides".to_vec(),
+                    ));
                 }
 
-
                 // =================================================
                 // MOT DE PASSE CORRECT
                 // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1031:
                 // Vérifier si déjà connecté
                 // ------------------------------------------------
 
-                let is_already_connected =
-                    match sqlx::query_scalar::<_, i64>(
-                        r#"
+                let is_already_connected = match sqlx::query_scalar::<_, i64>(
+                    r#"
                         SELECT EXISTS(
                             SELECT 1
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1044:
                               AND status = 'CONNECTED'
                         )
                         "#,
-                    )
-                    .bind(&login_data.user_id)
-                    .fetch_one(&pool)
-                    .await
-                    {
+                )
+                .bind(&login_data.user_id)
+                .fetch_one(&pool)
+                .await
+                {
+                    Ok(value) => value != 0,
 
-                        Ok(value) =>
-                            value != 0,
+                    Err(error) => {
+                        error!("Erreur lors de la vérification de connexion : {}", error);
 
-                        Err(error) => {
+                        return Some(Packet::new(
+                            PacketType::LoginResponse,
+                            b"Erreur serveur".to_vec(),
+                        ));
+                    }
+                };
 
-                            error!(
-                                "Erreur lors de la vérification de connexion : {}",
-                                error
-                            );
-
-                            return Some(
-                                Packet::new(
-                                    PacketType::LoginResponse,
-                                    b"Erreur serveur".to_vec(),
-                                )
-                            );
-                        }
-                    };
-
-
                 if is_already_connected {
+                    debug!("Tentative de connexion avec un compte déjà connecté");
 
-                    debug!(
-                        "Tentative de connexion avec un compte déjà connecté"
-                    );
-
-                    return Some(
-                        Packet::new(
-                            PacketType::LoginResponse,
-                            b"Ce compte est deja connecte".to_vec(),
-                        )
-                    );
+                    return Some(Packet::new(
+                        PacketType::LoginResponse,
+                        b"Ce compte est deja connecte".to_vec(),
+                    ));
                 }
 
-
                 // ------------------------------------------------
                 // CONNECTED
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1091:
 
-                if let Err(error) =
-                    sqlx::query(
-                        r#"
+                if let Err(error) = sqlx::query(
+                    r#"
                         UPDATE users
 
                         SET status = 'CONNECTED'
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1098:
 
                         WHERE user_id = ?
                         "#,
-                    )
-                    .bind(&login_data.user_id)
-                    .execute(&pool)
-                    .await
+                )
+                .bind(&login_data.user_id)
+                .execute(&pool)
+                .await
                 {
+                    error!("Erreur lors de la connexion du joueur : {}", error);
 
-                    error!(
-                        "Erreur lors de la connexion du joueur : {}",
-                        error
-                    );
-
-                    return Some(
-                        Packet::new(
-                            PacketType::LoginResponse,
-                            b"Erreur serveur".to_vec(),
-                        )
-                    );
+                    return Some(Packet::new(
+                        PacketType::LoginResponse,
+                        b"Erreur serveur".to_vec(),
+                    ));
                 }
 
-
                 // ------------------------------------------------
                 // Reset login attempts
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1124:
 
-                if let Err(error) =
-                    sqlx::query(
-                        r#"
+                if let Err(error) = sqlx::query(
+                    r#"
                         DELETE FROM login_attempts
 
                         WHERE user_id = ?
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1131:
                         "#,
-                    )
-                    .bind(&login_data.user_id)
-                    .execute(&pool)
-                    .await
+                )
+                .bind(&login_data.user_id)
+                .execute(&pool)
+                .await
                 {
+                    error!("Impossible de réinitialiser les tentatives : {}", error);
 
-                    error!(
-                        "Impossible de réinitialiser les tentatives : {}",
-                        error
-                    );
-
-                    return Some(
-                        Packet::new(
-                            PacketType::LoginResponse,
-                            b"Erreur serveur".to_vec(),
-                        )
-                    );
+                    return Some(Packet::new(
+                        PacketType::LoginResponse,
+                        b"Erreur serveur".to_vec(),
+                    ));
                 }
 
-
                 // ------------------------------------------------
                 // Login réussi
                 // ------------------------------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1155:
 
-                debug!(
-                    "Utilisateur authentifié : {}",
-                    email
-                );
+                debug!("Utilisateur authentifié : {}", email);
 
+                client.set_user_id(Some(login_data.user_id.clone()));
 
-                client.set_user_id(
-                    Some(
-                        login_data.user_id.clone()
-                    )
-                );
-
-
-                Some(
-                    Packet::new(
-                        PacketType::LoginResponse,
-                        format!(
-                            "Utilisateur {} authentifié",
-                            email
-                        )
-                        .into_bytes(),
-                    )
-                )
+                Some(Packet::new(
+                    PacketType::LoginResponse,
+                    format!("Utilisateur {} authentifié", email).into_bytes(),
+                ))
             }
 
-
             // =================================================
             // CHAT
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1185:
-
             PacketType::Chat => {
+                debug!("Message : {}", String::from_utf8_lossy(&packet.payload));
 
-                debug!(
-                    "Message : {}",
-                    String::from_utf8_lossy(
-                        &packet.payload
-                    )
-                );
-
-                Some(
-                    Packet::new(
-                        PacketType::Chat,
-                        packet.payload,
-                    )
-                )
+                Some(Packet::new(PacketType::Chat, packet.payload))
             }
 
-
             // =================================================
             // MOVE
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1207:
-
             PacketType::Move => {
+                debug!("Déplacement reçu");
 
-                debug!(
-                    "Déplacement reçu"
-                );
-
-                Some(
-                    Packet::new(
-                        PacketType::Move,
-                        packet.payload,
-                    )
-                )
+                Some(Packet::new(PacketType::Move, packet.payload))
             }
 
-
             // =================================================
             // Réponses interdites venant du client
             // =================================================
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/handler.rs:1226:
-
-            PacketType::LoginResponse
-            | PacketType::SignUpResponse => {
-
+            PacketType::LoginResponse | PacketType::SignUpResponse => {
                 error!(
                     "Réponse reçue du client alors qu'elle doit être envoyée par le serveur : {:?}",
                     packet.packet_type
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/mod.rs:1:
-pub mod packet;
 pub mod client;
-pub mod server;
 pub mod handler;
+pub mod packet;
 pub mod parser;
-
-
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:21:
     Move = 4,
     Log = 5,
     SignUp = 6,
-     LoginResponse = 7,
+    LoginResponse = 7,
     SignUpResponse = 8,
     BAN = 9,
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:45:
     ERROR,
 }
 
-
 #[derive(Debug, Serialize, Deserialize)]
 pub struct ClientLog {
     pub level: LogLevel,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:80:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:90:
         }
     }
 }
-pub fn encode_ban(
-    ban_type: BanType,
-    reason: &str,
-    date_deban: Option<&str>,
-) -> Vec<u8> {
-
+pub fn encode_ban(ban_type: BanType, reason: &str, date_deban: Option<&str>) -> Vec<u8> {
     format!(
         "{}\0{}\0{}",
         ban_type as u8,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:106:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:125:
 
     stream.write_all(&size).await?;
 
-    let packet_type =
-        (packet.packet_type as u16).to_be_bytes();
+    let packet_type = (packet.packet_type as u16).to_be_bytes();
 
     stream.write_all(&packet_type).await?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:136:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:149:
 }
 
 /// Reçoit un paquet.
-pub async fn receive_packet(
-    stream: &mut TcpStream,
-) -> io::Result<Packet> {
-
+pub async fn receive_packet(stream: &mut TcpStream) -> io::Result<Packet> {
     // Taille
     let header = recv_exact(stream, 4).await?;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:159:
-    let size = u32::from_be_bytes([
-        header[0],
-        header[1],
-        header[2],
-        header[3],
-    ]) as usize;
+    let size = u32::from_be_bytes([header[0], header[1], header[2], header[3]]) as usize;
 
     if size < 2 {
         error!("paquet invalide");
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/packet.rs:183:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:1:
-pub fn parse_login_payload(
-    payload: &[u8],
-) -> Result<(String, String), String> {
-
+pub fn parse_login_payload(payload: &[u8]) -> Result<(String, String), String> {
     let mut offset = 0;
 
     // -------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:12:
         return Err("Email length manquante".into());
     }
 
-    let email_length =
-        u16::from_be_bytes([
-            payload[offset],
-            payload[offset + 1],
-        ]) as usize;
+    let email_length = u16::from_be_bytes([payload[offset], payload[offset + 1]]) as usize;
 
     offset += 2;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:28:
         return Err("Email incomplet".into());
     }
 
-    let email = String::from_utf8(
-        payload[offset..offset + email_length]
-            .to_vec()
-    )
-    .map_err(|_| "Email UTF-8 invalide")?;
+    let email = String::from_utf8(payload[offset..offset + email_length].to_vec())
+        .map_err(|_| "Email UTF-8 invalide")?;
 
     offset += email_length;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:44:
         return Err("Password length manquante".into());
     }
 
-    let password_length =
-        u16::from_be_bytes([
-            payload[offset],
-            payload[offset + 1],
-        ]) as usize;
+    let password_length = u16::from_be_bytes([payload[offset], payload[offset + 1]]) as usize;
 
     offset += 2;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:60:
         return Err("Password incomplet".into());
     }
 
-    let password = String::from_utf8(
-        payload[offset..offset + password_length]
-            .to_vec()
-    )
-    .map_err(|_| "Password UTF-8 invalide")?;
+    let password = String::from_utf8(payload[offset..offset + password_length].to_vec())
+        .map_err(|_| "Password UTF-8 invalide")?;
 
     Ok((email, password))
 }
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:71:
-pub fn parse_signup_payload(
-    payload: &[u8],
-) -> Result<(String, String), String> {
-
+pub fn parse_signup_payload(payload: &[u8]) -> Result<(String, String), String> {
     let mut offset = 0;
 
     // -------------------------
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:82:
         return Err("Email length manquante".into());
     }
 
-    let email_length =
-        u16::from_be_bytes([
-            payload[offset],
-            payload[offset + 1],
-        ]) as usize;
+    let email_length = u16::from_be_bytes([payload[offset], payload[offset + 1]]) as usize;
 
     offset += 2;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:98:
         return Err("Email incomplet".into());
     }
 
-    let email = String::from_utf8(
-        payload[offset..offset + email_length]
-            .to_vec()
-    )
-    .map_err(|_| "Email UTF-8 invalide")?;
+    let email = String::from_utf8(payload[offset..offset + email_length].to_vec())
+        .map_err(|_| "Email UTF-8 invalide")?;
 
     offset += email_length;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:114:
         return Err("Password length manquante".into());
     }
 
-    let password_length =
-        u16::from_be_bytes([
-            payload[offset],
-            payload[offset + 1],
-        ]) as usize;
+    let password_length = u16::from_be_bytes([payload[offset], payload[offset + 1]]) as usize;
 
     offset += 2;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/parser.rs:130:
         return Err("Password incomplet".into());
     }
 
-    let password = String::from_utf8(
-        payload[offset..offset + password_length]
-            .to_vec()
-    )
-    .map_err(|_| "Password UTF-8 invalide")?;
+    let password = String::from_utf8(payload[offset..offset + password_length].to_vec())
+        .map_err(|_| "Password UTF-8 invalide")?;
 
     Ok((email, password))
 }
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
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/account_creator.rs:1:
-use uuid::Uuid;
 use sqlx::SqlitePool;
+use uuid::Uuid;
 pub async fn create_account(
     pool: &SqlitePool,
     email: &str,
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/account_creator.rs:106:
 
     tx.commit().await?;
 
-    Ok(())}
+    Ok(())
+}
 
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
-
+pub mod account_creator;
 pub mod logger;
-pub mod vault;
 pub mod password;
-pub mod account_creator;
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
-use the_last_signal_server::database::{
-    database_manager::DatabaseManager,
-    migrations,
-};
-use log::{debug,info};
+use log::{debug, info};
+use the_last_signal_server::database::{database_manager::DatabaseManager, migrations};
 use the_last_signal_server::network::server::Server;
 use the_last_signal_server::utils::logger::logger::ServerLogger;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:9:
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:30:
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
   Compiling cfg-if v1.0.4
   Compiling libc v0.2.189
   Compiling stable_deref_trait v1.2.1
   Compiling zerofrom v0.1.8
   Compiling typenum v1.20.1
   Compiling pin-project-lite v0.2.17
   Compiling yoke v0.8.3
   Compiling smallvec v1.15.2
   Compiling zerovec v0.11.8
   Compiling writeable v0.6.4
   Compiling futures-core v0.3.34
   Compiling litemap v0.8.3
   Compiling generic-array v0.14.7
   Compiling tinystr v0.8.4
   Compiling memchr v2.8.3
   Compiling icu_locale_core v2.3.0
   Compiling potential_utf v0.1.6
   Compiling zerotrie v0.2.5
   Compiling block-buffer v0.10.4
   Compiling utf8_iter v1.0.4
   Compiling scopeguard v1.2.0
   Compiling icu_collections v2.3.0
   Compiling lock_api v0.4.14
   Compiling icu_properties_data v2.3.0
   Compiling icu_normalizer_data v2.3.0
   Compiling mio v1.2.2
   Compiling socket2 v0.6.5
   Compiling icu_provider v2.3.1
   Compiling futures-sink v0.3.34
   Compiling bytes v1.12.1
   Compiling once_cell v1.21.4
   Compiling icu_properties v2.3.0
   Compiling icu_normalizer v2.3.0
   Compiling serde_core v1.0.229
   Compiling equivalent v1.0.2
   Compiling cpufeatures v0.2.17
   Compiling parking_lot_core v0.9.12
   Compiling tracing-core v0.1.36
   Compiling futures-task v0.3.34
   Compiling slab v0.4.12
   Compiling idna_adapter v1.2.2
   Compiling futures-io v0.3.34
   Compiling allocator-api2 v0.2.21
   Compiling percent-encoding v2.3.2
   Compiling foldhash v0.2.0
   Compiling form_urlencoded v1.2.2
   Compiling futures-util v0.3.34
   Compiling hashbrown v0.16.1
   Compiling idna v1.1.0
   Compiling parking_lot v0.12.5
   Compiling serde v1.0.229
   Compiling num-traits v0.2.19
   Compiling crossbeam-utils v0.8.22
   Compiling zmij v1.0.23
   Compiling itoa v1.0.18
   Compiling crc-catalog v2.5.0
   Compiling subtle v2.6.1
   Compiling rand_core v0.10.1
   Compiling hashbrown v0.17.1
   Compiling parking v2.2.1
   Compiling event-listener v5.4.2
   Compiling serde_json v1.0.151
   Compiling crc v3.4.0
   Compiling crossbeam-queue v0.3.13
   Compiling indexmap v2.14.1
   Compiling either v1.18.0
   Compiling futures-intrusive v0.5.0
   Compiling hashlink v0.11.1
   Compiling url v2.5.8
   Compiling crypto-common v0.1.7
   Compiling digest v0.10.7
   Compiling getrandom v0.4.3
   Compiling tokio v1.53.1
   Compiling spin v0.9.9
   Compiling tracing v0.1.44
   Compiling flume v0.12.0
   Compiling sha2 v0.10.9
   Compiling futures-executor v0.3.34
   Compiling atoi v2.0.0
   Compiling futures-channel v0.3.34
   Compiling log v0.4.34
   Compiling thiserror v2.0.20
   Compiling getrandom v0.2.17
   Compiling base64 v0.22.1
   Compiling bitflags v2.13.1
   Compiling uuid v1.26.0
   Compiling aho-corasick v1.1.5
   Compiling foreign-types-shared v0.1.1
   Compiling regex-syntax v0.8.11
   Compiling tokio-stream v0.1.19
   Compiling sqlx-core v0.9.0
   Compiling regex-automata v0.4.18
   Compiling sqlx-sqlite v0.9.0
   Compiling foreign-types v0.3.2
   Compiling libsqlite3-sys v0.37.0
   Compiling rand_core v0.6.4
   Compiling openssl-sys v0.9.117
   Compiling cpufeatures v0.3.1
   Compiling simd-adler32 v0.3.10
   Compiling sqlx-macros-core v0.9.0
   Compiling linux-raw-sys v0.12.1
   Compiling adler2 v2.0.1
   Compiling iana-time-zone v0.1.65
   Compiling base64ct v1.8.3
   Compiling password-hash v0.5.0
   Compiling chrono v0.4.45
   Compiling miniz_oxide v0.9.1
   Compiling rustix v1.1.4
   Compiling sqlx-macros v0.9.0
   Compiling openssl v0.10.81
   Compiling chacha20 v0.10.2
   Compiling zeroize v1.9.0
   Compiling regex v1.13.1
   Compiling crc32fast v1.5.1
   Compiling blake2 v0.10.6
   Compiling fastrand v2.5.0
   Compiling byteorder v1.5.0
   Compiling nu-ansi-term v0.50.3
   Compiling tempfile v3.27.0
   Compiling flexi_logger v0.31.10
   Compiling sqlx v0.9.0
   Compiling fernet v0.2.2
   Compiling argon2 v0.5.3
   Compiling flate2 v1.1.10
   Compiling rand v0.10.2
   Compiling the-last-signal-server v0.1.0 (/home/runner/work/The-last-signal-/The-last-signal-/server_rust)
warning: unused import: `Error`
 --> src/database/database_manager.rs:6:5
  |
6 |     Error,
  |     ^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: fields `user_id` and `password_hash` are never read
  --> src/network/handler.rs:41:5
   |
40 | pub struct User {
   |            ---- fields in this struct
41 |     user_id: String,
   |     ^^^^^^^
42 |     password_hash: String,
   |     ^^^^^^^^^^^^^
   |
   = note: `#[warn(dead_code)]` (part of `#[warn(unused)]`) on by default

warning: constant `PO` is never used
 --> src/gameplay/tresor.rs:8:7
  |
8 | const PO: u32 = PA * 10;
  |       ^^

warning: constant `PP` is never used
 --> src/gameplay/tresor.rs:9:7
  |
9 | const PP: u32 = PO * 10;
  |       ^^

warning: `the-last-signal-server` (lib) generated 4 warnings (run `cargo fix --lib -p the-last-signal-server` to apply 1 suggestion)
warning: unused import: `debug`
 --> src/main.rs:5:11
  |
5 | use log::{debug,info};
  |           ^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `the-last-signal-server` (bin "the-last-signal-server" test) generated 1 warning (run `cargo fix --bin "the-last-signal-server" -p the-last-signal-server --tests` to apply 1 suggestion)
warning: `the-last-signal-server` (lib test) generated 4 warnings (4 duplicates)
warning: `the-last-signal-server` (bin "the-last-signal-server") generated 1 warning (1 duplicate)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 19.25s
     Running unittests src/lib.rs (server_rust/target/debug/deps/the_last_signal_server-cbb2c1b1f7016014)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (server_rust/target/debug/deps/the_last_signal_server-57e5b599d732d645)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/integration_test.rs (server_rust/target/debug/deps/integration_test-22c358623fd8c378)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests the_last_signal_server

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

