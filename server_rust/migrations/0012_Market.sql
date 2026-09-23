CREATE TABLE IF NOT EXISTS objets_dispo (
    objet_id INTEGER PRIMARY KEY AUTOINCREMENT,

    nom TEXT NOT NULL UNIQUE,

    type TEXT NOT NULL,

    image_path TEXT,

    prix_base INTEGER NOT NULL DEFAULT 0,

    prix_marche INTEGER NOT NULL DEFAULT 0,

    CHECK (type IN (
        'equipment',
        'potion',
        'enchanted_book',
        'consumable',
        'material',
        'armes',
        'basic',
        'muni',
        'mineral'
    )),

    CHECK (prix_base >= 0),
    CHECK (prix_marche >= 0)
);
CREATE TABLE IF NOT EXISTS ordres_achat (
    ordre_id INTEGER PRIMARY KEY AUTOINCREMENT,

    objet_id INTEGER NOT NULL,
    joueur_id INTEGER NOT NULL,

    quantite INTEGER NOT NULL,
    quantite_restante INTEGER NOT NULL,

    prix_unitaire_max INTEGER NOT NULL,

    date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    statut TEXT NOT NULL DEFAULT 'actif',

    FOREIGN KEY (objet_id)
        REFERENCES objets_dispo(objet_id),

    CHECK (quantite > 0),
    CHECK (quantite_restante >= 0),
    CHECK (quantite_restante <= quantite),
    CHECK (prix_unitaire_max >= 0),

    CHECK (statut IN (
        'actif',
        'execute',
        'annule'
    ))
);
CREATE TABLE IF NOT EXISTS ordres_vente (
    ordre_id INTEGER PRIMARY KEY AUTOINCREMENT,

    objet_id INTEGER NOT NULL,
    joueur_id INTEGER NOT NULL,

    quantite INTEGER NOT NULL,
    quantite_restante INTEGER NOT NULL,

    prix_unitaire_min INTEGER NOT NULL,

    date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    statut TEXT NOT NULL DEFAULT 'actif',

    FOREIGN KEY (objet_id)
        REFERENCES objets_dispo(objet_id),

    CHECK (quantite > 0),
    CHECK (quantite_restante >= 0),
    CHECK (quantite_restante <= quantite),
    CHECK (prix_unitaire_min >= 0),

    CHECK (statut IN (
        'actif',
        'execute',
        'annule'
    ))
);
CREATE TABLE IF NOT EXISTS transactions_marche (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    objet_id INTEGER NOT NULL,

    ordre_achat_id INTEGER NOT NULL,
    ordre_vente_id INTEGER NOT NULL,

    acheteur_id INTEGER NOT NULL,
    vendeur_id INTEGER NOT NULL,

    quantite INTEGER NOT NULL,

    prix_unitaire INTEGER NOT NULL,

    montant_total INTEGER NOT NULL,

    date_transaction DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (objet_id)
        REFERENCES objets_dispo(objet_id),

    CHECK (quantite > 0),
    CHECK (prix_unitaire >= 0),
    CHECK (montant_total >= 0)
);
