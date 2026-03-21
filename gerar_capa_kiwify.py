# -*- coding: utf-8 -*-
"""
Capas Kiwify — cores claras (cream + ouro + sálvia).
- 300x250 → capa_kiwify_Destrave_Sua_Energia.png
- 600x120 (faixa) → capa_kiwify_Destrave_600x120.png
- 1376x768 (widescreen) → capa_kiwify_Destrave_1376x768.png
"""
from __future__ import annotations

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print('Instale Pillow: pip install Pillow')
    sys.exit(1)

W, H = 300, 250

# Paleta clara (alinhada ao ebook / LP)
CREAM = (252, 249, 245)
CREAM_DEEP = (238, 230, 220)
TEXT = (74, 56, 53)
TEXT_SOFT = (120, 108, 100)
GOLD = (196, 176, 130)
GOLD_DEEP = (160, 135, 95)
SAGE = (175, 188, 160)
SAGE_SOFT = (220, 228, 210)
LINE = (216, 208, 198)
WHITE = (255, 255, 255)


def _font_dir() -> str:
    return os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')


def load_font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    fonts = _font_dir()
    if italic:
        order = ['ariali.ttf', 'calibrii.ttf', 'georgiai.ttf']
    elif bold:
        order = ['arialbd.ttf', 'segoeuib.ttf', 'calibrib.ttf']
    else:
        order = ['arial.ttf', 'segoeui.ttf', 'calibri.ttf']
    for name in order:
        path = os.path.join(fonts, name)
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def composite_rgba(under: Image.Image, layer: Image.Image) -> Image.Image:
    return Image.alpha_composite(under.convert('RGBA'), layer.convert('RGBA')).convert('RGB')


def build_cover() -> Image.Image:
    img = Image.new('RGB', (W, H), CREAM)
    dr = ImageDraw.Draw(img)

    # Degradê vertical bem suave
    for y in range(H):
        t = y / max(H - 1, 1)
        r = int(CREAM[0] * (1 - t) + CREAM_DEEP[0] * t)
        g = int(CREAM[1] * (1 - t) + CREAM_DEEP[1] * t)
        b = int(CREAM[2] * (1 - t) + CREAM_DEEP[2] * t)
        dr.line((0, y, W, y), fill=(r, g, b))

    # Blobs decorativos (cantos)
    for cx, cy, r, col in [
        (-30, 40, 90, (*SAGE_SOFT, 100)),
        (W + 20, H - 30, 100, (*CREAM_DEEP, 80)),
        (W - 50, -40, 70, (*GOLD, 35)),
    ]:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        img = composite_rgba(img, lay)
    dr = ImageDraw.Draw(img)

    # Halo suave dourado (direita — leitura “energia” sem poluir)
    for r, a in [(95, 30), (65, 50), (38, 90)]:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        cx, cy = W - 28, H // 2 + 8
        ld.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*GOLD, a))
        img = composite_rgba(img, lay)
    dr = ImageDraw.Draw(img)

    # Moldura
    inset = 7
    dr.rounded_rectangle(
        (inset, inset, W - inset, H - inset),
        10,
        fill=None,
        outline=GOLD_DEEP,
        width=2,
    )
    dr.rounded_rectangle(
        (inset + 2, inset + 2, W - inset - 2, H - inset - 2),
        8,
        fill=None,
        outline=LINE,
        width=1,
    )

    font_tag = load_font(9, bold=True)
    font_t1 = load_font(19, bold=True)
    font_t2 = load_font(22, bold=True)
    font_sub = load_font(10, italic=True)
    font_pill = load_font(8, bold=True)

    x0 = 14
    y = 11

    # Selo compacto
    tag = 'E-BOOK + BÔNUS'
    tw = dr.textbbox((0, 0), tag, font=font_tag)[2]
    dr.rounded_rectangle((x0, y, x0 + tw + 14, y + 18), 6, fill=SAGE, outline=TEXT, width=1)
    dr.text((x0 + 7, y + 4), tag, font=font_tag, fill=WHITE)
    y += 26

    # Título (2 linhas — legível em 300px)
    dr.text((x0, y), 'Destrave', font=font_t1, fill=TEXT)
    y += 22
    # "Sua " + "Energia" ouro
    part_a = 'Sua '
    part_b = 'Energia'
    xa = x0
    dr.text((xa, y), part_a, font=font_t2, fill=TEXT)
    wa = dr.textbbox((0, 0), part_a, font=font_t2)[2]
    dr.text((xa + wa, y), part_b, font=font_t2, fill=GOLD_DEEP)

    y += 28
    dr.line((x0, y, W - 52, y), fill=GOLD, width=1)
    y += 7

    sub = '3 práticas · neurociência & espiritualidade'
    dr.text((x0, y), sub, font=font_sub, fill=TEXT_SOFT)

    y += 16
    # Pílulas mini (cabem em uma linha)
    pills = ['Taça', 'Espelho', 'Visualização']
    px = x0
    for i, p in enumerate(pills):
        pw = dr.textbbox((0, 0), p, font=font_pill)[2] + 10
        fill_c = SAGE_SOFT if i == 0 else (CREAM_DEEP if i == 1 else (235, 245, 240))
        dr.rounded_rectangle((px, y, px + pw, y + 16), 4, fill=fill_c, outline=GOLD_DEEP, width=1)
        dr.text((px + 5, y + 4), p, font=font_pill, fill=TEXT)
        px += pw + 5
        if px > W - 60:
            break

    y = H - 22
    foot = 'PDF · acesso imediato'
    dr.text((x0, y), foot, font=load_font(9, bold=True), fill=TEXT_SOFT)

    return img


