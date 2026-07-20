# 🐍 Python CI Report

Run : 537
Branch : main
Commit : 50c100f4def2db750dcd69d2da0999396a10243c
Date : Mon Jul 20 00:43:10 UTC 2026

---

# 📊 Summary

## ⚫ Black

**Files to reformat:** 37

<details>
<summary>Show files</summary>
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/Secure_save.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/debugger.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/generate_map.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/banque.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/grade_manager.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/index_manager.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/admin_manager.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/jet_de_des.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/horloge.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/inv.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/table_de_conversion.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/inventaire.py
/home/runner/work/The-last-signal-/The-last-signal-/dashboard.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_docs.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_performance.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_python.py
/home/runner/work/The-last-signal-/The-last-signal-/client-python/client.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_security.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/database/update_rust.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/database_manager.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/main.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/navigation.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/organization.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/problem.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/links.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/python_docs.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/rust_docs.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/report.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/markdown.py
/home/runner/work/The-last-signal-/The-last-signal-/Ancien/tresor.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/spelling.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/score.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/update_database.py
/home/runner/work/The-last-signal-/The-last-signal-/voir_database.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/generate_problems_md.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/generate_dashboard.py
/home/runner/work/The-last-signal-/The-last-signal-/scripts/documentation/titles.py
</details>
## Flake8

### 📊 Erreurs par code

| Code | Nombre |
|------|-------:|


<details>
<summary>📋 Voir toutes les erreurs Flake8</summary>

| Fichier | Ligne | Code | Message |
|---------|------:|------|---------|
## Quality Analysis
### Complexity
dashboard.py
    F 10:0 start_server - A
client-python/client.py
    M 151:4 VispyWidget.on_key_vispy - C
    C 47:0 VispyWidget - B
    M 395:4 MainFrame.clear_layout - A
    M 48:4 VispyWidget.__init__ - A
    C 237:0 MainMenuWidget - A
    C 285:0 MainFrame - A
    M 352:4 MainFrame.show_menu - A
    M 379:4 MainFrame.show_empty - A
    M 441:4 MainFrame.show_save_select - A
    M 452:4 MainFrame.layout - A
    C 10:0 Joueur - A
    C 34:0 Map3D - A
    M 216:4 VispyWidget.update_info - A
    M 269:4 MainMenuWidget._new_game - A
    M 273:4 MainMenuWidget._load_game - A
    C 278:0 EmptyWidget - A
    F 467:0 main - A
    M 11:4 Joueur.__init__ - A
    M 26:4 Joueur._initialiser_stats - A
    M 35:4 Map3D.__init__ - A
    M 41:4 Map3D.get_height - A
    M 202:4 VispyWidget.refresh_joueur - A
    M 238:4 MainMenuWidget.__init__ - A
    M 279:4 EmptyWidget.__init__ - A
    M 287:4 MainFrame.__init__ - A
    M 362:4 MainFrame.start_new_game - A
    M 374:4 MainFrame.start_load_game - A
    M 407:4 MainFrame.start_game - A
    M 434:4 MainFrame.load_game_from_slot - A
    M 460:4 MainFrame.closeEvent - A
Ancien/jet_de_des.py
    F 2:0 jet_de_des - A
Ancien/main.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/heure_locale.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/tresor.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/localisation.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/inv.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/index_manager.py
    F 18:0 _ajouter_objet_au_index - B
    F 56:0 rechercher_dans_index - A
    F 74:0 supprimer_de_l_index - A
    F 47:0 _ajouter_mot_cle - A
    F 11:0 mettre_a_jour_index - A
    F 6:0 initialiser_index - A
