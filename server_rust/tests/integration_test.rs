
use the_last_signal_server::network::packet::PacketType;
use the_last_signal_server::database::{
    database_manager::DatabaseManager,
    migrations,
};
use log::{debug,info};

use the_last_signal_server::utils::logger::logger::ServerLogger;

use the_last_signal_server::gameplay::tresor::Tresor;
#[test]
async fn test_tresor() {
    let _guard = ServerLogger::init();
    
    
    let database_url = 
        std::env::var("DATABASE_Test_URL")?;
    let database_path =
        std::env::var("DATABASE_Test_PATH")?;

    let database =
        DatabaseManager::new(&database_path,& database_url)
            .await?;

    database.ping().await?;

    migrations::run(&database.pool())
        .await?;

    info!("Base SQLite prête.");
    ServerLogger::set_database(database.pool().clone());
    let mut tresor = Tresor::new();
    for i in 1..=10000{
    for i in 1..=7 {
        

    let message_normal = tresor
        .ouvrir(
                  &database.pool().clone(),
            1,
            i, 
            false)
        .await?;
    debug!("Trésor {} normal : {:?}", i, message_normal);

    let message_admin = tresor
        .ouvrir(
                &database.pool().clone(),
                1,
               i,
               true)
        .await?;
    debug!("Trésor {} admin : {:?}", i, message_admin);
    }
    }
}
                    
