"""Generate the small set of assets used by the Senda Pa landing page.

Run from the landing root:
    python tools/prepare_site_assets.py

The landing is intentionally static and self-contained. This script reads
screenshots from the Godot project and writes optimized files into assets/.
By default the game is expected at ../flutter/cubil. Override it with the
SENDA_PA_GAME environment variable if the projects are in another location.
"""

from __future__ import annotations

import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

SITE = Path(__file__).resolve().parents[1]
GAME = Path(os.environ.get("SENDA_PA_GAME", SITE.parent / "flutter" / "cubil")).resolve()
if not (GAME / "docs").is_dir():
    raise SystemExit(
        f"No encuentro el proyecto del juego en {GAME}. "
        "Define SENDA_PA_GAME con la ruta correcta."
    )
ASSETS = SITE / "assets"
SCREENS = ASSETS / "screens"
FEATURES = ASSETS / "features"
FONTS = ASSETS / "fonts"
SCREENS.mkdir(parents=True, exist_ok=True)
FEATURES.mkdir(parents=True, exist_ok=True)
FONTS.mkdir(parents=True, exist_ok=True)

PAPER = "#f6efdf"
INK = "#332b24"
SOFT = "#6f6153"
TERRACOTTA = "#c96b4e"
TERRA_DARK = "#a84e36"
SAGE = "#a9c47f"
FOREST = "#2e4436"
CREAM = "#fff9ed"


def font(name: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONTS / name), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight, 100])
        except Exception:
            pass
    return f


def webp(src: Path, dest: Path, width: int, quality: int = 90) -> None:
    im = Image.open(src).convert("RGB")
    if im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
    im.save(dest, "WEBP", quality=quality, method=6)


def crop_webp(
    src: Path,
    dest: Path,
    box: tuple[int, int, int, int],
    size: tuple[int, int],
    quality: int = 90,
) -> None:
    im = Image.open(src).convert("RGB").crop(box)
    im = ImageOps.fit(im, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    im.save(dest, "WEBP", quality=quality, method=6)


def rounded(im: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), radius=radius, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def phone(img: Image.Image, width: int) -> Image.Image:
    screen_w = width
    screen_h = round(width * 19.5 / 9)
    screen = ImageOps.fit(img.convert("RGB"), (screen_w, screen_h), Image.Resampling.LANCZOS)
    screen = rounded(screen, round(width * 0.075))
    frame = Image.new("RGBA", (width + 18, screen_h + 18), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((0, 0, frame.width, frame.height), radius=round(width * 0.105), fill="#2d2925")
    frame.alpha_composite(screen, (9, 9))
    return frame


def og_image() -> None:
    W, H = 1200, 630
    base = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(base)

    # Warm sun and a sage hill, both very quiet.
    sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    sd.ellipse((880, -150, 1360, 330), fill=(240, 217, 168, 255))
    sun = sun.filter(ImageFilter.GaussianBlur(2))
    base = Image.alpha_composite(base.convert("RGBA"), sun)

    hill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hill)
    hd.ellipse((-260, 430, 540, 860), fill=(169, 196, 127, 120))
    hill = hill.filter(ImageFilter.GaussianBlur(1))
    base = Image.alpha_composite(base, hill)
    d = ImageDraw.Draw(base)

    # Type.
    d.text((78, 74), "UN PUZZLE ISOMÉTRICO PARA IR SIN PRISA", font=font("Nunito-700.ttf", 20), fill=TERRA_DARK)
    d.text((72, 110), "Senda", font=font("Fredoka.ttf", 126, 600), fill=INK)
    x = 72 + d.textlength("Senda", font=font("Fredoka.ttf", 126, 600)) + 22
    d.text((x, 110), "Pa", font=font("Fredoka.ttf", 126, 600), fill=TERRACOTTA)
    d.text((80, 262), "El pueblito de los animalitos.", font=font("Fredoka.ttf", 40, 400), fill=INK)
    d.text(
        (80, 328),
        "48 niveles  ·  24 amigos  ·  granja  ·  duelo Wi-Fi local",
        font=font("Nunito-600.ttf", 23),
        fill=SOFT,
    )

    # A small painted call to action.
    pill = (80, 398, 475, 464)
    d.rounded_rectangle(pill, radius=33, fill=TERRACOTTA)
    d.text((104, 414), "Muy pronto en Google Play", font=font("Nunito-800.ttf", 23), fill=CREAM)
    d.text((82, 548), "Senda Pa  ·  Android", font=font("Nunito-700.ttf", 21), fill=SOFT)

    # Two phones, slightly staggered, like a little diorama.
    p1 = phone(Image.open(SCREENS / "nivel.webp"), 164)
    p2 = phone(Image.open(SCREENS / "coleccion.webp"), 164)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = ImageDraw.Draw(shadow)
    sh.rounded_rectangle((700, 186, 700 + p1.width, 186 + p1.height), radius=28, fill=(74, 53, 36, 65))
    sh.rounded_rectangle((865, 240, 865 + p2.width, 240 + p2.height), radius=28, fill=(74, 53, 36, 65))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    base = Image.alpha_composite(base, shadow)
    base.alpha_composite(p1, (700, 150))
    base.alpha_composite(p2, (865, 210))

    base.convert("RGB").save(ASSETS / "og-image.jpg", "JPEG", quality=90, optimize=True)


def main() -> None:
    # Full screenshots.
    webp(GAME / "build" / "release_splash.jpg", SCREENS / "portada.webp", 760, 91)
    webp(GAME / "build" / "release_home.jpg", SCREENS / "inicio.webp", 760, 91)
    for src, dest in [
        ("02-camino.png", "nivel.webp"),
        ("05-coleccion.png", "coleccion.webp"),
        ("14-granja-completa.png", "granja.webp"),
        ("12-tienda.png", "tienda.webp"),
        ("04-victoria.png", "victoria.webp"),
        ("08-salto.png", "salto.webp"),
    ]:
        webp(GAME / "docs" / src, SCREENS / dest, 860, 90)

    # Detail crops for the bento.
    crop_webp(GAME / "docs" / "02-camino.png", FEATURES / "niveles.webp", (18, 158, 412, 552), (1000, 1000))
    crop_webp(GAME / "docs" / "05-coleccion.png", FEATURES / "amigos.webp", (14, 64, 416, 194), (1000, 323))
    crop_webp(GAME / "docs" / "14-granja-completa.png", FEATURES / "granja.webp", (15, 125, 415, 685), (900, 1260))
    crop_webp(GAME / "docs" / "12-tienda.png", FEATURES / "gorros.webp", (15, 120, 415, 660), (900, 1215))
    crop_webp(GAME / "build" / "release_home.jpg", FEATURES / "regalo.webp", (40, 245, 500, 381), (1000, 296))

    # Favicons and app mark.
    icon = Image.open(GAME / "icon.png").convert("RGBA")
    icon.save(ASSETS / "icon.png", "PNG")
    for size in (192, 180, 32):
        icon.resize((size, size), Image.Resampling.LANCZOS).save(ASSETS / f"icon-{size}.png", "PNG")
    icon.save(ASSETS / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

    # A very fine paper grain, used at low opacity in CSS.
    random.seed(7)
    noise = Image.new("RGBA", (96, 96))
    px = noise.load()
    for y in range(96):
        for x in range(96):
            v = random.randint(70, 190)
            px[x, y] = (v, v, v, random.randint(8, 22))
    noise.save(ASSETS / "noise.png", "PNG", optimize=True)

    og_image()


if __name__ == "__main__":
    main()
