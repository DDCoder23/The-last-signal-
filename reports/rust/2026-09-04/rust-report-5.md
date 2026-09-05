# Rust Report

Run : 1525
Branch : main
Commit : 7d3a94b8654d5cdbbeb276285e0fbf2a33e6241c
Date : Fri Sep  4 20:30:35 UTC 2026


## Cargo fmt
`cargo metadata` exited with an error: error: manifest path `server_rust/Cargo.toml` does not exist

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

⚠️ cargo fmt --check failed

## Cargo clippy

## Cargo test
error: manifest path `server_rust/Cargo.toml` does not exist
