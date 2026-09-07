# -*- coding: utf-8 -*-
"""
============================================================
  THIS IS THE ONLY FILE YOU NEED TO EDIT
============================================================
Change anything below, save, then run:   python build.py

TO ADD A PROJECT
  Copy one whole { ... } block inside PROJECTS, paste it where
  you want it to appear, change the wording. 'slug' becomes the
  web address — lowercase-with-hyphens, and never repeat one.

TO ADD IMAGES
  Put files in  site/assets/images/  then replace the
  'cover_note' / 'gallery' text with the filename.
============================================================
"""

PROFILE = {
    "name":            "Jamielyn Ludovice",
    "first":           "Jamielyn",
    "last":            "Ludovice",
    "subtitle":        "MULTIMEDIA · E-COMMERCE · INTERIOR STYLING · CREATIVE SYSTEMS",
    "subtitle_plain":  "Multidisciplinary Creative Specialist",
    "vcard_title":     "Multidisciplinary Creative Specialist",
    "vcard_file":      "Jamielyn_Ludovice",
    "location":        "Manila, Philippines",
    # --- shown on card.html (the NFC page) -------------------------------
    "card_eyebrow":    "DIGITAL BUSINESS CARD",
    "role":            "Multidisciplinary Creative Specialist",
    "company":         "K-PICK Trading Corp.",   # set to "" to hide the company line
    "initials":        "JL",
    "avatar":          "assets/images/profile.jpg",   # square, for the NFC card
    # The tall portrait on the home and About pages. A file in Portfolio/images/.
    # Leave "" and both fall back to the placeholder box.
    "portrait":        "portrait.jpg",
    "phone":           "+63 939 488 6685",
    "tel":             "+639394886685",
    "email":           "ludovice.jamielyn00@gmail.com",
    "linkedin":        "https://www.linkedin.com/in/jamielyn-ludovice-4b0a25380/",
    "linkedin_label":  "linkedin.com/in/jamielyn-ludovice",
    # --- socials --------------------------------------------------------
    # Username only — no @, no https, no tracking parameters.
    # Leave any of these blank ("") and that link simply will not appear.
    "whatsapp":  "639394886685",
    # Web3Forms access key (free, https://web3forms.com — enter your email, copy the key).
    # It is a PUBLIC key, safe to put in the site. Leave "" to fall back to a mailto link.
    "web3forms_key": "6ad39c40-43bd-4760-a45d-c0f0eb5decd1",
    "instagram": "jamiii_ludovice",
    "tiktok":    "figjgy",

    # --- the opening line -------------------------------------------------
    # This is option 4. The other five are in Portfolio_Foundation_Jamielyn.md
    # if you want to swap — it is one line.
    "status": "Open to freelance and contract work",
    "intro": ("Most brands look like three different companies. The listing, the post and "
              "the sign at the door were each made by someone else \u2014 so none of them match. "
              "I design the whole surface as one thing, then build the system that keeps it "
              "that way."),
}

# Only numbers you can defend if someone asks where they came from.
STATS = [
    {"n": "3",  "l": "Brands"},
    {"n": "3",  "l": "Marketplaces"},
    {"n": "30", "l": "Posts / brand / month"},
    {"n": "5",  "l": "Automations"},
]

# The scrolling strip on the home page. Add or remove freely.
MARQUEE = [
    "Marketing content", "Shopee", "Lazada", "TikTok Shop", "Shopify", "Listing optimisation",
    "Storefront design", "Front-end design", "Responsive layout", "Banners & tarpaulins", "Pubmats", "Content calendars",
    "Short-form video", "Product photography", "Ad creatives", "Photo retouching",
    "Product rendering",
    "Blender", "SketchUp",
    "Interior decoration", "Booth design", "Brand sourcing", "Supplier research",
    "UX / UI design", "Dashboard design", "Notion systems", "n8n", "GoHighLevel", "Automation",
    "AI agents", "Telegram bots", "MCP integrations",
]

DISCIPLINES = {
    "marketing": "Marketing & Content",
    "ecommerce": "E-Commerce",
    "graphic":   "Graphic & Layout",
    "web":       "Web & Frontend",
    "rendering": "Rendering",
    "interior":  "Interior Decoration",
    "systems":   "Systems & Automation",
    "sourcing":  "Brand Sourcing & Research",
}

