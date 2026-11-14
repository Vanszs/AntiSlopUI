#!/usr/bin/env python3
"""Repository structural checks; intentionally uses only stdlib + optional PyYAML."""
import csv
import shlex
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from stats import block as stats_block, compute


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
    if not match:
        raise ValueError("missing opening/closing YAML frontmatter")
    raw = match.group(1)
    try:
        import yaml
        data = yaml.safe_load(raw) or {}
        return data, raw
    except ImportError:
        data, section = {}, None
        lines = raw.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            key = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
            nested = re.match(r"^\s{2}([\w-]+):\s*(.*)$", line)
            if key:
                k, value = key.groups()
                section = k if not value else None
                if value in ("|", ">", "|-", ">-"):
                    chunks, i = [], i + 1
                    while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                        chunks.append(lines[i].strip())
                        i += 1
                    data[k] = " ".join(x for x in chunks if x)
                    continue
                data[k] = value.strip().strip("\"'")
            elif nested and section:
                k, value = nested.groups()
                if k == "references":
                    refs = []
                    i += 1
                    while i < len(lines):
                        item = re.match(r"^\s{4}-\s*(.+?)\s*$", lines[i])
                        if item:
                            refs.append(item.group(1).strip("\"'"))
                        elif lines[i].strip() and not lines[i].startswith("    "):
                            break
                        i += 1
                    data.setdefault(section, {})[k] = refs
                    continue
                data.setdefault(section, {})[k] = value.strip().strip("\"'")
            elif section == "metadata" and re.match(r"^\s{2}references:\s*$", line):
                data.setdefault("metadata", {})["references"] = []
            i += 1
        return data, raw


def check(name, failures):
    if failures:
        print("FAIL {}: {}".format(name, "; ".join(str(x) for x in failures)))
        return False
    print("PASS {}".format(name))
    return True


def run_check(results, name, fn):
    try:
        failures = fn()
    except Exception as exc:
        failures = ["{}: {}".format(type(exc).__name__, exc)]
    results.append(check(name, failures))


def persisted_probe():
    out = Path(tempfile.mkdtemp(prefix="persist-", dir="/tmp/opencode" if Path("/tmp/opencode").exists() else None))
    cmd = [sys.executable, str(ROOT / "ui-ux-pro-max/scripts/search.py"), "saas dashboard", "--design-system", "--persist", "-p", "ValidateProbe", "-o", str(out)]
    proc = subprocess.run(cmd, cwd="/tmp/opencode/validate-cwd" if Path("/tmp/opencode/validate-cwd").exists() else str(ROOT), capture_output=True, text=True, timeout=90)
    if proc.returncode:
        raise RuntimeError("persist probe exit {}: {}".format(proc.returncode, (proc.stdout + proc.stderr)[-1500:]))
    master = out / "design-system/validateprobe/MASTER.md"
    if not master.is_file():
        raise RuntimeError("persist probe did not create promised {}".format(master))
    return out, master


