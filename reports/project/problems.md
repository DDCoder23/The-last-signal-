# 📚 Documentation Problems

Generated: 2026-08-25 04:18:06

## Summary

|Type|Count|
|---|---:|
|❌ Errors|126|
|⚠️ Warnings|844|
|**Total**|**975**|

---

# 📄 

## ❌ Error

- **Module :** links
- **Message :** Traceback (most recent call last):
  File "/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/score.py", line 30, in generate_score
    result = check()
  File "/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/links.py", line 19, in check_links
    for f in ROOT.rglob("*.md")
             ^^^^
NameError: name 'ROOT' is not defined


## ❌ Error

- **Module :** rust
- **Message :** Traceback (most recent call last):
  File "/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/score.py", line 30, in generate_score
    result = check()
  File "/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/rust_docs.py", line 70, in check_rust_docs
    element_name = name_match.group(1) if name_match else "unknown"
                   ~~~~~~~~~~~~~~~~^^^
IndexError: no such group


## ⚠️ Info

- **Module :** organization
- **Message :** La racine contient beaucoup de fichiers.
- **suggestion :** Créer des dossiers pour mieux organiser le projet.

## ❌ Error

- **Module :** navigation
- **Message :** Traceback (most recent call last):
  File "/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/score.py", line 32, in generate_score
    raise TypeError(f"result doit être un dict, reçu {type(result).__name__}")
TypeError: result doit être un dict, reçu int


