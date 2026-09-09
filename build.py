#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUILD THE PORTFOLIO SITE
------------------------
Everything you can change lives in content.py.
Edit that file, then run:      python build.py
The whole site is written into  site/  ready to drag onto Vercel.
"""
import os, re, shutil, html, urllib.parse
from content import (PROFILE, STATS, DISCIPLINES, PROJECTS, EXPERTISE, STACK, ABOUT, BIO,
                     PATTERN, PHILOSOPHY, TESTIMONIALS, TESTIMONIALS_PENDING,
                     MARQUEE, CREDENTIALS, BACKGROUND)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
E = html.escape
_url_quote = urllib.parse.quote


def paras(text):
    """Escape, and turn a blank line in content.py into a real paragraph break.

    Without this a two-paragraph 'approach' rendered as one unbroken wall of
    text - the \\n\\n survived into the HTML, where it is just whitespace.
    """
    blocks = [b.strip() for b in (text or "").split("\n\n") if b.strip()]
    return "".join("<p>%s</p>" % E(b) for b in blocks) or "<p></p>"


def bio_html(paragraphs):
    """Escape each paragraph, then turn **text** into <strong>text</strong>."""
    out = []
    for para in paragraphs:
        safe = E(para)
        safe = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)
        out.append(f'<p style="margin-top:1rem;color:var(--dim)">{safe}</p>')
    return "".join(out)

# ----------------------------------------------------------------- shared css
CSS = """
/* ---- theme tokens ------------------------------------------------------ */
:root{
 --bg:#0B0B0B;--ink:#F5F2ED;--dim:rgba(245,242,237,.62);
 --acc:#8B0D1A;--acc-lift:#A81324;--acc-text:#E8909C;
 --glass:rgba(245,242,237,.055);--glass-2:rgba(245,242,237,.085);
 --edge:rgba(245,242,237,.14);--edge-top:rgba(245,242,237,.30);
 --shade:rgba(0,0,0,.55);--blob1:rgba(139,13,26,.16);--blob2:rgba(139,13,26,.07);
 --max:62rem;--pad:1.5rem;--rad:20px;
}
[data-theme="light"]{
 --bg:#EFEBE4;--ink:#12100F;--dim:rgba(18,16,15,.62);
 --acc:#8B0D1A;--acc-lift:#700A15;--acc-text:#8B0D1A;
 --glass:rgba(255,255,255,.45);--glass-2:rgba(255,255,255,.62);
 --edge:rgba(18,16,15,.10);--edge-top:rgba(255,255,255,.85);
 --shade:rgba(90,70,70,.14);--blob1:rgba(139,13,26,.10);--blob2:rgba(139,13,26,.05);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
font-family:'Jost',system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.7;
font-weight:300;letter-spacing:.005em;
-webkit-font-smoothing:antialiased;padding-top:5.25rem;padding-bottom:3rem;overflow-x:hidden;
transition:background .35s,color .35s}
h1,h2,h3,h4,.serif{font-family:'Cormorant Garamond',Georgia,serif;margin:0;
line-height:1.15;font-weight:400;letter-spacing:.005em}
p{margin:0}a{color:inherit;text-decoration:none}img{max-width:100%;display:block}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--pad);width:100%;position:relative;z-index:1}
.eyebrow{font-size:10.5px;text-transform:uppercase;letter-spacing:.24em;font-weight:400;
font-family:'Jost',system-ui,sans-serif}
.muted{color:var(--dim)}
.acc{color:var(--acc-text)}

/* ---- the glass substrate ----------------------------------------------- */
.blobs{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}
.blobs i{position:absolute;display:block;border-radius:50%;filter:blur(80px)}
.b1{width:62vw;height:62vw;max-width:400px;max-height:400px;background:var(--blob1);top:-18%;left:-22%}
.b2{width:48vw;height:48vw;max-width:300px;max-height:300px;background:var(--blob2);bottom:-12%;right:-18%}
.glass{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(20px) saturate(150%);backdrop-filter:blur(20px) saturate(150%);
box-shadow:0 14px 40px var(--shade),inset 0 1px 0 var(--edge-top)}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
 .glass,.pill-in{background:rgba(20,20,20,.94)}
 [data-theme="light"] .glass,[data-theme="light"] .pill-in{background:rgba(255,255,255,.94)}
}

/* ---- nav --------------------------------------------------------------- */
.pill{position:fixed;left:0;right:0;top:max(.75rem,env(safe-area-inset-top));z-index:100;
display:flex;justify-content:center;padding:0 1rem;pointer-events:none}
.pill-in{pointer-events:auto;display:flex;gap:.15rem;align-items:center;max-width:100%;
background:var(--glass-2);-webkit-backdrop-filter:blur(20px) saturate(160%);
backdrop-filter:blur(20px) saturate(160%);border:1px solid var(--edge);border-radius:999px;
padding:.4rem;box-shadow:0 12px 34px var(--shade),inset 0 1px 0 var(--edge-top);
overflow-x:auto;scrollbar-width:none;scroll-behavior:smooth}
.pill-in::-webkit-scrollbar{display:none}
.pill-in a{flex:0 0 auto;display:flex;align-items:center;padding:.7rem 1.1rem;border-radius:999px;
white-space:nowrap;font:400 13px/1 'Jost',system-ui,sans-serif;letter-spacing:.04em;color:var(--dim);min-height:40px;
transition:color .2s,background .2s}
.pill-in a:hover{color:var(--ink)}
.pill-in a.on{background:var(--acc);color:#F5F2ED}
.tgl{flex:0 0 auto;width:40px;height:40px;margin-left:.25rem;border-radius:999px;cursor:pointer;
background:transparent;border:1px solid var(--edge);color:var(--ink);font-size:15px;line-height:1;
display:flex;align-items:center;justify-content:center;transition:border-color .2s,background .2s}
.tgl:hover{border-color:var(--acc)}
.tgl svg{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.8;
stroke-linecap:round;stroke-linejoin:round;transition:transform .25s,opacity .25s}
.tgl:hover svg{transform:scale(1.08)}
[data-theme="dark"] .tgl-moon{display:none}
[data-theme="dark"] .tgl-sun{display:block}
[data-theme="light"] .tgl-sun{display:none}
[data-theme="light"] .tgl-moon{display:block}
a:focus-visible,button:focus-visible{outline:2px solid var(--acc);outline-offset:3px}

/* ---- header ------------------------------------------------------------ */
header{padding:2.5rem 0 3rem;position:relative;z-index:1}
[id]{scroll-margin-top:6rem}
h1{font-size:clamp(2.75rem,10vw,4.25rem);font-weight:300;letter-spacing:-.005em}
.sub{margin-top:.75rem}
.contact{display:flex;flex-direction:column;gap:.25rem;margin-top:2rem}
.contact a{display:flex;align-items:center;gap:.85rem;font-size:1.0625rem;min-height:46px}
.contact a:hover .ico{stroke:var(--acc-text)}
.ico-sm{width:14px;height:14px;flex:0 0 14px;stroke:currentColor;vertical-align:-2px;margin-right:.35rem}
.suite-tab .ico-sm,.cls-tab .ico-sm{stroke:currentColor}
.act-pill .ico-sm,.noimg-tag .ico-sm{width:12px;height:12px;flex-basis:12px;margin-right:0}
.plat-dot{display:inline-block;width:8px;height:8px;border-radius:50%;flex:none}
.ico{width:18px;height:18px;flex:0 0 18px;stroke:var(--dim);fill:none;stroke-width:1.8;
stroke-linecap:round;stroke-linejoin:round;transition:stroke .25s}
.socialrow{display:flex;gap:.65rem;margin-top:1.25rem;flex-wrap:wrap}
.socialrow a{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;
justify-content:center;background:var(--glass);border:1px solid var(--edge);
-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
transition:border-color .2s,transform .2s}
.socialrow a:hover{border-color:var(--acc);transform:translateY(-2px)}
.socialrow svg{width:21px;height:21px;stroke:var(--ink);fill:none;stroke-width:1.7;
stroke-linecap:round;stroke-linejoin:round}
.btn{display:flex;align-items:center;justify-content:center;gap:.6rem;background:var(--acc);
color:#F5F2ED;border:0;cursor:pointer;padding:1.15rem 2rem;border-radius:999px;
font:500 11.5px/1 'Jost',system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;
width:100%;margin-top:1.75rem;min-height:52px;box-shadow:0 8px 22px var(--shade);
transition:background .25s,transform .12s}
.btn:hover{background:var(--acc-lift)}.btn:active{transform:scale(.985)}
.btn svg{stroke:#F5F2ED;width:16px;height:16px;flex:0 0 16px}
.btn.ghost svg{stroke:currentColor}
.service-card .btn,.dfy-btns .btn,.work-btns .btn{width:100%;padding:1rem 1.25rem}
@media(min-width:840px){.dfy-btns .btn,.work-btns .btn{width:auto;min-width:240px}}

/* ---- sections ---------------------------------------------------------- */
section{padding:4rem 0;position:relative;z-index:1}
.lede{font-size:clamp(1.15rem,4.5vw,1.5rem);line-height:1.55;margin-bottom:2.5rem}
.ph{width:100%;background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);
display:flex;align-items:center;justify-content:center;text-align:center;padding:1rem;
color:var(--dim);font-size:10px;text-transform:uppercase;letter-spacing:.22em;font-weight:400}
.r43{aspect-ratio:4/3}.r34{aspect-ratio:3/4}.r32{aspect-ratio:3/2}
.r169{aspect-ratio:16/9}.r11{aspect-ratio:1/1}
.shot{position:relative;width:100%;overflow:hidden;border-radius:var(--rad);
background:var(--glass-2);border:1px solid var(--edge)}
.shot img{position:absolute;inset:0;width:100%;height:100%;
object-fit:cover;object-position:50% 50%;display:block;
transition:transform .55s cubic-bezier(.22,.61,.36,1),filter .45s ease}
/* image hover — lift and warm slightly, never crop-jump */
.shot::after{content:'';position:absolute;inset:0;pointer-events:none;opacity:0;
background:radial-gradient(70% 60% at 50% 100%,rgba(139,13,26,.28),transparent 70%);
transition:opacity .45s ease}
.gal .shot:hover img,.galfig:hover .shot img,.shotframe:hover .shot img{transform:scale(1.045)}
.gal .shot:hover::after,.galfig:hover .shot::after{opacity:1}
.gal .shot,.galfig .shot{transition:border-color .35s ease,box-shadow .35s ease}
.gal .shot:hover,.galfig:hover .shot{border-color:rgba(139,13,26,.6);
box-shadow:0 18px 46px var(--shade)}

.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem}
.stats>div{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(20px) saturate(150%);backdrop-filter:blur(20px) saturate(150%);
box-shadow:0 14px 40px var(--shade),inset 0 1px 0 var(--edge-top);padding:1.75rem 1.25rem}
.stats .n{display:block;font-family:'Cormorant Garamond',Georgia,serif;font-size:3rem;
font-weight:300;line-height:1}
.stats .n::after{content:'';display:block;width:26px;height:2px;background:var(--acc);margin-top:.75rem}
.stats .l{display:block;margin-top:.6rem}

.marquee{position:relative;z-index:1;overflow:hidden;margin:3.5rem 0;padding:1.1rem 0;
border-top:1px solid var(--edge);border-bottom:1px solid var(--edge);
background:var(--glass);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);
-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);
mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.mtrack{display:flex;width:max-content;animation:slide 46s linear infinite}
.marquee:hover .mtrack{animation-play-state:paused}
.mset{display:flex;flex:0 0 auto}
.mset span{display:flex;align-items:center;white-space:nowrap;padding:0 1.5rem;
font-size:12px;text-transform:uppercase;letter-spacing:.22em;color:var(--dim)}
.mset span::after{content:'';width:4px;height:4px;border-radius:50%;
background:var(--acc);margin-left:3rem;opacity:.7}
@keyframes slide{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
@media(prefers-reduced-motion:reduce){.mtrack{animation:none}
.marquee{-webkit-mask-image:none;mask-image:none;overflow-x:auto;scrollbar-width:none}
.marquee::-webkit-scrollbar{display:none}}

.grouphead{display:flex;align-items:center;gap:1rem;margin-bottom:2.25rem}
.grouphead::before{content:'';flex:0 0 8px;width:8px;height:8px;background:var(--acc);border-radius:2px}
.grouphead .rule{flex:1;height:1px;background:var(--edge)}

.cards{display:grid;gap:1.5rem;align-items:stretch}
.card{display:flex;flex-direction:column;height:100%;
background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(20px) saturate(150%);backdrop-filter:blur(20px) saturate(150%);
box-shadow:0 14px 40px var(--shade),inset 0 1px 0 var(--edge-top);overflow:hidden;
transition:border-color .25s,transform .25s,box-shadow .25s}
.card:hover{border-color:var(--acc);transform:translateY(-4px);
box-shadow:0 20px 50px var(--shade),inset 0 1px 0 var(--edge-top)}
.card .ph,.card .shot{border:0;border-radius:0;box-shadow:none;background:var(--glass-2);flex:none}
.card:hover .shot img{transform:scale(1.05)}
.card:hover .shot::after{opacity:1}
.card .body{padding:1.5rem;display:flex;flex-direction:column;flex:1 1 auto}
.card h3{font-size:1.5rem;font-weight:400;margin-bottom:.6rem}
.card .sum{font-size:.9375rem;color:var(--dim);margin-top:.85rem}
.card .more{margin-top:auto;padding-top:1.25rem;align-self:flex-start}
.chip{display:inline-block;background:var(--glass-2);border:1px solid var(--edge);
color:var(--ink);padding:5px 11px;border-radius:999px;font-size:10px;text-transform:uppercase;
letter-spacing:.14em;font-weight:400}
.chip.live{display:inline-flex;align-items:center;border-color:rgba(34,197,94,.32);background:rgba(34,197,94,.08);color:#86efac;margin-left:.4rem}
.live-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#22c55e;
box-shadow:0 0 8px #22c55e;margin-right:.45rem;animation:live-pulse 2s cubic-bezier(.4,0,.6,1) infinite}
@keyframes live-pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.8)}}
.live-link{display:inline-flex;align-items:center;gap:.6rem;background:var(--glass-2);border:1px solid rgba(34,197,94,.35);
color:var(--ink);border-radius:999px;padding:.65rem 1.25rem;font:400 12px/1 'Jost',system-ui,sans-serif;
letter-spacing:.14em;text-transform:uppercase;transition:border-color .2s,background .2s}
.live-link:hover{border-color:#22c55e;background:rgba(34,197,94,.12)}

.shot img{cursor:zoom-in}
.lb{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
background:rgba(11,11,11,.88);-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);
opacity:0;pointer-events:none;transition:opacity .25s ease;padding:1.5rem}
.lb.open{opacity:1;pointer-events:auto}
.lb-close{position:absolute;top:max(1rem,env(safe-area-inset-top));right:max(1rem,env(safe-area-inset-right));
width:44px;height:44px;border-radius:50%;background:var(--glass);border:1px solid var(--edge);
color:var(--ink);font-size:24px;line-height:1;display:flex;align-items:center;justify-content:center;
cursor:pointer;transition:border-color .2s,transform .2s}
.lb-close:hover{border-color:var(--acc);transform:scale(1.06)}
.lb-body{max-width:92vw;max-height:88vh;display:flex;flex-direction:column;align-items:center}
.lb-body img{max-width:100%;max-height:80vh;object-fit:contain;border-radius:12px;
box-shadow:0 24px 60px rgba(0,0,0,.65);border:1px solid var(--edge)}
.lb-cap{margin-top:.85rem;font-size:13px;color:var(--dim);text-align:center;
font-family:'Jost',system-ui,sans-serif;letter-spacing:.04em}
.more{display:inline-flex;align-items:center;gap:.5rem;margin-top:1.25rem;
font:400 12px/1 'Jost',system-ui,sans-serif;letter-spacing:.18em;text-transform:uppercase}
.more::after{content:'→';color:var(--dim)}

.filters{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:2.5rem}
.filters button{cursor:pointer;background:var(--glass);border:1px solid var(--edge);
-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
color:var(--dim);border-radius:999px;padding:.6rem 1.1rem;min-height:44px;
font:400 12px/1 'Jost',system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;
transition:color .2s,background .2s,border-color .2s}
.filters button:hover{color:var(--ink)}
.filters button.on{background:var(--acc);border-color:var(--acc);color:#F5F2ED}

.cols{display:grid;gap:1rem;margin-top:2rem}
.cols>div{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);padding:1.5rem}
.cols .lab{display:block;margin-bottom:.5rem;color:var(--dim)}
.cols p{font-size:.9375rem;color:var(--dim)}
.tags{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1rem}
.gal{display:grid;gap:1rem;margin-top:2.5rem}
.galwide{grid-column:1/-1}
.galset{padding:1.1rem 1.1rem 1rem;background:var(--glass);-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%);border:1px solid var(--edge);border-radius:var(--rad)}
.galset-head{display:flex;align-items:baseline;justify-content:space-between;gap:1rem;margin-bottom:.8rem}
.galset-head h4{font-family:'Cormorant Garamond',Georgia,serif;font-size:1.25rem;font-weight:400;margin:0;color:var(--ink)}
.galset-head .muted{font-size:12px}
.strip{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 3*.75rem)/4);gap:.75rem;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:.5rem;
scrollbar-width:thin;scrollbar-color:var(--edge) transparent}
.strip::-webkit-scrollbar{height:6px}.strip::-webkit-scrollbar-track{background:transparent}.strip::-webkit-scrollbar-thumb{background:var(--edge);border-radius:999px}
.strip .shot{scroll-snap-align:start;border-radius:12px;border:1px solid var(--edge);transition:transform .2s,border-color .2s}
.strip .shot:hover{transform:translateY(-2px);border-color:rgba(139,13,26,.55)}
.strip[data-n="1"]{grid-auto-columns:100%}
.strip[data-n="2"]{grid-auto-columns:calc((100% - .75rem)/2)}
@media(max-width:820px){.strip{grid-auto-columns:calc((100% - 2*.75rem)/3)}}
@media(max-width:520px){.strip{grid-auto-columns:calc((100% - .75rem)/2)}}
.r45{aspect-ratio:4/5}
.vidrow{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.vidrow.one{grid-template-columns:1fr}
@media(max-width:640px){.vidrow{grid-template-columns:1fr 1fr}}
.vid{position:relative;border-radius:var(--rad);overflow:hidden;background:#000;border:1px solid var(--edge)}
.vid video{display:block;width:100%;height:100%;object-fit:cover;background:#000}
.r916{aspect-ratio:9/16}
.galfig{margin:0}.galfig figcaption{font-size:12.5px;color:var(--dim);line-height:1.5;margin-top:.55rem;padding:0 .15rem}
.pn{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem}
.pn a{flex:1;background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);padding:1.25rem;font-size:.9375rem;
transition:border-color .25s}
.pn a:hover{border-color:var(--acc)}
.pn span{display:block;color:var(--dim);font-size:11px;text-transform:uppercase;
letter-spacing:.22em;font-weight:400;margin-bottom:.35rem}

.pattern{display:grid;gap:0;background:var(--glass);border:1px solid var(--edge);
border-radius:var(--rad);-webkit-backdrop-filter:blur(20px) saturate(150%);
backdrop-filter:blur(20px) saturate(150%);box-shadow:0 14px 40px var(--shade),
inset 0 1px 0 var(--edge-top);overflow:hidden}
.pattern>div{padding:1.75rem 1.5rem;border-top:1px solid var(--edge)}
.pattern>div:first-child{border-top:0}
.pattern p{margin-top:.85rem;font-size:.9375rem;color:var(--dim)}

.aboutgrid{display:grid;gap:2rem;margin-bottom:1.5rem}
.shotframe{width:100%;max-width:20rem;padding:.75rem;border-radius:calc(var(--rad) + 6px);
background:var(--glass);border:1px solid var(--edge);
-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);
box-shadow:0 14px 40px var(--shade),inset 0 1px 0 var(--edge-top)}
.shotframe .ph,.shotframe .shot{border-radius:calc(var(--rad) - 4px)}
.facts{display:grid;gap:1rem;margin-top:1.75rem}
.fact{border-bottom:1px solid var(--edge);padding-bottom:.85rem}
.fact span{display:block;margin-bottom:.3rem}
.fact a{border-bottom:1px solid transparent;transition:border-color .2s}
.fact a:hover{border-color:var(--acc)}
.creds{display:grid;gap:.75rem}
.cred{display:flex;align-items:baseline;gap:1rem;background:var(--glass);
border:1px solid var(--edge);border-radius:14px;padding:1rem 1.25rem;
-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px)}
.cred::before{content:'';flex:0 0 7px;width:7px;height:7px;border-radius:50%;
background:var(--acc);transform:translateY(-2px)}
.cred .r{flex:1;min-width:0}
.cred .r b{display:block;font-weight:400;font-size:1.0625rem}
.cred .r span{display:block;font-size:.8125rem;color:var(--dim)}
.cred time{flex:0 0 auto;font-size:.8125rem;color:var(--dim);
font-variant-numeric:tabular-nums;white-space:nowrap}
.bg-note{margin-top:1.25rem}
.bg-note .deg{display:block;margin-top:.85rem;font-size:1.0625rem}
.bg-note .sch{display:block;color:var(--dim);font-size:.9375rem}
.bg-note ul{margin:.75rem 0 0;padding-left:1.1rem;color:var(--dim);font-size:.9375rem}
.bg-note li{margin-top:.25rem}
.bg-note li::marker{color:var(--acc)}
.bg-note .stat{display:block;margin-top:.85rem;padding-top:.85rem;
border-top:1px solid var(--edge);color:var(--dim);font-size:.875rem}
.meta{margin-top:.6rem;font-size:.875rem;color:var(--dim);
text-transform:uppercase;letter-spacing:.16em}
.meta span{color:var(--acc-text);margin:0 .3rem}
.aboutbtns{display:grid;gap:.75rem;margin-top:1.75rem}
.btn.ghost{background:var(--glass);border:1px solid var(--edge);color:var(--ink);
box-shadow:none;-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.btn.ghost:hover{border-color:var(--acc);background:var(--glass-2)}
.bio{padding:1.75rem 1.5rem}
.bio p{color:var(--dim);font-size:1.0625rem}

.tools{display:grid;gap:1rem}
.tool{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);padding:1.75rem 1.5rem}
.tool ul{list-style:none;margin:1.25rem 0 0;padding:0}
.tool li{font-size:.9375rem;color:var(--dim);padding:.55rem 0;
border-top:1px solid var(--edge)}
.tool li:first-child{border-top:0;padding-top:0}
.philo{margin-top:1rem;padding:1.25rem 1.5rem}
.philo p{margin-top:.5rem;font-size:.9375rem;color:var(--dim);font-style:italic}

.qmq{position:relative;margin:0 calc(50% - 50vw);padding:.5rem 0 1rem;
overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;
scrollbar-width:none;cursor:grab;overscroll-behavior-x:contain;
-webkit-mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent);
mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent)}
.qmq::-webkit-scrollbar{display:none}
.qmq.grabbing{cursor:grabbing}
.qmq.grabbing .quotes figure{pointer-events:none}
.qtrack{display:flex;width:max-content;padding-inline:var(--pad)}
.quotes{display:flex;flex:0 0 auto}
.quotes figure{flex:0 0 auto;width:min(84vw,24rem);margin:0 .5rem;display:flex;
flex-direction:column;background:var(--glass);border:1px solid var(--edge);
border-radius:var(--rad);-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);
padding:1.75rem 1.5rem}
.quotes figure::before{content:'\u201C';display:block;font-family:'Cormorant Garamond',Georgia,serif;
font-size:3rem;line-height:.7;color:var(--acc);opacity:.55;margin-bottom:.5rem}
.quotes blockquote{margin:0;font-size:.9375rem;line-height:1.6;font-style:italic;color:var(--ink)}
.quotes .pending{border-style:dashed}
.quotes .pending::before{opacity:.28}
.quotes .pending figcaption{margin-top:.85rem}
.quotes figcaption{margin-top:auto;padding-top:1.25rem;font-size:.875rem;
display:flex;align-items:center;gap:.85rem}
.quotes figcaption strong{display:block;font-weight:400}
.quotes .who{min-width:0}
.quotes .av{flex:0 0 42px;width:42px;height:42px;border-radius:50%;object-fit:cover;
border:1px solid var(--edge)}
.quotes .ini{display:flex;align-items:center;justify-content:center;background:var(--acc);
color:#F5F2ED;font-size:.8125rem;letter-spacing:.06em}
.quotes .pending .ini{background:transparent;color:var(--dim)}
.quotes .await{color:var(--dim);font-style:normal;font-size:10px;
text-transform:uppercase;letter-spacing:.22em}
@media(prefers-reduced-motion:reduce){.qmq{scroll-behavior:auto}}

.exp{display:grid;gap:1rem;margin-top:2.5rem}
.exp>div{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);padding:1.75rem 1.5rem}
.exp h4{display:flex;align-items:center;gap:.6rem;margin:0 0 .75rem}
.exp h4::before{content:'';flex:0 0 8px;width:8px;height:8px;background:var(--acc);border-radius:2px}
.exp p{font-size:.9375rem;color:var(--dim)}
.stack{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(20px) saturate(150%);backdrop-filter:blur(20px) saturate(150%);
box-shadow:0 14px 40px var(--shade),inset 0 1px 0 var(--edge-top);padding:2rem 1.5rem}
.stackgrid{display:grid;gap:1.75rem}
.stackgrid ul{list-style:none;margin:.75rem 0 0;padding:0}
.stackgrid li{font-size:.9375rem;color:var(--dim);padding:.15rem 0}

footer{padding:4rem 0 3rem;position:relative;z-index:1}
.footin{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(20px) saturate(150%);backdrop-filter:blur(20px) saturate(150%);
box-shadow:0 14px 40px var(--shade),inset 0 1px 0 var(--edge-top);padding:2.5rem 1.75rem}
footer h2{font-size:clamp(2.25rem,8vw,3rem);font-weight:300;margin-bottom:1.5rem}
footer .contact a:hover{color:var(--acc-text)}
.copy{margin-top:2.5rem}.copy span{display:block;margin-bottom:.35rem}

.js .rv{opacity:0;transform:translateY(20px);transition:opacity .6s cubic-bezier(.4,0,.2,1),
transform .6s cubic-bezier(.4,0,.2,1)}
.js .rv.on{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.js .rv{opacity:1;transform:none;transition:none}
html{scroll-behavior:auto}.pill-in{scroll-behavior:auto}*{transition:none!important}}

@media(min-width:768px){
 body{padding-top:6rem}
 header{padding:3.5rem 0 3rem}
 .headrow{display:flex;align-items:flex-end;justify-content:space-between;gap:3rem}
 .btn{width:auto;margin-top:0}
 .stats{grid-template-columns:repeat(4,1fr)}
 .cards{grid-template-columns:repeat(2,1fr)}
 .cols.c3{grid-template-columns:repeat(3,1fr)}
 .exp{grid-template-columns:repeat(2,1fr)}
 .stackgrid{grid-template-columns:repeat(4,1fr);gap:2rem}
 .pattern{grid-template-columns:repeat(3,1fr)}
 .pattern>div{border-top:0;border-left:1px solid var(--edge)}
 .pattern>div:first-child{border-left:0}
 .aboutgrid{grid-template-columns:5fr 7fr;gap:2.5rem;align-items:start}
 .facts{grid-template-columns:repeat(2,1fr);gap:1.25rem 2rem}
 .aboutbtns{grid-template-columns:auto auto;justify-content:start}
 .tools{grid-template-columns:repeat(3,1fr)}
 .gal{grid-template-columns:repeat(2,1fr)}
 .footrow{display:grid;grid-template-columns:minmax(240px,1fr) minmax(340px,1.25fr);gap:3.5rem;align-items:start}
 .copy{text-align:left;margin-top:2rem}
}

