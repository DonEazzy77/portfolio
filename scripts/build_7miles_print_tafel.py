#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drucksachen-Tafel fuer die 7miles-Case-Seite (/arbeiten/7miles).

Aufruf ohne Argumente aus dem Repo:  python3 scripts/build_7miles_print_tafel.py
Die Showcase-Quellen entstehen vorher im 7miles-Projekt mit:
  VK_SHOWCASE=1      python3 scripts/build_businesscard.py
  STEMPEL_SHOWCASE=1 python3 scripts/build_stamp.py
  FLYER_SHOWCASE=1   python3 scripts/build_flyer.py

Setzt die Kachel `7miles-w3-print.png` aus den Original-Proofs zusammen:
Visitenkarte (Showcase-Rendering, Kontaktdaten als Mockup-Balken),
beide Stempel-Proofs und die Gutscheinkarte.

Warum es dieses Skript gibt: die Vorgaenger-Kachel vom 21.08.2026 wurde ohne
Quellskript zusammengesetzt; eine Ausrichtungskorrektur war deshalb nur durch
Neubau moeglich. Quellskripte immer ablegen.

Eingaben erwartet unter SRC (Projekt "Fahrschule 7Miles"):
  assets/print/visitenkarten/showcase/vk_vorderseite_crest.png
  assets/print/visitenkarten/showcase/vk_daniel_rueckseite.png
  assets/print/stempel/showcase/stempel_rechteck_vorschau.png
  assets/print/stempel/showcase/stempel_rund_vorschau.png
  assets/print/flyer/showcase/gutschein_front.png
"""
import os, sys
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "Fahrschule 7Miles")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "assets", "showcase", "7miles-w3-print.png")

W, H = 2568, 1806
ASPHALT = (38, 40, 46)
CONCRETE = (245, 245, 242)
WHITE = (255, 255, 255)
PAD = 44                    # Aussenrand der Tafel
GAP = 26                    # Abstand zwischen den Feldern
RADIUS = 10

def load(rel):
    p = os.path.join(SRC, rel)
    if not os.path.exists(p):
        raise SystemExit(f"fehlt: {p}")
    return Image.open(p).convert("RGB")

def fit(im, bw, bh):
    """Groesstmoeglich einpassen, Seitenverhaeltnis erhalten."""
    s = min(bw / im.width, bh / im.height)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)

def panel(size, fill):
    return Image.new("RGB", size, fill)

def zentriert(canvas, im, box):
    """Mittet im in box=(x,y,w,h) — beide Achsen."""
    x, y, bw, bh = box
    canvas.paste(im, (int(x + (bw - im.width) / 2), int(y + (bh - im.height) / 2)))

def main():
    cv = Image.new("RGB", (W, H), WHITE)

    innen_w = W - 2 * PAD
    oben_h = int((H - 2 * PAD - GAP) * 0.455)
    unten_h = H - 2 * PAD - GAP - oben_h

    # --- oben: Visitenkarte vorne + hinten auf dunklem Feld -----------------
    top = panel((innen_w, oben_h), ASPHALT)
    vk_f = load("assets/print/visitenkarten/showcase/vk_vorderseite_crest.png")
    vk_b = load("assets/print/visitenkarten/showcase/vk_daniel_rueckseite.png")
    zell_w = (innen_w - GAP) // 2
    inner_pad = 34
    for i, im in enumerate((vk_f, vk_b)):
        k = fit(im, zell_w - 2 * inner_pad, oben_h - 2 * inner_pad)
        zentriert(top, k, (i * (zell_w + GAP), 0, zell_w, oben_h))
    cv.paste(top, (PAD, PAD))

    # --- unten: zwei Stempel auf hellem Feld + Gutschein auf dunklem --------
    gut_w = int(innen_w * 0.235)
    stempel_w = innen_w - GAP - gut_w
    bottom_y = PAD + oben_h + GAP

    st = panel((stempel_w, unten_h), CONCRETE)
    rect = load("assets/print/stempel/showcase/stempel_rechteck_vorschau.png")
    rund = load("assets/print/stempel/showcase/stempel_rund_vorschau.png")
    # zwei gleich breite Zellen, beide Motive in ihrer Zelle gemittet.
    # Das war der Fehler der Vorgaengerkachel: Rechteck klebte am linken Rand,
    # Rund stand mittig — zwei verschiedene Bezugsachsen in einem Feld.
    sp = 26
    zw = (stempel_w - 2 * sp) // 2
    zh = unten_h - 2 * sp
    zentriert(st, fit(rect, zw - 14, zh), (sp, sp, zw, zh))
    zentriert(st, fit(rund, zw - 14, zh), (sp + zw, sp, zw, zh))
    cv.paste(st, (PAD, bottom_y))

    gp = panel((gut_w, unten_h), ASPHALT)
    gut = load("assets/print/flyer/showcase/gutschein_front.png")
    zentriert(gp, fit(gut, gut_w - 2 * 30, unten_h - 2 * 30), (0, 0, gut_w, unten_h))
    cv.paste(gp, (PAD + stempel_w + GAP, bottom_y))

    cv.save(OUT, dpi=(144, 144))
    print("OK ->", OUT, cv.size)

if __name__ == "__main__":
    main()
