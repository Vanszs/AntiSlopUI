# Mandatory Post-Filter

Treat generated recommendations as proposals. Apply these substitutions before code; the cited gate/catalog section remains authoritative. This table covers the substitutions the generator applies in code; if a value is absent here and violates the frozen contract in `SKILL.md`, treat it as banned and record the substitution.

| Vendor output | Substitute | Authority |
|---|---|---|
| SaaS `Glassmorphism + Flat Design` | Choose an evidence-supported allowed style; record override | ui-reasoning.csv; catalog K4 |
| Glass/transparent cards | Solid surface; at most one image-overlay surface with fallback | catalog K4 |
| Violet/indigo background tint | Neutral surface or supported brand/domain tint | gate C1 |
| `indigo-950` text | High-contrast neutral or supported brand text; verify contrast | gate C7 |
| `Playfair Display + Inter` | Non-banned display/body pairing supported by typography results | catalog T11 |
| Display face not in this table (Satoshi, Clash, Orbitron, Syne, Lora, Archivo, same-face pairings) | Never keep a vendor display face. Use: editorial/luxury/culture → Fraunces; software/data/developer → Bricolage Grotesque; neutral B2B/enterprise/docs → Bricolage Grotesque; playful/consumer/education → Cabinet Grotesk. Ambiguous → Bricolage Grotesque. Body: any single non-display face; Inter only alongside a different display face | Deterministic table (inlined) |
| Mono/technical display face | Reserve for code; choose a suitable display face | Typography catalog |
| Prose effect strings | Treat as descriptions, not implementation instructions; use a concrete supported effect | Styles catalog |
| Vendor prose motion duration | Apply the motion table; do not infer permission from prose | `anti-ai-slop-ui-ux/SKILL.md` §Motion |

Record each substitution exactly: `OVERRIDE: <from> → <to> [<reason>]`.

Determinism: the hue is decided by the product domain in the query. `-p` names the output folder and never changes the palette. Recommendations are deterministic for a given query; persisted artifacts additionally embed a generation timestamp.
The substitution set is a fixed 7-hue list. The primary is always the domain hue. Secondary and CTA derive from it: a banned secondary collapses to the primary, and a second banned accent takes the next hue in the fixed list.
