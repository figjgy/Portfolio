# -*- coding: utf-8 -*-
"""Portfolio consistency check. Run before every push.

Catches the things that go wrong silently:
  * a caption list that no longer lines up with its gallery (captions then
    attach to the WRONG picture - this happened on the K-Pick page 2026-09-07
    when two gallery sets were merged into one and the caption was not)
  * an image or video named in content.py that is not in images/ or videos/
  * an image the built site asks for that is not in site/assets/
  * leftover "Image - ..." placeholders and "[ Add ... ]" TODO text
  * a project with no cover, or no year while every other project has one
  * internal links in site/ that point at a file that does not exist
"""
import importlib.util, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
IMG_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.svg')

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

problems, notes = [], []
c = load("content", "content.py")
images = set(os.listdir("images")) if os.path.isdir("images") else set()
videos = set(os.listdir("videos")) if os.path.isdir("videos") else set()


def media_of(pr):
    out = []
    if pr.get("cover"):
        out.append(pr["cover"])
    for g in pr.get("gallery") or []:
        if isinstance(g, dict):
            out += list(g.get("grid") or []) + list(g.get("video") or [])
        elif isinstance(g, (list, tuple)):
            out += list(g)
        elif isinstance(g, str) and g.lower().endswith(IMG_EXT + ('.mp4',)):
            out.append(g)
    return out


print("=" * 66)
print("  PORTFOLIO CHECK")
print("=" * 66)

print("\n1. CAPTIONS LINED UP WITH GALLERIES")
for pr in c.PROJECTS:
    g, caps = pr.get("gallery") or [], pr.get("gallery_captions") or []
    if caps and len(caps) != len(g):
        problems.append("%s: %d captions for %d gallery items - captions will "
                        "attach to the wrong picture" % (pr["slug"], len(caps), len(g)))
        print("   MISMATCH  %-26s %d caps / %d items" % (pr["slug"], len(caps), len(g)))
if not any(p.startswith(tuple(x["slug"] for x in c.PROJECTS)) and "captions" in p for p in problems):
    print("   ok - every project with captions has one per gallery item")

print("\n2. FILES NAMED IN content.py THAT EXIST ON DISK")
missing = 0
for pr in c.PROJECTS:
    for f in media_of(pr):
        pool = videos if f.lower().endswith(".mp4") else images
        if f not in pool:
            problems.append("%s: %s is referenced but not in %s/"
                            % (pr["slug"], f, "videos" if f.endswith(".mp4") else "images"))
            print("   MISSING   %-26s %s" % (pr["slug"], f)); missing += 1
if not missing:
    print("   ok - every referenced file is present")

print("\n3. FILES THE BUILT SITE ASKS FOR")
if os.path.isdir("site"):
    absent = set()
    for f in glob.glob("site/**/*.html", recursive=True):
        s = open(f, encoding="utf-8").read()
        for m in re.findall(r'assets/(images|video)/([\w.\-]+)', s):
            if not os.path.exists(os.path.join("site", "assets", m[0], m[1])):
                absent.add("/".join(m))
    for a in sorted(absent):
        problems.append("built site requests missing asset " + a)
        print("   MISSING   " + a)
    if not absent:
        print("   ok - every asset the pages request is in site/assets/")
else:
    notes.append("site/ not built yet - run: python build.py")

print("\n4. INTERNAL LINKS")
if os.path.isdir("site"):
    broken = set()
    for f in glob.glob("site/**/*.html", recursive=True):
        d = os.path.dirname(f)
        for href in re.findall(r'href="([^"#?:]+)"', open(f, encoding="utf-8").read()):
            if href.startswith(("http", "//", "mailto", "tel")):
                continue
            if "+" in href or "$" in href or "{" in href:
                continue            # href built by inline JS, not a real path
            # a leading slash is relative to the site root, not to this file
            t = (os.path.normpath(os.path.join("site", href.lstrip("/")))
                 if href.startswith("/") else os.path.normpath(os.path.join(d, href)))
            if os.path.exists(t) or os.path.exists(t + ".html") or os.path.isdir(t):
                continue
            broken.add("%s -> %s" % (os.path.relpath(f, "site"), href))
    for b in sorted(broken):
        problems.append("broken link " + b)
        print("   BROKEN    " + b)
    if not broken:
        print("   ok - no internal link points at a missing file")

print("\n5. PLACEHOLDERS STILL WAITING FOR REAL WORK")
ph = 0
for pr in c.PROJECTS:
    for g in pr.get("gallery") or []:
        if isinstance(g, str) and not g.lower().endswith(IMG_EXT + ('.mp4',)):
            print("   %-26s gallery: %s" % (pr["slug"], g)); ph += 1
    if not pr.get("cover"):
        print("   %-26s NO COVER  (%s)" % (pr["slug"], (pr.get("cover_note") or "")[:40])); ph += 1
    for k, v in pr.items():
        if isinstance(v, str) and "[ Add" in v:
            print("   %-26s %s: %s" % (pr["slug"], k, v[:45])); ph += 1
notes.append("%d placeholders still to fill - these are waiting on Jamie's files, not faults" % ph)
if not ph:
    print("   none - every project has real artwork")

print("\n6. YEARS")
noyear = [p["slug"] for p in c.PROJECTS if not p.get("year")]
for s in noyear:
    print("   %-26s has no year while the rest do" % s)
    notes.append("%s has no year set" % s)
if not noyear:
    print("   ok - every project has a year")

print("\n" + "=" * 66)
if problems:
    print("  %d PROBLEM(S) - fix before pushing" % len(problems))
    for p in problems:
        print("   - " + p)
else:
    print("  NO PROBLEMS. Safe to build and push.")
for n in notes:
    print("  note: " + n)
print("=" * 66)
sys.exit(1 if problems else 0)
