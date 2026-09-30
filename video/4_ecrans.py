"""Captures d'écran de l'outil (format téléphone) pour la page de présentation -> static/images/ecran-*.jpg"""
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ICI = Path(__file__).parent
DEST = ICI.parent / "static" / "images"
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:1320/quittance-tranquille/"


def sauver(png, nom):
    Image.open(BytesIO(png)).convert("RGB").resize((585, 1266), Image.LANCZOS).save(DEST / nom, quality=84, optimize=True, progressive=True)


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, color_scheme="light", locale="fr-FR")
    pg = ctx.new_page()
    pg.add_init_script("document.documentElement.style.scrollBehavior='auto'")
    pg.goto(URL)
    pg.fill("#b_n", "Jean Martin")
    pg.fill("#l_n", "Camille Dupont")
    pg.fill("#b_a", "12 rue des Lilas\n69003 Lyon")
    pg.fill("#a", "3 avenue de la Gare, appt 12\n69007 Lyon")
    pg.fill("#y", "700")
    pg.fill("#c", "50")
    pg.evaluate("scrollTo(0, document.querySelector('#t1').getBoundingClientRect().top + scrollY - 90)")
    sauver(pg.screenshot(), "ecran-bail.jpg")
    pg.evaluate("scrollTo(0, document.querySelector('#t2').getBoundingClientRect().top + scrollY - 90)")
    sauver(pg.screenshot(), "ecran-rappels.jpg")
    pg.click("#ouvrir")
    pg.wait_for_selector("#apercu .doc-titre")
    pg.evaluate("scrollTo(0, 0)")
    sauver(pg.screenshot(), "ecran-quittance.jpg")
    pg.evaluate("scrollTo(0, document.querySelector('.apercu-colonne').getBoundingClientRect().top + scrollY - 70)")
    sauver(pg.screenshot(), "ecran-apercu.jpg")
    pg.evaluate("scrollTo(0, 0)")
    pg.click("text=En partie : reçu")
    pg.fill("#g_v", "400")
    pg.evaluate("scrollTo(0, document.querySelector('#g1').getBoundingClientRect().top + scrollY - 80)")
    sauver(pg.screenshot(), "ecran-recu.jpg")
    b.close()
print("ok")