---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/admin_manager.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'calculer_distance_levenshtein'ligne 27 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'calculer_distance_levenshtein' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trouver_commandes_similaires'ligne 43 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trouver_commandes_similaires' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'admin_only'ligne 55 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'admin_only' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'ConsoleAdmin' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'activer_admin'ligne 443 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'activer_admin' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'installer_raccourci_admin'ligne 463 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'installer_raccourci_admin' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'demander_mot_de_passe'ligne 486 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'demander_mot_de_passe' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'admin_mode_decorator' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrapper'ligne 56 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrapper' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'log'ligne 99 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'log' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'executer'ligne 102 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'executer' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'executer_commande'ligne 126 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'executer_commande' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'keyPressEvent'ligne 464 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'keyPressEvent' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrapper'ligne 511 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrapper' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/banque.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'FenetreBanque' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_banque'ligne 294 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_banque' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'rembourser' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'emprunter' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'verifier_blocage_boutons'ligne 91 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'verifier_blocage_boutons' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'investir' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'investir' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'verifier_investissements' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'sauvegarder_etat_banque' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_banque'ligne 245 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_banque' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'charger_etat_banque' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/configuration.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'ModeDeJeuDialog' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'demander_configuration_jeu' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/debugger.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'log_debug'ligne 33 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'log_debug' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_imports_from_file'ligne 45 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_imports_from_file' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'modules_in_text'ligne 60 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'modules_in_text' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'SoftCriticalDummy' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'DummyModule' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'DummyLoader' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'SoftCriticalLoader' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'MissingModuleFinder' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'SoftDebugger' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'debug'ligne 211 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'debug' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_module'ligne 113 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_module' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'exec_module'ligne 117 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'exec_module' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_module'ligne 120 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_module' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'exec_module'ligne 124 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'exec_module' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'find_spec'ligne 130 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'find_spec' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'enable'ligne 157 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'enable' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'dependency_check'ligne 169 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'dependency_check' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'handle_error'ligne 181 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'handle_error' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'handle_warning'ligne 187 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'handle_warning' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrap'ligne 190 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrap' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrapped'ligne 191 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'wrapped' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/generate_map.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_map' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_map' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/grade_manager.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'gestionnaire_de_grade'ligne 1 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'gestionnaire_de_grade' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'gestionnaire_de_vehicule'ligne 10 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'gestionnaire_de_vehicule' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'gestionnaire_de_batiments'ligne 20 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'gestionnaire_de_batiments' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'manage'ligne 29 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'manage' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur'ligne 2 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur'ligne 12 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur'ligne 22 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur'ligne 30 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decorateur' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne'ligne 3 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne'ligne 13 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne'ligne 23 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne'ligne 31 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'fonction_interne' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/heure_locale.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trouver_fuseau'ligne 97 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trouver_fuseau' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/horloge.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'arreter_toutes_horloges' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'chercher'ligne 216 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'chercher' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'réinitialiser'ligne 221 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'réinitialiser' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'demarrer' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'arreter' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'enregistrer_evenement' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'obtenir_heure' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'obtenir_heure_formatee' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'sauvegarder_dans_json' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'charger_depuis_json'ligne 171 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'charger_depuis_json' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/index_manager.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'initialiser_index' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'mettre_a_jour_index' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'supprimer_de_l_index' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/inv.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'qtes'ligne 19 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'qtes' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'FenetreInventaire' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'qtes'ligne 59 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'qtes' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'FenetreInventaire' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_inventaire'ligne 516 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_inventaire' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'on_search_text_changed' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'effectuer_recherche_optimisee' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'mettre_a_jour_inventaire_complet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'mettre_a_jour_inventaire_rapide' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'demander_quantite_conversion' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'convertir_livre' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'vendre_objet'ligne 359 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'vendre_objet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'vendre_tous_meme_nom' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'boire' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'charger_prix_objets'ligne 477 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'charger_prix_objets' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'effectuer_recherche' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'filtrer_inventaire'ligne 502 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'filtrer_inventaire' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/inventaire.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trouver_cles_par_liste_non_ordonnee' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'qtes'ligne 33 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'qtes' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'pregenerer_cache_enchantements' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trier' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Objet' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'equipement' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Armes' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Potion' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Livres' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nettoyer_stuff_zero'ligne 325 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nettoyer_stuff_zero' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generer_cle_unique' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'safe_increment'ligne 357 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'safe_increment' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'safe_increment' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'QuantiteDialog' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'FenetreMagasin' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_magasin'ligne 746 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_magasin' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attribut_superieur_a_un'ligne 211 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attribut_superieur_a_un' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nom_affiche'ligne 214 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nom_affiche' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nom'ligne 221 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nom' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'image'ligne 224 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'image' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ajouter'ligne 227 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ajouter' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'retirer'ligne 230 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'retirer' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'enchanter'ligne 254 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'enchanter' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'taux_de_critique'ligne 288 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'taux_de_critique' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'enchanter'ligne 292 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'enchanter' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'appliquer_effet'ligne 305 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'appliquer_effet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'diminuer_quantite' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'augmenter_quantite' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'mettre_a_jour_prix_total' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_quantite' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'charger_objets_dispo' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'mettre_a_jour_magasin' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'acheter_objet' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/localisation.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'obtenir_localisation_par_ip'ligne 5 ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/main.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'lister_profils_sauvegardes'ligne 51 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'lister_profils_sauvegardes' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'SaveSelectWidget' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'reprendre_joueur'ligne 137 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'reprendre_joueur' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'reconstruire_stuff'ligne 152 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'reconstruire_stuff' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Jeu' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Lutin' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Perso' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Joueur' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Adversaire' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Combat' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'autosave_provider_factory'ligne 426 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'autosave_provider_factory' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Map3D' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'VispyWidget' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'TresorDialogQt' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'MainMenuWidget' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'EmptyWidget' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'MainFrame' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main'ligne 1099 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_modifier'ligne 227 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_modifier' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generer_stats'ligne 233 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generer_stats' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'position'ligne 257 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'position' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'set_position'ligne 260 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'set_position' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'deplacer'ligne 274 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'deplacer' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'subir_degats'ligne 283 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'subir_degats' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'liste'ligne 288 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'liste' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'jet_attaque'ligne 295 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'calcul_degats'ligne 300 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'save'ligne 350 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'save' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'to_dict'ligne 360 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'to_dict' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'cara_sup'ligne 405 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'cara_sup' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attaquer'ligne 415 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'provider'ligne 429 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'provider' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_height'ligne 449 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_height' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'on_key_vispy'ligne 559 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'on_key_vispy' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'refresh_joueur'ligne 632 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'refresh_joueur' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_info'ligne 646 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_info' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_tresor'ligne 664 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_tresor' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'on_take'ligne 731 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'on_take' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'closeEvent'ligne 782 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'closeEvent' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'mettre_a_jour_horloge' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nouveau_jour' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nouvelle_semaine' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nouveau_mois' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'nouvelle_annee' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'show_menu'ligne 929 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'show_menu' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_new_game'ligne 939 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_new_game' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_load_game'ligne 977 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_load_game' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'show_empty' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'clear_layout' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_game'ligne 1010 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_game' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'load_game_from_slot'ligne 1066 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'load_game_from_slot' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'show_save_select'ligne 1073 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'show_save_select' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'layout' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'closeEvent'ligne 1092 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'closeEvent' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'on_exit'ligne 1101 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'on_exit' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/table_de_conversion.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'StatsConversion' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'qtes' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'chercher_livre'ligne 25 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'chercher_livre' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'convertir_livres'ligne 130 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'convertir_livres' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l1_l2'ligne 153 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l1_l2' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l2_l3'ligne 190 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l2_l3' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l3_l4'ligne 227 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l3_l4' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l4_l5'ligne 269 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l4_l5' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l5_l6'ligne 317 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'l5_l6' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'niveau_to_romain'ligne 52 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_niveau'ligne 56 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_nom'ligne 65 ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/Ancien/tresor.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'tresor' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_tresor'ligne 992 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_tresor' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ouvrir_tresor'ligne 915 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ouvrir_tresor' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ouvrir_tresor_admin'ligne 973 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ouvrir_tresor_admin' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/__init__.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/client.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'connect'ligne 26 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'connect' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'send_packet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'receive_packet'ligne 85 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'receive_packet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'disconnect'ligne 158 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'disconnect' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/logs.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'log'ligne 4 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'log' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/main.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main'ligne 10 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packet.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'PacketType' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'Packet' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'encode'ligne 30 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'encode' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decode'ligne 52 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decode' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/__init__.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/ban.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'BanType' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'BanPacket' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload'ligne 23 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/chat.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'ChatPacket' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload'ligne 15 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/log.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'LogPacket' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload'ligne 12 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/login.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'LoginPacket' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload'ligne 29 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/move.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'MovePacket' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload'ligne 19 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/ping.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'PingPacket' ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/client_python/packets/singup.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'SingupPacket' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload'ligne 29 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'from_payload' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/dashboard.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_server'ligne 10 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'start_server' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_docs.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_docs_database'ligne 7 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_docs_database' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_performance.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_performance_database'ligne 1 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_performance_database' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_python.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_python_database'ligne 18 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_python_database' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_python_database' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_rust.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_rust_database'ligne 19 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_rust_database' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_rust_database' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_security.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_security_database'ligne 13 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_security_database' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_security_database' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/database/utils.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'read_report'ligne 5 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'read_report' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_int'ligne 15 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_int' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_float'ligne 25 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_float' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/database_manager.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La classe 'DatabaseManager' ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_tables'ligne 25 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_tables' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_tables' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_run'ligne 360 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_run' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'insert'ligne 414 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'insert' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'close'ligne 436 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'close' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_security'ligne 438 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_security' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_security_issue'ligne 462 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_security_issue' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_performance'ligne 492 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_performance' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/docs_score.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/links.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_links'ligne 16 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_links' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_links'ligne 68 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'extract_links' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_empty_links'ligne 85 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_empty_links' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_local_links'ligne 111 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_local_links' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_external_links'ligne 141 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_external_links' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_anchors'ligne 169 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_anchors' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_images'ligne 191 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_images' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_duplicate_links'ligne 226 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_duplicate_links' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/markdown.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'load_markdownlint_report'ligne 32 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'load_markdownlint_report' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_markdown_files'ligne 44 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_markdown'ligne 56 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_empty_files'ligne 91 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_empty_files' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_encoding'ligne 117 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_encoding' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_line_length'ligne 129 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_line_length' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_trailing_spaces'ligne 146 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_trailing_spaces' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_code_blocks'ligne 163 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_code_blocks' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_lists'ligne 177 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_lists' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_tables'ligne 215 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_tables' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_html'ligne 248 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_html' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/navigation.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_navigation'ligne 1 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_navigation' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/organization.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_organization'ligne 4 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_organization' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/problem.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_problem'ligne 3 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_problem' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/python_docs.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Info