def build_banner_600x120() -> Image.Image:
    """Faixa horizontal 600x120 — título + selo + pílulas + halo à direita."""
    bw, bh = 600, 120
    img = Image.new('RGB', (bw, bh), CREAM)
    dr = ImageDraw.Draw(img)

    # Gradiente horizontal suave
    for x in range(bw):
        t = x / max(bw - 1, 1)
        r = int(CREAM[0] * (1 - t * 0.15) + CREAM_DEEP[0] * (t * 0.12))
        g = int(CREAM[1] * (1 - t * 0.15) + CREAM_DEEP[1] * (t * 0.12))
        b = int(CREAM[2] * (1 - t * 0.15) + CREAM_DEEP[2] * (t * 0.12))
        dr.line((x, 0, x, bh), fill=(r, g, b))

    # Halo dourado à direita
    for r, a in [(100, 28), (70, 45), (40, 75)]:
        lay = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        cx, cy = bw - 36, bh // 2
        ld.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*GOLD, a))
        img = composite_rgba(img, lay)
    dr = ImageDraw.Draw(img)

    inset = 5
    dr.rounded_rectangle(
        (inset, inset, bw - inset, bh - inset),
        8,
        fill=None,
        outline=GOLD_DEEP,
        width=2,
    )

    font_tag = load_font(8, bold=True)
    font_title = load_font(20, bold=True)
    font_sub = load_font(10, italic=True)
    font_pill = load_font(8, bold=True)
    font_foot = load_font(8, bold=True)

    x0 = 12
    y_tag = 14
    tag = 'E-BOOK + BÔNUS'
    tw = dr.textbbox((0, 0), tag, font=font_tag)[2]
    dr.rounded_rectangle((x0, y_tag, x0 + tw + 12, y_tag + 20), 5, fill=SAGE, outline=TEXT, width=1)
    dr.text((x0 + 6, y_tag + 5), tag, font=font_tag, fill=WHITE)

    xt = x0 + tw + 22
    yt = 16
    # Título em uma linha: "Destrave Sua " + "Energia"
    a, b = 'Destrave Sua ', 'Energia'
    dr.text((xt, yt), a, font=font_title, fill=TEXT)
    wa = dr.textbbox((0, 0), a, font=font_title)[2]
    dr.text((xt + wa, yt), b, font=font_title, fill=GOLD_DEEP)

    y_sub = 44
    dr.line((x0, y_sub - 4, bw - 130, y_sub - 4), fill=GOLD, width=1)
    sub = '3 práticas · neurociência & espiritualidade'
    dr.text((x0, y_sub), sub, font=font_sub, fill=TEXT_SOFT)

    y_p = 66
    pills = ['Taça', 'Espelho', 'Visualização']
    px = x0
    for i, p in enumerate(pills):
        pw = dr.textbbox((0, 0), p, font=font_pill)[2] + 10
        if px + pw > bw - 125:
            break
        fill_c = SAGE_SOFT if i == 0 else (CREAM_DEEP if i == 1 else (235, 245, 240))
        dr.rounded_rectangle((px, y_p, px + pw, y_p + 18), 4, fill=fill_c, outline=GOLD_DEEP, width=1)
        dr.text((px + 5, y_p + 5), p, font=font_pill, fill=TEXT)
        px += pw + 6

    foot = 'PDF · acesso imediato'
    fw = dr.textbbox((0, 0), foot, font=font_foot)[2]
    dr.text((bw - fw - 14, bh - 24), foot, font=font_foot, fill=TEXT_SOFT)

    return img


