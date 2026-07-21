from pathlib import Path
import re


def check_rust_docs():
    rs_files = list(Path(".").rglob("*.rs"))

    result = {
        "score": 0,
        "max_score": 100,
        "results": {},
        "problems": []
    }

    if not rs_files:
        result["results"]["files"] = 0
        return result

    total_pub_fn = 0
    documented_pub_fn = 0

    total_struct = 0
    documented_struct = 0

    total_enum = 0
    documented_enum = 0

    total_trait = 0
    documented_trait = 0

    module_docs = 0
    examples = 0

    for file in rs_files:

        lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()

        if any(line.startswith("//!") for line in lines[:20]):
            module_docs += 1

        for i, line in enumerate(lines):

            stripped = line.strip()

            if "```rust" in stripped:
                examples += 1

            if re.match(r"pub\s+fn\s+", stripped):
                total_pub_fn += 1

                if i > 0 and lines[i-1].strip().startswith("///"):
                    documented_pub_fn += 1
                else:
                    result["problems"].append({
                        "file": str(file),
                        "severity": "warning",
                        "message": f"Fonction publique non documentée : {stripped}"
                    })

            elif re.match(r"pub\s+struct\s+", stripped):
                total_struct += 1

                if i > 0 and lines[i-1].strip().startswith("///"):
                    documented_struct += 1
                else:
                    result["problems"].append({
                        "file": str(file),
                        "severity": "warning",
                        "message": f"Structure publique non documentée : {stripped}"
                    })

            elif re.match(r"pub\s+enum\s+", stripped):
                total_enum += 1

                if i > 0 and lines[i-1].strip().startswith("///"):
                    documented_enum += 1
                else:
                    result["problems"].append({
                        "file": str(file),
                        "severity": "warning",
                        "message": f"Enum publique non documentée : {stripped}"
                    })

            elif re.match(r"pub\s+trait\s+", stripped):
                total_trait += 1

                if i > 0 and lines[i-1].strip().startswith("///"):
                    documented_trait += 1
                else:
                    result["problems"].append({
                        "file": str(file),
                        "severity": "warning",
                        "message": f"Trait public non documenté : {stripped}"
                    })

    def ratio(done, total):
        if total == 0:
            return 1
        return done / total

    score = 0

    score += ratio(documented_pub_fn, total_pub_fn) * 40
    score += ratio(documented_struct, total_struct) * 20
    score += ratio(documented_enum, total_enum) * 10
    score += ratio(documented_trait, total_trait) * 10

    if module_docs == len(rs_files):
        score += 10
    elif rs_files:
        score += 10 * module_docs / len(rs_files)

    if examples > 0:
        score += 10

    result["score"] = round(score)

    result["results"] = {
        "files": len(rs_files),
        "pub_functions": f"{documented_pub_fn}/{total_pub_fn}",
        "pub_structs": f"{documented_struct}/{total_struct}",
        "pub_enums": f"{documented_enum}/{total_enum}",
        "pub_traits": f"{documented_trait}/{total_trait}",
        "modules_documented": f"{module_docs}/{len(rs_files)}",
        "examples": examples
    }

    return result