PROJECTS = [
    # ---------------------------------------------------------- E-COMMERCE
    {
        "slug": "marketplace-management",
        "title": "Shopee, Lazada & TikTok Shop",
        "discipline": "ecommerce",
        "year": "2026",
        "featured": True,
        "tags": ["Shop design", "Listing optimisation", "Marketplace compliance"],
        "cover_note": "Image — shop front & listing graphics",
        "summary": ("Storefront design, listing graphics and optimisation across three "
                    "marketplaces — including clearing the listings that get flagged."),
        "challenge": ("Three marketplaces, each with its own rules, layout system and reasons "
                      "for taking a product down. A flagged listing earns nothing while it sits."),
        "approach": ("Designed the shop fronts and campaign banners, built the listing graphics "
                     "and A+ content, and optimised titles, keywords and images for search. "
                     "Worked through flagged and restricted products — reading each violation, "
                     "correcting the wording or the artwork, and getting the listing live again."),
        "result": ("Three storefronts kept consistent, on-brand and selling, with flagged "
                   "products fixed rather than left down."),
        "gallery": ["Image — Shopee storefront", "Image — listing graphics set",
                    "Image — A+ content layout"],
    },
    {
        "slug": "margegold-jewelry",
        "title": "Margegold Jewelry — Shopify store & marketplace listings",
        "discipline": "ecommerce",
        "year": "",          # <- add the years you worked on this, e.g. "2024–2025"
        "featured": True,
        "link": "https://margejewelry.com/",
        "tags": ["Shopify", "Product photography", "Listing images", "Video editing", "TikTok Shop", "Shopee", "Ads creatives"],
        "cover": "margegold-cover.jpg",
        "cover_note": "Hero listing slide — Big Lock Paperclip Necklace",
        "gallery": [
            {"title": "Big Lock Paperclip Necklace", "sub": "8-slide listing · 18K Saudi gold",
             "grid": [f"mg-necklace-{i}.jpg" for i in range(1, 9)], "ratio": "r11", "alt": "Paperclip necklace listing slide"},
            {"title": "Mini Diacut Heart Ring", "sub": "8-slide listing",
             "grid": [f"mg-ring-{i}.jpg" for i in range(1, 9)], "ratio": "r11", "alt": "Heart ring listing slide"},
            {"title": "Diacut Bar Stud Earrings", "sub": "8-slide listing",
             "grid": [f"mg-stud-{i}.jpg" for i in range(1, 9)], "ratio": "r11", "alt": "Stud earrings listing slide"},
            {"title": "Croissant Design Earrings", "sub": "8-slide listing",
             "grid": [f"mg-croissant-{i}.jpg" for i in range(1, 9)], "ratio": "r11", "alt": "Croissant earrings listing slide"},
            {"title": "Ad creatives", "sub": "dusty-rose lifestyle set · 4:5 for feed placements",
             "grid": [f"mg-ad-a-{i}.jpg" for i in range(1, 6)] + [f"mg-ad-b-{i}.jpg" for i in range(1, 5)], "ratio": "r45", "alt": "Margegold ad creative"},
            ["margegold-video-1.mp4", "margegold-video-2.mp4", "margegold-video-3.mp4"],
        ],
        "gallery_captions": [
            "Every product follows the same 8 slides: silk hero, macro, dimension diagram, on-model, gift box, in-hand, detail, collage. Scroll sideways to see the sequence.",
            "", "", "", "",
            "Short-form brand videos — edit, text overlays and the Marge Jewelry end card",
        ],
        "summary": ("Product photography and listing images for a jewellery brand's live "
                    "Shopify store, margejewelry.com, plus its TikTok Shop, Shopee and Lazada "
                    "listings, the ad creatives, and the short-form brand videos."),
        "challenge": ("Jewellery is small, reflective and sells almost entirely on the "
                      "photograph. The same pieces had to work on four surfaces at once — "
                      "an owned Shopify storefront, three marketplace grids and a TikTok feed — "
                      "and a catalogue of near-identical pieces needed one strict, repeatable "
                      "look so the store reads as one brand, not a hundred separate photos."),
        "approach": ("Set one 8-slide listing architecture and applied it to every product: "
                     "hero on white silk, macro detail, a dimension diagram, on-model, the gift "
                     "box, in-hand scale, a second detail and a collage. Same angle, crop, "
                     "background and retouch across the catalogue, sized for TikTok Shop, Shopee "
                     "and Lazada, then a separate dusty-rose lifestyle set in 4:5 for paid ads. "
                     "Edited the brand's short-form videos too — cut, text overlays and the "
                     "logo end card — for TikTok, Reels and paid placements."),
        "result": ("A live Shopify store where every product page carries the same photography "
                   "standard, matching listings on the marketplaces, ad creatives and video "
                   "produced in-house instead of bought in."),
    },
    # ---------------------------------------------------------------- WEB
    {
        "slug": "kpick-website",
        "title": "kpicktradingcorp.com",
        "discipline": "web",
        "year": "2026",
        "featured": True,
        "link": "https://kpicktradingcorp.com/",
        "link_label": "Visit the live site",
        "tags": ["Front-end design", "Interactive UI", "Responsive layout", "B2B website"],
        "cover": "kpick-web-cover.jpg",
        "cover_note": "kpicktradingcorp.com \u2014 homepage",
        "summary": ("Front-end design for the company website \u2014 a B2B medical distribution "
                    "site read by hospital and clinic procurement teams."),
        "challenge": ("The audience is procurement officers, not shoppers. They arrive looking "
                      "for one specific thing \u2014 a certification, a product spec, a way to "
                      "raise a quote \u2014 and they are usually deciding whether the company "
                      "is credible enough to buy from at all. A regulated medical distributor "
                      "also carries a great deal of material that has to be reachable without "
                      "burying the pages that actually move an order forward."),
        "approach": ("Designed the front end across the homepage, the two brand pages, the "
                     "Learning Centre and the supporting sections. Set the visual system \u2014 "
                     "type, colour, spacing, components \u2014 and laid out the page structure so "
                     "the brand lines, certifications, company history and FAQs each have their "
                     "own clear place. The Learning Centre goes further than a specification "
                     "table: nine devices are explained by letting the reader operate them \u2014 "
                     "change a gauge and the needle redraws, draw a dose and the barrel fills, "
                     "with the numbers updating underneath. Built for the phone first, since "
                     "buyers open it between other things."),
        "result": ("A live site the company points buyers to \u2014 quote request and compliance "
                   "documents reachable from anywhere on the page, and a Learning Centre that "
                   "answers the product questions a sales rep would otherwise answer twice a day."),
        "gallery": [
            {"title": "Desktop", "sub": "homepage \u00b7 above and below the fold",
             "ratio": "r169", "alt": "kpicktradingcorp.com desktop layout",
             "grid": ["kpick-web-desk-1.jpg", "kpick-web-desk-2.jpg"]},
            {"title": "Learning Centre", "sub": "nine devices explained by letting you operate them",
             "ratio": "r169", "alt": "kpicktradingcorp.com Learning Centre",
             "grid": ["kpick-web-learn.jpg", "kpick-web-module.jpg"]},
            {"title": "Credentials", "sub": "compliance and registration, with the documents behind it",
             "ratio": "r169", "alt": "kpicktradingcorp.com credentials page",
             "grid": ["kpick-web-creds.jpg"]},
            {"title": "Generate Quote / PO", "sub": "step 1 of 3 \u00b7 customer, products, review",
             "ratio": "r169", "alt": "kpicktradingcorp.com quote and purchase order builder",
             "grid": ["kpick-web-quote.jpg"]},
            {"title": "Phone", "sub": "same page, built for the screen it is actually opened on",
             "ratio": "r916", "alt": "kpicktradingcorp.com mobile layout",
             "grid": ["kpick-web-mob-1.jpg", "kpick-web-mob-2.jpg"]},
        ],
        "gallery_captions": [
            "The hero answers the three procurement questions in one screen \u2014 what is "
            "sold, which certifications it carries, and who it is for \u2014 then splits "
            "into the two brand lines. Generate Quote sits beside View Certifications "
            "because those are the only two things a buyer comes to do",
            "The Learning Centre is the part I am proudest of. Nine devices explained by "
            "letting you operate them \u2014 pick a barrel and a gauge and the syringe "
            "redraws to scale, drag the dose and the barrel fills while volume, fill "
            "percentage, needle length and packing update underneath. A specification table "
            "tells a buyer the numbers; this shows them what the numbers mean. Every claim "
            "is sourced from manufacturer specifications, dated, and labelled educational "
            "material rather than clinical advice",
            "Credentials given their own page instead of a line in the footer: DTI, SEC, "
            "the Philippine FDA licence to operate and the exclusive-distributor status, "
            "each with the document behind it and its validity date. Procurement asks for "
            "exactly these four things, so they are one click from anywhere",
            "The one page that is not a brochure. A buyer builds the request themselves \u2014 "
            "customer details, then products and quantities from the live catalogue, then a "
            "review \u2014 and K-Pick receives a summary it can price, instead of an email "
            "saying \u2018how much for syringes\u2019. Three numbered steps so nobody "
            "abandons it halfway, a pinned Google Maps delivery address because that is what "
            "couriers need, and no prices shown anywhere: quotation stays with the team",
            "The same page on a phone: the two brand cards collapse to full-width rows, the "
            "figures stack, and the nav becomes one button \u2014 nothing is dropped, only "
            "re-ordered, because a procurement officer opening this between meetings still "
            "needs the certifications and the quote link",
        ],
    },
    # ------------------------------------------------------------- CREATIVE
    {
        "slug": "ads-creatives",
        "title": "Ad creatives for overseas brands",
        "discipline": "marketing",
        "year": "2025\u20132026",
        "featured": True,
        "tags": ["Ad creatives", "Paid social", "Art direction", "Copywriting"],
        "cover": "ads-cover.jpg",
        "cover_note": "Ad creatives \u2014 Upscale Menswear, Big Paw Olive Oil, Luv\u00e9, PMT",
        "summary": ("Paid-social creative for four overseas brands \u2014 US menswear, "
                    "a California olive oil producer, a lash brand and an apparel drop \u2014 "
                    "each in its own voice, none of them mine."),
        "challenge": ("Selling to a market I do not live in. There is no walking into the "
                      "store, no reading the room \u2014 the creative has to carry the whole "
                      "message on its own, in a scroll, to someone who has never heard of "
                      "the brand. And four brands means four voices: a menswear house that "
                      "must feel expensive cannot use the same layout as an olive oil "
                      "producer that must feel warm."),
        "approach": ("Built each brand its own visual system first \u2014 type, crop, colour, "
                     "where the logo sits, how the button looks \u2014 then worked inside it "
                     "so every ad in a set reads as one campaign instead of a pile of "
                     "one-offs. Funnel position drives the layout: a cold-audience ad leads "
                     "with the objection in plain words, a warm one leads with the product "
                     "and the offer. Sized natively per placement \u2014 4:5 and 1:1 for feed, "
                     "9:16 for stories \u2014 never one export stretched to fit all three."),
        "result": ("Four brands running on creative that looks like it came from inside "
                   "each company, produced from Manila."),
        "gallery": [
            {"title": "Upscale Menswear", "sub": "US luxury clothier \u00b7 feed 4:5",
             "ratio": "r45", "alt": "Upscale Menswear ad creative",
             "grid": ["ads-um-1.jpg", "ads-um-2.jpg", "ads-um-3.jpg",
                      "ads-um-4.jpg", "ads-um-5.jpg", "ads-um-6.jpg"]},
            {"title": "Big Paw Olive Oil Co.", "sub": "California olive oil & balsamic \u00b7 feed 1:1",
             "ratio": "r11", "alt": "Big Paw Olive Oil ad creative",
             "grid": ["ads-bp-1.jpg", "ads-bp-2.jpg", "ads-bp-3.jpg",
                      "ads-bp-4.jpg", "ads-bp-5.jpg"]},
            {"title": "Luv\u00e9 \u2014 cold audience", "sub": "magnetic lashes \u00b7 hook-led, top of funnel",
             "ratio": "r11", "alt": "Luv\u00e9 top-of-funnel ad creative",
             "grid": ["ads-luve-tof-1.jpg", "ads-luve-tof-2.jpg", "ads-luve-tof-3.jpg",
                      "ads-luve-tof-4.jpg", "ads-luve-tof-5.jpg"]},
            {"title": "Luv\u00e9 \u2014 ready to buy", "sub": "same product \u00b7 offer-led, bottom of funnel",
             "ratio": "r11", "alt": "Luv\u00e9 bottom-of-funnel ad creative",
             "grid": ["ads-luve-bof-1.jpg", "ads-luve-bof-2.jpg", "ads-luve-bof-3.jpg",
                      "ads-luve-bof-4.jpg", "ads-luve-bof-5.jpg"]},
            {"title": "PMT \u2014 Palestine special edition",
             "sub": "apparel drop \u00b7 stories 9:16", "ratio": "r916",
             "alt": "PMT Palestine special edition story creative",
             "grid": ["ads-pmt-1.jpg", "ads-pmt-2.jpg", "ads-pmt-3.jpg", "ads-pmt-4.jpg",
                      "ads-pmt-5.jpg", "ads-pmt-6.jpg", "ads-pmt-7.jpg", "ads-pmt-8.jpg",
                      "ads-pmt-9.jpg", "ads-pmt-10.jpg"]},
        ],
        "gallery_captions": [
            "Quiet luxury has to be built, not claimed \u2014 thin letter-spaced type, the "
            "product shot large, one white button, and nothing else competing for the eye",
            "Warm and appetite-led instead: the bottles photographed like food, benefits "
            "stated plainly, one red button repeated in every post so it becomes the brand's",
            "Cold audience. Each one opens on the objection a first-time buyer actually has "
            "\u2014 fit on monolid eyes, glue near the eye, the price of extensions \u2014 "
            "and answers it before mentioning the offer",
            "Same product, warm audience. The doubt is already handled, so these lead with "
            "the result and the discount and get out of the way",
            "A drop, so the set is built on scarcity and repetition \u2014 one type "
            "treatment, one gold-on-black palette, the shirt shown folded, hung, worn and "
            "on the street until it is recognisable at thumbnail size. Scroll sideways to see the whole drop.",
        ],
    },
    # ------------------------------------------------- SOURCING & RESEARCH
    {
        "slug": "brand-sourcing",
        "title": "Brand sourcing & supplier research",
        "discipline": "sourcing",
        "year": "2026",
        "featured": True,
        "tags": ["Supplier research", "Market analysis", "Regulatory screening"],
        "cover": "sourcing-cover.jpg",
        "cover_note": "Supplier comparison — three candidates on one page",
        "summary": ("Finding Korean manufacturers worth carrying, checking they are real, and "
                    "working out whether the product can actually be sold here."),
        "challenge": ("A distributor only grows as fast as it finds brands worth carrying. The "
                      "hard part is not finding names \u2014 it is separating manufacturers from "
                      "traders, and finding out early whether a product can legally be sold in "
                      "the Philippines at all."),
        "approach": ("Research manufacturers and their full product lines from primary sources "
                     "rather than brochures. Verify origin, certifications and what a company "
                     "actually makes versus what it resells. Map each one against what the "
                     "market already carries, then build side-by-side comparisons \u2014 product "
                     "overlap, gaps, regulatory requirements, and the questions leadership "
                     "needs answered before committing to anything."),
        "result": ("Sungshim and EROP brought in and built out, and a repeatable way of "
                   "evaluating the next one \u2014 so a decision rests on documents rather than "
                   "on a good first meeting."),
        "gallery": ["sourcing-method.jpg", "sourcing-map.jpg"],
        "gallery_captions": ["The verification sequence — the cheap checks run first, and any one of them can end it",
                             "Product-line map — where a supplier overlaps the market, and where it fills a gap"],
    },
    # ---------------------------------------------------------- MARKETING
    {
        "slug": "content-calendar-system",
        "title": "Three-brand content calendar",
        "discipline": "marketing",
        "year": "2026",
        "featured": True,
        "tags": ["Content strategy", "Notion", "Social media"],
        "cover": "calendar-cover.jpg",
        "cover_note": "Three brands on one month grid",
        "summary": ("Three brands, three audiences, one system — around 30 scheduled posts "
                    "per brand every month."),
        "challenge": ("Three brands with completely different audiences — marketplace shoppers, "
                      "smart-lock buyers, hospital procurement officers — all needing daily "
                      "content, all previously ad-hoc."),
        "approach": ("Built a Notion calendar covering all three with a fixed weekly theme "
                     "structure, so posting never starts from a blank page, wired to push each "
                     "day's task to the social media coordinator automatically."),
        "result": ("Around 30 posts per brand per month, scheduled a month ahead, with "
                   "compliance rules built into the system."),
        "gallery": ["calendar-themes.jpg", "calendar-board.jpg"],
        "gallery_captions": ["The weekly theme system — every weekday has a fixed job, so nobody starts from a blank page",
                             "Each day's row pushes itself onto the coordinator's board the morning it is due"],
    },
    {
        "slug": "philmed-expo-2026",
        "title": "PhilMed Expo 2026",
        "discipline": "marketing",
        "year": "2026",
        "featured": True,
        "tags": ["Event marketing", "Booth design", "Video production"],
        "cover": "philmed-cover.jpg",
        "cover_note": "PhilMed Expo 2026 — booth designed in 3D before fabrication",
        "summary": ("Two booths, three days, solo coverage — from the 3D booth design to the "
                    "follow-up system that held 91 leads."),
        "challenge": ("Two booths, three days, brands nobody in the room had heard of, and a "
                      "medical audience that does not respond to consumer marketing."),
        "approach": ("Designed the booth in 3D before fabrication — curved back wall, brand "
                     "fascia, backlit panels and a central demo station. Built the three-day "
                     "content plan with per-date scripts, wrote the shooting guide, then shot "
                     "and edited on-site coverage for both booths and ran the follow-up."),
        "result": ("91 leads captured and organised into a tiered follow-up system with owners "
                   "and next actions, not a stack of business cards."),
        "gallery": [{"video": ["philmed-booth-walkthrough.mp4"], "ratio": "r169"},
                    "philmed-booth.jpg", "philmed-stand.jpg", "philmed-floor.jpg",
                    "philmed-brief.jpg", "philmed-demo.jpg"],
        "gallery_captions": [
            "The walkthrough rendered from the 3D model before anything was built \u2014 "
            "used to settle sightlines, where the counter sits and what a visitor reads "
            "first, while it was still cheap to change",
            "The same stand as built — two brands sharing one island, each with its own "
            "fascia and its own wall, so neither reads as a sub-brand of the other",
            "The K-PICK wall: product boards, a looping product film and the trocar rack "
            "at hand height, all laid out in the 3D plan before anything was printed",
            "Third day, mid-morning. The counter was placed on the aisle side on purpose — "
            "the display case is what stops people, the conversation happens over it",
            "Working the floor. Every conversation that got past hello was written down "
            "the same hour, which is how the 91 leads survived the week",
            "The demo station doing its job — visitors watching the assist robot run "
            "instead of being talked at",
        ],
    },
    {
        "slug": "short-form-scripting",
        "title": "Short-form video scripting",
        "discipline": "marketing",
        "year": "2026",
        "featured": False,
        "tags": ["TikTok", "Reels", "Scriptwriting"],
        "cover": "scripting-cover.jpg",
        "cover_note": "The four-line script sheet",
        "summary": "18 scripts for a single relaunch week, in a format any shooter can execute.",
        "challenge": ("A brand needed a relaunch after going quiet, and it had to work for a "
                      "Filipino audience without sounding like an ad."),
        "approach": ("Wrote 18 scripts for one relaunch week in a four-line hook, problem, "
                     "solution, CTA format with per-scene breakdowns. Taglish hooks, "
                     "trend-aware formats."),
        "result": "A repeatable scripting format now used across all three brands.",
        "gallery": ["scripting-scenes.jpg", "scripting-week.jpg"],
        "gallery_captions": [
            "The same sheet expanded into scenes. Whoever holds the camera reads one row "
            "and shoots it \u2014 visual, on-screen text, audio, seconds \u2014 so a script "
            "handed to a different person still comes back looking like the same brand",
            "The week is planned as a sequence, not as 18 separate ideas: comeback, problem, "
            "product, proof, offer, community. That order is why the week builds instead of "
            "saying the same thing six times",
        ],
    },
    # ---------------------------------------------------------- GRAPHIC
    {
        "slug": "banners-tarpaulins",
        "title": "Banners, tarpaulins & print layout",
        "discipline": "graphic",
        "year": "2026",
        "featured": True,
        "tags": ["Large-format layout", "Print production", "Brand systems"],
        "cover_note": "Image — tarpaulin & banner layouts",
        "summary": ("Large-format work laid out for print — sized, bled and readable from "
                    "across a hall."),
        "challenge": ("Print is unforgiving. A tarpaulin that reads well on a laptop can be "
                      "illegible at three metres, and a file sent without bleed comes back wrong."),
        "approach": ("Laid out banners, tarpaulins, standees and booth panels at true size with "
                     "correct bleed and margins, type scaled to viewing distance, and colours "
                     "checked for print rather than screen."),
        "result": "Files that print right the first time, on brand across every size.",
        "gallery": ["Image — tarpaulin layout", "Image — booth panel set"],
    },
    {
        "slug": "social-graphics",
        "title": "Social media graphics & pubmats",
        "discipline": "graphic",
        "year": "2026",
        "featured": False,
        "tags": ["Pubmats", "Brand templates", "Carousels"],
        "cover_note": "Image — pubmat set",
        "summary": ("Daily graphics across three brands, built on templates so the look holds "
                    "when someone else produces them."),
        "challenge": ("Daily posting across three brands with different palettes, and more than "
                      "one person producing the artwork."),
        "approach": ("Built template systems per brand — grids, type scale, colour rules — then "
                     "produced the pubmats, carousels and campaign sets on top of them."),
        "result": "A consistent look that survives being handed to someone else.",
        "gallery": ["Image — pubmat series", "Image — carousel set"],
    },
    # ---------------------------------------------------------- RENDERING
    {
        "slug": "product-rendering",
        "title": "Product rendering",
        "discipline": "rendering",
        "year": "2026",
        "featured": True,
        "tags": ["Blender", "Product visualisation"],
        "cover_note": "Image — rendered product",
        "summary": ("Products built from manufacturer specifications and rendered, because "
                    "photography was not possible."),
        "challenge": ("Medical syringes are small, transparent and nearly impossible to "
                      "photograph well. Suppliers sent nothing usable."),
        "approach": ("Built the products in Blender from real manufacturer specifications and "
                     "rendered turntables and transparent stills, plus an eight-scene animated "
                     "product film with callouts and spec overlays."),
        "result": "Marketing visuals for products we had no photography for.",
        "gallery": ["Image — turntable frame", "Image — spec overlay scene"],
    },
    # ---------------------------------------------------------- INTERIOR
    {
        "slug": "interior-decoration",
        "title": "Interior decoration",
        "discipline": "interior",
        "year": "2026",
        "featured": True,
        "tags": ["Condos & homes", "SketchUp", "Materials & costing"],
        "cover_note": "Image — interior visual",
        "summary": ("Decoration for condos and homes — modelled to real measurements, with a "
                    "costed materials list behind it."),
        "challenge": ("Clients want to see the room before they commit, and they want to know "
                      "what it will cost before they say yes."),
        "approach": ("Measured the space and modelled it to exact dimensions, worked out the "
                     "finishes, furniture and layout, then produced a materials take-off from "
                     "the model and turned it into an estimate covering materials and labour."),
        "result": "A room the client can see, with a number they can decide on.",
        "gallery": ["Image — living area", "Image — quantity schedule"],
    },
    # ---------------------------------------------------------- SYSTEMS
    {
        "slug": "multimedia-hub",
        "title": "K-PICK Multimedia Hub",
        "discipline": "systems",
        "year": "2026",
        "featured": True,
        "tags": ["UX / UI design", "Dashboard design", "Flask", "Notion API", "Role-based access"],
        "cover": "hub-cover.jpg",
        "cover_note": "The Hub dashboard — manager view",
        "summary": ("A web dashboard with role-based access, built so leadership could stop "
                    "asking for updates."),
        "challenge": ("Content, leads, tasks and attendance lived in four places, and leadership "
                      "could not see progress without asking."),
        "approach": ("Built a web dashboard with login and role-based access — manager, member "
                     "and viewer each see something different. Content calendar, lead tracker, "
                     "task board, daily log and attendance, with Notion as the backend."),
        "result": "Leadership checks the dashboard instead of asking.",
        "gallery": ["hub-roles.jpg", "hub-leads.jpg"],
        "gallery_captions": ["Manager, member and viewer each get a different screen from the same data",
                             "Lead tracker — tier decides the owner, status is set by whoever spoke to them last"],
    },
    {
        "slug": "kibo",
        "title": "Kibo \u2014 reporting bot & desktop assistant",
        "discipline": "systems",
        "year": "2026",
        "featured": True,
        "tags": ["Telegram bot", "AI assistant", "Python", "Desktop app", "Automation"],
        "cover": "kibo-cover.jpg",
        "cover_note": "Kibo — desktop assistant and reporting bot",
        "summary": ("A character with two jobs: a Telegram bot that writes the daily "
                    "report, and a desktop assistant that quietly records what the work "
                    "day actually consisted of."),
        "challenge": ("The end-of-day report was written by hand every evening, from "
                      "memory, at the point in the day when memory is worst. Whole tasks "
                      "went unrecorded \u2014 especially the ones done in cloud tools, which "
                      "leave no file behind to remind you."),
        "approach": ("Built Kibo as one character across two surfaces. On Telegram he "
                     "assembles the end-of-day report from the day's activity and sends it "
                     "on command. On the desktop he sits on screen, tracks which "
                     "application and which piece of work is in front, and writes those "
                     "into the day's log by himself \u2014 with idle detection so a window "
                     "left open overnight is not billed as work, and a privacy filter so "
                     "personal apps and files never reach a report leadership reads."),
        "result": ("The daily report writes itself from real activity instead of memory, "
                   "and the work done in cloud tools \u2014 previously invisible \u2014 now "
                   "appears in it."),
        "gallery": ["kibo-desktop.jpg", "kibo-report.jpg", "kibo-menu.jpg"],
        "gallery_captions": ["Kibo on the desktop \u2014 tracks the app in front and logs it to the day",
                             "The end-of-day report, assembled and sent on Telegram",
                             "Right-click menu \u2014 write to EOD, pause, or fix a wrong entry"],
    },
    {
        "slug": "automation-stack",
        "title": "The automation stack — AI agents, bots & MCP integrations",
        "discipline": "systems",
        "year": "2026",
        "featured": True,
        "tags": ["AI agents", "Python", "Telegram Bot API", "MCP integrations", "Monitoring"],
        "cover": "automation-cover.jpg",
        "cover_note": "The automation stack — architecture",
        "summary": ("Six services in production, built and maintained with AI agents: a Telegram "
                    "bot that writes the daily report, a desktop activity tracker, a watchdog, "
                    "an ERP-to-dashboard pipeline, Notion automations over MCP, and mail sync "
                    "with translation."),
        "challenge": ("Reporting, monitoring and admin were eating hours that should have gone "
                      "to content — and every task had the same shape: fetch something from one "
                      "place, transform it, post it somewhere else, on a schedule."),
        "approach": ("Built the stack in Python with AI coding agents (Claude, Antigravity) doing "
                     "the heavy lifting and me directing, testing and owning the system. In "
                     "production: a Telegram bot (Bot API) that collects files and window titles "
                     "and writes the end-of-day report, a desktop tracker with idle detection and "
                     "a privacy filter, a watchdog that restarts what dies, an ERP feed classified "
                     "into sales actions on a Flask dashboard, Notion databases read and written "
                     "over MCP, nightly backups, IMAP mail sync with Korean translation, and local "
                     "Whisper transcription. Every service has a single-instance lock, a log, and "
                     "a test harness."),
        "result": ("The daily report writes itself, the dashboard tells the team what to do with "
                   "slow-moving stock, and a supervisor keeps the stack up without babysitting. "
                   "The same pattern — fetch, transform, post, on a schedule — is what I set up "
                   "for other people: Telegram, Notion, marketplaces, image hosts, browser steps."),
        "gallery": ["automation-diagram.jpg", "automation-report.jpg", "automation-products.jpg"],
        "gallery_captions": ["The report pipeline — five inputs, one collector, three destinations",
                             "A day's report, assembled and sent without a line typed by hand",
                             "The ERP feed classified into one action per product"],
    },
]