/* ---- micro-saas scanner tool ------------------------------------------- */
.tool-grid{display:grid;gap:2rem;margin-top:2.5rem}
.tool-box{background:var(--glass);border:1px solid var(--edge);border-radius:var(--rad);
-webkit-backdrop-filter:blur(20px) saturate(150%);backdrop-filter:blur(20px) saturate(150%);
box-shadow:0 14px 40px var(--shade),inset 0 1px 0 var(--edge-top);padding:1.75rem}
.field-row{margin-bottom:1.35rem}
.field-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.45rem}
.tool-select,.tool-textarea{width:100%;background:rgba(18,16,15,.65);border:1px solid var(--edge);
color:var(--ink);border-radius:14px;padding:.85rem 1rem;font-family:'Jost',system-ui,sans-serif;
font-size:14px;line-height:1.5;box-sizing:border-box;transition:border-color .2s}
[data-theme="light"] .tool-select,[data-theme="light"] .tool-textarea{background:rgba(255,255,255,.75)}
.tool-textarea:focus,.tool-select:focus{outline:none;border-color:var(--acc)}
.count-badge{font-size:11px;color:var(--dim);letter-spacing:.04em}
.count-badge .ok{color:#4ade80}
.count-badge .warn{color:#facc15}
.count-badge .bad{color:#f87171}

/* ---- lead form (Web3Forms) ------------------------------------------- */
.lead-form{display:flex;flex-direction:column;gap:.6rem;max-width:26rem}
.lead-form .lead-hp{display:none}
.lead-row{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}
.lead-form input,.lead-form textarea{width:100%;background:rgba(18,16,15,.65);border:1px solid var(--edge);color:var(--ink);
border-radius:12px;padding:.7rem .9rem;font:inherit;font-size:13.5px;line-height:1.4;box-sizing:border-box;resize:vertical}
[data-theme="light"] .lead-form input,[data-theme="light"] .lead-form textarea{background:rgba(255,255,255,.75)}
.lead-form input:focus,.lead-form textarea:focus{outline:none;border-color:var(--acc)}
.lead-form ::placeholder{color:var(--dim);opacity:.8}
.lead-foot{display:flex;align-items:center;gap:.9rem;flex-wrap:wrap}
.lead-foot .btn{width:auto;margin:0;padding:.85rem 1.4rem;min-height:44px}
.lead-msg{font-size:12.5px;color:var(--dim)}.lead-msg.ok{color:#4ade80}.lead-msg.bad{color:#f87171}
footer .lead-col{display:flex;flex-direction:column;gap:.9rem;padding-top:.6rem}
footer .lead-col h3{font-size:1.05rem;font-weight:400;color:var(--ink);margin:0}
footer .lead-col p{font-size:13px;color:var(--dim);margin:0 0 .35rem;line-height:1.55}
footer .lead-form{max-width:none;margin:0}
footer .lead-form input,footer .lead-form textarea{padding:.85rem 1rem;font-size:14px;border-radius:12px}
footer .lead-form textarea{min-height:104px}
footer .lead-foot .btn{min-height:52px;padding:1rem 1.6rem}
footer .lead-foot{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem}
footer .lead-foot .btn{width:auto;margin:0;min-height:52px;padding:1rem 1.5rem;flex:none}
footer .lead-foot .lead-msg{flex-basis:100%}
@media(max-width:820px){.footrow{grid-template-columns:1fr}.copy{margin-top:1.5rem}}
@media(max-width:520px){footer .lead-foot .btn{width:100%}}
@media(max-width:640px){.lead-row{grid-template-columns:1fr}}
.jl-lead{padding:0 1.1rem .9rem}
#jl-lead[hidden]{display:none!important}
.jl-chat.lead-on .jl-chips,.jl-chat.lead-on .jl-chat-form{display:none}
.jl-lead-back{display:block;width:100%;margin-bottom:.55rem;background:transparent;border:0;color:var(--dim);font:inherit;font-size:12px;cursor:pointer;text-align:left;padding:0}
.jl-lead-back:hover{color:var(--ink)}
.jl-lead .lead-form{max-width:none;gap:.45rem}
.jl-lead .lead-form input,.jl-lead .lead-form textarea{padding:.55rem .8rem;font-size:13px;border-radius:10px}
.jl-lead .lead-foot .btn{padding:.6rem 1.1rem;min-height:38px;font-size:11px}

/* ---- assistant chat widget ------------------------------------------- */
.jl-chat-fab{position:fixed;right:22px;bottom:22px;z-index:300;width:54px;height:54px;border-radius:50%;
background:var(--acc);border:0;cursor:pointer;display:flex;align-items:center;justify-content:center;
box-shadow:0 12px 30px rgba(139,13,26,.45),0 0 0 1px rgba(255,255,255,.06);transition:transform .2s}
.jl-chat-fab:hover{transform:translateY(-2px)}
.jl-chat-fab svg{width:22px;height:22px;stroke:#F5F2ED;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.jl-chat-fab .dot{position:absolute;top:10px;right:10px;width:9px;height:9px;border-radius:50%;background:#4ade80;border:2px solid var(--acc)}
.jl-chat{position:fixed;right:22px;bottom:88px;z-index:300;width:min(380px,calc(100vw - 32px));max-height:min(620px,calc(100vh - 120px));
display:flex;flex-direction:column;background:var(--glass);-webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);
border:1px solid var(--edge);border-radius:20px;box-shadow:0 30px 70px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.08);
transform:translateY(12px) scale(.98);opacity:0;pointer-events:none;transition:opacity .22s,transform .22s;overflow:hidden}
.jl-chat.open{opacity:1;transform:none;pointer-events:auto}
.jl-chat::before{content:'';position:absolute;inset:0;pointer-events:none;background:radial-gradient(60% 50% at 0% 0%,rgba(139,13,26,.2),transparent 60%)}
.jl-chat>*{position:relative}
.jl-chat-head{display:flex;align-items:center;gap:.75rem;padding:.95rem 1.1rem;border-bottom:1px solid var(--edge)}
.jl-chat-head img{width:36px;height:36px;border-radius:50%;object-fit:cover;border:1px solid var(--edge)}
.jl-chat-head b{display:block;font-weight:500;font-size:14px;color:var(--ink)}
.jl-chat-head small{display:block;font-size:11px;color:var(--dim)}
.jl-chat-x{margin-left:auto;background:transparent;border:0;color:var(--dim);cursor:pointer;width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center}
.jl-chat-x:hover{background:var(--glass-2);color:var(--ink)}
.jl-chat-x svg{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:2}
.jl-chat-log{flex:1;overflow-y:auto;padding:1rem 1.1rem;display:flex;flex-direction:column;gap:.6rem;min-height:200px;
scrollbar-width:thin;scrollbar-color:rgba(245,242,237,.28) transparent}
.jl-chat-log::-webkit-scrollbar{width:6px}
.jl-chat-log::-webkit-scrollbar-track{background:transparent}
.jl-chat-log::-webkit-scrollbar-thumb{background:rgba(245,242,237,.22);border-radius:99px}
[data-theme="light"] .jl-chat-log{scrollbar-color:rgba(18,16,15,.28) transparent}
[data-theme="light"] .jl-chat-log::-webkit-scrollbar-thumb{background:rgba(18,16,15,.22)}
/* chat bubbles wrap long words on BOTH sides, not just the bot's */
.jl-msg{max-width:86%;padding:.6rem .85rem;border-radius:14px;font-size:13.5px;line-height:1.55;color:var(--ink);white-space:pre-wrap;overflow-wrap:anywhere}
.jl-msg.bot{align-self:flex-start;background:var(--glass-2);border:1px solid var(--edge);border-bottom-left-radius:5px}
.jl-msg.me{align-self:flex-end;background:var(--acc);color:#F5F2ED;border-bottom-right-radius:5px}
.jl-msg a{color:inherit;text-decoration:underline;text-underline-offset:3px}
.jl-chips{display:flex;flex-wrap:wrap;gap:.4rem;padding:0 1.1rem .75rem}
.jl-chips[hidden]{display:none!important}
.jl-chip{background:transparent;border:1px solid var(--edge);color:var(--dim);border-radius:999px;padding:.4rem .8rem;font:inherit;font-size:12px;cursor:pointer;transition:all .15s}
.jl-chip:hover{border-color:var(--acc);color:var(--ink)}
.jl-chat-form{display:flex;gap:.5rem;padding:.75rem 1.1rem 1rem;border-top:1px solid var(--edge)}
.jl-chat-form input{flex:1;background:rgba(18,16,15,.65);border:1px solid var(--edge);color:var(--ink);border-radius:999px;padding:.6rem 1rem;font:inherit;font-size:13.5px}
[data-theme="light"] .jl-chat-form input{background:rgba(255,255,255,.75)}
.jl-chat-form input:focus{outline:none;border-color:var(--acc)}
.jl-chat-form button{width:40px;height:40px;border-radius:50%;border:0;background:var(--acc);cursor:pointer;display:flex;align-items:center;justify-content:center;flex:none}
.jl-chat-form button svg{width:16px;height:16px;stroke:#F5F2ED;fill:none;stroke-width:1.8}
.jl-typing{display:inline-flex;gap:4px;align-items:center}
.jl-typing i{width:6px;height:6px;border-radius:50%;background:var(--dim);animation:jlb 1s infinite}
.jl-typing i:nth-child(2){animation-delay:.15s}.jl-typing i:nth-child(3){animation-delay:.3s}
@keyframes jlb{0%,80%,100%{opacity:.3;transform:translateY(0)}40%{opacity:1;transform:translateY(-3px)}}
@media(max-width:640px){.jl-chat{right:12px;bottom:82px}.jl-chat-fab{right:14px;bottom:14px}}

/* ---- inline flagged-word highlighting ---------------------------------- */
.hl-wrap{position:relative;background:var(--glass);border-radius:14px;
-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%)}
[data-theme="light"] .hl-wrap{background:rgba(255,255,255,.75)}
.hl-wrap .tool-textarea,.hl-backdrop{font-family:'Jost',system-ui,sans-serif;font-size:14px;line-height:1.55;
letter-spacing:0;word-spacing:0;font-kerning:none;font-variant-ligatures:none;tab-size:4;
padding:.85rem calc(1rem + 10px) .85rem 1rem;border:1px solid transparent;border-radius:14px;box-sizing:border-box;
white-space:pre-wrap;overflow-wrap:break-word;word-break:normal;hyphens:none;text-align:left}
.hl-wrap .tool-textarea{position:relative;z-index:1;background:transparent;border-color:var(--edge);
resize:vertical;overflow-y:auto;scrollbar-width:thin;scrollbar-gutter:stable;margin:0;display:block;width:100%}
.hl-wrap .tool-textarea::-webkit-scrollbar{width:10px}
.hl-wrap .tool-textarea:focus{border-color:var(--acc)}
[data-theme="light"] .hl-wrap .tool-textarea{background:transparent}
.hl-backdrop{position:absolute;inset:0;z-index:0;overflow:hidden;pointer-events:none;color:transparent;margin:0}
.hl-backdrop mark{background:rgba(220,38,38,.32);color:transparent;border-radius:3px;padding:0;margin:0;
box-shadow:0 0 0 1px rgba(220,38,38,.6);-webkit-box-decoration-break:clone;box-decoration-break:clone}
.hl-backdrop mark.warn{background:rgba(234,179,8,.28);box-shadow:0 0 0 1px rgba(234,179,8,.6)}

/* ---- "how this works" explainer ---------------------------------------- */
.howto{background:var(--glass);-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%);border:1px solid var(--edge);border-left:3px solid var(--acc);
border-radius:12px;padding:1rem 1.15rem;margin-bottom:1.5rem;font-size:13px;color:var(--dim);line-height:1.6}
.howto b{color:var(--ink);font-weight:500}
.howto ol{margin:.5rem 0 0;padding-left:1.15rem}
.howto li{margin-bottom:.2rem}
.cat-note{font-size:12px;color:var(--acc-text);margin-top:.45rem;line-height:1.45}
.plat-row{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.5rem}
.plat-btn{cursor:pointer;background:var(--glass);border:1px solid var(--edge);border-radius:999px;
padding:.55rem 1.15rem;color:var(--dim);font:400 12px/1 'Jost',system-ui,sans-serif;letter-spacing:.08em;
display:inline-flex;align-items:center;gap:.45rem;transition:all .2s}
.plat-btn:hover{color:var(--ink);border-color:var(--acc)}
.plat-btn.on{background:var(--acc);border-color:var(--acc);color:#F5F2ED}
.action-bar{display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin-top:1.25rem}
.btn.btn-sm{padding:.75rem 1.35rem;font-size:11px;min-height:42px;width:auto;margin-top:0}
.btn.btn-text{background:transparent;box-shadow:none;border:0;color:var(--dim);font-size:11px;
text-transform:uppercase;letter-spacing:.14em;cursor:pointer;padding:.5rem .75rem;min-height:auto;width:auto;margin-top:0}
.btn.btn-text:hover{color:var(--ink)}
.score-card{display:flex;align-items:center;gap:1.5rem;padding:1.35rem;background:var(--glass);-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%);
border:1px solid var(--edge);border-radius:18px;margin-bottom:1.5rem}
.score-dial{flex:0 0 76px;width:76px;height:76px;border-radius:50%;display:flex;flex-direction:column;
align-items:center;justify-content:center;border:3px solid var(--acc);background:var(--glass);
font-family:'Jost',system-ui,sans-serif;font-size:1.55rem;line-height:1;font-weight:500;font-variant-numeric:lining-nums tabular-nums}
.score-dial small{font-size:9.5px;font-family:'Jost',sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.1em;color:var(--dim)}
.score-info h4{font-size:1.2rem;margin-bottom:.25rem}
.score-info p{font-size:.875rem;color:var(--dim)}
.findings-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:.85rem}
.flag-list{display:grid;gap:.85rem;max-height:420px;overflow-y:auto;padding:2px .5rem 2px 2px;scrollbar-width:thin}
.flag-list::-webkit-scrollbar{width:8px}.flag-list::-webkit-scrollbar-thumb{background:var(--edge);border-radius:999px}
.flag-item{position:relative;overflow:hidden;padding:1.05rem 1.2rem 1.1rem;border-radius:14px;border:1px solid var(--edge);
background:var(--glass);-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%);
box-shadow:inset 0 1px 0 rgba(255,255,255,.06);font-size:13px;display:flex;flex-direction:column;gap:.5rem;
transition:border-color .2s,transform .2s}
.flag-item::before{content:'';position:absolute;inset:0;pointer-events:none;
background:radial-gradient(70% 90% at 0% 0%,var(--flag-tint,transparent),transparent 65%)}
.flag-item>*{position:relative}
.flag-item:hover{transform:translateY(-1px)}
.flag-item.critical{--flag-tint:rgba(220,38,38,.18);border-color:rgba(220,38,38,.4)}
.flag-item.warning{--flag-tint:rgba(234,179,8,.16);border-color:rgba(234,179,8,.4)}
.flag-item.safe{--flag-tint:rgba(34,197,94,.16);border-color:rgba(34,197,94,.4)}
.flag-head{display:flex;justify-content:space-between;align-items:flex-start;gap:.75rem;font-weight:500;font-size:14px;line-height:1.35;color:var(--ink)}
.flag-head>span:first-child{flex:1;min-width:0;overflow-wrap:anywhere}
.flag-tag{flex:none;font-size:9.5px;text-transform:uppercase;letter-spacing:.14em;padding:4px 9px;border-radius:999px;line-height:1;margin-top:2px}
.critical .flag-tag{background:#dc2626;color:#fff}
.warning .flag-tag{background:#eab308;color:#000}
.safe .flag-tag{background:#22c55e;color:#fff}
.flag-msg{color:var(--dim);font-size:12.5px;line-height:1.6}
.flag-fix{display:inline;align-self:flex-start;text-align:left;color:var(--acc-text);font-size:12px;line-height:1.55;
cursor:pointer;border:0;background:transparent;padding:0;margin-top:.15rem;text-decoration:underline;text-underline-offset:3px;font-family:inherit}
.flag-fix:hover{color:var(--ink)}
.pro-card{background:linear-gradient(135deg,rgba(139,13,26,.22),rgba(11,11,11,.65));
border:1px solid rgba(139,13,26,.45);border-radius:var(--rad);padding:1.75rem;margin-top:1.5rem;position:relative;overflow:hidden}
.pro-badge{display:inline-block;padding:3px 9px;border-radius:999px;background:var(--acc);color:#fff;
font-size:9.5px;text-transform:uppercase;letter-spacing:.16em;margin-bottom:.65rem}
.pro-card h3{font-size:1.35rem;margin-bottom:.45rem}
.pro-card p{font-size:.875rem;color:var(--dim);line-height:1.5}
.pro-card ul{list-style:none;padding:0;margin:1rem 0 1.25rem}
.pro-card li{font-size:13px;color:var(--dim);margin-bottom:.45rem;display:flex;align-items:center;gap:.5rem}
.pro-card li::before{content:'✓';color:var(--acc-text);font-weight:bold}
.pro-price{font-size:1.6rem;font-family:'Cormorant Garamond',Georgia,serif;color:var(--ink);margin-bottom:.85rem}
.pro-price span{font-size:.85rem;font-family:'Jost',sans-serif;color:var(--dim)}
@media(min-width:840px){.tool-grid{grid-template-columns:7fr 5fr;align-items:start}}

/* ---- suite navigation & calculators ----------------------------------- */
.suite-nav{display:flex;gap:.6rem;flex-wrap:wrap;margin:2rem 0 1.75rem;border-bottom:1px solid var(--edge);padding-bottom:1.25rem}
.suite-tab{cursor:pointer;background:var(--glass);border:1px solid var(--edge);border-radius:12px;
padding:.8rem 1.35rem;color:var(--dim);font:500 13px/1 'Jost',system-ui,sans-serif;letter-spacing:.04em;
display:inline-flex;align-items:center;gap:.55rem;transition:all .2s}
.suite-tab:hover{color:var(--ink);border-color:var(--acc)}
.suite-tab.on{background:var(--glass-2);border-color:var(--acc);color:var(--ink);box-shadow:0 0 20px rgba(139,13,26,.35)}
.suite-panel{display:none;scroll-margin-top:110px}
.suite-panel.on{display:block}

.metrics-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.85rem;margin-bottom:1.5rem}
.metrics-grid.cols-7{grid-template-columns:repeat(7,1fr)}
@media(max-width:1000px){.metrics-grid.cols-7{grid-template-columns:repeat(4,1fr)}}
@media(max-width:640px){.metrics-grid,.metrics-grid.cols-7{grid-template-columns:repeat(2,1fr)}}
.metric-box{background:var(--glass);-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%);border:1px solid var(--edge);border-radius:16px;padding:1rem .75rem;text-align:center;box-shadow:inset 0 1px 0 rgba(255,255,255,.06)}
.metric-box .m-val{font-family:'Jost',system-ui,sans-serif;font-size:1.6rem;font-weight:500;line-height:1.1;letter-spacing:-.01em;font-variant-numeric:lining-nums tabular-nums;font-feature-settings:'lnum' 1,'tnum' 1}
.metric-box .m-lbl{font-size:9.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.1em;margin-top:.45rem;line-height:1.3}
.metric-box .m-sub{font-size:11px;margin-top:.4rem;color:var(--dim);display:block;line-height:1.3}

.dfy-card,.work-card{position:relative;overflow:hidden;background:var(--glass);
-webkit-backdrop-filter:blur(22px) saturate(160%);backdrop-filter:blur(22px) saturate(160%);
border:1px solid var(--edge);border-radius:var(--rad);padding:2.25rem 2.25rem;margin-top:2.75rem;
box-shadow:0 24px 60px var(--shade),inset 0 1px 0 rgba(255,255,255,.08);display:flex;flex-direction:column;gap:1.5rem}
.dfy-card::before,.work-card::before{content:'';position:absolute;inset:0;pointer-events:none;
background:radial-gradient(60% 80% at 0% 0%,rgba(139,13,26,.22),transparent 60%),linear-gradient(135deg,rgba(255,255,255,.06),transparent 45%)}
.dfy-card>*,.work-card>*{position:relative}
@media(min-width:840px){.dfy-card{flex-direction:row;align-items:center;justify-content:space-between}}
.dfy-info h3,.work-card h3{font-size:1.75rem;font-weight:400;line-height:1.25;letter-spacing:-.01em;margin:.6rem 0 .75rem;max-width:34rem}
.dfy-info p,.work-card p{font-size:.95rem;color:var(--dim);max-width:38rem;line-height:1.7}
.dfy-btns,.work-btns{display:flex;gap:.75rem;flex-wrap:wrap}
.work-btns .btn{display:inline-flex;align-items:center;gap:.5rem}

/* ---- services grid (about page) --------------------------------------- */
.services-grid{display:grid;gap:1.5rem;margin-top:1.75rem}
@media(min-width:840px){.services-grid{grid-template-columns:repeat(3,1fr)}}
.service-card{position:relative;overflow:hidden;display:flex;flex-direction:column;
background:var(--glass);-webkit-backdrop-filter:blur(22px) saturate(160%);backdrop-filter:blur(22px) saturate(160%);
border:1px solid var(--edge);border-radius:var(--rad);padding:2rem 1.85rem 1.85rem;
box-shadow:0 18px 48px var(--shade),inset 0 1px 0 rgba(255,255,255,.08);
transition:transform .3s ease,border-color .3s ease,box-shadow .3s ease}
.service-card::before{content:'';position:absolute;inset:0;pointer-events:none;
background:linear-gradient(135deg,rgba(255,255,255,.07),transparent 40%),radial-gradient(70% 60% at 100% 100%,rgba(139,13,26,.16),transparent 65%)}
.service-card>*{position:relative}
.service-card:hover{transform:translateY(-4px);border-color:rgba(139,13,26,.55);box-shadow:0 28px 64px var(--shade),0 0 0 1px rgba(139,13,26,.25),inset 0 1px 0 rgba(255,255,255,.1)}
.service-card .pro-badge{align-self:flex-start}
.service-card h3{font-size:1.55rem;font-weight:400;line-height:1.2;letter-spacing:-.01em;margin:1rem 0 .65rem}
.service-card p{font-size:.9375rem;color:var(--dim);line-height:1.7;margin:0 0 .25rem}
.service-card ul{list-style:none;padding:0;margin:1.35rem 0 1.5rem;font-size:13.5px;color:var(--dim);line-height:1.55}
.service-card li{padding:.6rem 0;border-top:1px solid var(--edge);display:flex;align-items:flex-start;gap:.65rem}
.service-card li::before{content:'✓';color:var(--acc-text);font-weight:bold;flex:none;margin-top:.05em}
.service-card .btn{margin-top:auto}
.service-price{font-size:1.45rem;font-family:'Cormorant Garamond',Georgia,serif;margin-top:auto;padding-top:1rem;color:var(--ink)}
.service-price span{font-size:.8rem;font-family:'Jost',sans-serif;color:var(--dim);display:block}

/* ---- modal & toast (used by tools/index.html) -------------------------- */
.modal{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
background:rgba(11,11,11,.84);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);
opacity:0;pointer-events:none;transition:opacity .25s ease;padding:1.25rem}
.modal.open{opacity:1;pointer-events:auto}
.modal-card{position:relative;width:100%;max-width:24rem;background:var(--bg);
border:1px solid var(--edge);border-radius:24px;padding:2rem 1.75rem 1.75rem;text-align:left;
box-shadow:0 24px 60px var(--shade),inset 0 1px 0 var(--edge-top);
transform:scale(.95);transition:transform .25s cubic-bezier(.4,0,.2,1);max-height:90vh;overflow-y:auto}
.modal.open .modal-card{transform:scale(1)}
.modal-close{position:absolute;top:.85rem;right:.85rem;width:36px;height:36px;border-radius:50%;
background:var(--glass);border:1px solid var(--edge);color:var(--ink);font-size:20px;line-height:1;
display:flex;align-items:center;justify-content:center;cursor:pointer;transition:border-color .2s}
.modal-close:hover{border-color:var(--acc)}
.toast{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(20px);
background:var(--ink);color:var(--bg);padding:.75rem 1.25rem;border-radius:999px;
font-size:12px;font-weight:500;letter-spacing:.04em;opacity:0;pointer-events:none;
transition:opacity .25s,transform .25s;z-index:300;box-shadow:0 12px 32px var(--shade)}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* ---- Marketplace Audit Scorecard (Module 4) --------------------------- */
.audit-toolbar{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-bottom:1.5rem;background:var(--glass);-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%);padding:.9rem 1.1rem;border-radius:14px;border:1px solid var(--edge)}
.audit-toolbar>div{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}
.audit-toolbar>div:last-child{margin-left:auto}
@media(max-width:900px){.audit-toolbar>div{flex:1 1 100%}.audit-toolbar>div:last-child{margin-left:0}}
.audit-toolbar .btn,.rpt-actions .btn,.tb-btn{height:40px;min-height:40px;padding:0 1.1rem;font-size:11px;letter-spacing:.12em;width:auto;margin:0;display:inline-flex;align-items:center;gap:.45rem;white-space:nowrap}
.audit-toolbar .tool-select{height:40px;padding:0 .8rem;font-size:13px}
.audit-toolbar .file-btn{position:relative;overflow:hidden;display:inline-flex;align-items:center;cursor:pointer}
.audit-toolbar input[type="file"]{position:absolute;left:0;top:0;opacity:0;width:100%;height:100%;cursor:pointer}
.score-pill{display:inline-flex;align-items:center;justify-content:center;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;letter-spacing:.03em}
.score-pill.good{background:rgba(34,197,94,.18);color:#4ade80;border:1px solid rgba(34,197,94,.35)}
.score-pill.warn{background:rgba(234,179,8,.18);color:#facc15;border:1px solid rgba(234,179,8,.35)}
.score-pill.crit{background:rgba(239,68,68,.18);color:#f87171;border:1px solid rgba(239,68,68,.35)}

.audit-table-wrap{overflow-x:auto;border:1px solid var(--edge);border-radius:14px;background:var(--glass-2);margin-top:1rem}
.audit-table{width:100%;border-collapse:collapse;font-size:13px;text-align:left}
.audit-table th{background:rgba(11,11,11,.75);padding:.85rem 1rem;font-weight:500;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--dim);border-bottom:1px solid var(--edge);cursor:pointer;user-select:none;white-space:nowrap}
.audit-table th:hover{color:var(--ink)}
.audit-table td{padding:.85rem 1rem;border-bottom:1px solid var(--edge);color:var(--dim);vertical-align:middle;font-variant-numeric:lining-nums tabular-nums}
.audit-table tr:last-child td{border-bottom:none}
.audit-table tr:hover td{background:rgba(255,255,255,.02);color:var(--ink)}
.audit-table .sku-cell{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;color:var(--ink);white-space:nowrap}
.audit-table .title-cell{max-width:280px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

.rpt-form{background:var(--glass);-webkit-backdrop-filter:blur(18px) saturate(150%);backdrop-filter:blur(18px) saturate(150%);border:1px solid var(--edge);border-radius:14px;padding:1.25rem 1.35rem;margin-bottom:1.5rem}
.rpt-form label{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin-bottom:.35rem}
.rpt-meta{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1.25rem}
.rpt-meta .tool-select{height:44px;padding:0 .85rem}
@media(max-width:800px){.rpt-meta{grid-template-columns:repeat(2,1fr)}}
.rpt-rows{display:grid;grid-template-columns:minmax(170px,.8fr) 1fr 1fr;column-gap:.75rem;row-gap:.5rem;align-items:center;max-width:720px}
.rpt-row{display:contents}
.rpt-row label{margin:0;text-transform:none;letter-spacing:0;font-size:13px;color:var(--dim)}
.rpt-row label small{display:block;font-size:11px;opacity:.7}
.rpt-row input{width:100%;height:40px;background:rgba(18,16,15,.65);border:1px solid var(--edge);color:var(--ink);border-radius:9px;padding:0 .7rem;font:inherit;font-size:13px}
[data-theme="light"] .rpt-row input{background:rgba(255,255,255,.75)}
.rpt-row-head{display:contents}
.rpt-row-head span{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);padding-bottom:.15rem}
.rpt-actions{display:flex;justify-content:space-between;align-items:center;gap:.75rem;flex-wrap:wrap;margin-top:1.25rem}
.rpt-actions>div{display:flex;gap:.6rem;flex-wrap:wrap}
@media(max-width:640px){.rpt-rows{grid-template-columns:1fr 1fr;max-width:none}.rpt-row label{grid-column:1/-1;margin-top:.35rem}.rpt-row-head span:first-child{display:none}}
.rpt-preview{margin-top:.5rem}
.rpt-doc{background:#fff;color:#111;border-radius:14px;padding:32px;font-family:Georgia,'Times New Roman',serif;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.rpt-head{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;border-bottom:2px solid #8B0D1A;padding-bottom:16px;margin-bottom:20px}
.rpt-eyebrow{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8B0D1A}
.rpt-title{margin:.2em 0;font-size:24px;font-weight:500;color:#111}
.rpt-sub{color:#666;font-size:13px}
.rpt-kpi{text-align:right}.rpt-kpi-val{font-size:28px;font-weight:600}.rpt-kpi-lbl{font-size:12px;color:#666}
.rpt-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-bottom:20px}
.rpt-cell{border:1px solid #e5e5e5;border-radius:10px;padding:10px;text-align:center}.rpt-cell-val{font-size:18px;font-weight:600}.rpt-cell-lbl{font-size:11px;color:#666}
.rpt-table{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:22px}
.rpt-table th,.rpt-table td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;color:#111}
.rpt-table th{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#666}
.rpt-two{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.rpt-two h3,.rpt-notes h3{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#8B0D1A;margin:0 0 8px}
.rpt-two ol{padding-left:18px;font-size:13.5px;line-height:1.55;margin:0}
.rpt-notes{margin-top:18px;font-size:13.5px}.rpt-notes p{margin:0}
.rpt-trend{margin-top:18px}.rpt-spark{display:block}
.rpt-foot{margin-top:24px;font-size:11px;color:#999;border-top:1px solid #eee;padding-top:10px}
.rpt-good{color:#15803d}.rpt-bad{color:#b91c1c}.rpt-flat{color:#888}
@media(max-width:640px){.rpt-two{grid-template-columns:1fr}.rpt-head{flex-direction:column}.rpt-kpi{text-align:left}}
.cls-settings{margin-bottom:1.25rem;background:var(--glass);border:1px solid var(--edge);border-radius:14px;padding:.9rem 1.25rem}
.cls-settings summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
.cls-settings summary::-webkit-details-marker{display:none}
.cls-settings summary::after{content:'▾';font-size:14px;transition:transform .2s}
.cls-settings[open] summary::after{transform:rotate(180deg)}
.cls-settings summary:hover{color:var(--ink)}
.cls-settings-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.6rem 1.25rem;margin-top:.8rem;font-size:12.5px;color:var(--dim)}
.cls-settings-grid input{width:64px;background:rgba(18,16,15,.65);border:1px solid var(--edge);color:var(--ink);border-radius:8px;padding:.25rem .45rem;font:inherit;font-size:12.5px;margin:0 .25rem}
[data-theme="light"] .cls-settings-grid input{background:rgba(255,255,255,.75)}
.cls-filters{display:flex;flex-wrap:wrap;gap:.75rem;align-items:center;justify-content:space-between}
.cls-filters>div:last-child{display:flex;gap:.5rem;flex-wrap:wrap}
.cls-filters .tool-select{height:40px;padding:0 .8rem}
.cls-tabs{display:flex;flex-wrap:wrap;gap:.4rem}
.cls-tab{background:var(--glass-2);border:1px solid var(--edge);color:var(--dim);border-radius:999px;padding:.35rem .8rem;font:inherit;font-size:12px;cursor:pointer}
.cls-tab.on{background:var(--acc);border-color:var(--acc);color:#F5F2ED}
.act-pill{display:inline-flex;align-items:center;gap:.3rem;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;white-space:nowrap;border:1px solid transparent}
.act-pill.high{background:rgba(239,68,68,.18);color:#f87171;border-color:rgba(239,68,68,.35)}
.act-pill.medium{background:rgba(234,179,8,.18);color:#facc15;border-color:rgba(234,179,8,.35)}
.act-pill.low{background:rgba(148,163,184,.18);color:#cbd5e1;border-color:rgba(148,163,184,.35)}
.act-pill.growth{background:rgba(34,197,94,.18);color:#4ade80;border-color:rgba(34,197,94,.35)}
.cls-why{font-size:11.5px;color:var(--dim);max-width:260px}
.noimg-tag{display:inline-block;margin-left:.4rem;font-size:10.5px;padding:2px 7px;border-radius:999px;background:rgba(239,68,68,.15);color:#f87171}
.top-fixes-list{display:grid;gap:.75rem;margin-top:1rem}
.fix-item{display:flex;align-items:center;justify-content:space-between;gap:1rem;background:var(--glass);border:1px solid var(--edge);border-radius:12px;padding:.85rem 1.15rem;transition:border-color .2s}
.fix-item:hover{border-color:var(--acc)}
.fix-rank{font-family:'Jost',system-ui,sans-serif;font-size:1.1rem;font-weight:500;font-variant-numeric:lining-nums tabular-nums;color:var(--dim);min-width:28px}
.fix-content{flex:1}
.fix-title{font-size:13px;font-weight:500;color:var(--ink);margin-bottom:.2rem}
.fix-desc{font-size:12px;color:var(--dim);line-height:1.4}
.fix-stat{font-size:11px;padding:3px 9px;border-radius:999px;background:var(--glass-2);border:1px solid var(--edge);white-space:nowrap}

/* Detail Drawer */
.drawer-backdrop{position:fixed;inset:0;background:rgba(11,11,11,.8);z-index:250;opacity:0;pointer-events:none;transition:opacity .25s ease;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.drawer-backdrop.open{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;width:100%;max-width:500px;height:100%;background:var(--bg);border-left:1px solid var(--edge);z-index:260;transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;box-shadow:-20px 0 50px var(--shade);overflow:hidden}
.drawer.open{transform:translateX(0)}
.drawer-head{padding:1.5rem;border-bottom:1px solid var(--edge);display:flex;align-items:flex-start;justify-content:space-between;gap:1rem}
.drawer-body{padding:1.5rem;overflow-y:auto;flex:1;display:flex;flex-direction:column;gap:1.25rem}
.drawer-check-item{background:var(--glass-2);border:1px solid var(--edge);border-radius:12px;padding:.85rem 1rem}
.drawer-check-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:.35rem}
.drawer-check-name{font-size:13px;font-weight:500}
.drawer-check-pts{font-size:11px;font-weight:600}
.drawer-check-detail{font-size:12px;color:var(--dim);line-height:1.4}
"""

ICONS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
'<g id="i-phone"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6'
'A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9'
'a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></g>'
'<g id="i-mail"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/>'
'<path d="m22 6-10 7L2 6"/></g>'
'<g id="i-in"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/>'
'<rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></g>'
'<g id="i-wa"><path d="M21 11.5a8.4 8.4 0 0 1-12.6 7.3L3 20.5l1.8-5.3A8.4 8.4 0 1 1 21 11.5z"/>'
'<path d="M8.6 9.1c.2-.5.4-.5.6-.5h.5c.2 0 .4 0 .6.5l.7 1.7c.1.2 0 .4-.1.5l-.4.5c-.1.1-.2.3-.1.5a5.4 5.4 0 0 0 2.6 2.3c.2.1.4 0 .5-.1l.5-.6c.1-.2.3-.2.5-.1l1.6.8c.2.1.4.2.4.4a1.9 1.9 0 0 1-1.3 1.6c-.6.2-1.4.1-3.2-.8a9 9 0 0 1-3.5-3.7c-.6-1.2-.5-2.1-.2-2.6z"/></g>'
'<g id="i-ig"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>'
'<circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/></g>'
'<g id="i-shield"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3z"/><path d="m9 12 2 2 4-4"/></g>'
'<g id="i-chart"><path d="M3 3v18h18"/><path d="M7 15l4-5 3 3 5-7"/></g>'
'<g id="i-tag"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.2"/></g>'
'<g id="i-search"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></g>'
'<g id="i-box"><path d="M21 8 12 3 3 8v8l9 5 9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/></g>'
'<g id="i-trend"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></g>'
'<g id="i-alert"><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></g>'
'<g id="i-clock"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></g>'
'<g id="i-flame"><path d="M12 22c4 0 7-3 7-7 0-3-2-5-3-6-.3 2-1.5 3-2.5 3.5C14 10 13 7 9.5 4c.5 3-1 5-2.5 7A6.6 6.6 0 0 0 5 15c0 4 3 7 7 7z"/></g>'
'<g id="i-gift"><path d="M20 12v9H4v-9M2 7h20v5H2zM12 7v14"/><path d="M12 7c-1.5-3-6-3-6-1s3 1 6 1zM12 7c1.5-3 6-3 6-1s-3 1-6 1z"/></g>'
'<g id="i-mega"><path d="M3 10v4a1 1 0 0 0 1 1h3l6 4V5L7 9H4a1 1 0 0 0-1 1z"/><path d="M17 8a5 5 0 0 1 0 8M7 15v4"/></g>'
'<g id="i-rocket"><path d="M5 19c-1 1-1 3-1 3s2 0 3-1M14 4c3-2 6-1 6-1s1 3-1 6l-7 7-5-5 7-7z"/><path d="M9 11l-4 1-1 3 4 0M13 15l-1 4 3-1 0-4"/><circle cx="14.5" cy="9.5" r="1.3"/></g>'
'<g id="i-inbox"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5 4h14l3 8v8H2v-8l3-8z"/></g>'
'<g id="i-camera"><path d="M4 8h3l2-3h6l2 3h3a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2z"/><circle cx="12" cy="14" r="3.5"/></g>'
'<g id="i-camera-off"><path d="M4 8h3l2-3h6l2 3h3a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2z"/><circle cx="12" cy="14" r="3.5"/><path d="M3 3l18 18"/></g>'
'<g id="i-check"><path d="m5 12 5 5L20 7"/></g>'
'<g id="i-x"><path d="M6 6l12 12M18 6 6 18"/></g>'
'<g id="i-warn"><path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01"/></g>'
'<g id="i-star"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9L12 3z"/></g>'
'<g id="i-list"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></g>'
'<g id="i-chat"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-4.6A8 8 0 1 1 21 12z"/></g>'
'<g id="i-send"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z"/></g>'
'<g id="i-tt"><path d="M16 3c.4 2.2 1.9 3.8 4 4.1v3a7 7 0 0 1-4-1.3v5.9a5.7 5.7 0 1 1-5-5.7v3.1a2.7 2.7 0 1 0 2 2.6V3h3z"/></g>'
'<g id="i-dl"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/>'
'<path d="M12 15V3"/></g></defs></svg>')

VCARD_JS = """
function downloadVCard(){
 var v=["BEGIN:VCARD","VERSION:3.0","N:%(last)s;%(first)s;;;","FN:%(name)s","TITLE:%(title)s",
 "TEL;TYPE=CELL:%(tel)s","EMAIL;TYPE=INTERNET:%(email)s","URL:%(li)s"%(social)s,"END:VCARD"].join("\\r\\n");
 var b=new Blob(["\\ufeff"+v],{type:"text/vcard;charset=utf-8"});
 var u=URL.createObjectURL(b),a=document.createElement("a");
 a.href=u;a.download="%(file)s.vcf";document.body.appendChild(a);a.click();
 document.body.removeChild(a);setTimeout(function(){URL.revokeObjectURL(u);},1000);}
"""

REVEAL_JS = """
(function(){var e=[].slice.call(document.querySelectorAll('.rv'));
if(!('IntersectionObserver' in window)){e.forEach(function(x){x.classList.add('on')});return}
var o=new IntersectionObserver(function(en){en.forEach(function(x){
if(x.isIntersecting){x.target.classList.add('on');o.unobserve(x.target)}})},
{rootMargin:'0px 0px -80px 0px'});e.forEach(function(x){o.observe(x)})})();
"""


def socials():
    """Returns [(icon_id, label, url)] for whatever is filled in."""
    p = PROFILE
    out = []
    if p.get("whatsapp"):
        out.append(("i-wa", "WhatsApp", f"https://wa.me/{p['whatsapp']}"))
    if p.get("instagram"):
        out.append(("i-ig", f"@{p['instagram']}", f"https://instagram.com/{p['instagram']}"))
    if p.get("tiktok"):
        out.append(("i-tt", f"@{p['tiktok']}", f"https://tiktok.com/@{p['tiktok']}"))
    return out


def contact_nav(prefix=""):
    p = PROFILE
    return f'''<nav class="contact" aria-label="Contact">
<a href="tel:{E(p['tel'])}"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-phone"/></svg><span>{E(p['phone'])}</span></a>
<a href="mailto:{E(p['email'])}"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-mail"/></svg><span>{E(p['email'])}</span></a>
<a href="{E(p['linkedin'])}" rel="noopener"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-in"/></svg><span>{E(p['linkedin_label'])}</span></a>
</nav>
<div class="socialrow">{"".join(f'<a href="{E(u)}" rel="noopener" aria-label="{E(l)}" title="{E(l)}"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#{i}"/></svg></a>' for i, l, u in socials())}</div>'''


def nav(active, up=""):
    items = [("Home", f"{up}index.html", "home"),
             ("Work", f"{up}work/index.html", "work"),
             ("Tools", f"{up}tools/index.html", "tools"),
             ("About", f"{up}about.html", "about"),
             ("Card", f"{up}card.html", "card"),
             ("Contact", f"{up}index.html#contact", "contact")]
    out = []
    for label, href, key in items:
        cls = ' class="on"' if key == active else ""
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    tgl = ('<button class="tgl" type="button" id="t" aria-label="Switch between dark and light">'
           '<svg class="tgl-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/>'
           '<path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'
           '<svg class="tgl-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
           '</button>')
    return f'<nav class="pill" aria-label="Sections"><div class="pill-in">{"".join(out)}{tgl}</div></nav>'


THEME_JS = """
(function(){var r=document.documentElement,t=document.getElementById('t'),K='jl-theme';
try{var v=localStorage.getItem(K);if(v)r.setAttribute('data-theme',v);}catch(e){}
function syncLabel(){if(t){var isLight=r.getAttribute('data-theme')==='light';t.setAttribute('aria-label',isLight?'Switch to dark theme':'Switch to light theme')}}
syncLabel();
if(t)t.addEventListener('click',function(){
var n=r.getAttribute('data-theme')==='light'?'dark':'light';
r.setAttribute('data-theme',n);
var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute('content',n==='light'?'#EFEBE4':'#0B0B0B');
syncLabel();
try{localStorage.setItem(K,n);}catch(e){}});})();
"""


def lead_form(where="footer", extra=""):
    """Web3Forms lead form. `where` distinguishes the footer form from the chat one."""
    p = PROFILE
    key = p.get("web3forms_key", "")
    return f'''<form class="lead-form" id="lead-{where}" data-key="{E(key)}" data-where="{where}" novalidate>
<input type="hidden" name="subject" value="New inquiry from jamielyn-ludovice.vercel.app">
<input type="hidden" name="from_name" value="Portfolio site">
<input type="checkbox" name="botcheck" class="lead-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="lead-row"><input type="text" name="name" placeholder="Your name" required autocomplete="name">
<input type="email" name="email" placeholder="Email" required autocomplete="email"></div>
<input type="text" name="store" placeholder="Store / project link (optional)" autocomplete="url">
<textarea name="message" rows="3" placeholder="What do you need help with?" required></textarea>
<div class="lead-foot"><button class="btn" type="submit"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-send"/></svg>Send message</button>{extra}
<span class="lead-msg" aria-live="polite"></span></div>
</form>'''


LEAD_JS = r"""
(function(){
  var forms=document.querySelectorAll('.lead-form'); if(!forms.length) return;
  var MAIL='%(mail)s';
  forms.forEach(function(f){
    var msg=f.querySelector('.lead-msg'), btn=f.querySelector('button[type=submit]');
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var name=f.name.value.trim(), email=f.email.value.trim(), store=(f.store?f.store.value.trim():''), text=f.message.value.trim();
      if(!name||!email||!text){msg.textContent='Please fill in your name, email and message.';msg.className='lead-msg bad';return;}
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){msg.textContent='That email does not look right.';msg.className='lead-msg bad';return;}
      var key=f.dataset.key;
      if(!key){
        var body='Name: '+name+'\nEmail: '+email+(store?'\nStore: '+store:'')+'\n\n'+text;
        window.location.href='mailto:'+MAIL+'?subject='+encodeURIComponent('Inquiry from your portfolio')+'&body='+encodeURIComponent(body);
        msg.textContent='Opening your email app…';msg.className='lead-msg ok';return;
      }
      btn.disabled=true; msg.textContent='Sending…'; msg.className='lead-msg';
      var data=new FormData(f); data.append('access_key',key); data.append('page',location.href);
      fetch('https://api.web3forms.com/submit',{method:'POST',body:data,headers:{'Accept':'application/json'}})
        .then(function(r){return r.json();})
        .then(function(j){
          if(j&&j.success){f.reset();msg.textContent='Sent. I will reply to '+email+' within the day.';msg.className='lead-msg ok';
            if(window.showToast)window.showToast('Message sent.');}
          else{throw new Error((j&&j.message)||'failed');}
        })
        .catch(function(){msg.textContent='Could not send. Message me on WhatsApp instead: https://wa.me/%(wa)s';msg.className='lead-msg bad';})
        .then(function(){btn.disabled=false;});
    });
  });
})();
"""

def chat_widget(up=""):
    p = PROFILE
    return f'''<button class="jl-chat-fab" id="jl-chat-fab" type="button" aria-label="Chat with Jamie's assistant" aria-expanded="false">
<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-chat"/></svg><span class="dot" aria-hidden="true"></span></button>
<div class="jl-chat" id="jl-chat" role="dialog" aria-label="Assistant" aria-hidden="true">
  <div class="jl-chat-head"><img src="{up}{E(p['avatar'])}" alt=""><div><b>Jamie's assistant</b><small>Usually replies on WhatsApp within the day</small></div>
    <button class="jl-chat-x" id="jl-chat-x" type="button" aria-label="Close"><svg viewBox="0 0 24 24"><use href="#i-x"/></svg></button></div>
  <div class="jl-chat-log" id="jl-chat-log" aria-live="polite"></div>
  <div class="jl-chips" id="jl-chips"></div>
  <div class="jl-lead" id="jl-lead" hidden>
    <button class="jl-lead-back" id="jl-lead-back" type="button">← Back to chat</button>
    {lead_form('chat')}
  </div>
  <form class="jl-chat-form" id="jl-chat-form" autocomplete="off"><input id="jl-chat-in" type="text" placeholder="Ask about services, tools, or how to start" maxlength="300"><button type="submit" aria-label="Send"><svg viewBox="0 0 24 24"><use href="#i-send"/></svg></button></form>
</div>'''


def chat_kb():
    """Knowledge base for the on-site assistant, generated from content.py at build
    time so the answers can never drift from the pages. No API, no key, no cost -
    retrieval over this list happens in the visitor's own browser."""
    import json
    docs = []

    for pr in PROJECTS:
        parts = [pr.get("summary", ""), pr.get("challenge", ""),
                 pr.get("approach", ""), pr.get("result", "")]
        body = " ".join(x for x in parts if x)
        answer = pr.get("summary", "") or body[:220]
        extra = pr.get("approach") or pr.get("result") or ""
        if extra and extra != answer:
            answer += "\n\n" + extra
        docs.append({
            "id": "p:" + pr["slug"],
            "kind": "project",
            "title": pr["title"],
            "terms": " ".join([pr["title"], DISCIPLINES.get(pr["discipline"], ""),
                               " ".join(pr.get("tags", [])), body, pr.get("year", "")]),
            "answer": answer,
            "link": "work/" + pr["slug"] + ".html",
            "live": pr.get("link", ""),
        })

    for grp in EXPERTISE:
        docs.append({
            "id": "e:" + grp["group"],
            "kind": "skill",
            "title": grp["group"],
            "terms": grp["group"] + " " + " ".join(grp["items"]),
            "answer": grp["group"] + " covers: " + "; ".join(grp["items"]) + ".",
            "link": "about.html", "live": "",
        })

    # BACKGROUND is the education block (a dict); CREDENTIALS is the roles list.
    docs.append({
        "id": "b:education",
        "kind": "background",
        "title": BACKGROUND.get("degree", "Education"),
        "terms": ("education degree school studied university course graduate "
                  + BACKGROUND.get("degree", "") + " " + BACKGROUND.get("school", "")
                  + " " + " ".join(BACKGROUND.get("points", []))),
        "answer": (BACKGROUND.get("degree", "") + ", " + BACKGROUND.get("school", "")
                   + ("\n\n" + " ".join(BACKGROUND.get("points", []))
                      if BACKGROUND.get("points") else "")),
        "link": "about.html", "live": "",
    })

    for job in CREDENTIALS:
        role, org, per = job.get("role", ""), job.get("org", ""), job.get("period", "")
        docs.append({
            "id": "c:" + role + org,
            "kind": "credential",
            "title": role + (" - " + org if org else ""),
            "terms": "experience role position held " + role + " " + org + " " + per,
            "answer": role + (" at " + org if org else "") + (" (" + per + ")" if per else "") + ".",
            "link": "about.html", "live": "",
        })

    for t in TESTIMONIALS:
        if not (t.get("quote") or "").strip():
            continue
        docs.append({
            "id": "t:" + t["name"],
            "kind": "quote",
            "title": "Testimonial from " + t["name"],
            "terms": t["name"] + " " + t.get("role", "") + " " + t["quote"] + " testimonial reference recommend people say said review feedback opinion praise",
            "answer": '"' + t["quote"] + '"\n\n- ' + t["name"] + ", " + t.get("role", ""),
            "link": "about.html", "live": "",
        })

    docs.append({
        "id": "x:philosophy", "kind": "about", "title": "How Jamie works",
        "terms": "philosophy approach principle how do you work process system boring repeat " + PHILOSOPHY,
        "answer": PHILOSOPHY, "link": "about.html", "live": "",
    })
    docs.append({
        "id": "x:who", "kind": "about", "title": "About Jamie",
        "terms": "who whos sino ka about jamie jamielyn background yourself introduce location based who are you tell me about yourself "
                 + PROFILE["name"] + " " + PROFILE["role"] + " " + PROFILE["location"] + " " + PROFILE["intro"],
        "answer": PROFILE["intro"] + "\n\nBased in " + PROFILE["location"] + ".",
        "link": "about.html", "live": "",
    })
    # The KB is injected inside a <script> tag, so a future project description
    # containing "</script>" would end the block early and break every page.
    return json.dumps(docs, ensure_ascii=False).replace("</", "<\\/")

CHAT_JS = r"""
(function(){
  var fab=document.getElementById('jl-chat-fab'),box=document.getElementById('jl-chat'),log=document.getElementById('jl-chat-log'),
      chips=document.getElementById('jl-chips'),form=document.getElementById('jl-chat-form'),inp=document.getElementById('jl-chat-in'),x=document.getElementById('jl-chat-x');
  if(!fab||!box) return;
  var WA='https://wa.me/%(wa)s', MAIL='%(mail)s', KEY='jl-chat-v1', hist=[];
  var TOOLS='%(up)stools/', ABOUT='%(up)sabout.html', WORK='%(up)swork/';
  var A={
    services:"I work on three things: marketplace & Shopify stores (listings, storefront pages, promo planning, monthly reporting), 3D and spatial design (trade-show booths, product renders), and creative operations (Notion systems, Telegram bots, AI agents and automations).\n\nWhich one is closest to what you need?",
    shopify:"For Shopify and marketplace stores I do product photography and listing images, storefront and product-page builds, conversion fixes, promo calendars and a monthly performance report. Margegold Jewelry (margejewelry.com) is a live Shopify store I shot and built listings for.\n\nSend your store link and I'll reply with what I'd change first.",
    automation:"I build the systems I use daily: a Telegram reporting bot, a desktop activity tracker, a watchdog, an ERP-to-dashboard pipeline, Notion via MCP, and I build with AI agents (Claude, Antigravity) every day. If you have a repetitive task — download this, upload that, paste a link, click a button — that's exactly what these automate.\n\nTell me the task and I'll say how I'd automate it.",
    tools:"The free tools on this site are the same checks I run for clients: a listing policy & SEO scanner, ad efficiency (TACOS) calculator, voucher margin simulator, catalogue audit scorecard, product performance classifier and a monthly report generator. All run in your browser, nothing is uploaded.\n\nOpen the tools page: "+TOOLS,
    rates:"No fixed plans or subscriptions. Send me your store or project and what's slowing you down — I reply with what I'd do, how long it takes and a quote. Projects are 50%% to start, 50%% on delivery; retainers are monthly.\n\nFastest way: message me on WhatsApp.",
    start:"Message me on WhatsApp with your store link (or the project) and I'll come back with a plan and a quote: "+WA+"\n\nOr email: "+MAIL,
    hello:"Hi! I'm Jamie's assistant. Ask about services, the free tools, or how to start a project.",
    fallback:"I did not catch that one. I can answer about any of the projects on this site, the services, the free tools, rates or how to start — or hand you straight to Jamie on WhatsApp."
  };
  // ---- knowledge base, generated from content.py at build time -------------
  var KB=%(kb)s;
  var STOP={the:1,a:1,an:1,and:1,or:1,of:1,to:1,in:1,on:1,for:1,with:1,is:1,are:1,was:1,
    do:1,does:1,did:1,you:1,your:1,yours:1,i:1,me:1,my:1,we:1,it:1,this:1,that:1,can:1,
    could:1,would:1,how:1,what:1,which:1,who:1,any:1,have:1,has:1,about:1,tell:1,show:1,
    ba:1,ang:1,ng:1,sa:1,mo:1,ko:1,ako:1,ikaw:1,yung:1,yun:1,ito:1,ay:1,po:1,na:1,pa:1,
    may:1,mga:1,ninyo:1,niyo:1,kayo:1,pwede:1,puwede:1,kung:1,at:1,si:1,ni:1};
  // Taglish and shorthand the visitor is likely to type -> words the KB actually uses
  var SYN={magkano:'rate price',presyo:'rate price',bayad:'rate price',singil:'rate price',
    gaano:'rate',trabaho:'work project',ginawa:'work project',gawa:'work project',
    proyekto:'project',larawan:'photo photography',kuha:'photo photography',
    litrato:'photo photography',video:'video short form reels tiktok',
    bidyo:'video',disenyo:'design',dinisenyo:'design',website:'web site front-end',
    sistema:'system automation',bot:'bot telegram automation',
    tulong:'help service',serbisyo:'service',karanasan:'experience background',
    saan:'location based',taga:'location based',
    ecom:'ecommerce marketplace',ecommerce:'ecommerce marketplace shopee lazada tiktok shopify',
    shopee:'shopee marketplace',lazada:'lazada marketplace',tiktok:'tiktok marketplace video',
    shopify:'shopify ecommerce store',ai:'ai agent automation',agents:'agent automation',
    n8n:'automation workflow',notion:'notion system',blender:'render 3d product',
    sketchup:'3d interior render',expo:'exhibit booth event',booth:'exhibit booth event',
    tarp:'tarpaulin banner print',pubmat:'social graphics pubmat',
    resume:'background experience',cv:'background experience',
    hire:'start hire work with',kausap:'talk contact',makausap:'talk contact',
    sino:'who jamie about',foreign:'overseas international client',
    abroad:'overseas international',render:'render 3d blender product',
    pag_aaral:'education degree school',edukasyon:'education degree school',
    natapos:'education degree school',eskwela:'education school',
    kliyente:'client brand',brands:'brand client',
    say:'say people testimonial',reviews:'testimonial review people say'};
  function stem(w){ if(w.length>4&&/(ies)$/.test(w)) return w.slice(0,-3)+'y';
    if(w.length>4&&/(ses|xes|ches|shes)$/.test(w)) return w.slice(0,-2);
    if(w.length>2&&/s$/.test(w)&&!/(ss|us|is)$/.test(w)) return w.slice(0,-1);
    if(w.length>5&&/ing$/.test(w)) return w.slice(0,-3);
    return w; }
  function norm(t){return String(t).toLowerCase().replace(/[^a-z0-9à-ÿ\s]/g,' ')
    .split(/\s+/).filter(Boolean).map(stem);}
  function expand(ws){var o=[],seen={};function push(w){if(w&&!seen[w]){seen[w]=1;o.push(w);}}
    ws.forEach(function(w){if(STOP[w])return;push(w);
      if(SYN[w])SYN[w].split(' ').forEach(function(x){push(stem(x));});});return o;}
  var IDX=KB.map(function(d){var m={};norm(d.terms).forEach(function(w){if(!STOP[w])m[w]=(m[w]||0)+1;});
    var tm={};norm(d.title).forEach(function(w){if(!STOP[w])tm[w]=1;});return {d:d,m:m,tm:tm};});
  // A word that appears in only one or two entries identifies that entry far more
  // strongly than a word every page uses. Weight by how rare it is.
  var DF={};IDX.forEach(function(e){for(var k in e.m)DF[k]=(DF[k]||0)+1;});
  var NDOC=IDX.length||1;
  function idf(w){var d=DF[w]||NDOC;return 1+Math.log(NDOC/d);}
  function score(q){
    var ws=expand(norm(q)); if(!ws.length) return null;
    var best=null,bs=0,second=0;
    IDX.forEach(function(e){
      var sc=0;
      ws.forEach(function(w){
        var iw=idf(w);
        if(e.tm[w]) sc+=3*iw;                    // a hit in the title counts most
        else if(e.m[w]) sc+=(1 + Math.min(e.m[w]-1,2)*0.25)*iw;
        else if(w.length>4){                     // tolerate typos and part-words
          for(var k in e.m){ if(k.length>4 && (k.indexOf(w)===0||w.indexOf(k)===0)){sc+=0.6*iw;break;} }
        }
      });
      if(sc>bs){second=bs;bs=sc;best=e.d;} else if(sc>second){second=sc;}
    });
    if(bs<3.2) return null;                      // too weak - fall back to intents
    return {doc:best,score:bs,clear:bs-second};
  }
  function kbAnswer(hit){
    var d=hit.doc,t=d.answer;
    if(d.kind==='project'){
      t=d.title+' — '+t;
      t+='\n\nFull write-up: '+'%(up)s'+d.link;
      if(d.live) t+='\nLive: '+d.live;
    }
    return t;
  }
  var CHIPS=[['What do you do?','services'],['Shopify & marketplaces','shopify'],['Automation & AI agents','automation'],['Free tools','tools'],['Rates & how to start','rates'],['Leave a message','lead'],['Talk to Jamie','wa']];
  var RULES=[[/email|message|form|leave|write|send you/i,'lead'],[/wa|whats|talk|human|jamie|call|contact|number/i,'wa'],[/rate|price|cost|quote|how much|fee|budget|pay/i,'rates'],[/start|hire|begin|work with|proposal|book/i,'start'],
    [/shopify|shopee|lazada|tiktok|amazon|etsy|ebay|listing|store|product page|a\+|marketplace|photo/i,'shopify'],[/automat|bot|agent|ai|mcp|n8n|telegram|workflow|script|python|hermes|llm/i,'automation'],
    [/tool|scanner|tacos|voucher|audit|report|calculator/i,'tools'],[/service|do you|offer|help with|what can/i,'services'],[/booth|3d|render|blender|sketchup|interior|expo|exhibit/i,'services'],[/hi|hello|hey|kumusta|good/i,'hello']];
  function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
  function linkify(t){return esc(t).replace(/(https?:\/\/[^\s]+|[a-z0-9./-]+\.html|tools\/)/g,function(m){var h=m;if(!/^https?:/.test(m))h=m;return '<a href="'+h+'" target="_blank" rel="noopener">'+m+'</a>';}).replace(/([\w.+-]+@[\w-]+\.[\w.]+)/g,'<a href="mailto:$1">$1</a>');}
  function add(who,text,save){var d=document.createElement('div');d.className='jl-msg '+who;d.innerHTML=who==='bot'?linkify(text):esc(text);log.appendChild(d);log.scrollTop=log.scrollHeight;if(save!==false){hist.push([who,text]);try{localStorage.setItem(KEY,JSON.stringify(hist.slice(-30)));}catch(e){}}}
  function typing(cb){var d=document.createElement('div');d.className='jl-msg bot';d.innerHTML='<span class="jl-typing"><i></i><i></i><i></i></span>';log.appendChild(d);log.scrollTop=log.scrollHeight;setTimeout(function(){d.remove();cb();},520);}
  var lead=document.getElementById('jl-lead');
  function usedTopics(){
    var labels={}; CHIPS.forEach(function(c){labels[c[0]]=c[1];});
    var used={};
    hist.forEach(function(h){ if(h[0]==='me'&&labels[h[1]]) used[labels[h[1]]]=1; });
    return used;
  }
  function setLead(on){
    if(lead) lead.hidden=!on;
    box.classList.toggle('lead-on',!!on);
  }
  function chipsFor(intent){
    var used=usedTopics();
    if(intent) used[intent]=1;
    var showingLead=intent==='lead';
    setLead(showingLead);
    chips.innerHTML='';
    if(showingLead){ chips.hidden=true; return; }
    CHIPS.forEach(function(c){
      if(used[c[1]] && c[1]!=='lead' && c[1]!=='wa') return;
      var b=document.createElement('button');b.type='button';b.className='jl-chip';
      b.textContent=c[0];b.dataset.k=c[1];
      b.addEventListener('click',function(){ask(c[0],c[1]);});
      chips.appendChild(b);
    });
    chips.hidden=!chips.children.length;
  }
  function waLink(){var last=hist.filter(function(h){return h[0]==='me';}).slice(-3).map(function(h){return h[1];}).join(' / ');var msg='Hi Jamie! I was on your site'+(last?' and asked about: '+last:'')+'. Can we talk about a project?';return WA+'?text='+encodeURIComponent(msg);}
  function reply(intent){if(intent==='lead'){add('bot','Leave your details and I will reply by email within the day.');setLead(true);var n=lead&&lead.querySelector('input[name=name]');if(n)n.focus();return;}if(intent==='wa'){add('bot',"Sure — this opens WhatsApp with a short note so Jamie has the context:\n"+waLink());return;}add('bot',A[intent]||A.fallback);}
  function detect(t){for(var i=0;i<RULES.length;i++){if(RULES[i][0].test(t))return RULES[i][1];}return 'fallback';}
  // These four are about doing something, not about knowing something, so they
  // must win over any article the knowledge base might match.
  var HARD=/rate|price|cost|quote|how much|magkano|presyo|budget|hire|start|begin|book|whats ?app|contact|talk to|email|message you/i;
  function ask(text,intent){
    add('me',text);
    if(intent){ typing(function(){reply(intent);chipsFor(intent);}); return; }
    if(HARD.test(text)){ var k=detect(text); typing(function(){reply(k);chipsFor(k);}); return; }
    var hit=score(text);
    if(hit){ typing(function(){ add('bot',kbAnswer(hit)); chipsFor(''); }); return; }
    var k2=detect(text); typing(function(){reply(k2);chipsFor(k2);});
  }
  function open(){box.classList.add('open');box.setAttribute('aria-hidden','false');fab.setAttribute('aria-expanded','true');if(!log.children.length){add('bot',A.hello,false);chipsFor('hello');}setTimeout(function(){if(box.classList.contains('lead-on')){var n=lead&&lead.querySelector('input[name=name]');if(n)n.focus();}else inp.focus();},250);}
  function close(){box.classList.remove('open');box.setAttribute('aria-hidden','true');fab.setAttribute('aria-expanded','false');}
  fab.addEventListener('click',function(){box.classList.contains('open')?close():open();});
  x.addEventListener('click',close);
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
  var leadBack=document.getElementById('jl-lead-back');
  if(leadBack) leadBack.addEventListener('click',function(){chipsFor('');inp.focus();});
  form.addEventListener('submit',function(e){e.preventDefault();var t=inp.value.trim();if(!t)return;inp.value='';ask(t);});
  try{var saved=JSON.parse(localStorage.getItem(KEY)||'[]');if(saved.length){saved.forEach(function(h){add(h[0],h[1],false);});hist=saved;chipsFor('');}}catch(e){}
})();
"""

def shell(title, desc, body, active, up="", extra_js=""):
    p = PROFILE
    vj = VCARD_JS % dict(last=p['last'], first=p['first'], name=p['name'], title=p['vcard_title'],
                         tel=p['tel'], email=p['email'], li=p['linkedin'], file=p['vcard_file'],
                         social="".join(f',"URL:{u}"' for _, _, u in socials()))
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="author" content="{E(p['name'])}">
<meta name="theme-color" content="#0B0B0B">
<link rel="icon" type="image/png" href="{up}assets/images/favicon.png">
<link rel="apple-touch-icon" href="{up}assets/images/apple-touch-icon.png">
<script>(function(){{try{{var v=localStorage.getItem('jl-theme');if(v){{document.documentElement.setAttribute('data-theme',v);var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute('content',v==='light'?'#EFEBE4':'#0B0B0B');}}}}catch(e){{}}}})();</script>
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<script>document.documentElement.classList.add('js')</script>
<div class="blobs" aria-hidden="true"><i class="b1"></i><i class="b2"></i></div>
{ICONS}
{nav(active, up)}
{body}
{chat_widget(up)}
<script>{vj}{REVEAL_JS}{THEME_JS}{CHAT_JS % dict(wa=p['whatsapp'], mail=p['email'], up=up, kb=chat_kb())}{LEAD_JS % dict(wa=p['whatsapp'], mail=p['email'])}{extra_js}</script>
</body>
</html>
'''


def footer():
    p = PROFILE
    return f'''<footer id="contact">
<div class="wrap"><div class="footin footrow">
<div class="foot-left"><h2 class="serif">Let's talk.</h2>{contact_nav()}
<div class="copy"><span class="eyebrow muted">© 2026 {E((p['name']).upper())}</span>
<span class="eyebrow muted">{E((p['location']).upper())}</span></div></div>
<div class="lead-col"><h3 class="serif">Or leave a message</h3><p>Tell me about the store or project. I reply by email within the day.</p>{lead_form('footer', extra='<button class="btn ghost foot-vcard" type="button" onclick="downloadVCard()"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-dl"/></svg>Save contact</button>')}</div>
</div></div></footer>'''


def portrait_html(ratio="r34", note="IMAGE \u2014 PORTRAIT", style=""):
    """The photo on the home and About pages, or a placeholder if none is set.

    The ratio is locked on the WRAPPER and the image is absolutely positioned
    inside it. Putting aspect-ratio on the <img> itself fights the file's own
    intrinsic ratio and the width/height attributes, which is how it ended up
    taller than the box it was supposed to sit in.
    """
    st = ' style="%s"' % style if style else ""
    f = PROFILE.get("portrait")
    if not f:
        return '<div class="ph %s"%s>[ %s ]</div>' % (ratio, st, note)
    return ('<div class="shot %s"%s>'
            '<img src="assets/images/%s" alt="%s" width="900" height="1200" '
            'loading="lazy" decoding="async"></div>'
            % (ratio, st, E(f), E(PROFILE["name"])))


IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif', '.avif')


def is_image(val):
    if not val or not isinstance(val, str):
        return False
    clean = val.strip().lower()
    return any(clean.endswith(ext) for ext in IMAGE_EXTS)


def render_media(val, ratio="r43", alt="", up=""):
    """Render a responsive .shot container if val is an image file, or .ph placeholder if text."""
    if is_image(val):
        val = val.strip()
        src = val if val.startswith(("http://", "https://", "/")) else f"{up}assets/images/{val}"
        return (f'<div class="shot {ratio}">'
                f'<img src="{E(src)}" alt="{E(alt)}" width="800" height="600" '
                f'loading="lazy" decoding="async"></div>')
    note = val if val else "IMAGE"
    return f'<div class="ph {ratio}">[ {E(note.upper())} ]</div>'


def card_html(pr, base="work/", up=""):
    """base is the path prefix to the work/ folder from the page being built;
    up is the path prefix to the assets/ folder."""
    d = DISCIPLINES[pr['discipline']]
    cover = pr.get("cover") or pr.get("cover_note")
    visual = render_media(cover, "r43", pr['title'], up=up)
    live_chip = ('<span class="chip live"><span class="live-dot" aria-hidden="true"></span>Live</span>'
                 if pr.get("link") else "")
    return f'''<a class="card rv" href="{base}{pr['slug']}.html">
{visual}
<div class="body"><div style="display:flex;align-items:center;flex-wrap:wrap;gap:.4rem"><span class="chip">{E(d)}</span>{live_chip}</div>
<h3 style="margin-top:.85rem">{E(pr['title'])}</h3>
<p class="sum">{E(pr['summary'])}</p>
<span class="more">View project</span></div></a>'''


# ------------------------------------------------------------------- builders
def build_home():
    p = PROFILE
    feat = [x for x in PROJECTS if x.get('featured')]
    stats = "".join(
        f'<div class="rv"><span class="n">{E(s["n"])}</span>'
        f'<span class="eyebrow muted l">{E(s["l"])}</span></div>' for s in STATS)
    cards = "".join(card_html(x, base="work/", up="") for x in feat)
    strip = "".join(f'<span>{E(x)}</span>' for x in MARQUEE)
    marquee = (f'<div class="marquee" aria-label="What I do">'
               f'<div class="mtrack"><div class="mset">{strip}</div>'
               f'<div class="mset" aria-hidden="true">{strip}</div></div></div>')
    body = f'''<header id="top"><div class="wrap"><div class="headrow"><div>
<h1>{E(p['name'])}</h1>
<p class="eyebrow muted sub">{E(p['subtitle'])}</p>
{contact_nav()}</div>
<button class="btn" type="button" onclick="downloadVCard()">
<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-dl"/></svg>SAVE TO CONTACTS</button>
</div></div></header>
<main><div class="wrap">
<section class="rv"><p class="lede">{E(p['intro'])}</p></section>
<section class="stats" style="padding-top:0">{stats}</section>
</div>{marquee}<div class="wrap">
<section><h2 class="eyebrow grouphead"><span>SELECTED WORK</span><span class="rule"></span></h2>
<div class="cards">{cards}</div>
<p style="margin-top:3rem"><a class="more" href="work/index.html">See all {len(PROJECTS)} projects</a></p>
</section>
</div></main>{footer()}'''
    write("index.html", shell(f"{p['name']} — {p['subtitle_plain']}", p['intro'], body, "home"))


def build_work_index():
    p = PROFILE
    btns = '<button class="on" data-f="all" aria-pressed="true">All</button>' + "".join(
        f'<button data-f="{k}" aria-pressed="false">{E(v)}</button>' for k, v in DISCIPLINES.items())
    cards = "".join(
        f'<div data-d="{x["discipline"]}">{card_html(x, base="../work/", up="../")}</div>' for x in PROJECTS)
    js = """
(function(){var b=[].slice.call(document.querySelectorAll('.filters button'));
var c=[].slice.call(document.querySelectorAll('.cards>[data-d]'));
b.forEach(function(x){x.addEventListener('click',function(){
b.forEach(function(y){y.classList.remove('on');y.setAttribute('aria-pressed','false')});
x.classList.add('on');x.setAttribute('aria-pressed','true');var f=x.dataset.f;
c.forEach(function(z){z.style.display=(f==='all'||z.dataset.d===f)?'':'none'})})})})();
"""
    body = f'''<header id="top"><div class="wrap">
<p class="eyebrow muted">SELECTED WORK</p>
<h1 style="margin-top:.75rem">Projects</h1>
<p class="muted" style="margin-top:1rem;max-width:38rem">{len(PROJECTS)} projects across {len(DISCIPLINES)} disciplines.</p>
</div></header>
<main><div class="wrap"><section>
<div class="filters" role="group" aria-label="Filter by discipline">{btns}</div>
<div class="cards">{cards}</div>
</section></div></main>{footer()}'''
    write("work/index.html", shell(f"Work — {p['name']}",
          f"{len(PROJECTS)} projects across {len(DISCIPLINES)} disciplines.", body, "work", up="../",
          extra_js=js))


LIGHTBOX_HTML = """
<div id="lb" class="lb" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Image preview">
 <button class="lb-close" type="button" aria-label="Close image preview">&times;</button>
 <div class="lb-body">
  <img id="lb-img" src="" alt="">
  <p id="lb-cap" class="lb-cap"></p>
 </div>
</div>
"""

LIGHTBOX_JS = """
(function(){
 var lb=document.getElementById('lb');if(!lb)return;
 var img=document.getElementById('lb-img'),cap=document.getElementById('lb-cap'),last=null;
 function open(src,alt){
  last=document.activeElement;
  img.src=src;img.alt=alt||'';cap.textContent=alt||'';
  lb.classList.add('open');lb.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
  var b=lb.querySelector('.lb-close');if(b)b.focus();
 }
 function close(){
  lb.classList.remove('open');lb.setAttribute('aria-hidden','true');
  document.body.style.overflow='';
  img.src='';if(last)last.focus();
 }
 document.querySelectorAll('.shot img').forEach(function(el){
  el.addEventListener('click',function(e){e.stopPropagation();open(el.src,el.alt)});
 });
 lb.addEventListener('click',function(e){if(e.target===lb||e.target.closest('.lb-close'))close()});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('open'))close()});
})();
"""


def build_project(i, pr):
    p = PROFILE
    prev_p = PROJECTS[i - 1] if i > 0 else None
    next_p = PROJECTS[i + 1] if i < len(PROJECTS) - 1 else None
    tags = "".join(f'<span class="chip">{E(t)}</span>' for t in pr['tags'])
    cover = pr.get("cover") or pr.get("cover_note")
    cover_visual = render_media(cover, "r32", pr['title'], up="../")
    caps = pr.get('gallery_captions') or []
    gal_items = []
    for i, g in enumerate(pr.get('gallery', [])):
        if isinstance(g, dict) and g.get("video"):
            # Landscape / custom-ratio video block. The bare-list branch below is
            # the 9:16 phone-video row; this one lets a 16:9 walkthrough run full
            # width instead of being cropped to a vertical box.
            vr = g.get("ratio", "r169")
            vids = "".join(
                f'<div class="vid {vr}"><video controls muted playsinline preload="metadata" '
                f'poster="../assets/video/{E(v.rsplit(".",1)[0])}.jpg">'
                f'<source src="../assets/video/{E(v)}" type="video/mp4"></video></div>'
                for v in g["video"])
            n = len(g["video"])
            media = f'<div class="vidrow{" one" if n == 1 else ""}">{vids}</div>'
        elif isinstance(g, dict):
            ratio = g.get("ratio", "r11")
            tiles = "".join(render_media(f, ratio, g.get("alt", pr['title']), up="../") for f in g.get("grid", []))
            head = ""
            if g.get("title"):
                head = (f'<div class="galset-head"><h4>{E(g["title"])}</h4>'
                        + (f'<span class="muted">{E(g["sub"])}</span>' if g.get("sub") else "") + '</div>')
            n = len(g.get("grid", []))
            media = f'<div class="galset">{head}<div class="strip strip-{ratio}" data-n="{n}">{tiles}</div></div>'
        elif isinstance(g, (list, tuple)):
            vids = "".join(
                f'<div class="vid r916"><video controls muted playsinline preload="metadata" '
                f'poster="../assets/video/{E(v.rsplit(".",1)[0])}.jpg" width="1080" height="1920">'
                f'<source src="../assets/video/{E(v)}" type="video/mp4"></video></div>' for v in g)
            media = f'<div class="vidrow">{vids}</div>'
        else:
            media = render_media(g, "r43", (caps[i] if i < len(caps) else f"{pr['title']} preview"), up="../")
        wide = isinstance(g, (list, tuple, dict))
        if i < len(caps) and caps[i]:
            media = f'<figure class="galfig{" galwide" if wide else ""}">{media}<figcaption>{E(caps[i])}</figcaption></figure>'
        elif wide:
            media = f'<div class="galwide">{media}</div>'
        gal_items.append(media)
    galblock = f'<div class="gal">{"".join(gal_items)}</div>' if gal_items else ""
    live = (f'<p style="margin-top:1.25rem"><a class="live-link" href="{E(pr["link"])}" '
            f'target="_blank" rel="noopener">'
            f'<span class="live-dot" aria-hidden="true"></span>'
            f'{E(pr.get("link_label", "Visit the live site"))} \u2197</a></p>'
            if pr.get("link") else "")
    pn = '<div class="pn">'
    pn += (f'<a href="{prev_p["slug"]}.html"><span>Previous</span>{E(prev_p["title"])}</a>'
           if prev_p else '<span></span>')
    pn += (f'<a href="{next_p["slug"]}.html" style="text-align:right">'
           f'<span>Next</span>{E(next_p["title"])}</a>' if next_p else '<span></span>')
    pn += '</div>'
    cta = ""
    if pr.get("discipline") == "ecom":
        cta = f'''<div class="dfy-card" style="margin:2.5rem 0 2rem">
<div class="dfy-info">
<span class="pro-badge">AVAILABLE FOR CLIENT PROJECTS</span>
<h3 class="serif" style="font-size:1.4rem">Need a storefront overhaul or listing compliance scrub for your brand?</h3>
<p>I design high-converting A+ listing slides, optimize mobile storefronts, and resolve marketplace policy violations across Shopee, Lazada, TikTok Shop, Amazon &amp; Shopify.</p>
</div>
<div class="dfy-btns">
<div>
<a class="btn" href="https://wa.me/639394886685?text=Hi%20Jamie%21%20I%20saw%20your%20{E(pr['title'])}%20project%20and%20I%27d%20like%20to%20inquire%20about%20a%20storefront%20overhaul." target="_blank" rel="noopener">
<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg>Inquire on WhatsApp</a>
</div></div></div>'''
    elif pr.get("slug") == "philmed-expo-2026" or pr.get("discipline") == "interior":
        cta = f'''<div class="dfy-card" style="margin:2.5rem 0 2rem">
<div class="dfy-info">
<span class="pro-badge">AVAILABLE FOR CLIENT PROJECTS</span>
<h3 class="serif" style="font-size:1.4rem">Need a turnkey 3D booth or commercial spatial layout for your next event?</h3>
<p>From 3D photorealistic perspective renders to contractor elevation blueprints and print-ready graphic production.</p>
</div>
<div class="dfy-btns">
<div>
<a class="btn" href="https://wa.me/639394886685?text=Hi%20Jamie%21%20I%20saw%20your%20PhilMed%20booth%20project%20and%20I%27d%20like%20to%20inquire%20about%20a%203D%20booth%20design." target="_blank" rel="noopener">
<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg>Inquire on WhatsApp</a>
</div></div></div>'''
    body = f'''<header id="top"><div class="wrap">
<p class="eyebrow muted">{E((DISCIPLINES[pr['discipline']]).upper())}{(" · " + E(pr['year'])) if pr.get('year') else ""}</p>
<h1 style="margin-top:.75rem">{E(pr['title'])}</h1>
<div class="tags">{tags}</div>
{live}
</div></header>
<main><div class="wrap"><section>
{cover_visual}
<div class="cols c3">
<div><span class="eyebrow lab">Challenge</span>{paras(pr['challenge'])}</div>
<div><span class="eyebrow lab">What I did</span>{paras(pr['approach'])}</div>
<div><span class="eyebrow lab">Result</span>{paras(pr['result'])}</div>
</div>
{galblock}
{cta}
{pn}
<p style="margin-top:2.5rem"><a class="more" href="index.html">All projects</a></p>
</section></div></main>{LIGHTBOX_HTML}{footer()}'''
    write(f"work/{pr['slug']}.html",
          shell(f"{pr['title']} — {p['name']}", pr['summary'], body, "work", up="../",
                extra_js=LIGHTBOX_JS))


QUOTE_JS = r"""
(function(){
var box=document.querySelector('.qmq');if(!box)return;
var down=false,x0=0,l0=0;
box.addEventListener('pointerdown',function(e){
  if(e.pointerType==='touch')return;          /* let the OS handle real touch */
  down=true;x0=e.clientX;l0=box.scrollLeft;
  box.setPointerCapture(e.pointerId);box.classList.add('grabbing')});
box.addEventListener('pointermove',function(e){
  if(!down)return;e.preventDefault();box.scrollLeft=l0-(e.clientX-x0)});
function up(){down=false;box.classList.remove('grabbing')}
box.addEventListener('pointerup',up);
box.addEventListener('pointercancel',up);
box.addEventListener('dragstart',function(e){e.preventDefault()});
})();
"""


def build_about():
    p = PROFILE
    pat = "".join(
        f'<div><span class="eyebrow acc">{E((b["label"]).upper())}</span><p>{E(b["text"])}</p></div>'
        for b in PATTERN)
    tools = "".join(
        f'<div class="tool"><h4 class="eyebrow acc">{E((g["group"]).upper())}</h4>'
        f'<ul>{"".join(f"<li>{E(i)}</li>" for i in g["items"])}</ul></div>'
        for g in STACK)
    exp = "".join(
        f'<div class="rv"><h4 class="eyebrow">{E(g["group"])}</h4>'
        f'<p>{E(" · ".join(g["items"]))}</p></div>' for g in EXPERTISE)

    creds = "".join(
        '<li class="cred"><span class="r"><b>{}</b>{}</span>{}</li>'.format(
            E(c["role"]),
            f'<span>{E(c["org"])}</span>' if c.get("org") else "",
            f'<time>{E(c["period"])}</time>' if c.get("period") else "")
        for c in CREDENTIALS)
    bgblock = ""
    if BACKGROUND:
        b = BACKGROUND
        pts = "".join(f'<li>{E(x)}</li>' for x in b.get("points", []))
        bgblock = ('<div class="bg-note glass rv" '
                   'style="padding:1.5rem;border-radius:var(--rad);margin-top:0">'
                   + (f'<b class="deg" style="margin-top:0">{E(b["degree"])}</b>'
                      if b.get("degree") else "")
                   + (f'<span class="sch">{E(b["school"])}</span>' if b.get("school") else "")
                   + (f'<ul>{pts}</ul>' if pts else "")
                   + (f'<span class="stat">{E(b["note"])}</span>' if b.get("note") else "")
                   + '</div>')
    edusec = ('<section><h2 class="eyebrow grouphead"><span>EDUCATION</span>'
              '<span class="rule"></span></h2>' + bgblock + '</section>') if bgblock else ""
    credsec = ('<section><h2 class="eyebrow grouphead"><span>CREDENTIALS</span>'
               '<span class="rule"></span></h2>'
               f'<ul class="creds rv" style="list-style:none;margin:0;padding:0">{creds}</ul>'
               '</section>')

    def qcard(t):
        nm, rl = t.get("name", ""), t.get("role", "")
        ini = "".join(w[0] for w in nm.split()[:2]).upper()
        if t.get("photo"):
            av = (f'<img class="av" src="assets/images/{E(t["photo"])}" '
                  f'alt="{E(nm)}" width="42" height="42" loading="lazy">')
        else:
            av = f'<span class="av ini" aria-hidden="true">{E(ini)}</span>'
        q = (t.get("quote") or "").strip()
        quote = (f'<blockquote>{E(q)}</blockquote>' if q
                 else '<blockquote class="await">Quote to follow</blockquote>')
        cls = "" if q else ' class="pending"'
        return (f'<figure{cls}>{quote}<figcaption>{av}'
                f'<span class="who"><strong>{E(nm)}</strong>'
                f'<span class="muted">{E(rl)}</span></span></figcaption></figure>')

    blank = ('<figure class="pending"><blockquote class="await">Testimonial pending</blockquote>'
             '<figcaption><span class="av ini" aria-hidden="true">\u2014</span>'
             '<span class="who"><strong class="muted">Awaiting their words</strong>'
             '</span></figcaption></figure>')
    cards = "".join(qcard(t) for t in TESTIMONIALS) + blank * TESTIMONIALS_PENDING
    pending_left = TESTIMONIALS_PENDING + sum(
        1 for t in TESTIMONIALS if not (t.get("quote") or "").strip())
    note = ('<p class="muted" style="font-size:.875rem;margin-top:1.25rem">'
            'More requests are out. Real quotes only \u2014 nothing here is written by me.</p>'
            if pending_left else "")

    quotes = ('<section><h2 class="eyebrow grouphead"><span>WHAT PEOPLE SAY</span>'
              '<span class="rule"></span></h2>'
              '<div class="qmq" tabindex="0" role="region"'
              ' aria-label="Testimonials, scroll sideways">'
              f'<div class="qtrack quotes">{cards}</div></div>' + note + '</section>')

    body = f'''<header id="top"><div class="wrap">
<p class="eyebrow muted">ABOUT</p>
<h1 style="margin-top:.75rem">{E(p['name'])}</h1>
<p class="eyebrow muted sub">{E(p['subtitle'])}</p>
</div></header>
<main><div class="wrap">

<section class="rv" style="padding-top:2.5rem">
  <div class="aboutgrid">
    <div class="shotframe">{portrait_html("r34", "IMAGE — PORTRAIT", "margin:0")}</div>
    <div>
      <h3 class="serif" style="font-size:clamp(1.5rem,5vw,2rem)">{E(p['role'])}</h3>
      <p class="meta">{E(p['location'])} <span>·</span> {E(p.get('status',''))}</p>
      {bio_html(BIO)}
      <a class="btn ghost" href="card.html" style="margin-top:1.5rem">Open digital card</a>
    </div>
  </div>
</section>

<section>
  <h2 class="eyebrow grouphead"><span>HOW I WORK</span><span class="rule"></span></h2>
  <div class="pattern">{pat}</div>
  <div class="philo glass rv"><span class="eyebrow acc">PHILOSOPHY</span>
    <p>{E(PHILOSOPHY)}</p></div>
</section>

<section>
  <h2 class="eyebrow grouphead"><span>EXPERTISE</span><span class="rule"></span></h2>
  <div class="exp">{exp}</div>
</section>

<section>
  <h2 class="eyebrow grouphead"><span>TOOLS I USE</span><span class="rule"></span></h2>
  <div class="tools">{tools}</div>
</section>

{edusec}

{credsec}

<section>
  <h2 class="eyebrow grouphead"><span>SERVICES</span><span class="rule"></span></h2>
  <p class="muted" style="max-width:38rem;margin-bottom:1.75rem">
    Specialized services across digital commerce, commercial 3D environments, and creative operations.
    One-off projects or monthly retainers — message me with your store or event and I will send a scope and quote.
  </p>
  <div class="services-grid">
    <div class="service-card">
      <span class="pro-badge">DIGITAL SPACES</span>
      <h3 class="serif">Marketplace Storefront &amp; A+ Listing Overhaul</h3>
      <p>Turnkey visual architecture and listing compliance defense for brands on Shopee, Lazada, TikTok Shop, Amazon &amp; Shopify.</p>
      <ul>
        <li>Mobile-first branded storefront layout</li>
        <li>5 Hero listings with 7-slide conversion architecture</li>
        <li>Catalog policy scrub &amp; banned claim resolution</li>
        <li>High-intent keyword harvesting &amp; SEO tags</li>
      </ul>
      <a class="btn" href="https://wa.me/639394886685?text=Hi%20Jamie%21%20I%27d%20like%20to%20inquire%20about%20your%20Storefront%20%26%20A%2B%20Listing%20Overhaul%20package." target="_blank" rel="noopener" style="margin-top:1.25rem">
        <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg>Inquire on WhatsApp
      </a>
    </div>

    <div class="service-card" style="border-color:var(--acc)">
      <span class="pro-badge">PHYSICAL &amp; 3D SPACES</span>
      <h3 class="serif">Trade Show Booth &amp; 3D Product Turnkey</h3>
      <p>Complete 3D spatial design from architectural perspective renders to contractor blueprints and Blender product models.</p>
      <ul>
        <li>3D photorealistic booth renders (SketchUp / Enscape)</li>
        <li>Contractor construction elevations &amp; electrical layout</li>
        <li>Print-ready fascia, tarpaulin &amp; banner production files</li>
        <li>3D Blender product modeling (5 studio angles, lifestyle)</li>
      </ul>
      <a class="btn" href="https://wa.me/639394886685?text=Hi%20Jamie%21%20I%27d%20like%20to%20inquire%20about%20your%203D%20Booth%20%26%20Product%20Visualization%20package." target="_blank" rel="noopener" style="margin-top:1.25rem">
        <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg>Inquire on WhatsApp
      </a>
    </div>

    <div class="service-card">
      <span class="pro-badge">CREATIVE OPERATIONS</span>
      <h3 class="serif">Creative Ops Hub &amp; Automated Team Bots</h3>
      <p>Systematize multi-brand marketing chaos with centralized Notion command centers and automated reporting bots.</p>
      <ul>
        <li>Centralized 3-brand content calendar &amp; scheduling</li>
        <li>Automated Telegram / Slack team accomplishment bot</li>
        <li>SOP documentation &amp; campaign tracking dashboard</li>
        <li>Stock velocity &amp; reorder health tracker</li>
      </ul>
      <a class="btn" href="https://wa.me/639394886685?text=Hi%20Jamie%21%20I%27d%20like%20to%20inquire%20about%20your%20Notion%20Operations%20Hub%20%26%20Team%20Bot%20setup." target="_blank" rel="noopener" style="margin-top:1.25rem">
        <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg>Inquire on WhatsApp
      </a>
    </div>
  </div>
</section>

{quotes}

</div></main>{footer()}'''
    write("about.html", shell(f"About — {p['name']}", ABOUT, body, "about",
                              extra_js=QUOTE_JS))


TOOL_JS = r"""
(function(){
  var currentPlat = 'sea';
  var limits = {
    amazon:  { max: 200, optMin: 150, optMax: 200, name: 'Amazon (US/UK)',
               note: 'Title hard-capped at 200 characters — the A9 algorithm penalizes overage. No unverified superlatives (“best seller”) or pesticide / unregistered-product claims in the title.' },
    shopify: { max: 60,  optMin: 40,  optMax: 60,  name: 'Shopify & Google Shopping',
               note: 'Optimal title ≤60 characters so Google Search doesn’t truncate it. Meta description ≤160 characters — use the field below.' },
    tiktok:  { max: 200, optMin: 80,  optMax: 150, name: 'TikTok Shop (Global — US/UK)',
               note: 'Extreme scrutiny on rapid cosmetic or supplement result claims — any “in X days” language draws manual review.' },
    etsy:    { max: 140, optMin: 100, optMax: 140, name: 'Etsy',
               note: 'Title capped at 140 characters, plus a 13-tag keyword limit — use the tag counter below.' },
    sea:     { max: 255, optMin: 80,  optMax: 120, name: 'Shopee & Lazada (Southeast Asia)',
               note: '255-character limit. Local DTI/FDA triggers: “pampaputi”, “pinakamura”, “PM is the key”.' }
  };
  var PLAT_ORDER = ['amazon','shopify','tiktok','etsy','sea'];

  function showToast(msg){
    var t = document.getElementById('toast');
    if(!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(function(){ t.classList.remove('show'); }, 2400);
  }
  window.showToast = showToast;

  var BANNED_PATTERNS = [
    { regex: /\b(cure|cures|curing|curative)\b/gi, sev: 'critical', reason: 'Direct disease cure claims violate FDA/DTI and marketplace policies. Results in immediate product freezing.', fix: 'helps support / daily care' },
    { regex: /\b(anti-cancer|cancer cure|prevents cancer|anti-tumor)\b/gi, sev: 'critical', reason: 'Disease treatment and cure claims are strictly prohibited on e-commerce platforms.', fix: 'general wellness support' },
    { regex: /\b(fda approved|fda certified)\b/gi, sev: 'critical', reason: 'Stating "FDA Approved" in titles without exact CPR/registration number triggers algorithmic takedowns.', fix: 'FDA Notified / Registered' },
    { regex: /\b(covid|coronavirus|covid-19)\b/gi, sev: 'critical', reason: 'Automated platform pandemic exploitation keyword filter.', fix: '' },
    { regex: /\b(pampaputi|instant whitening|whitening in 7 days|permanent white)\b/gi, sev: 'critical', reason: 'Unverified medical whitening and rapid-result timelines violate cosmetic advertising rules.', fix: 'brightening & radiance' },
    { regex: /\b(slimming|weight loss|fat burner|burn fat fast|diet pills)\b/gi, sev: 'critical', reason: 'Rapid weight loss claims trigger immediate health policy audits.', fix: 'dietary supplement / fitness support' },
    { regex: /\b(100% effective|guaranteed effective|100% guaranteed|miracle cure|magic cure)\b/gi, sev: 'critical', reason: 'Absolute guarantee claims violate DTI Fair Trade policies and marketplace guidelines.', fix: 'clinically tested / quality formula' },
    { regex: /\b(no\.?\s*1|number\s*1|#1\s+brand|#1\s+in\s+the\s+philippines)\b/gi, sev: 'warning', reason: 'Superlatives ("No. 1") require certified DTI market survey proof. Bots penalize this in search rank.', fix: 'trusted / leading' },
    { regex: /\b(pinakamura|cheapest|lowest price guaranteed|shopee cheapest|lazada cheapest)\b/gi, sev: 'warning', reason: 'Unsubstantiated price comparison claims trigger unfair trade practice filters.', fix: 'affordable / value pack' },
    { regex: /\b(best seller|best quality in the world)\b/gi, sev: 'warning', reason: 'Subjective superlatives trigger quality report flags and waste title character quota.', fix: 'top choice / premium grade' },
    { regex: /\b(free shipping|free delivery)\b/gi, sev: 'warning', reason: 'Platform promotional tags belong in platform vouchers, not in the product title.', fix: '' },
    { regex: /\b(100% original|100% authentic|original guaranteed)\b/gi, sev: 'warning', reason: 'Using "100% Original" in titles often triggers algorithmic Brand IP Authenticity Audits.', fix: 'Official Store / Authentic Quality' },
    { regex: /\b(pm me|pm is the key|viber|whatsapp|telegram|direct transaction)\b/gi, sev: 'critical', reason: 'Off-platform transaction solicitation triggers immediate account suspension.', fix: '' }
  ];

  /* Each category is policed differently. The multiplier scales every penalty,
     and each profile adds its own watch-list of words that are only risky here. */
  var CATEGORY_PROFILES = {
    health: {
      label: 'Health, Beauty & Skincare', mult: 1.5,
      note: 'Strict profile — cosmetic claims are audited hardest. Every flag costs 1.5× here, and whitening / acne / anti-aging wording is checked on top.',
      watch: [
        { regex: /\b(whitening|anti-aging|anti aging|acne cure|glutathione|flawless skin|kutis artista)\b/gi,
          reason: 'Cosmetic efficacy wording in the Health & Beauty category draws a manual claims review even when it is not on the global banned list.',
          fix: 'brightening / skin care' }
      ]
    },
    medical: {
      label: 'Medical Devices & Supplements', mult: 2,
      note: 'Strictest profile — FDA and therapeutic wording carries a 2× penalty. In this category a disease or treatment claim is a takedown, not a warning.',
      watch: [
        { regex: /\b(therapeutic|treatment for|diagnos(is|e|tic)|medical grade|prescription|clinically proven|doctor recommended)\b/gi,
          reason: 'Therapeutic or diagnostic wording on a medical listing requires registration documents on file. Without a CPR number this is a takedown risk.',
          fix: 'for personal / clinic use' }
      ]
    },
    general: {
      label: 'General Merchandise & Home', mult: 1,
      note: 'Baseline profile — superlative and DTI fair-trade rules only. This is the most forgiving category.',
      watch: []
    },
    electronics: {
      label: 'Electronics & Gadgets', mult: 1.2,
      note: 'Authenticity and warranty wording is the main trigger here — IP and counterfeit flags cost 1.2× and brand-claim words are checked on top.',
      watch: [
        { regex: /\b(class a|replica|oem quality|copy original|high copy|refurbished as new)\b/gi,
          reason: 'Counterfeit-adjacent wording on an electronics listing triggers Brand IP enforcement, which escalates to account-level strikes.',
          fix: 'compatible / aftermarket' }
      ]
    }
  };

  var titleEl = document.getElementById('listing-title');
  var descEl = document.getElementById('listing-desc');
  var catEl = document.getElementById('risk-cat');
  var platBtns = document.querySelectorAll('.plat-btn');
  var charNum = document.getElementById('char-num');
  var charMax = document.getElementById('char-max');
  var charStatus = document.getElementById('char-status');
  var descWordNum = document.getElementById('desc-word-num');
  var scoreNum = document.getElementById('score-num');
  var scoreStatus = document.getElementById('score-status');
  var scoreDesc = document.getElementById('score-desc');
  var findingsList = document.getElementById('findings-list');
  var findingsSummary = document.getElementById('findings-summary');
  var platNoteEl = document.getElementById('plat-note');
  var etsyWrap = document.getElementById('etsy-tag-wrap');
  var etsyTagsEl = document.getElementById('etsy-tags');
  var etsyTagCount = document.getElementById('etsy-tag-count');
  var shopifyWrap = document.getElementById('shopify-meta-wrap');
  var shopifyMetaEl = document.getElementById('shopify-meta');
  var shopifyMetaCount = document.getElementById('shopify-meta-count');
  var catNoteEl = document.getElementById('cat-note');
  var titleHl = document.getElementById('title-hl');
  var descHl = document.getElementById('desc-hl');
  var lastFindings = [];
  var lastScore = null;

  function getWords(str){
    var m = str.trim().match(/\S+/g);
    return m ? m.length : 0;
  }

  function activeProfile(){
    var key = catEl ? catEl.value : 'general';
    return CATEGORY_PROFILES[key] || CATEGORY_PROFILES.general;
  }

  /* ---- inline highlighting ---------------------------------------------- */
  function escHtml(s){
    return s.replace(/[&<>]/g, function(c){
      return c === '&' ? '&amp;' : (c === '<' ? '&lt;' : '&gt;');
    });
  }

  function flaggedRanges(text){
    var prof = activeProfile();
    var all = BANNED_PATTERNS.concat(prof.watch || []);
    var ranges = [];
    all.forEach(function(item){
      var re = new RegExp(item.regex.source, 'gi');
      var m;
      while((m = re.exec(text)) !== null){
        if(m[0].length === 0){ re.lastIndex++; continue; }
        ranges.push({ start: m.index, end: m.index + m[0].length, sev: item.sev || 'warning' });
      }
    });
    ranges.sort(function(a, b){ return a.start - b.start; });
    var merged = [];
    ranges.forEach(function(r){
      var last = merged[merged.length - 1];
      if(last && r.start <= last.end){
        last.end = Math.max(last.end, r.end);
        if(r.sev === 'critical') last.sev = 'critical';
      } else {
        merged.push({ start: r.start, end: r.end, sev: r.sev });
      }
    });
    return merged;
  }

  function paintHighlights(el, backdrop){
    if(!el || !backdrop) return;
    var text = el.value || '';
    var ranges = flaggedRanges(text);
    var out = '', pos = 0;
    ranges.forEach(function(r){
      out += escHtml(text.slice(pos, r.start));
      out += '<mark class="' + (r.sev === 'critical' ? 'crit' : 'warn') + '">'
           + escHtml(text.slice(r.start, r.end)) + '</mark>';
      pos = r.end;
    });
    out += escHtml(text.slice(pos)) + '\n';
    backdrop.innerHTML = out;
    backdrop.scrollTop = el.scrollTop;
  }

  function updateConditionalFields(){
    if(platNoteEl) platNoteEl.textContent = limits[currentPlat].note || '';
    if(etsyWrap) etsyWrap.style.display = (currentPlat === 'etsy') ? '' : 'none';
    if(shopifyWrap) shopifyWrap.style.display = (currentPlat === 'shopify') ? '' : 'none';
  }

  function auditEtsyTags(){
    if(!etsyTagsEl || !etsyTagCount) return;
    var tags = etsyTagsEl.value.split(',').map(function(t){return t.trim();}).filter(Boolean);
    etsyTagCount.textContent = tags.length;
    etsyTagCount.className = tags.length > 13 ? 'bad' : (tags.length === 13 ? 'ok' : '');
  }

  function auditShopifyMeta(){
    if(!shopifyMetaEl || !shopifyMetaCount) return;
    var len = shopifyMetaEl.value.length;
    shopifyMetaCount.textContent = len;
    shopifyMetaCount.className = len > 160 ? 'bad' : (len >= 120 ? 'ok' : 'warn');
  }

  function audit(){
    if(!titleEl) return;
    auditEtsyTags();
    auditShopifyMeta();
    paintHighlights(titleEl, titleHl);
    paintHighlights(descEl, descHl);
    var title = titleEl.value || '';
    var desc = descEl ? (descEl.value || '') : '';
    var fullText = title + ' ' + desc;
    var plat = limits[currentPlat];
    var prof = activeProfile();
    if(catNoteEl) catNoteEl.textContent = prof.note;
    saveState();

    var tLen = title.length;
    if(charNum) charNum.textContent = tLen;
    if(charMax) charMax.textContent = plat.max;
    if(descWordNum) descWordNum.textContent = getWords(desc);

    if(tLen === 0){
      if(charStatus) { charStatus.textContent = 'Optimal: ' + plat.optMin + '–' + plat.optMax; charStatus.className = ''; }
      if(scoreNum) scoreNum.textContent = '--';
      var d0 = document.getElementById('score-dial');
      if(d0) d0.style.borderColor = 'var(--acc)';
      if(scoreStatus) scoreStatus.textContent = 'Ready to Scan';
      if(scoreDesc) scoreDesc.textContent = 'Paste your product title above to inspect for bot flags and SEO.';
      if(findingsList) findingsList.innerHTML = '<p class="muted" style="font-size:13px;padding:1rem 0">Enter your listing title or click "Load High-Risk Sample" to see real-time compliance results.</p>';
      if(findingsSummary) findingsSummary.textContent = 'Waiting for input...';
      lastFindings = [];
      lastScore = null;
      return;
    }

    if(tLen < plat.optMin){
      if(charStatus) { charStatus.textContent = 'Too short (' + tLen + '/' + plat.optMin + ' min recommended)'; charStatus.className = 'warn'; }
    } else if(tLen > plat.optMax && tLen <= plat.max){
      if(charStatus) { charStatus.textContent = 'Good (may truncate on mobile)'; charStatus.className = 'ok'; }
    } else if(tLen > plat.max){
      if(charStatus) { charStatus.textContent = 'Exceeds platform limit of ' + plat.max; charStatus.className = 'bad'; }
    } else {
      if(charStatus) { charStatus.textContent = 'Optimal length for mobile search'; charStatus.className = 'ok'; }
    }

    var findings = [];
    var score = 100;

    BANNED_PATTERNS.forEach(function(item){
      var matches = fullText.match(item.regex);
      if(matches && matches.length > 0){
        var seen = {};
        matches.forEach(function(m){
          var lower = m.toLowerCase();
          if(!seen[lower]){
            seen[lower] = true;
            findings.push({
              word: lower,
              severity: item.sev,
              reason: item.reason,
              fix: item.fix
            });
            score -= Math.round((item.sev === 'critical' ? 25 : 12) * prof.mult);
          }
        });
      }
    });

    /* category-specific watch list — only risky in this profile */
    (prof.watch || []).forEach(function(item){
      var matches = fullText.match(item.regex);
      if(matches && matches.length > 0){
        var seen = {};
        matches.forEach(function(m){
          var lower = m.toLowerCase();
          if(!seen[lower]){
            seen[lower] = true;
            findings.push({
              word: lower,
              severity: 'warning',
              reason: prof.label + ' category: ' + item.reason,
              fix: item.fix
            });
            score -= Math.round(12 * prof.mult);
          }
        });
      }
    });

    var letters = title.replace(/[^a-zA-Z]/g, '');
    if(letters.length > 10){
      var uppers = letters.replace(/[^A-Z]/g, '').length;
      if(uppers / letters.length > 0.45){
        findings.push({
          word: 'EXCESSIVE ALL-CAPS',
          severity: 'warning',
          reason: 'Over 45% uppercase letters detected. Marketplace search algorithms penalize titles written in ALL-CAPS as spam.',
          fix: 'Capitalize each word normally'
        });
        score -= 10;
      }
    }

    if(tLen < 30) score -= 20;
    else if(tLen > plat.max) score -= 30;

    score = Math.max(0, Math.min(100, score));
    lastFindings = findings;
    lastScore = score;

    if(scoreNum) scoreNum.textContent = score;
    var dial = document.getElementById('score-dial');
    if(dial){
      if(score >= 80) dial.style.borderColor = '#22c55e';
      else if(score >= 50) dial.style.borderColor = '#eab308';
      else dial.style.borderColor = '#dc2626';
    }

    if(scoreStatus){
      if(score >= 85) scoreStatus.textContent = 'Compliant & Search Ready';
      else if(score >= 50) scoreStatus.textContent = 'Needs Revision — Bot Risk';
      else scoreStatus.textContent = 'Critical Policy Violations Detected';
    }

    if(scoreDesc){
      if(score >= 85) scoreDesc.textContent = 'High search friendliness with zero flagged triggers.';
      else if(score >= 50) scoreDesc.textContent = 'Contains words that may reduce search ranking or trigger manual review.';
      else scoreDesc.textContent = 'High probability of immediate listing takedown, shadow-ban, or violation penalty point.';
    }

    if(findingsSummary){
      findingsSummary.textContent = findings.length + ' item(s) found';
    }

    if(findingsList){
      if(findings.length === 0){
        findingsList.innerHTML = '<div class="flag-item safe"><div class="flag-head"><span>Clean Listing</span><span class="flag-tag">Safe</span></div><div class="flag-msg">No prohibited medical claims, banned superlatives, or formatting policy flags were detected. Your listing is safe to publish!</div></div>';
      } else {
        var html = '';
        var sevRank = { critical: 0, warning: 1 };
        findings.slice().sort(function(a, b){ return (sevRank[a.severity] || 2) - (sevRank[b.severity] || 2); }).forEach(function(f){
          html += '<div class="flag-item ' + f.severity + '">';
          html += '<div class="flag-head"><span>Found: \"' + f.word.toUpperCase() + '\"</span><span class="flag-tag">' + f.severity + '</span></div>';
          html += '<div class="flag-msg">' + f.reason + '</div>';
          if(f.fix){
            var safeWord = f.word.replace(/'/g, "\\'");
            var safeFix = f.fix.replace(/'/g, "\\'");
            html += '<button class="flag-fix" type="button" onclick="window.replaceWord(\'' + safeWord + '\', \'' + safeFix + '\')">Suggested Safe Alternative: ' + f.fix + ' &rarr;</button>';
          }
          html += '</div>';
        });
        findingsList.innerHTML = html;
      }
    }
  }

  window.replaceWord = function(oldW, newW){
    if(!titleEl) return;
    var re = new RegExp('\\b' + oldW + '\\b', 'gi');
    titleEl.value = titleEl.value.replace(re, newW);
    audit();
    showToast('Replaced "' + oldW + '" with compliant alternative');
  };

  function sanitizeField(el, fixCasing){
    if(!el || !el.value.trim()) return false;
    var before = el.value;
    var val = before;
    BANNED_PATTERNS.forEach(function(item){
      if(item.fix !== undefined){
        val = val.replace(item.regex, item.fix ? item.fix : '');
      }
    });
    val = val.replace(/\s{2,}/g, ' ').trim();
    if(fixCasing){
      var letters = val.replace(/[^a-zA-Z]/g, '');
      if(letters.length > 10 && (letters.replace(/[^A-Z]/g, '').length / letters.length) > 0.5){
        val = val.toLowerCase().replace(/\b[a-z]/g, function(c){ return c.toUpperCase(); });
      }
    }
    el.value = val;
    return val !== before;
  }

  function sanitizeTitle(){
    var titleChanged = sanitizeField(titleEl, true);
    var descChanged = sanitizeField(descEl, false);
    audit();
    if(!titleChanged && !descChanged){
      showToast('No flagged words found in title or description.');
    } else if(titleChanged && descChanged){
      showToast('Title and description both sanitized!');
    } else if(descChanged){
      showToast('Description sanitized! (title had no violations)');
    } else {
      showToast('Title sanitized!');
    }
  }

  function loadSample(quiet){
    if(!titleEl) return;
    titleEl.value = 'K-PICK Sungshim Blood Glucose Monitoring System Set 100 Strips FDA Approved 100% Guaranteed Cure Best Whitening Formula';
    if(descEl) descEl.value = 'Number 1 best seller in the Philippines! Lowest price guaranteed. PM me on Viber/WhatsApp for bulk COD discount.';
    audit();
    if(!quiet) showToast('Loaded sample with realistic policy violations');
  }

  /* ---- copy a findings report ------------------------------------------- */
  function buildReport(){
    var plat = limits[currentPlat];
    var prof = activeProfile();
    var title = titleEl ? titleEl.value : '';
    var lines = [];
    lines.push('LISTING COMPLIANCE & SEO REPORT');
    lines.push('Platform: ' + plat.name + '  |  Category: ' + prof.label);
    lines.push('Title length: ' + title.length + ' / ' + plat.max
               + ' chars (optimal ' + plat.optMin + '-' + plat.optMax + ')');
    lines.push('Compliance score: ' + (lastScore === null ? 'not scanned' : lastScore + ' / 100'));
    lines.push('');
    lines.push('TITLE');
    lines.push(title || '(empty)');
    lines.push('');
    if(!lastFindings.length){
      lines.push('FINDINGS: none — no prohibited claims, banned superlatives or formatting flags detected.');
    } else {
      lines.push('FINDINGS (' + lastFindings.length + ')');
      lastFindings.forEach(function(f, i){
        lines.push((i + 1) + '. [' + f.severity.toUpperCase() + '] "' + f.word + '"');
        lines.push('   Why: ' + f.reason);
        if(f.fix) lines.push('   Use instead: ' + f.fix);
      });
    }
    lines.push('');
    lines.push('Generated with SellerGuard - jamielyn-ludovice.vercel.app/tools');
    return lines.join('\n');
  }

  function copyReport(){
    if(!titleEl || !titleEl.value.trim()){
      showToast('Nothing to report yet — paste a listing first.');
      return;
    }
    var text = buildReport();
    if(navigator.clipboard){
      navigator.clipboard.writeText(text).then(function(){
        showToast('Findings report copied — paste it into an email or chat.');
      });
    } else {
      showToast('Report ready, but this browser blocked the clipboard.');
    }
  }

  /* ---- remember the user's inputs between visits ------------------------- */
  var STORE_KEY = 'sellerguard-v2';
  var AE_IDS = ['ae-price','ae-cogs','ae-fee','ae-ad-order','ae-mon-rev','ae-mon-ad'];
  var VS_IDS = ['vs-regular','vs-cogs','vs-flash','vs-store','vs-comm','vs-target'];

  function readVals(ids){
    return ids.map(function(id){
      var e = document.getElementById(id);
      return e ? e.value : '';
    });
  }

  function writeVals(ids, vals){
    if(!vals) return;
    ids.forEach(function(id, i){
      var e = document.getElementById(id);
      if(e && vals[i] !== undefined) e.value = vals[i];
    });
  }

  var restoring = false;
  function saveState(){
    if(restoring) return;
    try{
      localStorage.setItem(STORE_KEY, JSON.stringify({
        plat: currentPlat,
        cat: catEl ? catEl.value : 'general',
        title: titleEl ? titleEl.value : '',
        desc: descEl ? descEl.value : '',
        tags: etsyTagsEl ? etsyTagsEl.value : '',
        meta: shopifyMetaEl ? shopifyMetaEl.value : '',
        ae: readVals(AE_IDS),
        vs: readVals(VS_IDS)
      }));
    }catch(e){ /* private mode or storage full - not worth interrupting the user */ }
  }

  function restoreState(){
    var s = null;
    try{ s = JSON.parse(localStorage.getItem(STORE_KEY) || 'null'); }catch(e){ s = null; }
    if(!s) return false;
    restoring = true;
    if(s.plat && limits[s.plat]){
      currentPlat = s.plat;
      platBtns.forEach(function(b){
        b.classList.remove('on');
        if(b.dataset.plat === s.plat) b.classList.add('on');
      });
    }
    if(catEl && s.cat) catEl.value = s.cat;
    if(titleEl && s.title) titleEl.value = s.title;
    if(descEl && s.desc) descEl.value = s.desc;
    if(etsyTagsEl && s.tags) etsyTagsEl.value = s.tags;
    if(shopifyMetaEl && s.meta) shopifyMetaEl.value = s.meta;
    writeVals(AE_IDS, s.ae);
    writeVals(VS_IDS, s.vs);
    restoring = false;
    return !!(s.title || s.desc);
  }

  function clearSaved(){
    try{ localStorage.removeItem(STORE_KEY); }catch(e){}
  }

  if(etsyTagsEl) etsyTagsEl.addEventListener('input', auditEtsyTags);
  if(shopifyMetaEl) shopifyMetaEl.addEventListener('input', auditShopifyMeta);

  function copyText(){
    if(!titleEl || !titleEl.value.trim()){
      showToast('Nothing to copy!');
      return;
    }
    if(navigator.clipboard){
      navigator.clipboard.writeText(titleEl.value).then(function(){
        showToast('Clean title copied to clipboard!');
      });
    } else {
      showToast('Title copied!');
    }
  }

  function clearAll(){
    if(titleEl) titleEl.value = '';
    if(descEl) descEl.value = '';
    if(etsyTagsEl) etsyTagsEl.value = '';
    if(shopifyMetaEl) shopifyMetaEl.value = '';
    audit();       // repaint first - audit() re-saves, so wipe storage after it
    clearSaved();
    showToast('Cleared — including the copy saved in this browser.');
  }

  platBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      platBtns.forEach(function(b){ b.classList.remove('on'); });
      btn.classList.add('on');
      currentPlat = btn.dataset.plat || 'sea';
      updateConditionalFields();
      audit();
    });
  });
  updateConditionalFields();

  if(titleEl) titleEl.addEventListener('input', audit);
  if(descEl) descEl.addEventListener('input', audit);
  if(catEl) catEl.addEventListener('change', audit);

  var btnFix = document.getElementById('btn-fix');
  if(btnFix) btnFix.addEventListener('click', sanitizeTitle);

  var btnSample = document.getElementById('btn-sample');
  if(btnSample) btnSample.addEventListener('click', loadSample);

  var btnCopy = document.getElementById('btn-copy');
  if(btnCopy) btnCopy.addEventListener('click', copyText);

  var btnReport = document.getElementById('btn-report');
  if(btnReport) btnReport.addEventListener('click', copyReport);

  var btnClear = document.getElementById('btn-clear');
  if(btnClear) btnClear.addEventListener('click', clearAll);

  /* keep the highlight layer aligned while the textarea scrolls */
  if(titleEl && titleHl) titleEl.addEventListener('scroll', function(){ titleHl.scrollTop = titleEl.scrollTop; });
  if(descEl && descHl) descEl.addEventListener('scroll', function(){ descHl.scrollTop = descEl.scrollTop; });

  /* ---- suite tab switcher ----------------------------------------------- */
  var suiteTabs = document.querySelectorAll('.suite-tab');
  var suitePanels = document.querySelectorAll('.suite-panel');
  suiteTabs.forEach(function(tab){
    tab.addEventListener('click', function(){
      suiteTabs.forEach(function(t){ t.classList.remove('on'); });
      suitePanels.forEach(function(p){ p.classList.remove('on'); });
      tab.classList.add('on');
      var target = document.getElementById(tab.dataset.tab);
      if(target) target.classList.add('on');
    });
  });

  /* ---- Module 2: Ad Efficiency & TACOS Calculator ------------------------ */
  function num(id){
    var el = document.getElementById(id);
    var v = el ? parseFloat(el.value) : NaN;
    return isNaN(v) ? 0 : v;
  }

  function calcAdEfficiency(){
    var price   = num('ae-price');
    var cogs    = num('ae-cogs');
    var feePct  = num('ae-fee') / 100;
    var adOrder = num('ae-ad-order');
    var monRev  = num('ae-mon-rev');
    var monAd   = num('ae-mon-ad');

    var feeAmt = price * feePct;
    var grossContribution = price - cogs - feeAmt;               // before ad spend
    var contribMargin = grossContribution - adOrder;              // after ad spend
    var contribMarginPct = price > 0 ? (contribMargin / price) * 100 : 0;

    var tacos, tacosNote;
    if(monRev > 0 && monAd > 0){
      tacos = (monAd / monRev) * 100;
      tacosNote = 'From monthly figures';
    } else if(price > 0 && adOrder > 0){
      tacos = (adOrder / price) * 100;
      tacosNote = 'Per-order estimate';
    } else {
      tacos = 0; tacosNote = 'Enter figures above';
    }

    var breakevenRoas = grossContribution > 0 ? (price / grossContribution) : 0;
    var actualRoas = adOrder > 0 ? (price / adOrder) : 0;
    var healthy = grossContribution > 0 && (adOrder === 0 || actualRoas >= breakevenRoas) && contribMargin >= 0;

    setText('ae-margin-val', '₱' + contribMargin.toFixed(2));
    setText('ae-margin-sub', contribMarginPct.toFixed(1) + '% of selling price');
    setText('ae-tacos-val', tacos.toFixed(1) + '%');
    setText('ae-tacos-sub', tacosNote);
    setText('ae-roas-val', breakevenRoas > 0 ? breakevenRoas.toFixed(2) + 'x' : '—');
    setText('ae-roas-sub', 'Minimum ROAS to avoid a loss');
    setStatus('ae-status-val', 'ae-status-box', healthy,
      healthy ? 'Healthy & Profitable' : 'Ad Spend Bleeding / High Risk');
    saveState();
  }

  function setText(id, val){
    var el = document.getElementById(id);
    if(el) el.textContent = val;
  }

  function setStatus(valId, boxId, healthy, label){
    var v = document.getElementById(valId);
    var b = document.getElementById(boxId);
    if(v) v.textContent = label;
    if(b){
      b.style.color = healthy ? '#4ade80' : '#f87171';
      b.style.borderColor = healthy ? 'rgba(34,197,94,.45)' : 'rgba(220,38,38,.45)';
      b.style.background = healthy ? 'rgba(34,197,94,.08)' : 'rgba(220,38,38,.08)';
    }
  }

  ['ae-price','ae-cogs','ae-fee','ae-ad-order','ae-mon-rev','ae-mon-ad'].forEach(function(id){
    var el = document.getElementById(id);
    if(el) el.addEventListener('input', calcAdEfficiency);
  });

  /* ---- Module 3: Campaign Voucher & Margin Simulator --------------------- */
  function calcVoucherSim(){
    var regular  = num('vs-regular');
    var cogs     = num('vs-cogs');
    var flashPct = num('vs-flash') / 100;
    var storePct = num('vs-store') / 100;
    var commPct  = num('vs-comm') / 100;
    var target   = num('vs-target');

    var afterFlash = regular * (1 - flashPct);
    var finalPrice = afterFlash * (1 - storePct);
    var netPayout  = finalPrice * (1 - commPct);
    var netMargin  = netPayout - cogs;
    var negative   = netMargin < 0;

    setText('vs-final-val', '₱' + finalPrice.toFixed(2));
    setText('vs-final-sub', 'What the buyer pays at checkout');
    setText('vs-payout-val', '₱' + netPayout.toFixed(2));
    setText('vs-payout-sub', 'After platform commission');
    setText('vs-margin-val', '₱' + netMargin.toFixed(2));
    setText('vs-margin-sub', negative ? 'Below product cost' : 'Above product cost');

    /* Reverse solve: deepest TOTAL discount that still clears cost + target margin.
       netPayout = regular * (1 - d) * (1 - comm)  and  netPayout - cogs >= target   */
    var maxD = null;
    if(regular > 0 && (1 - commPct) > 0){
      maxD = 1 - ((cogs + target) / (regular * (1 - commPct)));
    }
    var appliedD = 1 - (1 - flashPct) * (1 - storePct);
    if(maxD === null){
      setText('vs-max-val', '—');
      setText('vs-max-sub', 'Enter a regular price first');
    } else if(maxD <= 0){
      setText('vs-max-val', '0%');
      setText('vs-max-sub', 'Even at full price you miss the target');
    } else {
      setText('vs-max-val', (maxD * 100).toFixed(1) + '%');
      setText('vs-max-sub', 'Flash + voucher combined · now at ' + (appliedD * 100).toFixed(1) + '%');
    }

    setStatus('vs-status-val', 'vs-status-box', !negative,
      negative ? 'Negative Margin Alert!' : 'Healthy Margin');
    saveState();
  }

  VS_IDS.forEach(function(id){
    var el = document.getElementById(id);
    if(el) el.addEventListener('input', calcVoucherSim);
  });

  var vsPreset = document.getElementById('vs-preset');
  if(vsPreset){
    vsPreset.addEventListener('change', function(){
      var v = vsPreset.value;
      if(!v) return;
      var commEl = document.getElementById('vs-comm');
      if(commEl){
        commEl.value = v;
        calcVoucherSim();
        showToast('Commission set to ' + v + '% — double-check it in your Seller Centre.');
      }
    });
  }

  /* Boot: bring back whatever they were working on, otherwise show a worked
     example so the panels are never blank on a first visit. */
  var hadSaved = restoreState();
  updateConditionalFields();
  if(!hadSaved){
    loadSample(true);
    var aeDefaults = ['799', '320', '8', '90', '250000', '35000'];
    var vsDefaults = ['999', '420', '20', '10', '6', '0'];
    AE_IDS.forEach(function(id, i){
      var e = document.getElementById(id);
      if(e && !e.value) e.value = aeDefaults[i];
    });
    VS_IDS.forEach(function(id, i){
      var e = document.getElementById(id);
      if(e && !e.value) e.value = vsDefaults[i];
    });
  }

  /* ---- Module 4: Marketplace Audit Scorecard ---------------------------- */
  var AUDIT_PLATFORM_CONFIG = {
    amazon:  { name: 'Amazon', optMin: 150, optMax: 200, max: 200, minDesc: 300, minBullets: 3 },
    ebay:    { name: 'eBay',   optMin: 60,  optMax: 80,  max: 80,  minDesc: 200, minBullets: 2 },
    sea:     { name: 'Shopee & Lazada', optMin: 80, optMax: 120, max: 255, minDesc: 300, minBullets: 3 },
    tiktok:  { name: 'TikTok Shop', optMin: 80, optMax: 150, max: 200, minDesc: 250, minBullets: 2 },
    generic: { name: 'Generic Marketplace', optMin: 60, optMax: 150, max: 255, minDesc: 250, minBullets: 2 }
  };

  var AUDIT_SAMPLE_ROWS = [
    { sku: "AMZ-SERUM-01", title: "Snail Mucin 96% Hydrating Serum 100ml Advanced Repair Essence for Dry Sensitive Skin", description: "Infused with 96.3% snail secretion filtrate to deeply hydrate and repair dry damaged skin barriers. Lightweight soothing formula absorbs quickly without sticky residue. Paraben-free, sulfate-free, cruelty-free, and suitable for all sensitive skin types. Apply daily after facial toner for optimum dewy glow.", bullets: "Contains 96.3% filtered snail mucin\nDeep long-lasting hydration and barrier recovery\nFree from parabens, sulfates, and artificial fragrances\nLightweight non-greasy fast absorbing texture", price: "22.99", images: "img1.jpg, img2.jpg, img3.jpg, img4.jpg, img5.jpg, img6.jpg", reviews: "348", rating: "4.7", category: "Beauty & Personal Care", stock: "145", sales: "820" },
    { sku: "AMZ-PIL-02", title: "Ergonomic Memory Foam Lumbar Support Pillow for Office Chair and Car Seat Back Cushion", description: "Premium orthopedic high-density memory foam provides targeted lumbar and lower back pain relief during extended office working or driving sessions. Features 3D breathable washable mesh cover and dual adjustable elastic straps that secure tightly to any desk chair or vehicle seat.", bullets: "Ergonomic contoured spinal alignment curve\nHigh-density slow-rebound therapeutic memory foam\nBreathable machine-washable mesh zipper cover\nDual adjustable heavy-duty chair straps", price: "34.50", images: "p1.jpg, p2.jpg, p3.jpg, p4.jpg, p5.jpg", reviews: "120", rating: "4.5", category: "Home & Office", stock: "80", sales: "310" },
    { sku: "AMZ-SPK-03", title: "PORTABLE BLUETOOTH SPEAKER WATERPROOF", description: "Waterproof wireless speaker for outdoor travel and shower with bass sound.", bullets: "Bluetooth 5.0", price: "19.99", images: "spk1.jpg, spk2.jpg", reviews: "8", rating: "3.9", category: "Electronics", stock: "24", sales: "15" },
    { sku: "AMZ-BOT-04", title: "Stainless Steel Insulated Water Bottle 24oz Double Wall Vacuum Flask with Straw Lid and Spout", description: "Keep beverages ice cold for up to 24 hours or piping hot for 12 hours with our triple-layer copper insulation technology. Crafted from food-grade 18/8 stainless steel that will never rust or leave a metallic aftertaste. Includes 2 leak-proof lids: one silicone flip straw lid and one fast-flow chug spout lid with wide carry loop.", bullets: "Vacuum double wall temperature insulation\n18/8 food-grade pro stainless steel\nIncludes 2 interchangeable leak-proof sports lids\nSweat-free powder coat exterior finish", price: "26.00", images: "b1.jpg, b2.jpg, b3.jpg, b4.jpg, b5.jpg, b6.jpg, b7.jpg", reviews: "215", rating: "4.6", category: "Kitchen & Dining", stock: "110", sales: "540" },
    { sku: "AMZ-TEA-05", title: "Organic Green Tea Extract Capsules 500mg 100% Guaranteed Miracle Cure For Fast Weight Loss", description: "Ultra strength green tea fat burner guaranteed to cure digestive ailments and burn fat fast in 7 days without diet or exercise. FDA Approved formula with miracle natural herbs.", bullets: "Fat burner\nWeight loss\nDiet pills", price: "18.50", images: "t1.jpg, t2.jpg, t3.jpg", reviews: "14", rating: "3.6", category: "Health & Supplements", stock: "55", sales: "90" },
    { sku: "AMZ-BRD-06", title: "Bamboo Cutting Board Set with Deep Juice Groove 3-Piece Kitchen Chopping Blocks for Meat and Veggies", description: "Organic moso bamboo cutting boards designed for everyday culinary prep. Knife-friendly non-porous surface resists deep knife scarring, moisture absorption, and food odours. Features perimeter deep juice groove wells that catch excess liquid runoff to keep countertop workspaces clean and tidy.", bullets: "3 kitchen sizes: Small, Medium, Large prep boards\nBuilt-in perimeter liquid catch juice groove\nEco-friendly durable 100% organic moso bamboo\nReversible dual-sided chopping prep design", price: "29.99", images: "bb1.jpg, bb2.jpg, bb3.jpg, bb4.jpg, bb5.jpg", reviews: "89", rating: "4.4", category: "Kitchen & Dining", stock: "62", sales: "210" },
    { sku: "AMZ-MOU-07", title: "Wireless Vertical Mouse Ergonomic Optical Rechargeable with Adjustable DPI 800 1200 1600", description: "Scientific ergonomic vertical orientation encourages neutral healthy wrist handshake posture to prevent carpal tunnel strain and repetitive stress injury. Features silent click buttons, forward/back thumb navigation controls, built-in rechargeable lithium battery, and 2.4GHz USB nano receiver with 30ft range.", bullets: "Ergonomic 57-degree vertical handshake angle\nRechargeable USB-C lithium battery\n3 adjustable optical DPI precision levels\nPlug and play 2.4GHz lag-free wireless connection", price: "27.50", images: "m1.jpg, m2.jpg, m3.jpg, m4.jpg, m5.jpg", reviews: "142", rating: "4.3", category: "Computers & Accessories", stock: "40", sales: "180" },
    { sku: "AMZ-BND-08", title: "Resistance Exercise Bands Set 5-Pack with Door Anchor and Carrying Bag for Home Workouts", description: "Five color-coded natural latex resistance loop bands providing graduated tension from extra-light 5 lbs to extra-heavy 30 lbs. Perfect for physical therapy rehabilitation, glute activation, yoga, Pilates, and strength training. Includes compact travel pouch and instructional exercise guide.", bullets: "5 resistance level loop bands\n100% eco-friendly natural snap-resistant latex\nIncludes door anchor and compact carry pouch\nIdeal for strength conditioning and physical therapy", price: "15.99", images: "rb1.jpg, rb2.jpg, rb3.jpg, rb4.jpg, rb5.jpg", reviews: "450", rating: "4.6", category: "Sports & Fitness", stock: "190", sales: "950" },
    { sku: "SEA-CRM-01", title: "Centella Asiatica Calming Facial Gel Cream 50g Light Moisturizer for Oily Blemish Prone Skin", description: "Formulated with 70% pure Centella Asiatica leaf water and tea tree oil to soothe redness, relieve irritated breakouts, and provide weightless hydration. Oil-free gel texture absorbs in seconds, balancing excess sebum production while leaving a soft matte finish without clogging pores. Dermatologically tested for sensitive skin.", bullets: "Contains 70% Centella Asiatica botanical extract\nLightweight oil-free cooling gel absorption\nCalms redness and active skin inflammation\nBalances oil and moisture barrier levels", price: "450.00", images: "c1.jpg, c2.jpg, c3.jpg, c4.jpg, c5.jpg, c6.jpg", reviews: "520", rating: "4.8", category: "Health & Beauty", stock: "210", sales: "1400" },
    { sku: "SEA-LOT-02", title: "Pampaputi Instant Whitening Lotion 250ml FDA Approved No. 1 Best Seller Miracle Glow", description: "Pinakamura whitening lotion 100% effective guaranteed result in 7 days permanent white skin. Anti-cancer herbal extracts cures all skin pigmentation and blemishes.", bullets: "Instant white\nLowest price guaranteed\nFDA certified", price: "280.00", images: "w1.jpg, w2.jpg", reviews: "32", rating: "3.7", category: "Health & Beauty", stock: "75", sales: "110" },
    { sku: "SEA-KNF-03", title: "Magnetic Kitchen Knife Strip Holder 16 Inch Stainless Steel Wall Mount Tool Bar", description: "Heavy-duty dual neodymium magnetic core securely holds kitchen chef knives, scissors, and metal tools. Satin-finished 304 stainless steel resists rust and wipes clean easily. Easy wall mounting with included hardware screws and heavy-duty adhesive tape.", bullets: "Continuous ultra-strong magnetic grip surface\nSatin brushed 304 food-grade stainless steel\nDual mounting options: screw mount or adhesive\nFrees up kitchen drawer and countertop space", price: "399.00", images: "k1.jpg, k2.jpg, k3.jpg, k4.jpg, k5.jpg", reviews: "64", rating: "4.4", category: "Home & Living", stock: "50", sales: "180" },
    { sku: "SEA-MUG-04", title: "Minimalist Matte Ceramic Coffee Mug 350ml Heat Resistant Nordic Cup with Wooden Handle", description: "Handcrafted stoneware coffee mug featuring a contemporary matte glaze finish and ergonomic natural solid wood handle that stays cool to touch. 350ml capacity holds hot drip coffee, latte, tea, or cocoa. Lead-free and food-safe ceramic construction.", bullets: "Modern Nordic minimalist aesthetic\nInsulating natural solid beechwood handle\n350ml capacity for coffee, tea, and warm drinks\nDurable chip-resistant matte stoneware body", price: "249.00", images: "mg1.jpg, mg2.jpg, mg3.jpg, mg4.jpg, mg5.jpg", reviews: "88", rating: "4.5", category: "Home & Living", stock: "95", sales: "230" },
    { sku: "SEA-TWL-05", title: "Microfiber Quick Dry Gym Fitness Towel 3-Pack Lightweight Absorbent Travel Towel", description: "Ultra-fine microfiber waffle weave absorbs 4 times its weight in moisture and dries 3 times faster than conventional cotton terry cloth. Soft, compact, and lightweight with an integrated snap hanging loop. Machine washable and odor resistant.", bullets: "Includes 3 multi-size towels: Face, Hand, Gym\nFast drying breathable microfiber waffle weave\nSnap loop for easy hanging on exercise equipment\nUltra-compact fold fits gym bags and backpacks", price: "320.00", images: "tw1.jpg, tw2.jpg, tw3.jpg, tw4.jpg, tw5.jpg", reviews: "175", rating: "4.6", category: "Sports & Outdoors", stock: "130", sales: "610" },
    { sku: "SEA-POT-06", title: "Air Fryer Silicone Pot Liner Reusable Non-Stick Round Baking Basket Tray 8 Inch", description: "Food grade silicone baking tray designed for round air fryer baskets. Raised bottom ridges allow excess oil and grease to drain away from food for crispier results. Withstands heat up to 240C and dishwasher safe.", bullets: "Food safe heat resistant silicone up to 240C\nElevated bottom lines for oil drainage\nNon-stick easy rinse dishwasher safe\nSaves air fryer basket from grease buildup", price: "180.00", images: "pt1.jpg, pt2.jpg, pt3.jpg, pt4.jpg", reviews: "42", rating: "4.1", category: "Home & Living", stock: "60", sales: "120" },
    { sku: "SEA-MED-07", title: "Herbal Cough Syrup Direct Transaction PM is the key Viber WhatsApp Fast Delivery", description: "Contact us directly on Viber or WhatsApp to order. Cures asthma and lung inflammation 100% original authentic formula.", bullets: "PM me for discount\nFree delivery", price: "350.00", images: "sy1.jpg", reviews: "2", rating: "2.8", category: "Health & Beauty", stock: "10", sales: "5" },
    { sku: "SEA-LPT-08", title: "Foldable Laptop Stand Aluminum Ergonomic Riser 6-Level Height Adjustable Portable Holder", description: "Engineered from aircraft-grade aluminum alloy with silicone anti-slip pads to protect laptops up to 15.6 inches. 6 ergonomic tilt angle adjustments from 15 to 45 degrees improve posture and neck comfort while open-frame hollow design promotes rapid laptop heat dissipation.", bullets: "6 adjustable viewing angle ergonomic levels\nSolid lightweight aluminum alloy construction\nNon-slip silicone cushioning pads and hook stops\nFolds flat into portable pocket sleeve", price: "299.00", images: "lp1.jpg, lp2.jpg, lp3.jpg, lp4.jpg, lp5.jpg", reviews: "310", rating: "4.7", category: "Computers & Laptops", stock: "180", sales: "890" },
    { sku: "SEA-MCH-09", title: "Matcha Powder Culinary Grade 100g Pure Japanese Green Tea for Latte and Baking", description: "Finely ground from first-harvest green tea leaves. Rich in antioxidants and L-theanine for sustained natural energy without caffeine jitters. Perfect for whisking iced matcha lattes, smoothies, pastries, and ice cream.", bullets: "100% pure stone-ground culinary matcha\nRich vibrant green color and savory umami notes\nResealable foil pouch preserves fresh aroma\nZero added sugars, dairy, or preservatives", price: "420.00", images: "mc1.jpg, mc2.jpg, mc3.jpg, mc4.jpg, mc5.jpg", reviews: "94", rating: "4.5", category: "Groceries", stock: "70", sales: "240" },
    { sku: "TTS-LIP-01", title: "Hydrating Tinted Lip Glow Oil Plumping Formula Nourishing Berry Glaze 6ml", description: "Non-sticky high-shine lip oil enriched with cherry seed oil and vitamin E to nourish dry lips while delivering a translucent wash of plumping berry tint. Features oversized plush applicator wand that coats lips in a single swipe with long-lasting glass-like mirror shine.", bullets: "High-shine mirror finish with subtle plumping effect\nInfused with nourishing cherry oil and vitamin E\nOversized doe-foot wand for effortless application\nNon-greasy, non-sticky comfortable hydration", price: "189.00", images: "lip1.jpg, lip2.jpg, lip3.jpg, lip4.jpg, lip5.jpg, lip6.jpg", reviews: "890", rating: "4.8", category: "Beauty", stock: "450", sales: "3200" },
    { sku: "TTS-ORG-02", title: "Aesthetic Acrylic Desk Organizer Pen Holder 4-Grid Multi-Functional Stationery Storage Box", description: "Crystal clear premium acrylic desk caddy with 4 divided compartments for pens, highlighters, scissors, and makeup brushes. Thick heavy-duty polished edge construction keeps desktop workstations organized and aesthetically pleasing.", bullets: "4 spacious separated storage compartments\nCrystal clear shatter-resistant polished acrylic\nMultipurpose for stationery, cosmetics, or remotes\nNon-slip silicone rubber bottom base feet", price: "159.00", images: "org1.jpg, org2.jpg, org3.jpg, org4.jpg, org5.jpg", reviews: "140", rating: "4.5", category: "Stationery", stock: "85", sales: "410" },
    { sku: "TTS-PRN-03", title: "Mini Thermal Pocket Sticker Printer Bluetooth Wireless Inkless Printing with 5 Paper Rolls", description: "Pocket-sized wireless label and note printer connects instantly via Bluetooth to iOS and Android companion app. Uses thermal heating technology — requires zero ink, toner, or ribbons. Print study flashcards, shopping lists, receipts, and scrapbooking photo stickers anywhere.", bullets: "Inkless thermal printing technology\nBluetooth wireless connectivity for iOS and Android\nIncludes 5 rolls of white thermal sticker paper\nBuilt-in rechargeable 1000mAh lithium battery", price: "599.00", images: "pr1.jpg, pr2.jpg, pr3.jpg, pr4.jpg, pr5.jpg", reviews: "260", rating: "4.6", category: "Gadgets", stock: "60", sales: "780" },
    { sku: "TTS-PCH-04", title: "Hydrocolloid Pimple Spot Patches 36ct Invisible Blemish Covers Fast Acting Overnight Care", description: "Medical-grade hydrocolloid stickers absorb pus, oil, and impurities from active blemishes while protecting breakouts from picking, dirt, and bacteria. Ultra-thin translucent tapered edges blend seamlessly into all skin tones under makeup or overnight.", bullets: "36 multi-size patches (8mm and 12mm)\nAbsorbs impurities and flattens breakouts overnight\nInvisible matte finish suitable under makeup\nDrug-free and non-drying for sensitive skin", price: "120.00", images: "pch1.jpg, pch2.jpg, pch3.jpg, pch4.jpg, pch5.jpg", reviews: "410", rating: "4.7", category: "Beauty", stock: "320", sales: "1850" },
    { sku: "TTS-LMP-05", title: "Sunset Projection Lamp Romantic LED Night Light 16 Colors Remote Control 360 Rotation", description: "Atmospheric projection lamp for bedroom photography.", bullets: "16 RGB colors", price: "249.00", images: "lmp1.jpg, lmp2.jpg, lmp3.jpg", reviews: "19", rating: "3.8", category: "Lighting", stock: "15", sales: "45" },
    { sku: "TTS-SCALP-06", title: "Silicone Scalp Massager Shampoo Brush Soft Bristle Exfoliating Head Scrubber for All Hair Types", description: "Ergonomic manual scalp cleansing brush equipped with flexible silicone bristles that gently stimulate blood circulation, unclog hair follicles, and evenly distribute shampoo. Suitable for thick, fine, curly, or color-treated hair.", bullets: "Soft flexible thick silicone bristles\nErgonomic palm grip with non-slip handle\nPromotes scalp circulation and lather distribution\nSafe for wet shampooing or dry scalp massage", price: "99.00", images: "sc1.jpg, sc2.jpg, sc3.jpg, sc4.jpg, sc5.jpg", reviews: "380", rating: "4.6", category: "Personal Care", stock: "140", sales: "1100" },
    { sku: "TTS-COL-07", title: "Collagen Peptide Drink", description: "Collagen drink for skin.", bullets: "", price: "0", images: "", reviews: "0", rating: "0", category: "Beverages", stock: "0", sales: "0" },
    { sku: "TTS-MNT-08", title: "Magnetic Phone Car Mount 360 Degree Rotation Dashboard Air Vent Magnet Holder Strong Grip", description: "Equipped with 6 strong N52 neodymium magnets to securely grip any smartphone through road vibrations, bumps, and sharp turns. Includes adhesive metal plates and dual-mounting clips for air vent fins or dashboard placement.", bullets: "6 heavy-duty N52 neodymium magnets\n360-degree ball joint swivel viewing angle\nDual mount options: dashboard or air vent\nOne-handed quick snap docking and release", price: "199.00", images: "mnt1.jpg, mnt2.jpg, mnt3.jpg, mnt4.jpg, mnt5.jpg", reviews: "165", rating: "4.4", category: "Auto Accessories", stock: "75", sales: "520" }
  ];

  function parseCSV(text) {
    var lines = [];
    var row = [];
    var inQuotes = false;
    var current = '';
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      var next = text[i + 1];
      if (c === '"') {
        if (inQuotes && next === '"') {
          current += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if ((c === ',' || c === '\t') && !inQuotes) {
        row.push(current.trim());
        current = '';
      } else if ((c === '\r' || c === '\n') && !inQuotes) {
        if (c === '\r' && next === '\n') { i++; }
        row.push(current.trim());
        if (row.some(function(cell) { return cell.length > 0; })) {
          lines.push(row);
        }
        row = [];
        current = '';
      } else {
        current += c;
      }
    }
    if (current.length > 0 || row.length > 0) {
      row.push(current.trim());
      if (row.some(function(cell) { return cell.length > 0; })) {
        lines.push(row);
      }
    }
    if (lines.length < 2) return [];
    var headers = lines[0].map(function(h) { return h.replace(/^["']|["']$/g, '').trim().toLowerCase(); });
    var result = [];
    for (var r = 1; r < lines.length; r++) {
      var rData = lines[r];
      var obj = {};
      headers.forEach(function(h, idx) {
        obj[h] = (rData[idx] !== undefined ? rData[idx] : '').replace(/^["']|["']$/g, '').trim();
      });
      result.push(obj);
    }
    return result;
  }

  function mapRowToProduct(raw) {
    var keys = Object.keys(raw);
    function find(regex) {
      for (var i = 0; i < keys.length; i++) {
        if (regex.test(keys[i])) return raw[keys[i]];
      }
      return '';
    }
    var sku = find(/^(sku|seller\s*sku|item\s*id|product\s*id|id)$/i) || find(/sku|item.*id/i) || 'SKU-' + Math.floor(1000 + Math.random()*9000);
    var title = find(/^(title|name|product\s*name|listing\s*title)$/i) || find(/title|name/i) || 'Untitled Product';
    var desc = find(/^(description|body|details|desc|product\s*description)$/i) || find(/desc/i) || '';
    var bullets = find(/^(bullets|bullet\s*points|key\s*features|features|highlights)$/i) || find(/bullet|feature/i) || '';
    var priceStr = find(/^(price|sale\s*price|listing\s*price|retail\s*price|unit\s*price)$/i) || find(/price/i) || '0';
    var imagesStr = find(/^(images|image\s*count|main\s*image|image\s*urls?|photos?)$/i) || find(/image|photo/i) || '';
    var reviewsStr = find(/^(reviews|review\s*count|ratings|total\s*reviews)$/i) || find(/review/i) || '0';
    var ratingStr = find(/^(rating|avg\s*rating|stars|average\s*rating)$/i) || find(/rating|star/i) || '0';
    var category = find(/^(category|product\s*category|item\s*type)$/i) || find(/cat/i) || 'General';
    var stockStr = find(/^(stock|quantity|inventory|qty|available)$/i) || find(/stock|qty|inventory/i) || '0';
    var salesStr = find(/^(sales|units\s*sold|orders|sold)$/i) || find(/sold|sales|order/i) || '0';

    var imgCount = 0;
    if (/^\d+$/.test(imagesStr)) {
      imgCount = parseInt(imagesStr, 10);
    } else if (imagesStr) {
      var parts = imagesStr.split(/[,;|\n]+/).map(function(s){ return s.trim(); }).filter(Boolean);
      imgCount = parts.length > 0 ? parts.length : 1;
    }

    var bulletCount = 0;
    if (/^\d+$/.test(bullets)) {
      bulletCount = parseInt(bullets, 10);
    } else if (bullets) {
      var bParts = bullets.split(/[\n•\*\-]+/).map(function(s){ return s.trim(); }).filter(Boolean);
      bulletCount = bParts.length > 0 ? bParts.length : 1;
    }

    var price = parseFloat(priceStr.replace(/[^0-9.]/g, '')) || 0;
    var reviews = parseInt(reviewsStr.replace(/[^0-9]/g, ''), 10) || 0;
    var rating = parseFloat(ratingStr.replace(/[^0-9.]/g, '')) || 0;
    var stock = parseInt(stockStr.replace(/[^0-9\-]/g, ''), 10) || 0;
    var sales = parseInt(salesStr.replace(/[^0-9]/g, ''), 10) || 0;

    return {
      sku: sku,
      title: title,
      description: desc,
      bullets: bullets,
      bulletCount: bulletCount,
      price: price,
      images: imagesStr,
      imageCount: imgCount,
      reviews: reviews,
      rating: rating,
      category: category,
      stock: stock,
      sales: sales
    };
  }

  function scoreSKU(prod, platformKey) {
    var cfg = AUDIT_PLATFORM_CONFIG[platformKey] || AUDIT_PLATFORM_CONFIG.sea;
    var checks = [];
    var totalScore = 0;

    // 1. Title length (15 pts)
    var tLen = prod.title.length;
    var tPts = 0, tStatus = 'fail', tFix = '';
    if (tLen >= cfg.optMin && tLen <= cfg.optMax) {
      tPts = 15; tStatus = 'pass';
      tFix = 'Optimal title length (' + tLen + ' chars).';
    } else if (tLen > cfg.max) {
      tPts = 0; tStatus = 'fail';
      tFix = 'Title (' + tLen + ' chars) exceeds ' + cfg.name + ' hard cap of ' + cfg.max + ' chars. Shorten to ' + cfg.optMin + '–' + cfg.optMax + ' chars.';
    } else if (tLen < cfg.optMin) {
      tPts = Math.round(15 * Math.max(0, tLen / cfg.optMin));
      tStatus = tPts >= 10 ? 'warn' : 'fail';
      tFix = 'Title is too short (' + tLen + ' chars). Expand with search keywords to reach ' + cfg.optMin + '–' + cfg.optMax + ' chars.';
    } else {
      tPts = 10; tStatus = 'warn';
      tFix = 'Title (' + tLen + ' chars) is outside optimal range (' + cfg.optMin + '–' + cfg.optMax + ').';
    }
    checks.push({ id: 'title_len', name: 'Title Length (' + cfg.name + ')', pts: tPts, max: 15, status: tStatus, fix: tFix, severity: 2 });
    totalScore += tPts;

    // 2. Title keywords & no ALL CAPS (10 pts)
    var words = prod.title.split(/\s+/).filter(Boolean);
    var upperWords = words.filter(function(w){ return w.length >= 3 && w === w.toUpperCase() && /[A-Z]/.test(w); });
    var isAllCaps = words.length > 2 && (upperWords.length / words.length) >= 0.5;
    var stopWords = /^(and|the|for|with|in|a|an|of|to|by|at|from|or|on)$/i;
    var keywordTokens = words.filter(function(w){ return !stopWords.test(w) && w.length >= 3; });
    var kwPts = 0, kwStatus = 'fail', kwFix = '';
    if (isAllCaps) {
      kwPts = 2; kwStatus = 'fail';
      kwFix = 'Title is written in ALL CAPS. Search algorithms penalize uppercase titles. Use standard Title Case.';
    } else if (keywordTokens.length >= 3) {
      kwPts = 10; kwStatus = 'pass';
      kwFix = 'Title contains ' + keywordTokens.length + ' descriptive keywords without uppercase spam.';
    } else {
      kwPts = 4; kwStatus = 'warn';
      kwFix = 'Title lacks keyword richness (' + keywordTokens.length + ' tokens found). Add key benefits, specs, or model variants.';
    }
    checks.push({ id: 'title_kw', name: 'Title Keywords & Casing', pts: kwPts, max: 10, status: kwStatus, fix: kwFix, severity: 2 });
    totalScore += kwPts;

    // 3. Description length (10 pts)
    var dLen = prod.description.length;
    var dPts = 0, dStatus = 'fail', dFix = '';
    if (dLen >= cfg.minDesc) {
      dPts = 10; dStatus = 'pass';
      dFix = 'Description contains ' + dLen + ' characters (meets ≥' + cfg.minDesc + ' target).';
    } else if (dLen > 0) {
      dPts = Math.round(10 * (dLen / cfg.minDesc));
      dStatus = 'warn';
      dFix = 'Description is brief (' + dLen + ' chars). Expand to ≥' + cfg.minDesc + ' chars covering features, specs, and FAQs.';
    } else {
      dPts = 0; dStatus = 'fail';
      dFix = 'Listing has no description. Add comprehensive copy (≥' + cfg.minDesc + ' chars) to convert search visits.';
    }
    checks.push({ id: 'desc_len', name: 'Description Depth', pts: dPts, max: 10, status: dStatus, fix: dFix, severity: 2 });
    totalScore += dPts;

    // 4. Bullets >= 3 (10 pts)
    var bCount = prod.bulletCount;
    var bPts = 0, bStatus = 'fail', bFix = '';
    if (bCount >= cfg.minBullets) {
      bPts = 10; bStatus = 'pass';
      bFix = 'Has ' + bCount + ' feature bullets for quick customer scanning.';
    } else if (bCount >= 1) {
      bPts = 5; bStatus = 'warn';
      bFix = 'Only ' + bCount + ' bullet points found. Add at least ' + cfg.minBullets + ' key feature bullets.';
    } else {
      bPts = 0; bStatus = 'fail';
      bFix = 'No structured bullet points found. Add ≥' + cfg.minBullets + ' bullet points summarizing benefits.';
    }
    checks.push({ id: 'bullets', name: 'Key Feature Bullets', pts: bPts, max: 10, status: bStatus, fix: bFix, severity: 1 });
    totalScore += bPts;

    // 5. Images >= 5 (15 pts)
    var imgPts = 0, imgStatus = 'fail', imgFix = '';
    if (prod.imageCount >= 5) {
      imgPts = 15; imgStatus = 'pass';
      imgFix = 'Has ' + prod.imageCount + ' images (meets best practice of ≥5 gallery slides).';
    } else if (prod.imageCount >= 3) {
      imgPts = 8; imgStatus = 'warn';
      imgFix = 'Listing has only ' + prod.imageCount + ' images. Listings with 5+ visual slides convert 2.4× higher.';
    } else if (prod.imageCount >= 1) {
      imgPts = 4; imgStatus = 'fail';
      imgFix = 'Only ' + prod.imageCount + ' image detected. Add at least 5 high-resolution slides.';
    } else {
      imgPts = 0; imgStatus = 'fail';
      imgFix = 'Missing product images. Listings without images are suppressed in search.';
    }
    checks.push({ id: 'images_count', name: 'Gallery Image Count (≥5)', pts: imgPts, max: 15, status: imgStatus, fix: imgFix, severity: 3 });
    totalScore += imgPts;

    // 6. Main image present (5 pts)
    var mainPts = prod.imageCount >= 1 ? 5 : 0;
    var mainStatus = mainPts === 5 ? 'pass' : 'fail';
    var mainFix = mainPts === 5 ? 'Main hero image is present.' : 'Missing main cover image. Upload a clear hero image on a clean background.';
    checks.push({ id: 'main_image', name: 'Hero Cover Image', pts: mainPts, max: 5, status: mainStatus, fix: mainFix, severity: 4 });
    totalScore += mainPts;

    // 7. Reviews >= 10 (10 pts)
    var revPts = 0, revStatus = 'fail', revFix = '';
    if (prod.reviews >= 10) {
      revPts = 10; revStatus = 'pass';
      revFix = prod.reviews + ' customer reviews establish baseline social proof.';
    } else if (prod.reviews >= 1) {
      revPts = 5; revStatus = 'warn';
      revFix = 'Only ' + prod.reviews + ' reviews. Run review request automations or flash vouchers to cross 10 reviews.';
    } else {
      revPts = 0; revStatus = 'fail';
      revFix = 'Zero customer reviews (cold-start risk). Implement post-purchase review incentives or promotional sampling.';
    }
    checks.push({ id: 'reviews_count', name: 'Social Proof (≥10 Reviews)', pts: revPts, max: 10, status: revStatus, fix: revFix, severity: 2 });
    totalScore += revPts;

    // 8. Rating >= 4.2 (5 pts)
    var ratPts = 0, ratStatus = 'fail', ratFix = '';
    if (prod.reviews === 0) {
      ratPts = 0; ratStatus = 'warn';
      ratFix = 'No reviews yet to determine customer satisfaction rating.';
    } else if (prod.rating >= 4.2) {
      ratPts = 5; ratStatus = 'pass';
      ratFix = 'Rating is ' + prod.rating.toFixed(1) + ' / 5.0 (meets high quality threshold ≥4.2).';
    } else if (prod.rating >= 3.8) {
      ratPts = 2; ratStatus = 'warn';
      ratFix = 'Rating is ' + prod.rating.toFixed(1) + ' / 5.0 (below 4.2 benchmark). Address quality feedback.';
    } else {
      ratPts = 0; ratStatus = 'fail';
      ratFix = 'Critical low rating (' + prod.rating.toFixed(1) + ' / 5.0). High return/demotion risk.';
    }
    checks.push({ id: 'rating_score', name: 'Star Rating (≥4.2 Stars)', pts: ratPts, max: 5, status: ratStatus, fix: ratFix, severity: 3 });
    totalScore += ratPts;

    // 9. Price > 0 (5 pts)
    var prcPts = prod.price > 0 ? 5 : 0;
    var prcStatus = prcPts === 5 ? 'pass' : 'fail';
    var prcFix = prcPts === 5 ? 'Valid price configured (' + prod.price.toFixed(2) + ').' : 'Price is missing or 0. Listing cannot convert.';
    checks.push({ id: 'price_valid', name: 'Active Selling Price', pts: prcPts, max: 5, status: prcStatus, fix: prcFix, severity: 4 });
    totalScore += prcPts;

    // 10. Stock > 0 (10 pts)
    var stkPts = prod.stock > 0 ? 10 : 0;
    var stkStatus = stkPts === 10 ? 'pass' : 'fail';
    var stkFix = stkPts === 10 ? 'Stock available (' + prod.stock + ' units).' : 'Out of stock! Listing loses algorithmic search rank daily when inactive.';
    checks.push({ id: 'stock_positive', name: 'Inventory Availability', pts: stkPts, max: 10, status: stkStatus, fix: stkFix, severity: 4 });
    totalScore += stkPts;

    // 11. Compliance: BANNED_PATTERNS (5 pts)
    var combinedText = (prod.title + ' ' + prod.description).toLowerCase();
    var violations = [];
    BANNED_PATTERNS.forEach(function(pat){
      pat.regex.lastIndex = 0;
      var m = combinedText.match(pat.regex);
      if (m && m.length > 0) {
        violations.push({ word: m[0], sev: pat.sev, reason: pat.reason, fix: pat.fix });
      }
    });
    var compPts = 5, compStatus = 'pass', compFix = 'No prohibited claims or policy violations detected.';
    if (violations.length > 0) {
      var hasCrit = violations.some(function(v){ return v.sev === 'critical'; });
      compPts = hasCrit ? 0 : 2;
      compStatus = hasCrit ? 'fail' : 'warn';
      var wordsList = violations.map(function(v){ return '"' + v.word + '"'; }).join(', ');
      compFix = (hasCrit ? 'CRITICAL POLICY VIOLATION: ' : 'POLICY WARNING: ') + 'Flagged phrasing detected: ' + wordsList + '. ' + violations[0].reason;
      if (violations[0].fix) compFix += ' Replace with: "' + violations[0].fix + '".';
    }
    checks.push({ id: 'policy_compliance', name: 'Policy & Claims Compliance', pts: compPts, max: 5, status: compStatus, fix: compFix, severity: violations.some(function(v){ return v.sev === 'critical'; }) ? 4 : 2 });
    totalScore += compPts;

    var failedChecks = checks.filter(function(c){ return c.pts < c.max; });
    failedChecks.sort(function(a,b){
      if (b.severity !== a.severity) return b.severity - a.severity;
      return a.pts - b.pts;
    });
    var primaryFix = failedChecks.length > 0 ? failedChecks[0].fix : 'Listing fully optimized.';

    return {
      score: totalScore,
      checks: checks,
      primaryFix: primaryFix,
      failedChecks: failedChecks
    };
  }

  var currentAuditRows = [];
  var currentAuditResults = [];
  var currentSortCol = 'score';
  var currentSortAsc = true;

  function renderAuditSummary(platKey) {
    if (!currentAuditResults || currentAuditResults.length === 0) return;
    var total = currentAuditResults.length;
    var sumScore = currentAuditResults.reduce(function(acc, r){ return acc + r.score; }, 0);
    var avgScore = Math.round(sumScore / total);
    var critCount = currentAuditResults.filter(function(r){ return r.score < 50; }).length;
    var goodCount = currentAuditResults.filter(function(r){ return r.score >= 80; }).length;

    var sumTitleLen = currentAuditResults.reduce(function(acc, r){ return acc + r.title.length; }, 0);
    var avgTitleLen = Math.round(sumTitleLen / total);

    var lowImgCount = currentAuditResults.filter(function(r){ return r.imageCount < 5; }).length;
    var lowImgPct = Math.round((lowImgCount / total) * 100);

    var zeroRevCount = currentAuditResults.filter(function(r){ return r.reviews === 0; }).length;
    var zeroRevPct = Math.round((zeroRevCount / total) * 100);

    var cfg = AUDIT_PLATFORM_CONFIG[platKey] || AUDIT_PLATFORM_CONFIG.sea;

    var elScore = document.getElementById('audit-overall-score');
    if (elScore) {
      elScore.textContent = avgScore + '/100';
      elScore.style.color = avgScore >= 80 ? '#4ade80' : (avgScore >= 50 ? '#facc15' : '#f87171');
    }
    var elStatus = document.getElementById('audit-overall-status');
    if (elStatus) elStatus.textContent = avgScore >= 80 ? 'Catalogue Healthy & Ready' : (avgScore >= 50 ? 'Requires Systematic Optimization' : 'Critical Account Demotion Risk');

    var elTotal = document.getElementById('audit-total-skus');
    if (elTotal) elTotal.textContent = total;

    var elPlat = document.getElementById('audit-platform-label');
    if (elPlat) elPlat.textContent = cfg.name;

    var elCrit = document.getElementById('audit-crit-count');
    if (elCrit) elCrit.textContent = critCount;

    var elGood = document.getElementById('audit-good-count');
    if (elGood) elGood.textContent = goodCount;

    var elAvgTitle = document.getElementById('audit-avg-title-len');
    if (elAvgTitle) elAvgTitle.textContent = avgTitleLen + ' chars';

    var elTitleTarget = document.getElementById('audit-title-target');
    if (elTitleTarget) elTitleTarget.textContent = 'Target: ' + cfg.optMin + '–' + cfg.optMax + ' chars';

    var elLowImg = document.getElementById('audit-low-img-pct');
    if (elLowImg) elLowImg.textContent = lowImgPct + '% (' + lowImgCount + ' SKUs)';

    var elZeroRev = document.getElementById('audit-zero-rev-pct');
    if (elZeroRev) elZeroRev.textContent = zeroRevPct + '% (' + zeroRevCount + ' SKUs)';
  }

  function renderAuditTopFixes() {
    var fixesContainer = document.getElementById('audit-top-fixes');
    if (!fixesContainer) return;
    if (!currentAuditResults || currentAuditResults.length === 0) {
      fixesContainer.innerHTML = '<p class="muted" style="font-size:13px">Load a catalogue CSV or click "Load Sample" to see prioritized fixes.</p>';
      return;
    }

    // Map each check deficiency to an issue category
    var issueMap = {};
    currentAuditResults.forEach(function(r){
      r.failedChecks.forEach(function(fc){
        if (!issueMap[fc.id]) {
          issueMap[fc.id] = {
            id: fc.id,
            name: fc.name,
            severity: fc.severity,
            fixSample: fc.fix,
            skus: []
          };
        }
        issueMap[fc.id].skus.push(r.sku);
      });
    });

    var issueList = Object.keys(issueMap).map(function(k){ return issueMap[k]; });
    issueList.sort(function(a,b){
      var impactA = a.skus.length * a.severity;
      var impactB = b.skus.length * b.severity;
      return impactB - impactA;
    });

    var top10 = issueList.slice(0, 10);
    if (top10.length === 0) {
      fixesContainer.innerHTML = '<div style="padding:1rem;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);border-radius:12px;color:#4ade80;font-size:13px">Outstanding — no critical issues or policy violations found across this catalogue.</div>';
      return;
    }

    var totalSkus = currentAuditResults.length;
    var html = top10.map(function(item, idx){
      var pct = Math.round((item.skus.length / totalSkus) * 100);
      var sevLabel = item.severity >= 4 ? 'CRITICAL' : (item.severity >= 3 ? 'HIGH' : (item.severity >= 2 ? 'MEDIUM' : 'LOW'));
      var sevClass = item.severity >= 4 ? 'crit' : (item.severity >= 3 ? 'warn' : 'good');
      return '<div class="fix-item">' +
        '<div class="fix-rank">#' + (idx + 1) + '</div>' +
        '<div class="fix-content">' +
          '<div style="display:flex;align-items:center;gap:.6rem;flex-wrap:wrap">' +
            '<span class="score-pill ' + sevClass + '">' + sevLabel + '</span>' +
            '<span class="fix-title">' + item.name + '</span>' +
          '</div>' +
          '<div class="fix-desc" style="margin-top:.35rem">' + item.fixSample + '</div>' +
        '</div>' +
        '<div class="fix-stat">' + item.skus.length + ' SKUs (' + pct + '%)</div>' +
      '</div>';
    }).join('');

    fixesContainer.innerHTML = html;
  }

  function sortAndRenderAuditTable() {
    var tbody = document.getElementById('audit-tbody');
    if (!tbody) return;
    if (!currentAuditResults || currentAuditResults.length === 0) {
      tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:2rem;" class="muted">No data loaded yet. Upload a CSV or load sample.</td></tr>';
      return;
    }

    currentAuditResults.sort(function(a,b){
      var valA = a[currentSortCol];
      var valB = b[currentSortCol];
      if (typeof valA === 'string') {
        return currentSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }
      return currentSortAsc ? valA - valB : valB - valA;
    });

    var html = currentAuditResults.map(function(r){
      var pillCls = r.score >= 80 ? 'good' : (r.score >= 50 ? 'warn' : 'crit');
      var pillTxt = r.score >= 80 ? 'Good' : (r.score >= 50 ? 'Warn' : 'Crit');
      var safeTitle = (r.title || '').replace(/"/g, '&quot;');
      var displayTitle = r.title.length > 48 ? r.title.slice(0, 48) + '…' : r.title;
      return '<tr data-sku="' + r.sku + '" style="cursor:pointer" onclick="window.openAuditDrawer(this.dataset.sku)">' +
        '<td class="sku-cell">' + r.sku + '</td>' +
        '<td class="title-cell" title="' + safeTitle + '">' + displayTitle + '</td>' +
        '<td style="text-align:center"><span class="score-pill ' + pillCls + '">' + r.score + ' · ' + pillTxt + '</span></td>' +
        '<td style="text-align:center">' + r.imageCount + '</td>' +
        '<td style="text-align:center">' + r.reviews + '</td>' +
        '<td style="text-align:right">₱/$/€' + r.price.toFixed(2) + '</td>' +
        '<td style="text-align:right">' + (r.stock <= 0 ? '<span style="color:#f87171">0</span>' : r.stock) + '</td>' +
        '<td style="font-size:12px;max-width:240px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="' + (r.primaryFix || '').replace(/"/g, '&quot;') + '">' + (r.primaryFix || '—') + '</td>' +
        '<td style="text-align:center" onclick="event.stopPropagation()">' +
          '<button class="btn ghost" type="button" data-sku="' + r.sku + '" onclick="window.openAuditDrawer(this.dataset.sku)" style="padding:4px 10px;font-size:11px">Inspect</button>' +
        '</td>' +
      '</tr>';
    }).join('');

    tbody.innerHTML = html;
  }

  function runAudit(rawRows, platformKey) {
    if (!rawRows || rawRows.length === 0) return;
    currentAuditRows = rawRows;
    var platKey = platformKey || (document.getElementById('audit-platform') ? document.getElementById('audit-platform').value : 'sea');
    currentAuditResults = rawRows.map(function(raw){
      var prod = mapRowToProduct(raw);
      var scored = scoreSKU(prod, platKey);
      return {
        sku: prod.sku,
        title: prod.title,
        description: prod.description,
        bullets: prod.bullets,
        imageCount: prod.imageCount,
        reviews: prod.reviews,
        rating: prod.rating,
        price: prod.price,
        stock: prod.stock,
        sales: prod.sales,
        category: prod.category,
        score: scored.score,
        checks: scored.checks,
        primaryFix: scored.primaryFix,
        failedChecks: scored.failedChecks
      };
    });

    try {
      localStorage.setItem('audit-v1', JSON.stringify({ platform: platKey, rows: rawRows }));
    } catch(e) {}

    renderAuditSummary(platKey);
    renderAuditTopFixes();
    sortAndRenderAuditTable();
  }

  function openAuditDrawer(sku) {
    var item = currentAuditResults.find(function(r){ return r.sku === sku; });
    if (!item) return;
    var drawer = document.getElementById('audit-drawer');
    var backdrop = document.getElementById('audit-drawer-backdrop');
    if (!drawer || !backdrop) return;

    var badge = document.getElementById('drawer-sku-badge');
    if (badge) badge.textContent = 'SKU INSPECTION · ' + item.sku;
    var titleEl = document.getElementById('drawer-title');
    if (titleEl) titleEl.textContent = item.title;
    var idEl = document.getElementById('drawer-sku-id');
    if (idEl) idEl.textContent = 'Category: ' + item.category + ' | Stock: ' + item.stock + ' units | Price: ₱/$/€' + item.price.toFixed(2);
    var scoreVal = document.getElementById('drawer-score-val');
    if (scoreVal) scoreVal.textContent = item.score + '/100';

    var pillCls = item.score >= 80 ? 'good' : (item.score >= 50 ? 'warn' : 'crit');
    var pillTxt = item.score >= 80 ? 'OPTIMIZED' : (item.score >= 50 ? 'NEEDS WORK' : 'CRITICAL RISK');
    var scorePill = document.getElementById('drawer-score-pill');
    if (scorePill) scorePill.innerHTML = '<span class="score-pill ' + pillCls + '">' + pillTxt + '</span>';

    var listHtml = item.checks.map(function(c){
      var icon = '<svg class="ico ico-sm" style="stroke:' + (c.status === 'pass' ? '#4ade80' : (c.status === 'warn' ? '#facc15' : '#f87171')) + '" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-' + (c.status === 'pass' ? 'check' : (c.status === 'warn' ? 'warn' : 'x')) + '"/></svg>';
      var color = c.status === 'pass' ? '#4ade80' : (c.status === 'warn' ? '#facc15' : '#f87171');
      return '<div class="drawer-check-item">' +
        '<div class="drawer-check-head">' +
          '<div class="drawer-check-name">' + icon + ' ' + c.name + '</div>' +
          '<div class="drawer-check-pts" style="color:' + color + '">' + c.pts + ' / ' + c.max + ' pts</div>' +
        '</div>' +
        '<div class="drawer-check-detail">' + c.fix + '</div>' +
      '</div>';
    }).join('');
    var checksList = document.getElementById('drawer-checks-list');
    if (checksList) checksList.innerHTML = listHtml;

    drawer.classList.add('open');
    backdrop.classList.add('open');
  }
  window.openAuditDrawer = openAuditDrawer;

  function closeAuditDrawer() {
    var drawer = document.getElementById('audit-drawer');
    var backdrop = document.getElementById('audit-drawer-backdrop');
    if (drawer) drawer.classList.remove('open');
    if (backdrop) backdrop.classList.remove('open');
  }
  window.closeAuditDrawer = closeAuditDrawer;

  function downloadBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(url); }, 1000);
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      showToast('Audit summary copied to clipboard!');
    } catch(e) {
      showToast('Unable to copy summary automatically.');
    }
    document.body.removeChild(ta);
  }

  function exportAuditCSV() {
    if (!currentAuditResults || currentAuditResults.length === 0) {
      showToast('No audit data to export. Load sample or upload CSV first.');
      return;
    }
    var headers = ['SKU','Product Title','Health Score','Status','Images','Reviews','Rating','Price','Stock','Primary Fix'];
    var lines = [headers.join(',')];
    currentAuditResults.forEach(function(r){
      var status = r.score >= 80 ? 'Optimized' : (r.score >= 50 ? 'Needs Work' : 'Critical');
      var row = [
        '"' + (r.sku || '').replace(/"/g, '""') + '"',
        '"' + (r.title || '').replace(/"/g, '""') + '"',
        r.score,
        '"' + status + '"',
        r.imageCount,
        r.reviews,
        r.rating,
        r.price,
        r.stock,
        '"' + (r.primaryFix || '').replace(/"/g, '""') + '"'
      ];
      lines.push(row.join(','));
    });
    var blob = new Blob([lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    downloadBlob(blob, 'marketplace-audit-scorecard.csv');
    showToast('CSV audit report downloaded.');
  }
  window.exportAuditCSV = exportAuditCSV;

  function exportAuditHTML() {
    if (!currentAuditResults || currentAuditResults.length === 0) {
      showToast('No audit data to export. Load sample or upload CSV first.');
      return;
    }
    var platKey = document.getElementById('audit-platform') ? document.getElementById('audit-platform').value : 'sea';
    var platName = AUDIT_PLATFORM_CONFIG[platKey] ? AUDIT_PLATFORM_CONFIG[platKey].name : 'Marketplace';
    var avgScore = Math.round(currentAuditResults.reduce(function(acc, r){ return acc + r.score; }, 0) / currentAuditResults.length);
    var critCount = currentAuditResults.filter(function(r){ return r.score < 50; }).length;
    var goodCount = currentAuditResults.filter(function(r){ return r.score >= 80; }).length;

    var rowsHtml = currentAuditResults.map(function(r){
      var pillCls = r.score >= 80 ? 'color:#4ade80' : (r.score >= 50 ? 'color:#facc15' : 'color:#f87171');
      return '<tr>' +
        '<td style="font-family:monospace;font-weight:bold">' + r.sku + '</td>' +
        '<td>' + r.title + '</td>' +
        '<td style="text-align:center;font-weight:bold;' + pillCls + '">' + r.score + '</td>' +
        '<td style="text-align:center">' + r.imageCount + '</td>' +
        '<td style="text-align:center">' + r.reviews + '</td>' +
        '<td style="text-align:right">₱/$/€' + r.price.toFixed(2) + '</td>' +
        '<td style="text-align:right">' + r.stock + '</td>' +
        '<td style="font-size:12px;color:#aaa">' + r.primaryFix + '</td>' +
      '</tr>';
    }).join('');

    var html = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n' +
      '<title>Marketplace Catalogue Audit Report · ' + platName + '</title>\n' +
      '<style>\n' +
      'body{margin:0;padding:2rem;background:#0B0B0B;color:#F5F2ED;font-family:system-ui,-apple-system,sans-serif;line-height:1.5}\n' +
      '.wrap{max-width:1100px;margin:0 auto}\n' +
      'h1{font-size:2rem;margin-bottom:.5rem;color:#F5F2ED}\n' +
      '.strip{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.5rem 0 2rem}\n' +
      '.card{background:#161616;border:1px solid #2a2a2a;border-radius:12px;padding:1.25rem;text-align:center}\n' +
      '.card .val{font-size:2rem;font-weight:bold;margin-bottom:.25rem}\n' +
      '.card .lbl{font-size:11px;text-transform:uppercase;color:#888;letter-spacing:.08em}\n' +
      'table{width:100%;border-collapse:collapse;margin-top:1.5rem;font-size:13px}\n' +
      'th{background:#1c1c1c;padding:.75rem 1rem;text-align:left;border-bottom:2px solid #333;font-size:11px;text-transform:uppercase;color:#888}\n' +
      'td{padding:.75rem 1rem;border-bottom:1px solid #222}\n' +
      '.footer{margin-top:3rem;text-align:center;color:#666;font-size:12px;border-top:1px solid #222;padding-top:1.5rem}\n' +
      '</style>\n</head>\n<body>\n<div class="wrap">\n' +
      '<h1>Marketplace Catalogue Audit Report</h1>\n' +
      '<p style="color:#888;margin-top:0">Target Platform: <b>' + platName + '</b> · Generated: ' + (new Date()).toLocaleDateString() + '</p>\n' +
      '<div class="strip">\n' +
        '<div class="card"><div class="val" style="color:' + (avgScore>=80?'#4ade80':(avgScore>=50?'#facc15':'#f87171')) + '">' + avgScore + '/100</div><div class="lbl">Catalogue Health Score</div></div>\n' +
        '<div class="card"><div class="val">' + currentAuditResults.length + '</div><div class="lbl">Audited SKUs</div></div>\n' +
        '<div class="card"><div class="val" style="color:#f87171">' + critCount + '</div><div class="lbl">Critical Risk (&lt;50)</div></div>\n' +
        '<div class="card"><div class="val" style="color:#4ade80">' + goodCount + '</div><div class="lbl">Optimized (80+)</div></div>\n' +
      '</div>\n' +
      '<h2>Detailed SKU Scorecard</h2>\n' +
      '<table>\n' +
        '<thead><tr><th>SKU</th><th>Product Title</th><th style="text-align:center">Score</th><th style="text-align:center">Images</th><th style="text-align:center">Reviews</th><th style="text-align:right">Price</th><th style="text-align:right">Stock</th><th>Primary Recommended Action</th></tr></thead>\n' +
        '<tbody>' + rowsHtml + '</tbody>\n' +
      '</table>\n' +
      '<div class="footer">Generated by Micro-SaaS SellerGuard · Jamie Lyn Ludovice Portfolio</div>\n' +
      '</div>\n</body>\n</html>';

    var blob = new Blob([html], { type: 'text/html;charset=utf-8;' });
    downloadBlob(blob, 'marketplace-audit-report.html');
    showToast('HTML audit report downloaded.');
  }
  window.exportAuditHTML = exportAuditHTML;

  function copyAuditSummary() {
    if (!currentAuditResults || currentAuditResults.length === 0) {
      showToast('No audit data to copy. Load sample or upload CSV first.');
      return;
    }
    var platKey = document.getElementById('audit-platform') ? document.getElementById('audit-platform').value : 'sea';
    var platName = AUDIT_PLATFORM_CONFIG[platKey] ? AUDIT_PLATFORM_CONFIG[platKey].name : 'Marketplace';
    var avgScore = Math.round(currentAuditResults.reduce(function(acc, r){ return acc + r.score; }, 0) / currentAuditResults.length);
    var critCount = currentAuditResults.filter(function(r){ return r.score < 50; }).length;
    var goodCount = currentAuditResults.filter(function(r){ return r.score >= 80; }).length;

    var text = 'MARKETPLACE CATALOGUE AUDIT REPORT\n' +
      '==================================================\n' +
      'Platform: ' + platName + '\n' +
      'Total SKUs Audited: ' + currentAuditResults.length + '\n' +
      'Overall Health Score: ' + avgScore + '/100\n' +
      '- Critical Risk SKUs (<50): ' + critCount + '\n' +
      '- High Conversion SKUs (80+): ' + goodCount + '\n\n' +
      'TOP CATALOGUE FIXES:\n';

    var topFixesEls = document.querySelectorAll('#audit-top-fixes .fix-item');
    if (topFixesEls && topFixesEls.length > 0) {
      topFixesEls.forEach(function(el, idx){
        var title = el.querySelector('.fix-title') ? el.querySelector('.fix-title').textContent : '';
        var stat = el.querySelector('.fix-stat') ? el.querySelector('.fix-stat').textContent : '';
        text += (idx + 1) + '. ' + title + ' (' + stat + ')\n';
      });
    } else {
      text += 'Catalogue fully optimized.\n';
    }
    text += '==================================================\n' +
      'Generated by Micro-SaaS SellerGuard\n';

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function(){
        showToast('Audit summary copied to clipboard!');
      }).catch(function(){
        fallbackCopy(text);
      });
    } else {
      fallbackCopy(text);
    }
  }
  window.copyAuditSummary = copyAuditSummary;

  function loadAuditSample() {
    var plat = document.getElementById('audit-platform') ? document.getElementById('audit-platform').value : 'sea';
    runAudit(AUDIT_SAMPLE_ROWS, plat);
    showToast('Loaded 25 generic sample SKUs across 3 platforms!');
  }
  window.loadAuditSample = loadAuditSample;

  /* ===================== TOOL 5: PRODUCT PERFORMANCE CLASSIFIER ===================== */
  var CLS_KEY = 'classify-v1';
  var CLS_ROWS = [];
  var CLS_FILTER = 'all';
  function svgIco(n){ return '<svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-' + n + '"/></svg>'; }
  var CLS_ICON = {'Expired stock':svgIco('alert'),'Clearance sale':svgIco('clock'),'Flash sale':svgIco('flame'),'Bundle / voucher':svgIco('gift'),'Promo push':svgIco('mega'),'Scale':svgIco('rocket'),'Restock first':svgIco('inbox')};
  var CLS_ORDER = {High:0, Growth:1, Medium:2, Low:3};

  function clsNum(v){ if (v === null || v === undefined) return null; var n = parseFloat(String(v).replace(/[^0-9.\-]/g,'')); return isNaN(n) ? null : n; }
  function clsFind(raw, regex){ var keys = Object.keys(raw); for (var i=0;i<keys.length;i++){ if (regex.test(keys[i]) && String(raw[keys[i]]).trim() !== '') return raw[keys[i]]; } return null; }
  function clsDays(dateStr){
    if (!dateStr) return null;
    var d = new Date(String(dateStr).trim()); if (isNaN(d.getTime())) return null;
    var today = new Date(); today.setHours(0,0,0,0);
    return Math.round((d - today) / 86400000);
  }
  function clsThresholds(){
    function g(id, def){ var el = document.getElementById(id); var v = el ? parseFloat(el.value) : NaN; return isNaN(v) ? def : v; }
    return { clear: g('cls-t-clear',60), bundle: g('cls-t-bundle',120), flash: g('cls-t-flash',10), months: g('cls-t-months',3), scale: g('cls-t-scale',30) };
  }
  function clsNormalize(raw){
    var imgRaw = clsFind(raw, /^(image|has_image|main image|image url|photo)/i);
    var hasImage = true;
    if (imgRaw !== null) { var iv = String(imgRaw).trim().toLowerCase(); hasImage = !(iv === '' || iv === 'no' || iv === 'n' || iv === 'false' || iv === '0'); }
    var p = {
      sku: String(clsFind(raw, /^(sku|seller sku|item id|product id|id)$/i) || clsFind(raw, /sku/i) || '').trim(),
      name: String(clsFind(raw, /^(name|title|product name|product title|item name)/i) || '(unnamed)').trim(),
      brand: String(clsFind(raw, /^(brand|vendor|store|shop)/i) || '').trim(),
      stock: clsNum(clsFind(raw, /^(stock|quantity|qty|inventory|on hand|stock_boxes)/i)),
      sold: clsNum(clsFind(raw, /(sold_30d|sold 30d|units sold|sales 30d|sales_30d|sold last 30|monthly sales|^sold$|^sales$)/i)),
      price: clsNum(clsFind(raw, /^(price|selling price|sale price|list price)/i)),
      cost: clsNum(clsFind(raw, /^(cost|cogs|unit cost|cost price)/i)),
      expiry: clsFind(raw, /^(expiry|expiration|expires|expiry date|best before)/i),
      hasImage: hasImage
    };
    p.daysToExpiry = clsDays(p.expiry);
    p.needsImage = !hasImage;
    return p;
  }
  function clsClassify(p, t){
    var stock = p.stock || 0, sold = p.sold || 0, dexp = p.daysToExpiry, why = [];
    if (dexp !== null && dexp < 0 && stock > 0) return {action:'Expired stock', priority:'High', why:['expired ' + (-dexp) + ' days ago, ' + stock + ' still in stock']};
    if (stock <= 0) return {action:'Restock first', priority:'Low', why:['no sellable stock']};
    if (dexp !== null && dexp <= t.clear) return {action:'Clearance sale', priority:'High', why:['expires in ' + dexp + ' days']};
    if (sold === 0) {
      why.push('0 sold in 30 days');
      if (stock >= t.flash) { why.push(stock + ' units sitting'); return {action:'Flash sale', priority:'High', why:why}; }
      return {action:'Promo push', priority:'Medium', why:why};
    }
    if (sold >= t.scale && stock < sold) return {action:'Scale', priority:'Growth', why:[sold + ' sold / 30d, only ' + stock + ' left — restock and advertise']};
    var months = stock / sold;
    if (dexp !== null && dexp <= t.bundle) return {action:'Bundle / voucher', priority:'Medium', why:['expires in ' + dexp + ' days', months.toFixed(1) + ' months of stock']};
    if (months >= t.months) return {action:'Bundle / voucher', priority:'Medium', why:[months.toFixed(1) + ' months of stock at this pace']};
    return {action:'Promo push', priority:'Medium', why:[sold + ' sold / 30d, ' + months.toFixed(1) + ' months of stock']};
  }
  function clsRun(rawRows){
    var t = clsThresholds();
    CLS_ROWS = rawRows.map(function(r){ var p = clsNormalize(r); var c = clsClassify(p, t); p.action = c.action; p.priority = c.priority; p.why = c.why; p.months = (p.sold && p.stock) ? p.stock / p.sold : null; return p; });
    CLS_ROWS.sort(function(a,b){ var d = (CLS_ORDER[a.priority]||9) - (CLS_ORDER[b.priority]||9); return d !== 0 ? d : (b.stock||0) - (a.stock||0); });
    try { localStorage.setItem(CLS_KEY, JSON.stringify({rows: rawRows, at: Date.now()})); } catch(e){}
    clsRenderKpis(); clsRenderBrands(); clsRender();
  }
  function clsCount(a){ return CLS_ROWS.filter(function(p){ return p.action === a; }).length; }
  function clsRenderKpis(){
    function set(id,v){ var el = document.getElementById(id); if (el) el.textContent = v; }
    set('cls-k-expired', clsCount('Expired stock')); set('cls-k-clear', clsCount('Clearance sale')); set('cls-k-flash', clsCount('Flash sale'));
    set('cls-k-bundle', clsCount('Bundle / voucher')); set('cls-k-promo', clsCount('Promo push')); set('cls-k-scale', clsCount('Scale'));
    set('cls-k-noimg', CLS_ROWS.filter(function(p){ return p.needsImage; }).length);
  }
  function clsRenderBrands(){
    var sel = document.getElementById('cls-brand'); if (!sel) return;
    var cur = sel.value; var brands = {}; CLS_ROWS.forEach(function(p){ if (p.brand) brands[p.brand] = 1; });
    var names = Object.keys(brands).sort();
    sel.innerHTML = '<option value="">All brands</option>' + names.map(function(b){ return '<option value="' + escHtml(b) + '"' + (b === cur ? ' selected' : '') + '>' + escHtml(b) + '</option>'; }).join('');
  }
  function clsFiltered(){
    var q = (document.getElementById('cls-q') ? document.getElementById('cls-q').value : '').toLowerCase();
    var br = document.getElementById('cls-brand') ? document.getElementById('cls-brand').value : '';
    return CLS_ROWS.filter(function(p){
      if (CLS_FILTER === 'noimage') { if (!p.needsImage) return false; }
      else if (CLS_FILTER !== 'all' && p.action !== CLS_FILTER) return false;
      if (br && p.brand !== br) return false;
      if (q && (p.name + ' ' + p.sku).toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
  }
  function clsFmt(v, d){ if (v === null || v === undefined) return '—'; return Number(v).toLocaleString('en-US', {maximumFractionDigits: d === undefined ? 1 : d}); }
  function clsRender(){
    var list = clsFiltered(); var tb = document.getElementById('cls-tbody'); var st = document.getElementById('cls-status');
    if (st) st.textContent = CLS_ROWS.length ? (list.length + ' of ' + CLS_ROWS.length + ' products shown — sorted by urgency') : 'No data loaded yet.';
    if (!tb) return;
    if (!list.length) { tb.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:2rem;" class="muted">' + (CLS_ROWS.length ? 'Nothing in this filter.' : 'Upload a CSV or load the sample.') + '</td></tr>'; return; }
    tb.innerHTML = list.map(function(p){
      var exp = p.daysToExpiry === null ? '—' : (p.daysToExpiry < 0 ? '<span style="color:#f87171;font-weight:600">expired</span>' : escHtml(String(p.expiry)) + ' (' + p.daysToExpiry + 'd)');
      return '<tr>' +
        '<td><span class="act-pill ' + p.priority.toLowerCase() + '">' + (CLS_ICON[p.action] || '') + ' ' + escHtml(p.action) + '</span></td>' +
        '<td class="title-cell" title="' + escHtml(p.name) + '"><span style="color:var(--ink)">' + escHtml(p.name) + '</span>' + (p.needsImage ? '<span class="noimg-tag"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-camera-off"/></svg>no image</span>' : '') + '<div class="sku-cell" style="font-size:11px;opacity:.7">' + escHtml(p.sku) + '</div></td>' +
        '<td>' + escHtml(p.brand || '—') + '</td>' +
        '<td>' + clsFmt(p.stock, 0) + '</td>' +
        '<td>' + clsFmt(p.sold, 0) + '</td>' +
        '<td>' + (p.months === null ? '—' : clsFmt(p.months, 1)) + '</td>' +
        '<td>' + exp + '</td>' +
        '<td>' + (p.price === null ? '—' : clsFmt(p.price, 2)) + '</td>' +
        '<td class="cls-why">' + escHtml(p.why.join(' · ')) + '</td>' +
      '</tr>';
    }).join('');
  }
  function clsSetFilter(f){
    CLS_FILTER = f;
    document.querySelectorAll('#cls-tabs .cls-tab').forEach(function(b){ b.classList.toggle('on', b.dataset.f === f); });
    clsRender();
  }
  function clsExportCSV(){
    if (!CLS_ROWS.length) { showToast('Load data first.'); return; }
    var head = ['action','priority','sku','name','brand','stock','sold_30d','months_of_stock','expiry','days_to_expiry','price','needs_image','why'];
    var lines = [head.join(',')].concat(CLS_ROWS.map(function(p){
      return [p.action,p.priority,p.sku,p.name,p.brand,p.stock,p.sold,p.months===null?'':p.months.toFixed(2),p.expiry||'',p.daysToExpiry===null?'':p.daysToExpiry,p.price===null?'':p.price,p.needsImage?'yes':'no',p.why.join('; ')]
        .map(function(v){ v = v === null || v === undefined ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g,'""') + '"' : v; }).join(',');
    }));
    downloadBlob(new Blob([lines.join('\n')], {type:'text/csv'}), 'product-action-plan.csv');
    showToast('Exported ' + CLS_ROWS.length + ' products.');
  }
  function clsPlanText(){
    var groups = ['Expired stock','Clearance sale','Flash sale','Bundle / voucher','Promo push','Scale','Restock first'];
    var out = ['PRODUCT ACTION PLAN — ' + CLS_ROWS.length + ' products', ''];
    groups.forEach(function(g){
      var items = CLS_ROWS.filter(function(p){ return p.action === g; }); if (!items.length) return;
      out.push(g.toUpperCase() + ' (' + items.length + ')');
      items.forEach(function(p){ out.push('  - ' + p.name + (p.sku ? ' [' + p.sku + ']' : '') + ' — ' + p.why.join(', ')); });
      out.push('');
    });
    var noimg = CLS_ROWS.filter(function(p){ return p.needsImage; });
    if (noimg.length) { out.push('NEEDS IMAGE (' + noimg.length + ')'); noimg.forEach(function(p){ out.push('  - ' + p.name); }); }
    return out.join('\n');
  }
  function clsCopyPlan(){
    if (!CLS_ROWS.length) { showToast('Load data first.'); return; }
    var t = clsPlanText();
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(t).then(function(){ showToast('Action plan copied.'); }, function(){ fallbackCopy(t); }); }
    else fallbackCopy(t);
  }
  var CLS_SAMPLE = (function(){
    var today = new Date(); function d(days){ var x = new Date(today.getTime() + days*86400000); return x.toISOString().slice(0,10); }
    var rows = [
      ['SKU-COF-001','Colombian Dolce Capsules 12pc','Bean House','Coffee',30,0,609,320,d(-6),'yes'],
      ['SKU-COF-002','Pistachio Iced Latte Capsules 10pc','Bean House','Coffee',51,0,719,380,d(24),'yes'],
      ['SKU-COF-003','Lungo Decaf Capsules 12pc','Bean House','Coffee',37,0,609,320,d(25),'yes'],
      ['SKU-COF-004','Espresso Pods 16pc','Rene','Coffee',26,0,539,300,d(56),'yes'],
      ['SKU-COF-005','House Blend Decaf 12pc','Bean House','Coffee',26,0,609,320,d(297),'yes'],
      ['SKU-COF-006','Vertuo Chiaro Decaf 10pc','Vertuo','Coffee',24,0,799,420,d(-37),'yes'],
      ['SKU-COF-007','Century Capsules Turkish 10pc','Gaeng','Coffee',45,0,349,190,d(145),'yes'],
      ['SKU-BEV-001','Sparkling Pear 350ml','Sparkle Co','Beverage',212,0,79,45,d(203),'yes'],
      ['SKU-BEV-002','Sparkling Plum 350ml','Sparkle Co','Beverage',43,0,79,45,d(77),'yes'],
      ['SKU-BEV-003','Sparkling Yuzu 350ml','Sparkle Co','Beverage',18,44,79,45,d(150),'yes'],
      ['SKU-HAIR-001','Airy Polish Oil 100ml','Dashu','Hair',87,0,259,120,d(298),'yes'],
      ['SKU-HAIR-002','Anti-Hair Loss Shampoo 500ml','Dashu','Hair',28,0,790,380,d(674),'yes'],
      ['SKU-HAIR-003','Down Tech Fold Wax','Dashu','Hair',22,0,1349,700,'','yes'],
      ['SKU-HAIR-004','Perfect Serum Shampoo 680ml','Scene','Hair',27,0,299,150,d(118),'yes'],
      ['SKU-HAIR-005','Styling Shampoo 680ml','Scene','Hair',36,0,299,150,'','yes'],
      ['SKU-HAIR-006','Ash Khaki Hair Colour 7K','Scene','Hair',32,0,299,140,d(181),'yes'],
      ['SKU-HAIR-007','Shining Essence 8g','Scene','Hair',31,0,299,140,d(173),'yes'],
      ['SKU-HAIR-008','Perfect Serum Original 80ml','Scene','Hair',120,95,349,160,d(400),'yes'],
      ['SKU-HAIR-009','Damage Care Treatment 180ml','Scene','Hair',9,0,399,180,d(220),'yes'],
      ['SKU-SKIN-001','Snail Mucin Serum 50ml','Glow Lab','Skincare',140,160,499,210,d(500),'yes'],
      ['SKU-SKIN-002','Centella Calming Cream 50ml','Glow Lab','Skincare',60,52,599,260,d(420),'yes'],
      ['SKU-SKIN-003','Rice Toner 150ml','Glow Lab','Skincare',210,38,449,190,d(380),'yes'],
      ['SKU-SKIN-004','Vitamin C Ampoule 30ml','Glow Lab','Skincare',5,41,899,400,d(300),'yes'],
      ['SKU-SKIN-005','Sun Stick SPF50','Glow Lab','Skincare',0,22,649,280,d(600),'yes'],
      ['SKU-SKIN-006','Sheet Mask 10pc Set','Glow Lab','Skincare',400,70,299,120,d(260),'no'],
      ['SKU-MED-001','Wound Dressing Large 10pc','Nexa','Medical',29,0,199,90,'','no'],
      ['SKU-MED-002','Nitrile Gloves Large 100pc','Nexa','Medical',101,0,199,110,'','yes'],
      ['SKU-MED-003','Adhesive Roll 10cm x 1m','Dimple','Medical',64,0,749,400,d(778),'yes'],
      ['SKU-MED-004','Cooling Roll-On 30ml','Mentho','Medical',20,0,399,180,'','yes'],
      ['SKU-MED-005','Alcohol Wipes 100pc','Nexa','Medical',300,140,149,60,d(700),'yes'],
      ['SKU-HOME-001','Bamboo Kitchen Towels 6pc','Casa','Home',75,12,349,150,'','yes'],
      ['SKU-HOME-002','Silicone Food Bags 4pc','Casa','Home',48,3,599,260,'','no'],
      ['SKU-HOME-003','Glass Storage Set 5pc','Casa','Home',0,0,1299,600,'','yes'],
      ['SKU-HOME-004','Air Fryer Liners 50pc','Casa','Home',220,8,249,90,'','yes'],
      ['SKU-HOME-005','Ceramic Mug 350ml','Casa','Home',66,31,299,110,'','no'],
      ['SKU-PET-001','Cat Litter Deodoriser 500g','Pawly','Pet',80,0,399,170,d(95),'yes'],
      ['SKU-PET-002','Dog Dental Chews 20pc','Pawly','Pet',15,40,449,200,d(130),'yes'],
      ['SKU-PET-003','Salmon Cat Treats 60g','Pawly','Pet',7,0,199,80,d(45),'yes'],
      ['SKU-PET-004','Pet Wipes 80pc','Pawly','Pet',150,55,229,90,d(500),'no'],
      ['SKU-PET-005','Collapsible Water Bowl','Pawly','Pet',33,2,259,110,'','yes']
    ];
    return rows.map(function(r){ return {sku:r[0], name:r[1], brand:r[2], category:r[3], stock:r[4], sold_30d:r[5], price:r[6], cost:r[7], expiry:r[8], image:r[9]}; });
  })();
  function loadClassifySample(){ clsRun(CLS_SAMPLE); showToast('Loaded 40 generic sample products.'); }
  window.loadClassifySample = loadClassifySample; window.clsRun = clsRun; window.clsPlanText = clsPlanText; window.clsExportCSV = clsExportCSV; window.clsSetFilter = clsSetFilter;

  (function clsWire(){
    var b;
    if ((b = document.getElementById('cls-sample-btn'))) b.addEventListener('click', loadClassifySample);
    if ((b = document.getElementById('cls-export-csv'))) b.addEventListener('click', clsExportCSV);
    if ((b = document.getElementById('cls-copy-plan'))) b.addEventListener('click', clsCopyPlan);
    if ((b = document.getElementById('cls-file'))) b.addEventListener('change', function(e){
      var file = e.target.files && e.target.files[0]; if (!file) return;
      var reader = new FileReader();
      reader.onload = function(evt){ var rows = parseCSV(evt.target.result); if (!rows.length) { showToast('Could not parse CSV. Check the header row.'); return; } clsRun(rows); showToast('Classified ' + rows.length + ' products.'); };
      reader.readAsText(file);
    });
    document.querySelectorAll('#cls-tabs .cls-tab').forEach(function(t){ t.addEventListener('click', function(){ clsSetFilter(t.dataset.f); }); });
    if ((b = document.getElementById('cls-brand'))) b.addEventListener('change', clsRender);
    if ((b = document.getElementById('cls-q'))) b.addEventListener('input', clsRender);
    ['cls-t-clear','cls-t-bundle','cls-t-flash','cls-t-months','cls-t-scale'].forEach(function(id){ var el = document.getElementById(id); if (el) el.addEventListener('input', function(){ if (CLS_ROWS.length) { var raw = null; try { raw = JSON.parse(localStorage.getItem(CLS_KEY) || 'null'); } catch(e){} if (raw && raw.rows) clsRun(raw.rows); } }); });
    try { var saved = JSON.parse(localStorage.getItem(CLS_KEY) || 'null'); if (saved && saved.rows && saved.rows.length && document.getElementById('cls-tbody')) clsRun(saved.rows); } catch(e){}
  })();

  /* ===================== TOOL 6: MONTHLY PERFORMANCE REPORT ===================== */
  var RPT_KEY = 'report-v1';
  var RPT_FIELDS = [
    ['revenue','Revenue',true],['orders','Orders',true],['sessions','Sessions / visits',true],
    ['ad_spend','Ad spend',true],['ad_sales','Ad-attributed sales',true],['units','Units sold',false],
    ['returns','Returns (orders)',false],['impressions','Organic impressions',false]
  ];
  function rptVal(id){ var el = document.getElementById(id); if (!el) return null; var v = parseFloat(String(el.value).replace(/[^0-9.\-]/g,'')); return isNaN(v) ? null : v; }
  function rptText(id){ var el = document.getElementById(id); return el ? String(el.value || '').trim() : ''; }
  function rptRead(){
    var d = { store: rptText('rpt-store') || 'Store', marketplace: rptText('rpt-marketplace') || 'Marketplace', month: rptText('rpt-month'), cur: rptText('rpt-cur') || '₱', notes: rptText('rpt-notes'), now: {}, prev: {} };
    RPT_FIELDS.forEach(function(f){ d.now[f[0]] = rptVal('rpt-' + f[0] + '-now'); d.prev[f[0]] = rptVal('rpt-' + f[0] + '-prev'); });
    return d;
  }
  function rptMetrics(m){
    var r = {};
    r.revenue = m.revenue; r.orders = m.orders; r.sessions = m.sessions; r.ad_spend = m.ad_spend; r.ad_sales = m.ad_sales; r.units = m.units; r.returns = m.returns; r.impressions = m.impressions;
    r.aov = (m.revenue && m.orders) ? m.revenue / m.orders : null;
    r.cvr = (m.orders !== null && m.sessions) ? m.orders / m.sessions : null;
    r.roas = (m.ad_sales !== null && m.ad_spend) ? m.ad_sales / m.ad_spend : null;
    r.tacos = (m.ad_spend !== null && m.revenue) ? m.ad_spend / m.revenue : null;
    r.ad_share = (m.ad_sales !== null && m.revenue) ? m.ad_sales / m.revenue : null;
    r.return_rate = (m.returns !== null && m.orders) ? m.returns / m.orders : null;
    r.organic_rev = (m.revenue !== null && m.ad_sales !== null) ? m.revenue - m.ad_sales : null;
    return r;
  }
  function rptDelta(a, b){ if (a === null || b === null || b === 0) return null; return (a - b) / Math.abs(b); }
  function rptFmtMoney(v, cur){ if (v === null || v === undefined) return '—'; return cur + Number(v).toLocaleString('en-US', {maximumFractionDigits: 0}); }
  function rptFmtNum(v, d){ if (v === null || v === undefined) return '—'; return Number(v).toLocaleString('en-US', {maximumFractionDigits: d === undefined ? 0 : d}); }
  function rptFmtPct(v, d){ if (v === null || v === undefined) return '—'; return (v * 100).toFixed(d === undefined ? 1 : d) + '%'; }
  function rptArrow(dlt, goodUp){
    if (dlt === null) return '<span class="rpt-flat">—</span>';
    var up = dlt >= 0, good = goodUp ? up : !up;
    var s = (up ? '▲ ' : '▼ ') + Math.abs(dlt * 100).toFixed(1) + '%';
    return '<span class="' + (Math.abs(dlt) < 0.005 ? 'rpt-flat' : (good ? 'rpt-good' : 'rpt-bad')) + '">' + s + '</span>';
  }
  function rptInsights(d){
    var n = rptMetrics(d.now), p = rptMetrics(d.prev), cur = d.cur;
    var dRev = rptDelta(n.revenue, p.revenue), dSes = rptDelta(n.sessions, p.sessions), dCvr = rptDelta(n.cvr, p.cvr), dAov = rptDelta(n.aov, p.aov),
        dRoas = rptDelta(n.roas, p.roas), dSpend = rptDelta(n.ad_spend, p.ad_spend), dOrd = rptDelta(n.orders, p.orders), dImp = rptDelta(n.impressions, p.impressions);
    var what = [], next = [];
    function pct(x){ return Math.abs(x * 100).toFixed(0) + '%'; }
    // 1 revenue headline
    if (dRev !== null) what.push('Revenue ' + (dRev >= 0 ? 'grew ' : 'fell ') + pct(dRev) + ' month-over-month to ' + rptFmtMoney(n.revenue, cur) + '.');
    // 2 traffic up, conversion down
    if (dSes !== null && dCvr !== null && dSes > 0.05 && dCvr < -0.05) { what.push('Traffic rose ' + pct(dSes) + ' but conversion dropped ' + pct(dCvr) + ' — more visitors, fewer buyers.'); next.push('Review the product pages that gained traffic: price position, main image, reviews and stock availability.'); }
    // 3 traffic down, conversion up
    if (dSes !== null && dCvr !== null && dSes < -0.05 && dCvr > 0.05) { what.push('Fewer sessions (' + pct(dSes) + ') but conversion improved ' + pct(dCvr) + ' — the audience is smaller and better qualified.'); next.push('Increase top-of-funnel: sponsored placements on best converters, and refresh listing keywords to win back organic traffic.'); }
    // 4 both down
    if (dSes !== null && dCvr !== null && dSes < -0.05 && dCvr < -0.05) { what.push('Both traffic and conversion declined — check for listing suppression, stock-outs, or a competitor price move.'); next.push('Run an account-health and Buy Box check first; then a competitor price scan on the top 10 SKUs.'); }
    // 5 ROAS
    if (n.roas !== null) {
      if (n.roas < 2) { what.push('Ads returned ' + n.roas.toFixed(2) + 'x — below the 2x line where most catalogues lose money after fees.'); next.push('Cut campaigns with ACoS above product margin, move the budget to the top 3 ROAS campaigns, and add negative keywords from the search-term report.'); }
      else if (n.roas < 3) { what.push('Ads returned ' + n.roas.toFixed(2) + 'x — profitable only on high-margin SKUs.'); next.push('Pause ads on SKUs under 30% margin; keep budget on hero products.'); }
      else { what.push('Ads returned a healthy ' + n.roas.toFixed(2) + 'x' + (dRoas !== null ? ' (' + (dRoas >= 0 ? 'up ' : 'down ') + pct(dRoas) + ' MoM)' : '') + '.'); if (dRoas !== null && dRoas < -0.1) next.push('ROAS slipped ' + pct(dRoas) + ' — pull the search-term report, add negatives for the new wasted terms, and hold budget flat until efficiency recovers.'); else if (dRoas === null || dRoas >= 0) next.push('Scale winning campaigns by 15–20% budget while ROAS holds above 3x; watch TACOS as the guardrail.'); }
    }
    // 6 TACOS
    if (n.tacos !== null && n.tacos > 0.15) { what.push('TACOS is ' + rptFmtPct(n.tacos) + ' — ads are carrying ' + rptFmtPct(n.ad_share) + ' of revenue, organic is not growing on its own.'); next.push('Invest in organic rank: listing SEO on the top ad-driven SKUs so paid traffic converts into ranking.'); }
    // 7 AOV
    if (dAov !== null && dAov < -0.05) { what.push('Average order value fell ' + pct(dAov) + ' to ' + rptFmtMoney(n.aov, cur) + '.'); next.push('Add bundles and a free-shipping threshold just above the current AOV to lift basket size.'); }
    else if (dAov !== null && dAov > 0.05) { what.push('Average order value rose ' + pct(dAov) + ' to ' + rptFmtMoney(n.aov, cur) + ' — bundles/upsells are working.'); }
    // 8 spend up, revenue flat
    if (dSpend !== null && dRev !== null && dSpend > 0.15 && dRev < 0.05) { what.push('Ad spend rose ' + pct(dSpend) + ' while revenue stayed flat — the extra budget did not buy growth.'); next.push('Roll spend back to last month\'s level and re-test with a tighter keyword set.'); }
    // 9 returns
    if (n.return_rate !== null && n.return_rate > 0.05) { what.push('Return rate is ' + rptFmtPct(n.return_rate) + ' — above the 5% comfort line.'); next.push('Read the return reasons; fix sizing/description mismatches on the top-returned SKUs before spending more on ads.'); }
    // 10 impressions vs orders
    if (dImp !== null && dOrd !== null && dImp > 0.1 && dOrd < 0) { what.push('Organic impressions grew ' + pct(dImp) + ' but orders fell — visibility improved, the listing is not converting the new eyeballs.'); next.push('A/B the main image and the first bullet on the SKUs with the biggest impression gain.'); }
    // 11 conversion benchmark
    if (n.cvr !== null && n.cvr < 0.01) { what.push('Conversion is ' + rptFmtPct(n.cvr, 2) + ' — under 1%, well below marketplace norms (2–5%).'); next.push('Prioritise a listing conversion audit: images, price, reviews, and delivery promise.'); }
    // 12 strong month
    if (dRev !== null && dRev > 0.15 && (dCvr === null || dCvr >= 0)) { next.push('Lock in the gain: secure stock cover for 60 days on the top sellers so growth is not capped by stock-outs.'); }
    // fallbacks
    if (!what.length) what.push('Performance is stable month-over-month with no metric moving more than 5%.');
    while (next.length < 3) {
      var fill = ['Refresh the top 10 listings\' keywords and images ahead of next month\'s campaign dates.', 'Review slow movers (0 sold in 30 days) and queue clearance or bundle promos.', 'Check account health and policy notices before the next campaign period.'];
      var f = fill[next.length % fill.length]; if (next.indexOf(f) === -1) next.push(f); else break;
    }
    return { what: what.slice(0,3), next: next.slice(0,3), now: n, prev: p };
  }
  function rptRows(d, ins){
    var cur = d.cur, n = ins.now, p = ins.prev;
    var rows = [
      ['Revenue', rptFmtMoney(n.revenue,cur), rptFmtMoney(p.revenue,cur), rptArrow(rptDelta(n.revenue,p.revenue), true)],
      ['Orders', rptFmtNum(n.orders), rptFmtNum(p.orders), rptArrow(rptDelta(n.orders,p.orders), true)],
      ['Sessions', rptFmtNum(n.sessions), rptFmtNum(p.sessions), rptArrow(rptDelta(n.sessions,p.sessions), true)],
      ['Conversion rate', rptFmtPct(n.cvr,2), rptFmtPct(p.cvr,2), rptArrow(rptDelta(n.cvr,p.cvr), true)],
      ['Average order value', rptFmtMoney(n.aov,cur), rptFmtMoney(p.aov,cur), rptArrow(rptDelta(n.aov,p.aov), true)],
      ['Ad spend', rptFmtMoney(n.ad_spend,cur), rptFmtMoney(p.ad_spend,cur), rptArrow(rptDelta(n.ad_spend,p.ad_spend), false)],
      ['Ad-attributed sales', rptFmtMoney(n.ad_sales,cur), rptFmtMoney(p.ad_sales,cur), rptArrow(rptDelta(n.ad_sales,p.ad_sales), true)],
      ['ROAS', n.roas===null?'—':n.roas.toFixed(2)+'x', p.roas===null?'—':p.roas.toFixed(2)+'x', rptArrow(rptDelta(n.roas,p.roas), true)],
      ['TACOS', rptFmtPct(n.tacos), rptFmtPct(p.tacos), rptArrow(rptDelta(n.tacos,p.tacos), false)],
      ['Organic revenue', rptFmtMoney(n.organic_rev,cur), rptFmtMoney(p.organic_rev,cur), rptArrow(rptDelta(n.organic_rev,p.organic_rev), true)]
    ];
    if (n.units !== null) rows.push(['Units sold', rptFmtNum(n.units), rptFmtNum(p.units), rptArrow(rptDelta(n.units,p.units), true)]);
    if (n.return_rate !== null) rows.push(['Return rate', rptFmtPct(n.return_rate), rptFmtPct(p.return_rate), rptArrow(rptDelta(n.return_rate,p.return_rate), false)]);
    if (n.impressions !== null) rows.push(['Organic impressions', rptFmtNum(n.impressions), rptFmtNum(p.impressions), rptArrow(rptDelta(n.impressions,p.impressions), true)]);
    return rows;
  }
  function rptMonthLabel(m){ if (!m) return 'This month'; var parts = m.split('-'); var names = ['January','February','March','April','May','June','July','August','September','October','November','December']; var mi = parseInt(parts[1],10)-1; return (names[mi] || m) + ' ' + parts[0]; }
  function rptHistory(){ try { var h = JSON.parse(localStorage.getItem(RPT_KEY) || '[]'); return Array.isArray(h) ? h : []; } catch(e){ return []; } }
  function rptSaveHistory(d){
    if (!d.month || d.now.revenue === null) return;
    var h = rptHistory().filter(function(x){ return x.month !== d.month; });
    h.push({ month: d.month, revenue: d.now.revenue, orders: d.now.orders, ad_spend: d.now.ad_spend, roas: rptMetrics(d.now).roas });
    h.sort(function(a,b){ return a.month < b.month ? -1 : 1; });
    while (h.length > 12) h.shift();
    try { localStorage.setItem(RPT_KEY, JSON.stringify(h)); } catch(e){}
  }
  function rptSparkline(h){
    if (!h || h.length < 2) return '';
    var w = 320, ht = 48, pad = 4, max = Math.max.apply(null, h.map(function(x){ return x.revenue || 0; })) || 1, min = Math.min.apply(null, h.map(function(x){ return x.revenue || 0; }));
    var pts = h.map(function(x, i){ var px = pad + i * ((w - 2*pad) / (h.length - 1)); var py = ht - pad - ((x.revenue || 0) - min) / ((max - min) || 1) * (ht - 2*pad); return px.toFixed(1) + ',' + py.toFixed(1); });
    return '<svg class="rpt-spark" viewBox="0 0 ' + w + ' ' + ht + '" width="' + w + '" height="' + ht + '" aria-label="Revenue, last ' + h.length + ' months"><polyline fill="none" stroke="#8B0D1A" stroke-width="2" points="' + pts.join(' ') + '"/>' +
      pts.map(function(pt){ var xy = pt.split(','); return '<circle cx="' + xy[0] + '" cy="' + xy[1] + '" r="2.5" fill="#8B0D1A"/>'; }).join('') + '</svg><div class="muted" style="font-size:11px">Revenue trend · ' + h[0].month + ' → ' + h[h.length-1].month + '</div>';
  }
  function rptRender(){
    var d = rptRead();
    if (d.now.revenue === null && d.now.orders === null) { var box = document.getElementById('rpt-preview'); if (box) box.innerHTML = '<p class="muted" style="font-size:13px">Fill in this month\'s numbers (or load the sample) to generate the report.</p>'; return null; }
    var ins = rptInsights(d), rows = rptRows(d, ins);
    rptSaveHistory(d);
    var hist = rptHistory();
    var html = '<div class="rpt-doc">' +
      '<div class="rpt-head"><div><div class="rpt-eyebrow">Monthly Performance Report</div><h2 class="rpt-title">' + escHtml(d.store) + ' · ' + escHtml(d.marketplace) + '</h2><div class="rpt-sub">' + escHtml(rptMonthLabel(d.month)) + ' vs previous month</div></div>' +
      '<div class="rpt-kpi"><div class="rpt-kpi-val">' + rptFmtMoney(ins.now.revenue, d.cur) + '</div><div class="rpt-kpi-lbl">Revenue ' + rptArrow(rptDelta(ins.now.revenue, ins.prev.revenue), true) + '</div></div></div>' +
      '<div class="rpt-grid">' + [['Orders', rptFmtNum(ins.now.orders), rptDelta(ins.now.orders, ins.prev.orders), true], ['Conversion', rptFmtPct(ins.now.cvr, 2), rptDelta(ins.now.cvr, ins.prev.cvr), true], ['AOV', rptFmtMoney(ins.now.aov, d.cur), rptDelta(ins.now.aov, ins.prev.aov), true], ['ROAS', ins.now.roas === null ? '—' : ins.now.roas.toFixed(2) + 'x', rptDelta(ins.now.roas, ins.prev.roas), true], ['TACOS', rptFmtPct(ins.now.tacos), rptDelta(ins.now.tacos, ins.prev.tacos), false]].map(function(k){ return '<div class="rpt-cell"><div class="rpt-cell-val">' + k[1] + '</div><div class="rpt-cell-lbl">' + k[0] + ' ' + rptArrow(k[2], k[3]) + '</div></div>'; }).join('') + '</div>' +
      '<table class="rpt-table"><thead><tr><th>Metric</th><th>This month</th><th>Last month</th><th>Change</th></tr></thead><tbody>' + rows.map(function(r){ return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td><td>' + r[3] + '</td></tr>'; }).join('') + '</tbody></table>' +
      '<div class="rpt-two"><div><h3>What happened</h3><ol>' + ins.what.map(function(x){ return '<li>' + escHtml(x) + '</li>'; }).join('') + '</ol></div><div><h3>Next month — actions</h3><ol>' + ins.next.map(function(x){ return '<li>' + escHtml(x) + '</li>'; }).join('') + '</ol></div></div>' +
      (d.notes ? '<div class="rpt-notes"><h3>Account health &amp; notes</h3><p>' + escHtml(d.notes) + '</p></div>' : '') +
      (hist.length >= 2 ? '<div class="rpt-trend">' + rptSparkline(hist) + '</div>' : '') +
      '<div class="rpt-foot">Prepared with the Monthly Performance Report tool · ' + new Date().toISOString().slice(0,10) + '</div></div>';
    var box = document.getElementById('rpt-preview'); if (box) box.innerHTML = html;
    return { d: d, ins: ins, rows: rows, html: html };
  }
  function rptPlain(md){
    var r = rptRender(); if (!r) { showToast('Fill in the numbers first.'); return ''; }
    var d = r.d, ins = r.ins, out = [];
    var strip = function(s){ return String(s).replace(/<[^>]+>/g,''); };
    out.push((md ? '# ' : '') + 'MONTHLY PERFORMANCE REPORT — ' + d.store + ' · ' + d.marketplace);
    out.push(rptMonthLabel(d.month) + ' vs previous month'); out.push('');
    out.push(md ? '| Metric | This month | Last month | Change |\n|---|---|---|---|' : 'METRICS');
    r.rows.forEach(function(row){ out.push(md ? '| ' + row[0] + ' | ' + row[1] + ' | ' + row[2] + ' | ' + strip(row[3]) + ' |' : '  ' + row[0] + ': ' + row[1] + ' (last ' + row[2] + ', ' + strip(row[3]) + ')'); });
    out.push(''); out.push((md ? '## ' : '') + 'WHAT HAPPENED'); ins.what.forEach(function(x, i){ out.push((i+1) + '. ' + x); });
    out.push(''); out.push((md ? '## ' : '') + 'NEXT MONTH — ACTIONS'); ins.next.forEach(function(x, i){ out.push((i+1) + '. ' + x); });
    if (d.notes) { out.push(''); out.push((md ? '## ' : '') + 'ACCOUNT HEALTH & NOTES'); out.push(d.notes); }
    return out.join('\n');
  }
  function rptCopy(md){
    var t = rptPlain(md); if (!t) return;
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(function(){ showToast(md ? 'Markdown copied.' : 'Report text copied.'); }, function(){ fallbackCopy(t); }); else fallbackCopy(t);
  }
  function rptDownload(){
    var r = rptRender(); if (!r) { showToast('Fill in the numbers first.'); return; }
    var css = '.rpt-doc{font-family:Georgia,serif;color:#111;max-width:820px;margin:0 auto;padding:40px}.rpt-head{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;border-bottom:2px solid #8B0D1A;padding-bottom:16px;margin-bottom:20px}.rpt-eyebrow{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8B0D1A}.rpt-title{margin:.2em 0;font-size:26px;font-weight:500}.rpt-sub{color:#666;font-size:13px}.rpt-kpi{text-align:right}.rpt-kpi-val{font-size:30px;font-weight:600}.rpt-kpi-lbl{font-size:12px;color:#666}.rpt-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:20px}.rpt-cell{border:1px solid #e5e5e5;border-radius:10px;padding:10px;text-align:center}.rpt-cell-val{font-size:18px;font-weight:600}.rpt-cell-lbl{font-size:11px;color:#666}.rpt-table{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:22px}.rpt-table th,.rpt-table td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left}.rpt-table th{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#666}.rpt-two{display:grid;grid-template-columns:1fr 1fr;gap:24px}.rpt-two h3,.rpt-notes h3{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:#8B0D1A;margin:0 0 8px}.rpt-two ol{padding-left:18px;font-size:13.5px;line-height:1.55}.rpt-notes{margin-top:18px;font-size:13.5px}.rpt-trend{margin-top:18px}.rpt-foot{margin-top:28px;font-size:11px;color:#999;border-top:1px solid #eee;padding-top:10px}.rpt-good{color:#15803d}.rpt-bad{color:#b91c1c}.rpt-flat{color:#888}@media print{body{margin:0}.rpt-doc{padding:0}}';
    var doc = '<!doctype html><html><head><meta charset="utf-8"><title>Monthly Performance Report — ' + escHtml(r.d.store) + ' ' + escHtml(r.d.month) + '</title><style>' + css + '</style></head><body>' + r.html + '</body></html>';
    downloadBlob(new Blob([doc], {type:'text/html'}), 'performance-report-' + (r.d.month || 'month') + '.html');
    showToast('Report downloaded — open it and print to PDF.');
  }
  function loadReportSample(){
    var set = function(id, v){ var el = document.getElementById(id); if (el) el.value = v; };
    var now = new Date(); var ym = now.getFullYear() + '-' + String(now.getMonth()+1).padStart(2,'0');
    set('rpt-store','Glow Lab Official'); set('rpt-marketplace','Shopee'); set('rpt-month', ym); set('rpt-cur','₱');
    var now_ = {revenue:412500, orders:1375, sessions:61200, ad_spend:38800, ad_sales:121000, units:1810, returns:44, impressions:940000};
    var prev = {revenue:376900, orders:1348, sessions:52400, ad_spend:31200, ad_sales:118500, units:1720, returns:31, impressions:820000};
    RPT_FIELDS.forEach(function(f){ set('rpt-' + f[0] + '-now', now_[f[0]]); set('rpt-' + f[0] + '-prev', prev[f[0]]); });
    set('rpt-notes','Account health: Excellent. 1 listing policy notice cleared on the 12th. Stock-out on 2 hero SKUs for 5 days mid-month.');
    rptRender(); showToast('Sample month loaded.');
  }
  window.loadReportSample = loadReportSample; window.rptRender = rptRender; window.rptPlain = rptPlain; window.rptInsights = rptInsights; window.rptMetrics = rptMetrics; window.rptDownload = rptDownload;
  (function rptWire(){
    var b;
    if ((b = document.getElementById('rpt-sample-btn'))) b.addEventListener('click', loadReportSample);
    if ((b = document.getElementById('rpt-generate'))) b.addEventListener('click', function(){ if (rptRender()) showToast('Report generated.'); else showToast('Fill in this month\'s revenue and orders first.'); });
    if ((b = document.getElementById('rpt-download'))) b.addEventListener('click', rptDownload);
    if ((b = document.getElementById('rpt-copy-text'))) b.addEventListener('click', function(){ rptCopy(false); });
    if ((b = document.getElementById('rpt-copy-md'))) b.addEventListener('click', function(){ rptCopy(true); });
    var m = document.getElementById('rpt-month'); if (m && !m.value) { var n = new Date(); m.value = n.getFullYear() + '-' + String(n.getMonth()+1).padStart(2,'0'); }
  })();

  /* Setup audit listeners */
  var sampleBtn = document.getElementById('audit-sample-btn');
  if (sampleBtn) sampleBtn.addEventListener('click', loadAuditSample);

  var fileInput = document.getElementById('audit-file');
  if (fileInput) {
    fileInput.addEventListener('change', function(e){
      var file = e.target.files && e.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function(evt){
        var text = evt.target.result;
        var rows = parseCSV(text);
        if (!rows || rows.length === 0) {
          showToast('Could not parse CSV file. Ensure it has valid header columns.');
          return;
        }
        var plat = document.getElementById('audit-platform') ? document.getElementById('audit-platform').value : 'sea';
        runAudit(rows, plat);
        showToast('Uploaded & audited ' + rows.length + ' SKUs successfully!');
      };
      reader.readAsText(file);
    });
  }

  var platSelect = document.getElementById('audit-platform');
  if (platSelect) {
    platSelect.addEventListener('change', function(){
      if (currentAuditRows && currentAuditRows.length > 0) {
        runAudit(currentAuditRows, platSelect.value);
      }
    });
  }

  var expCsvBtn = document.getElementById('audit-export-csv');
  if (expCsvBtn) expCsvBtn.addEventListener('click', exportAuditCSV);

  var expHtmlBtn = document.getElementById('audit-export-html');
  if (expHtmlBtn) expHtmlBtn.addEventListener('click', exportAuditHTML);

  var copySumBtn = document.getElementById('audit-copy-summary');
  if (copySumBtn) copySumBtn.addEventListener('click', copyAuditSummary);

  var drawerClose = document.getElementById('audit-drawer-close');
  if (drawerClose) drawerClose.addEventListener('click', closeAuditDrawer);

  var drawerBackdrop = document.getElementById('audit-drawer-backdrop');
  if (drawerBackdrop) drawerBackdrop.addEventListener('click', closeAuditDrawer);

  var sortHeaders = document.querySelectorAll('#audit-table th[data-sort]');
  sortHeaders.forEach(function(th){
    th.addEventListener('click', function(){
      var col = th.dataset.sort;
      if (currentSortCol === col) {
        currentSortAsc = !currentSortAsc;
      } else {
        currentSortCol = col;
        currentSortAsc = col === 'score' ? false : true;
      }
      sortAndRenderAuditTable();
    });
  });

  try {
    var savedAudit = JSON.parse(localStorage.getItem('audit-v1') || 'null');
    if (savedAudit && savedAudit.rows && savedAudit.rows.length > 0) {
      if (platSelect && savedAudit.platform) platSelect.value = savedAudit.platform;
      runAudit(savedAudit.rows, savedAudit.platform || 'sea');
    }
  } catch(e) {}

  calcAdEfficiency();
  calcVoucherSim();
  audit();
})();
"""


def build_tools():
    p = PROFILE
    wa_msg = ("Hi Jamie! I tested your Listing Scanner and I'd like to book a "
              "Storefront & Compliance Overhaul for my shop.")
    wa_href = f"https://wa.me/{p['whatsapp']}?text={_url_quote(wa_msg)}" if p.get("whatsapp") else "#"

    body = f'''<header id="top"><div class="wrap">
<p class="eyebrow muted">MICRO-SAAS · SELLERGUARD v2.0</p>
<h1 style="margin-top:.75rem">E-Commerce Operations Command Center</h1>
<p class="muted" style="margin-top:1rem;max-width:44rem">
Part of the 7-tool operations suite: listing policy &amp; SEO scanner, bulk marketplace audit scorecard,
ad-spend efficiency calculator, and campaign margin simulator — built on the exact math senior e-commerce
and marketplace-ops roles are hired to know.
</p>
</div></header>
<main><div class="wrap">

<nav class="suite-nav" role="tablist" aria-label="Tool suite">
  <button class="suite-tab on" type="button" data-tab="panel-scanner"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-shield"/></svg>Listing Policy &amp; SEO Scanner</button>
  <button class="suite-tab" type="button" data-tab="panel-tacos"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-chart"/></svg>Ad Efficiency &amp; TACOS Calculator</button>
  <button class="suite-tab" type="button" data-tab="panel-voucher"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-tag"/></svg>Campaign Voucher &amp; Margin Simulator</button>
  <button class="suite-tab" type="button" data-tab="panel-audit"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-search"/></svg>Marketplace Audit Scorecard</button>
  <button class="suite-tab" type="button" data-tab="panel-classify"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-box"/></svg>Product Performance Classifier</button>
  <button class="suite-tab" type="button" data-tab="panel-report"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-trend"/></svg>Monthly Performance Report</button>
</nav>

<!-- ============================================================ MODULE 1 -->
<section id="panel-scanner" class="suite-panel on">
  <div class="howto">
    <b>What this does:</b> checks a product listing for wording that gets it demoted,
    flagged or taken down — before you publish it.
    <ol>
      <li>Pick the marketplace you're selling on (each has its own character limit and rules).</li>
      <li>Pick the category — medical and beauty listings are policed harder than general merchandise.</li>
      <li>Paste your title and description. Flagged words are highlighted as you type.</li>
      <li>Hit <b>Auto-Sanitize All</b> to replace every flagged phrase with a compliant alternative.</li>
    </ol>
  </div>
  <div class="plat-row" role="tablist" aria-label="Target platform">
    <button class="plat-btn" type="button" data-plat="amazon"><span class="plat-dot" style="background:#f59e0b"></span> Amazon</button>
    <button class="plat-btn" type="button" data-plat="shopify"><span class="plat-dot" style="background:#22c55e"></span> Shopify / Google</button>
    <button class="plat-btn" type="button" data-plat="tiktok"><span class="plat-dot" style="background:#e5e7eb"></span> TikTok Shop</button>
    <button class="plat-btn" type="button" data-plat="etsy"><span class="plat-dot" style="background:#f97316"></span> Etsy</button>
    <button class="plat-btn on" type="button" data-plat="sea"><span class="plat-dot" style="background:#8B0D1A"></span> Shopee &amp; Lazada</button>
  </div>
  <p id="plat-note" class="muted" style="font-size:12.5px;margin:.75rem 0 0;max-width:44rem"></p>

  <div class="tool-grid">
    <!-- Left Column: Inputs & Editor -->
    <div class="tool-box">
      <div class="field-row">
        <label class="eyebrow muted" for="risk-cat" style="display:block;margin-bottom:.4rem">Category Risk Profile</label>
        <select id="risk-cat" class="tool-select">
          <option value="health">Health, Beauty &amp; Skincare (Strict Whitening / Acne / Anti-aging rules)</option>
          <option value="medical">Medical Devices &amp; Supplements (FDA claims, Cure &amp; Disease rules)</option>
          <option value="general" selected>General Merchandise &amp; Home (Superlative &amp; DTI Rules)</option>
          <option value="electronics">Electronics &amp; Gadgets (Authenticity &amp; Warranty Policy)</option>
        </select>
        <p id="cat-note" class="cat-note"></p>
      </div>

      <div class="field-row">
        <div class="field-head">
          <label class="eyebrow muted" for="listing-title">Listing Title</label>
          <div class="count-badge"><span id="char-num">0</span> / <span id="char-max">255</span> chars (<span id="char-status">Optimal: 80–120</span>)</div>
        </div>
        <div class="hl-wrap">
          <div id="title-hl" class="hl-backdrop" aria-hidden="true"></div>
          <textarea id="listing-title" class="tool-textarea" rows="3" placeholder="Paste your product title here... (e.g. K-PICK Blood Glucose Monitor Set 100 Strips FDA Approved 100% Guaranteed Cure)"></textarea>
        </div>
      </div>

      <div id="etsy-tag-wrap" class="field-row" style="display:none">
        <div class="field-head">
          <label class="eyebrow muted" for="etsy-tags">Etsy Tags (comma-separated, 13 max)</label>
          <div class="count-badge"><span id="etsy-tag-count">0</span> / 13 tags</div>
        </div>
        <input id="etsy-tags" class="tool-select" style="height:44px" placeholder="handmade jewelry, boho earrings, gift for her, ...">
      </div>

      <div id="shopify-meta-wrap" class="field-row" style="display:none">
        <div class="field-head">
          <label class="eyebrow muted" for="shopify-meta">Meta Description (Google Search snippet)</label>
          <div class="count-badge"><span id="shopify-meta-count">0</span> / 160 chars</div>
        </div>
        <textarea id="shopify-meta" class="tool-textarea" rows="2" placeholder="The one or two sentences that show up under your link in Google Search..."></textarea>
      </div>

      <div class="field-row">
        <div class="field-head">
          <label class="eyebrow muted" for="listing-desc">Description or Bullet Points (Optional)</label>
          <div class="count-badge"><span id="desc-word-num">0</span> words</div>
        </div>
        <div class="hl-wrap">
          <div id="desc-hl" class="hl-backdrop" aria-hidden="true"></div>
          <textarea id="listing-desc" class="tool-textarea" rows="4" placeholder="Paste your bullet points or description here to scan for hidden therapeutic claims, unauthorized superlatives, or off-platform contact links..."></textarea>
        </div>
      </div>

      <div class="action-bar">
        <button id="btn-fix" class="btn btn-sm" type="button">
          <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/></svg>Auto-Sanitize All
        </button>
        <button id="btn-sample" class="btn ghost btn-sm" type="button">Load High-Risk Sample</button>
        <button id="btn-copy" class="btn ghost btn-sm" type="button">
          <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>Copy Clean Text
        </button>
        <button id="btn-report" class="btn ghost btn-sm" type="button">
          <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/></svg>Copy Findings Report
        </button>
        <button id="btn-clear" class="btn btn-text" type="button">Clear</button>
      </div>
    </div>

    <!-- Right Column: Audit Dashboard -->
    <div>
      <div class="tool-box">
        <div class="score-card">
          <div id="score-dial" class="score-dial"><span id="score-num">--</span><small>Score</small></div>
          <div class="score-info">
            <h4 id="score-status">Ready to Scan</h4>
            <p id="score-desc">Enter listing text to run policy checks.</p>
          </div>
        </div>

        <div class="findings-head">
          <span class="eyebrow acc">COMPLIANCE &amp; SEO FINDINGS</span>
          <span id="findings-summary" class="count-badge">Waiting for input...</span>
        </div>

        <div id="findings-list" class="flag-list">
          <!-- Dynamic findings inserted here -->
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================================ MODULE 2 -->
<section id="panel-tacos" class="suite-panel">
  <div class="howto">
    <b>What this does:</b> tells you whether your ads are still making money, or quietly
    eating the margin on every order.
    <ol>
      <li>Enter what one unit sells for, what it costs you, and the platform's cut.</li>
      <li>Enter what you spend on ads to win one order.</li>
      <li>Optionally add your monthly revenue and ad spend for a true store-wide TACOS.</li>
      <li>Read the verdict: green means the ads pay for themselves, red means they don't.</li>
    </ol>
  </div>
  <div class="tool-grid">
    <div class="tool-box">
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="ae-price">Selling Price (₱)</label>
        <input id="ae-price" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 799"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="ae-cogs">Product Cost / COGS (₱)</label>
        <input id="ae-cogs" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 320"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="ae-fee">Platform Fee (%)</label>
        <input id="ae-fee" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 8"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="ae-ad-order">Ad Spend per Order (₱)</label>
        <input id="ae-ad-order" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 90"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="ae-mon-rev">Monthly Revenue (₱) <span class="muted">— optional, for TACOS</span></label>
        <input id="ae-mon-rev" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 250000"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="ae-mon-ad">Monthly Ad Spend (₱) <span class="muted">— optional, for TACOS</span></label>
        <input id="ae-mon-ad" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 35000"></div>
    </div>
    <div class="tool-box">
      <div class="metrics-grid">
        <div class="metric-box"><div class="m-val" id="ae-margin-val">₱0.00</div><div class="m-lbl">Contribution Margin</div><div class="m-sub" id="ae-margin-sub"></div></div>
        <div class="metric-box"><div class="m-val" id="ae-tacos-val">0%</div><div class="m-lbl">True TACOS</div><div class="m-sub" id="ae-tacos-sub"></div></div>
        <div class="metric-box"><div class="m-val" id="ae-roas-val">—</div><div class="m-lbl">Breakeven ROAS</div><div class="m-sub" id="ae-roas-sub"></div></div>
      </div>
      <div id="ae-status-box" class="flag-item" style="align-items:center;text-align:center">
        <span id="ae-status-val" class="eyebrow" style="font-size:13px">Enter figures to evaluate</span>
      </div>
    </div>
  </div>
</section>

<!-- ============================================================ MODULE 3 -->
<section id="panel-voucher" class="suite-panel">
  <div class="howto">
    <b>What this does:</b> stacks a flash sale, a store voucher and the platform's commission
    on top of each other, so you see the real payout before a 9.9 or 11.11 sale runs you at a loss.
    <ol>
      <li>Enter your regular price and what the product costs you.</li>
      <li>Pick your marketplace — the commission rate fills in automatically.</li>
      <li>Stack the discounts you're planning. The alert turns red the moment the payout drops below cost.</li>
      <li>Check <b>Max Safe Discount</b> for the deepest total discount you can still afford.</li>
    </ol>
  </div>
  <div class="tool-grid">
    <div class="tool-box">
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="vs-regular">Regular Price (₱)</label>
        <input id="vs-regular" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 999"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="vs-cogs">Product Cost / COGS (₱)</label>
        <input id="vs-cogs" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 420"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="vs-flash">Flash Sale Discount (%)</label>
        <input id="vs-flash" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 20"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="vs-store">Store Voucher (%)</label>
        <input id="vs-store" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 10"></div>
      <div class="field-row">
        <label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="vs-preset">Marketplace (fills the commission)</label>
        <select id="vs-preset" class="tool-select">
          <option value="">Custom — I'll type it myself</option>
          <option value="6">Shopee PH — approx. 6%</option>
          <option value="7">Lazada PH — approx. 7%</option>
          <option value="5">TikTok Shop PH — approx. 5%</option>
          <option value="15">Amazon (most categories) — approx. 15%</option>
          <option value="6.5">Etsy (fees + payment) — approx. 6.5%</option>
        </select>
        <p class="cat-note">Indicative rates only — confirm the exact commission in your own Seller Centre, it varies by category and seller programme.</p>
      </div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="vs-comm">Platform Commission (%)</label>
        <input id="vs-comm" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 6"></div>
      <div class="field-row"><label class="eyebrow muted" style="display:block;margin-bottom:.4rem" for="vs-target">Target Margin per Order (₱) <span class="muted">— 0 = breakeven</span></label>
        <input id="vs-target" type="number" min="0" step="any" class="tool-select" style="height:44px" placeholder="e.g. 100"></div>
    </div>
    <div class="tool-box">
      <div class="metrics-grid">
        <div class="metric-box"><div class="m-val" id="vs-final-val">₱0.00</div><div class="m-lbl">Final Checkout Price</div><div class="m-sub" id="vs-final-sub"></div></div>
        <div class="metric-box"><div class="m-val" id="vs-payout-val">₱0.00</div><div class="m-lbl">Net Seller Payout</div><div class="m-sub" id="vs-payout-sub"></div></div>
        <div class="metric-box"><div class="m-val" id="vs-margin-val">₱0.00</div><div class="m-lbl">Net Margin</div><div class="m-sub" id="vs-margin-sub"></div></div>
        <div class="metric-box"><div class="m-val" id="vs-max-val">—</div><div class="m-lbl">Max Safe Discount</div><div class="m-sub" id="vs-max-sub"></div></div>
      </div>
      <div id="vs-status-box" class="flag-item" style="align-items:center;text-align:center">
        <span id="vs-status-val" class="eyebrow" style="font-size:13px">Enter figures to evaluate</span>
      </div>
    </div>
  </div>
</section>

<!-- ============================================================ MODULE 4: AUDIT SCORECARD -->
<section id="panel-audit" class="suite-panel">
  <div class="howto">
    <b>What this does:</b> bulk audits your marketplace listing catalogue (Amazon, eBay, Shopee, Lazada, TikTok Shop) against conversion, SEO, and compliance standards — delivering an instant SKU health score and prioritized fixes.
    <ol>
      <li>Select your target marketplace platform to set optimal title length limits and weighted rules.</li>
      <li>Upload your catalogue CSV export, or click <b>Load Sample (25 SKUs)</b> for an instant demonstration.</li>
      <li>Review the catalogue health score strip, top fixes ranking, and SKU breakdown table.</li>
      <li>Click any SKU row or the Inspect button to open the full listing inspection drawer with exact remediation steps.</li>
    </ol>
  </div>

  <div class="audit-toolbar">
    <div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap">
      <label class="eyebrow muted" for="audit-platform">Platform:</label>
      <select id="audit-platform" class="tool-select" style="width:auto;min-width:145px;height:38px;padding:.4rem .8rem">
        <option value="amazon">Amazon</option>
        <option value="ebay">eBay</option>
        <option value="sea" selected>Shopee / Lazada</option>
        <option value="tiktok">TikTok Shop</option>
        <option value="generic">Generic Marketplace</option>
      </select>
    </div>

    <div style="display:flex;gap:.6rem;align-items:center;flex-wrap:wrap">
      <label class="btn ghost file-btn">
        <svg class="ico" viewBox="0 0 24 24" style="width:14px;height:14px;margin-right:.4rem" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4m14-7-5-5-5 5m5-5v12"/></svg>
        <span>Upload CSV</span>
        <input type="file" id="audit-file" accept=".csv,text/csv">
      </label>
      <button class="btn" id="audit-sample-btn" type="button">Load Sample (25 SKUs)</button>
    </div>

    <div style="margin-left:auto;display:flex;gap:.5rem;flex-wrap:wrap">
      <button class="btn ghost" id="audit-export-csv" type="button">Export CSV</button>
      <button class="btn ghost" id="audit-export-html" type="button">Export Report (HTML)</button>
      <button class="btn ghost" id="audit-copy-summary" type="button">Copy Summary</button>
    </div>
  </div>

  <!-- Summary strip -->
  <div class="metrics-grid cols-7" id="audit-summary-strip">
    <div class="metric-box">
      <div class="m-val" id="audit-overall-score">—</div>
      <div class="m-lbl">Catalogue Health Score</div>
      <div class="m-sub" id="audit-overall-status">No catalogue loaded</div>
    </div>
    <div class="metric-box">
      <div class="m-val" id="audit-total-skus">0</div>
      <div class="m-lbl">Total Audited SKUs</div>
      <div class="m-sub" id="audit-platform-label">Select platform</div>
    </div>
    <div class="metric-box">
      <div class="m-val" id="audit-crit-count" style="color:#f87171">0</div>
      <div class="m-lbl">Critical Risk SKUs (&lt;50)</div>
      <div class="m-sub">Urgent fixes needed</div>
    </div>
    <div class="metric-box">
      <div class="m-val" id="audit-good-count" style="color:#4ade80">0</div>
      <div class="m-lbl">Optimized SKUs (80+)</div>
      <div class="m-sub">High conversion ready</div>
    </div>
    <div class="metric-box">
      <div class="m-val" id="audit-avg-title-len">0</div>
      <div class="m-lbl">Avg Title Length</div>
      <div class="m-sub" id="audit-title-target">Target: 80–120 chars</div>
    </div>
    <div class="metric-box">
      <div class="m-val" id="audit-low-img-pct">0%</div>
      <div class="m-lbl">&lt; 5 Images Ratio</div>
      <div class="m-sub">Lacks visual proof</div>
    </div>
    <div class="metric-box">
      <div class="m-val" id="audit-zero-rev-pct">0%</div>
      <div class="m-lbl">0 Reviews Ratio</div>
      <div class="m-sub">Cold-start risk</div>
    </div>
  </div>

  <!-- Top 10 Fixes -->
  <div class="tool-box" style="margin-top:1.5rem">
    <div class="field-head">
      <span class="eyebrow muted">PRIORITY ACTION PLAN</span>
      <span class="muted" style="font-size:12px">Ranked by Impact: (Affected SKUs × Issue Severity)</span>
    </div>
    <h3 style="font-size:1.25rem;font-weight:400;margin:.4rem 0 1rem">Top Catalogue Fixes</h3>
    <div id="audit-top-fixes" class="top-fixes-list">
      <p class="muted" style="font-size:13px">Load a catalogue CSV or click "Load Sample" to see prioritized fixes.</p>
    </div>
  </div>

  <!-- SKU Scorecard Table -->
  <div class="tool-box" style="margin-top:1.5rem">
    <div class="field-head">
      <span class="eyebrow muted">SKU BREAKDOWN</span>
      <span class="muted" style="font-size:12px">Click any row to open the full listing inspection drawer</span>
    </div>
    <div class="audit-table-wrap">
      <table class="audit-table" id="audit-table">
        <thead>
          <tr>
            <th data-sort="sku">SKU ↕</th>
            <th data-sort="title">Product Title ↕</th>
            <th data-sort="score" style="text-align:center">Health Score ↕</th>
            <th data-sort="imageCount" style="text-align:center">Images</th>
            <th data-sort="reviews" style="text-align:center">Reviews</th>
            <th data-sort="price" style="text-align:right">Price</th>
            <th data-sort="stock" style="text-align:right">Stock</th>
            <th>Primary Recommended Fix</th>
            <th style="text-align:center">Action</th>
          </tr>
        </thead>
        <tbody id="audit-tbody">
          <tr><td colspan="9" style="text-align:center;padding:2rem;" class="muted">No data loaded yet. Upload a CSV or load sample.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section id="panel-classify" class="suite-panel">
  <div class="howto">
    <b>What this does:</b> turns a stock &amp; sales export into one clear action per product — expired, clearance, flash sale, bundle, promo push, restock, or scale — so a slow-moving catalogue becomes a to-do list.
    <ol>
      <li>Upload a CSV with columns like <code>sku, name, brand, stock, sold_30d, price, cost, expiry, image</code> (headers are matched flexibly), or click <b>Load Sample (40 SKUs)</b>.</li>
      <li>Adjust the thresholds if your category moves faster or slower.</li>
      <li>Filter by action, brand or search, then export the CSV or copy the action plan grouped by what to do.</li>
    </ol>
  </div>

  <div class="audit-toolbar">
    <div style="display:flex;gap:.6rem;align-items:center;flex-wrap:wrap">
      <label class="btn ghost file-btn">
        <span>Upload CSV</span>
        <input type="file" id="cls-file" accept=".csv,text/csv">
      </label>
      <button class="btn" id="cls-sample-btn" type="button">Load Sample (40 SKUs)</button>
    </div>
    <div style="margin-left:auto;display:flex;gap:.5rem;flex-wrap:wrap">
      <button class="btn ghost" id="cls-export-csv" type="button">Export CSV</button>
      <button class="btn ghost" id="cls-copy-plan" type="button">Copy Action Plan</button>
    </div>
  </div>

  <details class="cls-settings">
    <summary>Thresholds — click to adjust</summary>
    <div class="cls-settings-grid">
      <label>Clearance if expiring within <input type="number" id="cls-t-clear" value="60" min="1"> days</label>
      <label>Bundle / voucher if expiring within <input type="number" id="cls-t-bundle" value="120" min="1"> days</label>
      <label>Flash sale needs at least <input type="number" id="cls-t-flash" value="10" min="0"> units in stock</label>
      <label>Bundle if stock covers <input type="number" id="cls-t-months" value="3" min="1" step="0.5"> + months</label>
      <label>Scale if sold &ge; <input type="number" id="cls-t-scale" value="30" min="1"> in 30 days and stock is below that</label>
    </div>
  </details>

  <div class="metrics-grid cols-7" id="cls-kpis">
    <div class="metric-box"><div class="m-val" id="cls-k-expired" style="color:#f87171">0</div><div class="m-lbl">Expired stock</div><div class="m-sub">pull from listings</div></div>
    <div class="metric-box"><div class="m-val" id="cls-k-clear" style="color:#f87171">0</div><div class="m-lbl">Clearance sale</div><div class="m-sub">expiring soon</div></div>
    <div class="metric-box"><div class="m-val" id="cls-k-flash" style="color:#fb923c">0</div><div class="m-lbl">Flash sale</div><div class="m-sub">0 sold in 30 days</div></div>
    <div class="metric-box"><div class="m-val" id="cls-k-bundle" style="color:#facc15">0</div><div class="m-lbl">Bundle / voucher</div><div class="m-sub">months of stock</div></div>
    <div class="metric-box"><div class="m-val" id="cls-k-promo" style="color:#facc15">0</div><div class="m-lbl">Promo push</div><div class="m-sub">selling, but slowly</div></div>
    <div class="metric-box"><div class="m-val" id="cls-k-scale" style="color:#4ade80">0</div><div class="m-lbl">Scale</div><div class="m-sub">restock &amp; advertise</div></div>
    <div class="metric-box"><div class="m-val" id="cls-k-noimg">0</div><div class="m-lbl">No image</div><div class="m-sub">needs photo / content</div></div>
  </div>

  <div class="tool-box" style="margin-top:1.5rem">
    <div class="cls-filters">
      <div class="cls-tabs" id="cls-tabs">
        <button class="cls-tab on" type="button" data-f="all">All</button>
        <button class="cls-tab" type="button" data-f="Expired stock"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-alert"/></svg>Expired</button>
        <button class="cls-tab" type="button" data-f="Clearance sale"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-clock"/></svg>Clearance</button>
        <button class="cls-tab" type="button" data-f="Flash sale"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-flame"/></svg>Flash sale</button>
        <button class="cls-tab" type="button" data-f="Bundle / voucher"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-gift"/></svg>Bundle</button>
        <button class="cls-tab" type="button" data-f="Promo push"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-mega"/></svg>Promo</button>
        <button class="cls-tab" type="button" data-f="Scale"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-rocket"/></svg>Scale</button>
        <button class="cls-tab" type="button" data-f="Restock first">Restock</button>
        <button class="cls-tab" type="button" data-f="noimage"><svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-camera-off"/></svg>No image</button>
      </div>
      <div>
        <select id="cls-brand" class="tool-select" style="width:auto;min-width:140px"><option value="">All brands</option></select>
        <input id="cls-q" class="tool-select" type="search" placeholder="Search name / SKU" style="width:200px">
      </div>
    </div>
    <p class="muted" id="cls-status" style="font-size:12px;margin:.6rem 0 0">No data loaded yet.</p>
    <div class="audit-table-wrap">
      <table class="audit-table" id="cls-table">
        <thead><tr>
          <th>Action</th><th>Product</th><th>Brand</th><th>Stock</th><th>Sold / 30d</th><th>Months of stock</th><th>Expiry</th><th>Price</th><th>Why</th>
        </tr></thead>
        <tbody id="cls-tbody">
          <tr><td colspan="9" style="text-align:center;padding:2rem;" class="muted">Upload a CSV or load the sample.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section id="panel-report" class="suite-panel">
  <div class="howto">
    <b>What this does:</b> turns this month's and last month's numbers into a client-ready one-page report — every metric with its month-over-month change, plus three plain-language findings and three actions written from the numbers (rules, not guesswork).
    <ol>
      <li>Type this month's and last month's figures from Seller Center / Business Insights (or click <b>Load Sample</b>).</li>
      <li>Click <b>Generate</b> — the report renders below as a document.</li>
      <li>Download it as HTML (print to PDF), or copy as text / Markdown for email and Notion. The last 12 months are remembered for the trend line.</li>
    </ol>
  </div>

  <div class="rpt-form">
    <div class="rpt-meta">
      <div><label>Store</label><input type="text" id="rpt-store" placeholder="Store name" class="tool-select"></div>
      <div><label>Marketplace</label><input type="text" id="rpt-marketplace" placeholder="Shopee / Amazon / eBay…" class="tool-select"></div>
      <div><label>Month</label><input type="month" id="rpt-month" class="tool-select"></div>
      <div><label>Currency</label><select id="rpt-cur" class="tool-select"><option value="₱">₱ PHP</option><option value="$">$ USD</option><option value="A$">A$ AUD</option><option value="£">£ GBP</option><option value="€">€ EUR</option><option value="S$">S$ SGD</option></select></div>
    </div>
    <div class="rpt-rows">
    <div class="rpt-row rpt-row-head"><span></span><span>This month</span><span>Last month</span></div>
      <div class="rpt-row"><label>Revenue</label><input type="number" id="rpt-revenue-now" placeholder="this month"><input type="number" id="rpt-revenue-prev" placeholder="last month"></div>
      <div class="rpt-row"><label>Orders</label><input type="number" id="rpt-orders-now" placeholder="this month"><input type="number" id="rpt-orders-prev" placeholder="last month"></div>
      <div class="rpt-row"><label>Sessions / visits</label><input type="number" id="rpt-sessions-now" placeholder="this month"><input type="number" id="rpt-sessions-prev" placeholder="last month"></div>
      <div class="rpt-row"><label>Ad spend</label><input type="number" id="rpt-ad_spend-now" placeholder="this month"><input type="number" id="rpt-ad_spend-prev" placeholder="last month"></div>
      <div class="rpt-row"><label>Ad-attributed sales</label><input type="number" id="rpt-ad_sales-now" placeholder="this month"><input type="number" id="rpt-ad_sales-prev" placeholder="last month"></div>
      <div class="rpt-row"><label>Units sold<small>optional</small></label><input type="number" id="rpt-units-now" placeholder="this month"><input type="number" id="rpt-units-prev" placeholder="last month"></div>
      <div class="rpt-row"><label>Returns (orders)<small>optional</small></label><input type="number" id="rpt-returns-now" placeholder="this month"><input type="number" id="rpt-returns-prev" placeholder="last month"></div>
      <div class="rpt-row"><label>Organic impressions<small>optional</small></label><input type="number" id="rpt-impressions-now" placeholder="this month"><input type="number" id="rpt-impressions-prev" placeholder="last month"></div>
    </div>
    <div style="margin-top:1rem"><label>Account health &amp; notes <span style="text-transform:none;letter-spacing:0;opacity:.7">(optional)</span></label><textarea id="rpt-notes" class="tool-textarea" rows="2" placeholder="Policy notices, stock-outs, campaign dates, anything the client should know"></textarea></div>
    <div class="rpt-actions">
      <div><button class="btn" id="rpt-generate" type="button">Generate report</button>
      <button class="btn ghost" id="rpt-sample-btn" type="button">Load sample</button></div>
      <div><button class="btn ghost" id="rpt-download" type="button">Download HTML</button>
      <button class="btn ghost" id="rpt-copy-text" type="button">Copy text</button>
      <button class="btn ghost" id="rpt-copy-md" type="button">Copy Markdown</button></div>
    </div>
  </div>

  <div id="rpt-preview" class="rpt-preview"><p class="muted" style="font-size:13px">Fill in this month's numbers (or load the sample) to generate the report.</p></div>
</section>

<!-- Detail Slide-Over Drawer -->
<div id="audit-drawer-backdrop" class="drawer-backdrop" aria-hidden="true"></div>
<aside id="audit-drawer" class="drawer" aria-hidden="true" role="dialog" aria-label="SKU Audit Details">
  <div class="drawer-head">
    <div>
      <span class="pro-badge" id="drawer-sku-badge">SKU INSPECTION</span>
      <h3 id="drawer-title" style="font-size:1.15rem;font-weight:500;margin-top:.4rem;line-height:1.3">Product Name</h3>
      <p class="muted" id="drawer-sku-id" style="font-size:12px;font-family:monospace;margin-top:.2rem">SKU-000</p>
    </div>
    <button class="modal-close" id="audit-drawer-close" type="button" aria-label="Close drawer" style="position:static">&times;</button>
  </div>
  <div class="drawer-body">
    <div style="display:flex;align-items:center;justify-content:space-between;background:var(--glass);padding:1rem;border-radius:12px;border:1px solid var(--edge)">
      <div>
        <div class="eyebrow muted" style="font-size:10px">Overall SKU Health</div>
        <div style="font-size:1.8rem;font-family:'Cormorant Garamond',Georgia,serif;font-weight:600" id="drawer-score-val">0/100</div>
      </div>
      <div id="drawer-score-pill"></div>
    </div>
    <div class="eyebrow muted" style="margin-top:.5rem">Audit Checklist Breakdown</div>
    <div id="drawer-checks-list" style="display:flex;flex-direction:column;gap:.75rem"></div>
  </div>
</aside>

<!-- ============================================================ WORK WITH ME -->
<section class="work-card" style="margin-top:3.5rem">
  <span class="pro-badge">WORK WITH ME</span>
  <h3 class="serif">Like what the tools show? I do this for stores every week.</h3>
  <p>Catalogue audits, listing rebuilds, promo planning, monthly reporting — as a one-off project or an ongoing retainer.
  Send me your store link and what is slowing you down; I reply with what I would do, how long it takes, and a quote. No fixed plans, no subscriptions.</p>
  <div class="work-btns">
    <a class="btn" href="{E(wa_href)}" target="_blank" rel="noopener"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg>Message on WhatsApp</a>
    <a class="btn ghost" href="mailto:{E(PROFILE['email'])}?subject=Project%20inquiry%20from%20your%20tools%20page">Email me</a>
  </div>
</section>

</div></main>

<div id="toast" class="toast" aria-live="polite"></div>
{footer()}'''
    write("tools/index.html", shell("E-Commerce Operations Command Center — SellerGuard",
          "Global marketplace listing compliance scanner, TACOS/ad-efficiency calculator, and "
          "campaign voucher margin simulator for Amazon, Shopify, TikTok Shop, Etsy, Shopee & Lazada.",
          body, "tools", up="../", extra_js=TOOL_JS))


def build_404():
    # Root-absolute links (up="/") - a 404 can be served at ANY depth, so
    # relative paths would break the stylesheet and every link on it.
    body = f'''<header id="top"><div class="wrap">
<p class="eyebrow muted">404</p>
<h1 style="margin-top:.75rem">Page not found</h1>
<p class="muted" style="margin-top:1.25rem;max-width:34rem">That page does not exist,
or it moved. Here is everything else.</p>
</div></header>
<main><div class="wrap">
<section style="padding-top:1rem">
  <h2 class="eyebrow grouphead"><span>GO SOMEWHERE</span><span class="rule"></span></h2>
  <div class="cards">
    <a class="card rv" href="/work/index.html"><div class="body">
      <h3>All work</h3>
      <p class="sum">{len(PROJECTS)} projects across {len(DISCIPLINES)} disciplines.</p>
      <span class="more">Browse the work &#8594;</span></div></a>
    <a class="card rv" href="/tools/index.html"><div class="body">
      <h3>Tools &amp; SaaS</h3>
      <p class="sum">Marketplace listing compliance &amp; SEO audit scanner.</p>
      <span class="more">Launch tool &#8594;</span></div></a>
    <a class="card rv" href="/about.html"><div class="body">
      <h3>About</h3>
      <p class="sum">Background, expertise, tools and credentials.</p>
      <span class="more">Read about me &#8594;</span></div></a>
    <a class="card rv" href="/card.html"><div class="body">
      <h3>Digital card</h3>
      <p class="sum">Contact details, and save them straight to your phone.</p>
      <span class="more">Open the card &#8594;</span></div></a>
  </div>
  <p style="margin-top:3rem"><a class="more" href="/index.html">Back to the start</a></p>
</section>
</div></main>{footer()}'''
    write("404.html", shell("Page not found", "That page does not exist.", body, "",
                            up="/"))


# ------------------------------------------------- NFC card: standalone, tiny
def build_card():
    p = PROFILE
    vj = VCARD_JS % dict(last=p['last'], first=p['first'], name=p['name'], title=p['vcard_title'],
                         tel=p['tel'], email=p['email'], li=p['linkedin'], file=p['vcard_file'],
                         social="".join(f',"URL:{u}"' for _, _, u in socials()))
    company = (f'<p class="org">{E(p["company"])} &middot; {E(p["location"])}</p>'
               if p.get("company") else f'<p class="org">{E(p["location"])}</p>')
    write("card.html", f"""<!DOCTYPE html>
<html lang="en" data-theme="dark"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(p['name'])}</title>
<meta name="description" content="{E(p['subtitle_plain'])}">
<meta name="theme-color" content="#0B0B0B">
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="assets/images/favicon.png">
<link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png">
<script>(function(){{try{{var v=localStorage.getItem('jl-theme');if(v){{document.documentElement.setAttribute('data-theme',v);var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute('content',v==='light'?'#EFEBE4':'#0B0B0B');}}}}catch(e){{}}}})();</script>
<style>
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
:root{{
 --bg:#0B0B0B;--ink:#F5F2ED;--dim:rgba(245,242,237,.60);--acc:#8B0D1A;--acc-lift:#A81324;
 --glass:rgba(245,242,237,.055);--edge:rgba(245,242,237,.14);--edge-top:rgba(245,242,237,.30);
 --shade:rgba(0,0,0,.55);--blob1:rgba(139,13,26,.18);--blob2:rgba(139,13,26,.09);
}}
[data-theme="light"]{{
 --bg:#EFEBE4;--ink:#12100F;--dim:rgba(18,16,15,.62);--acc:#8B0D1A;--acc-lift:#700A15;
 --glass:rgba(255,255,255,.42);--edge:rgba(18,16,15,.10);--edge-top:rgba(255,255,255,.85);
 --shade:rgba(90,70,70,.16);--blob1:rgba(139,13,26,.11);--blob2:rgba(139,13,26,.06);
}}
html,body{{height:100%}}
body{{
 margin:0;background:var(--bg);color:var(--ink);
 font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;line-height:1.55;
 display:flex;align-items:center;justify-content:center;
 padding:max(1.25rem,env(safe-area-inset-top)) 1.25rem max(1.25rem,env(safe-area-inset-bottom));
 overflow-x:hidden;transition:background .35s,color .35s;
}}
.blobs{{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}}
.blobs i{{position:absolute;display:block;border-radius:50%;filter:blur(70px)}}
.b1{{width:70vw;height:70vw;max-width:420px;max-height:420px;background:var(--blob1);
 top:-14%;left:-22%}}
.b2{{width:60vw;height:60vw;max-width:360px;max-height:360px;background:var(--blob2);
 bottom:-16%;right:-20%}}
.card{{
 position:relative;z-index:1;width:100%;max-width:24rem;
 background:var(--glass);border:1px solid var(--edge);border-radius:26px;
 -webkit-backdrop-filter:blur(22px) saturate(150%);backdrop-filter:blur(22px) saturate(150%);
 box-shadow:0 18px 50px var(--shade),inset 0 1px 0 var(--edge-top);
 padding:2rem 1.5rem 1.75rem;text-align:center;transition:background .35s,border-color .35s;
}}
.toggle{{
 position:absolute;top:1rem;right:1rem;width:52px;height:30px;border-radius:999px;cursor:pointer;
 background:var(--glass);border:1px solid var(--edge);padding:0;
 -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);
}}
.toggle::after{{content:'';position:absolute;top:3px;left:3px;width:22px;height:22px;
 border-radius:50%;background:var(--ink);opacity:.85;transition:transform .3s}}
[data-theme="light"] .toggle::after{{transform:translateX(22px)}}
.toggle:focus-visible{{outline:2px solid var(--acc);outline-offset:2px}}
.av{{
 position:relative;width:104px;height:104px;margin:.25rem auto 1.25rem;border-radius:50%;
 overflow:hidden;background:var(--glass);border:1px solid var(--edge);
 box-shadow:0 8px 24px var(--shade),inset 0 1px 0 var(--edge-top);
 display:flex;align-items:center;justify-content:center;
}}
/* absolute, so it COVERS the initials instead of sharing the flex row */
.av img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
.av span{{font-size:2rem;font-weight:600;letter-spacing:.04em;color:var(--dim)}}
.eyebrow{{margin:0;font-size:10px;font-weight:400;letter-spacing:.26em;color:var(--dim)}}
h1{{margin:.6rem 0 0;font-family:Georgia,'Times New Roman',serif;font-size:2.1rem;
font-weight:400;line-height:1.15;letter-spacing:.005em}}
.role{{margin:.7rem 0 0;font-size:.9375rem;font-weight:400;letter-spacing:.02em;color:var(--ink)}}
.org{{margin:.4rem 0 0;font-size:.875rem;color:var(--dim)}}
hr{{border:0;height:1px;background:var(--edge);margin:1.5rem 0}}
.save{{
 display:flex;align-items:center;justify-content:center;width:100%;min-height:54px;
 border:0;border-radius:999px;cursor:pointer;background:var(--acc);color:#F5F2ED;
 font:400 13px/1 system-ui,sans-serif;letter-spacing:.16em;text-transform:uppercase;
 box-shadow:0 8px 22px var(--shade);transition:background .25s,transform .12s;
}}
.save:active{{transform:scale(.98)}}
.save:hover{{background:var(--acc-lift)}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:.75rem;margin-top:.75rem}}
.row a{{
 display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:16px;
 background:var(--glass);border:1px solid var(--edge);color:var(--ink);text-decoration:none;
 font:400 15px/1 system-ui,sans-serif;
 -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transition:border-color .2s}}
.row a:active{{border-color:var(--acc)}}
.tool-btn{{
 display:flex;align-items:center;justify-content:center;gap:.5rem;min-height:52px;border-radius:16px;
 background:var(--glass);border:1px solid var(--edge);color:var(--ink);
 font:400 14px/1 system-ui,sans-serif;cursor:pointer;
 -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transition:border-color .2s,background .2s;
}}
.tool-btn:hover{{border-color:var(--acc);background:var(--glass-2)}}
.tool-btn:active{{transform:scale(.98)}}
.tool-btn svg{{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}
.full{{
 display:inline-flex;align-items:center;justify-content:center;min-height:44px;margin-top:1.5rem;
 color:var(--ink);text-decoration:underline;text-underline-offset:5px;
 font:400 14px/1 system-ui,sans-serif;letter-spacing:.04em}}
.socials{{display:flex;justify-content:center;gap:.75rem;margin-top:1.25rem}}
.socials a{{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;
justify-content:center;background:var(--glass);border:1px solid var(--edge);
-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transition:border-color .2s}}
.socials a:active{{border-color:var(--acc)}}
.socials svg{{width:21px;height:21px;stroke:var(--ink);fill:none;stroke-width:1.7;
stroke-linecap:round;stroke-linejoin:round}}
.note{{margin:1.25rem 0 0;font-size:12px;color:var(--dim);line-height:1.5}}
button:focus-visible,a:focus-visible{{outline:2px solid var(--acc);outline-offset:3px}}

.modal{{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
background:rgba(11,11,11,.84);-webkit-backdrop-filter:blur(20px);backdrop-filter:blur(20px);
opacity:0;pointer-events:none;transition:opacity .25s ease;padding:1.25rem}}
.modal.open{{opacity:1;pointer-events:auto}}
.modal-card{{position:relative;width:100%;max-width:20rem;background:var(--bg);
border:1px solid var(--edge);border-radius:24px;padding:2rem 1.5rem 1.75rem;text-align:center;
box-shadow:0 24px 60px var(--shade),inset 0 1px 0 var(--edge-top);
transform:scale(.95);transition:transform .25s cubic-bezier(.4,0,.2,1)}}
.modal.open .modal-card{{transform:scale(1)}}
.modal-close{{position:absolute;top:.85rem;right:.85rem;width:36px;height:36px;border-radius:50%;
background:var(--glass);border:1px solid var(--edge);color:var(--ink);font-size:20px;line-height:1;
display:flex;align-items:center;justify-content:center;cursor:pointer;transition:border-color .2s}}
.modal-close:hover{{border-color:var(--acc)}}
.qr-wrap{{background:#fff;padding:12px;border-radius:14px;display:inline-block;margin:1rem auto .75rem;
box-shadow:0 8px 24px rgba(0,0,0,.25)}}
.qr-wrap canvas{{display:block;max-width:100%;height:auto}}
.qr-note{{font-size:12px;color:var(--dim);margin:0 0 1.25rem;line-height:1.4}}
.modal-btn{{width:100%;min-height:46px;border-radius:999px;border:1px solid var(--edge);
background:var(--glass-2);color:var(--ink);font:400 12px/1 system-ui,sans-serif;
letter-spacing:.14em;text-transform:uppercase;cursor:pointer;transition:border-color .2s}}
.modal-btn:hover{{border-color:var(--acc)}}

.toast{{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(20px);
background:var(--ink);color:var(--bg);padding:.75rem 1.25rem;border-radius:999px;
font-size:12px;font-weight:500;letter-spacing:.04em;opacity:0;pointer-events:none;
transition:opacity .25s,transform .25s;z-index:300;box-shadow:0 12px 32px var(--shade)}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
@media(prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){{
 .card{{background:rgba(20,20,20,.94)}}
 [data-theme="light"] .card{{background:rgba(255,255,255,.94)}}
}}
</style></head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<g id="i-wa"><path d="M21 11.5a8.4 8.4 0 0 1-12.6 7.3L3 20.5l1.8-5.3A8.4 8.4 0 1 1 21 11.5z"/><path d="M8.6 9.1c.2-.5.4-.5.6-.5h.5c.2 0 .4 0 .6.5l.7 1.7c.1.2 0 .4-.1.5l-.4.5c-.1.1-.2.3-.1.5a5.4 5.4 0 0 0 2.6 2.3c.2.1.4 0 .5-.1l.5-.6c.1-.2.3-.2.5-.1l1.6.8c.2.1.4.2.4.4a1.9 1.9 0 0 1-1.3 1.6c-.6.2-1.4.1-3.2-.8a9 9 0 0 1-3.5-3.7c-.6-1.2-.5-2.1-.2-2.6z"/></g>
<g id="i-ig"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/></g>
<g id="i-tt"><path d="M16 3c.4 2.2 1.9 3.8 4 4.1v3a7 7 0 0 1-4-1.3v5.9a5.7 5.7 0 1 1-5-5.7v3.1a2.7 2.7 0 1 0 2 2.6V3h3z"/></g>
</defs></svg>
<div class="blobs" aria-hidden="true"><i class="b1"></i><i class="b2"></i></div>

<main class="card">
 <button class="toggle" type="button" id="t" aria-label="Switch between dark and light"></button>

 <div class="av">
  <img src="{E(p['avatar'])}" alt="{E(p['name'])}"
       onerror="this.remove()">
  <span aria-hidden="true">{E(p['initials'])}</span>
 </div>

 <p class="eyebrow">{E(p['card_eyebrow'])}</p>
 <h1>{E(p['name'])}</h1>
 <p class="role">{E(p['role'])}</p>
 {company}

 <hr>

 <button class="save" type="button" onclick="downloadVCard()">Save Contact</button>
 <div class="row">
  <a href="mailto:{E(p['email'])}">Email</a>
  <a href="tel:{E(p['tel'])}">Call</a>
 </div>
 <div class="row">
  <button class="tool-btn" type="button" onclick="openQR()">
   <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="3" height="3"/><rect x="18" y="18" width="3" height="3"/><path d="M7 7h.01M17 7h.01M7 17h.01"/></svg>
   <span>QR Code</span>
  </button>
  <button class="tool-btn" type="button" onclick="shareCard()">
   <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
   <span>Share</span>
  </button>
 </div>

 <div class="socials">{"".join(f'<a href="{E(u)}" rel="noopener" aria-label="{E(l)}"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#{i}"/></svg></a>' for i, l, u in socials())}</div>

 <a class="full" href="index.html">View Full Portfolio</a>
 <p class="note">The contact file contains only the public details shown on this page.</p>
</main>

<div id="qrmodal" class="modal" aria-hidden="true" role="dialog" aria-modal="true" aria-label="QR Code">
 <div class="modal-card">
  <button class="modal-close" type="button" onclick="closeQR()" aria-label="Close">&times;</button>
  <p class="eyebrow" style="margin-bottom:.75rem">SCAN WITH PHONE CAMERA</p>
  <div class="qr-wrap"><canvas id="qrcanvas"></canvas></div>
  <p class="qr-note">Opens this digital business card on any phone</p>
  <button class="modal-btn" type="button" onclick="closeQR()">Done</button>
 </div>
</div>
<div id="toast" class="toast" aria-live="polite"></div>

<script src="assets/qr.min.js"></script>
<script>
{vj}
(function(){{
 var r=document.documentElement,t=document.getElementById('t'),K='jl-theme';
 try{{var v=localStorage.getItem(K);if(v)r.setAttribute('data-theme',v);}}catch(e){{}}
 t.addEventListener('click',function(){{
  var n=r.getAttribute('data-theme')==='light'?'dark':'light';
  r.setAttribute('data-theme',n);
  var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute('content',n==='light'?'#EFEBE4':'#0B0B0B');
  try{{localStorage.setItem(K,n);}}catch(e){{}}
 }});
}})();

function showToast(msg){{
 var t=document.getElementById('toast');if(!t)return;
 t.textContent=msg;t.classList.add('show');
 setTimeout(function(){{t.classList.remove('show');}},2400);
}}
var qrInst=null;
function openQR(){{
 var m=document.getElementById('qrmodal');if(!m)return;
 m.classList.add('open');m.setAttribute('aria-hidden','false');
 document.body.style.overflow='hidden';
 if(!qrInst && typeof QRious!=='undefined'){{
  qrInst=new QRious({{element:document.getElementById('qrcanvas'),value:window.location.href,size:200,level:'M'}});
 }}
}}
function closeQR(){{
 var m=document.getElementById('qrmodal');if(!m)return;
 m.classList.remove('open');m.setAttribute('aria-hidden','true');
 document.body.style.overflow='';
}}
document.getElementById('qrmodal').addEventListener('click',function(e){{
 if(e.target===this||e.target.closest('.modal-close'))closeQR();
}});
document.addEventListener('keydown',function(e){{
 if(e.key==='Escape'&&document.getElementById('qrmodal').classList.contains('open'))closeQR();
}});
function shareCard(){{
 if(navigator.share){{
  navigator.share({{title:document.title,text:"Jamielyn Ludovice — Multimedia Marketing Specialist",url:window.location.href}}).catch(function(){{}});
 }}else if(navigator.clipboard){{
  navigator.clipboard.writeText(window.location.href).then(function(){{
   showToast("Card link copied to clipboard!");
  }});
 }}else{{
  showToast(window.location.href);
 }}
}}
</script>
</body></html>
""")


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="16" fill="#8B0D1A"/>
<text x="32" y="43" font-family="'Cormorant Garamond', Georgia, serif" font-size="34" font-weight="500" fill="#F5F2ED" text-anchor="middle" letter-spacing="-1">JL</text>
</svg>
"""


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    write("assets/style.css", CSS.strip() + "\n")
    # Real favicon.png / apple-touch-icon.png now come from Portfolio/images/
    # (copied in below along with every other image) - the old text-based
    # FAVICON_SVG is unused but left defined below in case it's needed again.
    qr_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qrious.min.js")
    if os.path.isfile(qr_src):
        shutil.copy2(qr_src, os.path.join(OUT, "assets", "qr.min.js"))
    # site/ is deleted and rebuilt every run, so images must live OUTSIDE it.
    # Portfolio/images/ is the source folder - it is copied in on every build.
    dest = os.path.join(OUT, "assets", "images")
    os.makedirs(dest, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    os.makedirs(src, exist_ok=True)
    copied = 0
    for f in sorted(os.listdir(src)):
        fp = os.path.join(src, f)
        if os.path.isfile(fp) and not f.startswith("."):
            shutil.copy2(fp, os.path.join(dest, f))
            copied += 1
    # Portfolio/videos/ -> site/assets/video/  (mp4 + poster jpg, same rule as images)
    vsrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
    if os.path.isdir(vsrc):
        vdest = os.path.join(OUT, "assets", "video")
        os.makedirs(vdest, exist_ok=True)
        for f in sorted(os.listdir(vsrc)):
            fp = os.path.join(vsrc, f)
            if os.path.isfile(fp) and not f.startswith("."):
                shutil.copy2(fp, os.path.join(vdest, f))
    with open(os.path.join(src, "README.txt"), "w", encoding="utf-8") as f:
        f.write("PUT YOUR IMAGES HERE - screenshots, renders, portraits.\n"
                "Then name the file in content.py.\n\n"
                "Do NOT put them in site/assets/images/ - build.py deletes and\n"
                "rebuilds the whole site/ folder every run, so anything left there\n"
                "is lost. This folder is copied in fresh on every build.\n")
    write("vercel.json", '{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
    build_home(); build_work_index(); build_tools(); build_about(); build_card(); build_404()
    for i, pr in enumerate(PROJECTS):
        build_project(i, pr)
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"Built {n} files into  {OUT}")
    print(f"  {len(PROJECTS)} project pages · {len(DISCIPLINES)} disciplines")
    print("  card.html is the standalone NFC page")


if __name__ == "__main__":
    main()
