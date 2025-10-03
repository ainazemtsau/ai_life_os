#!/usr/bin/env python3
"""
Fan-out global tasks by module into per-module scaffolds.

Usage:
  python .specify/scripts/fanout_tasks.py <feature_id> [--tasks PATH] [--outdir PATH]

Behavior:
- Parse `.specify/specs/<feature_id>/tasks.md` (or --tasks).
- Collect checkbox items; detect module by:
    (a) @module(<name>) tag, or
    (b) path-based hints in the line (backend/, frontend/, api/, repo/, ios/, android/).
- For each <module>, create/update:
    .specify/specs/<feature_id>/tasks.by-module/<module>-tasks.md
  Insert or replace only the block between:
    <!-- FANOUT:BEGIN -->
    ... generated list of source items ...
    <!-- FANOUT:END -->
- If `.specify/templates/module-tasks-template.md` exists, seed a new file from it,
  then append the FANOUT block at the end. If file exists, replace the FANOUT block only.
- Print a summary: module → count, and list "unassigned" items (no module detected).

Exit codes:
  0 = success; 1 = no tasks file; 2 = no module-tagged or inferred items; 3 = malformed.
"""

import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict

# Checkbox lines like "- [ ] ...", "- [x] ..."
CHECKBOX_RE = re.compile(r'^\s*-\s*\[(?P<done>[ xX])\]\s*(?P<body>.+)$')

# @module(repo)
MODULE_TAG_RE = re.compile(r'@module\((?P<name>[^)]+)\)', re.IGNORECASE)

# Simple path-based inference (extend as you like)
PATH_HINTS = {
    "backend/": "backend",
    "frontend/": "frontend",
    "api/": "api",
    "repo/": "repo",
    "ios/": "ios",
    "android/": "android",
}

FANOUT_BEGIN = "<!-- FANOUT:BEGIN -->"
FANOUT_END = "<!-- FANOUT:END -->"

DEFAULT_TEMPLATE_HEADER = """# Module Tasks: [MODULE NAME] for Feature [FEATURE NAME]

**Inputs**
- Global constitution: `.specify/memory/constitution.md`
- Module constitution (optional): `.specify/memory/[module].constitution.md`
- Global tasks: `.specify/specs/[###-feature-name]/tasks.md`
- Feature docs: `plan.md` (required), `data-model.md`, `contracts/`, `research.md`

**Note**
This file has a protected fan-out block below. Run `/fanout-tasks` to refresh it.
"""

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

def write_text(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def replace_block(original: str, begin: str, end: str, new_block: str) -> str:
    if begin in original and end in original:
        pre, _, rest = original.partition(begin)
        _, _, post = rest.partition(end)
        return f"{pre}{begin}\n{new_block}\n{end}{post}"
    # append at end
    if not original.endswith("\n"):
        original += "\n"
    return f"{original}\n{begin}\n{new_block}\n{end}\n"

def seed_module_file(module_file: Path, feature_id: str, module: str, template_path: Path) -> str:
    current = read_text(module_file)
    if current:
        return current
    tmpl = read_text(template_path) or DEFAULT_TEMPLATE_HEADER
    tmpl = tmpl.replace("[MODULE NAME]", module).replace("[FEATURE NAME]", feature_id)
    return tmpl.rstrip() + "\n"

def detect_module(line: str) -> str | None:
    # (a) explicit tag
    mm = MODULE_TAG_RE.search(line)
    if mm:
        return mm.group("name").strip()
    # (b) path hints
    lower = line.lower()
    for hint, module in PATH_HINTS.items():
        if hint in lower:
            return module
    return None

def parse_checkbox_items(text: str):
    items = []
    for idx, line in enumerate(text.splitlines()):
        m = CHECKBOX_RE.match(line)
        if not m:
            continue
        done = m.group("done").lower() == "x"
        body = m.group("body")
        module = detect_module(line)
        items.append(dict(idx=idx, line=line, body=body, done=done, module=module))
    return items

def build_fanout_block(items_for_module):
    # Keep original order as in the file
    lines = [
        "## Global Items (source)",
        "",
        "*Do not edit this block manually; run `/fanout-tasks` to refresh.*",
        "",
    ]
    if not items_for_module:
        lines.append("(No items)")
    else:
        for it in items_for_module:
            # Preserve checkbox state and the text after the checkbox
            lines.append(f"- [{'x' if it['done'] else ' '}] {it['body']}")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feature_id")
    ap.add_argument("--tasks", default=None, help="Path to the global tasks.md")
    ap.add_argument("--outdir", default=None, help="Output dir for module task files")
    args = ap.parse_args()

    root = Path(".").resolve()
    tasks_path = Path(args.tasks) if args.tasks else root / ".specify" / "specs" / args.feature_id / "tasks.md"
    if not tasks_path.exists():
        print(f"ERROR: tasks file not found: {tasks_path}", file=sys.stderr)
        sys.exit(1)

    outdir = Path(args.outdir) if args.outdir else root / ".specify" / "specs" / args.feature_id / "tasks.by-module"
    template_path = root / ".specify" / "templates" / "module-tasks-template.md"

    text = read_text(tasks_path)
    items = parse_checkbox_items(text)

    by_module = defaultdict(list)
    unassigned = []
    for it in items:
        if it["module"]:
            by_module[it["module"]].append(it)
        else:
            unassigned.append(it)

    if not by_module and not unassigned:
        print("ERROR: no checkbox tasks found in global tasks.md", file=sys.stderr)
        sys.exit(3)

    # Write/update each module file
    for module, its in sorted(by_module.items(), key=lambda kv: kv[0]):
        module_file = outdir / f"{module}-tasks.md"
        current = seed_module_file(module_file, args.feature_id, module, template_path)
        fanout = build_fanout_block(sorted(its, key=lambda it: it["idx"]))
        updated = replace_block(current, FANOUT_BEGIN, FANOUT_END, fanout)
        write_text(module_file, updated)

    # Summary
    print("\nFan-out summary:")
    if by_module:
        for module, its in sorted(by_module.items()):
            print(f"  - {module:<10} {len(its):>3} items  → { (outdir / f'{module}-tasks.md').as_posix() }")
    else:
        print("  (no module-assigned items)")

    if unassigned:
        print("\nUnassigned items (no @module tag and no path hint):")
        for it in unassigned:
            print(f"  - line {it['idx']+1}: {it['body'][:100]}")

if __name__ == "__main__":
    from collections import defaultdict
    main()
