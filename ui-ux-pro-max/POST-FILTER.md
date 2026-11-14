# Mandatory Post-Filter

Post-process all `--design-system` output before it reaches code. The vendor database is statistically averaged and can recommend values banned by this suite. Anti-AI-Slop owns the ban list and wins every conflict.

| Vendor output | Why it fails | Substitution |
|---|---|---|
| Primary `#6366F1` / `#8B5CF6` or indigo, violet, purple accents | P0 ban | Derive the hue from the product's real domain or brand, not a fixed substitute menu; state why it fits. Deep teal `#0F766E`, ink `#111827`, clay `#B45309`, moss `#3F6212`, slate-blue `#334155`, oxblood `#7F1D1D` are examples only. |
| SaaS recommendation `Glassmorphism + Flat Design` (`ui-reasoning.csv`) | Glassmorphism banned | Substitute an allowed style based on product evidence; record an `OVERRIDE`. |
| Violet-50 / indigo-50 background tints | Purple-family accents banned | Use a neutral surface or a domain/brand-derived tint; state why the hue fits. |
| Indigo-950 text | Purple-family accents banned | Use a high-contrast neutral or domain/brand-derived text color; verify contrast. |
| `Playfair Display + Inter` pairing | Banned pairing | Use a non-banned display/body pairing supported by the typography results. |
| Fira Code used as a display face | Monospace is not a display-face default | Reserve Fira Code for code; choose a suitable display face. |
| Uniform `max-w-6xl` / `max-w-7xl` on every section | Conflicts with vary-container-widths | Vary widths by content; use text `max-w-3xl`, grids `max-w-6xl`, and at least one full-bleed break. |
| Floating navbar `top-4 left-4 right-4` | Conflicts with fixed solid nav | Use `fixed top-0 border-b`; offset content for nav height. |
| Glassmorphism or `bg-white/10` glass cards | Banned | Use solid surfaces. At most ONE `bg-white/80` surface over imagery, with an `@supports` fallback. |
| `hover:scale-105` or layout-shifting hover | Causes layout shift | Use `hover:shadow-sm`, color, or border feedback only. |
| `transition-all` | Animates unintended properties | Name specific properties; motion limits live in the table in `anti-ai-slop-ui-ux/SKILL.md`. |
| Hover duration above 150ms | Sluggish interaction | Keep hover within the motion table in `anti-ai-slop-ui-ux/SKILL.md`. |
| Typewriter or streaming text effects | Distracting simulated typing | Show complete text; use a real progress/status indicator only when work is actually pending. |
| Parallax with multiple layers | Excess motion and performance cost | Remove parallax; use static depth cues. |
| Inter-everywhere typography | Fails non-Inter display-face pairing | Pair a non-Inter display face: Fraunces, Bricolage Grotesque, Satoshi, or Cabinet Grotesk. |
| Gradient-text headline | Conflicts with solid high-contrast text | Use a solid, high-contrast headline. |
| “Trusted by N+ teams” or other invented metric copy | Unsupported factual claim | Use real evidence or clearly marked placeholder copy. |

Record every substitution exactly as: `OVERRIDE: <vendor value> → <substituted value> (<ban rule>)`. This makes the diff auditable.
