use flexi_logger::{
    Cleanup,
    Criterion,
    DeferredNow,
    Duplicate,
    FileSpec,
    LogWriter,
    Logger,
    Naming,
    Record,
};

use sqlx::SqlitePool;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;
use tokio::sync::mpsc;

use crate::utils::logger::compressor::LogCompressor;

static LOG_SENDER: OnceLock<mpsc::UnboundedSender<DbLog>> = OnceLock::new();

#[derive(Debug)]
struct DbLog {
    level: String,
    module: String,
    message: String,
}

pub struct ServerLogger;

struct DatabaseWriter;

impl LogWriter for DatabaseWriter {
    fn write(
        &self,
        _now: &mut DeferredNow,
        record: &Record,
    ) -> anyhow::Result<()> {
        if let Some(sender) = LOG_SENDER.get() {
            let log = DbLog {
                level: record.level().to_string(),
                module: record.target().to_string(),
                message: format!("{}", record.args()),
            };

            let _ = sender.send(log);
        }

        Ok(())
    }

    fn flush(&self) -> anyhow::Result<()> {
        Ok(())
    }
}

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
            .add_writer("database", Box::new(DatabaseWriter))
            .rotate(
                Criterion::Size(10_000_000),
                Naming::Numbers,
                Cleanup::KeepLogFiles(10),
            )
            .append()
            .start()
            .unwrap();

        Self::compress();
    }

    pub fn set_database(pool: SqlitePool) {
        let (tx, mut rx) = mpsc::unbounded_channel();

        let _ = LOG_SENDER.set(tx);

        tokio::spawn(async move {
            while let Some(log) = rx.recv().await {
                let result = sqlx::query(
                    r#"
                    INSERT INTO logs (
                        level,
                        module,
                        message
                    )
                    VALUES (?, ?, ?)
                    "#,
                )
                .bind(&log.level)
                .bind(&log.module)
                .bind(&log.message)
                .execute(&pool)
                .await;

                if let Err(error) = result {
                    eprintln!(
                        "Impossible d'enregistrer le log en DB : {}",
                        error
                    );
                }
            }
        });
    }

    pub fn compress() {
        if let Err(e) =
            LogCompressor::compress_old_logs("logs", 10)
        {
            eprintln!(
                "Compression impossible : {}",
                e
            );
        }
    }
        }
