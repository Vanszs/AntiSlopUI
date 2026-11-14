# AntiSlopUI

![Version](https://img.shields.io/badge/suite%202.2.0-blue?style=for-the-badge)
![3 Skills](https://img.shields.io/badge/skills-3-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
[![validate](https://github.com/Vanszs/AntiSlopUI/actions/workflows/validate.yml/badge.svg)](https://github.com/Vanszs/AntiSlopUI/actions/workflows/validate.yml)

Three skills for AI coding agents that remove "AI slop" from generated UI and replace it
with intentional, branded, accessible work — plus a mechanical gate that fails the build
when a banned default slips through.

> If you could swap the logo with a competitor and nobody would notice — it's slop.

## What problem this solves

LLMs generate UI by averaging training data dominated by Tailwind docs, shadcn/ui examples,
abandoned repos with unchanged defaults, and 2020–2024 Dribbble SaaS shots. Output collapses
toward the visual mean: purple gradients, Inter everywhere, centered dual-CTA heroes, 3-card
grids, glass navbars, "Supercharge your workflow" copy.

That is structural. Every decision left unspecified gets the most probable token. The cure is
deliberate, content-specific variation — enforced, not suggested.

## Which skill loads when

Routing is the part most skill suites get wrong. These three descriptions are disjoint on
purpose; load order is stated inside the descriptions because a router never reads a README.

| Skill id | Load when | Do not load for |
|---|---|---|
| `anti-ai-slop-ui-ux` | **First**, before any UI code is written or reviewed. Owns the ban list, severity tiers and the PASS/FAIL audit | Backend, API, data pipelines, docs-only work |
| `component-reference-design` | You need a concrete pattern/markup for UI you are already building | Deciding whether to build UI; backend or data work |
| `ui-ux-pro-max` | You need industry-specific style/palette/typography evidence, after the filter is loaded | Code review; pattern lookup (use the palette skill) |

If you load only one skill, load the filter. The other two defer to it, and each carries a local
minimum contract so it still works alone: the palette ships a ship-gate, the research skill ships
an 8-bullet ban summary. Installing all three is still better than installing one.

## Precedence & conflict policy

1. **`anti-ai-slop-ui-ux` is the authority.** It owns the bans and the closed severity
   vocabulary (`P0` / `HIGH` / `MEDIUM` / `LOW`).
2. **Palette patterns conform.** A pattern is a starting point that must pass the filter.
3. **Research output is a proposal.** Every `--design-system` result passes through
   [`ui-ux-pro-max/POST-FILTER.md`](ui-ux-pro-max/POST-FILTER.md) before it reaches code —
   including its **style** field, which the vendor database reliably fills with
   `Glassmorphism` for SaaS.
4. **Craft is opt-in.** `component-reference-design/references/awards-craft.md` raises the
   ceiling only for explicitly premium/award work, only after the audit passes, and only via
   declared `OVERRIDE:` lines. Its hard gates (LCP ≤2.5s, CLS ≤0.1, INP ≤200ms,
   reduced-motion parity, keyboard, 390px parity, contrast) deny the tier on any failure.
5. **Exceptions are mechanical, not vibes.** A brand purple is legal only if the hex appears
   in user-supplied brand assets, recorded as `OVERRIDE: <value> → <value> [brand: <source>]`.
   Unknown proof is omitted and recorded `NO-PROOF: user supplied none`; inventing it is P0.
6. **The audit runs last and reports `PASS`/`FAIL`/`N-A`** with an evidence pointer per item.
   One P0 FAIL blocks delivery.

## Context budget

- **Always:** the `SKILL.md` of skills that apply (≤3 files).
- **On demand:** per skill, at most one reference file; the tell catalog is a second file when
  auditing (two total for a full run); two also when combining dashboards + charts. Every reference starts with a `## Contents` index —
  `grep -nE '^#{1,2} '`, then read only that range (END = next match − 1).
- **Never:** read the CSVs by hand. Query them through `search.py` (2–3 targeted queries).

## Installation

Every skill directory name equals its frontmatter `name` — the two must stay in sync.
Put the directory in the platform's skills root (or symlink it there).

### Claude Code

```bash
git clone https://github.com/Vanszs/AntiSlopUI.git
mkdir -p ~/.claude/skills
ln -s "$PWD/AntiSlopUI/anti-ai-slop-ui-ux" ~/.claude/skills/anti-ai-slop-ui-ux
ln -s "$PWD/AntiSlopUI/component-reference-design" ~/.claude/skills/component-reference-design
ln -s "$PWD/AntiSlopUI/ui-ux-pro-max" ~/.claude/skills/ui-ux-pro-max
```

### Codex

```bash
mkdir -p ~/.agents/skills
ln -s "$PWD/AntiSlopUI/anti-ai-slop-ui-ux" ~/.agents/skills/anti-ai-slop-ui-ux
ln -s "$PWD/AntiSlopUI/component-reference-design" ~/.agents/skills/component-reference-design
ln -s "$PWD/AntiSlopUI/ui-ux-pro-max" ~/.agents/skills/ui-ux-pro-max
```

### opencode

```bash
mkdir -p ~/.config/opencode/skills
ln -s "$PWD/AntiSlopUI/anti-ai-slop-ui-ux" ~/.config/opencode/skills/anti-ai-slop-ui-ux
ln -s "$PWD/AntiSlopUI/component-reference-design" ~/.config/opencode/skills/component-reference-design
ln -s "$PWD/AntiSlopUI/ui-ux-pro-max" ~/.config/opencode/skills/ui-ux-pro-max
```

Note: opencode derives the skill id from the **path**, and treats frontmatter `name` as a
display label. Keep the directory name canonical anyway.

### Kiro

Kiro native skills live in `.kiro/skills/`. Do **not** copy this suite into
`.kiro/steering/` — steering files default to always-included, which injects every skill
and every reference into every request and defeats progressive disclosure.

```bash
mkdir -p your-project/.kiro/skills
cp -r AntiSlopUI/anti-ai-slop-ui-ux your-project/.kiro/skills/
cp -r AntiSlopUI/component-reference-design your-project/.kiro/skills/
cp -r AntiSlopUI/ui-ux-pro-max your-project/.kiro/skills/
```

### Any other agent (AGENTS.md / CLAUDE.md pointer)

```markdown
## UI work
Read `anti-ai-slop-ui-ux/SKILL.md` before writing or reviewing any UI code. It is a hard
filter that owns the ban list, not advice. For patterns, open at most one file from
`component-reference-design/references/`. Run the Pre-Delivery Slop Audit and report
PASS/FAIL/N-A per item with evidence. Never invent social proof; omit it and record
`NO-PROOF: user supplied none`.
```

### Prerequisites

Python 3.8+ is required only for the `ui-ux-pro-max` research tool. The other two skills are
pure Markdown.

```bash
python3 --version          # macOS: brew install python3
                           # Ubuntu/Debian: sudo apt install python3
                           # Windows: winget install Python.Python.3.12
```

If your agent has no shell, the filter documents a fallback: skip the CSV research, use the
pattern library plus authored defaults, and state the limitation in the output.

## Usage

1. **Filter** — read bans, severity tiers and the deterministic terms (`tell`, brand, proof).
2. **Palette** — pick a pattern by its *when-to-use* note; vary anatomy, widths, padding.
3. **Research** — generate an industry design system, then post-filter it (style included).
4. **Audit** — run the PASS/FAIL audit; then `scripts/audit.py` on the artifact in CI.

```bash
# Full design system (print)
python3 ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"

# Persist MASTER + per-page overrides into design-system/<slug>/ (gitignored)
python3 ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system --persist -p "Ledger"

# Choose the output directory explicitly (default: current working directory)
python3 ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system --persist -p "Ledger" -o ./design

# Single domain / stack
python3 ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style
python3 ui-ux-pro-max/scripts/search.py "form validation" --stack react
```

Commands are repo-relative. When the skill is installed elsewhere (e.g.
`~/.claude/skills/ui-ux-pro-max`, `.kiro/skills/ui-ux-pro-max`), invoke it as
`python3 "<skill-dir>/scripts/search.py" …` — the script resolves its data directory
relative to itself, so only the path you type changes.

## What's inside

```
AntiSlopUI/
├── anti-ai-slop-ui-ux/                  # FILTER — authority on bans
│   ├── SKILL.md                         # 12 hard gates, deterministic terms, sole motion
│   │                                    # table, text measure, audit, fallback
│   └── references/
│       ├── slop-uiux-patterns.md        # TELL → WHY-SLOP → FIX → SEVERITY catalog
│       └── slop-code-patterns.md        # code-level tells (React/TSX/a11y)
│
├── component-reference-design/          # PALETTE — what to build
│   ├── SKILL.md                         # routing table, anti-monotony rules, quality bar
│   └── references/                      # layouts, typography, components, animation,
│                                        # design-systems, charts, dashboards, awards-craft
│
├── ui-ux-pro-max/                       # RESEARCH — CSV design-system generator
│   ├── SKILL.md                         # workflow, path convention, post-filter step
│   ├── POST-FILTER.md                   # vendor output → compliant substitution
│   ├── data/                            # CSV databases (query via search.py)
│   └── scripts/                         # search engine
│
├── scripts/
│   ├── validate.py                      # repo-level validation (22 checks)
│   ├── audit.py                         # artifact-level P0 gate (case-insensitive)
│   └── stats.py                         # recompute/splice the stats block below
│
└── .github/workflows/validate.yml       # CI: validate + audit a generated design system
```

## Verification

Claims in this repository are checked, not asserted:

```bash
python3 scripts/validate.py       # 22 structural + semantic checks, non-zero exit on failure
python3 scripts/audit.py <path>   # artifact gate: banned values in CSS/HTML/TSX/MD
python3 scripts/stats.py          # recompute stats from the CSVs
python3 scripts/stats.py --write  # splice corrected numbers into this README
```

What is enforced:

- frontmatter spec (name = directory, lowercase-hyphen, `metadata` string→string), reference
  and markdown-link integrity, no stale install paths
- CSV structure (every row matches its header; IDs unique and contiguous)
- documented CLI truth (`--domain` / `--stack` values must exist in argparse)
- persistence contract (the directory tree the docs name is the tree the code writes)
- `## Contents` present in every reference; no ban-voiding clauses
- a single motion canon outside the filter's table; no unexplained duration >300ms
- descriptions dispatching (no two claim "any UI"; each has a "Not for" clause or load order)
- README claims matching the implementation (including the check count)
- `audit.py` run against a freshly generated `MASTER.md` — this is what catches a generator
  that emits `transition: all` or an indigo accent
- `metadata.suite_version` agreement across all three skills (it increments only when the
  suite's shared contract changes; per-skill `version` stays independent)

## Stats

<!-- stats:begin -->
| Metric | Value |
| --- | ---: |
| Skills | 3 |
| Markdown files | 15 |
| Reference files | 10 |
| Reasoning rules | 100 |
| UI styles | 66 |
| Color palettes | 96 |
| Font pairings | 57 |
| UX guidelines | 99 |
| Chart types | 25 |
| Tech stacks | 13 |
<!-- stats:end -->

## Contributing

```bash
git clone https://github.com/Vanszs/AntiSlopUI.git
cd AntiSlopUI
git checkout -b feat/your-feature
# edit
python3 scripts/validate.py && python3 scripts/audit.py .
git commit -m "feat: description"
git push -u origin feat/your-feature
gh pr create
```

Rules of the house: no claim without a validated number, no ban without a compliant default,
no reference file without `## Contents`, no new motion duration outside the canonical table.
If your change conflicts with the filter, the filter wins.

## Acknowledgments

- **[UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** by
  [NextLevelBuilder](https://github.com/nextlevelbuilder) — the `ui-ux-pro-max/` directory is
  their design intelligence system, vendored under MIT with local fixes (paths, CSV quoting,
  docstrings, and a compliance post-filter inside the generator). Local notice: [`ui-ux-pro-max/LICENSE`](ui-ux-pro-max/LICENSE). Consider [supporting their project](https://paypal.me/uiuxpromax).
- Inspired by MUI, shadcn/ui, Radix, Headless UI, Material Design 3, Apple HIG, IBM Carbon,
  NNG, Refactoring UI, Every-Layout, Tailwind UI, Ant Design, Chakra UI, Josh Comeau,
  Emil Kowalski, and [Adrian Krebs](https://slop-detect.com/).
- The opt-in craft tier's weights follow the Awwwards evaluation system
  (Design 40 · Usability 30 · Creativity 20 · Content 10).

## License

MIT — see [LICENSE](LICENSE). UI/UX Pro Max is MIT licensed
(see their [LICENSE](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/LICENSE)).
