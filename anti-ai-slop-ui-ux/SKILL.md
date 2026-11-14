---
name: anti-ai-slop-ui-ux
description: "Hard ban filter for AI-slop UI defaults. Load FIRST, before any UI code is written or reviewed; it owns the ban list that component-reference-design and ui-ux-pro-max defer to. Bans purple/indigo accent gradients, gradient-text headlines, Inter-everywhere, 3-card grids, glassmorphism, emoji icons, pill CTAs, hover:scale-105, invented metrics, and missing prefers-reduced-motion, with severity tiers and a PASS/FAIL pre-delivery audit. Not for backend, API, data-pipeline, or docs-only work."
license: MIT
metadata:
  author: "b4r7x"
  version: "2.2.0"
  updated: "2026-11-14"
  references: "references/slop-uiux-patterns.md, references/slop-code-patterns.md"
---

# Anti-AI-Slop UI/UX — Deterministic Filter

## STOP — run the audit

Load this filter before UI work. Before delivery, report `PASS`, `FAIL`, or `N-A` plus an evidence pointer for every audit item. `N-A` is allowed only when the component does not exist on the page. Any P0 failure blocks delivery; **3+ tells = block and regenerate**.

## Precedence & conflict resolution

This skill owns the suite's UI ban list. Its rules override conflicting recommendations from the companion skills and CSVs.
- `ui-ux-pro-max/scripts/search.py --design-system` may recommend indigo `#6366F1`; reject unless it appears in user-supplied brand assets.
- `ui-ux-pro-max` recommends Glassmorphism for SaaS in `ui-reasoning.csv`; reject it Glass is an explicit exception only as ONE surface over imagery, `bg-white/80` or stronger, with an `@supports` fallback; state the exception.
- Vendor palettes may include banned indigo/purple hexes, backgrounds, or text tints; reject unless user-supplied brand assets contain the value.
- Playfair Display + Inter pairing remains banned.
- `hover:scale-105` remains banned. When a recommendation conflicts with a P0/HIGH ban, the ban wins.

## How to use

### Design/build
1. Read this skill. Use the gate table below, then consult the relevant UI catalog section for details.
2. Choose color, type, layout, copy, and motion deliberately; document exceptions using the required `OVERRIDE:` format.
3. Route code-level review to `references/slop-code-patterns.md`; route visual tells to `references/slop-uiux-patterns.md`.
4. Run the detailed pre-delivery audit.

### Review/refactor
1. Count tells using the definition below; fix all P0/HIGH findings.
2. Report each finding as `tell → why-slop → fix → severity` with evidence.
3. **3+ tells = block and regenerate.** No secondary threshold.

## Deterministic terms

A **tell** is one row in `references/slop-uiux-patterns.md` sections 1–10 with severity exactly one of `P0`, `HIGH`, `MEDIUM`, or `LOW`. Severity vocabulary is closed. Count each matching catalog row once. **3+ tells = block and regenerate.**

A banned purple, indigo, or other prohibited hue is “real brand” only when present in user-supplied brand assets: a logo file, existing CSS tokens, or brand PDF. Otherwise it is a violation. Record an exception exactly as `OVERRIDE: <value> → <value> [brand: <source>]`.

Placeholder content is allowed only when visibly labeled and structurally distinct, e.g. `<figcaption>Sample data — replace before launch</figcaption>` or `data-sample="true"`. `[placeholder]`, lorem ipsum, and TODO remain banned. Unknown social proof or metrics must be omitted and recorded `NO-PROOF: user supplied none`; omission is compliant, invention is P0.

## Hard gates

| ID | Banned | Compliant default | Severity |
|---|---|---|---|
| H2 | Gradient-text headline | Solid, high-contrast headline | P0 |
| C1 | Purple/indigo primary accent without supplied brand asset | Use a non-purple/indigo brand hue | P0 |
| C2 | Canonical purple/indigo or blue/cyan gradient combinations | Flat color or compliant intentional gradient | P0 |
| C7 | Low-contrast body text | Verify WCAG AA contrast | P0 |
| K6 | Purple left-border card accent | Remove; reserve left borders for semantic alerts | P0 |
| MO10 | Missing reduced-motion support | Gate animation; static under reduced motion | P0 |
| T1 | Inter/Geist for display and body without a second face | Pair a distinctive display face with body type | HIGH |
| K1 | Identical 3-column feature cards | Vary size/structure or use a list/table | HIGH |
| K3 | `hover:scale-105` in a grid | Shadow/border color transition | HIGH |
| I1 | Emoji as functional icons | Consistent SVG icon set | HIGH |
| B3 | Pill buttons everywhere | `rounded-md`/`rounded-lg`; pills only semantic | HIGH |
| N1 | Floating glassmorphic navbar | Fixed solid navbar with border | HIGH |

