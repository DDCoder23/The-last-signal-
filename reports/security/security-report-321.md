# Security Report

Date : Sat Jul 18 21:02:44 UTC 2026

## Bandit
[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.13.14
Run started:2026-07-18 21:02:44.907370+00:00

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
	Total lines of code: 6633
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 38
		Medium: 5
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 1
		High: 42
Files skipped (0):

## pip-audit
Found 4 known vulnerabilities in 2 packages
Name  Version ID              Fix Versions
----- ------- --------------- ------------
click 8.1.8   PYSEC-2026-2132 8.3.3
mcp   1.23.3  CVE-2026-52870  1.27.2
mcp   1.23.3  CVE-2026-52869  1.27.2
mcp   1.23.3  CVE-2026-59950  1.28.1

## Safety
/opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages/safety/auth/main.py:5: AuthlibDeprecationWarning: authlib.jose module is deprecated, please use joserfc instead.
It will be compatible before version 2.0.0.
  from authlib.jose.errors import ExpiredTokenError


[33m[1m+===========================================================================================================================================================================================+[0m


[31m[1mDEPRECATED: [0m[33m[1mthis command (`check`) has been DEPRECATED, and will be unsupported beyond 01 June 2024.[0m


[32mWe highly encourage switching to the new [0m[32m[1m`scan`[0m[32m command which is easier to use, more powerful, and can be set up to mimic the deprecated command if required.[0m


[33m[1m+===========================================================================================================================================================================================+[0m


+==============================================================================+

                               /$$$$$$            /$$
                              /$$__  $$          | $$
           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$
          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$
         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$
          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$
          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$
         |_______/  \_______/|__/     \_______/   \___/   \____  $$
                                                          /$$  | $$
                                                         |  $$$$$$/
  by safetycli.com                                        \______/

+==============================================================================+

 [1mREPORT[0m 

  Safety [1mv3.8.1[0m is scanning for [1mVulnerabilities[0m[1m...[0m
[1m  Scanning dependencies[0m in your [1menvironment:[0m

  -> /opt/hostedtoolcache/Python/3.13.14/x64/lib/python3.13/site-packages

  Using [1mopen-source vulnerability database[0m
[1m  Found and scanned 110 packages[0m
  Timestamp [1m2026-07-18 21:02:52[0m
[1m  0[0m[1m vulnerabilities reported[0m
[1m  0[0m[1m vulnerabilities ignored[0m
+==============================================================================+

 [32m[1mNo known security vulnerabilities reported.[0m 

+==============================================================================+[0m


[33m[1m+===========================================================================================================================================================================================+[0m


[31m[1mDEPRECATED: [0m[33m[1mthis command (`check`) has been DEPRECATED, and will be unsupported beyond 01 June 2024.[0m


[32mWe highly encourage switching to the new [0m[32m[1m`scan`[0m[32m command which is easier to use, more powerful, and can be set up to mimic the deprecated command if required.[0m


[33m[1m+===========================================================================================================================================================================================+[0m



## cargo-audit
[0m[0m[1m[32m    Fetching[0m advisory database from `https://github.com/RustSec/advisory-db.git`
[0m[0m[1m[32m      Loaded[0m 1166 security advisories (from /home/runner/.cargo/advisory-db)
[0m[0m[1m[32m    Updating[0m crates.io index
[0m[0m[1m[31merror:[0m not found: Couldn't load Cargo.lock
Caused by:
  -> I/O operation failed: I/O operation failed: entity not found
  -> I/O operation failed: entity not found

## Semgrep
               
               
┌─────────────┐
│ Scan Status │
└─────────────┘
  Scanning 41 files tracked by git with 1074 Code rules:
                                                                                                                        
  Language      Rules   Files          Origin      Rules                                                                
 ─────────────────────────────        ───────────────────                                                               
  <multilang>      60      41          Community    1074                                                                
  python          243      24                                                                                           
  json              4       1                                                                                           
  rust              4       1                                                                                           
  html              1       1                                                                                           
                                                                                                                        
                
                
┌──────────────┐
│ Scan Summary │
└──────────────┘
✅ Scan completed successfully.
 • Findings: 0 (0 blocking)
 • Rules run: 310
 • Targets scanned: 41
 • Parsed lines: ~100.0%
 • Scan skipped: 
   ◦ Files matching .semgrepignore patterns: 2
 • Scan was limited to files tracked by git
 • For a detailed list of skipped files and lines, run semgrep with the --verbose flag
Ran 310 rules on 41 files: 0 findings.
(need more rules? `semgrep login` for additional free Semgrep Registry rules)

If Semgrep missed a finding, please send us feedback to let us know!
See https://semgrep.dev/docs/reporting-false-negatives/

## Gitleaks

    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

[90m9:03PM[0m [32mINF[0m [1m1805 commits scanned.[0m
[90m9:03PM[0m [32mINF[0m [1mscanned ~43560215 bytes (43.56 MB) in 1.48s[0m
[90m9:03PM[0m [32mINF[0m [1mno leaks found[0m

## Python Licenses
 Name                                      Version    License                              
 Authlib                                   1.7.2      BSD License                          
 CacheControl                              0.14.4     Apache-2.0                           
 Jinja2                                    3.1.6      BSD License                          
 MarkupSafe                                3.0.3      BSD-3-Clause                         
 PyJWT                                     2.13.0     MIT                                  
 PyYAML                                    6.0.3      MIT License                          
 Pygments                                  2.20.0     BSD-2-Clause                         
 annotated-doc                             0.0.4      MIT                                  
 annotated-types                           0.7.0      MIT License                          
 anyio                                     4.14.2     MIT                                  
 attrs                                     26.1.0     MIT                                  
 bandit                                    1.9.4      Apache-2.0                           
 boltons                                   21.0.0     BSD License                          
 boolean.py                                5.0        BSD-2-Clause                         
 bracex                                    3.0        MIT                                  
 certifi                                   2026.6.17  Mozilla Public License 2.0 (MPL 2.0) 
 cffi                                      2.1.0      MIT-0                                
 charset-normalizer                        3.4.9      MIT                                  
 click                                     8.1.8      BSD License                          
 click-option-group                        0.5.9      BSD-3-Clause                         
 colorama                                  0.4.6      BSD License                          
 cryptography                              49.0.0     Apache-2.0 OR BSD-3-Clause           
 cyclonedx-python-lib                      11.11.0    Apache Software License              
 defusedxml                                0.7.1      Python Software Foundation License   
 dparse                                    0.6.4      MIT License                          
 exceptiongroup                            1.2.2      MIT License                          
 face                                      26.0.1     UNKNOWN                              
 filelock                                  3.31.0     MIT                                  
 glom                                      25.12.0    BSD License                          
 googleapis-common-protos                  1.75.0     Apache Software License              
 h11                                       0.16.0     MIT License                          
 httpcore                                  1.0.9      BSD-3-Clause                         
 httpx                                     0.28.1     BSD License                          
 httpx-sse                                 0.4.3      MIT                                  
 idna                                      3.18       BSD-3-Clause                         
 importlib_metadata                        8.7.1      Apache-2.0                           
 iniconfig                                 2.3.0      MIT                                  
 joblib                                    1.5.3      BSD-3-Clause                         
 joserfc                                   1.7.3      BSD License                          
 jsonschema                                4.25.1     MIT                                  
 jsonschema-specifications                 2025.9.1   MIT                                  
 license-expression                        30.4.4     Apache-2.0                           
 markdown-it-py                            4.2.0      MIT License                          
 marshmallow                               4.3.0      MIT                                  
 mcp                                       1.23.3     MIT License                          
 mdurl                                     0.1.2      MIT License                          
 msgpack                                   1.2.1      Apache-2.0                           
 nltk                                      3.10.0     Apache Software License              
 opentelemetry-api                         1.37.0     Apache-2.0                           
 opentelemetry-exporter-otlp-proto-common  1.37.0     Apache-2.0                           
 opentelemetry-exporter-otlp-proto-http    1.37.0     Apache-2.0                           
 opentelemetry-instrumentation             0.58b0     Apache-2.0                           
 opentelemetry-instrumentation-requests    0.58b0     Apache-2.0                           
 opentelemetry-instrumentation-threading   0.58b0     Apache-2.0                           
 opentelemetry-proto                       1.37.0     Apache-2.0                           
 opentelemetry-sdk                         1.37.0     Apache-2.0                           
 opentelemetry-semantic-conventions        0.58b0     Apache-2.0                           
 opentelemetry-util-http                   0.58b0     Apache-2.0                           
 packageurl-python                         0.17.6     MIT License                          
 packaging                                 26.2       Apache-2.0 OR BSD-2-Clause           
 peewee                                    3.19.0     UNKNOWN                              
 pip-api                                   0.0.34     Apache Software License              
 pip-requirements-parser                   32.0.1     MIT                                  
 pip_audit                                 2.10.1     Apache Software License              
 platformdirs                              4.10.1     MIT                                  
 pluggy                                    1.6.0      MIT License                          
 protobuf                                  6.33.6     3-Clause BSD License                 
 py-serializable                           2.1.0      Apache Software License              
 pycparser                                 3.0        BSD-3-Clause                         
 pydantic                                  2.13.4     MIT                                  
 pydantic-settings                         2.14.2     MIT                                  
 pydantic_core                             2.46.4     MIT                                  
 pyparsing                                 3.3.2      MIT                                  
 pytest                                    9.1.1      MIT                                  
 python-dotenv                             1.2.2      BSD-3-Clause                         
 python-multipart                          0.0.32     Apache-2.0                           
 referencing                               0.37.0     MIT                                  
 regex                                     2026.7.10  Apache-2.0 AND CNRI-Python           
 requests                                  2.34.2     Apache Software License              
 rich                                      15.0.0     MIT License                          
 rpds-py                                   2026.6.3   MIT                                  
 ruamel.yaml                               0.19.1     MIT License                          
 ruamel.yaml.clib                          0.2.15     MIT License                          
 safety                                    3.8.1      MIT                                  
 safety-schemas                            0.0.16     MIT License                          
 semantic-version                          2.10.0     BSD License                          
 semgrep                                   1.170.0    LGPL-2.1-or-later                    
 shellingham                               1.5.4      ISC License (ISCL)                   
 sortedcontainers                          2.4.0      Apache Software License              
 sse-starlette                             3.4.5      BSD-3-Clause                         
 starlette                                 1.3.1      BSD-3-Clause                         
 stevedore                                 5.9.0      Apache-2.0                           
 tenacity                                  9.1.4      Apache Software License              
 tomli                                     2.4.1      MIT                                  
 tomli_w                                   1.2.0      MIT License                          
 tomlkit                                   0.15.1     MIT License                          
 tqdm                                      4.69.0     MPL-2.0 AND MIT                      
 truststore                                0.10.4     MIT                                  
 typer                                     0.23.1     MIT                                  
 typing-inspection                         0.4.2      MIT                                  
 typing_extensions                         4.16.0     PSF-2.0                              
 urllib3                                   2.7.0      MIT                                  
 uvicorn                                   0.51.0     BSD-3-Clause                         
 wcmatch                                   8.5.2      MIT                                  
 wrapt                                     1.17.3     BSD License                          
 zipp                                      4.1.0      MIT                                  

## Cargo Deny
2026-07-18 21:03:02 [[31mERROR[0m] the directory /home/runner/work/The-last-signal-/The-last-signal- doesn't contain a Cargo.toml file[0m

## Outdated Python packages
Package                                  Version Latest Type
---------------------------------------- ------- ------ -----
boltons                                  21.0.0  26.1.0 wheel
click                                    8.1.8   8.4.2  wheel
exceptiongroup                           1.2.2   1.3.1  wheel
importlib_metadata                       8.7.1   9.0.0  wheel
jsonschema                               4.25.1  4.26.0 wheel
mcp                                      1.23.3  1.28.1 wheel
opentelemetry-api                        1.37.0  1.44.0 wheel
opentelemetry-exporter-otlp-proto-common 1.37.0  1.44.0 wheel
opentelemetry-exporter-otlp-proto-http   1.37.0  1.44.0 wheel
opentelemetry-proto                      1.37.0  1.44.0 wheel
opentelemetry-sdk                        1.37.0  1.44.0 wheel
peewee                                   3.19.0  4.2.6  wheel
protobuf                                 6.33.6  7.35.1 wheel
pydantic_core                            2.46.4  2.47.0 wheel
safety-schemas                           0.0.16  0.0.18 wheel
typer                                    0.23.1  0.27.0 wheel
wcmatch                                  8.5.2   11.0   wheel
wrapt                                    1.17.3  2.2.2  wheel

## Outdated Rust crates
error: could not find `Cargo.toml` in `/home/runner/work/The-last-signal-/The-last-signal-` or any parent directory

# Global Security Score

| Level | Count |
|-------|------:|
| Critical | 0 |
| High | 46 |
| Medium | 7 |
| Low | 41 |

## Score : 0/100
No security database script found.
