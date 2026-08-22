INSERT INTO roles (role_name, description)
VALUES
    ('joueur', 'Joueur normal'),
    ('modo', 'Modérateur'),
    ('admin', 'Administrateur'),
    ('Dev', 'Développeur'),
    ('SuperDev', 'Développeur avec plus de perms');
  INSERT INTO permissions (permission_name, description)
VALUES
    ('accounts.read', 'Lire les comptes'),
    ('accounts.write', 'Modifier les comptes'),
    ('accounts.delete', 'delete accounts'),
    ('permissions.read', 'Lire les permissions'),
    ('permissions.write', 'Modifier les permissions'),
    ('roles.read', 'Lire les rôles'),
    ('roles.write', 'Modifier les rôles'),
    ('objets_dispo.read', 'Lire les objets disponibles'),
    ('objets_dispo.write', 'Modifier les objets disponible'),
    ('chat.acces', 'accès au chat'),
    ('chat.moderation', 'moderation du chat'),
    ('log.search', 'recherche dans les logs');
INSERT OR IGNORE INTO role_permissions (
    role_id,
    permission_id
)
SELECT
    r.role_id,
    p.permission_id
FROM roles r
CROSS JOIN permissions p
WHERE r.role_name = 'SuperDev';
INSERT OR IGNORE INTO role_permissions (
    role_id,
    permission_id
)
SELECT
    r.role_id,
    p.permission_id
FROM roles r
CROSS JOIN permissions p
WHERE r.role_name = 'Dev'
  AND p.permission_name NOT IN (
      'accounts.delete',
      'roles.write',
      'log.search'
  );
INSERT OR IGNORE INTO role_permissions (
    role_id,
    permission_id
)
SELECT
    r.role_id,
    p.permission_id
FROM roles r
CROSS JOIN permissions p
WHERE r.role_name = 'joueur'
  AND p.permission_name  IN (
      'chat.acces'
  );