For the full catalog: `grep -n '^## \|^| K' references/slop-uiux-patterns.md`.

## The five axes

| Axis | Banned default | Required action |
|---|---|---|
| Color | Purple/indigo accent, purple/blue-cyan default gradients | Choose brand-safe palette; document valid brand overrides |
| Type | Inter-everywhere, gradient headlines, Playfair + Inter | Distinctive display face; solid headline; restrained weights |
| Layout | Centered sameness, repetitive three-column grids | Vary structure and emphasis by content |
| Copy | Hype, generic CTAs, invented proof | Specific copy; omit unknown proof and record `NO-PROOF` |
| Motion | Gratuitous motion or missing reduced-motion behavior | Follow the sole motion table; animate only to support a task |

## Motion table

| Motion class | Duration / behavior |
|---|---|
| Hover | 100–150ms |
| Entrances and exits | 150–250ms |
| Page/route transitions | ≤300ms |
| Craft-tier exception | ≤400ms ONLY with `OVERRIDE:` |
| Ambient animation | Maximum 1; pause on hover/focus; render static under `prefers-reduced-motion` |

All motion examples elsewhere use 200ms. Outside this table, point here instead of restating durations. Respect `prefers-reduced-motion`; use transform/opacity where appropriate.

## Text measure

Use `max-w-3xl` for prose containers, `max-w-prose` for paragraphs, and `max-w-6xl` for grids. A column in a two-column hero split may use `max-w-2xl`.

## Brand, proof, and placeholder rules

Apply the deterministic terms above. Do not invent metrics, testimonials, customer logos, benchmarks, or other social proof. Record absent user proof as `NO-PROOF: user supplied none`. Labeled sample data is permitted only in the specified visible/structurally distinct form; unlabeled placeholders, lorem ipsum, and TODO are banned.

## If You Cannot Run Commands

If shell access is unavailable, do NOT read CSVs. Use `component-reference-design` patterns plus the authored defaults in this suite, and state that limitation in the output.

## Pre-Delivery Slop Audit

Report `PASS`, `FAIL`, or `N-A` plus an evidence pointer per item. `N-A` is valid only when that component does not exist on the page. A P0 failure blocks delivery; **3+ tells = block and regenerate**.

**Color & type**
- [ ] No banned purple/indigo without user-supplied brand asset; any exception recorded as `OVERRIDE:` with source.
- [ ] No gradient text; display/body type pairing avoids banned defaults.
- [ ] Body text meets WCAG AA contrast.

**Layout & cards**
- [ ] Structure varies by content; no repetitive identical three-column card grids.
- [ ] No banned glass surfaces; permitted imagery exception meets all stated conditions.
- [ ] No emoji functional icons or banned left-border accents.

**Copy & proof**
- [ ] No banned hype/generic copy or `[placeholder]`, lorem ipsum, TODO.
- [ ] Unknown metrics/social proof omitted with `NO-PROOF: user supplied none`.
- [ ] Any sample content is visibly labeled and structurally distinct.

**Motion & accessibility**
- [ ] Motion follows the motion table; reduced-motion renders static.
- [ ] No `hover:scale-105`; focus states visible; forms have labels and validation states.
- [ ] Images have appropriate alt text; color is not the only indicator.

**Gestalt**
- [ ] Could a competitor swap the logo without notice? If yes, FAIL.
- [ ] Counted catalog tells; **3+ tells = block and regenerate**.

## References

- `references/slop-uiux-patterns.md` — Open for visual/UI tell definitions, severity, fixes, and compliant examples.
- `references/slop-code-patterns.md` — Open for React/TypeScript/Next.js code-level tells and review patterns.

## Output expectations

Report the audit status and evidence. Explain every `OVERRIDE:` and `NO-PROOF:` record. Design decisions must be content-specific; do not claim completion when any blocking P0 failure remains.
