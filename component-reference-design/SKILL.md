---
name: component-reference-design
description: "Positive pattern library: copy-pasteable, accessible Tailwind markup for layouts, typography, card variants, buttons, forms, navigation, data display, overlays, charts, dashboards, and an opt-in award-tier rubric. Load only when you need a concrete pattern for UI you are already building, and load it alongside anti-ai-slop-ui-ux (which owns the ban list). Not a starting point for deciding whether to build UI, and not for backend or data work."
metadata:
  author: "Vanszs (catalog by b4r7x)"
  version: "1.2.0"
  suite_version: "2.2.0"
  updated: "2026-11-14"
  references: "references/layouts.md, references/typography.md, references/components.md, references/animation.md, references/design-systems.md, references/charts.md, references/dashboards.md, references/awards-craft.md"
license: MIT
---

# Component Reference Design — Positive Pattern Library

## Purpose
A **reference of what good looks like**, sourced from trusted design systems.
Where `Anti-AI-Slop` tells you what to AVOID, this skill shows you what to BUILD:
modern layouts, varied section anatomies, proven type systems, every card and
component variant, and tasteful accessible motion — all copy-pasteable and a11y-correct.

> Use the two skills together: **Anti-AI-Slop = the filter, Component Reference = the palette.**

## How To Use This Skill
1. Identify what you're building (a page layout? a card? a form? a nav?).
2. Open the matching reference file (see Category Map) and pick a pattern by its
   **when-to-use** note — not by "what looks coolest in isolation."
3. Copy the concrete markup; swap in real content, brand color, and a non-Inter
   display font.
4. Apply the **Anti-Monotony Rules** below so the page doesn't feel templated.
5. Run the local ship gate below before shipping. If `anti-ai-slop-ui-ux` is installed, its audit supersedes this one.

## Ship gate (use when the filter is not installed)

Record each item as **PASS / FAIL / N-A + evidence**:
1. No purple/indigo accent.
2. No gradient-text headline.
3. No glass surface except one over imagery with an `@supports` fallback.
4. Motion stays within the canonical table; reduced-motion renders static.
5. No hover enlargement on any interactive element (shadow, colour or border feedback only).
6. Radius uses a scale, not one radius everywhere.
7. Shipped palette meets WCAG AA contrast.
8. No invented proof; record `NO-PROOF` when evidence was not supplied.

## Precedence & Conflict Resolution
This skill is the palette; `Anti-AI-Slop` is the filter and authority. Its bans win every conflict; state the compliant substitution.
Glass is an explicit exception only as ONE surface over imagery, `bg-white/80` or stronger, with an `@supports` fallback; state the exception.
Vary container widths by content; a grid may repeat `max-w-6xl`, but not every section. K3 bans hover enlargement in a grid; avoid scaling hover elsewhere too. Never use `transition-all`; pills are for tags and avatars only.

### Craft tier is opt-in
`references/awards-craft.md` is the only file allowed to raise the craft ceiling, and only when the user explicitly asks for premium / award-grade / "wow" / studio / launch work. It carries a scored rubric (Design 40 · Usability 30 · Creativity 20 · Content 10), hard performance and a11y gates that deny the tier on failure, and a cost table for every craft pattern. It never buys a ban, and its two permitted relaxations are declared in `OVERRIDE:` form. Do not load it for dashboards, admin tools, docs, checkout, or forms.

## Context Budget
Always load this `SKILL.md` first.
Open at most ONE reference file per task; two when combining dashboards + charts, or when auditing (the tell catalog counts as the second). Never read a whole reference file: read its Contents TOC, grep the heading, then read that range only. Mandatory recipe:
```sh
# run from this skill's directory (cd component-reference-design)
grep -nE '^#{1,2} ' references/layouts.md   # every section heading, h1 or h2
sed -n 'START,ENDp' references/layouts.md   # END = the next match's line number minus 1
```

Motion values here defer to the canonical table in `anti-ai-slop-ui-ux/SKILL.md`; the numbers are restated so this skill stays usable when installed alone: hovers 100–150ms, entrances/exits 150–250ms, page/route ≤300ms. Craft tier may use 400ms only with `OVERRIDE: ... [craft tier §5]`.
Use Category Map to select the narrowest relevant reference.

## Category Map (where to look)

