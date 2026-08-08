use the_last_signal_server::network::packet::PacketType;
use the_last_signal_server::database::{
    database_manager::DatabaseManager,
    migrations,
};
use log::info;

use the_last_signal_server::network::server::Server;
use the_last_signal_server::utils::logger::logger::ServerLogger;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let _guard = ServerLogger::init();
    let database_url = 
        std::env::var("DATABASE_URL")?;
    let database_path =
        std::env::var("DATABASE_PATH")?;

    let database =
        DatabaseManager::new(&database_path,& database_url)
            .await?;

    database.ping().await?;

    migrations::run(&database.pool())
        .await?;

    info!("Base PostgreSQL prête.");

    let server =
        Server::new(
            "127.0.0.1:5000",
            database,
        )
        .await?;


    server.start().await;

    Ok(())
}