# The three-panel story at the top of the About page.
PATTERN = [
    {"label": "The pattern",
     "text": ("A brand usually looks like three different companies. The marketplace "
              "listing, the daily post and the tarpaulin at the door were each made by "
              "someone different \u2014 so none of them match.")},
    {"label": "What I do",
     "text": ("I take the whole surface \u2014 the shop, the calendar, the print, the renders, "
              "the space \u2014 and design it as one thing. Then I build the system that keeps "
              "it consistent after I hand it over.")},
    {"label": "What happens",
     "text": ("In practice that means three brands across three marketplaces, around 30 "
              "posts each per month, an exhibition booth, and a dashboard leadership "
              "actually checks.")},
]

PHILOSOPHY = "I would rather build the boring system than do the same task ninety times."

# ---------------------------------------------------------------------------
# BACKGROUND — training and study.
# Written as what you studied, not as a degree. Never claim a qualification
# you do not hold; a portfolio is judged on the work, and an overstated line
# here is the one thing that can undo all of it.
# Set BACKGROUND = None to remove the block entirely.
# ---------------------------------------------------------------------------
BACKGROUND = {
    "label": "Education",
    "degree": "Bachelor of Science in Architecture",
    "school": "University of Northeastern Philippines",
    # Bullets under the school. Add or remove freely.
    "points": [
        "Relevant coursework in Process Design and Project Management.",
    ],
    # The completion status. Leave "" to keep it off.
    "note": "",
}

