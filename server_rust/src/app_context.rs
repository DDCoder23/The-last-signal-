use crate::database::database_manager::DatabaseManager;
use crate::logger::Logger;

pub struct AppContext {
    pub database: DatabaseManager,
    pub logger: Logger,
}
