INSERT INTO enchantments (enchantment_name) VALUES
    ('Aura de feu'),
    ('Poison'),
    ('Durability'),
    ('Putréfaction'),
    ('Foudre'),
    ('Critique'),
    ('Cryogenisation'),
    ('Précision'),
    ('Rapidity'),
    ('Respiration'),
    ('Vitality'),
    ('Protection'),
    ('Renvoie'),
    ('luck');
INSERT INTO enchantment_types (enchantment_id, equipment_type)
SELECT enchantment_id, 'épée'
FROM enchantments
WHERE enchantment_name IN (
    'Aura de feu',
    'Poison',
    'Durability',
    'Putréfaction',
    'Foudre',
    'Critique',
    'Cryogenisation',
    'Précision'
);
INSERT INTO enchantment_types (enchantment_id, equipment_type)
SELECT enchantment_id, 'armure'
FROM enchantments
WHERE enchantment_name IN (
    'Respiration',
    'Durability',
    'Vitality',
    'Protection',
    'Renvoie'
);
INSERT INTO enchantment_types (enchantment_id, equipment_type)
SELECT enchantment_id, 'shield'
FROM enchantments
WHERE enchantment_name = 'Protection';
INSERT INTO enchantment_types (enchantment_id, equipment_type)
SELECT enchantment_id, 'armes à feu'
FROM enchantments
WHERE enchantment_name IN (
    'Rapidity',
    'Critique'
);
INSERT INTO enchantment_types (enchantment_id, equipment_type)
SELECT enchantment_id, 'pioche'
FROM enchantments
WHERE enchantment_name = 'luck';
INSERT INTO enchantment_levels (
    enchantment_id,
    book_level,
    max_enchantment_level
)
SELECT
    e.enchantment_id,
    niveau.book_level,
    niveau.book_level
FROM enchantments e
CROSS JOIN (
    SELECT 1 AS book_level
    UNION ALL SELECT 2
    UNION ALL SELECT 3
    UNION ALL SELECT 4
    UNION ALL SELECT 5
    UNION ALL SELECT 6
) AS niveau;
