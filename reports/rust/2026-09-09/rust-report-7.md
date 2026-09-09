# Rust Report

Run : 1691
Branch : main
Commit : 0f8ddf62a613def0f0d8b2ce12605c82dce40f5b
Date : Wed Sep  9 18:05:53 UTC 2026


## Cargo fmt
error: this file contains an unclosed delimiter
   --> /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/table_de_conversion.rs:580:14
    |
 39 | impl TableDeConversion {
    |                        - unclosed delimiter
...
543 |     ) -> Result<(), String> {
    |                             - unclosed delimiter
...
546 |         for _ in 0..nb {
    |                        - unclosed delimiter
...
580 |             
    |             ^

Error writing files: failed to resolve mod `table_de_conversion`: cannot parse /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/gameplay/table_de_conversion.rs
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:1:
-use the_last_signal_server::database::{
-    database_manager::DatabaseManager,
-    migrations,
-};
 use log::info;
+use the_last_signal_server::database::{database_manager::DatabaseManager, migrations};
 use the_last_signal_server::network::server::Server;
 use the_last_signal_server::utils::logger::logger::ServerLogger;
 
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:9:
 #[tokio::main]
 
 /*
-    Fonction asynchrone exécutée par le runtime Tokio. 
+    Fonction asynchrone exécutée par le runtime Tokio.
     Point d'entrée principal du serveur.
 
     Initialise :
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:20:
 */
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
Diff in /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/main.rs:41:
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
   Compiling pin-project-lite v0.2.17
   Compiling smallvec v1.16.0
   Compiling yoke v0.8.3
   Compiling futures-core v0.3.34
   Compiling writeable v0.6.4
   Compiling typenum v1.20.1
   Compiling zerovec v0.11.8
   Compiling memchr v2.8.3
   Compiling tinystr v0.8.4
   Compiling litemap v0.8.3
   Compiling potential_utf v0.1.6
   Compiling icu_locale_core v2.3.0
   Compiling zerotrie v0.2.5
   Compiling utf8_iter v1.0.4
   Compiling scopeguard v1.2.0
   Compiling lock_api v0.4.14
   Compiling icu_collections v2.3.0
   Compiling icu_normalizer_data v2.3.0
   Compiling icu_properties_data v2.3.0
   Compiling socket2 v0.6.5
   Compiling mio v1.2.3
   Compiling futures-sink v0.3.34
   Compiling bytes v1.12.1
   Compiling serde_core v1.0.229
   Compiling icu_provider v2.3.1
   Compiling icu_normalizer v2.3.0
   Compiling icu_properties v2.3.0
   Compiling equivalent v1.0.2
   Compiling once_cell v1.21.4
   Compiling rand_core v0.10.1
   Compiling generic-array v0.14.9
   Compiling tracing-core v0.1.36
   Compiling parking_lot_core v0.9.12
   Compiling cpufeatures v0.2.17
   Compiling futures-task v0.3.34
   Compiling futures-io v0.3.34
   Compiling idna_adapter v1.2.2
   Compiling slab v0.4.12
   Compiling foldhash v0.2.0
   Compiling allocator-api2 v0.2.21
   Compiling percent-encoding v2.3.2
   Compiling form_urlencoded v1.2.2
   Compiling futures-util v0.3.34
   Compiling idna v1.1.0
   Compiling hashbrown v0.16.1
   Compiling serde v1.0.229
   Compiling num-traits v0.2.19
   Compiling parking_lot v0.12.5
   Compiling crossbeam-utils v0.8.23
   Compiling getrandom v0.4.3
   Compiling zmij v1.0.23
   Compiling hashbrown v0.17.1
   Compiling itoa v1.0.18
   Compiling crc-catalog v2.5.0
   Compiling parking v2.2.1
   Compiling crc v3.4.0
   Compiling event-listener v5.4.2
   Compiling serde_json v1.0.151
   Compiling crossbeam-queue v0.3.14
   Compiling indexmap v2.14.2
   Compiling futures-intrusive v0.5.0
   Compiling either v1.18.0
   Compiling hashlink v0.11.1
   Compiling url v2.5.8
   Compiling block-buffer v0.10.4
   Compiling crypto-common v0.1.6
   Compiling digest v0.10.7
   Compiling tokio v1.53.1
   Compiling spin v0.9.9
   Compiling cmov v0.5.4
   Compiling flume v0.12.0
   Compiling ctutils v0.4.2
   Compiling tracing v0.1.44
   Compiling sha2 v0.10.9
   Compiling futures-executor v0.3.34
   Compiling atoi v2.0.0
   Compiling futures-channel v0.3.34
   Compiling hybrid-array v0.4.15
   Compiling log v0.4.34
   Compiling thiserror v2.0.20
   Compiling base64 v0.22.1
   Compiling block-buffer v0.12.1
   Compiling crypto-common v0.2.2
   Compiling uuid v1.26.0
   Compiling aho-corasick v1.1.5
   Compiling base64ct v1.8.3
   Compiling regex-syntax v0.8.11
   Compiling tokio-stream v0.1.19
   Compiling foreign-types-shared v0.1.1
   Compiling cpufeatures v0.3.1
   Compiling sqlx-core v0.9.0
   Compiling foreign-types v0.3.2
   Compiling regex-automata v0.4.18
   Compiling phc v0.6.1
   Compiling sqlx-sqlite v0.9.0
   Compiling digest v0.11.3
   Compiling libsqlite3-sys v0.37.0
   Compiling sqlx-macros-core v0.9.0
   Compiling openssl-sys v0.9.117
   Compiling iana-time-zone v0.1.65
   Compiling adler2 v2.0.1
   Compiling bitflags v2.13.1
   Compiling simd-adler32 v0.3.10
   Compiling miniz_oxide v0.9.1
   Compiling openssl v0.10.81
   Compiling chrono v0.4.45
   Compiling zeroize v1.9.0
   Compiling sqlx-macros v0.9.0
   Compiling blake2 v0.11.0
   Compiling regex v1.13.1
   Compiling password-hash v0.6.1
   Compiling crc32fast v1.5.1
   Compiling chacha20 v0.10.2
   Compiling getrandom v0.2.17
   Compiling nu-ansi-term v0.50.3
   Compiling byteorder v1.5.0
   Compiling flexi_logger v0.31.10
   Compiling sqlx v0.9.0
   Compiling fernet v0.2.2
   Compiling rand v0.10.2
   Compiling flate2 v1.1.10
   Compiling argon2 v0.6.0
   Compiling the-last-signal-server v0.1.0 (/home/runner/work/The-last-signal-/The-last-signal-/server_rust)
error: this file contains an unclosed delimiter
   --> src/gameplay/table_de_conversion.rs:580:14
    |
 39 | impl TableDeConversion {
    |                        - unclosed delimiter
...
543 |     ) -> Result<(), String> {
    |                             - unclosed delimiter
...
546 |         for _ in 0..nb {
    |                        - unclosed delimiter
...
580 |             
    |             ^

error: could not compile `the-last-signal-server` (lib) due to 1 previous error
warning: build failed, waiting for other jobs to finish...
