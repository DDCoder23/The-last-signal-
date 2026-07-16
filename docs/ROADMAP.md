# 🗺️ **ROADMAP - The Last Signal** 
> *MMORPG de survie post-apocalyptique en monde persistant*
> **Dernière mise à jour** : 16 juillet 2026
> **Version** : 0.1.0 (Pré-Prototype)
---


## 📅 **Phases**

---

### 🟡 **Phase 1 : Documentation & Préparation (JUILLET 2026 - **MARS 2027**)**
**Objectif** : Finaliser **toute la documentation** et préparer le développement sans précipitation.
   Tâche | Sous-tâches | Responsable | État | Échéance | Critères de succès |
 |-------|-------------|-------------|------|----------|-------------------|
 | **📚 Finaliser le GDD** | Terminer les 53 fichiers restants (mécaniques, lore, design des systèmes). | **Vous** | 🟡 En cours | **30/11/2026** | 100% du GDD validé et partagé avec l’équipe. |
 | **🏗 Finaliser le TDD** | Architecture technique, schémas réseau, base de données. | **Vous** | ⚪ Non commencé | **15/01/2027** | TDD approuvé par Cyril. |
 | **📖 Lore & Univers** | Histoire, factions, personnages, et événements du monde. | **Vous** + Louanne | ⚪ Non commencé | **28/02/2027** | Lore cohérent et intégré au GDD. |
 | **🎮 Design du Gameplay** | Système de survie, combat, craft, économie (spécifications détaillées). | **Vous** | ⚪ Non commencé | **15/03/2027** | Tous les systèmes décrits dans le GDD. |
 | **📂 Organisation du Projet** | Structure des dossiers, conventions de code, et outils (CI/CD). | **Vous** + Cyril | ⚪ Non commencé | **31/03/2027** | Repository prêt pour le développement. |

➡️ **Durée** : **9 mois** (au lieu de 3) → **Priorité absolue à la documentation**.

---

### 🟡 **Phase 2 : Prototypage Minimal (AVRIL 2027 - **SEPTEMBRE 2027**)**
**Objectif** : Un **prototype jouable** avec les mécaniques de base, **sans pression**.
 | Tâche | Sous-tâches | Responsable | État | Échéance | Critères de succès |
 |-------|-------------|-------------|------|----------|-------------------|
 | **🎮 Prototype Client (Python)** | Affichage 2D basique, déplacement, interactions (ramasser un objet). | **Vous** | ⚪ Non commencé | **30/06/2027** | Joueur peut se déplacer et interagir avec 3 objets. |
 | **🦀 Serveur Rust (MVP)** | Gestion de 10 connexions, synchronisation des positions. | **Vous** + Cyril | ⚪ Non commencé | **15/08/2027** | Serveur stable avec 10 joueurs simultanés. |
 | **🗄 Base de Données (PostgreSQL)** | Schéma pour joueurs, inventaire, et monde. | **Vous** | ⚪ Non commencé | **30/07/2027** | Base locale fonctionnelle. |
 | **🎨 Assets Minimaux** | 1 tilemap (biome "Ruines"), 1 sprite joueur, 3 sprites objets. | Axel, David | ⚪ Non commencé | **30/08/2027** | Assets intégrés et animés. |
 | **🔧 Outils de Build** | Scripts pour lancer le client/serveur en local. | **Vous** | ⚪ Non commencé | **30/09/2027** | 1 commande pour démarrer le jeu. |

➡️ **Durée** : **6 mois** → **MVP jouable en local**.

---

### 🟡 **Phase 3 : Alpha Fermée (OCTOBRE 2027 - **DÉCEMBRE 2027**)**
**Objectif** : **Version jouable en interne** avec les mécaniques de survie.
 | Tâche | Sous-tâches | Responsable | État | Échéance | Critères de succès |
 |-------|-------------|-------------|------|----------|-------------------|
 | **🌐 Communication Client-Serveur** | Protocole réseau finalisé (WebSockets), sync des actions. | **Vous** + Cyril | ⚪ Non commencé | **31/10/2027** | 20 joueurs sans désynchronisation. |
 | **⚔️ Combat PvE (Basique)** | 1 type d’ennemi, attaques simples, gestion des dégâts. | **Vous** | ⚪ Non commencé | **30/11/2027** | Joueur peut tuer 3 ennemis différents. |
 | **🏺 Inventaire & Craft** | Ramassage, stock, et craft de 5 objets. | **Vous** | ⚪ Non commencé | **15/12/2027** | Joueur peut crafter une épée et une potion. |
 | **🌍 Monde Statique** | 1 biome ("Ruines") avec ressources et points d’intérêt. | **Vous** + Axel | ⚪ Non commencé | **31/12/2027** | Monde de 200x200 cases explorable. |
 | **👥 Système de Survie** | Faim et santé (2 besoins de base). | **Vous** | ⚪ Non commencé | **31/12/2027** | Joueur doit manger pour survivre. |

➡️ **Durée** : **3 mois** → **Jeu jouable en interne**.

