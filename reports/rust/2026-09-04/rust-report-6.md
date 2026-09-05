# Rust Report

Run : 1526
Branch : main
Commit : 4ef726700dd64241f5c8afbb4f5ee58a2729ac19
Date : Fri Sep  4 21:28:58 UTC 2026


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
