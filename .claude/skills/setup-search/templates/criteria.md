# Search criteria (<YYYY-MM-DD>)

<!-- Every <...> is filled by setup-search from the user's answers. Never keep a placeholder or invent a value: ask. -->

- Type: <long-term rental / ...>, <flat / house>
- Size: <MIN_M2> m² minimum, <MIN_ROOMS> rooms minimum
- Rent: <MAX_RENT> €/month max (<charges included / excluded>)
- Workplace: <ADDRESS OR STATION>
- Area: <cities, arrondissements, départements> (CDC Habitat places, CDC spelling: <e.g. Hauts-de-Seine; PARIS (75001,...,75020)>), < <MAX_COMMUTE> by public transport to the workplace
- Commute BORDERLINE band: <e.g. last 15 min before the max>
- Search centre: city: <City>, postcode: <Postcode>, lat: <LAT>, lng: <LNG>, radius_km: <RADIUS_KM>
- DPE: <accepted letters> (others are deal-breakers; missing DPE = TO_CHECK)
- Deal-breakers: <...>
- Avoid (flag as TO_CHECK, don't exclude): <...>
- Implausible price: below <...> €/month
- Sites: <subset of Gens de Confiance, Leboncoin, CDC Habitat, SeLoger, Jinka>
- url_seloger: <search URL copied from the site, if SeLoger>
- url_jinka: <Jinka alert URL, if Jinka>
- Frequency: every <N> min, <time window>

## Replying to listings
- Listing published more than 48h ago: notify only
- Listing under 48h old with status OK: draft the message from data/messages.md
- TO_CHECK / BORDERLINE: notify only
- Sending: only after the user's explicit approval (`validation` mode). Switch to `auto` only if the user writes it here:
  mode: validation
  cap: <N> contacts / day
