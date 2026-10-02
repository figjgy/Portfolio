# SUPERDESIGN PROMPT — paste this whole block

*Attach `Portfolio_Foundation_Jamielyn.md` alongside it.*
*Then export the code and deploy to Vercel.*

---

Build a one-page personal portfolio website. It will be opened by tapping an NFC business card, so design mobile-first — it has to load fast and read well on a phone held in one hand. Make it responsive up to desktop.

**Who it's for**

Jamielyn Ludovice — Marketing & Multimedia at K-PICK Trading Corp., a Korean medical-device importer in Manila. Her range is the story: content and video, 3D product rendering, interior and exhibition booth design, and she builds the internal software her team runs on. Most portfolios show one of those. This one shows four.

**Opening line**

"Marketing & Multimedia at K-PICK Trading Corp. I run content for three brands, model products and exhibition spaces in 3D, and build the internal systems that keep it all running."

**Critical layout rule**

The contact block and a "Save to Contacts" button go at the very TOP, above the work. Someone who taps the card wants the phone number in three seconds, not after scrolling a portfolio. Make the Save button a real vCard download, not a mailto link.

**Sections, in this order**

1. Hero — name, role, positioning line, photo, contact block, Save to Contacts button
2. Stats — 4 numbers, large type, no icons
3. Selected work — 9 project cards in 4 labelled groups: **Spatial & 3D** first, then **Content & Video**, then **Systems & Automation**, then **Strategy & Research**
4. Skills — 5 groups, plain text, no progress bars and no percentage ratings
5. Tools — one compact row
6. About — three or four sentences
7. Footer — contact repeated

**Project card structure**

Each card: large image area at the top, then title, then a one-line discipline tag, then Challenge / What I did / Result as three short blocks. The image area must be prominent — the 3D and interior work is the strongest material and the layout should assume a real render is going there. Include visible placeholders where images go.

**Visual direction**

Confident and quiet. Medical-industry professional, not agency-creative. Generous whitespace, one accent colour, strong typographic hierarchy, real editorial rhythm — this should look like a considered document, not a template. No gradient meshes, no glassmorphism, no floating 3D blobs, no stock illustration.

Type: a serif or a distinctive geometric sans for headings, a clean neutral sans for body. Set body at 16–17px with generous line height.

Give me **two directions**: one light, one dark. Same structure, different atmosphere.

**Build notes**

- Single self-contained page. Inline the CSS. No build step required — it must deploy to Vercel as a static file.
- Semantic HTML, proper heading order, alt text on every image.
- Fast: system fonts or a single web font, no heavy libraries.
- Smooth scroll, subtle reveal on scroll at most. No parallax, no autoplay anything.
- Tap targets at least 44px. It will be used on a phone, one-handed, possibly standing at a trade show.

**Content rule — important**

Do not invent anything. Use only the attached foundation document for every word. Where the foundation marks something as missing (contact details, years of experience, education), leave a clearly visible placeholder rather than making something up.