# ---------------------------------------------------------------------------
# CREDENTIALS — positions held and certifications. Newest first.
# 'org' can be left blank. Keep these factual and verifiable.
# ---------------------------------------------------------------------------
CREDENTIALS = [
    {"role": "Creative Member",      "org": "UAPSA – University of Northeastern Philippines", "period": "2025–2026"},
    {"role": "Deputy Creative Head", "org": "UAPSA – University of Northeastern Philippines", "period": "2024–2025"},
    {"role": "Multimedia Director",  "org": "UAPSA – University of Northeastern Philippines", "period": "2023–2024"},
    {"role": "Safety Officer 2 (SO2)", "org": "DOLE-accredited training", "period": ""},
]

# Real quotes only — never invent one.
# While this list is empty the section still shows, with placeholder cards
# marked "pending", so you can see where they will sit.
# Format:  {"quote": "...", "name": "...", "role": "..."}
#   "photo"  — a file in site/assets/images/  (leave "" and it uses initials)
#   "quote"  — leave "" and the card shows as pending with their name on it
TESTIMONIALS = [
    {
        "quote": ("What I like most about working with her is that she doesn\u2019t just focus "
                  "on making things look good \u2014 she also thinks about how to make the work "
                  "easier and more efficient. Her graphic designs are clean and well thought "
                  "out, and her automation skills really help reduce repetitive tasks. She\u2019s "
                  "creative, organized, dependable, and always willing to find a better way "
                  "to get things done."),
        "name":  "Leila Almario",
        "role":  "Social Media, K-PICK Trading Corp.",
        "photo": "leila.jpg",
    },
    {
        "quote": ("Most designers hand you a picture; Jamie hands you a system. When we "
                  "launched the K-Pick website and synced our catalog to Shopee, Lazada, and "
                  "TikTok Shop, her photography, renders, and creatives were consistent across "
                  "every channel, correctly sized, and ready the day we needed them. She is "
                  "also comfortable in tools like Notion, n8n, and Telegram bots, so she meets "
                  "our automation work halfway instead of working around it. Reliable, fast, "
                  "and genuinely good at making the company look like one brand."),
        "name":  "Jhon Wilfred",
        "role":  "K-PICK Trading Corp.",          # <- add his exact title here
        "photo": "jhon.jpg",
    },
]

