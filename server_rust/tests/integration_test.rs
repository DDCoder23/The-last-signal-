
use the_last_signal_server::gameplay::tresor::Tresor;
#[test]
fn test_tresor() {
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
                    
