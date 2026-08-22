# Build Report

Run : 617
OS : macos-latest
Branch : main
Commit : be7d5f4e5becb7c791953fb846c4b331843242c5
Date : Sat Aug 22 22:16:17 UTC 2026


## Python
Listing 'client_python'...
Compiling 'client_python/__init__.py'...
Compiling 'client_python/client.py'...
Compiling 'client_python/logs.py'...
Compiling 'client_python/main.py'...
Compiling 'client_python/packet.py'...
Listing 'client_python/packets'...
Compiling 'client_python/packets/__init__.py'...
Compiling 'client_python/packets/chat.py'...
Compiling 'client_python/packets/log.py'...
Compiling 'client_python/packets/login.py'...
Compiling 'client_python/packets/move.py'...
Compiling 'client_python/packets/ping.py'...
Compiling 'client_python/packets/singup.py'...
Listing 'tests'...
Compiling 'tests/__init__.py'...
Compiling 'tests/test_client.py'...
Compiling 'tests/test_crypto_rotor.py'...
Compiling 'tests/test_fuzzing.py'...
Compiling 'tests/test_load.py'...
Compiling 'tests/test_sql_injection.py'...

## Rust
[1m[92m    Updating[0m crates.io index
[1m[92m     Locking[0m 237 packages to latest Rust 1.98.0 compatible versions
[1m[92m      Adding[0m generic-array v0.14.7 [1m[33m(available: v0.14.9)[0m
[1m[92m      Adding[0m rand_core v0.6.4 [1m[33m(available: v0.10.1)[0m
[1m[92m Downloading[0m crates ...
[1m[92m  Downloaded[0m base64 v0.23.1
[1m[92m  Downloaded[0m aho-corasick v1.1.5
[1m[92m  Downloaded[0m aes v0.9.2
[1m[92m  Downloaded[0m blake2 v0.10.6
[1m[92m  Downloaded[0m aes-gcm v0.11.1
[1m[92m  Downloaded[0m anyhow v1.0.104
[1m[92m  Downloaded[0m allocator-api2 v0.2.21
[1m[92m  Downloaded[0m atoi v2.0.0
[1m[92m  Downloaded[0m bitflags v2.13.1
[1m[92m  Downloaded[0m argon2 v0.5.3
[1m[92m  Downloaded[0m bumpalo v3.20.3
[1m[92m  Downloaded[0m autocfg v1.5.1
[1m[92m  Downloaded[0m block-buffer v0.12.1
[1m[92m  Downloaded[0m time-core v0.1.9
[1m[92m  Downloaded[0m adler2 v2.0.1
[1m[92m  Downloaded[0m md-5 v0.11.0
[1m[92m  Downloaded[0m num-conv v0.2.2
[1m[92m  Downloaded[0m openssl-macros v0.1.1
[1m[92m  Downloaded[0m percent-encoding v2.3.2
[1m[92m  Downloaded[0m block-buffer v0.10.4
[1m[92m  Downloaded[0m zstd v0.13.3
[1m[92m  Downloaded[0m parking_lot v0.12.5
[1m[92m  Downloaded[0m password-hash v0.5.0
[1m[92m  Downloaded[0m pkg-config v0.3.34
[1m[92m  Downloaded[0m polyval v0.7.3
[1m[92m  Downloaded[0m potential_utf v0.1.6
[1m[92m  Downloaded[0m rand_core v0.10.1
[1m[92m  Downloaded[0m scopeguard v1.2.0
[1m[92m  Downloaded[0m sha2 v0.11.0
[1m[92m  Downloaded[0m synstructure v0.13.2
[1m[92m  Downloaded[0m tracing-attributes v0.1.31
[1m[92m  Downloaded[0m unicode-bidi v0.3.18
[1m[92m  Downloaded[0m cfg-if v1.0.4
[1m[92m  Downloaded[0m chacha20 v0.10.1
[1m[92m  Downloaded[0m cipher v0.5.2
[1m[92m  Downloaded[0m core-foundation-sys v0.8.7
[1m[92m  Downloaded[0m crc32fast v1.5.1
[1m[92m  Downloaded[0m crypto-common v0.1.7
[1m[92m  Downloaded[0m crypto-common v0.2.2
[1m[92m  Downloaded[0m digest v0.11.3
[1m[92m  Downloaded[0m fernet v0.2.2
[1m[92m  Downloaded[0m find-msvc-tools v0.1.11
[1m[92m  Downloaded[0m futures-io v0.3.34
[1m[92m  Downloaded[0m futures-task v0.3.34
[1m[92m  Downloaded[0m hashbrown v0.16.1
[1m[92m  Downloaded[0m hashlink v0.11.1
[1m[92m  Downloaded[0m hmac v0.13.0
[1m[92m  Downloaded[0m icu_normalizer_data v2.3.0
[1m[92m  Downloaded[0m lazy_static v1.5.0
[1m[92m  Downloaded[0m zeroize v1.9.0
[1m[92m  Downloaded[0m zerovec v0.11.8
[1m[92m  Downloaded[0m zerovec-derive v0.11.6
[1m[92m  Downloaded[0m zopfli v0.8.3
[1m[92m  Downloaded[0m lock_api v0.4.14
[1m[92m  Downloaded[0m matchers v0.2.0
[1m[92m  Downloaded[0m miniz_oxide v0.8.9
[1m[92m  Downloaded[0m num-traits v0.2.19
[1m[92m  Downloaded[0m ppmd-rust v1.4.0
[1m[92m  Downloaded[0m proc-macro2 v1.0.107
[1m[92m  Downloaded[0m rand v0.10.2
[1m[92m  Downloaded[0m regex v1.13.1
[1m[92m  Downloaded[0m serde_core v1.0.229
[1m[92m  Downloaded[0m serde_derive v1.0.229
[1m[92m  Downloaded[0m sharded-slab v0.1.7
[1m[92m  Downloaded[0m socket2 v0.6.5
[1m[92m  Downloaded[0m sqlx-core v0.9.0
[1m[92m  Downloaded[0m sqlx-mysql v0.9.0
[1m[92m  Downloaded[0m sqlx-sqlite v0.9.0
[1m[92m  Downloaded[0m thiserror-impl v2.0.20
[1m[92m  Downloaded[0m bzip2 v0.6.1
[1m[92m  Downloaded[0m cc v1.4.4
[1m[92m  Downloaded[0m constant_time_eq v0.4.2
[1m[92m  Downloaded[0m cpubits v0.1.1
[1m[92m  Downloaded[0m cpufeatures v0.2.17
[1m[92m  Downloaded[0m cpufeatures v0.3.0
[1m[92m  Downloaded[0m crc v3.4.0
[1m[92m  Downloaded[0m crossbeam-queue v0.3.13
[1m[92m  Downloaded[0m crossbeam-utils v0.8.22
[1m[92m  Downloaded[0m ctr v0.10.1
[1m[92m  Downloaded[0m deflate64 v0.1.12
[1m[92m  Downloaded[0m deranged v0.5.8
[1m[92m  Downloaded[0m foreign-types v0.3.2
[1m[92m  Downloaded[0m foreign-types-shared v0.1.1
[1m[92m  Downloaded[0m futures-executor v0.3.34
[1m[92m  Downloaded[0m futures-sink v0.3.34
[1m[92m  Downloaded[0m itoa v1.0.18
[1m[92m  Downloaded[0m zip v8.6.0
[1m[92m  Downloaded[0m zlib-rs v0.6.7
[1m[92m  Downloaded[0m zstd-safe v7.2.4
[1m[92m  Downloaded[0m mio v1.2.2
[1m[92m  Downloaded[0m parking v2.2.1
[1m[92m  Downloaded[0m rand_core v0.6.4
[1m[92m  Downloaded[0m sha2 v0.10.9
[1m[92m  Downloaded[0m shlex v2.0.1
[1m[92m  Downloaded[0m stringprep v0.1.5
[1m[92m  Downloaded[0m thiserror v2.0.20
[1m[92m  Downloaded[0m tinystr v0.8.4
[1m[92m  Downloaded[0m tokio-macros v2.7.2
[1m[92m  Downloaded[0m typenum v1.20.1
[1m[92m  Downloaded[0m universal-hash v0.6.1
[1m[92m  Downloaded[0m openssl-sys v0.9.117
[1m[92m  Downloaded[0m tinyvec_macros v0.1.1
[1m[92m  Downloaded[0m tracing-log v0.2.0
[1m[92m  Downloaded[0m base64ct v1.8.3
[1m[92m  Downloaded[0m ctutils v0.4.2
[1m[92m  Downloaded[0m form_urlencoded v1.2.2
[1m[92m  Downloaded[0m futures-core v0.3.34
[1m[92m  Downloaded[0m generic-array v0.14.7
[1m[92m  Downloaded[0m heck v0.5.0
[1m[92m  Downloaded[0m hex v0.4.3
[1m[92m  Downloaded[0m inout v0.2.2
[1m[92m  Downloaded[0m litemap v0.8.3
[1m[92m  Downloaded[0m zmij v1.0.23
[1m[92m  Downloaded[0m nu-ansi-term v0.50.3
[1m[92m  Downloaded[0m once_cell v1.21.4
[1m[92m  Downloaded[0m parking_lot_core v0.9.12
[1m[92m  Downloaded[0m powerfmt v0.2.0
[1m[92m  Downloaded[0m quote v1.0.47
[1m[92m  Downloaded[0m regex-syntax v0.8.11
[1m[92m  Downloaded[0m same-file v1.0.6
[1m[92m  Downloaded[0m sha1 v0.11.0
[1m[92m  Downloaded[0m slab v0.4.12
[1m[92m  Downloaded[0m smallvec v1.15.2
[1m[92m  Downloaded[0m spin v0.9.9
[1m[92m  Downloaded[0m sqlx-macros-core v0.9.0
[1m[92m  Downloaded[0m subtle v2.6.1
[1m[92m  Downloaded[0m writeable v0.6.4
[1m[92m  Downloaded[0m zerofrom-derive v0.1.7
[1m[92m  Downloaded[0m version_check v0.9.5
[1m[92m  Downloaded[0m byteorder v1.5.0
[1m[92m  Downloaded[0m cmov v0.5.4
[1m[92m  Downloaded[0m crc-catalog v2.5.0
[1m[92m  Downloaded[0m displaydoc v0.2.7
[1m[92m  Downloaded[0m dotenvy v0.15.7
[1m[92m  Downloaded[0m either v1.18.0
[1m[92m  Downloaded[0m equivalent v1.0.2
[1m[92m  Downloaded[0m errno v0.3.14
[1m[92m  Downloaded[0m fastrand v2.5.0
[1m[92m  Downloaded[0m foldhash v0.2.0
[1m[92m  Downloaded[0m ghash v0.6.0
[1m[92m  Downloaded[0m hybrid-array v0.4.14
[1m[92m  Downloaded[0m iana-time-zone v0.1.65
[1m[92m  Downloaded[0m idna_adapter v1.2.2
[1m[92m  Downloaded[0m jobserver v0.1.35
[1m[92m  Downloaded[0m zeroize_derive v1.5.0
[1m[92m  Downloaded[0m zerotrie v0.2.5
[1m[92m  Downloaded[0m memchr v2.8.3
[1m[92m  Downloaded[0m pbkdf2 v0.13.0
[1m[92m  Downloaded[0m pin-project-lite v0.2.17
[1m[92m  Downloaded[0m rustix v1.1.4
[1m[92m  Downloaded[0m simd-adler32 v0.3.10
[1m[92m  Downloaded[0m sqlx-macros v0.9.0
[1m[92m  Downloaded[0m whoami v2.1.3
[1m[92m  Downloaded[0m utf8_iter v1.0.4
[1m[92m  Downloaded[0m yoke v0.8.3
[1m[92m  Downloaded[0m unicode-properties v0.1.4
[1m[92m  Downloaded[0m aead v0.6.1
[1m[92m  Downloaded[0m base64 v0.22.1
[1m[92m  Downloaded[0m digest v0.10.7
[1m[92m  Downloaded[0m event-listener v5.4.2
[1m[92m  Downloaded[0m futures-channel v0.3.34
[1m[92m  Downloaded[0m getrandom v0.2.17
[1m[92m  Downloaded[0m getrandom v0.4.3
[1m[92m  Downloaded[0m icu_provider v2.3.1
[1m[92m  Downloaded[0m libbz2-rs-sys v0.2.5
[1m[92m  Downloaded[0m serde v1.0.229
[1m[92m  Downloaded[0m tinyvec v1.12.0
[1m[92m  Downloaded[0m typed-path v0.12.3
[1m[92m  Downloaded[0m zerofrom v0.1.8
[1m[92m  Downloaded[0m yoke-derive v0.8.2
[1m[92m  Downloaded[0m const-oid v0.10.2
[1m[92m  Downloaded[0m flume v0.12.0
[1m[92m  Downloaded[0m icu_locale_core v2.3.0
[1m[92m  Downloaded[0m serde_json v1.0.151
[1m[92m  Downloaded[0m uuid v1.25.0
[1m[92m  Downloaded[0m walkdir v2.5.0
[1m[92m  Downloaded[0m bytes v1.12.1
[1m[92m  Downloaded[0m flate2 v1.1.9
[1m[92m  Downloaded[0m icu_collections v2.3.0
[1m[92m  Downloaded[0m indexmap v2.14.0
[1m[92m  Downloaded[0m lzma-rust2 v0.16.5
[1m[92m  Downloaded[0m sqlx v0.9.0
[1m[92m  Downloaded[0m url v2.5.8
[1m[92m  Downloaded[0m futures-intrusive v0.5.0
[1m[92m  Downloaded[0m unicode-normalization v0.1.25
[1m[92m  Downloaded[0m icu_properties v2.3.0
[1m[92m  Downloaded[0m openssl v0.10.81
[1m[92m  Downloaded[0m stable_deref_trait v1.2.1
[1m[92m  Downloaded[0m thread_local v1.1.10
[1m[92m  Downloaded[0m tokio-stream v0.1.19
[1m[92m  Downloaded[0m hkdf v0.13.0
[1m[92m  Downloaded[0m idna v1.1.0
[1m[92m  Downloaded[0m tempfile v3.27.0
[1m[92m  Downloaded[0m hashbrown v0.17.1
[1m[92m  Downloaded[0m signal-hook-registry v1.4.8
[1m[92m  Downloaded[0m syn v2.0.119
[1m[92m  Downloaded[0m syn v3.0.3
[1m[92m  Downloaded[0m unicode-ident v1.0.24
[1m[92m  Downloaded[0m futures-util v0.3.34
[1m[92m  Downloaded[0m icu_properties_data v2.3.0
[1m[92m  Downloaded[0m tracing-core v0.1.36
[1m[92m  Downloaded[0m chrono v0.4.45
[1m[92m  Downloaded[0m zstd-sys v2.0.16+zstd.1.5.7
[1m[92m  Downloaded[0m log v0.4.34
[1m[92m  Downloaded[0m vcpkg v0.2.15
[1m[92m  Downloaded[0m flexi_logger v0.31.10
[1m[92m  Downloaded[0m sqlx-postgres v0.9.0
[1m[92m  Downloaded[0m tracing v0.1.44
[1m[92m  Downloaded[0m time v0.3.55
[1m[92m  Downloaded[0m regex-automata v0.4.18
[1m[92m  Downloaded[0m tracing-subscriber v0.3.23
[1m[92m  Downloaded[0m icu_normalizer v2.3.0
[1m[92m  Downloaded[0m tokio v1.53.1
[1m[92m  Downloaded[0m libc v0.2.189
[1m[92m  Downloaded[0m libsqlite3-sys v0.37.0
[1m[92m   Compiling[0m proc-macro2 v1.0.107
[1m[92m   Compiling[0m unicode-ident v1.0.24
[1m[92m   Compiling[0m quote v1.0.47
[1m[92m   Compiling[0m libc v0.2.189
[1m[92m   Compiling[0m cfg-if v1.0.4
[1m[92m   Compiling[0m typenum v1.20.1
[1m[92m   Compiling[0m syn v2.0.119
[1m[92m   Compiling[0m syn v3.0.3
[1m[92m   Compiling[0m jobserver v0.1.35
[1m[92m   Compiling[0m find-msvc-tools v0.1.11
[1m[92m   Compiling[0m shlex v2.0.1
[1m[92m   Compiling[0m cc v1.4.4
[1m[92m   Compiling[0m pkg-config v0.3.34
[1m[92m   Compiling[0m synstructure v0.13.2
[1m[92m   Compiling[0m rand_core v0.10.1
[1m[92m   Compiling[0m getrandom v0.4.3
[1m[92m   Compiling[0m zerovec-derive v0.11.6
[1m[92m   Compiling[0m displaydoc v0.2.7
[1m[92m   Compiling[0m zerofrom-derive v0.1.7
[1m[92m   Compiling[0m yoke-derive v0.8.2
[1m[92m   Compiling[0m version_check v0.9.5
[1m[92m   Compiling[0m generic-array v0.14.7
[1m[92m   Compiling[0m icu_normalizer_data v2.3.0
[1m[92m   Compiling[0m serde_core v1.0.229
[1m[92m   Compiling[0m icu_properties_data v2.3.0
[1m[92m   Compiling[0m zerofrom v0.1.8
[1m[92m   Compiling[0m hybrid-array v0.4.14
[1m[92m   Compiling[0m stable_deref_trait v1.2.1
[1m[92m   Compiling[0m yoke v0.8.3
[1m[92m   Compiling[0m vcpkg v0.2.15
[1m[92m   Compiling[0m parking_lot_core v0.9.12
[1m[92m   Compiling[0m autocfg v1.5.1
[1m[92m   Compiling[0m num-traits v0.2.19
[1m[92m   Compiling[0m crypto-common v0.2.2
[1m[92m   Compiling[0m zerovec v0.11.8
[1m[92m   Compiling[0m serde v1.0.229
[1m[92m   Compiling[0m zeroize_derive v1.5.0
[1m[92m   Compiling[0m zeroize v1.9.0
[1m[92m   Compiling[0m serde_derive v1.0.229
[1m[92m   Compiling[0m zmij v1.0.23
[1m[92m   Compiling[0m smallvec v1.15.2
[1m[92m   Compiling[0m crossbeam-utils v0.8.22
[1m[92m   Compiling[0m memchr v2.8.3
[1m[92m   Compiling[0m tinystr v0.8.4
[1m[92m   Compiling[0m litemap v0.8.3
[1m[92m   Compiling[0m writeable v0.6.4
[1m[92m   Compiling[0m cmov v0.5.4
[1m[92m   Compiling[0m icu_locale_core v2.3.0
[1m[92m   Compiling[0m ctutils v0.4.2
[1m[92m   Compiling[0m block-buffer v0.12.1
[1m[92m   Compiling[0m potential_utf v0.1.6
[1m[92m   Compiling[0m zerotrie v0.2.5
[1m[92m   Compiling[0m futures-core v0.3.34
[1m[92m   Compiling[0m utf8_iter v1.0.4
[1m[92m   Compiling[0m pin-project-lite v0.2.17
[1m[92m   Compiling[0m serde_json v1.0.151
[1m[92m   Compiling[0m icu_collections v2.3.0
[1m[92m   Compiling[0m icu_provider v2.3.1
[1m[92m   Compiling[0m tracing-attributes v0.1.31
[1m[92m   Compiling[0m thiserror-impl v2.0.20
[1m[92m   Compiling[0m scopeguard v1.2.0
[1m[92m   Compiling[0m lock_api v0.4.14
[1m[92m   Compiling[0m futures-sink v0.3.34
[1m[92m   Compiling[0m log v0.4.34
[1m[92m   Compiling[0m icu_properties v2.3.0
[1m[92m   Compiling[0m icu_normalizer v2.3.0
[1m[92m   Compiling[0m errno v0.3.14
[1m[92m   Compiling[0m cpufeatures v0.3.0
[1m[92m   Compiling[0m equivalent v1.0.2
[1m[92m   Compiling[0m once_cell v1.21.4
[1m[92m   Compiling[0m subtle v2.6.1
[1m[92m   Compiling[0m idna_adapter v1.2.2
[1m[92m   Compiling[0m block-buffer v0.10.4
[1m[92m   Compiling[0m crypto-common v0.1.7
[1m[92m   Compiling[0m mio v1.2.2
[1m[92m   Compiling[0m socket2 v0.6.5
[1m[92m   Compiling[0m futures-task v0.3.34
[1m[92m   Compiling[0m thiserror v2.0.20
[1m[92m   Compiling[0m futures-io v0.3.34
[1m[92m   Compiling[0m const-oid v0.10.2
[1m[92m   Compiling[0m foldhash v0.2.0
[1m[92m   Compiling[0m core-foundation-sys v0.8.7
[1m[92m   Compiling[0m percent-encoding v2.3.2
[1m[92m   Compiling[0m slab v0.4.12
[1m[92m   Compiling[0m allocator-api2 v0.2.21
[1m[92m   Compiling[0m bytes v1.12.1
[1m[92m   Compiling[0m iana-time-zone v0.1.65
[1m[92m   Compiling[0m futures-util v0.3.34
[1m[92m   Compiling[0m hashbrown v0.16.1
[1m[92m   Compiling[0m tokio v1.53.1
[1m[92m   Compiling[0m form_urlencoded v1.2.2
[1m[92m   Compiling[0m tracing-core v0.1.36
[1m[92m   Compiling[0m digest v0.11.3
[1m[92m   Compiling[0m digest v0.10.7
[1m[92m   Compiling[0m idna v1.1.0
[1m[92m   Compiling[0m parking_lot v0.12.5
[1m[92m   Compiling[0m libsqlite3-sys v0.37.0
[1m[92m   Compiling[0m inout v0.2.2
[1m[92m   Compiling[0m zstd-sys v2.0.16+zstd.1.5.7
[1m[92m   Compiling[0m cpufeatures v0.2.17
[1m[92m   Compiling[0m itoa v1.0.18
[1m[92m   Compiling[0m parking v2.2.1
[1m[92m   Compiling[0m hashbrown v0.17.1
[1m[92m   Compiling[0m crc-catalog v2.5.0
[1m[92m   Compiling[0m crc v3.4.0
[1m[92m   Compiling[0m tracing v0.1.44
[1m[92m   Compiling[0m event-listener v5.4.2
[1m[92m   Compiling[0m indexmap v2.14.0
[1m[92m   Compiling[0m sha2 v0.10.9
[1m[92m   Compiling[0m futures-intrusive v0.5.0
[1m[92m   Compiling[0m tokio-stream v0.1.19
[1m[92m   Compiling[0m url v2.5.8
[1m[92m   Compiling[0m crossbeam-queue v0.3.13
[1m[92m   Compiling[0m either v1.18.0
[1m[92m   Compiling[0m hashlink v0.11.1
[1m[92m   Compiling[0m chrono v0.4.45
[1m[92m   Compiling[0m signal-hook-registry v1.4.8
[1m[92m   Compiling[0m spin v0.9.9
[1m[92m   Compiling[0m aho-corasick v1.1.5
[1m[92m   Compiling[0m openssl-sys v0.9.117
[1m[92m   Compiling[0m tokio-macros v2.7.2
[1m[92m   Compiling[0m base64 v0.22.1
[1m[92m   Compiling[0m cpubits v0.1.1
[1m[92m   Compiling[0m regex-syntax v0.8.11
[1m[92m   Compiling[0m crc32fast v1.5.1
[1m[92m   Compiling[0m uuid v1.25.0
[1m[92m   Compiling[0m regex-automata v0.4.18
[1m[92m   Compiling[0m sqlx-core v0.9.0
[1m[92m   Compiling[0m flume v0.12.0
[1m[92m   Compiling[0m cipher v0.5.2
[1m[92m   Compiling[0m futures-executor v0.3.34
[1m[92m   Compiling[0m atoi v2.0.0
[1m[92m   Compiling[0m futures-channel v0.3.34
[1m[92m   Compiling[0m getrandom v0.2.17
[1m[92m   Compiling[0m simd-adler32 v0.3.10
[1m[92m   Compiling[0m bitflags v2.13.1
[1m[92m   Compiling[0m zstd-safe v7.2.4
[1m[92m   Compiling[0m sqlx-sqlite v0.9.0
[1m[92m   Compiling[0m universal-hash v0.6.1
[1m[92m   Compiling[0m heck v0.5.0
[1m[92m   Compiling[0m dotenvy v0.15.7
[1m[92m   Compiling[0m rustix v1.1.4
[1m[92m   Compiling[0m hex v0.4.3
[1m[92m   Compiling[0m openssl v0.10.81
[1m[92m   Compiling[0m adler2 v2.0.1
[1m[92m   Compiling[0m foreign-types-shared v0.1.1
[1m[92m   Compiling[0m miniz_oxide v0.8.9
[1m[92m   Compiling[0m foreign-types v0.3.2
[1m[92m   Compiling[0m sqlx-macros-core v0.9.0
[1m[92m   Compiling[0m polyval v0.7.3
[1m[92m   Compiling[0m rand_core v0.6.4
[1m[92m   Compiling[0m aes v0.9.2
[1m[92m   Compiling[0m sha2 v0.11.0
[1m[92m   Compiling[0m hmac v0.13.0
[1m[92m   Compiling[0m openssl-macros v0.1.1
[1m[92m   Compiling[0m anyhow v1.0.104
[1m[92m   Compiling[0m lazy_static v1.5.0
[1m[92m   Compiling[0m nu-ansi-term v0.50.3
[1m[92m   Compiling[0m powerfmt v0.2.0
[1m[92m   Compiling[0m time-core v0.1.9
[1m[92m   Compiling[0m num-conv v0.2.2
[1m[92m   Compiling[0m bumpalo v3.20.3
[1m[92m   Compiling[0m libbz2-rs-sys v0.2.5
[1m[92m   Compiling[0m deranged v0.5.8
[1m[92m   Compiling[0m tinyvec_macros v0.1.1
[1m[92m   Compiling[0m zlib-rs v0.6.7
[1m[92m   Compiling[0m base64ct v1.8.3
[1m[92m   Compiling[0m password-hash v0.5.0
[1m[92m   Compiling[0m time v0.3.55
[1m[92m   Compiling[0m flate2 v1.1.9
[1m[92m   Compiling[0m tinyvec v1.12.0
[1m[92m   Compiling[0m bzip2 v0.6.1
[1m[92m   Compiling[0m zopfli v0.8.3
[1m[92m   Compiling[0m sharded-slab v0.1.7
[1m[92m   Compiling[0m pbkdf2 v0.13.0
[1m[92m   Compiling[0m lzma-rust2 v0.16.5
[1m[92m   Compiling[0m zstd v0.13.3
[1m[92m   Compiling[0m ghash v0.6.0
[1m[92m   Compiling[0m sqlx-macros v0.9.0
[1m[92m   Compiling[0m ctr v0.10.1
[1m[92m   Compiling[0m regex v1.13.1
[1m[92m   Compiling[0m matchers v0.2.0
[1m[92m   Compiling[0m aead v0.6.1
[1m[92m   Compiling[0m tracing-log v0.2.0
[1m[92m   Compiling[0m blake2 v0.10.6
[1m[92m   Compiling[0m sha1 v0.11.0
[1m[92m   Compiling[0m chacha20 v0.10.1
[1m[92m   Compiling[0m thread_local v1.1.10
[1m[92m   Compiling[0m deflate64 v0.1.12
[1m[92m   Compiling[0m same-file v1.0.6
[1m[92m   Compiling[0m ppmd-rust v1.4.0
[1m[92m   Compiling[0m byteorder v1.5.0
[1m[92m   Compiling[0m typed-path v0.12.3
[1m[92m   Compiling[0m constant_time_eq v0.4.2
[1m[92m   Compiling[0m fastrand v2.5.0
[1m[92m   Compiling[0m tempfile v3.27.0
[1m[92m   Compiling[0m zip v8.6.0
[1m[92m   Compiling[0m fernet v0.2.2
[1m[92m   Compiling[0m walkdir v2.5.0
[1m[92m   Compiling[0m tracing-subscriber v0.3.23
[1m[92m   Compiling[0m rand v0.10.2
[1m[92m   Compiling[0m argon2 v0.5.3
[1m[92m   Compiling[0m flexi_logger v0.31.10
[1m[92m   Compiling[0m aes-gcm v0.11.1
[1m[92m   Compiling[0m sqlx v0.9.0
[1m[92m   Compiling[0m unicode-normalization v0.1.25
[1m[92m   Compiling[0m base64 v0.23.1
[1m[92m   Compiling[0m the-last-signal-server v0.1.0 (/Users/runner/work/The-last-signal-/The-last-signal-/server_rust)
[1m[33mwarning[0m[1m: unused import: `Error`[0m
 [1m[94m--> [0msrc/database/database_manager.rs:6:5
  [1m[94m|[0m
[1m[94m6[0m [1m[94m|[0m     Error,
  [1m[94m|[0m     [1m[33m^^^^^[0m
  [1m[94m|[0m
  [1m[94m= [0m[1mnote[0m: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

[1m[33mwarning[0m[1m: unused import: `uuid::Uuid`[0m
 [1m[94m--> [0msrc/database/migrations.rs:2:5
  [1m[94m|[0m
[1m[94m2[0m [1m[94m|[0m use uuid::Uuid;
  [1m[94m|[0m     [1m[33m^^^^^^^^^^[0m

[1m[33mwarning[0m[1m: unused import: `Rng`[0m
 [1m[94m--> [0msrc/gameplay/dice.rs:1:12
  [1m[94m|[0m
[1m[94m1[0m [1m[94m|[0m use rand::{Rng,RngExt};
  [1m[94m|[0m            [1m[33m^^^[0m

[1m[33mwarning[0m[1m: unused import: `log::debug`[0m
 [1m[94m--> [0msrc/gameplay/tresor.rs:4:5
  [1m[94m|[0m
[1m[94m4[0m [1m[94m|[0m use log::debug;
  [1m[94m|[0m     [1m[33m^^^^^^^^^^[0m

[1m[91merror[E0616][0m[1m: field `user_id` of struct `Client` is private[0m
   [1m[94m--> [0msrc/network/handler.rs:115:32
    [1m[94m|[0m
[1m[94m115[0m [1m[94m|[0m                         client.user_id = Some(user_id.clone());
    [1m[94m|[0m                                [1m[91m^^^^^^^[0m [1m[91mprivate field[0m

[1m[91merror[E0616][0m[1m: field `user_id` of struct `Client` is private[0m
   [1m[94m--> [0msrc/network/handler.rs:366:24
    [1m[94m|[0m
[1m[94m366[0m [1m[94m|[0m                 client.user_id = Some(login_data.user_id.clone());
    [1m[94m|[0m                        [1m[91m^^^^^^^[0m [1m[91mprivate field[0m

[1mFor more information about this error, try `rustc --explain E0616`.[0m
[1m[33mwarning[0m: `the-last-signal-server` (lib) generated 4 warnings
[1m[91merror[0m: could not compile `the-last-signal-server` (lib) due to 2 previous errors; 4 warnings emitted
[1m[33mwarning[0m: build failed, waiting for other jobs to finish...

## Godot
No Godot project found.

## Summary

- Python build completed
- Rust build completed
- Godot build completed
