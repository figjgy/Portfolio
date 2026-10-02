# Antigravity prompts — adding 7 tools to the portfolio SaaS page

Paste **Prompt 0 first** in a new Antigravity session (it gives the agent the map).
Then paste one tool prompt at a time. After each tool, paste **Prompt V** (verify)
before moving on. Finish with **Prompt D** (deploy).

Order: 0 → 1 → V → 2 → V → 3 → V → 4 → V → 5 → V → 6 → V → 7 → V → D

> **Status 2026-09-06:** Tools 1, 2 and 3 are DONE and verified
> (`tests/test_tools.js` → 42/42 PASS). Start Antigravity at **Prompt 0, then
> Prompt 4**. Tell it: "Tools 1–3 already exist as #panel-audit, #panel-classify,
> #panel-report — do not rebuild them; extend tests/test_tools.js, do not replace it."
> Also: **no pricing, plans, subscriptions or "starts at ₱" anywhere on the site.**
> Every service card ends in a WhatsApp / email inquiry button. The pricing section,
> Pro modal and currency toggle were removed on 2026-09-06 — do not re-add them.
> **No emojis anywhere in the UI.** Use the inline SVG sprite already in `ICONS`
> (build.py): `<svg class="ico ico-sm" viewBox="0 0 24 24"><use href="#i-NAME"/></svg>`.
> Available: shield chart tag search box trend alert clock flame gift mega rocket
> inbox camera camera-off check x warn star list wa mail phone. Add new `<g id="i-…">`
> symbols to `ICONS` if you need more — 24×24, stroke-only, Feather style.
> A site-wide assistant chat widget exists (`chat_widget()` + `CHAT_JS` in build.py,
> injected by `shell()`). Do not add a second chat; extend its `A{}` answers / `RULES`.
> Media: `content.py` galleries accept image filenames (from `images/`), and a **list of
> .mp4 filenames** (from `videos/`, each with a same-name .jpg poster) which renders a
> 3-up row of 9:16 videos. `gallery_captions` adds a caption under each item. Keep
> videos ≤ 3 MB (1080p, H.264 CRF 27) — the site is static on Vercel.


---

## Prompt 0 — Context (paste first, every session)

```
You are working in C:\Users\User\JAMIE CLAUDE\Portfolio — a static portfolio site
generator. Read these before changing anything:

- build.py   : Python generator. `python build.py` DELETES site/ and rebuilds it.
               Shared CSS is the `CSS` string near line 30. The tools page is built
               by `build_tools()` (~line 1867) and its JavaScript is the `TOOL_JS`
               raw string (~line 1083). The three existing tools are tabs:
               #panel-scanner, #panel-tacos, #panel-voucher, switched by
               `.suite-nav .suite-tab[data-tab]`.
- content.py : all text/profile content. Do not put code here.
- images/    : source images, copied into site/assets/images on every build.
- site/      : generated output. Never hand-edit; it is overwritten. It IS committed
               because Vercel serves it directly (Root Directory = site).
- README.md and CLAUDE.md in the parent folder explain the deployment.

Hard rules:
1. All new tools go INTO build_tools() as new tab panels + INTO TOOL_JS. One
   page, one file, no frameworks, no external JS except from cdnjs.cloudflare.com.
2. Any CSS used by a tool goes into the shared `CSS` string, not inline <style>.
3. Palette is locked: background #0B0B0B, accent #8B0D1A (fills/markers only —
   never crimson text on black), text #F5F2ED. Reuse existing classes:
   .btn, .btn.ghost, .field, .result-card, .pill, .tag, .suite-panel, .howto.
4. Never build an onclick like onclick="fn(${JSON.stringify(x)})" — the quotes
   break the attribute. Use data-* attributes + addEventListener, or
   onclick="fn(this.dataset.x)".
5. Every tool must work with NO backend: parse CSV client-side (write a small
   CSV parser or use PapaParse from cdnjs), compute in the browser, export with
   Blob downloads. Persist inputs in localStorage under a tool-specific key.
6. Every tool has a one-line "How to use" (.howto) and a sample-data button
   ("Load sample") so a visitor sees output within 5 seconds.
7. Sample data must be generic (e.g. "Snail Mucin Serum 50ml"), never real
   K-PICK or client products or prices.
8. After editing, run: python build.py  — then confirm site/tools/index.html
   contains the new panel id. Then run: node --check on the extracted inline
   script (extract everything between <script> and </script> to a temp file).
9. Keep existing tools working. Do not rename existing ids or STORE_KEY.

Confirm you have read build.py's build_tools() and TOOL_JS, then wait for the
next prompt.
```

