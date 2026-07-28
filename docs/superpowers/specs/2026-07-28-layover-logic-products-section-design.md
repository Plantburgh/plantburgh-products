# Layover Logic — Plantburgh Products section

**Date:** 2026-07-28
**Repo:** `Plantburgh/plantburgh-products` (public; local `Desktop/Created Apps Vibed/flipline-site/`)
**Status:** approved, ready to plan

## Goal

Give Layover Logic its own section on the Plantburgh Products site, matching the
existing per-product pattern (`flipline/`, `duesy/`). Marketing only — the app
itself and its picks data are hosted elsewhere and are explicitly out of scope
for this repo.

## Decisions

Three decisions were made by the owner before design and constrain everything
below.

### 1. The app is NOT hosted here

This repo is public. Hosting the PWA here would mean committing
`content/picks.json` — 3,165 hand-verified picks across 100 cities, weeks of
research — as a plain file anyone can download in a single request.

Therefore: **the products site carries the landing page only.** The app and its
picks stay off public git, on a separate host still to be chosen.

Consequence: this section has **no dependency on the app host existing**. It
ships complete and standalone. When a host is picked, one link is added.

### 2. Private beta, not live

Layover Logic is the only product on the shelf that currently works, but it is
presented as **private beta**, not as a public app. The landing page therefore
**must not link to the app**. Its call to action is a mailto for beta access.

This is what keeps the private-beta claim true rather than decorative. A page
that says "private beta" while linking straight to a working app is a fake
label.

### 3. Legal pages match the siblings

Both `flipline/` and `duesy/` ship `privacy.html` + `terms.html`. Layover Logic
gets the same, despite collecting nothing — consistency now, and the pages are
prerequisites if it ever reaches an app store or takes payment.

## Files

New directory `layover-logic/`, following the sibling pattern exactly:

| File | Purpose |
|---|---|
| `layover-logic/index.html` | Landing page |
| `layover-logic/styles.css` | Page-scoped look (products pages each carry their own) |
| `layover-logic/privacy.html` | Privacy policy |
| `layover-logic/terms.html` | Terms of use |

Modified: root `index.html` — one new `.product` shelf entry.

No build step, no dependencies, no JavaScript. The site is static HTML + CSS and
stays that way.

## Catalog entry

Inserted **third**, after Flipline and Duesy (both store-bound, closer to
launch) and before the three in-development entries. Honest ordering by
maturity without overselling.

- Bin label: `Layover Logic` / `web app · offline` / `aircrew`
- Name line: *Rest first. Then the city.*
- Status chip: `private beta`, using the existing muted `.status.dev` style

The bin label says `web app`, not `iOS · Android`. Layover Logic installs to the
home screen on both, but the siblings' platform labels denote native store apps;
reusing that wording here would imply a store listing that does not exist.

The muted chip matters: it visually groups Layover Logic with "not yet yours"
rather than with the lavender `coming soon · Google Play` chips, which promise a
store listing that does not apply to a PWA.

Rendered as `<a class="product" href="layover-logic/">` — a link, like Flipline
and Duesy, unlike the three link-less in-development entries.

## Landing page

### Structure

Same skeleton as `duesy/index.html`:

1. `header` — wordmark + nav links (All products · Privacy · Terms)
2. `section.hero` — h1, sub, status chip, beta CTA, and an `aside` visual
3. `section.features` — four cards
4. `footer` — copyright + Privacy · Terms · Contact

The hero chip reads `● Private beta · flight crew`. Directly beneath it sits the
page's only call to action:

```html
<a class="cta" href="mailto:reihlandre@gmail.com?subject=Layover%20Logic%20beta">
  Ask for a beta invite</a>
```

followed by one muted line of expectation-setting: *Testing with crew first —
tell us your base and fleet.* This mailto is the **only** action on the page.
There is no app link, no download button, and no store badge.

### Look

Carries the real app's palette so page and product read as one thing:

| Token | Value |
|---|---|
| background | `#07090c` |
| panel | `#0a0d11` |
| accent (mint) | `#6ee7b7` |
| text | `#e7ecf2` |
| muted | `#93a1b3` |
| hairline | `#232831` |

Typography stays the site-wide Archivo + IBM Plex Mono so it remains a
Plantburgh page. Dark palette, shared type — the same relationship
`flipline/` already has.

### Hero aside — the layover strip

The product's core insight, stated plainly. Mono, right-aligned figures,
mint on the result row:

```
MUC · layover          wheels-down 14:20
                       pickup      06:05
layover                     15h 45m
− rest floor                 9h 30m
− transit both ways          1h 10m
─────────────────────────────────────
free                         5h 05m
                       → 3 picks fit
```

Marked `aria-label`'d as an example calculation, decorative rule
`aria-hidden`.

### Feature cards

1. **Rest math first** — starts from when you actually sleep, not when the
   van leaves. Subtracts the rest floor, transit both ways, and buffers, then
   shows what is genuinely left.
2. **Works with no signal** — the whole guide sits on the phone. Verified
   end-to-end: server killed, app still opens with all picks.
3. **Picks checked by hand** — hours, closing times and distance from the
   crew hotel verified per pick, not scraped.
4. **No account, nothing uploaded** — no sign-in, no tracking, nothing leaves
   the device.

### Claims deliberately excluded

Per the owner's no-fake-features rule:

- **No push/alert claims.** The push toggle was removed from the app because a
  PWA cannot deliver background alerts on iOS. The page must not reintroduce
  the promise.
- **No crowd-sourced or aggregated-ratings framing.** Crew-verified `yes/of`
  counts are authored curation fields today, not aggregated user votes. Copy
  says *checked by hand*.
- **No store badges.** It is not on any store and is not submitted.

## Privacy page

Short and true:

- No account, no server, no analytics, no third-party SDKs.
- Everything entered stays in the browser's local storage on the device.
- The beta log (opens, screens, cities, JS errors) is **local-only and never
  transmitted**.
- Feedback is sent only when the user taps share, and the exact payload is
  shown before sending.
- Contact: `reihlandre@gmail.com`.

## Terms page

Standard beta terms — provided as-is, no warranty, may change or end — plus one
clause that carries real weight:

> **The rest math is a planning aid, not a duty-time or regulatory compliance
> calculator.** It does not compute legal rest requirements, and it is not a
> substitute for your airline's rostering rules or your regulator's flight-time
> limitations. Opening hours, closures and transit times change; verify anything
> you are relying on.

For aircrew this distinction is the difference between a useful tool and a
liability. It belongs on the page before a single tester relies on it.

## Out of scope

- Hosting the app or committing any picks data to this repo.
- The `plantburghproducts.com` CNAME and DNS cutover — owner will do this later.
  All links in the section are relative, so a domain switch is a no-op.
- Any change to `flipline/`, `duesy/`, or `products.css`.

## Verification

- Every new page loads with correct relative paths from a local static server,
  at the repo root **and** under a `/plantburgh-products/` subpath (GitHub Pages
  serves the site at a subpath today).
- All internal links resolve: catalog → section, section → privacy/terms,
  section → All products, footer links.
- No link anywhere points at the app.
- Renders correctly at 375px and desktop widths.
- Text contrast on the dark palette meets WCAG AA.
