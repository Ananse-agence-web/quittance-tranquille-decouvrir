"""Montage final : cartes + séquences filmées dans un cadre de téléphone + voix off -> sortie/demo.mp4 (1920x1080)."""
import json
import subprocess
import textwrap
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from scenes import MARGE, SCENES

ICI = Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1920, 1080, 30
TMP = ICI / "sortie" / "tmp"
TMP.mkdir(parents=True, exist_ok=True)
DUREES = json.loads((ICI / "voix" / "durees.json").read_text(encoding="utf-8"))
SEGMENTS = json.loads((ICI / "capture" / "segments.json").read_text(encoding="utf-8"))
LOGO = ICI.parent / "static" / "images" / "icon-512.png"

F = "C:/Windows/Fonts/"
def police(nom, taille):
    return ImageFont.truetype(F + nom, taille)
GRAS, SEMI, NORMAL = "segoeuib.ttf", "seguisb.ttf", "segoeui.ttf"
SERIF = "georgiab.ttf"

TEAL, TEAL_VIF, SOLEIL, ROUGE = (13, 110, 98), (60, 194, 173), (242, 179, 61), (200, 65, 46)
CLAIR = (200, 236, 229)

ECH = 1.07
EW, EH = int(390 * ECH), int(844 * ECH)
BORD = 14
EX, EY = 400, (H - EH) // 2


def fond():
    """Dégradé vert profond + halos."""
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(8 + 4 * t), int(38 + 36 * t), int(38 + 30 * t)))
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse([1100, -300, 2300, 700], fill=90)
    im = Image.composite(Image.new("RGB", (W, H), (24, 156, 138)), im, halo.filter(ImageFilter.GaussianBlur(170)))
    halo2 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo2).ellipse([-400, 650, 700, 1500], fill=55)
    return Image.composite(Image.new("RGB", (W, H), SOLEIL), im, halo2.filter(ImageFilter.GaussianBlur(170)))


def marque(im, x=70, y=56, taille=44):
    logo = Image.open(LOGO).convert("RGBA").resize((taille, taille))
    im.paste(logo, (x, y), logo)
    d = ImageDraw.Draw(im)
    f = police(GRAS, int(taille * 0.62))
    d.text((x + taille + 14, y + taille / 2), "Quittance ", font=f, fill="white", anchor="lm")
    w = d.textlength("Quittance ", font=f)
    d.text((x + taille + 14 + w, y + taille / 2), "Tranquille", font=f, fill=SOLEIL, anchor="lm")


def texte_multi(d, xy, txt, f, fill, interligne=1.2, anchor="la"):
    x, y = xy
    for ligne in txt.split("\n"):
        d.text((x, y), ligne, font=f, fill=fill, anchor=anchor)
        y += int(f.size * interligne)
    return y


def fond_app(sc):
    im = fond()
    ombre = Image.new("L", (W, H), 0)
    ImageDraw.Draw(ombre).rounded_rectangle([EX - BORD + 20, EY - BORD + 40, EX + EW + BORD + 20, EY + EH + BORD + 40], 60, fill=150)
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, ombre.filter(ImageFilter.GaussianBlur(40)))
    marque(im)
    d = ImageDraw.Draw(im)
    x = 1010
    y = texte_multi(d, (x, 300), sc["titre"], police(SERIF, 80), "white", 1.15)
    d.rounded_rectangle([x, y + 24, x + 110, y + 32], 4, fill=SOLEIL)
    y = texte_multi(d, (x, y + 70), sc["sous"], police(SEMI, 42), CLAIR, 1.3)
    voix = "\n".join(textwrap.wrap("« " + sc["voix"] + " »", 52))
    texte_multi(d, (x, max(y + 60, 800)), voix, police(NORMAL, 27), (170, 205, 198), 1.35)
    return im


