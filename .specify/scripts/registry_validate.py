#!/usr/bin/env python3
import sys, json, re, pathlib

try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # allow JSON fallback

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+].*)?$")

def err(msg: str) -> None:
    print(f"[registry_validate] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def load_yaml_or_json(p: pathlib.Path):
    text = p.read_text(encoding="utf-8")
    if p.suffix in (".yaml", ".yml"):
        if yaml is None:
            err("PyYAML not installed. Install it (e.g., backend: uv add -D pyyaml) or use JSON.")
        return yaml.safe_load(text)
    import json as _json
    return _json.loads(text)

def main() -> None:
    repo = pathlib.Path(__file__).resolve().parents[2]
    reg_path = repo / ".specify" / "memory" / "public" / "registry.yaml"
    if not reg_path.exists():
        err("registry.yaml not found")
    data = load_yaml_or_json(reg_path)

    if data.get("version") != 1:
        err("registry version must be 1")

    modules = data.get("modules")
    if modules is None:
        err("modules missing (must be dict)")

    if not isinstance(modules, dict):
        err("modules must be a dict")

    for mid, m in modules.items():
        for k in ("kind", "semver", "manifest", "contract", "import_hint", "allowed_dirs", "uses"):
            if m.get(k) in (None, []):
                err(f"{mid}: missing or empty '{k}'")
        if not SEMVER_RE.match(m["semver"]):
            err(f"{mid}: invalid semver '{m['semver']}'")
        man = repo / m["manifest"]
        con = repo / m["contract"]
        if not man.exists():
            err(f"{mid}: manifest not found at {man}")
        if not con.exists():
            err(f"{mid}: contract not found at {con}")
        # allowed_dirs exist? (we just check that parent dirs exist)
        for g in m["allowed_dirs"]:
            root = repo / g.split("/")[0]
            if not (root.exists() or str(root) == "."):
                err(f"{mid}: allowed_dirs root '{root}' not found")

    print(json.dumps({"ok": True, "modules": list(modules.keys())}))

if __name__ == "__main__":
    main()
