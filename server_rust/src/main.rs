mod database;
mod network;

use database::{
    database_manager::DatabaseManager,
    migrations,
};
use network::server::Server;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {

    println!("==============================");
    println!("The Last Signal Server");
    println!("==============================");

    // URL PostgreSQL
    let database_url =
        std::env::var("DATABASE_URL")
            .expect("DATABASE_URL non définie.");

    // Connexion
    let database =
        DatabaseManager::new(&database_url)
            .await?;

    // Vérifie la connexion
    database.ping().await?;

    println!("Connexion PostgreSQL établie.");

    // Applique les migrations
    migrations::run(&database.pool).await?;

    println!("Base de données prête.");

    // Démarrage du serveur
    let server = Server::new(
        "127.0.0.1:5000",
        database,
    );

    server.start().await;

    Ok(())
}
