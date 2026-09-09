use the_last_signal_server::database::{
    database_manager::DatabaseManager,
    migrations,
};
use log::info;
use the_last_signal_server::network::server::Server;
use the_last_signal_server::gameplay::{objets::Livre,table_de_conversion::convertir_livres};
use the_last_signal_server::utils::logger::logger::ServerLogger;
use std::collections::HashMap;
#[tokio::main]

/*
    Fonction asynchrone exécutée par le runtime Tokio. 
    Point d'entrée principal du serveur.

    Initialise :
    - le logger
    - la base de données
    - les migrations
    - le serveur TCP
*/
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

    info!("Base SQLite prête.");
    ServerLogger::set_database(database.pool().clone());
    let mut inventaire = HashMap::new();
    inventaire.insert("livre enchant niv 1".to_string(), 
                      Livre::new(nom: String::from("livre enchant niv 1"), 
                                 quantite: 1, 
                                 category: String::from("épée") , 
                                 enchantements: Vec::from["Aura de feu I"], 
                                niv: 1,)),
    inventaire.insert("livre enchant niv 1".to_string(), 
                      Livre::new(nom: String::from("livre enchant niv 1"), 
                                 quantite: 1, 
                                 category: String::from("épée") , 
                                 enchantements: Vec::from["Aura de feu I"], 
                                niv: 1,)),
   
    
    let server =
        Server::new(
            "127.0.0.1:5000",
            database,
        )
        .await?;


    server.start().await;
    

    Ok(())
}
