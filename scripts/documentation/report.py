from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import Any

REPORT_DIR=Path("reports/docs")
REPORT_DIR.mkdir(parents=True,exist_ok=True)

def _status(score:int)->str:
    if score>=90:return "ðŸŸ¢ Excellent"
    if score>=80:return "ðŸŸ¢ TrÃ¨s bon"
    if score>=70:return "ðŸŸ¡ Bon"
    if score>=60:return "ðŸŸ  Moyen"
    return "ðŸ”´ Ã€ amÃ©liorer"

def _flatten(details:dict[str,Any])->list[dict]:
    out=[]
    for module,result in details.items():
        for p in result.get("problems",[]):
            x=dict(p);x.setdefault("module",module);out.append(x)
    return out

def generate_report(total:int,scores:dict[str,int],details:dict[str,Any])->None:
    REPORT_DIR.mkdir(parents=True,exist_ok=True)
    problems=_flatten(details)
    summary={"generated":datetime.now().isoformat(),"score":total,"status":_status(total),"scores":scores,"problem_count":len(problems)}
    (REPORT_DIR/"score.txt").write_text(str(total),encoding="utf-8")
    (REPORT_DIR/"summary.json").write_text(json.dumps(summary,indent=4,ensure_ascii=False),encoding="utf-8")
    (REPORT_DIR/"score.json").write_text(json.dumps({**summary,"details":details},indent=4,ensure_ascii=False),encoding="utf-8")
    (REPORT_DIR/"problems.json").write_text(json.dumps(problems,indent=4,ensure_ascii=False),encoding="utf-8")
    md=["# ðŸ“Š Documentation Quality Report\n\n",f"**Date :** {datetime.now():%Y-%m-%d %H:%M:%S}\n\n",f"# {total}/100\n\n",f"**Statut :** {_status(total)}\n\n","## RÃ©sultats\n|Module|Score|\n|---|---:|\n"]
    for k,v in scores.items(): md.append(f"|{k}|**{v}**|\n")
    md.append("\n## ProblÃ¨mes\n")
    if problems:
        for p in problems:
            md.append(f"- [{p.get('severity','info').upper()}] `{p.get('module')}` `{p.get('file')}` : {p.get('message')}\n")
    else:
        md.append("Aucun problÃ¨me dÃ©tectÃ©.\n")
    (REPORT_DIR/"score.md").write_text("".join(md),encoding="utf-8")
    p=["# ðŸ“‹ ProblÃ¨mes\n\n"]
    for pr in problems:
        p.append(f"## {pr.get('module')}\n- {pr.get('file')}\n- {pr.get('severity')}\n- {pr.get('message')}\n\n")
    (REPORT_DIR/"problems.md").write_text("".join(p),encoding="utf-8")
