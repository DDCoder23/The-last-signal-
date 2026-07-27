use tracing_appender::{
    non_blocking::WorkerGuard,
    rolling,
};

pub fn create_file_appender() -> (
    tracing_appender::non_blocking::NonBlocking,
    WorkerGuard,
) {
    let file_appender =
        rolling::daily("logs", "server.log");

    tracing_appender::non_blocking(file_appender)
}