Ancien/grade_manager.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/configuration.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/debugger.py
    F 45:0 extract_imports_from_file - B
    C 129:0 MissingModuleFinder - B
    M 169:4 SoftDebugger.dependency_check - B
    M 130:4 MissingModuleFinder.find_spec - A
    M 76:4 SoftCriticalDummy.__getattr__ - A
    F 33:0 log_debug - A
    C 67:0 SoftCriticalDummy - A
    M 68:4 SoftCriticalDummy.__init__ - A
    C 152:0 SoftDebugger - A
    F 60:0 modules_in_text - A
    M 85:4 SoftCriticalDummy._soft_stub - A
    C 96:0 DummyModule - A
    M 101:4 DummyModule.__getattr__ - A
    C 112:0 DummyLoader - A
    C 119:0 SoftCriticalLoader - A
    M 157:4 SoftDebugger.enable - A
    F 211:0 debug - A
    M 90:4 SoftCriticalDummy.__call__ - A
    M 97:4 DummyModule.__init__ - A
    M 108:4 DummyModule.__call__ - A
    M 113:4 DummyLoader.create_module - A
    M 117:4 DummyLoader.exec_module - A
    M 120:4 SoftCriticalLoader.create_module - A
    M 124:4 SoftCriticalLoader.exec_module - A
    M 153:4 SoftDebugger.__init__ - A
    M 181:4 SoftDebugger.handle_error - A
    M 187:4 SoftDebugger.handle_warning - A
    M 190:4 SoftDebugger.wrap - A
Ancien/banque.py
    M 263:4 FenetreBanque.charger_etat_banque - B
    M 116:4 FenetreBanque.investir - B
    M 91:4 FenetreBanque.verifier_blocage_boutons - B
    C 6:0 FenetreBanque - A
    M 41:4 FenetreBanque.rembourser - A
    M 202:4 FenetreBanque.verifier_investissements - A
    M 221:4 FenetreBanque.sauvegarder_etat_banque - A
    M 245:4 FenetreBanque.afficher_banque - A
    F 294:0 afficher_banque - A
    M 72:4 FenetreBanque.emprunter - A
    M 8:4 FenetreBanque.__init__ - A
Ancien/table_de_conversion.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/horloge.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/Secure_save.py
    M 172:4 AutoSaver._loop - B
    F 139:0 load_from_slot - A
    C 162:0 AutoSaver - A
    F 31:0 log_save_event - A
    F 94:0 atomic_write_zip - A
    M 193:4 AutoSaver.start - A
    F 79:0 aesgcm_decrypt - A
    F 107:0 save_to_slot - A
    M 200:4 AutoSaver.stop - A
    F 57:0 normalize_password - A
    F 61:0 derive_key - A
    F 72:0 aesgcm_encrypt - A
    F 88:0 ensure_profile_dir - A
    M 163:4 AutoSaver.__init__ - A
Ancien/admin_manager.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
Ancien/generate_map.py
    F 1:0 generate_map - C
Ancien/inventaire.py
    ERROR: invalid non-printable character U+FEFF (<unknown>, line 1)
scripts/generate_problems_md.py
    F 10:0 generate_problems_md - C
scripts/update_database.py
    F 9:0 update_database - A
scripts/generate_dashboard.py
    F 123:0 generate_json - C
    F 88:0 calculate_quality - A
    F 12:0 get_documentation_score - A
    F 28:0 get_database_data - A
scripts/database_manager.py
    C 9:0 DatabaseManager - A
    M 333:4 DatabaseManager.add_run - A
    M 387:4 DatabaseManager.insert - A
    M 11:4 DatabaseManager.__init__ - A
    M 25:4 DatabaseManager.create_tables - A
    M 409:4 DatabaseManager.close - A
    M 411:4 DatabaseManager.add_security - A
    M 435:4 DatabaseManager.add_security_issue - A
scripts/documentation/python_docs.py
    F 9:0 check_python_docs - D
scripts/documentation/navigation.py
    F 1:0 check_navigation - A
scripts/documentation/report.py
    F 25:0 generate_report - C
    F 11:0 _status - B
scripts/documentation/score.py
    F 11:0 generate_score - B
scripts/documentation/markdown.py
    F 91:0 check_empty_files - B
    F 129:0 check_line_length - B
    F 146:0 check_trailing_spaces - B
    F 248:0 check_html - A
    F 44:0 get_markdown_files - A
    F 117:0 check_encoding - A
    F 163:0 check_code_blocks - A
    F 177:0 check_lists - A
    F 215:0 check_tables - A
    F 32:0 load_markdownlint_report - A
    F 56:0 check_markdown - A
