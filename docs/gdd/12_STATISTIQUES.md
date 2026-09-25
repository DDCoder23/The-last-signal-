[🏠 Documentation](../README.md) > [🎮 GDD](README.md)

# 📊 Statistiques

> **Document :** Statistiques
> **Code :** GDD-012
> **Version :** 1.0.0
> **Statut :** 🟡 En cours de définition

---

## 📑 Table des matières

1. [Présentation](#1--présentation)
2. [Objectifs](#2--objectifs)
3. [Principes](#3--principes)
4. [Catégories de statistiques](#4--catégories-de-statistiques)
5. [Statistiques principales](#5--statistiques-principales)
6. [Statistiques secondaires](#6--statistiques-secondaires)
7. [Statistiques de combat](#7--statistiques-de-combat)
8. [Statistiques défensives](#8--statistiques-défensives)
9. [Statistiques liées à la survie](#9--statistiques-liées-à-la-survie)
10. [Statistiques liées aux actions](#10--statistiques-liées-aux-actions)
11. [Évolution des statistiques](#11--évolution-des-statistiques)
12. [Influence de l'équipement](#12--influence-de-léquipement)
13. [Influence des compétences](#13--influence-des-compétences)
14. [Influence des états](#14--influence-des-états)
15. [Limites et valeurs](#15--limites-et-valeurs)
16. [Affichage des statistiques](#16--affichage-des-statistiques)
17. [Tableau des statistiques](#17--tableau-des-statistiques)
18. [Documents liés](#18--documents-liés)

---

## 1. 📖 Présentation

Les statistiques représentent les caractéristiques numériques utilisées pour décrire l'état et les capacités d'un personnage dans **The Last Signal**.

Elles permettent aux différents systèmes du jeu de déterminer les capacités d'un personnage et leurs interactions avec le monde.

Les statistiques peuvent être influencées par la progression, les compétences, l'équipement, les états du personnage et certaines situations de jeu.

---

## 2. 🎯 Objectifs

Le système de statistiques doit permettre de :

* représenter les caractéristiques du personnage ;
* différencier les personnages ;
* fournir des valeurs utilisables par les systèmes de jeu ;
* permettre une progression cohérente ;
* gérer les effets de l'équipement ;
* gérer les effets des compétences ;
* permettre le calcul des actions et interactions ;
* conserver un système compréhensible pour le joueur.

Les statistiques doivent être suffisamment nombreuses pour représenter les différents systèmes du jeu sans créer une complexité inutile.

---

## 3. 🧭 Principes

Les statistiques suivent plusieurs principes.

### Cohérence

Chaque statistique doit avoir une fonction clairement définie.

### Utilité

Une statistique ne doit pas exister uniquement pour augmenter le nombre de paramètres.

### Interactions

Les statistiques peuvent être utilisées par plusieurs systèmes du jeu.

### Équilibrage

Les valeurs doivent être équilibrées afin qu'aucune statistique ne rende les autres inutiles.

### Lisibilité

Le joueur doit pouvoir comprendre l'effet général d'une statistique.

---

## 4. 🧩 Catégories de statistiques

Les statistiques peuvent être regroupées en plusieurs catégories :

* statistiques principales ;
* statistiques secondaires ;
* statistiques de combat ;
* statistiques défensives ;
* statistiques de survie ;
* statistiques liées aux actions.

Cette organisation permet de distinguer les caractéristiques fondamentales des valeurs calculées.

---

## 5. 💪 Statistiques principales

Les statistiques principales représentent les caractéristiques fondamentales du personnage.

Les statistiques définitives seront déterminées lors de la conception détaillée du système.

| ID         | Statistique | Description | Valeur initiale |   Maximum |
| ---------- | ----------- | ----------- | --------------: | --------: |
| `STAT-001` | À définir   | À définir   |       À définir | À définir |
| `STAT-002` | À définir   | À définir   |       À définir | À définir |
| `STAT-003` | À définir   | À définir   |       À définir | À définir |
| `STAT-004` | À définir   | À définir   |       À définir | À définir |
| `STAT-005` | À définir   | À définir   |       À définir | À définir |

> Les statistiques ci-dessus sont des emplacements de conception et ne constituent pas encore une liste définitive.

---

## 6. 📈 Statistiques secondaires

Les statistiques secondaires peuvent être calculées à partir de plusieurs paramètres.

Elles peuvent notamment représenter :

* une capacité maximale ;
* une vitesse ;
* une efficacité ;
* une résistance ;
* une régénération ;
* une probabilité ;
* une valeur dérivée.

Une statistique secondaire peut dépendre :

* d'une ou plusieurs statistiques principales ;
* du niveau ;
* d'une compétence ;
* d'un équipement ;
* d'un état du personnage.

Les formules définitives seront définies lors de l'équilibrage.

---

## 7. ⚔️ Statistiques de combat

Les statistiques de combat sont utilisées par le système de combat.

Elles peuvent notamment concerner :

* les dégâts ;
* la précision ;
* la vitesse d'action ;
* les chances de réussite ;
* les effets des attaques ;
* les capacités offensives.

Les valeurs exactes et leurs formules seront définies dans **16_COMBAT.md**.

---

## 8. 🛡️ Statistiques défensives

Les statistiques défensives représentent la capacité du personnage à résister aux différentes menaces.

Elles peuvent notamment concerner :

* la défense ;
* les résistances ;
* la réduction de dégâts ;
* l'esquive ;
* certaines protections spécifiques.

Les statistiques défensives doivent être équilibrées avec les statistiques offensives.

---

## 9. ❤️ Statistiques liées à la survie

Le monde de **The Last Signal** étant basé sur la survie, certaines statistiques peuvent représenter l'état physique du personnage.

Elles peuvent notamment concerner :

* la santé ;
* l'endurance ;
* la faim ;
* la soif ;
* la fatigue ;
* l'état général.

Ces valeurs peuvent évoluer pendant l'exploration et les différentes activités du jeu.

---

## 10. 🏃 Statistiques liées aux actions

Certaines statistiques peuvent influencer les actions réalisées par le personnage.

Elles peuvent notamment affecter :

* la vitesse de déplacement ;
* la capacité de transport ;
* l'utilisation d'objets ;
* la vitesse d'interaction ;
* certaines actions physiques ;
* la récupération.

Les effets précis seront définis dans les systèmes concernés.

---

## 11. 🔄 Évolution des statistiques

Les statistiques peuvent évoluer au cours de la progression du personnage.

Leur évolution peut dépendre :

* du niveau ;
* de points de statistiques ;
* des compétences ;
* des classes ;
* de l'équipement ;
* des effets temporaires ;
* des effets permanents.

Toutes les statistiques ne doivent pas nécessairement évoluer de la même manière.

---

## 12. 🎒 Influence de l'équipement

L'équipement peut modifier certaines statistiques.

Un objet peut notamment fournir :

* un bonus ;
* une pénalité ;
* une résistance ;
* une modification d'une valeur secondaire ;
* un effet particulier.

Les règles détaillées concernant les objets et l'équipement sont définies dans :

* **20_INVENTAIRE.md** ;
* **21_EQUIPEMENT.md** ;
* **22_OBJETS.md**.

Les bonus doivent être contrôlés afin d'éviter des valeurs excessives.

---

## 13. 🧠 Influence des compétences

Les compétences peuvent modifier les statistiques du personnage.

Une compétence peut :

* augmenter une statistique ;
* réduire une pénalité ;
* améliorer une valeur secondaire ;
* modifier une formule ;
* fournir un effet temporaire ;
* fournir un effet permanent.

Le système détaillé est défini dans **13_COMPETENCES.md**.

---

## 14. 🩹 Influence des états

Les statistiques peuvent être temporairement modifiées par l'état du personnage.

Ces modifications peuvent être provoquées par :

* blessures ;
* fatigue ;
* faim ;
* soif ;
* effets environnementaux ;
* contamination ;
* effets de certains objets ;
* effets de compétences ;
* événements.

Les effets doivent être clairement identifiables par le joueur.

---

## 15. ⚖️ Limites et valeurs

Chaque statistique doit posséder des limites adaptées à son fonctionnement.

Selon la statistique, il peut exister :

* une valeur minimale ;
* une valeur maximale ;
* une valeur de départ ;
* une valeur normale ;
* une valeur temporaire ;
* une valeur calculée.

Les limites définitives seront déterminées pendant l'équilibrage.

> **Valeurs définitives :** À définir.

---

## 16. 🖥️ Affichage des statistiques

Le joueur doit pouvoir consulter les statistiques importantes de son personnage.

L'interface peut afficher :

* la valeur actuelle ;
* la valeur maximale ;
* les bonus ;
* les pénalités ;
* les effets actifs ;
* l'évolution récente ;
* la description de la statistique.

Les informations détaillées doivent être accessibles sans surcharger l'interface principale.

---

## 17. 📋 Tableau des statistiques

| ID         | Nom       | Catégorie  | Type       | Modifiable    | Valeur    |
| ---------- | --------- | ---------- | ---------- | ------------- | --------- |
| `STAT-001` | À définir | Principale | Permanente | Oui           | À définir |
| `STAT-002` | À définir | Principale | Permanente | Oui           | À définir |
| `STAT-003` | À définir | Secondaire | Calculée   | Indirectement | À définir |
| `STAT-004` | À définir | Combat     | Calculée   | Indirectement | À définir |
| `STAT-005` | À définir | Défensive  | Calculée   | Indirectement | À définir |
| `STAT-006` | À définir | Survie     | Variable   | Oui           | À définir |

> Ce tableau sera complété lorsque les statistiques définitives seront validées.

---

## 18. 📚 Documents liés

### GDD

* [`01_VISION.md`](01_VISION.md)
* [`09_PERSONNAGES.md`](09_PERSONNAGES.md)
* [`10_CREATION_PERSONNAGE.md`](10_CREATION_PERSONNAGE.md)
* [`11_PROGRESSION.md`](11_PROGRESSION.md)
* [`13_COMPETENCES.md`](13_COMPETENCES.md)
* [`14_CLASSES.md`](14_CLASSES.md)
* [`15_GAMEPLAY.md`](15_GAMEPLAY.md)
* [`16_COMBAT.md`](16_COMBAT.md)
* [`18_MONSTRES.md`](18_MONSTRES.md)
* [`19_BOSS.md`](19_BOSS.md)
* [`20_INVENTAIRE.md`](20_INVENTAIRE.md)
* [`21_EQUIPEMENT.md`](21_EQUIPEMENT.md)
* [`22_OBJETS.md`](22_OBJETS.md)
* [`29_METIERS.md`](29_METIERS.md)
* [`30_CRAFT.md`](30_CRAFT.md)
* [`31_RECOLTE.md`](31_RECOLTE.md)
* [`33_BIOMES.md`](33_BIOMES.md)
* [`34_METEO.md`](34_METEO.md)
* [`35_JOUR_NUIT.md`](35_JOUR_NUIT.md)

### Documentation générale

* [`../README.md`](../README.md)
* [`../ROADMAP.md`](../ROADMAP.md)
* [`../ARCHITECTURE.md`](../ARCHITECTURE.md)

---

## 📌 État du document

**Version :** 1.0.0
**Statut :** 🟡 En cours de définition
**Dernière mise à jour :** À définir

Ce document définit la structure générale du système de statistiques. Les statistiques définitives, leurs valeurs, leurs formules et leurs limites seront précisées lors de la conception et de l'équilibrage des systèmes de jeu.
---

## Navigation

⬅️ [Progression](11_PROGRESSION.md)

➡️ [Competences](13_COMPETENCES.md)
