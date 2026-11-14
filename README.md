# AntiSlopUI

![Version](https://img.shields.io/badge/version-2.1.0-blue?style=for-the-badge)
![3 Skills](https://img.shields.io/badge/skills-3-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
[![validate](https://github.com/Vanszs/AntiSlopUI/actions/workflows/validate.yml/badge.svg)](https://github.com/Vanszs/AntiSlopUI/actions/workflows/validate.yml)

A three-skill suite for AI coding agents that eliminates "AI slop" and produces
intentional, branded, accessible UI/UX — instead of the statistical-mean defaults
that make machine-generated interfaces instantly recognizable.

> If you could swap the logo with a competitor and nobody would notice — it's slop.

## The problem

LLMs generate UI by averaging across training data dominated by Tailwind docs,
shadcn/ui examples, abandoned repos with unchanged defaults, and 2020–2024 Dribbble
SaaS shots. Output **collapses toward the visual mean**: purple/indigo gradients,
Inter everywhere, centered dual-CTA heroes, 3-card feature grids, glassmorphism
navbars, and copy like "Supercharge your workflow."

That is structural, not a bug — every decision left unspecified gets filled with the
single most probable token. **The cure is deliberate, content-specific variation.**

## The suite

```
┌──────────────────────────────────────────────────────────────────┐
│  FILTER — Anti-AI-Slop                                           │
│  What to AVOID. Hard bans, severity tiers, pre-delivery audit.   │
│  AUTHORITY on conflicts.                                         │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  PALETTE — Component Reference Design                            │
│  What to BUILD. Copy-pasteable, accessible patterns from MUI,    │
│  shadcn, Radix, MD3, Apple HIG, Carbon, NNG, Refactoring UI.     │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  RESEARCH — UI/UX Pro Max                                        │
│  Design intelligence. Design-system generator over CSV data.     │
│  Output is a PROPOSAL — it must pass the post-filter.            │
└──────────────────────────────────────────────────────────────────┘
```

Filter out slop → build from proven patterns → research industry-specific solutions.

## Precedence & conflict policy

This is the rule that keeps the three skills from fighting each other. It is
deliberate and non-negotiable:

1. **`Anti-AI-Slop` is the authority.** It owns the ban list (P0/HIGH/MEDIUM/LOW).
2. **Palette patterns conform to it.** A pattern is never a license to ship a banned
   default; it is a starting point that must pass the filter.
3. **Research output is a proposal, not a verdict.** Every `--design-system` result
   goes through [`ui-ux-pro-max/POST-FILTER.md`](ui-ux-pro-max/POST-FILTER.md) before
   it reaches code. Known substitutions: indigo `#6366F1` primary → a brand-safe hue;
   uniform `max-w-7xl` → varied container widths; floating glass navbar → fixed solid
   nav; glassmorphism → solid surfaces; `hover:scale-105` → color/border/shadow.
4. **Craft is opt-in, not a bypass.** `component-reference-design/references/awards-craft.md`
   raises the ceiling only when the user asks for premium/award-grade work, and only
   after the filter audit passes. It may request exactly two relaxations (400ms hero
   choreography, one pausable ambient animation); both must be declared as
   `OVERRIDE:`. Its hard gates — LCP ≤2.5s, CLS ≤0.1, INP ≤200ms, reduced-motion
   parity, keyboard, 390px parity, contrast — deny the tier on any failure.
5. **Exceptions must be stated.** One glass surface over imagery, a real brand purple,
   a genuinely time-bound eyebrow badge — allowed, but say
   `OVERRIDE: <value> → <replacement> (<rule>)` so the decision is auditable.
6. **The pre-delivery audit runs last**, after palette and research have contributed.

If you load only one skill, load the filter. The other two are useless without it.

## Context budget

Skill files are dense on purpose and expensive to load whole. Read deliberately:

- **Always:** the `SKILL.md` of the skills relevant to the task (≤3 files).
- **On demand:** at most **one** reference file per task (two only when combining
  dashboards + charts). Grep to the section you need — do not read a 680-line
  reference file end to end.
- **Never:** load the CSVs by hand. Query them through `search.py` (2–3 targeted
  queries per task), not by reading the database.

## Installation

Each skill is a directory whose **name must match the `name` in its frontmatter**
(lowercase, hyphens only) — that is what agent platforms key on.

### Kiro (steering)

```bash
git clone https://github.com/Vanszs/AntiSlopUI.git
cp -r AntiSlopUI/anti-ai-slop-ui-ux your-project/.kiro/steering/
cp -r AntiSlopUI/component-reference-design your-project/.kiro/steering/
cp -r AntiSlopUI/ui-ux-pro-max your-project/.kiro/steering/
```

### Claude Code / Codex / opencode / Hermes (skills dirs)

Copy (or symlink) the skill directory into the platform's skills root:

```bash
git clone https://github.com/Vanszs/AntiSlopUI.git

# Claude Code
cp -r AntiSlopUI/anti-ai-slop-ui-ux ~/.claude/skills/anti-ai-slop-ui-ux

# Codex
cp -r AntiSlopUI/anti-ai-slop-ui-ux ~/.codex/skills/anti-ai-slop-ui-ux

# opencode
cp -r AntiSlopUI/anti-ai-slop-ui-ux ~/.config/opencode/skills/anti-ai-slop-ui-ux
```

Do the same for `component-reference-design` and `ui-ux-pro-max` if you want all
three. Symlinks work on all four platforms and keep a single source of truth:

```bash
ln -s "$PWD/AntiSlopUI/anti-ai-slop-ui-ux" ~/.claude/skills/anti-ai-slop-ui-ux
```

### Any other agent (AGENTS.md / CLAUDE.md pointer)

If your agent has no skills mechanism, point it at the file and make the constraint
explicit:

```markdown
## UI work
Read `anti-ai-slop-ui-ux/SKILL.md` (path relative to the clone) before writing any UI code. It is a hard
filter, not advice. For patterns, read at most one file from
`component-reference-design/references/`. Run the Pre-Delivery Slop Audit
and report PASS/FAIL per item with evidence.
```

### Prerequisites

Python 3.8+ is required **only** for the `ui-ux-pro-max` research tool:

```bash
python3 --version          # macOS: brew install python3
                           # Ubuntu/Debian: sudo apt install python3
                           # Windows: winget install Python.Python.3.12
```

The two other skills are pure Markdown and need nothing.

## Usage

### Workflow

1. **Ask** — request any UI/UX task (build, design, review, fix).
2. **Filter** — the ban list and instant-death signature set the hard boundaries.
3. **Palette** — pick a pattern by its *when-to-use* note, not by what looks coolest.
4. **Research** — generate an industry-specific design system, then post-filter it.
5. **Audit** — run the Pre-Delivery Slop Audit; one P0 FAIL blocks delivery.

### Example prompts

```
Build a landing page for my SaaS product
→ Filter: no purple gradients, no Inter-everywhere, no 3-card grid
→ Palette: asymmetric split hero, distinctive display font, varied section padding
→ Research: SaaS reasoning rules → post-filter any indigo/uniform-container output

Design a dashboard for healthcare analytics
→ Filter: no glassmorphism, no emoji icons, no left-border cards
→ Palette: dashboard app shell, TanStack Table, KPI cards with delta inversion
→ Research: healthcare reasoning rules, data-dense dashboard style
```

### Research tool

```bash
# Full design system (print)
python3 ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"

# Persist as MASTER.md + per-page overrides (writes design-system/, gitignored)
python3 ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system --persist -p "Ledger"

# Single domain
python3 ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style
python3 ui-ux-pro-max/scripts/search.py "heatmap" --domain chart

# Stack guidelines
python3 ui-ux-pro-max/scripts/search.py "form validation" --stack react
```

Paths above are repo-relative. If the skill is installed elsewhere (e.g.
`.kiro/steering/<skill-dir>`, `~/.claude/skills/<skill-dir>`), resolve
`ui-ux-pro-max/scripts/search.py` relative to the skill directory.

## What's inside

```
AntiSlopUI/
├── anti-ai-slop-ui-ux/                       # FILTER — what to AVOID (authority)
│   ├── SKILL.md                        # Instant-death signature, 5 slop axes,
│   │                                   # per-component bans, severity, audit
│   └── references/
│       ├── slop-uiux-patterns.md       # TELL → WHY-SLOP → FIX → SEVERITY catalog
│       └── slop-code-patterns.md       # Code-level slop (React/TSX/a11y A11Y1–23)
│
├── component-reference-design/         # PALETTE — what to BUILD
│   ├── SKILL.md                        # Category map, anti-monotony rules, quality bar
│   └── references/
│       ├── layouts.md                  # 16 layouts + 2025–2026 page skeletons
│       ├── typography.md               # Pairings, modular scales, clamp() recipes
│       ├── components.md               # 17 cards, 10 buttons, 13 forms, 13 nav, 16 data
│       ├── animation.md                # Overlays + 13 motion recipes
│       ├── design-systems.md           # 18-system index + W3C DTCG tokens
│       ├── charts.md                   # Recharts patterns + 15-point anti-slop scan
│       ├── dashboards.md               # Clean admin dashboard patterns (15 principles)
│       └── awards-craft.md             # OPT-IN craft tier: Awwwards-weighted rubric,
│                                        # hard perf/a11y gates, costed craft patterns
│
├── ui-ux-pro-max/                      # RESEARCH — design intelligence (vendored)
│   ├── SKILL.md                        # Workflow, path convention, post-filter step
│   ├── POST-FILTER.md                  # Vendor output → filter-compliant substitution
│   ├── data/                           # CSV databases (query via search.py)
│   ├── data/stacks/                    # Per-stack guidelines
│   └── scripts/                        # BM25-style search engine
│
├── scripts/
│   ├── validate.py                     # Structural validation (9 checks, exit code)
│   └── stats.py                        # Recompute + splice the stats block below
│
└── .github/workflows/validate.yml      # CI: runs validate.py on push/PR
```

## Verification

The repo validates itself — claims in this README are checked, not asserted:

```bash
python3 scripts/stats.py        # recompute the stats block from the CSVs
python3 scripts/stats.py --write# splice corrected numbers into this README
python3 scripts/validate.py     # 10 structural checks, non-zero exit on failure
```

What the validator enforces: (1) frontmatter spec compliance — `name` equals the
directory, lowercase-hyphen only, description ≥60 chars; (2) every
`metadata.references` path exists; (3) every markdown link resolves; (4) no stale
Kiro-only install paths; (5) no path mentioned in this README is missing; (6) the
stats table below matches the CSVs, computed with a real CSV parser rather than line
counts; (7) every stack file is listed; (8) the research tool still runs; (9) a
conflict guard that flags banned literals (`#6366F1`, `max-w-7xl`, `hover:scale-105`,
`transition-all`, …) appearing outside a ban context — the ban catalogue and the
vendored CSV data are exempt by design; (10) the craft-tier rubric weights are still
Design 40 · Usability 30 · Creativity 20 · Content 10 and sum to 100.

CI runs on every push and pull request.

## Stats

<!-- stats:begin -->
| Metric | Value |
| --- | ---: |
| Skills | 3 |
| Markdown files | 15 |
| Reference files | 10 |
| Reasoning rules | 100 |
| UI styles | 67 |
| Color palettes | 96 |
| Font pairings | 57 |
| UX guidelines | 99 |
| Chart types | 25 |
| Tech stacks | 13 |
<!-- stats:end -->

## Contributing

Contributions welcome. Useful directions:

- **New slop tells** as they emerge — add to `anti-ai-slop-ui-ux/references/slop-uiux-patterns.md`
  with tell, why-slop, fix, severity.
- **New patterns** — add to the matching `component-reference-design/references/*.md`
  with when-to-use, concrete Tailwind markup, and source.
- **Reasoning rules / styles / palettes** — `ui-ux-pro-max/data/*.csv`.
- **Stack coverage** — new `ui-ux-pro-max/data/stacks/*.csv`.

```bash
git clone https://github.com/Vanszs/AntiSlopUI.git
cd AntiSlopUI
git checkout -b feat/your-feature
# edit
python3 scripts/validate.py     # must exit 0 before you push
git commit -m "feat: description"
git push -u origin feat/your-feature
gh pr create
```

Rules of the house: no new claim without a validated number, no new ban without a
concrete FIX, no new reference file without a `when-to-use` column. If your change
introduces a conflict with the filter, the filter wins.

## Acknowledgments

**Vendored work:**

- **[UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** by
  [NextLevelBuilder](https://github.com/nextlevelbuilder) — the `ui-ux-pro-max/`
  directory contains their design intelligence system (reasoning rules, UI styles,
  font pairings, search engine), used as-is with permission. Consider
  [supporting their project](https://paypal.me/uiuxpromax).

**Inspired by:**

- [MUI](https://mui.com/), [shadcn/ui](https://ui.shadcn.com/),
  [Radix](https://www.radix-ui.com/), [Headless UI](https://headlessui.com/)
- [Material Design 3](https://m3.material.io/),
  [Apple HIG](https://developer.apple.com/design/human-interface-guidelines),
  [IBM Carbon](https://carbondesignsystem.com/)
- [NNG](https://www.nngroup.com/), [Refactoring UI](https://www.refactoringui.com/),
  [Every-Layout](https://every-layout.dev/)
- [Tailwind UI](https://tailwindui.com/), [Ant Design](https://ant.design/),
  [Chakra UI](https://chakra-ui.com/)
- [Josh Comeau](https://www.joshwcomeau.com/), [Emil Kowalski](https://emilkowal.ski/),
  [Adrian Krebs](https://slop-detect.com/)

## License

MIT — see [LICENSE](LICENSE). UI/UX Pro Max is also MIT licensed
(see their [LICENSE](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/LICENSE)).