# How many placeholder cards to show while TESTIMONIALS is still empty.
TESTIMONIALS_PENDING = 1

EXPERTISE = [
    {"group": "Marketing & Content", "items": [
        "Content calendar strategy", "Social media management",
        "Short-form scripting for TikTok, Reels and Facebook",
        "Video production and editing", "Event and exhibit coverage",
        "Copywriting in English, Filipino and Taglish"]},
    {"group": "E-Commerce", "items": [
        "Shopee, Lazada and TikTok Shop", "Storefront and campaign design",
        "Listing graphics and A+ content", "Title, keyword and image optimisation",
        "Marketplace compliance and violation resolution"]},
    {"group": "Graphic & Layout", "items": [
        "Banners, tarpaulins and standees", "Large-format print layout",
        "Pubmats and carousels", "Brand template systems",
        "Corporate collateral and presentations"]},
    {"group": "Rendering & Interior", "items": [
        "Blender product rendering", "SketchUp modelling",
        "Interior decoration for condos and homes",
        "Materials take-off and cost estimation", "Booth and exhibition design"]},
    {"group": "Brand Sourcing & Research", "items": [
        "Korean manufacturer sourcing", "Supplier and product-line comparison",
        "Market and competitor research", "Regulatory feasibility screening",
        "B2B lead generation", "Bilingual executive reporting"]},
    {"group": "Systems & Automation", "items": [
        "Internal dashboard development in Flask", "Bot development",
        "Notion databases and workflow automation", "Process automation and monitoring",
        "Data structuring and lead management"]},
]

