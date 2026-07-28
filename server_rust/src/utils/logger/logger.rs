use flexi_logger::{
    Cleanup,
    Criterion,
    Duplicate,
    FileSpec,
    Logger,
    Naming,
};

use std::path::PathBuf;
use crate::utils::logger::compressor::LogCompressor;

pub struct ServerLogger;

impl ServerLogger {
    pub fn init() {
        

        let log_dir = PathBuf::from("../logs");

        Logger::try_with_str("info")
            .unwrap()

            .duplicate_to_stdout(Duplicate::All)

            .log_to_file(
                FileSpec::default()
                    .directory("log_dir")
                    .basename("the_last_signal"),
            )

            .rotate(
                Criterion::Size(10_000_000),
                Naming::Numbers,
                Cleanup::KeepLogFiles(11),
            )

            .start()
            .unwrap();

        // Premier nettoyage au démarrage
        Self::compress();
    }

    pub fn compress() {
        if let Err(e) =
            LogCompressor::compress_old_logs(
                "logs",
                10,
            )
        {
            eprintln!(
                "Compression impossible : {}",
                e
            );
        }
    }
}
