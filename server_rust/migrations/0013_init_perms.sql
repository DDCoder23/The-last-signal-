INSERT INTO roles (role_name, description)
VALUES
    ('joueur', 'Joueur normal'),
    ('modo', 'Modérateur'),
    ('admin', 'Administrateur'),
    ('Dev', 'Développeur'),
    ('SuperDev', 'Développeur avec plus de perms')
  INSERT INTO permissions (permission_name, description)
VALUES
    ('accounts.read', 'Lire les comptes'),
    ('accounts.write', 'Modifier les comptes'),
    ('permissions.read', 'Lire les permissions'),
    ('permissions.write', 'Modifier les permissions'),
    ('roles.read', 'Lire les rôles'),
    ('roles.write', 'Modifier les rôles'),
    ('objets_dispo.read', 'Lire les objets disponibles'),
    ('objets_dispo.write', 'Modifier les objets disponibles');