---

## Prompt 1 — Marketplace Audit Scorecard

```
Add a 4th tab to the tools page: "🔍 Marketplace Audit Scorecard"
(id panel-audit).

Purpose: a seller uploads a CSV export of their listings and gets a health score
per SKU plus the top fixes. Must work for Amazon, eBay, Shopee, Lazada, TikTok
Shop exports — so map columns flexibly by header name (case-insensitive,
partial match): sku|seller sku|item id, title|name|product name,
description|body, bullets|bullet points|key features, price|sale price,
images|image count|main image (count URLs separated by , ; | ),
reviews|review count|ratings, rating|avg rating|stars, category,
stock|quantity|inventory, sales|units sold|orders.

UI:
- File input (CSV) + "Load sample" (25 generic rows across 3 platforms) +
  platform selector (Amazon / eBay / Shopee-Lazada / TikTok Shop / Generic)
  which sets title/description limits and weights.
- Summary strip: overall health score 0-100, # SKUs, # critical, # good,
  average title length, % with <5 images, % with 0 reviews.
- Table: SKU, title (truncated), score (colour pill: <50 red, 50-79 amber,
  80+ green), top issue. Sortable by score. Click a row → detail drawer with
  every check and the exact fix.
- "Top 10 fixes" list, ranked by (number of SKUs affected × severity).
- Buttons: Export CSV (scores + issues), Export audit report (self-contained
  HTML file with the summary, top fixes, and table — styled with the same
  palette), Copy summary text.

Scoring per SKU (weights configurable in a JS object): title length in range
for platform (15), title has ≥3 keyword-like tokens and no ALL CAPS (10),
description length ≥ 300 chars (10), bullets ≥ 3 (10), images ≥ 5 (15),
main image present (5), reviews ≥ 10 (10), rating ≥ 4.2 (5), price present
and > 0 (5), stock > 0 (10), no banned words from the existing Scanner's
lists (5). Reuse the Scanner's flagged-word logic — do not duplicate it.

Persist last upload (parsed rows, not the file) in localStorage key
'audit-v1'. Add a .howto line. Update the tools-page hero/intro copy in
build_tools() so it says "7 tools" if a count is mentioned.
```

---

## Prompt 2 — Product Performance Classifier

```
Add a 5th tab: "📦 Product Performance Classifier" (id panel-classify).

Purpose: upload sales/stock CSV → each SKU gets ONE recommended action.
Columns (flexible header match): sku, name|title, brand, stock|quantity,
sold_30d|units sold|sales 30d, price, cost (optional), expiry|expiration
(optional date), image|has_image (optional yes/no or URL).

Rules (thresholds editable in a small settings panel, defaults shown):
- expiry in the past                           → "Expired stock"   (High)
- stock ≤ 0                                    → "Restock first"   (Low)
- expiry ≤ 60 days                             → "Clearance sale"  (High)
- sold_30d = 0 and stock ≥ 10                  → "Flash sale"      (High)
- sold_30d = 0 and stock < 10                  → "Promo push"      (Medium)
- expiry ≤ 120 days, or stock/sold_30d ≥ 3 months → "Bundle / voucher" (Medium)
- sold_30d ≥ 30 and stock < sold_30d           → "Scale — restock & advertise" (Growth)
- otherwise                                    → "Promo push"      (Medium)
Also flag needs_image = true when image column is empty/no.

UI: 6 KPI cards (one per action + "No image"), filter tabs, brand dropdown,
search, table with action pill, stock, sold/30d, months of stock, expiry days,
price, and a "why" line. Sort High first. Export CSV and "Copy action plan"
(plain text grouped by action). Sample data: 40 generic rows. localStorage
key 'classify-v1'.
```

---

## Prompt 3 — Monthly Performance Report Generator

