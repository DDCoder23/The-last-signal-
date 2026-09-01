# Rust Report

Run : 1158
Branch : main
Commit : 3c3fd15d1a9cb6a96ad7048ef7d610e477b3a29e
Date : Sun Aug 23 11:14:21 UTC 2026


## Cargo fmt
error: expected `{`, found `;`
  --> /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:80:31
   |
80 |                         .await;
   |                               ^ expected `{`
   |
note: the `if` expression is missing a block after this condition
  --> /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs:78:24
   |
78 |                       if let Some(response) =
   |  ________________________^
79 | |                      PacketHandler::handle(self, packet,self.pool.clone())
80 | |                         .await;
   | |______________________________^

Error writing files: failed to resolve mod `client`: cannot parse /home/runner/work/The-last-signal-/The-last-signal-/server_rust/src/network/client.rs
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
   Compiling pin-project-lite v0.2.17
   Compiling yoke v0.8.3
   Compiling smallvec v1.15.2
   Compiling zerovec v0.11.8
   Compiling memchr v2.8.3
   Compiling hybrid-array v0.4.14
   Compiling tinystr v0.8.4
   Compiling jobserver v0.1.35
   Compiling getrandom v0.4.3
   Compiling litemap v0.8.3
   Compiling cc v1.4.4
   Compiling futures-core v0.3.34
   Compiling scopeguard v1.2.0
   Compiling once_cell v1.21.4
   Compiling writeable v0.6.4
   Compiling crypto-common v0.2.2
   Compiling lock_api v0.4.14
   Compiling icu_locale_core v2.3.0
   Compiling zeroize v1.9.0
   Compiling potential_utf v0.1.6
   Compiling zerotrie v0.2.5
   Compiling utf8_iter v1.0.4
   Compiling icu_collections v2.3.0
   Compiling icu_provider v2.3.1
   Compiling serde_core v1.0.229
   Compiling cmov v0.5.4
   Compiling num-traits v0.2.19
   Compiling icu_properties_data v2.3.0
   Compiling ctutils v0.4.2
   Compiling parking_lot_core v0.9.12
   Compiling icu_normalizer_data v2.3.0
   Compiling block-buffer v0.12.1
   Compiling socket2 v0.6.5
   Compiling mio v1.2.2
   Compiling equivalent v1.0.2
   Compiling bytes v1.12.1
   Compiling futures-sink v0.3.34
   Compiling icu_normalizer v2.3.0
   Compiling parking_lot v0.12.5
   Compiling icu_properties v2.3.0
   Compiling iana-time-zone v0.1.65
   Compiling cpufeatures v0.3.0
   Compiling cpufeatures v0.2.17
   Compiling generic-array v0.14.7
   Compiling serde v1.0.229
   Compiling log v0.4.34
   Compiling futures-io v0.3.34
   Compiling hashbrown v0.17.1
   Compiling percent-encoding v2.3.2
   Compiling allocator-api2 v0.2.21
   Compiling idna_adapter v1.2.2
   Compiling slab v0.4.12
   Compiling futures-task v0.3.34
   Compiling foldhash v0.2.0
   Compiling indexmap v2.14.0
   Compiling idna v1.1.0
   Compiling hashbrown v0.16.1
   Compiling futures-util v0.3.34
   Compiling form_urlencoded v1.2.2
   Compiling zmij v1.0.23
   Compiling crossbeam-utils v0.8.22
   Compiling itoa v1.0.18
   Compiling crc-catalog v2.5.0
   Compiling subtle v2.6.1
   Compiling parking v2.2.1
   Compiling serde_json v1.0.151
   Compiling crossbeam-queue v0.3.13
   Compiling event-listener v5.4.2
   Compiling crc v3.4.0
   Compiling url v2.5.8
   Compiling hashlink v0.11.1
   Compiling either v1.18.0
   Compiling block-buffer v0.10.4
   Compiling crypto-common v0.1.7
   Compiling futures-intrusive v0.5.0
   Compiling const-oid v0.10.2
   Compiling digest v0.11.3
   Compiling digest v0.10.7
   Compiling tokio v1.53.1
   Compiling zstd-sys v2.0.16+zstd.1.5.7
   Compiling libsqlite3-sys v0.37.0
   Compiling spin v0.9.9
   Compiling tracing-core v0.1.36
   Compiling inout v0.2.2
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
   Compiling aho-corasick v1.1.5
   Compiling tokio-stream v0.1.19
   Compiling regex-syntax v0.8.11
   Compiling cpubits v0.1.1
   Compiling sqlx-core v0.9.0
   Compiling regex-automata v0.4.18
   Compiling thiserror v2.0.20
   Compiling cipher v0.5.2
   Compiling getrandom v0.2.17
   Compiling simd-adler32 v0.3.10
   Compiling bitflags v2.13.1
   Compiling base64 v0.22.1
   Compiling zstd-safe v7.2.4
   Compiling crc32fast v1.5.1
   Compiling sqlx-sqlite v0.9.0
   Compiling universal-hash v0.6.1
   Compiling uuid v1.25.0
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
   Compiling hmac v0.13.0
   Compiling sha2 v0.11.0
   Compiling bumpalo v3.20.3
   Compiling lazy_static v1.5.0
   Compiling deranged v0.5.8
   Compiling tinyvec_macros v0.1.1
   Compiling nu-ansi-term v0.50.3
   Compiling linux-raw-sys v0.12.1
   Compiling libbz2-rs-sys v0.2.5
   Compiling zlib-rs v0.6.7
   Compiling base64ct v1.8.3
   Compiling powerfmt v0.2.0
   Compiling num-conv v0.2.2
   Compiling time-core v0.1.9
   Compiling time v0.3.55
   Compiling password-hash v0.5.0
   Compiling bzip2 v0.6.1
   Compiling rustix v1.1.4
   Compiling tinyvec v1.12.0
   Compiling lzma-rust2 v0.16.5
   Compiling flate2 v1.1.9
   Compiling sharded-slab v0.1.7
   Compiling zopfli v0.8.3
   Compiling pbkdf2 v0.13.0
   Compiling zstd v0.13.3
   Compiling ghash v0.6.0
   Compiling sqlx-macros v0.9.0
   Compiling matchers v0.2.0
   Compiling regex v1.13.1
   Compiling ctr v0.10.1
   Compiling tracing-log v0.2.0
   Compiling aead v0.6.1
   Compiling blake2 v0.10.6
   Compiling sha1 v0.11.0
   Compiling chacha20 v0.10.1
   Compiling thread_local v1.1.10
   Compiling same-file v1.0.6
   Compiling constant_time_eq v0.4.2
   Compiling ppmd-rust v1.4.0
   Compiling deflate64 v0.1.12
   Compiling fastrand v2.5.0
   Compiling typed-path v0.12.3
   Compiling byteorder v1.5.0
   Compiling tempfile v3.27.0
   Compiling fernet v0.2.2
   Compiling walkdir v2.5.0
   Compiling zip v8.6.0
   Compiling tracing-subscriber v0.3.23
   Compiling rand v0.10.2
   Compiling argon2 v0.5.3
   Compiling aes-gcm v0.11.1
   Compiling sqlx v0.9.0
   Compiling flexi_logger v0.31.10
   Compiling anyhow v1.0.104
   Compiling unicode-normalization v0.1.25
   Compiling base64 v0.23.1
   Compiling the-last-signal-server v0.1.0 (/home/runner/work/The-last-signal-/The-last-signal-/server_rust)
