use rand::Rng;
use sqlx::SqlitePool;
use std::collections::HashMap;
use crate::gameplay::objets::{Livre, Objet};

#[derive(Debug, Clone)]
pub struct StatsConversion {
    pub livres_utilises: u32,
    pub livres_crees: u32,
}

impl Default for StatsConversion {
    fn default() -> Self {
        StatsConversion {
            livres_utilises: 0,
            livres_crees: 0,
        }
    }
}

pub struct InventaireManager;

impl InventaireManager {
    /// Retourne la quantité et la catégorie d'un livre dans l'inventaire du joueur
    pub fn qtes(
        nom: &str,
        stuff: &HashMap<String, Objet>,
    ) -> (u32, Option<String>) {
        if let Some(livre) = stuff.get(nom) {
            (livre.objet.quantite, livre.category.clone())
        } else {
            (0, None)
        }
    }
}

pub struct TableDeConversion;

impl TableDeConversion {
    /// Fusionne jusqu'à 6 listes d'enchantements en :
    /// - Supprimant les enchantements de niveau inférieur si un niveau supérieur existe.
    /// - Limitant le résultat à `niv` enchantements.
    /// - Conservant les enchantements de niveau supérieur.
    pub fn fusionner_enchantements(niv: usize, listes: &[Vec<String>]) -> Vec<String> {
        let mut enchantements_max: HashMap<String, u32> = HashMap::new();

        // Traiter chaque liste
        for liste in listes {
            for enchant in liste {
                let nom = Self::get_nom(enchant);
                let niveau = Self::get_niveau(enchant);

                // Si l'enchantement n'est pas encore présent ou si le nouveau niveau est supérieur
                if !enchantements_max.contains_key(&nom) || niveau > enchantements_max[&nom] {
                    enchantements_max.insert(nom, niveau);
                }
            }
        }

        // Reconstruire la liste des enchantements avec leur niveau maximal
        let mut liste_fusionnee: Vec<String> = enchantements_max
            .iter()
            .map(|(nom, niveau)| format!("{} {}", nom, Self::niveau_to_romain(*niveau)))
            .collect();

        // Trier par niveau décroissant
        liste_fusionnee.sort_by(|a, b| {
            let niv_b = Self::get_niveau(b);
            let niv_a = Self::get_niveau(a);
            niv_b.cmp(&niv_a)
        });

        // Limiter à `niv` enchantements
        if liste_fusionnee.len() > niv {
            liste_fusionnee.truncate(niv);
        }

        liste_fusionnee
    }

    /// Extrait le niveau d'un enchantement (ex: "Poison VI" -> 6)
    fn get_niveau(enchant: &str) -> u32 {
        let parts: Vec<&str> = enchant.split_whitespace().collect();
        if parts.is_empty() {
            return 0;
        }

        let niveau_str = parts[parts.len() - 1];
        match niveau_str {
            "I" => 1,
            "II" => 2,
            "III" => 3,
            "IV" => 4,
            "V" => 5,
            "VI" => 6,
            _ => 0,
        }
    }

    /// Extrait le nom de l'enchantement (ex: "Poison VI" -> "Poison")
    fn get_nom(enchant: &str) -> String {
        let parts: Vec<&str> = enchant.split_whitespace().collect();
        if parts.len() > 1 {
            parts[..parts.len() - 1].join(" ")
        } else {
            enchant.to_string()
        }
    }