- **Module :** python
- **Message :** TODO présent dans le fichier.

## ⚠️ Info

- **Module :** python
- **Message :** FIXME présent dans le fichier.

## ⚠️ Info

- **Module :** python
- **Message :** XXX présent dans le fichier.

## ⚠️ Info

- **Module :** python
- **Message :** HACK présent dans le fichier.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_python_docs' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/report.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_report'ligne 25 ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/rust_docs.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_rust_docs' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/score.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_score'ligne 11 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_score' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/spelling.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_spelling' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/titles.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_titles'ligne 17 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_titles' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_single_h1'ligne 52 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_single_h1' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_heading_order'ligne 67 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_heading_order' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_heading_spacing'ligne 91 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_heading_spacing' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_empty_titles'ligne 114 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_empty_titles' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_title_length'ligne 132 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_title_length' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_duplicate_titles'ligne 154 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check_duplicate_titles' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/generate_dashboard.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_documentation_score'ligne 12 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_documentation_score' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_database_data'ligne 28 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_database_data' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'calculate_quality'ligne 88 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'calculate_quality' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_json'ligne 123 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_json' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_json' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/generate_problems_md.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_problems_md'ligne 10 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_problems_md' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/recherche.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'rechercher' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ecrire_fichier'ligne 94 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ecrire_fichier' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main'ligne 172 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/transformateur.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/update_database.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_database'ligne 9 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'update_database' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/utils/calculateur.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'log_erreur_async' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'creer_fichier_vide_async' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'calculer_taille_dossier_async'ligne 33 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'calculer_taille_dossier_async' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'mettre_a_jour_excel_fichiers_et_dossiers' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/utils/file_chercheur.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'iter_files'ligne 16 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'iter_files' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/utils/gestionnaire.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main'ligne 6 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ecrire'ligne 74 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ecrire' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/utils/gestionnaire_de_fichiers.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trouver_chemins_par_type'ligne 7 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'trouver_chemins_par_type' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/scripts/voir_database.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_database'ligne 14 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'afficher_database' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/security/__init__.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/security/vault.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_key' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'load_key'ligne 30 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'load_key' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'encrypt_vault'ligne 40 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'encrypt_vault' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decrypt_vault'ligne 54 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'decrypt_vault' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_secret'ligne 68 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'add_secret' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_secret' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_communication_key' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'get_or_create_communication_key' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/setup.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/__init__.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/security/attack_test.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'run'ligne 39 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'sha256_file'ligne 63 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'clone_repository'ligne 84 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'clone_repository' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_test_environment_files'ligne 195 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_test_environment_files' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'find_master_keys'ligne 287 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attack_cargo_lock'ligne 364 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attack_env'ligne 402 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attack_idea'ligne 444 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attack_security_access'ligne 487 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attack_security_file'ligne 569 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'attack_vault'ligne 646 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'restore_file'ligne 692 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'run_integrity_check'ligne 722 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'execute_integrity_attack'ligne 747 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'execute_integrity_attack' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'execute_vault_attack'ligne 825 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'execute_vault_attack' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'verify_git_clean'ligne 958 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main'ligne 1017 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main' dépasse 80 lignes.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/security/integrity_check.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create'ligne 236 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'check'ligne 262 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main'ligne 343 ne possède pas de docstring.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/security/test_fuzzing.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_packet'ligne 17 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'create_packet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'send_packet'ligne 30 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'send_packet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'random_payload'ligne 48 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'random_payload' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'random_packet'ligne 55 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'random_packet' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main'ligne 75 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'main' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/security/test_load.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ping'ligne 14 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ping' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'run_test'ligne 50 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'run_test' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_main'ligne 85 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_main' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/security/test_sql_injection.py

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_advanced_attacks_database' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_advanced_attacks_database' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_binary_protocol_attacks' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_binary_protocol_attacks' dépasse 80 lignes.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'login_thread'ligne 256 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'login_thread' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ban_toggle'ligne 294 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'ban_toggle' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/test_client.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_main'ligne 3 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_main' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_key'ligne 5 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_key' ne possède pas d'annotations de type.

