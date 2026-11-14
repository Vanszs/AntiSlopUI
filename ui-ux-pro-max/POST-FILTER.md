# Mandatory Post-Filter

Post-process all `--design-system` output before it reaches code. The vendor database is statistically averaged and can recommend values banned by this suite. Anti-AI-Slop owns the ban list and wins every conflict.

| Vendor output | Why it fails | Substitution |
|---|---|---|
| Primary `#6366F1` / `#8B5CF6` or indigo, violet, purple accents | P0 ban | Use a brand-safe neutral, earthy, or product-specific hue. Ready options: deep teal `#0F766E`, ink `#111827`, clay `#B45309`, moss `#3F6212`, slate-blue `#334155`, oxblood `#7F1D1D`. State the override. |
| Uniform `max-w-6xl` / `max-w-7xl` on every section | Conflicts with vary-container-widths | Vary widths by content; use text `max-w-3xl`, grids `max-w-6xl`, and at least one full-bleed break. |
| Floating navbar `top-4 left-4 right-4` | Conflicts with fixed solid nav | Use `fixed top-0 border-b`; offset content for nav height. |
| Glassmorphism or `bg-white/10` glass cards | Banned | Use solid surfaces. At most ONE `bg-white/80` surface over imagery, with an `@supports` fallback. |
| `hover:scale-105` or layout-shifting hover | Causes layout shift | Use `hover:shadow-sm`, color, or border feedback only. |
| `transition-all` | Animates unintended properties | Name specific properties; motion budget: hovers 100–150ms, entrances 200–300ms, exits faster, `transform`/`opacity` only. |
| Inter-everywhere typography | Fails non-Inter display-face pairing | Pair a non-Inter display face: Fraunces, Bricolage Grotesque, Satoshi, or Cabinet Grotesk. |
| Gradient-text headline | Conflicts with solid high-contrast text | Use a solid, high-contrast headline. |
| “Trusted by N+ teams” or other invented metric copy | Unsupported factual claim | Use real evidence or clearly marked placeholder copy. |

Record every substitution exactly as: `OVERRIDE: <vendor value> → <substituted value> (<ban rule>)`. This makes the diff auditable.