---
---
### 🟡 **Phase 4 : Alpha Ouverte (JANVIER 2028 - **JUIN 2028**)**
**Objectif** : **Tests avec des amis/contributeurs**.
 | Tâche | Sous-tâches | Responsable | État | Échéance | Critères de succès |
 |-------|-------------|-------------|------|----------|-------------------|
 | **👥 Système de Guildes (Basique)** | Création et gestion des membres. | **Vous** | ⚪ Non commencé | **29/02/2028** | 3 guildes créées. |
 | **💰 Économie Minimale** | Échange d’objets entre joueurs. | **Vous** | ⚪ Non commencé | **31/03/2028** | 10 objets échangeables. |
 | **🌑 2ème Biome ("Forêt")** | Nouveaux ennemis et ressources. | Axel, David | ⚪ Non commencé | **30/04/2028** | Biome intégré et testé. |
 | **🔒 Sauvegarde & Connexion** | Comptes locaux, sauvegarde des progrès. | **Vous** | ⚪ Non commencé | **31/05/2028** | Joueur peut reprendre sa partie. |
 | **🐛 Corrections & Optimisations** | Fix des bugs majeurs, amélioration des performances. | **Vous** + Cyril | ⚪ Non commencé | **30/06/2028** | 60 FPS, 0 bugs critiques. |

➡️ **Durée** : **6 mois** → **Version stable pour tests externes**.

---
---
### 🟡 **Phase 5 : Bêta Fermée (JUILLET 2028 - **DÉCEMBRE 2028**)**
**Objectif** : **Ajout des fonctionnalités majeures**.
 | Tâche | Sous-tâches | Responsable | État | Échéance | Critères de succès |
 |-------|-------------|-------------|------|----------|-------------------|
 | **⚔️ Combat PvP** | Duels et arènes. | **Vous** | ⚪ Non commencé | **31/08/2028** | 10 combats PvP sans bugs. |
 | **🌍 3ème Biome ("Désert")** | Boss, ressources rares. | Axel, David | ⚪ Non commencé | **30/09/2028** | Biome équilibré. |
 | **🛠 Craft Avancé** | 20 recettes, outils améliorés. | **Vous** | ⚪ Non commencé | **31/10/2028** | Joueur peut crafter 1 objet par catégorie. |
 | **🎭 2 Classes** | Survivant et Combattant (compétences uniques). | **Vous** | ⚪ Non commencé | **30/11/2028** | 2 classes jouables. |
 | **📖 Quêtes Principales** | 3 quêtes liées au lore. | Louanne + **Vous** | ⚪ Non commencé | **31/12/2028** | 1 quête terminée par testeur. |

➡️ **Durée** : **6 mois** → **Contenu complet pour la bêta**.

---
---
### 🟡 **Phase 6 : Bêta Ouverte (JANVIER 2029 - **JUIN 2029**)**
**Objectif** : **Préparation au lancement**.
 | Tâche | Sous-tâches | Responsable | État | Échéance | Critères de succès |
 |-------|-------------|-------------|------|----------|-------------------|
 | **🌎 4ème Biome ("Montagnes")** | Boss final et lore complet. | Axel, David | ⚪ Non commencé | **28/02/2029** | Biome testé. |
 | **🎵 Musique & Sons** | Bande-son et effets sonores. | À recruter | ⚪ Non commencé | **31/03/2029** | 5 musiques + 20 effets sonores. |
 | **🌐 Serveurs Cloud** | Déploiement sur AWS/Azure. | **Vous** + Cyril | ⚪ Non commencé | **30/04/2029** | 100 joueurs simultanés stables. |
 | **📢 Marketing** | Site web, réseaux sociaux. | **Vous** | ⚪ Non commencé | **31/05/2029** | 1000 followers. |
 | **🎮 Tests Massifs** | Feedback et corrections finales. | Équipe | ⚪ Non commencé | **30/06/2029** | 90% de satisfaction. |

➡️ **Durée** : **6 mois**.

---
---
### 🟢 **Phase 7 : Lancement Officiel (JUILLET 2029)**
**Objectif** : **Version 1.0**.
 | Tâche | Sous-tâches | Responsable | État | Échéance | Critères de succès |
 |-------|-------------|-------------|------|----------|-------------------|
 | **🚀 Lancement v1.0** | Déploiement final. | Équipe | ⚪ Non commencé | **01/07/2029** | 500 joueurs le jour J. |
 | **📦 Mises à Jour Automatiques** | Système de patchs. | **Vous** | ⚪ Non commencé | **15/07/2029** | Mises à jour sans downtime. |
 | **🎁 Événements de Lancement** | Tournois, cadeaux. | **Vous** | ⚪ Non commencé | **31/07/2029** | 2000 joueurs actifs la 1ère semaine. |

---
---
### 🟢 **Phase 8 : Post-Lancement (AOÛT 2029 - ...)**
**Objectif** : **Améliorations continues**.
 | Tâche | Échéance | Notes |
 |-------|----------|-------|
 | Nouveau biome (tous les 6 mois) | À partir de 2030 | Selon la demande. |
 | Nouvelle classe (tous les ans) | 2030 | Ingénieur. |
 | Mode Hardcore | 2030 | Permadeath. |
 | Version Mobile (Optionnel) | 2031+ | Si ressources disponibles. |

---

---
## 📊 **Nouveaux KPIs Réalistes**
 | Métrique | Objectif Phase 1 | Objectif Phase 2 | Objectif Final |
 |----------|------------------|------------------|----------------|
 | **Joueurs simultanés** | - | 20 | 100+ (lancement) |
 | **Taux de rétention (7j)** | - | 20% | 50% |
 | **Nombre de bugs critiques** | 0 (doc) | 2 max | 0 |
 | **Satisfaction** | - | 70% | 90% |
 | **FPS moyen** | - | 45 | 60+ |

---
---
## 🔗 **Dépendances (Mise à Jour)**
```mermaid
graph TD
    A[GDD] --> B[TDD]
    B --> C[Prototype Client]
    C --> D[Serveur Rust]
    D --> E[Communication Client-Serveur]
    E --> F[Alpha Fermée]
    F --> G[Alpha Ouverte]
    G --> H[Bêta Fermée]
    H --> I[Bêta Ouverte]
    I --> J[Lancement v1.0]