---

# 📄 /home/runner/work/The-last-signal-/The-last-signal-/tests/test_crypto_rotor.py

## ⚠️ Warning

- **Module :** python
- **Message :** Le module ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'splitmix64' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'derive_rotor_seed' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'generate_rotor' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'inverse_permutation'ligne 128 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'inverse_permutation' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'rotor_forward' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'rotor_inverse' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'communication_key'ligne 199 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'communication_key' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_splitmix64_deterministic'ligne 210 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_splitmix64_deterministic' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_splitmix64_different_seeds'ligne 220 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_splitmix64_different_seeds' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_splitmix64_is_u64'ligne 229 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_splitmix64_is_u64' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_seed_deterministic'ligne 243 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_seed_deterministic' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_seeds_are_different'ligne 260 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_seeds_are_different' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_seed_is_u64'ligne 275 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_seed_is_u64' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_has_256_values'ligne 293 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_has_256_values' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_is_permutation'ligne 305 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_is_permutation' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_all_16_rotors_are_valid'ligne 319 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_all_16_rotors_are_valid' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_is_deterministic'ligne 337 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_is_deterministic' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotors_are_different'ligne 354 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotors_are_different' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_forward_inverse'ligne 393 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_rotor_forward_inverse' ne possède pas d'annotations de type.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_all_16_rotors_forward_inverse'ligne 427 ne possède pas de docstring.

