# Rust Report

Run : 1459
Branch : main
Commit : 0008b6e8fd2b75a4d70aa9d1e68a4c6f36fa2e41
Date : Tue Sep  1 13:18:33 UTC 2026


## Cargo fmt
error: unknown start of token: `
  --> /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/password.rs:31:1
   |
31 | ```
   | ^^^
   |
   = note: character appears 2 more times
help: Unicode character '`' (Grave Accent) looks like ''' (Single Quote), but it is not
   |
31 - ```
31 + '''
   |

error: unknown start of token: `
  --> /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/password.rs:35:1
   |
35 | ```
   | ^^^
   |
   = note: character appears 2 more times
help: Unicode character '`' (Grave Accent) looks like ''' (Single Quote), but it is not
   |
35 - ```
35 + '''
   |

Error writing files: failed to resolve mod `password`: cannot parse /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/utils/password.rs
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
   Compiling pin-project-lite v0.2.17
   Compiling smallvec v1.15.2
   Compiling yoke v0.8.3
   Compiling writeable v0.6.4
   Compiling zerovec v0.11.8
   Compiling typenum v1.20.1
   Compiling memchr v2.8.3
   Compiling tinystr v0.8.4
   Compiling litemap v0.8.3
   Compiling futures-core v0.3.34
   Compiling potential_utf v0.1.6
   Compiling icu_locale_core v2.3.0
   Compiling zerotrie v0.2.5
   Compiling utf8_iter v1.0.4
   Compiling scopeguard v1.2.0
   Compiling icu_collections v2.3.0
   Compiling lock_api v0.4.14
   Compiling icu_normalizer_data v2.3.0
   Compiling icu_properties_data v2.3.0
   Compiling mio v1.2.2
   Compiling socket2 v0.6.5
   Compiling rand_core v0.10.1
   Compiling futures-sink v0.3.34
   Compiling once_cell v1.21.4
   Compiling icu_provider v2.3.1
   Compiling bytes v1.12.1
   Compiling serde_core v1.0.229
   Compiling icu_properties v2.3.0
   Compiling icu_normalizer v2.3.0
   Compiling equivalent v1.0.2
   Compiling generic-array v0.14.9
   Compiling getrandom v0.4.3
   Compiling parking_lot_core v0.9.12
   Compiling tracing-core v0.1.36
   Compiling foldhash v0.2.0
   Compiling idna_adapter v1.2.2
   Compiling cpufeatures v0.2.17
   Compiling futures-task v0.3.34
   Compiling futures-io v0.3.34
   Compiling slab v0.4.12
   Compiling percent-encoding v2.3.2
   Compiling allocator-api2 v0.2.21
   Compiling form_urlencoded v1.2.2
   Compiling futures-util v0.3.34
   Compiling idna v1.1.0
   Compiling hashbrown v0.16.1
   Compiling serde v1.0.229
   Compiling parking_lot v0.12.5
   Compiling num-traits v0.2.19
   Compiling zmij v1.0.23
   Compiling crossbeam-utils v0.8.22
   Compiling itoa v1.0.18
   Compiling hashbrown v0.17.1
   Compiling crc-catalog v2.5.0
   Compiling parking v2.2.1
   Compiling crc v3.4.0
   Compiling event-listener v5.4.2
   Compiling crossbeam-queue v0.3.13
   Compiling serde_json v1.0.151
   Compiling either v1.18.0
   Compiling indexmap v2.14.1
   Compiling futures-intrusive v0.5.0
   Compiling hashlink v0.11.1
   Compiling url v2.5.8
   Compiling block-buffer v0.10.4
   Compiling crypto-common v0.1.6
   Compiling digest v0.10.7
   Compiling tokio v1.53.1
   Compiling spin v0.9.9
   Compiling cmov v0.5.4
   Compiling tracing v0.1.44
   Compiling flume v0.12.0
   Compiling ctutils v0.4.2
   Compiling sha2 v0.10.9
   Compiling futures-executor v0.3.34
   Compiling atoi v2.0.0
   Compiling futures-channel v0.3.34
   Compiling hybrid-array v0.4.14
   Compiling log v0.4.34
   Compiling thiserror v2.0.20
   Compiling base64 v0.22.1
   Compiling bitflags v2.13.1
   Compiling block-buffer v0.12.1
   Compiling crypto-common v0.2.2
   Compiling uuid v1.26.0
   Compiling aho-corasick v1.1.5
   Compiling base64ct v1.8.3
   Compiling regex-syntax v0.8.11
   Compiling tokio-stream v0.1.19
   Compiling sqlx-core v0.9.0
   Compiling cpufeatures v0.3.1
   Compiling foreign-types-shared v0.1.1
   Compiling foreign-types v0.3.2
   Compiling regex-automata v0.4.18
   Compiling phc v0.6.1
   Compiling sqlx-sqlite v0.9.0
   Compiling digest v0.11.3
   Compiling libsqlite3-sys v0.37.0
   Compiling sqlx-macros-core v0.9.0
   Compiling openssl-sys v0.9.117
   Compiling getrandom v0.2.17
   Compiling adler2 v2.0.1
   Compiling simd-adler32 v0.3.10
   Compiling linux-raw-sys v0.12.1
   Compiling iana-time-zone v0.1.65
   Compiling rustix v1.1.4
   Compiling chrono v0.4.45
   Compiling miniz_oxide v0.9.1
   Compiling sqlx-macros v0.9.0
   Compiling zeroize v1.9.0
   Compiling openssl v0.10.81
   Compiling blake2 v0.11.0
   Compiling regex v1.13.1
   Compiling password-hash v0.6.1
   Compiling crc32fast v1.5.1
   Compiling chacha20 v0.10.2
   Compiling fastrand v2.5.0
   Compiling nu-ansi-term v0.50.3
   Compiling byteorder v1.5.0
   Compiling flexi_logger v0.31.10
   Compiling tempfile v3.27.0
   Compiling sqlx v0.9.0
   Compiling rand v0.10.2
   Compiling fernet v0.2.2
   Compiling flate2 v1.1.10
   Compiling argon2 v0.6.0
   Compiling rand_core v0.6.4
   Compiling the-last-signal-server v0.1.0 (/home/runner/work/The-last-signal-/The-last-signal-/server_rust)
error: unknown start of token: `
  --> src/utils/password.rs:31:1
   |
31 | ```
   | ^^^
   |
   = note: character appears 2 more times
help: Unicode character '`' (Grave Accent) looks like ''' (Single Quote), but it is not
   |
31 - ```
31 + '''
   |

error: unknown start of token: `
  --> src/utils/password.rs:35:1
   |
35 | ```
   | ^^^
   |
   = note: character appears 2 more times
help: Unicode character '`' (Grave Accent) looks like ''' (Single Quote), but it is not
   |
35 - ```
35 + '''
   |

warning: unused import: `Error`
 --> src/database/database_manager.rs:6:5
  |
6 |     Error,
  |     ^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `the-last-signal-server` (lib) generated 1 warning
error: could not compile `the-last-signal-server` (lib) due to 2 previous errors; 1 warning emitted
warning: build failed, waiting for other jobs to finish...
warning: `the-last-signal-server` (lib test) generated 1 warning (1 duplicate)
error: could not compile `the-last-signal-server` (lib test) due to 2 previous errors; 1 warning emitted
