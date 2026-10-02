# SUPERDESIGN PROMPT v3 — full navigable site, content-driven
*Paste the whole block. Attach `Portfolio_Foundation_Jamielyn.md`.*
*Supersedes v1 and v2 — same palette, different architecture.*

---

Build a multi-page portfolio website, not a single scrolling page. Every project is clickable and opens its own page with its own URL. All content comes from one editable file so the owner can update the site without touching any code.

Deploy target is **Vercel**.

---

## 1 · Architecture — this part matters most

Use **Next.js (App Router) with static export**, or **Astro**. Either deploys to Vercel with zero configuration. Do not hand-write nine separate HTML files.

```
/content/site.js          ← ALL text, projects and links live here. The only file she edits.
/app/page.jsx             ← home
/app/work/page.jsx        ← all projects, filterable by discipline
/app/work/[slug]/page.jsx ← one page per project, generated from site.js
/app/about/page.jsx       ← about + skills + tools
/app/not-found.jsx        ← 404
```

Project pages must be **statically generated** from the content file — `generateStaticParams` in Next, or `getStaticPaths` in Astro. Adding a project means adding one object to the array. Nothing else.

## 2 · The content file — spell this schema out exactly

```js
export const profile = {
  name: "Jamielyn Ludovice",
  subtitle: "MULTIMEDIA · 3D · SPATIAL DESIGN · SYSTEMS",
  intro: "Multimedia designer working across four things most people keep separate: content and video, 3D product visualisation, interior and exhibition design, and the systems that run them.",
  photo: "/images/profile.jpg",
  phone:        { display: "+63 939 488 6685", link: "tel:+639394886685" },
  email:        { display: "ludovice.jamielyn00@gmail.com", link: "mailto:ludovice.jamielyn00@gmail.com" },
  linkedin:     { display: "linkedin.com/in/jamielyn-ludovice",
                  link: "https://www.linkedin.com/in/jamielyn-ludovice-4b0a25380/" },
};

export const stats = [
  { number: "91", label: "Projects delivered" },
  // …
];

export const disciplines = [
  { id: "spatial",  name: "Spatial & 3D" },
  { id: "content",  name: "Content & Video" },
  { id: "systems",  name: "Systems & Automation" },
  { id: "strategy", name: "Strategy & Research" },
];

export const projects = [
  {
    slug: "eroptix-booth",           // becomes /work/eroptix-booth
    title: "EROPTIX exhibition booth",
    discipline: "spatial",
    tags: ["SketchUp", "Ruby scripting", "Brand environments"],
    year: "2026",
    cover: "/images/eroptix-booth/cover.jpg",
    gallery: [
      { src: "/images/eroptix-booth/01.jpg", caption: "" },
    ],
    challenge: "…",
    approach:  "…",
    result:    "…",
    featured: true,                  // shows on the home page
  },
];

export const skills = [ { group: "Spatial & 3D", items: ["…"] } ];
export const tools  = ["SketchUp", "Blender", "…"];
```

Put a comment block at the top of the file, written for a non-developer, explaining how to add a project and where to drop the images.

## 3 · Pages

**Home** — hero with name, subtitle, intro, contact block and Save to Contacts. Stats row. Four or five featured projects. Link to see all work. Short about teaser. Footer.

**Work index** — every project as a card in a responsive grid. Filter buttons across the top by discipline: All · Spatial & 3D · Content & Video · Systems & Automation · Strategy & Research. Filtering is client-side and instant, no page reload. Show the active filter clearly.

**Project detail** — large cover image, title, discipline, year, tag row. Then Challenge, Approach, Result as clearly separated blocks. Then the gallery. At the bottom: previous / next project links, and a back-to-work link. This page must read well on its own, because it will be sent as a single link.

**About** — the longer bio, the five skill groups, the tool row, and contact repeated.

**404** — in the same design. A missing page should not look broken.

## 4 · Navigation

Fixed header on every page: name or a monogram on the left, links on the right — Work, About, Contact. On mobile it collapses to a hamburger opening a full-screen crimson panel with off-white links. Mark the current page with a crimson underline.

Contact in the nav scrolls to the footer block, it is not a separate page.

## 5 · Palette — exact values, nothing outside this

```
--black:       #0B0B0B    base
--crimson:     #8B0D1A    the single accent
--off-white:   #F5F2ED    all body text on dark
--surface:     #141414    cards
--hairline:    rgba(245,242,237,0.12)
--muted:       rgba(245,242,237,0.62)
--crimson-dim: rgba(139,13,26,0.18)
```

**Contrast rules — measured, not preferences:**

- **Never put crimson text on black.** #8B0D1A on #0B0B0B is **2.03:1** — illegible and fails accessibility. This is the easiest mistake to make with this palette, so check every heading.
- Off-white on black is **17.6:1** — all body copy and headings.
- Off-white on crimson is **8.7:1** — buttons are crimson fill with off-white text, never reversed.

Crimson is for fills and gestures only: buttons, active states, thin rules, tag chips, stat numerals, the nav underline, and one soft radial glow in the home hero — used once on the whole site, nowhere else.

## 6 · Typography

High-contrast serif for the name and headings — Playfair Display, Cormorant or similar. Quiet neutral sans for everything else. Eyebrow labels in uppercase sans, letter-spacing ~0.18em. Body 16–17px, line height 1.65.

## 7 · Atmosphere

Premium and restrained. A well-set book, not a landing page. Deep black ground, generous negative space, one crimson gesture per screen. No gradient meshes, no glassmorphism, no neon, no stock illustration, no parallax.

## 8 · Header copy

Name: **Jamielyn Ludovice**
Subtitle: **MULTIMEDIA · 3D · SPATIAL DESIGN · SYSTEMS**

Intro as plain text — **no quotation marks, no italics.** It is her own statement, not a testimonial.

**Remove entirely, do not leave as placeholders:** the `[YEARS OF EXP]` line and the Education section.

## 9 · Save to Contacts

Crimson fill, off-white text, full width on mobile, in the hero and in the footer. Downloads a real vCard file:

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

## 10 · Technical requirements

- Mobile-first. It will be opened by tapping an NFC card, one-handed, possibly standing at a trade show. Tap targets at least 44px.
- Static export — no server, no database, no API routes.
- Per-page `<title>` and meta description pulled from the content file. Open Graph tags so shared links preview properly.
- Semantic HTML, correct heading order, alt text on every image from the content file.
- Next.js `Image` or equivalent, lazy loading below the fold.
- Visible, correctly sized placeholders wherever an image is missing — it should be obvious what still needs supplying.
- One web font family plus a system sans. No heavy libraries.

## 11 · Content rule

Do not invent anything. Every word comes from the attached foundation document. Nine projects, four disciplines, five skill groups.
