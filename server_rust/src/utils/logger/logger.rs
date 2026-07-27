use tracing_subscriber::{
    fmt,
    layer::SubscriberExt,
    util::SubscriberInitExt,
    EnvFilter,
};
use crate::logger::compressor::LogCompressor;


use crate::logger::file::create_file_appender;

pub struct Logger;

impl Logger {
    pub fn init() -> tracing_appender::non_blocking::WorkerGuard {

        let (file_writer, guard) =
            create_file_appender();

        tracing_subscriber::registry()

            .with(
                EnvFilter::from_default_env()
                    .add_directive(
                        tracing::Level::INFO.into()
                    ),
            )

            .with(
                fmt::layer()
                    .with_writer(std::io::stdout),
            )

            .with(
                fmt::layer()
                    .with_writer(file_writer)
                    .with_ansi(false),
            )

            .init();

        guard
    }
}