## ⚠️ Warning

- **Module :** python
- **Message :** La fonction 'test_all_16_rotors_forward_inverse' ne possède pas d'annotations de type.

---

# 📄 README.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 17 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 19 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (1).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (8).

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:2 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:176 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:1 titre dupliqué (déjà présent dans README_ENG.md:1).

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:2 titre dupliqué (déjà présent dans README_ENG.md:2).

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:56 titre dupliqué (déjà présent dans README_ENG.md:53).

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:104 titre dupliqué (déjà présent dans README_ENG.md:103).

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:197 titre dupliqué (déjà présent dans README_ENG.md:198).

## ⚠️ Warning

- **Module :** titles
- **Message :** README.md:204 titre dupliqué (déjà présent dans README_ENG.md:205).

---

# 📄 README_ENG.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 16 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 18 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (1).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (201).

## ⚠️ Warning

- **Module :** titles
- **Message :** README_ENG.md:2 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** README_ENG.md:14 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** README_ENG.md:32 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** README_ENG.md:176 titre sans ligne vide avant.

---

# 📄 docs/ARCHITECTURE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/ARCHITECTURE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/CHANGELOG.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (40).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:25 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:36 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:1 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:1).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:7 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:7).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:9 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:27).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:25 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:25).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:27 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:27).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:36 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:34).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG.md:38 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:27).

---

# 📄 docs/CHANGELOG_ENG.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (17).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (20).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (39).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG_ENG.md:25 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG_ENG.md:34 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CHANGELOG_ENG.md:36 titre dupliqué (déjà présent dans docs/CHANGELOG_ENG.md:27).

---

# 📄 docs/CODING_RULES.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 151 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 257 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (258).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (415).

## ❌ Error

- **Module :** titles
- **Message :** docs/CODING_RULES.md: contient 22 titres H1 (1 attendu).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CODING_RULES.md:293 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/CODING_RULES.md:363 titre dupliqué (déjà présent dans README_ENG.md:103).

---

# 📄 docs/DATABASE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/DATABASE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/NETWORK.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/NETWORK.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/QRB_flake8_error.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 899 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1147 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1241 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1338 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1425 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1505 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1555 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1615 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1686 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1811 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1841 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 1878 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (3).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (339).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (1491).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (1804).

## ❌ Error

