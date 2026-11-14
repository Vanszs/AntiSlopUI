#!/usr/bin/env python3
"""Mechanical P0 audit for generated UI artifacts."""
import argparse
import json
import re
import sys
from pathlib import Path

RULES = [
    ("transition-all", re.compile(r"transition\s*:\s*all|transition-all", re.I)),
    ("accent-hex", re.compile(r"#(?:6366f1|8b5cf6|7c3aed|a78bfa|818cf8|4f46e5|c4b5fd)\b", re.I)),
    ("accent-tailwind", re.compile(r"\b(?:indigo|violet|purple)-\d{2,3}\b", re.I)),
    ("hover-scale", re.compile(r"hover:scale-1\d\d", re.I)),
    ("group-hover-scale", re.compile(r"group-hover:scale", re.I)),
    ("white-opacity", re.compile(r"bg-white/1[00]?\b", re.I)),
    ("backdrop-blur-lg", re.compile(r"backdrop-blur-lg\b", re.I)),
    ("text-transparent-gradient", re.compile(r"(?=.*text-transparent)(?=.*bg-clip-text)", re.I)),
    ("duration-over-400ms", re.compile(r"\bduration-(?:4[1-9]\d|[5-9]\d\d|\d{4,})\b|\b(?:4[1-9]\d|[5-9]\d\d|\d{4,})ms\b", re.I)),
    ("uniform-container", re.compile(r"\bmax-w-7xl\b", re.I)),
    ("empty-src", re.compile(r"\bsrc\s*=\s*(['\"])[ ]*\1", re.I)),
]
EXTENSIONS = {".css", ".html", ".tsx", ".md"}


def files_for(paths):
    for item in paths:
        path = Path(item)
        candidates = path.rglob("*") if path.is_dir() else [path]
        for file in candidates:
            if file.is_file() and file.suffix.lower() in EXTENSIONS and not ({".git", "__pycache__"} & set(file.parts)):
                yield file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--allow", action="append", default=[], help="allow matching lines containing substring")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    allow = list(args.allow)
    allow_file = Path(__file__).with_name("audit-allowlist.txt")
    if allow_file.exists():
        allow.extend(line.strip() for line in allow_file.read_text(encoding="utf-8").splitlines()
                     if line.strip() and not line.lstrip().startswith("#"))
    violations = []
    for path in files_for(args.paths):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            compact = re.sub(r"\s+", " ", line).strip()
            for name, pattern in RULES:
                matches = list(pattern.finditer(compact))
                if name == "text-transparent-gradient" and matches:
                    matches = [pattern.search(" ".join(text.splitlines()[max(0, line_no-3):line_no+2]))]
                if name == "uniform-container":
                    matches = matches if compact.count("max-w-7xl") > 0 else []
                for match in matches:
                    if any(token in compact for token in allow):
                        continue
                    violations.append({"path": str(path), "line": line_no, "rule": name, "snippet": compact[:240]})
    containers = {}
    for v in violations:
        if v["rule"] == "uniform-container":
            containers[v["path"]] = containers.get(v["path"], 0) + 1
    violations = [v for v in violations if v["rule"] != "uniform-container"] + [
        v for v in violations if v["rule"] == "uniform-container" and containers[v["path"]] > 1
    ]
    # max-w-7xl is only banned when repeated and no alternative max-w utility exists.
    filtered = []
    for v in violations:
        if v["rule"] != "uniform-container":
            filtered.append(v)
            continue
        text = Path(v["path"]).read_text(encoding="utf-8")
        if len(re.findall(r"\bmax-w-7xl\b", text, re.I)) > 1 and not re.search(r"\bmax-w-(?!7xl\b)[\w-]+", text, re.I):
            filtered.append(v)
    violations = filtered
    if args.json:
        print(json.dumps({"violations": violations, "count": len(violations)}, ensure_ascii=False))
    else:
        for v in violations:
            print("{}:{} {} | {}".format(v["path"], v["line"], v["rule"], v["snippet"]))
        print("{} violation(s) across {} file(s)".format(len(violations), len(list(files_for(args.paths)))))
    return 1 if violations else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("audit error: {}: {}".format(type(exc).__name__, exc), file=sys.stderr)
        raise SystemExit(2)