def main():
    results = []
    skills = sorted(p for p in ROOT.glob("*/SKILL.md") if p.is_file())
    md_files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)

    failures = []
    parsed = {}
    for path in skills:
        try:
            data, _ = frontmatter(path)
            parsed[path] = data
            name, desc = data.get("name"), data.get("description")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name) or name != path.parent.name:
                failures.append("{}: invalid/mismatched name {!r}".format(path.relative_to(ROOT), name))
            if not isinstance(desc, str) or len(desc.strip()) < 60:
                failures.append("{}: description must be at least 60 characters".format(path.relative_to(ROOT)))
        except Exception as exc:
            failures.append("{}: {}".format(path.relative_to(ROOT), exc))
    results.append(check("1 FRONTMATTER SPEC", failures))

    failures = []
    for path, data in parsed.items():
        refs = ((data.get("metadata") or {}).get("references") or [])
        # The Agent Skills spec requires metadata to be string->string, so reference
        # lists are stored as a comma-separated string. Accept both forms.
        if isinstance(refs, str):
            refs = [part.strip() for part in refs.split(",") if part.strip()]
        elif isinstance(refs, list):
            pass
        for ref in refs:
            if isinstance(ref, dict):
                ref = ref.get("path", "")
            if not isinstance(ref, str) or not (path.parent / ref).exists():
                failures.append("{}: missing reference {!r}".format(path.relative_to(ROOT), ref))
    results.append(check("2 REFERENCE INTEGRITY", failures))

    failures = []
    link_re = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in md_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for target in link_re.findall(text):
            target = target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            parsed_url = urlsplit(target)
            local = unquote(parsed_url.path)
            if local and not (path.parent / local).exists():
                failures.append("{}: missing link target {!r}".format(path.relative_to(ROOT), target))
    results.append(check("3 LINK INTEGRITY", failures))

    failures = ["{}:{} contains steering/ui-ux-pro-max".format(p.relative_to(ROOT), i)
                for p in md_files for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
                if "steering/ui-ux-pro-max" in line]
    results.append(check("4 NO STALE PATHS", failures))

    failures = []
    codepath = re.compile(r"(?<![\w./-])(?:[\w.-]+/)+[\w.-]+\.(?:md|py|csv)")
    readme = ROOT / "README.md"
    if readme.exists():
        for line_no, line in enumerate(readme.read_text(encoding="utf-8").splitlines(), 1):
            for target in re.findall(r"`([^`]+)`", line):
                if " " not in target and not re.search(r"[*?\[\]{}]", target) and codepath.fullmatch(target):
                    if not (ROOT / target).exists():
                        failures.append("README.md:{} missing `{}`".format(line_no, target))
    results.append(check("5 NO BANNED-FILE-DRIFT", failures))

    labels = [label for label, _ in compute(ROOT)]
    failures = []
    if not readme.exists():
        failures.append("README.md missing")
    else:
        text = readme.read_text(encoding="utf-8")
        match = re.search(r"<!-- stats:begin -->(.*?)<!-- stats:end -->", text, re.S)
        if not match:
            print("FAIL 6 STATS SYNC: missing block; paste this exact block:\n{}".format(stats_block(ROOT)))
            results.append(False)
        else:
            found = {}
            table = match.group(1)
            if not re.search(r"(?m)^\s*\|\s*Metric\s*\|\s*Value\s*\|\s*$", table):
                failures.append("table header must be `| Metric | Value |`")
            for line in table.splitlines():
                m = re.match(r"\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
                if m and m.group(1).strip() != "Metric" and not set(m.group(2).strip()) <= set(":- "):
                    label, value = m.group(1).strip(), m.group(2).strip()
                    if label not in labels or not value.isdigit():
                        failures.append("invalid stats row {!r}: {!r}".format(label, value))
                    else:
                        if label in found:
                            failures.append("duplicate stats row {!r}".format(label))
                        found[label] = int(value)
            if set(found) != set(labels):
                failures.append("table must contain exactly these metric rows: {}".format(", ".join(labels)))
            for label, value in compute(ROOT):
                if found.get(label) != value:
                    failures.append("{}: expected {}, found {}".format(label, value, found.get(label)))
            results.append(check("6 STATS SYNC", failures))

    failures = []
    skill = ROOT / "ui-ux-pro-max/SKILL.md"
    if skill.exists():
        text = skill.read_text(encoding="utf-8").casefold().replace("-", "").replace("_", "")
        for stack in sorted((ROOT / "ui-ux-pro-max/data/stacks").glob("*.csv")):
            slug = stack.stem.casefold().replace("-", "").replace("_", "")
            if slug not in text:
                failures.append("available stacks listing missing {}".format(stack.stem))
    results.append(check("7 STACK COVERAGE", failures))

    try:
        proc = subprocess.run([sys.executable, "ui-ux-pro-max/scripts/search.py", "saas dashboard", "--design-system"],
                              cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, text=True)
        if proc.returncode or not proc.stdout.strip():
            failures = ["exit {}; output {}".format(proc.returncode, (proc.stdout + proc.stderr).strip()[:500])]
        else:
            failures = []
    except Exception as exc:
        failures = [str(exc)]
    results.append(check("8 TOOL SANITY", failures))

    allowlist = []
    allow_path = ROOT / "scripts/conflict-allowlist.txt"
    if allow_path.exists():
        allowlist = [line.strip() for line in allow_path.read_text(encoding="utf-8").splitlines()
                     if line.strip() and not line.lstrip().startswith("#")]
    banned = ("#6366F1", "indigo-500", "max-w-7xl", "hover:scale-105", "backdrop-blur-lg", "transition-all")
    allowed_words = ("❌", "BAN", "ban", "never", "Never", "avoid", "Avoid", "P0", "slop", "Slop", "→", "don't", "Don't", "instead", "Instead", "FAIL", "⚠", "OVERRIDE", "vendor", "Vendor", "substitut")
    # Reviewed exemptions: these files exist to *catalogue* banned values. Scanning them
    # for banned literals is a category error, so they are excluded rather than allowlisted.
    exempt_prefixes = ("anti-ai-slop-ui-ux/", "ui-ux-pro-max/data/")
    exempt_files = ("ui-ux-pro-max/POST-FILTER.md",)
    failures = []
    for path in (p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and p.suffix not in (".pyc",)):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(exempt_prefixes) or rel in exempt_files or rel == "scripts/audit.py":
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(lines, 1):
            hits = [word for word in banned if word in line]
            if hits and not any(word in line for word in allowed_words) and not any(
                    entry.startswith(rel + ":") and entry.split(":", 1)[1] in line for entry in allowlist):
                failures.append("{}:{} {} | {}".format(rel, line_no, ", ".join(hits), line.strip()))
    results.append(check("9 CONFLICT GUARD", failures))

    # 10 RUBRIC INTEGRITY: the opt-in craft tier must keep the published weights.
    failures = []
    craft = ROOT / "component-reference-design/references/awards-craft.md"
    if not craft.exists():
        failures.append("missing awards-craft.md")
    else:
        text = craft.read_text(encoding="utf-8")
        expected = {"Design": 40, "Usability": 30, "Creativity": 20, "Content": 10}
        row_re = re.compile(r"(?m)^\|\s*\*\*?([A-Za-z]+)\*\*?\s*\|\s*(\d{1,3})\b")
        found = {name: int(weight) for name, weight in row_re.findall(text)}
        if not found:
            failures.append("no rubric rows found (expected **Design** | 40 style rows)")
        else:
            if found != expected:
                failures.append("weights must be exactly {} (found {})".format(expected, found))
            if sum(found.values()) != 100:
                failures.append("weights must sum to 100 (found {})".format(sum(found.values())))
        for label in ("Hard gates", "prefers-reduced-motion", "OVERRIDE:"):
            if label not in text:
                failures.append("missing required section/term {!r}".format(label))
    results.append(check("10 RUBRIC INTEGRITY", failures))

    def csv_structure():
        problems = []
        csv_paths = sorted(set((ROOT / "ui-ux-pro-max/data").glob("*.csv")) | set((ROOT / "data/stacks").glob("*.csv")))
        for path in csv_paths:
            with path.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream, strict=True))
            if not rows:
                problems.append("{}: empty CSV".format(path.relative_to(ROOT)))
                continue
            width = len(rows[0])
            ids = [row[0] for row in rows[1:] if row]
            if any(len(row) != width for row in rows[1:]):
                problems.append("{}: row field count differs from header ({})".format(path.relative_to(ROOT), width))
            if len(ids) != len(set(ids)):
                problems.append("{}: duplicate first-column IDs".format(path.relative_to(ROOT)))
            nums = sorted(int(value) for value in ids if value.isdigit())
            if nums and nums != list(range(nums[0], nums[-1] + 1)):
                problems.append("{}: numeric ID gaps".format(path.relative_to(ROOT)))
        return problems
    run_check(results, "11 CSV STRUCTURE", csv_structure)

    def documented_cli():
        problems = []
        script = ROOT / "ui-ux-pro-max/scripts/search.py"
        source = script.read_text(encoding="utf-8")
        domains = re.search(r"--domain[^\n]*choices=\s*list\(CSV_CONFIG\.keys\(\)\)", source)
        stacks = re.search(r"--stack[^\n]*choices=\s*AVAILABLE_STACKS", source)
        sys.path.insert(0, str(script.parent))
        try:
            from core import CSV_CONFIG, AVAILABLE_STACKS
            domain_choices, stack_choices = set(CSV_CONFIG), set(AVAILABLE_STACKS)
        finally:
            sys.path.pop(0)
        for doc in (ROOT / "ui-ux-pro-max/SKILL.md", ROOT / "README.md"):
            if not doc.exists():
                continue
            text = doc.read_text(encoding="utf-8")
            for line_no, line in enumerate(text.splitlines(), 1):
                if "search.py" not in line:
                    continue
                for value in re.findall(r"--domain\s+([\w-]+)", line):
                    if value not in domain_choices:
                        problems.append("{}:{} undocumented domain {}".format(doc.relative_to(ROOT), line_no, value))
                for value in re.findall(r"--stack\s+([\w-]+)", line):
                    if value not in stack_choices:
                        problems.append("{}:{} undocumented stack {}".format(doc.relative_to(ROOT), line_no, value))
                match = re.search(r"(?:python3?\s+)?(?:[\w./-]*search\.py\s+.+)", line)
                if match and not re.search(r"<[^>]+>", match.group(0)):
                    command = match.group(0).strip().strip("`")
                    command = re.sub(r"(?:[\w./-]*search\.py)", shlex.quote(str(script)), command, count=1)
                    try:
                        proc = subprocess.run(shlex.split(command), cwd="/tmp/opencode/validate-cwd" if Path("/tmp/opencode/validate-cwd").exists() else str(ROOT), capture_output=True, text=True, timeout=30)
                        if proc.returncode:
                            problems.append("{}:{} command exit {}: {}".format(doc.relative_to(ROOT), line_no, proc.returncode, (proc.stderr or proc.stdout)[:300]))
                    except Exception as exc:
                        problems.append("{}:{} {}".format(doc.relative_to(ROOT), line_no, exc))
        return problems
    run_check(results, "12 DOCUMENTED CLI TRUTH", documented_cli)

    probe = {}
    def persist_contract():
        out, master = persisted_probe()
        probe.update(out=out, master=master)
        promised = [out / "design-system/validateprobe/MASTER.md", out / "design-system/validateprobe/pages"]
        missing = [str(p) for p in promised if not p.exists()]
        text = master.read_text(encoding="utf-8")
        for item in re.findall(r"(?:design-system/)[\w./-]+", text):
            rel = item.rstrip(".,)`]")
            actual = out / rel
            if rel == "design-system/pages/":
                actual = out / "design-system/validateprobe/pages"
            if rel and not actual.exists() and not rel.endswith(("[page].md", "MASTER.md")):
                missing.append("generated artifact references absent path {}".format(rel))
        return missing
    run_check(results, "13 PERSIST CONTRACT", persist_contract)

    def frontmatter_types():
        failures = []
        for path in skills:
            data, raw = frontmatter(path)
            metadata = data.get("metadata", {})
            if not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items()):
                failures.append("{}: metadata must be string-to-string map".format(path.relative_to(ROOT)))
            if "yaml" not in sys.modules:
                section = re.search(r"(?ms)^metadata:\s*\n(.*?)(?=^\S|\Z)", raw)
                if section and (re.search(r"(?m)^\s*-", section.group(1)) or re.search(r"(?m)^\s*\w+:\s*\d{4}-\d\d-\d\d\s*$", section.group(1))):
                    failures.append("{}: fallback metadata list/date is not string-map safe".format(path.relative_to(ROOT)))
        return failures
    run_check(results, "14 FRONTMATTER TYPES", frontmatter_types)

    run_check(results, "15 TOC PRESENCE", lambda: ["{}: missing ## Contents in first 20 lines".format(p.relative_to(ROOT)) for p in ROOT.glob("*/references/*.md") if not any(line.strip() == "## Contents" for line in p.read_text(encoding="utf-8").splitlines()[:20])])

    def ban_voiding():
        findings = []
        for path in md_files:
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if re.search(r"bare minimum guidelines|Improvise beyond what's documented", line, re.I) and "within the bans" not in line.casefold():
                    findings.append("{}:{} ban-voiding phrase".format(path.relative_to(ROOT), n))
        return findings
    run_check(results, "16 NO BAN-VOIDING CLAUSE", ban_voiding)

    def single_motion():
        failures = []
        for path in md_files:
            if path == ROOT / "anti-ai-slop-ui-ux/SKILL.md":
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "OVERRIDE" not in line and re.search(r"600ms|500ms|1–1\.5s|duration-(?:[5-9])\d\d\b", line):
                    failures.append("{}:{} noncanonical duration".format(path.relative_to(ROOT), number))
        return failures
    run_check(results, "17 SINGLE MOTION CANON", single_motion)

    def description_disjointness():
        descriptions = []
        failures = []
        for path in skills:
            desc = str(parsed.get(path, {}).get("description", ""))
            descriptions.append((path, desc))
            has_negative_space = re.search(r"not for", desc, re.I) is not None
            has_load_order = re.search(r"\bload\w*\b|\bafter\b", desc, re.I) is not None
            if not (has_negative_space and has_load_order):
                failures.append("{}: description needs Not for and load-order clause".format(path.relative_to(ROOT)))
        for i, (left, a) in enumerate(descriptions):
            for right, b in descriptions[i+1:]:
                if re.search(r"\bany UI\b", a, re.I) and re.search(r"\bany UI\b", b, re.I):
                    failures.append("{} and {} share phrase 'any UI'".format(left.relative_to(ROOT), right.relative_to(ROOT)))
        return failures
    run_check(results, "18 DESCRIPTION DISJOINTNESS", description_disjointness)

    def readme_claim_sync():
        text = readme.read_text(encoding="utf-8")
        failures = ["README.md contains --write# (missing shell-comment space)"] if "--write#" in text else []
        match = re.search(r"(\d+) structural checks", text, re.I)
        implemented = len(results) + 2  # This check plus the generated-artifact audit below.
        if match and int(match.group(1)) != implemented:
            failures.append("README claims {} checks; implemented {}".format(match.group(1), implemented))
        return failures
    run_check(results, "19 README CLAIM SYNC", readme_claim_sync)

    def generated_audit():
        if "master" not in probe:
            raise RuntimeError("persist probe unavailable")
        proc = subprocess.run([sys.executable, str(ROOT / "scripts/audit.py"), str(probe["master"])], capture_output=True, text=True, timeout=30)
        return [] if proc.returncode == 0 else ["audit exit {}: {}".format(proc.returncode, (proc.stdout + proc.stderr).strip())]
    run_check(results, "20 GENERATED ARTIFACT AUDIT", generated_audit)

    if "--json" in sys.argv:
        print(json.dumps({"passed": sum(results), "failed": len(results) - sum(results), "checks": len(results)}))
    raise SystemExit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
