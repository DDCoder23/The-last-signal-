import os
import re
from typing import Dict, List, Any

def check_rust_docs() -> Dict[str, Any]:
    """
    Vérifie la qualité de la documentation dans les fichiers Rust.
    Retourne un score en entier (0-100).

    Returns:
        Dict avec:
        - score: Note globale (0-100) en INT
        - max_score: Score maximum possible (100)
        - results: Détails par fichier
        - problems: Liste des problèmes trouvés
    """
    rust_files = []
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    exclude_dirs = {'target', '.git', '__pycache__', 'venv'}
    
    # Trouve tous les fichiers .rs 
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.rs'):
                rust_files.append(os.path.join(root, file))
    print(rust_files)
    if not rust_files:
        return {
            "score": 0,  
            "max_score": 100,
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
                    if match:
                        # ✅ Extraction correcte du nom
                        if element_type == 'function':
                            # Pour les fonctions : extrait le nom entre 'fn' et '('
                            name_match = re.match(r'^\s*(pub\s+)?fn\s+(\w+)', line)
                            element_name = name_match.group(2) if name_match else "unknown"
                        else:
                            parts = line.split()
                            
                    else:
                        # Pour struct/enum/mod/trait : dernier mot du pattern
                        element_name = parts[1] if len(parts) > 1 else "unknown"

                    
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
                            problems.append({
                                    "file": file_path,
                                    "line": i + 1,
                                    "severity": "warning",
                                    "message": f"{element_type.capitalize()} '{element_name}' sans documentation",
                                    "suggestion": f"Ajoutez /// avant cette {element_type}"
                            })

        


            if file_problems:
                problems.extend(file_problems)

    # Calcul du score en pourcentage (0-100)
    if total_elements > 0:
        score = max(0, 100 - (total_issues * 100 / total_elements))
    else:
        score = 100

    return {
        "score": int(score),  # ✅ Score en INT (0-100)
        "max_score": 100,      # ✅ Max score en INT
        "results": {
            "files_checked": len(rust_files),
            "total_elements": total_elements,
            "elements_without_docs": total_issues
        },
        "problems": problems
    }
