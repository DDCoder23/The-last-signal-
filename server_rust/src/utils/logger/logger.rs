
use flexi_logger::{
    Cleanup,
    Criterion,
    DeferredNow,
    Duplicate,
    FileSpec,
    Logger,
    Naming,
    Record,
};
use std::io::Write;


use std::path::{PathBuf,Path};
use crate::utils::logger::compressor::LogCompressor;


fn log_format(
    w: &mut dyn Write,
    now: &mut DeferredNow,
    record: &Record,
) -> std::io::Result<()> {
    let file = record
        .file()
        .and_then(|f| Path::new(f).file_name())
        .and_then(|f| f.to_str())
        .unwrap_or("unknown");

    write!(
        w,
        "[{}] [{}] [{}:{}] {}",
        now.format("%Y-%m-%d %H:%M:%S"),
        record.level(),
        file,
        record.line().unwrap_or(0),
        record.args()
    )
}
pub struct ServerLogger;

impl ServerLogger {
    pub fn init() {
        

        let log_dir = PathBuf::from("../logs");

        Logger::try_with_str("trace,sqlx=warn")
            .unwrap()

            .duplicate_to_stdout(Duplicate::All)

            .log_to_file(
                FileSpec::default()
                    .directory(log_dir)
                    .basename("the_last_signal"),
            )
            .format(log_format)

            .rotate(
                Criterion::Size(10_000_000),
                Naming::Numbers,
                Cleanup::KeepLogFiles(10000000000),
            )
            .append()

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
