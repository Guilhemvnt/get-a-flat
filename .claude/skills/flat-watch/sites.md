# Per-site recipes (tested October 2026; sites change, so if a selector breaks, find the equivalent and update this file)

Replace `<RENT>`, `<SIZE>`, `<City>`, `<Postcode>`, `<LAT>`, `<LNG>`, `<RADIUS_KM>` with the values from `data/criteria.md` (Size, Rent, Search centre). `<RADIUS_M>` = `<RADIUS_KM>` × 1000. URL price filters are charges included: if the criteria's rent is charges excluded, use `<RENT>` = max rent + 15% and check the exact total on the listing.

Ids in seen.md carry a site prefix (see its header).

## Gens de Confiance (account required)

- Search, sorted by date:
  `https://gensdeconfiance.com/fr/ui/results?types=offering&maxPrice=<RENT>&minSquareMeters=<SIZE>&rentalTypes=home&category=realestate__rent&radius=<RADIUS_KM>&locationDisplayName=<City>%2C+France&lat=<LAT>&lon=<LNG>`
- **Always set `radius`**: without it the search only covers the centre (~50 results) and misses the suburbs. 15 km around Paris covers the inner suburbs.
- Listing: `https://gensdeconfiance.com/fr/ui/post/realestate__rent/<uuid>`; id in seen.md = first 8 chars.
- DPE is not shown in the list: open the listing, click « Voir tous les critères », DPE = first letter inside `[class*=_circle]` (none = not provided).
- Read the lease type in the criteria: « bail mobilité », « sous-location », « temporaire » → EXCLUDED.

## Leboncoin (DataDome anti-bot)

- Search, sorted by date:
  `https://www.leboncoin.fr/recherche?category=10&locations=<City>_<Postcode>__<LAT>_<LNG>_5000_<RADIUS_M>&real_estate_type=2&price=min-<RENT>&square=<SIZE>-max&sort=time&order=desc`
  (No `energy_rate` filter in the URL: it would drop listings without a DPE, which must be TO_CHECK. Filter DPE from the JSON. `real_estate_type=2` is flat, `1` is house.)
- Don't parse the HTML: with `javascript_tool`, read the `#__NEXT_DATA__` JSON and search it recursively for an `ads` array. Useful fields: `list_id`, `price[0]`, `subject`, `first_publication_date`, `attributes` (`square`, `energy_rate`, `furnished`, `charges_included`), `location` (`city_label`, `district`, `lat`, `lng`).
- Listing: `https://www.leboncoin.fr/ad/locations/<list_id>`. Directions origin = `lat,lng`.
- Title containing « chambre » / « colocation » → EXCLUDED or TO_CHECK.
- DataDome captcha → stop Leboncoin for this pass and notify. Automation may breach the terms of use: stick to one page per pass.

## CDC Habitat (social landlord, public search)

- The page **never finishes loading**: don't use `get_page_text` or long `browser_batch` calls on it.
- Navigate once to
  `https://www.cdc-habitat.fr/Recherche/show/lbLieu=<PLACE>%3B&nbLoyerMax=<RENT>&cdTypage=location&` (first PLACE)
  then, with `javascript_tool`, do a same-origin `fetch` of `/Recherche/show/lbLieu=<PLACE>%3B&nbLoyerMax=<RENT>&cdTypage=location&` for each PLACE = each CDC place listed in the Area line of `data/criteria.md`, URL-encoded. Places use CDC's own spelling: département name (`Hauts-de-Seine`, `Val-d'Oise`) or, for Paris, `PARIS (75001,75002,...,75020)`.
- Parse with `DOMParser`, keep the `<article>` elements that aren't « Stationnement » (parking), id = end of the `a[href*=annonces]` href.
- New listing: `fetch` its page, DPE in `img[alt^="DPE"]`, address in the text.
- CDC searches cover a whole département: exclude anything beyond the max commute.

## SeLoger (not tested yet: check on the first pass and complete this section)

- Search URL formats change often. On the first pass, ask the user to set the filters on the site (rental, flat, max rent, min size, area, sort by newest) and paste the resulting URL. Store it in `data/criteria.md` (`url_seloger:`) and reuse it every pass.
- First try reading the page's JSON data with `javascript_tool` (`#__NEXT_DATA__` or another `<script type="application/json">`). If there is none, use `get_page_text` on the list.
- Id in seen.md = the number at the end of the listing URL.
- DPE and charges are on the listing page (« Diagnostic de performance énergétique » section). Many listings go through agencies: flag agency fees when stated.
- Anti-bot captcha: same rule as Leboncoin. Stop the site for this pass and notify; one page per pass.

## Jinka (aggregator, account required; not tested yet)

- Jinka collects listings from several sites (SeLoger, Leboncoin, PAP, agencies…). The user creates an alert in Jinka with their criteria and pastes the alert URL. Store it in `data/criteria.md` (`url_jinka:`).
- Open that URL and read the list (page text or JSON). For each listing, get the **source site** and its link.
- **Dedupe**: the same listing may already be in seen.md under its source site. Match on the source site id/link first. Without one, a seen listing in the same city with m² within ±2 and rent within ±10% (charges may differ) is a *possible duplicate*: record it as TO_CHECK « possible duplicate of <id> » instead of dropping or re-notifying it. Record the line in the source site's section with that site's prefixed id when known, else in the Jinka section as `jinka:<id>`.
- DPE and lease type are often missing on Jinka: open the source listing to check them, otherwise classify as TO_CHECK.
- Contact happens on the source site, not on Jinka (see contact-listing).
