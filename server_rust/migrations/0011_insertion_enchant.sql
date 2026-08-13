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
SELECT enchantment_id, 'pioche'
FROM enchantments
WHERE enchantment_name = 'luck';