```
Add a 6th tab: "📈 Monthly Performance Report" (id panel-report).

Purpose: a consultant types this month's and last month's numbers and gets a
client-ready one-page report.

Inputs (two columns: This month / Last month): revenue, orders, sessions or
visits, ad spend, ad-attributed sales, units sold, returns (optional),
average organic rank or impressions (optional), account health notes (text).
Store name, marketplace, month (YYYY-MM), currency symbol selector (₱ $ A$ £ €).

Computed: AOV, conversion rate (orders/sessions), ROAS (ad sales/ad spend),
TACOS (ad spend/revenue), ad-sales share, return rate, month-over-month delta
for every metric with ▲▼ and %.

Auto-written insights (rule-based, no AI): generate 3 "What happened" lines
and 3 "Next month actions" from the deltas (e.g. sessions up but CVR down →
"traffic grew X% but conversion fell Y% — review product page and price
position"; ROAS < 3 → "ads efficiency below target — cut campaigns under
break-even, shift budget to top ROAS campaigns"). Cover at least 10 rules.

Outputs: on-screen report preview styled like a document (white card on the
dark page), "Download HTML report" (self-contained, printable to PDF via
browser), "Copy as text", "Copy as Markdown". Keep the last 12 months in
localStorage key 'report-v1' and show a tiny 12-month revenue sparkline
(inline SVG, no library) when ≥2 months exist.
```

---

## Prompt 4 — Ads Efficiency Tracker (extend the TACOS tab)

```
Extend the existing "📊 Ad Efficiency & TACOS Calculator" tab (panel-tacos) —
do not create a new tab. Keep the current single-product calculator at the top,
then add a "Campaign tracker" section below it.

Campaign tracker: editable table, add/remove rows. Columns: campaign name,
platform (Amazon SP / eBay Promoted / Shopee Ads / Lazada Sponsored /
TikTok Ads / Other), spend, ad sales, orders, clicks, impressions, product
margin %. Computed per row: ROAS, ACoS, CPC, CTR, CVR, break-even ACoS
(= margin %), and a verdict pill: "Scale" (ACoS < 0.7×margin and orders ≥ 5),
"Hold" (ACoS ≤ margin), "Cut" (ACoS > margin), "Needs data" (< 5 orders).
Totals row. A "Reallocate" suggestion: list Cut campaigns with their spend,
and Scale campaigns, with the sentence "Move ~X from cut campaigns to scale
campaigns". CSV import (flexible headers) and export. Sample: 8 campaigns.
localStorage key 'ads-v1'.
```

---

## Prompt 5 — Competitor Price Position

```
Add a tab: "🏁 Competitor Price Position" (id panel-priceposition).

Purpose: for each of my SKUs, paste up to 5 competitor prices and see where I
sit and what I can afford to do.

Inputs per row: my SKU/name, my price, my cost (optional), platform fee %
(default from a small settings box: 8), min margin % (default 20), competitor
prices (comma-separated, e.g. "899, 949, 1,050"). Rows addable; CSV import.

Computed: lowest / median / highest competitor, my position label (Cheapest /
Below median / Above median / Most expensive), gap to lowest in currency and
%, my floor price (cost / ((1-fee)(1-margin))) when cost is given, and a
recommendation: "Hold" (within ±5% of median), "Match to X" (if lowest is
above my floor), "Cannot match — floor is X, sell on value/bundle" (if lowest
is below floor), "Raise to median X" (if I'm the cheapest by >10%).
Colour bar per row showing competitor prices as dots and mine as a marker.
Export CSV, copy summary. Sample: 10 rows. localStorage 'priceposition-v1'.
```

---

## Prompt 6 — Promo Calendar Builder

```
Add a tab: "🗓️ Promo Calendar Builder" (id panel-promocal).

Purpose: pick a country, get the key shopping dates pre-loaded, drop products
into them, export a calendar.

Country presets (editable list in JS): Philippines (payday 15th & 30th every
month, 1.1, 2.2, 3.3 … 12.12, Mother's Day, Father's Day, Back to School Jun,
Ber-months Sept 1, Undas, Christmas, Black Friday, Cyber Monday), Australia
(Australia Day, Valentine's, Mother's Day, EOFY Jun 30, Afterpay Day Aug,
Father's Day Sep, Click Frenzy Nov, Black Friday, Cyber Monday, Boxing Day),
USA (Valentine's, Prime Day Jul, Back to School, Labor Day, Black Friday,
Cyber Monday, Christmas), UK, Singapore/Malaysia (11.11, 12.12, Hari Raya,
CNY, GSS). Dates for the current year and next year, computed for movable
ones where simple (else fixed month labels).

UI: month grid (12 months, current year → +12 months), events shown as chips.
Left panel: product/promo list (name, type: Flash sale / Voucher / Bundle /
Launch / Content). Click a product then click a date to assign; or drag if
simple. Each assignment: product, date, type, note. Export: CSV, ICS calendar
file (VEVENT per assignment), and a printable HTML month view.
localStorage 'promocal-v1'. Sample: 6 promos assigned across next 3 months.
```

---

## Prompt 7 — Product Page CRO Checker

