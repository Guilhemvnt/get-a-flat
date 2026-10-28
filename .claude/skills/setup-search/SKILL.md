---
name: setup-search
description: Sets up a rental search (criteria, contact message, seen-listings file) in data/. Run once before /flat-watch, or when the user wants to change their criteria. Triggers: "I'm looking for a flat", "set up my search", "change my criteria".
---

# Set up the search

All paths are relative to the repo root (`git rev-parse --show-toplevel`): `cd` there first. All personal state lives in `data/` (git-ignored). Never write personal info anywhere else in the repo.

## 1. Criteria

If `data/criteria.md` exists (the user wants to change criteria), edit only the lines they mention, and date them. Steps 2 and 3 still run but only create what is missing. Otherwise ask the user (one grouped, copy-pasteable question):

```
Type: long-term rental (purchase not supported)
Property: flat / house
Workplace (for commute): ...
Max commute by public transport: ... (e.g. 1h)
Area: cities, arrondissements, départements
Search centre: city + postcode, and radius in km (e.g. Paris 75001, 15 km)
Max rent: ... € (charges included?)
Min size: ... m²   Min rooms: ...
Accepted DPE: e.g. A to D
Deal-breakers: e.g. flatshare, room in a private home, sublet, bail mobilité, short-term
Avoid (flag, don't exclude): ...
Implausible price (likely scam/sublet): below ... €/month
Sites: Gens de Confiance / Leboncoin / CDC Habitat / SeLoger / Jinka / other
Check frequency: 15 / 30 min, time window
Auto-send cap (only used if you later enable auto mode): ... contacts / day
```

Write the answer to `data/criteria.md`, starting from `templates/criteria.md`; replace every template value with the user's answer. Fill `lat`/`lng` from the search centre (look it up, e.g. on Google Maps). Date every rule added later ("added YYYY-MM-DD").

## 2. Contact message

If `data/messages.md` is missing, copy `templates/messages.md` there. Ask the user to fill in the "profile" block: full name, job situation as they want it worded, guarantor / Visale, and where their rental file is ready. **Status stays PENDING until the user has approved the text word for word.**

## 3. Seen listings

If `data/seen.md` is missing, copy `templates/seen.md` there. Never overwrite an existing one: it holds the watch history.

## 4. Prerequisites to check with the user

- The **Claude in Chrome** extension is installed and connected, in the Chrome profile where the user is logged in to the sites. Never type their passwords: they log in themselves.
- Open one tab per site to check the login. Leboncoin, Gens de Confiance and Jinka need an account to contact landlords or see alerts; CDC Habitat search is public.
- The computer must stay on (no sleep) with Chrome open. On Linux: `systemd-inhibit --what=sleep:idle sleep infinity`.
- To follow from a phone: run `/remote-control` in the session; PushNotifications then reach the mobile app.

Then offer to run `/flat-watch`.
