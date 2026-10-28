# get-a-flat

Claude Code skills for renting a flat in France. Claude checks listings on Gens de Confiance, Leboncoin, CDC Habitat, SeLoger and Jinka in **your** Chrome, filters them against your criteria (budget, size, energy rating (DPE), commute to work), notifies your phone, and drafts messages to landlords. Nothing is sent until you approve it.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- The **Claude in Chrome** extension, in the Chrome profile where you are logged in to the listing sites (Claude never types your passwords)
- Python 3 (for `scripts/maps.py`, standard library only)
- A computer that stays on while monitoring runs

## Getting started

```bash
git clone <this repo> && cd get-a-flat
claude
```

Then, in Claude:

1. `/setup-search`: Claude asks for your criteria and creates `data/criteria.md`, `data/messages.md` and `data/seen.md`.
2. `/flat-watch`: one search pass. To repeat it, say "run the watch every 30 min".
3. `/remote-control`: follow and approve from the Claude app on your phone.
4. "apply for the Montreuil one" or "reply to the landlord: ...": `contact-listing` drafts the message, you approve it, Claude sends it.

## Skills

| Skill | What it does |
|---|---|
| `setup-search` | Collects your criteria and message template, prepares `data/` |
| `flat-watch` | Reads listings, rules out mismatches, adds a Google Maps directions link, notifies you |
| `contact-listing` | Drafts messages to landlords and sends them once you approve |

Per-site recipes are in `.claude/skills/flat-watch/sites.md`: search URLs, where to find the DPE, and a workaround for pages that never finish loading. The SeLoger and Jinka sections have not been tested yet.

## Safeguards

- Claude contacts no one and applies nowhere without your explicit "yes", unless you have written `mode: auto` in your criteria.
- Claude never ticks a commitment box (fees) or sends documents from your rental file without your consent, even in auto mode.
- On a captcha or logout, Claude stops and tells you. It does not try to get around it.
- Automating Leboncoin or SeLoger may breach their terms of use, and your account could be suspended.

## Privacy

Everything about you (criteria, message, seen listings) stays in `data/`, which git ignores.

The skills are written in English, but the sites, listings and landlord messages are in French. Keywords to match (e.g. « bail mobilité ») and message templates stay in French.