```
Add a tab: "🛒 Product Page CRO Checker" (id panel-cro).

Purpose: score a product page against conversion best practices.

Two modes:
A) Paste HTML: the user pastes the page's HTML (view-source) into a textarea —
   parse with DOMParser and run the checks. This is the default and always
   works (no CORS).
B) Paste URL: try fetch(); if blocked by CORS (it usually will be), show a
   clear message "Browsers block cross-site reads — paste the page HTML
   instead (Ctrl+U on the page, copy all)". Never fail silently.

Checks (each with weight, pass/fail, and a fix sentence):
- <title> present and 30-70 chars; meta description present 70-160
- exactly one <h1>; h1 contains the product name-ish text
- ≥5 product images (img tags in the main/product area or JSON-LD image array)
- images have alt text (≥80%)
- price visible (JSON-LD offers.price, or ₱/$/A$ pattern in text)
- add-to-cart/buy button present (button/input with text matching
  add to cart|buy now|add to bag|checkout)
- reviews/rating present (JSON-LD aggregateRating, or "reviews" text)
- trust signals: shipping/returns/guarantee words present
- bundle/upsell/cross-sell hints (frequently bought|bundle|complete the set|
  you may also like)
- size guide / variant selector present for apparel/beauty (select or radio
  with option text)
- JSON-LD Product schema present and valid-ish
- viewport meta present (mobile)
- page weight hint: count of <script> and <img>; warn if scripts > 30
- Shopify-specific (if HTML contains "cdn.shopify.com"): theme name from
  Shopify.theme, sections count, presence of predictive search, presence of
  Klaviyo/Judge.me/Loox/Yotpo/ReCharge/Bold scripts → list detected apps.

Output: score 0-100, pass/fail list grouped Critical / Important / Nice,
detected platform + apps, and a "Copy audit" button (plain text) plus
"Download audit HTML". Sample button loads a built-in sample product page
HTML (generic skincare product) so the demo works instantly.
localStorage 'cro-v1' for the last pasted HTML (cap at 500 KB).
```

---

## Prompt V — Verify (paste after every tool)

```
Verify the tool you just added, do not just eyeball it:
1. python build.py — must finish without errors; site/tools/index.html must
   contain the new panel id and the tab button.
2. Extract the inline <script> from site/tools/index.html to a temp .js file
   and run: node --check <file>. Fix any syntax error.
3. Write/extend a Node test harness at Portfolio/tests/test_tools.js: stub
   document.getElementById / querySelectorAll / localStorage / navigator
   (use Object.defineProperty for navigator on Node 22), load the extracted
   script, call the tool's "load sample" function, then assert on real
   outputs (scores, counts, verdicts, exported text). Minimum 8 assertions
   for this tool. Run it and paste the PASS/FAIL list.
4. Grep site/tools/index.html for onclick="…JSON.stringify — must be zero.
5. Open site/tools/index.html in a browser (or headless) and confirm the new
   tab switches, sample loads, and export downloads a file. Report what you
   actually saw.
6. Confirm the three original tools (Scanner, TACOS, Voucher) still load
   sample data and compute — run their existing checks.
Report: what changed, test results, anything you could not verify.
```

---

## Prompt D — Deploy

```
Deploy the portfolio:
1. python build.py one final time. Confirm site/ contains index.html,
   tools/index.html, about.html, card.html, work/, assets/, 404.html,
   vercel.json.
2. git status — stage ONLY: build.py, content.py, images/, site/, README.md,
   ANTIGRAVITY_PROMPTS.md, tests/. Do NOT stage anything named *secret*,
   *.key, .env, or files outside the Portfolio folder.
3. Commit: "Add 7 marketplace/Shopify tools to the SaaS page" and push to
   origin main (https://github.com/figjgy/Portfolio.git). If push needs
   credentials, stop and tell me — do not store a token in the repo.
4. After push, wait for Vercel, then open https://jamielyn-ludovice.vercel.app/tools
   and confirm the 7 tabs are visible and the sample buttons work. Vercel's
   Root Directory must stay = site (do not add rewrites).
Report the commit hash and the live URL check result.
```

---

## Notes for Jamie

- Antigravity works best one prompt at a time. If it starts "refactoring"
  build.py into many files, stop it: "Keep the single-file generator. Revert
  the split."
- If it asks for a design, say: "Match the existing tools page exactly."
- If a tool needs an API key (PageSpeed for the CRO tool), tell it: "Make the
  API optional — the tool must fully work without a key."
- Keep this file in the Portfolio folder; it is safe to commit (no secrets).
