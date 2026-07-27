mod database;
mod network;
mod utils;
use database::{
    database_manager::DatabaseManager,
    migrations,
};
use network::server::Server;
use utils::logger::logger::Logger;
Logger::init();
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    
    let database_url =
        std::env::var("DATABASE_URL")?;

    let database =
        DatabaseManager::new(&database_url)
            .await?;

    database.ping().await?;

    migrations::run(&database.pool())
        .await?;

    println!("Base PostgreSQL prête.");

    let server =
        Server::new(
            "127.0.0.1:5000",
            database,
        )
        .await;

    server.start().await;

    Ok(())
}
