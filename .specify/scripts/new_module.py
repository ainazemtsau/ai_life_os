#!/usr/bin/env python3
from __future__ import annotations
import sys, argparse, pathlib, datetime, json

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

REPO = pathlib.Path(__file__).resolve().parents[2]
REG = REPO/".specify/memory/public/registry.yaml"

def load_registry():
    if not REG.exists():
        raise SystemExit("registry.yaml not found")
    text = REG.read_text(encoding="utf-8")
    if REG.suffix in (".yaml",".yml"):
        if yaml is None:
            raise SystemExit("PyYAML not installed; cannot parse YAML.")
        return yaml.safe_load(text)
    import json as _json
    return _json.loads(text)

def dump_registry(data):
    if REG.suffix in (".yaml",".yml"):
        if yaml is None:
            raise SystemExit("PyYAML not installed; cannot dump YAML.")
        REG.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    else:
        import json as _json
        REG.write_text(_json.dumps(data, indent=2), encoding="utf-8")

def render_template(path: pathlib.Path, **ctx) -> str:
    t = path.read_text(encoding="utf-8")
    for k,v in ctx.items():
        t = t.replace(f"{{{{{k}}}}}", str(v))
    return t

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, help="module id, e.g. backend.repo")
    p.add_argument("--kind", choices=["python","typescript"], required=True)
    p.add_argument("--uses", default="", help="comma-separated module ids this module depends on")
    p.add_argument("--semver", default="0.1.0")
    args = p.parse_args()

    mid = args.id
    side, _, name = mid.partition(".")
    if not side or not name:
        raise SystemExit("module id must be in form 'side.name'")

    reg = load_registry()
    if reg.get("version") != 1:
        raise SystemExit("registry version must be 1")
    modules = reg.setdefault("modules", {})
    if mid in modules:
        raise SystemExit(f"module '{mid}' already exists in registry")

    # paths
    manifest_path = REPO/".specify/memory/public"/f"{mid}.api.md"
    if args.kind == "python":
        contract_path = REPO/"backend/src/ai_life_backend/contracts"/f"{name}_contracts.py"
        allowed = [f"backend/src/ai_life_backend/{name}/**", f"backend/tests/{name}/**"]
        import_hint = f"from ai_life_backend.{name}.public import {name}"
        # create dirs
        (REPO/f"backend/src/ai_life_backend/{name}").mkdir(parents=True, exist_ok=True)
        (REPO/f"backend/tests/{name}").mkdir(parents=True, exist_ok=True)
    else:
        contract_path = REPO/"frontend/src/contracts"/f"{name}.d.ts"
        allowed = [f"frontend/src/features/{name}/**", f"frontend/src/contracts/{name}.d.ts"]
        import_hint = f"import * as {name} from '@/features/{name}'"
        (REPO/f"frontend/src/features/{name}").mkdir(parents=True, exist_ok=True)
        (REPO/"frontend/src/contracts").mkdir(parents=True, exist_ok=True)

    # write manifest from template
    man_tpl = REPO/".specify/templates/public_manifest_template.md"
    manifest_path.write_text(
        render_template(
            man_tpl,
            module_id=mid,
            semver=args.semver,
            lang="ts" if args.kind=="typescript" else "py",
            usage_example="// fill later" if args.kind=="typescript" else "# fill later",
        ),
        encoding="utf-8",
    )

    # write contract from template
    if args.kind=="typescript":
        tpl = REPO/".specify/templates/contracts/ts_contract_template.d.ts"
    else:
        tpl = REPO/".specify/templates/contracts/python_protocol_template.py"
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text(render_template(tpl, module_id=mid), encoding="utf-8")

    # update registry
    uses = [u.strip() for u in args.uses.split(",") if u.strip()]
    modules[mid] = {
        "kind": args.kind,
        "semver": args.semver,
        "manifest": str(manifest_path.relative_to(REPO)).replace("\\","/"),
        "contract": str(contract_path.relative_to(REPO)).replace("\\","/"),
        "import_hint": import_hint,
        "allowed_dirs": allowed,
        "uses": uses,
        "notes": "",
    }
    dump_registry(reg)
    print(json.dumps({"ok": True, "created": mid, "manifest": str(manifest_path), "contract": str(contract_path)}))

if __name__ == "__main__":
    main()