scripts/documentation/problem.py
    F 3:0 add_problem - A
scripts/documentation/spelling.py
    F 4:0 check_spelling - A
scripts/documentation/titles.py
    F 90:0 check_heading_spacing - B
    F 66:0 check_heading_order - B
    F 131:0 check_title_length - A
    F 153:0 check_duplicate_titles - A
    F 113:0 check_empty_titles - A
    F 51:0 check_single_h1 - A
    F 16:0 check_titles - A
scripts/documentation/links.py
    F 93:0 check_local_links - B
    F 173:0 check_images - B
    F 123:0 check_external_links - A
    F 67:0 check_empty_links - A
    F 151:0 check_anchors - A
    F 208:0 check_duplicate_links - A
    F 50:0 extract_links - A
    F 16:0 check_links - A
scripts/documentation/organization.py
    F 1:0 check_organization - A
scripts/documentation/rust_docs.py
    F 1:0 check_rust_docs - A
scripts/database/utils.py
    F 5:0 read_report - A
    F 15:0 extract_int - A
    F 25:0 extract_float - A
scripts/database/update_docs.py
    F 7:0 update_docs_database - B
scripts/database/update_performance.py
    F 1:0 update_performance_database - A
scripts/database/update_rust.py
    F 19:0 update_rust_database - A
scripts/database/update_python.py
    F 18:0 update_python_database - A
scripts/database/update_security.py
    F 13:0 update_security_database - A

149 blocks (classes, functions, methods) analyzed.
Average complexity: A (3.402684563758389)
### Security
Run started:2026-07-20 00:43:14.307650+00:00