| You're building… | Open | Contains |
|------------------|------|----------|
| Page/app skeleton, grid, responsive structure | `references/layouts.md` | 25 numbered patterns: sections 1–16 core skeletons (holy-grail, sidebar shell, dashboard, split-screen, full-bleed, bento, masonry, magazine, asymmetric, sticky-aside, multi-column, card grid, container queries, Z/F, cover, Every-Layout primitives) + sections 17–25 extended (hero variants, SaaS flow, dashboard shell, bento recipes, e-commerce, editorial, auth/pricing, mobile/PWA, modern CSS) |
| Type scale, font pairing, fluid type | `references/typography.md` | 8+ display+body pairings, modular scales (1.2/1.25/1.333), clamp() recipes, per-role leading/measure/tracking, Tailwind config, MUI/MD3/Apple/Carbon scales compared |
| Card, button, form, nav, table, list, badge | `references/components.md` | Card variants (17), buttons (10), form controls (13), navigation (13), data-display (16) |
| Modal, drawer, toast, tooltip, popover, animation | `references/animation.md` | Overlay/feedback components + tasteful motion patterns (timing, easing, reduced-motion, 13 motion recipes) |
| Choosing a library / design tokens | `references/design-systems.md` | 18 design-system index (ecosystem, styling, a11y, theming, license, URL) + W3C DTCG tokens + decision matrix |
| Charts, graphs, KPI cards, sparklines, data-viz | `references/charts.md` | Beautiful modern Recharts patterns: product-derived hue/Okabe-Ito/OKLCH color systems, premium chrome (custom tooltip/legend/axes/grid), bar/line/area/donut/radial, KPI+sparkline cards, specialty (heatmap/treemap/funnel/radar/scatter/bullet/waffle), motion, dark-mode/responsive, a11y, 15-point anti-slop scan |
| Admin dashboard — app shell, sidebar, topbar, widgets, tables, filters | `references/dashboards.md` | Modern clean admin dashboard: 15 clean-dashboard principles, app shell (grid sidebar+header), sidebar nav (collapsible/rail/groups/footer), topbar (breadcrumb/⌘K search/notif/avatar/org-switcher), command palette, grid composition (KPI→hero+side→table, bento), KPI/stat cards (delta inversion), chart placement/chrome, filters & toolbar (date-range/segmented/chips/saved-views), data table (TanStack/density/sort/selection/pagination), all states (skeleton/empty/error/zero), 3-tier color tokens + dark, anti-pattern cheat sheet |
| Award-grade / premium / studio page (opt-in only) | `references/awards-craft.md` | Scored rubric (Awwwards weights), hard perf+a11y gates that deny the tier, cost table for kinetic type / transitions / scroll choreography / 3D / video / custom cursor, award-theatre anti-patterns, the only two permitted relaxations |

## The Anti-Monotony Rules (apply to every multi-section page)
1. **Never repeat the same section anatomy consecutively.** Vary: centered → split → bento → stats-bar → full-bleed → alternating.
2. **Vary container widths by content** — text measures, grid widths, and full-bleed sections should suit their content; include ≥1 full-bleed break per page.
3. **Vary section padding** — hero `py-32`, features `py-16`, CTA `py-12`. Never one uniform `py-20`.
4. **One dominant element per section** — size/weight ≥1.5× its neighbours.
5. **Break rhythm every 2–3 sections** — a full-bleed image, colour block, or stats bar.
6. **Mix grid structures** — 2-col, 4-col, asymmetric spans; a bento needs a real 2×2 dominant cell (else it's just a card grid).
7. **≥2 deliberate asymmetric moments per page** — unequal columns, off-centre headings, left-aligned text.

## Proven Storytelling Sequence (Evil Martians, 100 dev-tool landing pages)
`Hero (what is it?) → Trust (who uses it? — omit and record `NO-PROOF: user supplied none` when no evidence exists) → Features (what/why?) → Social proof (what do users say? — omit and record `NO-PROOF: user supplied none` when no evidence exists) → Supporting (FAQ / comparison / pricing) → Final CTA (what now?)` — with each section using a DIFFERENT anatomy.

## Non-Negotiable Quality Bar (every pattern here already follows it)
- **Semantic HTML first** — `<table>`, `<ul>`, `<dl>`, `<dialog>`, `<nav>`, `<button>`, `<a>` before div-soup.
- **Accessible by default** — labels wired, `aria-*` present, focus-visible rings, keyboard reachable, focus trap on modals.
- **`prefers-reduced-motion`** gates every spatial animation.
- **Radius is a scale** — inputs/buttons `rounded-md`, cards `rounded-lg`, modals `rounded-xl`, pills `rounded-full`.
- **Type** — distinctive display font (NOT Inter-everywhere), modular scale, `max-w-prose` body, 2–3 weights.
- **Motion budget** — hover 100–150ms, entrances/exits 150–250ms, page/route ≤300ms; 400ms only with `OVERRIDE:`. Use `transform`+`opacity` only.
- **WCAG AA contrast** — 4.5:1 body, 3:1 large/UI; test light and dark when a dark palette is supplied; otherwise ship light and state it.
- **Text measure** — prose `max-w-3xl`, paragraphs `max-w-prose`, grids `max-w-6xl`; a 2-column hero split may use `max-w-2xl`.

## Trusted Sources (full index in `references/design-systems.md`)
MUI · shadcn/ui · Radix Primitives & Themes · Headless UI · Ant Design · Chakra UI ·
Mantine · Tailwind UI · Material Design 3 · Apple HIG · IBM Carbon · Atlassian ·
Polaris (Shopify) · Fluent (Microsoft) · Base Web (Uber) · Park UI / Ark UI · daisyUI ·
Tremor · TanStack Table · Recharts · NNG · Refactoring UI · Every-Layout · Josh Comeau ·
Framer Motion / Motion · Emil Kowalski (Sonner, Vaul) · cmdk · W3C WAI-ARIA APG · W3C DTCG.

## Output Expectations
Use these patterns as a starting point, then make ≥1 deliberate, content-specific
choice per section (color, type, layout variation). The result should read as
**intentional, branded, varied, accessible, production-ready** — never templated.
