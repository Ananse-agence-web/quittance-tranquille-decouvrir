"""Filme l'outil (serveur Hugo local) au format téléphone, calé sur la durée de la voix.

Prérequis : l'outil tourne sur http://localhost:1320/quittance-tranquille/
  (hugo server --source ../../app --port 1320).
Produit : capture/capture.webm + capture/segments.json. Toutes les données sont fictives.
"""
import json
import shutil
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from scenes import MARGE

ICI = Path(__file__).parent
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:1320/quittance-tranquille/"
SORTIE = ICI / "capture"
DUREES = json.loads((ICI / "voix" / "durees.json").read_text(encoding="utf-8"))
duree = lambda sid: DUREES[sid]["duree"] + MARGE

TAP_JS = """
addEventListener('pointerdown', (e) => {
  const d = document.createElement('div');
  d.style.cssText = `position:fixed;left:${e.clientX-22}px;top:${e.clientY-22}px;width:44px;height:44px;border-radius:50%;
    background:rgba(242,179,61,.35);border:3px solid rgba(242,179,61,.95);pointer-events:none;z-index:99999;
    transition:transform .45s ease-out, opacity .45s ease-out;`;
  document.documentElement.appendChild(d);
  requestAnimationFrame(() => { d.style.transform = 'scale(1.6)'; d.style.opacity = '0'; });
  setTimeout(() => d.remove(), 500);
}, true);
// Pas de défilement « smooth » : on maîtrise les mouvements
document.documentElement.style.scrollBehavior = 'auto';
"""


def main():
    if SORTIE.exists():
        shutil.rmtree(SORTIE)
    SORTIE.mkdir()
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, color_scheme="light", locale="fr-FR",
                            record_video_dir=str(SORTIE), record_video_size={"width": 390, "height": 844}, accept_downloads=True,
                            has_touch=False)
        ctx.add_init_script(TAP_JS)
        page = ctx.new_page()
        t0 = time.monotonic()
        segments = {}
        horloge = lambda: time.monotonic() - t0
        attendre = lambda s: page.wait_for_timeout(int(s * 1000))

        def scene(sid, actions):
            debut = horloge()
            actions()
            reste = duree(sid) - (horloge() - debut)
            if reste > 0:
                attendre(reste)
            segments[sid] = {"debut": debut, "fin": horloge()}
            print(f"{sid}: {debut:.1f} → {segments[sid]['fin']:.1f}")

        def defiler_vers(sel, marge=90, pas=14):
            """Défilement doux jusqu'à l'élément."""
            cible = page.evaluate(f"(s) => document.querySelector(s).getBoundingClientRect().top + scrollY - {marge}", sel)
            depart = page.evaluate("scrollY")
            for i in range(1, pas + 1):
                page.evaluate(f"window.scrollTo(0, {depart + (cible - depart) * i / pas})")
                attendre(0.03)

        def taper(sel, texte, delai=45):
            page.click(sel)
            page.type(sel, texte, delay=delai)

        page.goto(URL)
        page.wait_for_selector("#apercu .doc-titre")
        attendre(0.5)

        def s03():
            defiler_vers("#outil", 70)
            attendre(0.4)
            taper("#b_n", "Jean Martin")
            taper("#l_n", "Camille Dupont")
            defiler_vers("#b_a", 120)
            taper("#b_a", "12 rue des Lilas, 69003 Lyon", 25)
            taper("#a", "3 av. de la Gare, 69007 Lyon", 25)
            defiler_vers("#y", 200)
            taper("#y", "700", 90)
            taper("#c", "50", 90)
            attendre(0.5)
        scene("03_bail", s03)

        def s04():
            defiler_vers("#t2", 80)
            attendre(0.6)
            page.click("input[name=rappel][value='3']")
            attendre(0.8)
            defiler_vers("#t3", 80)
            attendre(0.8)
            with page.expect_download():
                page.click("#config button[type=submit]")
            attendre(1.0)
        scene("04_agenda", s04)

        # La scène 05 est une carte : on ouvre le lien du rappel pendant ce temps (hors champ)
        page.click("#ouvrir")
        page.wait_for_selector("#apercu .doc-titre")
        page.evaluate("window.scrollTo(0, 0)")
        attendre(0.5)

        def s06():
            attendre(1.2)
            defiler_vers("#g_y", 160, 20)
            attendre(1.0)
            defiler_vers(".apercu-colonne", 70, 30)
            attendre(1.0)
        scene("06_quittance", s06)

        def s07():
            defiler_vers("#g1", 80, 16)
            attendre(0.5)
            page.click("text=En partie : reçu")
            attendre(0.6)
            defiler_vers("#bloc-verse", 220)
            taper("#g_v", "400", 120)
            attendre(0.8)
            defiler_vers(".apercu-colonne", 70, 26)
        scene("07_recu", s07)

        def s08():
            defiler_vers("#g1", 80, 12)
            page.click("text=En totalité : quittance")
            attendre(0.5)
            defiler_vers("#g2", 90, 16)
            attendre(0.5)
            with page.expect_download():
                page.click("#pdf")
            attendre(1.4)
            defiler_vers("#g3", 90, 18)
            attendre(0.6)
        scene("08_envoi", s08)

        video = page.video
        ctx.close()
        b.close()
        Path(video.path()).rename(SORTIE / "capture.webm")
        (SORTIE / "segments.json").write_text(json.dumps(segments, indent=2), encoding="utf-8")
        print("OK :", SORTIE / "capture.webm")


if __name__ == "__main__":
    main()
