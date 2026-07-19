# Rust CI Report

Date: Sun Jul 19 23:32:27 UTC 2026
Branch: main
Commit: 50d74c2194faac1117e397984ea98aeb6dfef2cc

## Cargo fmt
`cargo metadata` exited with an error: [1m[91merror[0m: could not find `Cargo.toml` in `/home/runner/work/The-last-signal-/The-last-signal-` or any parent directory

This utility formats all bin and lib files of the current crate using rustfmt.

Usage: cargo fmt [OPTIONS] [-- <rustfmt_options>...]

Arguments:
  [rustfmt_options]...  Options passed to rustfmt

Options:
  -q, --quiet
          No output printed to stdout
  -v, --verbose
          Use verbose output
      --version
          Print rustfmt version and exit
  -p, --package <package>...
          Specify package to format
      --manifest-path <manifest-path>
          Specify path to Cargo.toml
      --message-format <message-format>
          Specify message-format: short|json|human
      --all
          Format all packages, and also their local path-based dependencies
      --check
          Run rustfmt in check mode
  -h, --help
          Print help

Cargo fmt: 1

## Cargo clippy
[1m[91merror[0m: could not find `Cargo.toml` in `/home/runner/work/The-last-signal-/The-last-signal-` or any parent directory

Clippy warnings: 0

## Cargo test
[1m[91merror[0m: could not find `Cargo.toml` in `/home/runner/work/The-last-signal-/The-last-signal-` or any parent directory

Passed tests: 0
Failed tests: 0

## Cargo build
[1m[91merror[0m: could not find `Cargo.toml` in `/home/runner/work/The-last-signal-/The-last-signal-` or any parent directory

Coverage: 0

## Cargo audit
[0m[0m[1m[32m    Fetching[0m advisory database from `https://github.com/RustSec/advisory-db.git`
[0m[0m[1m[32m      Loaded[0m 1166 security advisories (from /home/runner/.cargo/advisory-db)
[0m[0m[1m[32m    Updating[0m crates.io index
[0m[0m[1m[31merror:[0m not found: Couldn't load Cargo.lock
Caused by:
  -> I/O operation failed: I/O operation failed: entity not found
  -> I/O operation failed: entity not found

Cargo audit: 0