# Grouped by what you use it for, not one long line.
# NOTE: only tools you actually use are listed. Add Photoshop / Illustrator
# here if you use them — I left them out because I could not confirm it.
STACK = [
    {"group": "Design & Layout", "items": [
        "Photoshop", "Illustrator", "Lightroom Classic", "Canva", "Photoroom",
        "Figma", "Superdesign"]},
    {"group": "3D & Space", "items": [
        "Blender", "SketchUp", "LayOut", "Enscape"]},
    {"group": "Video", "items": [
        "CapCut", "DJI Osmo", "HeyGen", "Whisper"]},
    {"group": "AI & Automation", "items": [
        "Claude", "Cowork", "n8n", "GoHighLevel", "Python", "Notion",
        "Telegram Bot API"]},
    {"group": "Web & Systems", "items": [
        "HTML / CSS / JS", "Flask", "Wix", "Vercel", "IMAP / REST APIs"]},
]

ABOUT = ("I work across marketing, e-commerce, layout, rendering and interior decoration — "
         "and I build the internal systems that keep the work moving without me in the "
         "middle of it. That range is what turned into the job title: Multidisciplinary "
         "Creative Specialist.")

# ---------------------------------------------------------------------------
# BIO — the long-form version on the About page. Structured on purpose:
# role stated plainly, then the main body of work, then everything built
# alongside it. Wrap a phrase in **double asterisks** for bold — build.py
# converts it to <strong>, everything else is escaped as plain text.
# ---------------------------------------------------------------------------
BIO = [
    ("I'm a **Multidisciplinary Creative Specialist** — I take on whatever a brand's "
     "surface needs: the marketplace listing, the daily post, the print, the render, "
     "the room. I design it as one system, then build the automation that keeps it "
     "consistent after I hand it over."),

    ("My general experience centres on marketing and e-commerce across three "
     "marketplaces — **Shopee, Lazada and TikTok Shop**. That covers storefront design, "
     "listing graphics and A+ content, title and image optimisation, and clearing "
     "flagged or restricted listings, alongside running **content calendars** that keep "
     "multiple brands posting on schedule."),

    ("Beyond that, I build **internal automation systems** — dashboards with "
     "role-based access for content, leads, tasks and attendance, and bots that write "
     "reports from real activity. I also produce **product renders in Blender** for "
     "items no camera can photograph, design **interior spaces in SketchUp** for condos "
     "and homes, and source and vet manufacturers for new brands to carry. I focus on "
     "work that stays correct and consistent long after I've moved on to the next thing."),
]
