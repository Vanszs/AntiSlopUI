# Mandatory Post-Filter

Treat generated recommendations as proposals. Apply these substitutions before code; the cited gate/catalog section remains authoritative.

| Vendor output | Substitute | Authority |
|---|---|---|
| SaaS `Glassmorphism + Flat Design` | Choose an evidence-supported allowed style; record override | ui-reasoning.csv; gate K4 |
| Glass/transparent cards | Solid surface; at most one image-overlay surface with fallback | gate K4 |
| Violet/indigo background tint | Neutral surface or supported brand/domain tint | gate C1 |
| `indigo-950` text | High-contrast neutral or supported brand text; verify contrast | gate C7 |
| `Playfair Display + Inter` | Non-banned display/body pairing supported by typography results | catalog T3 |
| Mono/technical display face | Reserve for code; choose a suitable display face | Typography catalog |
| Prose effect strings | Treat as descriptions, not implementation instructions; use a concrete supported effect | Styles catalog |
| Vendor prose motion duration | Apply the motion table; do not infer permission from prose | `anti-ai-slop-ui-ux/SKILL.md` §Motion |

Record each substitution exactly: `OVERRIDE: <from> → <to> [<reason>]`.

Determinism: same query + same `-p` = identical output.
Different `-p` may change the substituted hue; without `-p`, the query seeds it.
The substitution set is a fixed 8-hue list; the seed is unused when the vendor palette is already legal.