- **Module :** titles
- **Message :** docs/QRB_flake8_error.md: contient 3 titres H1 (1 attendu).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/QRB_flake8_error.md:942 saut de niveau H1 → H3.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/QRB_flake8_error.md:1370 saut de niveau H1 → H3.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/QRB_flake8_error.md:935 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/QRB_flake8_error.md:1363 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/QRB_flake8_error.md:1363 titre dupliqué (déjà présent dans docs/QRB_flake8_error.md:935).

---

# 📄 docs/README.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 12 > 120 caractères.

## ❌ Error

- **Module :** titles
- **Message :** docs/README.md: contient 6 titres H1 (1 attendu).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/README.md:2 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/README.md:2 titre dupliqué (déjà présent dans README_ENG.md:2).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/README.md:68 titre dupliqué (déjà présent dans README.md:122).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/README.md:175 titre dupliqué (déjà présent dans README.md:165).

---

# 📄 docs/ROADMAP.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 16 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 17 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 18 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 19 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 20 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 30 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 31 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 32 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 33 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 34 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 44 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 45 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 46 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 47 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 48 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 58 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 59 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 60 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 61 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 62 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 72 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 73 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 74 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 75 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 76 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 86 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 87 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 88 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 90 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 101 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 102 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (1).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (89).

## ❌ Error

- **Module :** markdown
- **Message :** Bloc de code non fermé.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/ROADMAP.md:54 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/ROADMAP.md:68 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/ROADMAP.md:82 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/ROADMAP.md:96 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/ROADMAP.md:106 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/ROADMAP.md:118 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/ROADMAP.md:129 titre sans ligne vide avant.

---

# 📄 docs/TEAM.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/TEAM.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gameplay/README.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gameplay/README.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/01_VISION.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 27 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 51 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 75 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 105 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (5).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (6).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (7).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (8).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/01_VISION.md:13 titre dupliqué (déjà présent dans docs/CODING_RULES.md:21).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/01_VISION.md:25 titre dupliqué (déjà présent dans docs/CODING_RULES.md:43).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/01_VISION.md:165 titre dupliqué (déjà présent dans docs/CODING_RULES.md:409).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/01_VISION.md:173 titre dupliqué (déjà présent dans docs/CODING_RULES.md:419).

---

# 📄 docs/gdd/02_UNIVERS.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 30 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 32 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 42 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (5).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (6).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (7).

## ⚠️ Warning

- **Module :** markdown
- **Message :** Espace en fin de ligne (8).

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/02_UNIVERS.md: contient 18 titres H1 (1 attendu).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/02_UNIVERS.md:3 titre dupliqué (déjà présent dans docs/README.md:41).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/02_UNIVERS.md:13 titre dupliqué (déjà présent dans docs/CODING_RULES.md:21).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/02_UNIVERS.md:312 titre dupliqué (déjà présent dans docs/CODING_RULES.md:409).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/02_UNIVERS.md:320 titre dupliqué (déjà présent dans docs/CODING_RULES.md:419).

---

# 📄 docs/gdd/03_SCENARIO.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 26 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 28 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 50 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 57 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 58 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 59 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 60 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 64 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 65 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 68 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 72 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 73 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 76 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 83 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 84 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 85 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 93 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 94 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 95 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 96 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 103 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 104 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 105 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 106 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 107 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 121 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 122 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 124 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 133 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 134 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 135 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 136 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 137 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 155 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 156 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 158 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 159 > 120 caractères.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:23 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:40 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:43 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:90 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:100 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:111 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:128 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:150 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:170 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:170 titre dupliqué (déjà présent dans docs/CODING_RULES.md:409).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/03_SCENARIO.md:182 titre dupliqué (déjà présent dans docs/CODING_RULES.md:419).

---

# 📄 docs/gdd/04_CHRONOLOGIE.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 9 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 11 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 17 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 35 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 50 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 78 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 110 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 112 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 132 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 146 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 154 > 120 caractères.

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 199 > 120 caractères.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/04_CHRONOLOGIE.md:201 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/04_CHRONOLOGIE.md:201 titre dupliqué (déjà présent dans docs/CODING_RULES.md:409).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/04_CHRONOLOGIE.md:210 titre dupliqué (déjà présent dans docs/CODING_RULES.md:419).