def cadre_telephone():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([EX - BORD, EY - BORD, EX + EW + BORD, EY + EH + BORD], 58, fill=(17, 24, 32, 255), outline=(62, 80, 88, 255), width=2)
    d.rounded_rectangle([EX, EY, EX + EW, EY + EH], 44, fill=(0, 0, 0, 0))
    return im


def icone_tel(d, cx, cy, h, coul):
    w = h * 0.55
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], h * 0.12, outline=coul, width=max(4, int(h / 18)))
    d.line([cx - w * 0.15, cy + h * 0.36, cx + w * 0.15, cy + h * 0.36], fill=coul, width=max(4, int(h / 18)))


def titre_marque(d, cx, y, taille):
    f = police(GRAS, taille)
    w1, w2 = d.textlength("Quittance ", font=f), d.textlength("Tranquille", font=f)
    x = cx - (w1 + w2) / 2
    d.text((x, y), "Quittance ", font=f, fill="white")
    d.text((x + w1, y), "Tranquille", font=f, fill=SOLEIL)


def carte(sc):
    im = fond()
    d = ImageDraw.Draw(im)
    cx = W // 2
    if sc["id"] in ("01_intro", "09_outro"):
        logo = Image.open(LOGO).convert("RGBA").resize((190, 190))
        im.paste(logo, (cx - 95, 180), logo)
        titre_marque(d, cx, 450, 100)
        texte_multi(d, (cx, 630), sc["sous"], police(SEMI, 50), CLAIR, 1.35, anchor="ma")
        if sc["id"] == "09_outro":
            d.rounded_rectangle([cx - 330, 850, cx + 330, 940], 45, fill=SOLEIL)
            d.text((cx, 895), "Créez vos quittances maintenant", font=police(GRAS, 38), fill=(40, 30, 5), anchor="mm")
        return im
    marque(im)
    texte_multi(d, (cx, 150), sc["titre"], police(SERIF, 76), "white", 1.15, anchor="ma")
    if sc["id"] == "02_donnees":
        y = 560
        d.rounded_rectangle([cx - 520, y - 150, cx - 200, y + 150], 30, fill=(12, 52, 48), outline=TEAL_VIF, width=5)
        icone_tel(d, cx - 360, y - 30, 130, TEAL_VIF)
        d.text((cx - 360, y + 85), "Votre appareil", font=police(GRAS, 34), fill="white", anchor="mm")
        d.rounded_rectangle([cx + 200, y - 150, cx + 520, y + 150], 30, fill=(16, 40, 42), outline=(90, 115, 118), width=4)
        for i in range(3):
            d.rounded_rectangle([cx + 290, y - 95 + i * 45, cx + 430, y - 60 + i * 45], 6, outline=(120, 145, 148), width=4)
        d.text((cx + 360, y + 85), "Serveur / cloud", font=police(GRAS, 34), fill=(150, 175, 178), anchor="mm")
        for x in range(cx - 190, cx + 190, 26):
            d.line([x, y, x + 14, y], fill=(90, 115, 118), width=5)
        d.ellipse([cx - 55, y - 55, cx + 55, y + 55], fill=ROUGE)
        d.line([cx - 24, y - 24, cx + 24, y + 24], fill="white", width=10)
        d.line([cx - 24, y + 24, cx + 24, y - 24], fill="white", width=10)
        texte_multi(d, (cx, 780), sc["sous"], police(SEMI, 44), CLAIR, 1.35, anchor="ma")
    elif sc["id"] == "05_rappel":
        # Notification d'agenda stylisée
        x0, y0, w, h = cx - 470, 380, 940, 250
        ombre = Image.new("L", (W, H), 0)
        ImageDraw.Draw(ombre).rounded_rectangle([x0 + 10, y0 + 30, x0 + w + 10, y0 + h + 30], 40, fill=140)
        im.paste(Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, ombre.filter(ImageFilter.GaussianBlur(30))))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 40, fill=(248, 247, 243))
        d.rounded_rectangle([x0 + 40, y0 + 40, x0 + 130, y0 + 130], 22, fill=(255, 255, 255), outline=(225, 222, 214), width=3)
        d.rectangle([x0 + 43, y0 + 43, x0 + 127, y0 + 70], fill=ROUGE)
        d.text((x0 + 85, y0 + 57), "OCT", font=police(GRAS, 20), fill="white", anchor="mm")
        d.text((x0 + 85, y0 + 102), "5", font=police(GRAS, 40), fill=(20, 32, 46), anchor="mm")
        d.text((x0 + 160, y0 + 58), "Agenda · 09:00", font=police(SEMI, 28), fill=(96, 110, 124), anchor="lm")
        d.text((x0 + 160, y0 + 106), "Loyer de Camille Dupont — quittance à générer", font=police(GRAS, 34), fill=(20, 32, 46), anchor="lm")
        d.text((x0 + 160, y0 + 160), "Une fois le paiement bien reçu, ouvrez ce lien :", font=police(NORMAL, 28), fill=(60, 72, 84), anchor="lm")
        d.text((x0 + 160, y0 + 203), "…/quittance-tranquille/generer/#…", font=police(SEMI, 28), fill=TEAL, anchor="lm")
        texte_multi(d, (cx, 760), sc["sous"], police(SEMI, 46), CLAIR, 1.4, anchor="ma")
    return im