Test results:
>> Issue: [B110:try_except_pass] Try, Except, Pass detected.
   Severity: Low   Confidence: High
   CWE: CWE-703 (https://cwe.mitre.org/data/definitions/703.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b110_try_except_pass.html
   Location: ./Ancien/Secure_save.py:52:4
51	
52	    except Exception:
53	        # Le journal ne doit JAMAIS faire planter le jeu
54	        pass
55	

--------------------------------------------------
>> Issue: [B403:blacklist] Consider possible security implications associated with dill module.
   Severity: Low   Confidence: High
   CWE: CWE-502 (https://cwe.mitre.org/data/definitions/502.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_imports.html#b403-import-pickle
   Location: ./Ancien/admin_manager.py:12:0
11	from PySide6.QtWidgets import QMessageBox
12	import dill
13	

--------------------------------------------------
>> Issue: [B307:blacklist] Use of possibly insecure function - consider using safer ast.literal_eval.
   Severity: Medium   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b307-eval
   Location: ./Ancien/admin_manager.py:117:25
116	            try:
117	                result = eval(cmd, self.contexte)
118	                if result is not None:

--------------------------------------------------
>> Issue: [B102:exec_used] Use of exec detected.
   Severity: Medium   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b102_exec_used.html
   Location: ./Ancien/admin_manager.py:121:16
120	            except SyntaxError:
121	                exec(cmd, self.contexte)
122	        except Exception:

--------------------------------------------------
>> Issue: [B301:blacklist] Pickle and modules that wrap it can be unsafe when used to deserialize untrusted data, possible security issue.
   Severity: Medium   Confidence: High
   CWE: CWE-502 (https://cwe.mitre.org/data/definitions/502.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b301-pickle
   Location: ./Ancien/admin_manager.py:316:23
315	            try:
316	                data = dill.load(fichier)
317	            except :

--------------------------------------------------
>> Issue: [B301:blacklist] Pickle and modules that wrap it can be unsafe when used to deserialize untrusted data, possible security issue.
   Severity: Medium   Confidence: High
   CWE: CWE-502 (https://cwe.mitre.org/data/definitions/502.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b301-pickle
   Location: ./Ancien/admin_manager.py:386:23
385	            try:
386	                data = dill.load(fichier)
387	            except :

--------------------------------------------------
>> Issue: [B110:try_except_pass] Try, Except, Pass detected.
   Severity: Low   Confidence: High
   CWE: CWE-703 (https://cwe.mitre.org/data/definitions/703.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b110_try_except_pass.html
   Location: ./Ancien/debugger.py:39:4
38	            f.write(msg + "\n")
39	    except Exception:
40	        pass
41	

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/inventaire.py:155:16
154	    poids = POIDS_CATEGORIES
155	    categorie = random.choices(categories, weights=poids, k=1)[0]
156	

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/inventaire.py:159:9
158	    combinaisons = cache_enchantements[niveau][categorie]
159	    en = random.choice(combinaisons)
160	    return en,categorie

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/jet_de_des.py:3:15
2	def jet_de_des(face,nb):
3	    return sum(random.randint(1, face) for _ in range(nb))

--------------------------------------------------
>> Issue: [B403:blacklist] Consider possible security implications associated with dill module.
   Severity: Low   Confidence: High
   CWE: CWE-502 (https://cwe.mitre.org/data/definitions/502.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_imports.html#b403-import-pickle
   Location: ./Ancien/main.py:40:0
39	import json
40	import dill
41	from inv import afficher_inventaire

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:354:28
353	                **({"gemmes": 1} if de.jet_de_des(20, 1) >= 18 else {}),
354	                **({"pain": random.randint(3, 5)} if de.jet_de_des(20, 1) >= 4 else {}),
355	            },

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:432:44
431	                **(
432	                    {"livre enchant niv 1": random.randint(1, 9)}
433	                    if de.jet_de_des(20, 1) >= 20

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:440:44
439	                **(
440	                    {"livre enchant niv 1": random.randint(1, 9)}
441	                    if de.jet_de_des(20, 1) >= 18

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:448:44
447	                **(
448	                    {"livre enchant niv 1": random.randint(1, 9)}
449	                    if de.jet_de_des(20, 1) >= 16

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:456:44
455	                **(
456	                    {"livre enchant niv 1": random.randint(1, 9)}
457	                    if de.jet_de_des(20, 1) >= 14

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:464:44
463	                **(
464	                    {"livre enchant niv 1": random.randint(1, 9)}
465	                    if de.jet_de_des(20, 1) >= 12

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:472:44
471	                **(
472	                    {"livre enchant niv 1": random.randint(1, 9)}
473	                    if de.jet_de_des(20, 1) >= 10

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:480:44
479	                **(
480	                    {"livre enchant niv 1": random.randint(1, 9)}
481	                    if de.jet_de_des(20, 1) >= 8

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:487:22
486	        self.quantite_objets = {
487	            "cuivre": random.randint(2, 9),
488	            "fer": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:488:19
487	            "cuivre": random.randint(2, 9),
488	            "fer": random.randint(2, 9),
489	            "lapiz": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:489:21
488	            "fer": random.randint(2, 9),
489	            "lapiz": random.randint(2, 9),
490	            "or": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:490:18
489	            "lapiz": random.randint(2, 9),
490	            "or": random.randint(2, 9),
491	            "redstone": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:491:24
490	            "or": random.randint(2, 9),
491	            "redstone": random.randint(2, 9),
492	            "netherite": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:492:25
491	            "redstone": random.randint(2, 9),
492	            "netherite": random.randint(2, 9),
493	            "diamant": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:493:23
492	            "netherite": random.randint(2, 9),
493	            "diamant": random.randint(2, 9),
494	            "balles": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:494:22
493	            "diamant": random.randint(2, 9),
494	            "balles": random.randint(2, 9),
495	            "carreau d'arbalète ": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:495:36
494	            "balles": random.randint(2, 9),
495	            "carreau d'arbalète ": random.randint(2, 9),
496	            "chargeur": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:496:24
495	            "carreau d'arbalète ": random.randint(2, 9),
496	            "chargeur": random.randint(2, 9),
497	            "flèches communes": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:497:33
496	            "chargeur": random.randint(2, 9),
497	            "flèches communes": random.randint(2, 9),
498	            "flèches peu rares": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:498:34
497	            "flèches communes": random.randint(2, 9),
498	            "flèches peu rares": random.randint(2, 9),
499	            "flèches rares": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:499:30
498	            "flèches peu rares": random.randint(2, 9),
499	            "flèches rares": random.randint(2, 9),
500	            "flèches super rares": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:500:36
499	            "flèches rares": random.randint(2, 9),
500	            "flèches super rares": random.randint(2, 9),
501	            "flèches exotiques": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:501:34
500	            "flèches super rares": random.randint(2, 9),
501	            "flèches exotiques": random.randint(2, 9),
502	            "flèches épiques": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:502:33
501	            "flèches exotiques": random.randint(2, 9),
502	            "flèches épiques": random.randint(2, 9),
503	            "flèches légendaire": random.randint(2, 9),

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:503:36
502	            "flèches épiques": random.randint(2, 9),
503	            "flèches légendaire": random.randint(2, 9),
504	

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:844:16
843	            total = sum(ch for _, ch in table)
844	            r = random.uniform(0, total)
845	            cumul = 0

--------------------------------------------------
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b311-random
   Location: ./Ancien/tresor.py:887:12
886	        total = sum(ch for _, ch in table)
887	        r = random.uniform(0, total)
888	        cumul = 0

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   CWE: CWE-89 (https://cwe.mitre.org/data/definitions/89.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b608_hardcoded_sql_expressions.html
   Location: ./scripts/database_manager.py:393:16
392	        self.cursor.execute(
393	            f"""
394	            INSERT INTO {table}
395	            ({columns})
396	            VALUES ({placeholders})
397	            """,
398	            tuple(values.values())

--------------------------------------------------
>> Issue: [B112:try_except_continue] Try, Except, Continue detected.
   Severity: Low   Confidence: High
   CWE: CWE-703 (https://cwe.mitre.org/data/definitions/703.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b112_try_except_continue.html
   Location: ./scripts/documentation/markdown.py:134:8
133	            lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
134	        except Exception:
135	            continue
136	        for i, line in enumerate(lines, 1):

--------------------------------------------------
>> Issue: [B112:try_except_continue] Try, Except, Continue detected.
   Severity: Low   Confidence: High
   CWE: CWE-703 (https://cwe.mitre.org/data/definitions/703.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b112_try_except_continue.html
   Location: ./scripts/documentation/markdown.py:151:8
150	            lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
151	        except Exception:
152	            continue
153	        for i, line in enumerate(lines,1):

--------------------------------------------------
>> Issue: [B112:try_except_continue] Try, Except, Continue detected.
   Severity: Low   Confidence: High
   CWE: CWE-703 (https://cwe.mitre.org/data/definitions/703.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b112_try_except_continue.html
   Location: ./scripts/documentation/markdown.py:168:8
167	            text=file.read_text(encoding="utf-8",errors="ignore")
168	        except Exception:
169	            continue
170	        if text.count("```") %2:

--------------------------------------------------
>> Issue: [B112:try_except_continue] Try, Except, Continue detected.
   Severity: Low   Confidence: High
   CWE: CWE-703 (https://cwe.mitre.org/data/definitions/703.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b112_try_except_continue.html
   Location: ./scripts/documentation/markdown.py:253:8
252	            text=file.read_text(encoding="utf-8",errors="ignore")
253	        except Exception:
254	            continue
255	        for tag in HTML_TAGS:

--------------------------------------------------
>> Issue: [B608:hardcoded_sql_expressions] Possible SQL injection vector through string-based query construction.
   Severity: Medium   Confidence: Medium
   CWE: CWE-89 (https://cwe.mitre.org/data/definitions/89.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b608_hardcoded_sql_expressions.html
   Location: ./voir_database.py:38:21
37	    # Données
38	    cursor.execute(f"SELECT * FROM {table}")
39	    rows = cursor.fetchall()

--------------------------------------------------

Code scanned:
	Total lines of code: 6694
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 38
		Medium: 6
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 2
		High: 42
Files skipped (0):
## Tests Pytest
Aucun dossier tests trouvé
