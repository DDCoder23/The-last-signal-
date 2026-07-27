use tracing_subscriber::{fmt, EnvFilter};

pub struct Logger;

impl Logger {
    pub fn init() {
        fmt()
            .with_env_filter(
                EnvFilter::from_default_env()
            )
            .with_target(true)
            .with_thread_ids(true)
            .with_file(true)
            .with_line_number(true)
            .init();
    }
}
