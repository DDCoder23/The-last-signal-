use the_last_signal_server::network::packet::PacketType;
use the_last_signal_server::gameplay::tresor::Tresor;
use the_last_signal_server::utils::logger::logger::ServerLogger;
use log::debug;
#[test]
fn test_packet_login() {
    assert_eq!(PacketType::Login as u8, 2);
}
use serde_json::{Map, Value};

use the_last_signal_server::utils::save::{
    manager::SaveManager,
    errors::SaveError,
};

#[test]
fn save_load_delete() {

    let manager = SaveManager::new();

    let profile = "integration_test";
    let slot = 1;
    let password = "password123";

    let mut data = Map::new();

    data.insert(
        "name".into(),
        Value::String("Morgan".into()),
    );

    data.insert(
        "level".into(),
        Value::from(42),
    );

    // Sauvegarde
    manager
        .save(
            profile,
            slot,
            &data,
            password,
        )
        .unwrap();

    // Vérification
    manager
        .verify(
            profile,
            slot,
        )
        .unwrap();

    // Chargement
    let loaded =
        manager
            .load(
                profile,
                slot,
                password,
            )
            .unwrap();

    assert_eq!(
        loaded,
        data,
    );

    // Suppression
    manager
        .delete(
            profile,
            slot,
        )
        .unwrap();
}
#[test]
fn wrong_password() {

    let manager = SaveManager::new();

    let mut data = Map::new();

    data.insert(
        "hp".into(),
        Value::from(100),
    );

    manager
        .save(
            "password_test",
            1,
            &data,
            "secret",
        )
        .unwrap();

    let result =
        manager.load(
            "password_test",
            1,
            "bad_password",
        );

    assert!(matches!(
        result,
        Err(SaveError::InvalidPassword)
    ));

    manager
        .delete(
            "password_test",
            1,
        )
        .unwrap();
}
#[test]
fn invalid_slot() {

    let manager = SaveManager::new();

    let data = Map::new();

    assert!(matches!(
        manager.save(
            "test",
            4,
            &data,
            "pwd",
        ),
        Err(SaveError::InvalidSlot)
    ));
}
#[test]
fn save_not_found() {

    let manager = SaveManager::new();

    assert!(matches!(
        manager.load(
            "profil_inexistant",
            1,
            "pwd",
        ),
        Err(SaveError::SaveNotFound)
    ));
}
#[test]
fn test_tresor(){
    let _guard = ServerLogger::init();
    let tresor = Tresor::new();
    let message = tresor.ouvrir(1, true);
    
    debug!(message);
}
