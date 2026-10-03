use the_last_signal_server::database::{
    database_manager::DatabaseManager,
    migrations,
};
use log::info;
use the_last_signal_server::network::server::Server;
use the_last_signal_server::gameplay::objets::Livre;
use the_last_signal_server::gameplay::{
    stuff_manager::Inventaire,
    tresor::Tresor,
};

use the_last_signal_server::utils::logger::logger::ServerLogger;
use std::collections::HashMap;

#[allow(dead_code)]
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let _guard = ServerLogger::init();

    let database_url =
        std::env::var("DATABASE_URL")?;

    let database_path =
        std::env::var("DATABASE_PATH")?;

    let database =
        DatabaseManager::new(
            &database_path,
            &database_url,
        )
        .await?;

    database.ping().await?;

    migrations::run(&database.pool())
        .await?;

    info!("Base SQLite prête.");

    ServerLogger::set_database(
        database.pool().clone()
    );

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

    #[derive(Debug, sqlx::FromRow)]
    struct LivreRapport {
        stuff_id: i64,
        stack_key: String,
        quantity: i64,
        book_level: i64,
        enchantment_name: String,
        enchantment_level: i64,
    }


    #[tokio::test]
    async fn test_tresor() -> Result<(), Box<dyn std::error::Error>> {

        // =====================================================
        // INITIALISATION
        // =====================================================

        let _guard = ServerLogger::init();

        let database_url =
            std::env::var("DATABASE_URL")?;

        let database_path =
            std::env::var("DATABASE_PATH")?;

        let database =
            DatabaseManager::new(
                &database_path,
                &database_url,
            )
            .await?;

        database.ping().await?;

        migrations::run(&database.pool())
            .await?;

        info!("Base SQLite prête.");

        ServerLogger::set_database(
            database.pool().clone()
        );


        // =====================================================
        // CONFIGURATION DU TEST
        // =====================================================

        let account_id: i64 = 1;
        let coefficient: f64 = 1.4;


        // =====================================================
        // TRÉSOR + INVENTAIRE
        // =====================================================

        let mut tresor = Tresor::new();

        let mut inventaire =
            Inventaire::new(
                database.pool().clone(),
                account_id,
            )
            .await?;


        // =====================================================
        // OUVERTURE DES 40 TRÉSORS
        //
        // 10 niveaux
        // × 2 admin
        // × 2 militaire
        //
        // = 40 ouvertures
        // =====================================================

        for niveau in 1..=10 {

            for is_admin in [false, true] {

                for is_militaire in [false, true] {

                    let objets = tresor
                        .ouvrir(
                            database.pool(),
                            account_id,
                            niveau,
                            is_admin,
                            is_militaire,
                            Some(coefficient),
                        )
                        .await?;


                    info!(
                        "Trésor ouvert : \
                         niveau={niveau}, \
                         is_admin={is_admin}, \
                         is_militaire={is_militaire}"
                    );


                    // =========================================
                    // AJOUT DES LIVRES À L'INVENTAIRE
                    // =========================================

                    for (nom_objet, quantite) in objets {

                        if !nom_objet.contains("livre enchant") {
                            continue;
                        }


                        inventaire
                            .ajouter_objet(
                                &nom_objet,
                                u64::from(quantite),
                            )
                            .await?;


                        info!(
                            "✓ Livre ajouté à l'inventaire : \
                             {nom_objet} x{quantite} \
                             (niveau={niveau}, \
                             admin={is_admin}, \
                             militaire={is_militaire})"
                        );
                    }
                }
            }
        }


        // =====================================================
        // FIN DES OUVERTURES
        // =====================================================

        info!(
            "=================================================="
        );

        info!(
            "40 ouvertures terminées."
        );

        info!(
            "Génération du rapport SQLite..."
        );


        // =====================================================
        // RÉCUPÉRATION DES LIVRES DEPUIS SQLITE
        // =====================================================
        //
        // On récupère les vrais livres créés par
        // Inventaire::ajouter_objet().
        //
        // On ne régénère donc aucun livre.
        // =====================================================

        let livres = sqlx::query_as::<_, LivreRapport>(
            r#"
            SELECT
                s.stuff_id,
                s.stack_key,
                s.quantity,
                eb.book_level,
                e.enchantment_name,
                be.enchantment_level

            FROM stuff s

            INNER JOIN enchanted_books eb
                ON eb.stuff_id = s.stuff_id

            INNER JOIN book_enchantments be
                ON be.book_id = eb.book_id

            INNER JOIN enchantments e
                ON e.enchantment_id = be.enchantment_id

            WHERE s.account_id = ?

            ORDER BY
                eb.book_level,
                s.stuff_id,
                e.enchantment_id
            "#,
        )
        .bind(account_id)
        .fetch_all(database.pool())
        .await?;


        // =====================================================
        // REGROUPEMENT DES ENCHANTEMENTS
        // =====================================================

        let mut livres_groupes:
            HashMap<i64, (String, i64, i64, Vec<String>)>
            = HashMap::new();


        for livre in livres {

            let entree =
                livres_groupes
                    .entry(livre.stuff_id)
                    .or_insert_with(|| {
                        (
                            livre.stack_key.clone(),
                            livre.quantity,
                            livre.book_level,
                            Vec::new(),
                        )
                    });


            entree.3.push(
                format!(
                    "{} {}",
                    livre.enchantment_name,
                    livre.enchantment_level
                )
            );
        }


        // =====================================================
        // RAPPORT FINAL
        // =====================================================

        println!();
        println!("============================================================");
        println!("                 RAPPORT FINAL");
        println!("============================================================");
        println!("Compte      : {account_id}");
        println!("Coefficient : {coefficient}");
        println!("Ouvertures  : 40");
        println!("============================================================");
        println!();


        // =====================================================
        // COMPTAGE GLOBAL
        // =====================================================

        let mut total_livres: i64 = 0;

        let mut total_par_niveau:
            HashMap<i64, i64>
            = HashMap::new();


        for (
            _stuff_id,
            (
                _stack_key,
                quantity,
                book_level,
                _enchantements,
            ),
        ) in &livres_groupes {

            total_livres += *quantity;

            *total_par_niveau
                .entry(*book_level)
                .or_insert(0)
                += *quantity;
        }


        println!(
            "TOTAL DE LIVRES : {total_livres}"
        );

        println!();


        // =====================================================
        // RÉPARTITION PAR NIVEAU DE LIVRE
        // =====================================================

        println!(
            "------------------------------------------------------------"
        );

        println!(
            "RÉPARTITION PAR NIVEAU DE LIVRE"
        );

        println!(
            "------------------------------------------------------------"
        );


        for niveau_livre in 1..=6 {

            let total =
                total_par_niveau
                    .get(&niveau_livre)
                    .copied()
                    .unwrap_or(0);

            println!(
                "Livre niveau {niveau_livre} : {total}"
            );
        }


        println!();


        // =====================================================
        // DÉTAIL DE CHAQUE LIVRE
        // =====================================================

        println!(
            "============================================================"
        );

        println!(
            "DÉTAIL DES COMBINAISONS D'ENCHANTEMENTS"
        );

        println!(
            "============================================================"
        );


        for (
            stuff_id,
            (
                stack_key,
                quantity,
                book_level,
                enchantements,
            ),
        ) in &livres_groupes {

            println!(
                "stuff_id={stuff_id}"
            );

            println!(
                "  niveau livre : {book_level}"
            );

            println!(
                "  quantité     : {quantity}"
            );

            println!(
                "  stack_key    : {stack_key}"
            );

            println!(
                "  enchantements: {}",
                enchantements.join(" + ")
            );

            println!();
        }


        // =====================================================
        // FIN
        // =====================================================

        println!(
            "============================================================"
        );

        println!(
            "Benchmark terminé."
        );

        println!(
            "============================================================"
        );


        Ok(())
    }
}