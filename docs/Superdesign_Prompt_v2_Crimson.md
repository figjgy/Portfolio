# SUPERDESIGN PROMPT v2 — Crimson palette
*Paste the whole block below. Attach `Portfolio_Foundation_Jamielyn.md`.*

---

Redesign the portfolio using this exact three-colour palette. Nothing outside it.

**Palette — use these hex values, do not substitute or tint**

```
--black:      #0B0B0B    near-black, the base
--crimson:    #8B0D1A    deep crimson, the single accent
--off-white:  #F5F2ED    warm off-white, all body text on dark
```

Derive only these from the three — no new hues:

```
--surface:    #141414    cards on black, a lift from the base
--hairline:   rgba(245,242,237,0.12)    dividers and card borders
--muted:      rgba(245,242,237,0.62)    secondary text, labels, captions
--crimson-dim: rgba(139,13,26,0.18)     tag and chip backgrounds
```

**Contrast rules — these are measured, follow them exactly**

- **Never set crimson as text on black.** #8B0D1A on #0B0B0B is only **2.03:1**. It is illegible and it fails accessibility. This is the single easiest mistake to make with this palette.
- Off-white on black is **17.6:1** — use it for all body copy and headings.
- Off-white on crimson is **8.7:1** — this is why buttons are crimson fill with off-white text, never the reverse.
- Crimson on off-white is **8.7:1** — in the light version, crimson text is fine.

**So crimson is used only for:** button fills, the active state, thin rules and dividers, small caps eyebrow labels *(only on off-white, never on black)*, a hairline under section headings, numerals in the stats row, and one large tinted shape in the hero.

**Typography**

High-contrast serif display for the name and section headings — Playfair Display, Cormorant or similar, with real weight contrast. A quiet neutral sans for everything else. The reference image gets its feel from that pairing: a wide, elegant serif against wide-tracked small caps.

- Name: serif, large, tight leading
- Section headings: serif, medium
- Eyebrow labels: sans, uppercase, letter-spacing around 0.18em, small, crimson on light / muted off-white on dark
- Body: sans, 16–17px, line height 1.65

**Atmosphere**

Premium and restrained. Think a well-set book cover, not a landing page. Deep black ground, generous negative space, one crimson gesture per screen and no more. A soft crimson radial glow bleeding in from a corner of the hero is welcome — the reference image does this well — but keep it subtle and use it once, nowhere else.

No gradient meshes. No glassmorphism. No neon. No drop shadows on text. No stock illustration.

**Structure — unchanged from the current build**

1. Hero — name, subtitle line, contact block, Save to Contacts button
2. Stats — 4 numbers, serif numerals in crimson, off-white labels
3. Selected work — 9 cards in 4 labelled groups: Spatial & 3D, then Content & Video, then Systems & Automation, then Strategy & Research
4. Skills — 5 groups, plain text, no bars or percentages
5. Tools — one compact row
6. Footer — contact repeated

**Header copy — replace what is there now**

Name: **Jamielyn Ludovice**

Subtitle, directly under the name, small caps with wide tracking:
**MULTIMEDIA · 3D · SPATIAL DESIGN · SYSTEMS**

Intro paragraph, set as plain text — **no quotation marks and no italics**. It is her own statement, not a testimonial:

> Multimedia designer working across four things most people keep separate: content and video, 3D product visualisation, interior and exhibition design, and the systems that run them.

**Remove entirely** — do not leave as placeholders:
- the `[YEARS OF EXP]` line in the header
- the Education section

**Contact**

```
Phone     display +63 939 488 6685      link tel:+639394886685
Email     ludovice.jamielyn00@gmail.com link mailto:ludovice.jamielyn00@gmail.com
LinkedIn  display linkedin.com/in/jamielyn-ludovice
          link https://www.linkedin.com/in/jamielyn-ludovice-4b0a25380/
```

Save to Contacts button — crimson fill, off-white text, full width on mobile. It must download a real vCard:

```
BEGIN:VCARD
VERSION:3.0
N:Ludovice;Jamielyn;;;
FN:Jamielyn Ludovice
TITLE:Multimedia · 3D · Spatial Design
TEL;TYPE=CELL:+639394886685
EMAIL;TYPE=INTERNET:ludovice.jamielyn00@gmail.com
URL:https://www.linkedin.com/in/jamielyn-ludovice-4b0a25380/
END:VCARD
```

**Project cards**

Large image area at the top of each card, 4:3 or 3:2. The 3D, booth and interior work are the strongest material and the layout must assume a real render is going there — do not design around small thumbnails. Card body: title in serif, discipline tag as a crimson-tinted chip, then Challenge / What I did / Result as three short blocks with off-white labels.

Show visible placeholders where images go, sized correctly, so it is obvious what is still missing.

**Build**

Single self-contained page, CSS inlined, no build step — it deploys to Vercel as a static file. Semantic HTML, correct heading order, alt text on every image. One web font family maximum plus a system sans. Tap targets at least 44px. Smooth scroll; a subtle fade-up on scroll at most, nothing more.

**Content rule**

Do not invent anything. Every word comes from the attached foundation document.
