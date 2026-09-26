use the_last_signal_server::database::{
    database_manager::DatabaseManager,
    migrations,
};
use log::info;
use the_last_signal_server::network::server::Server;
use the_last_signal_server::gameplay::objets::Livre;
use the_last_signal_server::gameplay::{
    stuff_manager::Inventaire,
    tresor::Tresor};

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
   
    // ------------------------------------------
    // Ouverture d'un trésor et ajout à l'inventaire (livres uniquement)
    // ------------------------------------------

    
    
    
    let server =
        Server::new(
            "127.0.0.1:5000",
            database,
        )
        .await?;


    server.start().await;
    

    Ok(())
}
#[cfg(test)]
mod tests {
    use super::*;

   #[tokio::test]
    async fn test_tresor() -> Result<(), Box<dyn std::error::Error>> {
        

        let database_url = std::env::var("DATABASE_URL")?;
        let database_path = std::env::var("DATABASE_PATH")?;

        let database =
            DatabaseManager::new(&database_path, &database_url)
                .await?;

        database.ping().await?;
        let account_id: i64 = 1;
    let mut tresor = Tresor::new();
    let mut inventaire = Inventaire::new(database.pool().clone(), account_id).await?;

    let objets = tresor
        .ouvrir(
            database.pool(),
            account_id,
            1,       // niveau du trésor
            true,   // is_admin
            false,   // is_militaire
            Some(1.3),
        )
        .await?;

    info!("Trésor ouvert pour le compte {account_id}:");
    for (nom_objet, quantite) in objets {
        // Filtre : n'ajouter que les livres enchantés
        if nom_objet.contains("livre enchant") {
            inventaire.ajouter_objet(&nom_objet, u64::from(quantite)).await?;
            info!("✓ Livre ajouté à l'inventaire : {nom_objet} x{quantite}");
        }
    
        }
        Ok(())
    }
}
