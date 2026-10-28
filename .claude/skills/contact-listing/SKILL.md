---
name: contact-listing
description: Drafts (and sends only after explicit approval) a message to a landlord or agency about a listing found by flat-watch, or a reply to a message received. Triggers: "apply for ...", "write the message for ...", "reply to the landlord", "send it".
---

# Contact a listing

## Before writing

All paths are relative to the repo root (`git rev-parse --show-toplevel`): `cd` there first.

1. Read `data/messages.md`. If `status: PENDING` or the profile is incomplete, ask for what's missing and send nothing.
2. Find the listing in `data/seen.md`. If it was published more than 48h ago, warn the user (it is often already in the application-review stage) and ask them to confirm.

## Drafting

- Fill in the template with the listing details (type, m², city, landlord's first name if shown).
- Add **one** useful question, only if the listing doesn't give that info: missing DPE, availability date.
- Show the user the full message and ask "send it as is?".
- For a reply to a landlord: keep the user's words, fix spelling only, and sum up the points to remember from the landlord's message (DPE to be redone, applications under review, visit…).

## Sending (only after an explicit "yes" for THIS message)

- Load the Chrome tools (and `PushNotification` in auto mode) in a single ToolSearch, call `tabs_context_mcp`, then fill in the form in a new Chrome tab, then check what the form adds **before** clicking send:
  - **Commitment boxes** (e.g. service fees payable if selected, on Gens de Confiance): never tick without specific consent; state the amount.
  - **Pre-filled phone number**: tell the user it will be shared.
  - **Attached rental file** (Leboncoin: « sans justificatifs » is ticked by default, « dossier complet » attaches the documents): never attach documents (payslips, ID, tax notice) without consent.
- After sending, check the site's status message (e.g. « dossier incomplet ») and report it.
- Set the line in `data/seen.md` to `CONTACTED (<YYYY-MM-DD>, <contact person>, <next step>)`.

## Auto mode

Only if `data/criteria.md` contains `mode: auto` written by the user **and** `cap` is a number (otherwise send nothing and notify the user to set it): send without asking for OK listings under 48h old, within the daily `cap` (count today's `CONTACTED (<YYYY-MM-DD>` lines in `data/seen.md` before each send; at the cap, stop and notify), using the APPROVED message. The "commitment boxes" and "attachments" rules still block even in auto mode. Notify on every send.