def build_slide_1376x768() -> Image.Image:
    """Capa widescreen 1376x768 — texto à esquerda, halo dourado grande à direita."""
    sw, sh = 1376, 768
    img = Image.new('RGB', (sw, sh), CREAM)
    dr = ImageDraw.Draw(img)

    for y in range(sh):
        t = y / max(sh - 1, 1)
        r = int(CREAM[0] * (1 - t) + CREAM_DEEP[0] * t)
        g = int(CREAM[1] * (1 - t) + CREAM_DEEP[1] * t)
        b = int(CREAM[2] * (1 - t) + CREAM_DEEP[2] * t)
        dr.line((0, y, sw, y), fill=(r, g, b))

    # Blobs grandes (escala widescreen)
    for cx, cy, r, col in [
        (-120, 180, 320, (*SAGE_SOFT, 95)),
        (sw + 100, sh - 80, 340, (*CREAM_DEEP, 85)),
        (sw - 200, -100, 220, (*GOLD, 40)),
        (200, sh + 60, 280, (*SAGE, 25)),
    ]:
        lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        img = composite_rgba(img, lay)
    dr = ImageDraw.Draw(img)

    # Halo principal (direita)
    ox, oy = int(sw * 0.78), int(sh * 0.48)
    for r, a in [(420, 22), (300, 38), (200, 58), (120, 85), (70, 115)]:
        lay = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.ellipse((ox - r, oy - r, ox + r, oy + r), fill=(*GOLD, a))
        img = composite_rgba(img, lay)
    dr = ImageDraw.Draw(img)

    inset = 22
    dr.rounded_rectangle(
        (inset, inset, sw - inset, sh - inset),
        18,
        fill=None,
        outline=GOLD_DEEP,
        width=3,
    )
    dr.rounded_rectangle(
        (inset + 5, inset + 5, sw - inset - 5, sh - inset - 5),
        14,
        fill=None,
        outline=LINE,
        width=1,
    )

    font_tag = load_font(20, bold=True)
    font_t1 = load_font(76, bold=True)
    font_t2 = load_font(84, bold=True)
    font_sub = load_font(28, italic=True)
    font_pill = load_font(22, bold=True)
    font_li = load_font(22)
    font_foot = load_font(20, bold=True)

    x0 = 64
    y = 56

    tag = 'E-BOOK + PROTOCOLO + BÔNUS'
    tw = dr.textbbox((0, 0), tag, font=font_tag)[2]
    th_b = 40
    dr.rounded_rectangle((x0, y, x0 + tw + 36, y + th_b), 12, fill=SAGE, outline=TEXT, width=2)
    dr.text((x0 + 18, y + 9), tag, font=font_tag, fill=WHITE)
    y += th_b + 36

    dr.text((x0, y), 'Destrave', font=font_t1, fill=TEXT)
    y += 88
    part_a = 'Sua '
    part_b = 'Energia'
    dr.text((x0, y), part_a, font=font_t2, fill=TEXT)
    wa = dr.textbbox((0, 0), part_a, font=font_t2)[2]
    dr.text((x0 + wa, y), part_b, font=font_t2, fill=GOLD_DEEP)

    y += 100
    line_end = min(sw // 2 + 80, ox - 80)
    dr.line((x0, y, line_end, y), fill=GOLD, width=3)
    y += 28

    sub = '3 práticas · neurociência & espiritualidade · poucos minutos por dia'
    dr.text((x0, y), sub, font=font_sub, fill=TEXT_SOFT)
    y += 48

    pills = ['Taça de água', 'Espelho EU SOU', 'Visualização']
    px = x0
    for i, p in enumerate(pills):
        pw = dr.textbbox((0, 0), p, font=font_pill)[2] + 28
        if px + pw > line_end:
            break
        fill_c = SAGE_SOFT if i == 0 else (CREAM_DEEP if i == 1 else (235, 245, 240))
        dr.rounded_rectangle((px, y, px + pw, y + 44), 10, fill=fill_c, outline=GOLD_DEEP, width=2)
        dr.text((px + 14, y + 11), p, font=font_pill, fill=TEXT)
        px += pw + 14

    y += 72
    extras = [
        'Manifestação antes de dormir · declarações no espelho · visualização emocional',
    ]
    for line in extras:
        dr.text((x0, y), line, font=font_li, fill=TEXT_SOFT)
        y += 32

    foot = 'PDF · acesso imediato · garantia 7 dias'
    dr.text((x0, sh - 72), foot, font=font_foot, fill=TEXT_SOFT)

    return img


def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))

    out1 = os.path.join(base, 'capa_kiwify_Destrave_Sua_Energia.png')
    img1 = build_cover()
    img1.save(out1, 'PNG', optimize=True)
    print(f'Capa 300x250: {out1}')

    out2 = os.path.join(base, 'capa_kiwify_Destrave_600x120.png')
    img2 = build_banner_600x120()
    img2.save(out2, 'PNG', optimize=True)
    print(f'Faixa 600x120: {out2}')

    out3 = os.path.join(base, 'capa_kiwify_Destrave_1376x768.png')
    img3 = build_slide_1376x768()
    img3.save(out3, 'PNG', optimize=True)
    print(f'Widescreen 1376x768: {out3}')


if __name__ == '__main__':
    main()