    /// Convertit un niveau en chiffres romains
    fn niveau_to_romain(n: u32) -> &'static str {
        match n {
            1 => "I",
            2 => "II",
            3 => "III",
            4 => "IV",
            5 => "V",
            6 => "VI",
            _ => "I",
        }
    }

    /// Retourne l'enchantement de niveau supérieur
    pub fn obtenir_enchantement_superieur(enchantement: &str) -> String {
        let parts: Vec<&str> = enchantement.split_whitespace().collect();
        if parts.len() < 2 {
            return enchantement.to_string();
        }

        let nom = parts[..parts.len() - 1].join(" ");
        let niveau_str = parts[parts.len() - 1];

        let niveau_actuel = match niveau_str {
            "I" => 1,
            "II" => 2,
            "III" => 3,
            "IV" => 4,
            "V" => 5,
            "VI" => 6,
            _ => return enchantement.to_string(),
        };

        if niveau_actuel < 6 {
            let niveau_superieur = niveau_actuel + 1;
            let niveau_romain = Self::niveau_to_romain(niveau_superieur);
            format!("{} {}", nom, niveau_romain)
        } else {
            enchantement.to_string()
        }
    }

    /// Recherche des livres de même catégorie
    fn chercher_livre(
        nb: usize,
        dict_livre: &[String],
        lv1: &Livre,
        clef1: &str,
        stuff: &HashMap<String, Objet>,
    ) -> Vec<String> {
        let mut lvs = Vec::new();

        for i in 0..nb {
            for cle in dict_livre.iter().skip(1) {
                if let Some(lv_temp) = stuff.get(cle) {
                    if lv_temp.category == lv1.category
                        && lv_temp.enchantements.is_some()
                        && !lv_temp.enchantements.as_ref().unwrap().is_empty()
                    {
                        lvs.push(cle.clone());
                        break;
                    }
                }
            }

            // Si pas de livre trouvé avec la même catégorie
            if lvs.len() <= i {
                lvs.push(clef1.to_string());
            }
        }

        lvs.into_iter().take(nb).collect()
    }

    /// Convertit des livres de niveau `niv` à `niv + 1`
    pub async fn convertir_livres(
        stuff: &mut HashMap<String, Objet>,
        niv: u32,
        nb: u32,
    ) -> Result<StatsConversion, String> {
        let mut stats = StatsConversion::default();

        if niv >= 1 && niv < 6 {
            match niv {
                1 => Self::l1_l2(stuff, nb as usize, &mut stats)?,
                2 => Self::l2_l3(stuff, nb as usize, &mut stats)?,
                3 => Self::l3_l4(stuff, nb as usize, &mut stats)?,
                4 => Self::l4_l5(stuff, nb as usize, &mut stats)?,
                5 => Self::l5_l6(stuff, nb as usize, &mut stats)?,
                _ => {}
            }
        }

        Ok(stats)
    }

    fn l1_l2(
        stuff: &mut HashMap<String, Objet>,
        nb: usize,
        stats: &mut StatsConversion,
    ) -> Result<(), String> {
        let mut rng = rand::rng();

        for _ in 0..nb {
            let livres_niv1: Vec<String> = stuff
                .iter()
                .filter(|(_, obj)| obj.niv == 1 && obj.objet.quantite > 0)
                .map(|(cle, _)| cle.clone())
                .collect();

            if livres_niv1.is_empty() {
                continue;
            }

            let mut livres_copy = livres_niv1.clone();
            livres_copy.shuffle(&mut rng);

            let clef1 = &livres_copy[0];
            let lv1 = stuff.get(clef1).ok_or("Livre not found")?.clone();

            let clefs_lv = Self::chercher_livre(1, &livres_niv1, &lv1, clef1, stuff);
            let clef2 = clefs_lv.get(0).ok_or("No second book found")?;

            let lv2 = stuff.get(clef2).ok_or("Livre not found")?.clone();

            if lv1.category == lv2.category
                && lv1.enchantements.is_some()
                && !lv1.enchantements.as_ref().unwrap().is_empty()
                && lv2.enchantements.is_some()
                && !lv2.enchantements.as_ref().unwrap().is_empty()
            {
                let enchantements = Self::fusionner_enchantements(
                    2,
                    &[
                        lv1.enchantements.as_ref().unwrap().clone(),
                        lv2.enchantements.as_ref().unwrap().clone(),
                    ],
                );

                let mut new_livre = Livre::new(
                    "livre enchant niv 2",
                    None,
                    1,
                    lv1.category.clone().as_deref(),
                    Some(enchantements),
                    2,
                );

                // Reduce quantities
                if let Some(livre1) = stuff.get_mut(clef1) {
                    livre1.retirer(1);
                }
                if let Some(livre2) = stuff.get_mut(clef2) {
                    livre2.retirer(1);
                }

                // Add or increment new book
                stuff
                    .entry("livre enchant niv 2".to_string())
                    .and_modify(|l| l.ajouter(1))
                    .or_insert(new_livre);

                stats.livres_utilises += 2;
                stats.livres_crees += 1;
            }
        }

        Ok(())
    }

    fn l2_l3(
        stuff: &mut HashMap<String, Objet>,
        nb: usize,
        stats: &mut StatsConversion,
    ) -> Result<(), String> {
        let mut rng = rand::rng();

        for _ in 0..nb {
            let livres_niv2: Vec<String> = stuff
                .iter()
                .filter(|(_, obj)| obj.niv == 2 && obj.objet.quantite > 0)
                .map(|(cle, _)| cle.clone())
                .collect();

            if livres_niv2.is_empty() {
                continue;
            }

            let mut livres_copy = livres_niv2.clone();
            livres_copy.shuffle(&mut rng);

            let clef1 = &livres_copy[0];
            let lv1 = stuff.get(clef1).ok_or("Livre not found")?.clone();

            let clefs_lv = Self::chercher_livre(2, &livres_niv2, &lv1, clef1, stuff);
            let clef2 = clefs_lv.get(0).ok_or("No second book found")?;
            let clef3 = clefs_lv.get(1).ok_or("No third book found")?;

            let lv2 = stuff.get(clef2).ok_or("Livre not found")?.clone();
            let lv3 = stuff.get(clef3).ok_or("Livre not found")?.clone();

            if lv1.category == lv2.category
                && lv2.category == lv3.category
                && lv1.enchantements.is_some()
                && !lv1.enchantements.as_ref().unwrap().is_empty()
                && lv2.enchantements.is_some()
                && !lv2.enchantements.as_ref().unwrap().is_empty()
                && lv3.enchantements.is_some()
                && !lv3.enchantements.as_ref().unwrap().is_empty()
            {
                let enchantements = Self::fusionner_enchantements(
                    3,
                    &[
                        lv1.enchantements.as_ref().unwrap().clone(),
                        lv2.enchantements.as_ref().unwrap().clone(),
                        lv3.enchantements.as_ref().unwrap().clone(),
                    ],
                );

                let new_livre = Livre::new(
                    "livre enchant niv 3",
                    None,
                    1,
                    lv1.category.clone().as_deref(),
                    Some(enchantements),
                    3,
                );

                // Reduce quantities
                if let Some(livre) = stuff.get_mut(clef1) {
                    livre.retirer(1);
                }
                if let Some(livre) = stuff.get_mut(clef2) {
                    livre.retirer(1);
                }
                if let Some(livre) = stuff.get_mut(clef3) {
                    livre.retirer(1);
                }

                // Add or increment new book
                stuff
                    .entry("livre enchant niv 3".to_string())
                    .and_modify(|l| l.ajouter(1))
                    .or_insert(new_livre);

                stats.livres_utilises += 3;
                stats.livres_crees += 1;
            }
        }

        Ok(())
    }

    fn l3_l4(
        stuff: &mut HashMap<String, Objet>,
        nb: usize,
        stats: &mut StatsConversion,
    ) -> Result<(), String> {
        let mut rng = rand::rng();
        for _ in 0..nb {
            let livres_niv3: Vec<String> = stuff
                .iter()
                .filter(|(_, obj)| obj.niv == 3 && obj.objet.quantite > 0)
                .map(|(cle, _)| cle.clone())
                .collect();

            if livres_niv3.is_empty() {
                continue;
            }

            let mut livres_copy = livres_niv3.clone();
            livres_copy.shuffle(&mut rng);

            let clef1 = &livres_copy[0];
            let lv1 = stuff.get(clef1).ok_or("Livre not found")?.clone();

            let clefs_lv = Self::chercher_livre(3, &livres_niv3, &lv1, clef1, stuff);
            let clef2 = clefs_lv.get(0).ok_or("No second book found")?;
            let clef3 = clefs_lv.get(1).ok_or("No third book found")?;
            let clef4 = clefs_lv.get(2).ok_or("No fourth book found")?;

            let lv2 = stuff.get(clef2).ok_or("Livre not found")?.clone();
            let lv3 = stuff.get(clef3).ok_or("Livre not found")?.clone();
            let lv4 = stuff.get(clef4).ok_or("Livre not found")?.clone();

            if lv1.category == lv2.category
                && lv2.category == lv3.category
                && lv3.category == lv4.category
                && lv1.enchantements.is_some()
                && !lv1.enchantements.as_ref().unwrap().is_empty()
                && lv2.enchantements.is_some()
                && !lv2.enchantements.as_ref().unwrap().is_empty()
                && lv3.enchantements.is_some()
                && !lv3.enchantements.as_ref().unwrap().is_empty()
                && lv4.enchantements.is_some()
                && !lv4.enchantements.as_ref().unwrap().is_empty()
            {
                let enchantements = Self::fusionner_enchantements(
                    4,
                    &[
                        lv1.enchantements.as_ref().unwrap().clone(),
                        lv2.enchantements.as_ref().unwrap().clone(),
                        lv3.enchantements.as_ref().unwrap().clone(),
                        lv4.enchantements.as_ref().unwrap().clone(),
                    ],
                );

                let new_livre = Livre::new(
                    "livre enchant niv 4",
                    None,
                    1,
                    lv1.category.clone().as_deref(),
                    Some(enchantements),
                    4,
                );

                // Reduce quantities
                for clef in &[clef1, clef2, clef3, clef4] {
                    if let Some(livre) = stuff.get_mut(*clef) {
                        livre.retirer(1);
                    }
                }

                // Add or increment new book
                stuff
                    .entry("livre enchant niv 4".to_string())
                    .and_modify(|l| l.ajouter(1))
                    .or_insert(new_livre);

                stats.livres_utilises += 4;
                stats.livres_crees += 1;
            }
        }

        Ok(())
    }

    fn l4_l5(
        stuff: &mut HashMap<String, Objet>,
        nb: usize,
        stats: &mut StatsConversion,
    ) -> Result<(), String> {
        let mut rng = rand::rng();
        for _ in 0..nb {
            let livres_niv4: Vec<String> = stuff
                .iter()
                .filter(|(_, obj)| obj.niv == 4 && obj.objet.quantite > 0)
                .map(|(cle, _)| cle.clone())
                .collect();

            if livres_niv4.is_empty() {
                continue;
            }

            let mut livres_copy = livres_niv4.clone();
            livres_copy.shuffle(&mut rng);

            let clef1 = &livres_copy[0];
            let lv1 = stuff.get(clef1).ok_or("Livre not found")?.clone();

            let clefs_lv = Self::chercher_livre(4, &livres_niv4, &lv1, clef1, stuff);
            let clef2 = clefs_lv.get(0).ok_or("No second book found")?;
            let clef3 = clefs_lv.get(1).ok_or("No third book found")?;
            let clef4 = clefs_lv.get(2).ok_or("No fourth book found")?;
            let clef5 = clefs_lv.get(3).ok_or("No fifth book found")?;

            let lv2 = stuff.get(clef2).ok_or("Livre not found")?.clone();
            let lv3 = stuff.get(clef3).ok_or("Livre not found")?.clone();
            let lv4 = stuff.get(clef4).ok_or("Livre not found")?.clone();
            let lv5 = stuff.get(clef5).ok_or("Livre not found")?.clone();

            if lv1.category == lv2.category
                && lv2.category == lv3.category
                && lv3.category == lv4.category
                && lv4.category == lv5.category
                && lv1.enchantements.is_some()
                && !lv1.enchantements.as_ref().unwrap().is_empty()
                && lv2.enchantements.is_some()
                && !lv2.enchantements.as_ref().unwrap().is_empty()
                && lv3.enchantements.is_some()
                && !lv3.enchantements.as_ref().unwrap().is_empty()
                && lv4.enchantements.is_some()
                && !lv4.enchantements.as_ref().unwrap().is_empty()
                && lv5.enchantements.is_some()
                && !lv5.enchantements.as_ref().unwrap().is_empty()
            {
                let enchantements = Self::fusionner_enchantements(
                    5,
                    &[
                        lv1.enchantements.as_ref().unwrap().clone(),
                        lv2.enchantements.as_ref().unwrap().clone(),
                        lv3.enchantements.as_ref().unwrap().clone(),
                        lv4.enchantements.as_ref().unwrap().clone(),
                        lv5.enchantements.as_ref().unwrap().clone(),
                    ],
                );

                let new_livre = Livre::new(
                    "livre enchant niv 5",
                    None,
                    1,
                    lv1.category.clone().as_deref(),
                    Some(enchantements),
                    5,
                );

                // Reduce quantities
                for clef in &[clef1, clef2, clef3, clef4, clef5] {
                    if let Some(livre) = stuff.get_mut(*clef) {
                        livre.retirer(1);
                    }
                }

                // Add or increment new book
                stuff
                    .entry("livre enchant niv 5".to_string())
                    .and_modify(|l| l.ajouter(1))
                    .or_insert(new_livre);

                stats.livres_utilises += 5;
                stats.livres_crees += 1;
            }
        }

        Ok(())
    }

    fn l5_l6(
        stuff: &mut HashMap<String, Objet>,
        nb: usize,
        stats: &mut StatsConversion,
    ) -> Result<(), String> {
        let mut rng = rand::rng();

        for _ in 0..nb {
            let livres_niv5: Vec<String> = stuff
                .iter()
                .filter(|(_, obj)| obj.niv == 5 && obj.objet.quantite > 0)
                .map(|(cle, _)| cle.clone())
                .collect();

            if livres_niv5.is_empty() {
                continue;
            }

            let mut livres_copy = livres_niv5.clone();
            livres_copy.shuffle(&mut rng);

            let clef1 = &livres_copy[0];
            let lv1 = stuff.get(clef1).ok_or("Livre not found")?.clone();

            let clefs_lv = Self::chercher_livre(5, &livres_niv5, &lv1, clef1, stuff);
            let clef2 = clefs_lv.get(0).ok_or("No second book found")?;
            let clef3 = clefs_lv.get(1).ok_or("No third book found")?;
            let clef4 = clefs_lv.get(2).ok_or("No fourth book found")?;
            let clef5 = clefs_lv.get(3).ok_or("No fifth book found")?;
            let clef6 = clefs_lv.get(4).ok_or("No sixth book found")?;

            let lv2 = stuff.get(clef2).ok_or("Livre not found")?.clone();
            let lv3 = stuff.get(clef3).ok_or("Livre not found")?.clone();
            let lv4 = stuff.get(clef4).ok_or("Livre not found")?.clone();
            let lv5 = stuff.get(clef5).ok_or("Livre not found")?.clone();
            let lv6 = stuff.get(clef6).ok_or("Livre not found")?.clone();

            if lv1.category == lv2.category
                && lv2.category == lv3.category
                && lv3.category == lv4.category
                && lv4.category == lv5.category
                && lv5.category == lv6.category
                && lv1.enchantements.is_some()
                && !lv1.enchantements.as_ref().unwrap().is_empty()
                && lv2.enchantements.is_some()
                && !lv2.enchantements.as_ref().unwrap().is_empty()
                && lv3.enchantements.is_some()
                && !lv3.enchantements.as_ref().unwrap().is_empty()
                && lv4.enchantements.is_some()
                && !lv4.enchantements.as_ref().unwrap().is_empty()
                && lv5.enchantements.is_some()
                && !lv5.enchantements.as_ref().unwrap().is_empty()
                && lv6.enchantements.is_some()
                && !lv6.enchantements.as_ref().unwrap().is_empty()
            {
                let enchantements = Self::fusionner_enchantements(
                    6,
                    &[
                        lv1.enchantements.as_ref().unwrap().clone(),
                        lv2.enchantements.as_ref().unwrap().clone(),
                        lv3.enchantements.as_ref().unwrap().clone(),
                        lv4.enchantements.as_ref().unwrap().clone(),
                        lv5.enchantements.as_ref().unwrap().clone(),
                        lv6.enchantements.as_ref().unwrap().clone(),
                    ],
                );

                let new_livre = Livre::new(
                    "livre enchant niv 6",
                    None,
                    1,
                    lv1.category.clone().as_deref(),
                    Some(enchantements),
                    6,
                );

                // Reduce quantities
                for clef in &[clef1, clef2, clef3, clef4, clef5, clef6] {
                    if let Some(livre) = stuff.get_mut(*clef) {
                        livre.retirer(1);
                    }
                }

                // Add or increment new book
                stuff
                    .entry("livre enchant niv 6".to_string())
                    .and_modify(|l| l.ajouter(1))
                    .or_insert(new_livre);

                stats.livres_utilises += 6;
                stats.livres_crees += 1;
            }
        }

        Ok(())
    }
}

            