def encoder(args, sortie):
    subprocess.run([FF, "-loglevel", "error", "-y", *args, "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", str(sortie)], check=True)


def main():
    cadre = TMP / "cadre.png"
    cadre_telephone().save(cadre)
    capture = ICI / "capture" / "capture.webm"
    parties = []
    for sc in SCENES:
        sid = sc["id"]
        wav = ICI / "voix" / DUREES[sid]["fichier"]
        out = TMP / f"{sid}.mp4"
        if sc["type"] == "carte":
            d = DUREES[sid]["duree"] + MARGE + 0.5
            img = TMP / f"{sid}.png"
            carte(sc).save(img)
            n = int(d * FPS)
            vf = (f"scale=2304:1296,zoompan=z='min(zoom+0.0006,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
                  f"fade=t=in:st=0:d=0.4,fade=t=out:st={d - 0.4:.2f}:d=0.4")
            encoder(["-loop", "1", "-i", str(img), "-i", str(wav), "-filter_complex",
                     f"[0:v]{vf}[v];[1:a]adelay=250|250,apad[a]", "-map", "[v]", "-map", "[a]", "-t", f"{d:.2f}"], out)
        else:
            seg = SEGMENTS[sid]
            d = seg["fin"] - seg["debut"]
            img = TMP / f"{sid}.png"
            fond_app(sc).save(img)
            fc = (f"[1:v]trim=start={seg['debut']:.3f}:end={seg['fin']:.3f},setpts=PTS-STARTPTS,fps={FPS},scale={EW}:{EH}:flags=lanczos[app];"
                  f"[0:v][app]overlay={EX}:{EY}[a1];[a1][2:v]overlay=0:0,fade=t=in:st=0:d=0.3,fade=t=out:st={d - 0.3:.2f}:d=0.3[v];"
                  f"[3:a]adelay=150|150,apad[a]")
            encoder(["-loop", "1", "-i", str(img), "-i", str(capture), "-loop", "1", "-i", str(cadre), "-i", str(wav),
                     "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{d:.2f}"], out)
        parties.append(out)
        print("ok", sid, f"{d:.1f}s")

    liste = TMP / "liste.txt"
    liste.write_text("".join(f"file '{p.as_posix()}'\n" for p in parties), encoding="utf-8")
    final = ICI / "sortie" / "demo.mp4"
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy",
                    "-movflags", "+faststart", str(final)], check=True)
    # Affiche (image de la carte d'intro)
    carte(SCENES[0]).convert("RGB").resize((1280, 720)).save(ICI / "sortie" / "affiche.jpg", quality=86)
    print("Vidéo :", final, f"({final.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
