---
name: flat-watch
description: One monitoring pass over rental listings (Gens de Confiance, Leboncoin, CDC Habitat, SeLoger, Jinka) through Claude in Chrome — filter against data/criteria.md, dedupe via data/seen.md, directions link, notification. Triggers: "/flat-watch", "look for flats", "run the watch", recurring task. Never contacts anyone, except through contact-listing's auto mode when the user enabled it.
---

# Flat watch: one pass

Prerequisites: `data/criteria.md` and `data/seen.md` exist (otherwise run `setup-search`). Re-read them every pass, they change. All paths are relative to the repo root (`git rev-parse --show-toplevel`): `cd` there first.

## Fixed rules

- **Never apply or contact anyone in this skill.** Filter + notify only; contacting goes through `contact-listing` (step 9).
- **One new tab**, closed at the end. Never close the user's other tabs.
- **Captcha, logout, repeated error** on a site: stop that site (don't work around it), carry on with the others, and notify.
- Only process listings **missing from seen.md** (ids are site-prefixed, search the whole file); step 6 is the only exception.
- Skip listings **older than 2 weeks** (probably let already → `OLD` line) and listings with an **implausible price** (below the `Implausible price` in `criteria.md`: often a sublet or a scam).

## Steps

1. Load the Chrome tools in a single ToolSearch (`tabs_context_mcp, tabs_create_mcp, tabs_close_mcp, navigate, javascript_tool, find, get_page_text, browser_batch, computer`, plus `PushNotification` and `CronCreate`), then call `tabs_context_mcp`.
2. For each site in `criteria.md`, follow its recipe in [sites.md](sites.md).
3. Classify each new listing:
   - **EXCLUDED** — short reason: DPE outside the accepted letters, below min size/rooms, sublet, bail mobilité, flatshare, room in a private home, short-term, too far, implausible price.
   - **BORDERLINE** — commute in the BORDERLINE band from `criteria.md`, or a criterion right at the limit.
   - **TO_CHECK** — DPE missing, doubtful neighbourhood, ambiguous type (title says « chambre »…), charges not stated.
   - **OK** — everything passes.
4. Commute: estimate it by public transport to the workplace (line(s) + duration). For every OK/BORDERLINE/TO_CHECK, generate the link:
   `python3 "$(git rev-parse --show-toplevel)/scripts/maps.py" "<origin>" "<workplace>"`
   Use the most precise origin available: address > `lat,lng` > `neighbourhood, city postcode`.
5. Add **every** new listing to `data/seen.md` (format at the top of the file), including EXCLUDED and OLD ones, so they are never read again.
6. Seen OK/BORDERLINE/TO_CHECK/CONTACTED listings absent from this pass's results may just be on page 2: open their page (max 5 per pass) and only if the site says removed/unavailable, add a comment ("let").
7. Report: a table `Where | Size | Rent incl. | DPE | Commute | listing · directions`, then the TO_CHECK ones with what to ask, then one line for the excluded ones.
8. If there is at least one **new OK or TO_CHECK**: send a short `PushNotification` (city, m², rent, DPE). Otherwise, nothing.
9. For OK listings under 48h old: if `criteria.md` contains `mode: auto`, run `contact-listing` in auto mode for each; otherwise offer it (don't run it on your own).

## Running on a schedule

Use `CronCreate` with the prompt `/flat-watch`, at the frequency in `criteria.md` (e.g. 8am-9pm every 30 min = `*/30 8-20 * * *` plus `0 21 * * *`; the hour field is inclusive, so `8-21` would also fire at 21:30). The task lives in the session: the terminal must stay open, the computer on, Chrome open. Tell the user it expires (7 days) and uses quota.