error: expected `{`, found `;`
  --> src/network/client.rs:80:31
   |
80 |                         .await;
   |                               ^ expected `{`
   |
note: the `if` expression is missing a block after this condition
  --> src/network/client.rs:78:24
   |
78 |                       if let Some(response) =
   |  ________________________^
79 | |                      PacketHandler::handle(self, packet,self.pool.clone())
80 | |                         .await;
   | |______________________________^

warning: unused import: `Error`
 --> src/database/database_manager.rs:6:5
  |
6 |     Error,
  |     ^^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: unused import: `uuid::Uuid`
 --> src/database/migrations.rs:2:5
  |
2 | use uuid::Uuid;
  |     ^^^^^^^^^^

warning: unused import: `crate::network::handler::PacketHandler`
 --> src/network/client.rs:8:5
  |
8 | use crate::network::handler::PacketHandler;
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

warning: unused import: `send_packet`
  --> src/network/client.rs:11:5
   |
11 |     send_packet,
   |     ^^^^^^^^^^^

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

error[E0308]: mismatched types
  --> src/network/handler.rs:69:17
   |
35 |     ) -> Option<Packet> {
   |          -------------- expected `std::option::Option<Packet>` because of return type
...
69 |                 Packet::new(PacketType::Ping, b"PONG".to_vec())
   |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
   |
   = note: expected enum `std::option::Option<Packet>`
            found struct `Packet`
help: try wrapping the expression in `Some`
   |
69 |                 Some(Packet::new(PacketType::Ping, b"PONG".to_vec()))
   |                 +++++                                               +

error[E0308]: mismatched types
  --> src/network/handler.rs:78:32
   |
35 |     ) -> Option<Packet> {
   |          -------------- expected `std::option::Option<Packet>` because of return type
...
78 |                         return Packet::new(PacketType::SignUp, b"SIGN_UP invalide".to_vec());
   |                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
   |
   = note: expected enum `std::option::Option<Packet>`
            found struct `Packet`
help: try wrapping the expression in `Some`
   |
78 |                         return Some(Packet::new(PacketType::SignUp, b"SIGN_UP invalide".to_vec()));
   |                                +++++                                                             +

error[E0308]: mismatched types
   --> src/network/handler.rs:116:25
    |
 35 |     ) -> Option<Packet> {
    |          -------------- expected `std::option::Option<Packet>` because of return type
...
116 |                         Packet::new(PacketType::SignUp, b"Utilisateur cree avec succes".to_vec())
    |                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
    |
    = note: expected enum `std::option::Option<Packet>`
             found struct `Packet`
help: try wrapping the expression in `Some`
    |
116 |                         Some(Packet::new(PacketType::SignUp, b"Utilisateur cree avec succes".to_vec()))
    |                         +++++                                                                         +

error[E0308]: mismatched types
   --> src/network/handler.rs:123:29
    |
 35 |     ) -> Option<Packet> {
    |          -------------- expected `std::option::Option<Packet>` because of return type
...
123 |                             Packet::new(PacketType::SignUp, b"Email deja utilise".to_vec())
    |                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
    |
    = note: expected enum `std::option::Option<Packet>`
             found struct `Packet`
help: try wrapping the expression in `Some`
    |
123 |                             Some(Packet::new(PacketType::SignUp, b"Email deja utilise".to_vec()))
    |                             +++++                                                               +

error[E0308]: mismatched types
   --> src/network/handler.rs:126:29
    |
 35 |     ) -> Option<Packet> {
    |          -------------- expected `std::option::Option<Packet>` because of return type
...
126 |                             Packet::new(PacketType::SignUp, b"Erreur serveur".to_vec())
    |                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
    |
    = note: expected enum `std::option::Option<Packet>`
             found struct `Packet`
help: try wrapping the expression in `Some`
    |
126 |                             Some(Packet::new(PacketType::SignUp, b"Erreur serveur".to_vec()))
    |                             +++++                                                           +

error[E0308]: mismatched types
   --> src/network/handler.rs:367:17
    |
 35 |     ) -> Option<Packet> {
    |          -------------- expected `std::option::Option<Packet>` because of return type
...
367 |                 Packet::new(PacketType::Login, format!("Utilisateur {} authentifié", email).into_bytes())
    |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
    |
    = note: expected enum `std::option::Option<Packet>`
             found struct `Packet`
help: try wrapping the expression in `Some`
    |
367 |                 Some(Packet::new(PacketType::Login, format!("Utilisateur {} authentifié", email).into_bytes()))
    |                 +++++                                                                                         +

error[E0308]: mismatched types
   --> src/network/handler.rs:372:17
    |
 35 |     ) -> Option<Packet> {
    |          -------------- expected `std::option::Option<Packet>` because of return type
...
372 |                 Packet::new(PacketType::Chat, packet.payload)
    |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
    |
    = note: expected enum `std::option::Option<Packet>`
             found struct `Packet`
help: try wrapping the expression in `Some`
    |
372 |                 Some(Packet::new(PacketType::Chat, packet.payload))
    |                 +++++                                             +

error[E0308]: mismatched types
   --> src/network/handler.rs:377:17
    |
 35 |     ) -> Option<Packet> {
    |          -------------- expected `std::option::Option<Packet>` because of return type
...
377 |                 Packet::new(PacketType::Move, packet.payload)
    |                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected `Option<Packet>`, found `Packet`
    |
    = note: expected enum `std::option::Option<Packet>`
             found struct `Packet`
help: try wrapping the expression in `Some`
    |
377 |                 Some(Packet::new(PacketType::Move, packet.payload))
    |                 +++++                                             +

For more information about this error, try `rustc --explain E0308`.
warning: `the-last-signal-server` (lib) generated 6 warnings
error: could not compile `the-last-signal-server` (lib) due to 9 previous errors; 6 warnings emitted
warning: build failed, waiting for other jobs to finish...
