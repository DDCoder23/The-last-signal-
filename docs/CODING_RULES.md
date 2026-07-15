[🏠 Documentation](README.md)

# 💻 Règles de développement (Coding Rules)

> **Projet :** The Last Signal Online

---

## 📋 Informations

| Propriété | Valeur |
|-----------|--------|
| **Document** | Règles de développement |
| **Code** | DOC-010 |
| **Version** | 1.0.0 |
| **Statut** | 🟢 Actif |
| **Dernière mise à jour** | 15 juillet 2026 |

---

# 📖 Table des matières

1. Objectif
2. Technologies utilisées
3. Organisation du projet
4. Structure des dossiers
5. Conventions de nommage
6. Style de code Python
7. Style de code Rust
8. Gestion des erreurs
9. Documentation du code
10. Gestion Git
11. Workflow GitHub
12. Pull Requests
13. Tests
14. Sécurité
15. Optimisation
16. Bonnes pratiques
17. Checklist avant publication

---

# 1. Objectif

Ce document définit les règles de développement de **The Last Signal Online**.

Son objectif est de garantir :

- une base de code homogène ;
- une maintenance facilitée ;
- une meilleure collaboration entre les membres de l'équipe ;
- une meilleure qualité du projet.

Ces règles s'appliquent à tous les contributeurs.

---

# 2. Technologies utilisées

| Technologie | Utilisation |
|--------------|-------------|
| Python | Client |
| Rust | Serveur |
| PostgreSQL | Base de données |
| Redis | Cache |
| WebSocket | Réseau |
| Docker | Déploiement |
| Git | Gestion de version |
| GitHub Actions | Intégration continue |
| Markdown | Documentation |

---

# 3. Organisation du projet

Le projet est divisé en modules indépendants.

Chaque module doit avoir une responsabilité unique.

Exemples :

- Réseau
- Joueur
- Inventaire
- Combat
- Monde
- IA
- Interface

---

# 4. Structure des dossiers

Chaque dossier doit avoir une utilité clairement définie.

Les fichiers doivent être rangés dans le dossier correspondant à leur fonctionnalité.

Éviter les fichiers contenant plusieurs systèmes différents.

---

# 5. Conventions de nommage

## Fichiers

Utiliser le snake_case.

Exemples :

```
player.py
inventory.py
network_client.py
```

---

## Classes

Utiliser le PascalCase.

Exemples :

```python
Player
Inventory
GameServer
Weapon
```

---

## Fonctions

Utiliser le snake_case.

```python
create_player()
save_inventory()
connect_server()
```

---

## Variables

Utiliser des noms explicites.

✔️

```python
player_health
current_weapon
inventory_size
```

❌

```python
a
tmp
x
test
```

---

## Constantes

Utiliser uniquement des MAJUSCULES.

```python
MAX_LEVEL
DEFAULT_SPEED
SERVER_PORT
```

---

# 6. Style Python

Le code Python doit respecter :

- PEP 8
- Annotations de types
- Fonctions courtes
- Variables explicites
- Peu de variables globales

Toutes les fonctions publiques doivent être documentées.

---

# 7. Style Rust

Le code Rust doit respecter :

- cargo fmt
- cargo clippy
- gestion correcte des erreurs
- documentation des fonctions publiques

---

# 8. Gestion des erreurs

Les erreurs ne doivent jamais être ignorées.

Toujours :

- afficher un message clair ;
- enregistrer l'erreur dans les logs ;
- éviter les crashs inutiles.

---

# 9. Documentation du code

Chaque fonction complexe doit contenir une documentation.

Les commentaires doivent expliquer **pourquoi** le code existe et non **ce qu'il fait**.

Éviter les commentaires inutiles.

---

# 10. Gestion Git

Ne jamais développer directement sur la branche `main`.

Chaque fonctionnalité possède sa propre branche.

Exemples :

```
feature/login
feature/inventory
feature/chat
feature/world
```

Pour les corrections :

```
fix/login
fix/database
```

Pour la documentation :

```
docs/gdd
docs/readme
```

---

# 11. Workflow GitHub

Le workflow est le suivant :

```
Issue

↓

Branche

↓

Développement

↓

Tests

↓

Pull Request

↓

Revue

↓

Fusion dans main
```

Aucune fonctionnalité importante ne doit être fusionnée sans revue de code.

---

# 12. Pull Requests

Chaque Pull Request doit :

- avoir un titre clair ;
- expliquer les modifications ;
- référencer une Issue si nécessaire ;
- être relue avant fusion.

---

# 13. Tests

Avant chaque fusion :

- le projet compile ;
- les tests passent ;
- aucun avertissement critique ;
- aucune erreur connue.

Les nouvelles fonctionnalités doivent être accompagnées de tests lorsque cela est possible.

---

# 14. Sécurité

Il est interdit de :

- publier des mots de passe ;
- publier des clés API ;
- publier des tokens GitHub ;
- désactiver volontairement une vérification de sécurité.

Les informations sensibles doivent être stockées dans des variables d'environnement.

---

# 15. Optimisation

Le code doit être :

- lisible ;
- maintenable ;
- performant.

Éviter l'optimisation prématurée.

Optimiser uniquement lorsqu'un problème de performance est identifié.

---

# 16. Bonnes pratiques

Toujours :

- écrire du code lisible ;
- éviter la duplication ;
- privilégier des fonctions courtes ;
- respecter l'architecture du projet ;
- documenter les décisions importantes.

---

# 17. Checklist avant publication

Avant chaque Pull Request :

- [ ] Le projet compile.
- [ ] Les tests passent.
- [ ] Le code respecte les conventions.
- [ ] La documentation est à jour.
- [ ] Le CHANGELOG est mis à jour si nécessaire.
- [ ] Aucun secret n'a été ajouté.
- [ ] Les nouveaux fichiers sont correctement organisés.
- [ ] Le code a été relu.

---

# 📚 Documents liés

- [🏠 Documentation](../docs/README.md)
- [🏗 Technical Design Document](../docs/02_TDD.md)
- [🛣 Roadmap](../docs/ROADMAP.md)
- [📝 Changelog](CHANGELOG.md)

---

## Navigation

⬅️ Retour : [Documentation](README.md)