---

# 📄 docs/gdd/05_FACTIONS.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Contenu très faible.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/05_FACTIONS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/06_REGIONS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/06_REGIONS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/07_VILLES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/07_VILLES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/08_DONJONS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/08_DONJONS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/09_PERSONNAGES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/09_PERSONNAGES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/10_CREATION_PERSONNAGE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/10_CREATION_PERSONNAGE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/11_PROGRESSION.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/11_PROGRESSION.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/12_STATISTIQUES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/12_STATISTIQUES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/13_COMPETENCES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/13_COMPETENCES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/14_CLASSES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/14_CLASSES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/15_GAMEPLAY.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/15_GAMEPLAY.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/16_COMBAT.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/16_COMBAT.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/17_IA.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/17_IA.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/18_MONSTRES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/18_MONSTRES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/19_BOSS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/19_BOSS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/20_INVENTAIRE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/20_INVENTAIRE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/21_EQUIPEMENT.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/21_EQUIPEMENT.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/22_OBJETS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/22_OBJETS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/23_BANQUE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/23_BANQUE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/24_COFFRES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/24_COFFRES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/25_ECONOMIE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/25_ECONOMIE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/26_COMMERCE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/26_COMMERCE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/27_HOTEL_DES_VENTES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/27_HOTEL_DES_VENTES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/28_MONNAIES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/28_MONNAIES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/29_METIERS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/29_METIERS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/30_CRAFT.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/30_CRAFT.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/31_RECOLTE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/31_RECOLTE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/32_CARTE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/32_CARTE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/33_BIOMES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/33_BIOMES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/34_METEO.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/34_METEO.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/35_JOUR_NUIT.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/35_JOUR_NUIT.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/36_GUILDES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/36_GUILDES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/37_GROUPES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/37_GROUPES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/38_CHAT.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/38_CHAT.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/39_PVE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/39_PVE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/40_PVP.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/40_PVP.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/41_QUETES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/41_QUETES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/42_EVENEMENTS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/42_EVENEMENTS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/43_SUCCES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/43_SUCCES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/44_HUD.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/44_HUD.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/45_MENUS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/45_MENUS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/46_ACCESSIBILITE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/46_ACCESSIBILITE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/47_MUSIQUES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/47_MUSIQUES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/48_AMBIANCES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/48_AMBIANCES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/49_EFFETS_SONORES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/49_EFFETS_SONORES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/50_DIRECTION_ARTISTIQUE.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/50_DIRECTION_ARTISTIQUE.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/51_CONCEPT_ART.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/51_CONCEPT_ART.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/52_MODELES_3D.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/52_MODELES_3D.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/53_ANIMATIONS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/53_ANIMATIONS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/54_EXTENSIONS.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/54_EXTENSIONS.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/55_IDEES.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/55_IDEES.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/gdd/README.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 12 > 120 caractères.

## ❌ Error

- **Module :** titles
- **Message :** docs/gdd/README.md: contient 5 titres H1 (1 attendu).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/README.md:2 titre sans ligne vide avant.

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/README.md:2 titre dupliqué (déjà présent dans README_ENG.md:2).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/README.md:18 titre dupliqué (déjà présent dans docs/CODING_RULES.md:9).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/README.md:36 titre dupliqué (déjà présent dans docs/README.md:41).

## ⚠️ Warning

- **Module :** titles
- **Message :** docs/gdd/README.md:150 titre dupliqué (déjà présent dans docs/CODING_RULES.md:409).

---

# 📄 docs/lore/README.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/lore/README.md: contient 0 titres H1 (1 attendu).

---

# 📄 docs/tdd/README.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** docs/tdd/README.md: contient 0 titres H1 (1 attendu).

---

# 📄 lychee/out.md

## ⚠️ Warning

- **Module :** markdown
- **Message :** Ligne 33 > 120 caractères.

---

# 📄 server_rust/README.md

## ❌ Error

- **Module :** markdown
- **Message :** Fichier vide.

## ❌ Error

- **Module :** titles
- **Message :** server_rust/README.md: contient 0 titres H1 (1 attendu).

---

