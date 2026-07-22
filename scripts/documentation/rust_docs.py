import os
import re
from typing import Dict, List, Any
from pathlib import Path
max_score=30
def check_rust_docs() -> Dict[str, Any]:
    """
    Vérifie la qualité de la documentation dans les fichiers Rust.

    Returns:
        Dict avec:
        - score: Note globale 
        - max_score: Score maximum possible 
        - results: Détails par fichier
        - problems: Liste des problèmes trouvés
    """
    rust_files = []
    base_dir = Path.cwd()
    exclude_dirs = {'target', '.git', '__pycache__', 'venv'}
    
    # Trouve tous les fichiers .rs 
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.rs'):
                rust_files.append(os.path.join(root, file))
    print( "fichier:")
    print(rust_files)
    if not rust_files:
        return {
            "score": 0,  
            "max_score": max_score,
            "results": {"files_checked": 0},
            "problems": []
        }

    problems: List[Dict[str, Any]] = []
    total_issues = 0
    total_elements = 0  # Nombre total d'éléments vérifiés
    patterns = {
    'function': r'^\s*(pub\s+)?fn\s+\w+\s*\([^)]*\)',
    'struct': r'^\s*(pub\s+)?struct\s+\w+',
    'enum': r'^\s*(pub\s+)?enum\s+\w+',
    'impl': r'^\s*impl\s+[\w<>=, ]+',
    'mod': r'^\s*(pub\s+)?mod\s+\w+',
    'trait': r'^\s*(pub\s+)?trait\s+\w+'
    }
    score=max_score
    for file_path in rust_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            file_problems = []
            file_elements = 0
            # Patterns pour détecter les éléments Rust publics
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:  
                    # ✅ Ignore les lignes vides
                    continue
                
                for element_type, pattern in patterns.items():
                    match = re.match(pattern, line)
                    print(match)
                    if not match:
                        continue
                    else:
                        # Cherche et extrait le nom
                        name_match = re.search(patterns[element_type], line)
                        element_name = name_match.group(1) if name_match else "unknown"
                        total_elements += 1
                        has_doc = False
                        if i > 0:
                            prev_line = lines[i-1].strip()
                            if (prev_line.startswith('///') or 
                                prev_line.startswith('/**') or 
                                prev_line.startswith('/*!')):
                                has_doc = True
                        if not has_doc:
                            total_issues += 1
                            score-=1
                            problems.append({
                                    "file": file_path,
                                    "line": i + 1,
                                    "severity": "warning",
                                    "message": f"{element_type.capitalize()} '{element_name}' sans documentation",
                                    "suggestion": f"Ajoutez /// avant cette {element_type}"
                            })
                        break
                    

        


            if file_problems:
                problems.extend(file_problems)

    # Calcul du score en pourcentage (0-20)


    return {
        "score": int(score),
        "max_score": max_score,      
        "results": {
            "files_checked": len(rust_files),
            "total_elements": total_elements,
            "elements_without_docs": total_issues
        },
        "problems": problems
    }
