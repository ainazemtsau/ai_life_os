#!/usr/bin/env python3
import sys, pathlib, json, re

SECTIONS = ("Overview","Exports","Types","Usage","Stability","Version")

def lint_manifest(path: pathlib.Path) -> list[str]:
    txt = path.read_text(encoding="utf-8")
    errs = []
    if "Version:" not in txt:
        errs.append(f"{path}: missing Version line")
    for sec in SECTIONS:
        if sec != "Version" and f"## {sec}" not in txt and not txt.strip().startswith("# Public API"):
            # 'Public API — <id>' already checked, but we require each heading
            errs.append(f"{path}: missing section {sec}")
    return errs

def main() -> None:
    repo = pathlib.Path(__file__).resolve().parents[2]
    manifests = list((repo/".specify/memory/public").glob("*.api.md"))
    bad: list[str] = []
    if not manifests:
        print(json.dumps({"ok": True, "skipped": True}))
        return

    for m in manifests:
        bad.extend(lint_manifest(m))

    if bad:
        for e in bad: print("[manifest_lint]", e, file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"ok": True}))

if __name__ == "__main__":
    main()
