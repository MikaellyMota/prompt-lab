# -*- coding: utf-8 -*-
"""Gerador do ebook: Destrave Sua Energia (3 praticas + protocolo + bonus)."""
import sys
sys.path.insert(0, r'C:\PromptLab\Lib\site-packages')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                 Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, NextPageTemplate)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.utils import simpleSplit

EBOOK_TITLE = 'Destrave Sua Energia'
EBOOK_SUBTITLE = ('3 pr\u00e1ticas para manifestar dinheiro, clareza e '
                  'poder pessoal')

W, H = A4
LM = RM = 20 * mm
TM = 22 * mm
BM = 20 * mm
IW = W - LM - RM

# ── Paleta clara (referência: capa cream + marrom + sálvia + mogno suave) ──
CREAM   = colors.HexColor('#FAF8F5')
TEXT    = colors.HexColor('#4A3835')
GRAY    = colors.HexColor('#8A817A')
WHITE   = colors.white
GOLD    = colors.HexColor('#C4B08A')
LGOLD   = colors.HexColor('#F5EFE6')
DEEP    = colors.HexColor('#3D2F2C')
BLANCH_SAGE   = colors.HexColor('#9AAA8C')
BLANCH_MAROON = colors.HexColor('#7D5E52')
INNER_BAR     = colors.HexColor('#EDE8E2')
HEADER_STRIP  = colors.HexColor('#E6E0D9')
LINE_SOFT     = colors.HexColor('#D8D0C8')

# Acentos suaves por capítulo (fundo de box / TOC)
ROSE    = colors.HexColor('#C9A7A1')
SROSE   = colors.HexColor('#FAF0EE')
PURPLE  = colors.HexColor('#A99BB3')
MED     = colors.HexColor('#9A8AA6')
LAV     = colors.HexColor('#EDE8EF')
LLIGHT  = colors.HexColor('#F6F3F8')
TEAL    = colors.HexColor('#8BAFA5')
LTEAL   = colors.HexColor('#EAF3F0')

TECH_COLORS = [ROSE, PURPLE, TEAL]
TECH_BG     = [SROSE, LLIGHT, LTEAL]

def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY    = S('body',   fontName='Helvetica', fontSize=10.5, leading=17, textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=8)
BODYL   = S('bodyl',  fontName='Helvetica', fontSize=10.5, leading=17, textColor=TEXT, alignment=TA_LEFT, spaceAfter=6)
BOLDB   = S('boldb',  fontName='Helvetica-Bold', fontSize=10.5, leading=17, textColor=TEXT, spaceAfter=6)
BULLET  = S('bul',    fontName='Helvetica', fontSize=10.5, leading=16, textColor=TEXT, leftIndent=16, firstLineIndent=-10, spaceAfter=5)
QUOTE   = S('quote',  fontName='Helvetica-Oblique', fontSize=11.5, leading=18, textColor=BLANCH_MAROON, alignment=TA_CENTER, spaceAfter=6)
STEP_T  = S('stept',  fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=TEXT, spaceAfter=3)
GOLD_T  = S('goldt',  fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=GOLD, spaceAfter=3)
AFF     = S('aff',    fontName='Helvetica-Oblique', fontSize=11, leading=17, textColor=TEXT, spaceAfter=5)
TOC_T   = S('toct',   fontName='Helvetica-Bold', fontSize=13, leading=18, textColor=TEXT, spaceAfter=3)
TOC_D   = S('tocd',   fontName='Helvetica', fontSize=10, leading=14, textColor=GRAY, spaceAfter=2)
SMALL   = S('small',  fontName='Helvetica', fontSize=9, leading=13, textColor=GRAY, spaceAfter=4)
CLOSING = S('cl',     fontName='Helvetica-Oblique', fontSize=14, leading=22, textColor=TEXT, alignment=TA_CENTER, spaceAfter=8)
MANIFESTO = S('manifest', fontName='Helvetica', fontSize=11.5, leading=18,
              textColor=TEXT, alignment=TA_CENTER, spaceAfter=6)


# ── Flowables ──────────────────────────────────────────────────────────────

class FullPage(Flowable):
    def wrap(self, avW, avH):
        return avW, 0
    def draw(self):
        pass


class AccentBar(Flowable):
    def __init__(self, iw=IW, color=GOLD, h=2.5):
        super().__init__()
        self.iw = iw; self.color = color; self.bh = h
    def wrap(self, *a):
        return self.iw, self.bh + 4
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 2, self.iw, self.bh, fill=1, stroke=0)


class ChapterHeader(Flowable):
    def __init__(self, num, title, subtitle, badge, color=PURPLE, iw=IW):
        super().__init__()
        self.num = num; self.title = title; self.subtitle = subtitle
        self.badge = badge; self.color = color; self.iw = iw
        self.height = 46 * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw
        h = self.height
        c.setFillColor(self.color)
        c.roundRect(0, 0, iw, h, 4 * mm, fill=1, stroke=0)
        c.setStrokeColor(LINE_SOFT)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, iw, h, 4 * mm, fill=0, stroke=1)
        c.setFillColor(TEXT)
        c.setFillAlpha(0.06)
        c.setFont('Helvetica-Bold', 90)
        c.drawRightString(iw - 6 * mm, 0 * mm, str(self.num))
        c.setFillAlpha(1.0)
        c.setFillColor(GOLD)
        c.roundRect(8 * mm, h - 14 * mm, 34 * mm, 8 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillColor(DEEP)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(10 * mm, h - 14 * mm + 2.5 * mm, self.badge)
        c.setFillColor(TEXT)
        c.setFont('Helvetica-Bold', 19)
        c.drawString(8 * mm, h - 26 * mm, self.title)
        c.setFillColor(GRAY)
        c.setFont('Helvetica-Oblique', 11)
        c.drawString(8 * mm, h - 33 * mm, self.subtitle)


class TipBox(Flowable):
    def __init__(self, lines, color=GOLD, bg=LGOLD, iw=IW, label='DICA'):
        super().__init__()
        self.lines = lines; self.color = color; self.bg = bg
        self.iw = iw; self.label = label
        self.height = (14 + len(lines) * 14 + 6) * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw; h = self.height
        c.setFillColor(self.bg)
        c.roundRect(0, 0, iw, h, 3 * mm, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, 0, 3 * mm, h, 1.5 * mm, fill=1, stroke=0)
        c.setFillColor(DEEP)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(8 * mm, h - 9 * mm, f'\u2728  {self.label}')
        c.setStrokeColor(self.color)
        c.setLineWidth(0.5)
        c.line(8 * mm, h - 11 * mm, iw - 5 * mm, h - 11 * mm)
        c.setFillColor(TEXT)
        c.setFont('Helvetica', 9.5)
        y = h - 15 * mm
        for line in self.lines:
            c.drawString(8 * mm, y, line)
            y -= 6.5 * mm


class RuleBox(Flowable):
    """Caixa de Regras de Ouro"""
    def __init__(self, rules, iw=IW, color=GOLD):
        super().__init__()
        self.rules = rules; self.iw = iw; self.color = color
        self.height = (14 + len(rules) * 13 + 6) * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw; h = self.height
        c.setFillColor(LGOLD)
        c.roundRect(0, 0, iw, h, 3 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(0, 0, 3 * mm, h, 1.5 * mm, fill=1, stroke=0)
        c.setFillColor(DEEP)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(8 * mm, h - 9 * mm, '\u2605  REGRAS DE OURO')
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.5)
        c.line(8 * mm, h - 11 * mm, iw - 5 * mm, h - 11 * mm)
        c.setFillColor(TEXT)
        c.setFont('Helvetica', 9.5)
        y = h - 15 * mm
        for rule in self.rules:
            c.drawString(8 * mm, y, f'\u2022  {rule}')
            y -= 6.5 * mm


class QuoteBox(Flowable):
    def __init__(self, text, author='', iw=IW, color=PURPLE, bg=LAV):
        super().__init__()
        self.text = text; self.author = author
        self.iw = iw; self.color = color; self.bg = bg
        self.height = 32 * mm if author else 26 * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw; h = self.height
        c.setFillColor(self.bg)
        c.roundRect(0, 0, iw, h, 3 * mm, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.roundRect(0, 0, 3 * mm, h, 1.5 * mm, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.setFillAlpha(0.2)
        c.setFont('Helvetica-Bold', 50)
        c.drawString(4 * mm, h - 16 * mm, '\u201c')
        c.setFillAlpha(1.0)
        c.setFillColor(self.color)
        c.setFont('Helvetica-Oblique', 11)
        c.drawCentredString(iw / 2, h - 13 * mm, self.text)
        if self.author:
            c.setFillColor(GRAY)
            c.setFont('Helvetica', 9)
            c.drawCentredString(iw / 2, h - 21 * mm, f'\u2014 {self.author}')


# ── Fundo de páginas ─────────────────────────────────────────────────────────

def _hline(c, y, x0=None, x1=None, w=0.6, col=None):
    col = col or GOLD
    x0 = x0 if x0 is not None else W * 0.18
    x1 = x1 if x1 is not None else W * 0.82
    c.saveState()
    c.setStrokeColor(col)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)
    c.restoreState()


def draw_cover_blanch(c):
    """Capa vetorial com hierarquia forte: moldura, brilho, painel e t\u00edtulo em destaque."""
    bg = colors.HexColor('#FCFAF7')
    text_main = colors.HexColor('#2F2623')
    text_soft = colors.HexColor('#6B625C')
    text_faint = colors.HexColor('#9A918A')
    sage = colors.HexColor('#8FA882')
    sage_edge = colors.HexColor('#55604C')
    mahogany = colors.HexColor('#8B5E4F')
    mahogany_edge = colors.HexColor('#4A3228')
    gold_glow = colors.HexColor('#C9B896')
    gold_accent = colors.HexColor('#B89B6A')
    line_col = colors.HexColor('#D5CDC4')
    panel_bg = colors.HexColor('#F3EBE3')
    shadow = colors.HexColor('#1A1412')

    c.setFillColor(bg)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Cantos com mais contraste
    c.saveState()
    c.setFillColor(colors.HexColor('#E8DFD4'))
    c.setFillAlpha(0.55)
    c.circle(-38 * mm, H + 28 * mm, 135 * mm, fill=1, stroke=0)
    c.circle(W + 38 * mm, -28 * mm, 125 * mm, fill=1, stroke=0)
    c.restoreState()

    # Moldura dupla (chama aten\u00e7\u00e3o sem pesar)
    inset = 11 * mm
    c.setStrokeColor(gold_accent)
    c.setLineWidth(1.15)
    c.roundRect(inset, inset, W - 2 * inset, H - 2 * inset, 2.5 * mm, fill=0, stroke=1)
    c.setStrokeColor(mahogany_edge)
    c.setLineWidth(0.5)
    c.setFillAlpha(0.35)
    c.roundRect(inset + 2.5 * mm, inset + 2.5 * mm,
                W - 2 * (inset + 2.5 * mm), H - 2 * (inset + 2.5 * mm),
                2 * mm, fill=0, stroke=1)
    c.setFillAlpha(1.0)

    # Ornamentos nos cantos internos da moldura
    L = 9 * mm
    gap_o = inset + 5 * mm
    c.setStrokeColor(gold_accent)
    c.setLineWidth(0.85)
    for ox, oy, dx, dy in [
        (gap_o, H - gap_o, 1, -1),
        (W - gap_o, H - gap_o, -1, -1),
        (gap_o, gap_o, 1, 1),
        (W - gap_o, gap_o, -1, 1),
    ]:
        c.line(ox, oy, ox + L * dx, oy)
        c.line(ox, oy, ox, oy + L * dy)

    # Halo mais intenso atr\u00e1s do t\u00edtulo
    vc = H * 0.52
    cy_glow = vc + 10 * mm
    for r, a in [(102, 0.038), (78, 0.055), (52, 0.08), (28, 0.1)]:
        c.setFillColor(gold_glow)
        c.setFillAlpha(a)
        c.circle(W / 2, cy_glow, r * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    mx = W * 0.14
    ty = vc + 50 * mm
    title_txt = 'Destrave Sua Energia'
    # Sombra em camadas (profundidade)
    c.saveState()
    c.setFont('Helvetica-Bold', 35)
    for dx, dy, a in [(2.2, -2.2, 0.08), (1.2, -1.2, 0.12), (0.5, -0.5, 0.16)]:
        c.setFillColor(shadow)
        c.setFillAlpha(a)
        c.drawCentredString(W / 2 + dx, ty + dy, title_txt)
    c.restoreState()
    c.setFillColor(text_main)
    c.setFont('Helvetica-Bold', 35)
    c.drawCentredString(W / 2, ty, title_txt)

    # Filete dourado sob o t\u00edtulo
    bar_w = 52 * mm
    c.setFillColor(gold_accent)
    c.setFillAlpha(0.9)
    c.roundRect(W / 2 - bar_w / 2, ty - 4.5 * mm, bar_w, 2.2 * mm, 0.8 * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    c.setFillColor(text_soft)
    c.setFont('Helvetica-Oblique', 11.2)
    sub = ('3 pr\u00e1ticas para manifestar dinheiro, clareza e poder '
           'pessoal')
    sub_w = 122 * mm
    sub_lines = simpleSplit(sub, 'Helvetica-Oblique', 11.2, sub_w)
    sy = ty - 16 * mm
    for line in sub_lines:
        c.drawCentredString(W / 2, sy, line)
        sy -= 4.2 * mm

    quote_y = sy - 8 * mm
    teaser = [
        'Voc\u00ea est\u00e1 prestes a mudar algo em voc\u00ea.',
        'N\u00e3o \u00e9 misticismo vazio.',
        '\u00c9 a uni\u00e3o entre inten\u00e7\u00e3o energ\u00e9tica,',
        'neuroci\u00eancia e espiritualidade.',
    ]
    tw = 128 * mm
    q_lead = 6.5 * mm
    pad_v = 5.5 * mm
    pad_h = 9 * mm

    # Conta linhas ap\u00f3s quebra (para altura do painel)
    def _quote_line_count():
        n = 0
        n += len(simpleSplit(teaser[0], 'Helvetica-BoldOblique', 13.5, tw))
        for raw in teaser[1:]:
            n += len(simpleSplit(raw, 'Helvetica-Oblique', 12.3, tw))
        return max(n, 4)

    n_q_lines = _quote_line_count()
    ly0 = quote_y - 6 * mm
    panel_top = ly0 + pad_v
    panel_bot = ly0 - n_q_lines * q_lead - pad_v
    box_h = panel_top - panel_bot
    box_w = tw + 2 * pad_h
    box_x = (W - box_w) / 2
    box_y = panel_bot

    # Painel do manifesto (cart\u00e3o)
    c.saveState()
    c.setFillColor(panel_bg)
    c.setFillAlpha(0.92)
    c.setStrokeColor(mahogany_edge)
    c.setLineWidth(0.65)
    c.roundRect(box_x, box_y, box_w, box_h, 4.5 * mm, fill=1, stroke=1)
    c.restoreState()
    c.setFillColor(gold_accent)
    c.rect(box_x + 1.2 * mm, box_y + 5 * mm, 3.2 * mm,
           max(box_h - 10 * mm, 12 * mm), fill=1, stroke=0)

    ly = ly0
    c.setFont('Helvetica-BoldOblique', 13.5)
    c.setFillColor(mahogany_edge)
    for part in simpleSplit(teaser[0], 'Helvetica-BoldOblique', 13.5, tw):
        c.drawCentredString(W / 2, ly, part)
        ly -= q_lead
    c.setFont('Helvetica-Oblique', 12.3)
    c.setFillColor(text_main)
    for raw in teaser[1:]:
        for part in simpleSplit(raw, 'Helvetica-Oblique', 12.3, tw):
            c.drawCentredString(W / 2, ly, part)
            ly -= q_lead

    bw, bh, gap = 64 * mm, 12.5 * mm, 6 * mm
    x0 = (W - (2 * bw + gap)) / 2
    yb = box_y - bh - 8 * mm
    if yb < 24 * mm:
        yb = 24 * mm
    for (x, fill_col, edge_col, lab) in (
        (x0, sage, sage_edge, 'NEUROCI\u00caNCIA'),
        (x0 + bw + gap, mahogany, mahogany_edge, 'ESPIRITUALIDADE'),
    ):
        c.setFillColor(colors.HexColor('#000000'))
        c.setFillAlpha(0.12)
        c.roundRect(x + 0.8 * mm, yb - 0.8 * mm, bw, bh, 3.2 * mm, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        c.setFillColor(fill_col)
        c.roundRect(x, yb, bw, bh, 3.2 * mm, fill=1, stroke=0)
        c.setStrokeColor(edge_col)
        c.setLineWidth(0.85)
        c.roundRect(x, yb, bw, bh, 3.2 * mm, fill=0, stroke=1)
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 9.2)
        c.drawCentredString(x + bw / 2, yb + 3.9 * mm, lab)

    yf = 20 * mm
    c.setStrokeColor(gold_accent)
    c.setLineWidth(0.55)
    c.line(mx, yf + 7 * mm, W - mx, yf + 7 * mm)
    c.setFillColor(text_faint)
    c.setFont('Helvetica-Bold', 7.2)
    c.drawCentredString(W / 2, yf + 3 * mm,
                        'Neuroci\u00eancia & Espiritualidade')


def draw_consistencia_page(c):
    """P\u00e1gina 'A regra de ouro' / CONSIST\u00caNCIA \u2014 conte\u00fado centrado na p\u00e1gina."""
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    _hline(c, H - 18 * mm, col=LINE_SOFT)
    _hline(c, 16 * mm, col=LINE_SOFT)

    cx = W / 2
    mid = H * 0.5
    for r, a in [(95, 0.04), (72, 0.06), (48, 0.08)]:
        c.setFillColor(GOLD)
        c.setFillAlpha(a)
        c.circle(cx, mid, r * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 8)
    c.drawCentredString(cx, mid + 52 * mm, 'A REGRA DE OURO')
    _hline(c, mid + 48 * mm, W * 0.35, W * 0.65)

    c.setFillColor(TEXT)
    c.setFont('Helvetica-Bold', 46)
    c.drawCentredString(cx, mid + 18 * mm, 'CONSIS-')
    c.drawCentredString(cx, mid - 10 * mm, 'T\u00caNCIA.')
    _hline(c, mid - 20 * mm, W * 0.30, W * 0.70)

    c.setFillColor(TEXT)
    c.setFont('Helvetica', 11)
    c.drawCentredString(cx, mid - 30 * mm, 'Fa\u00e7a todos os dias. Sem exce\u00e7\u00e3o.')
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Oblique', 10.5)
    c.drawCentredString(cx, mid - 39 * mm,
                        'A repeti\u00e7\u00e3o \u00e9 o que transforma inten\u00e7\u00e3o em realidade.')

    c.setFillColor(GRAY)
    c.setFont('Helvetica', 7)
    c.drawCentredString(cx, 11 * mm,
                        'Destrave Sua Energia \u2022 Neuroci\u00eancia & Espiritualidade')


def draw_inner(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INNER_BAR)
    c.rect(0, 0, 3 * mm, H, fill=1, stroke=0)
    c.setFillColor(HEADER_STRIP)
    c.rect(0, H - TM, W, TM, fill=1, stroke=0)
    c.setStrokeColor(LINE_SOFT)
    c.setLineWidth(0.6)
    c.line(0, H - TM, W, H - TM)
    c.setFillColor(TEXT)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(LM, H - TM + 8 * mm, EBOOK_TITLE.upper())
    c.setFillColor(GRAY)
    c.setFont('Helvetica-Oblique', 8)
    c.drawRightString(W - RM, H - TM + 8 * mm, 'Neuroci\u00eancia & Espiritualidade')
    pn = c.getPageNumber()
    if pn > 2:
        c.setFillColor(GRAY)
        c.setFont('Helvetica', 8)
        c.drawCentredString(W / 2, 10 * mm, str(pn - 2))


# ── Helpers ──────────────────────────────────────────────────────────────────
def b(t):   return Paragraph(t, BODY)
def bl(t):  return Paragraph(t, BODYL)
def bb(t):  return Paragraph(t, BOLDB)
def bul(t): return Paragraph(f'\u2022  {t}', BULLET)
def aff(t): return Paragraph(f'\u201c{t}\u201d', AFF)
def sp(n=5): return Spacer(1, n * mm)


def step_row(num, title, desc, color=PURPLE, iw=IW):
    return Table(
        [[Paragraph(f'<b>{num}</b>', S(f'sn{num}', fontName='Helvetica-Bold', fontSize=16,
                                        leading=20, textColor=color, alignment=TA_CENTER)),
          [Paragraph(f'<b>{title}</b>', STEP_T), Paragraph(desc, BODYL)]]],
        colWidths=[14 * mm, iw - 14 * mm],
        style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (1, 0), (1, 0), 6),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, LAV),
        ])
    )


# ── Conteúdo ─────────────────────────────────────────────────────────────────

def _abertura_vertical_pad_pt():
    """Padding topo/rodap\u00e9 (em pt) para centralizar o bloco da abertura no frame interno."""
    inner_h = H - TM - BM
    bar_h = 2.5 + 4  # AccentBar.wrap (altura do flowable)
    # Estimativa do par\u00e1grafo manifesto (linhas + <br/><br/>)
    para_h_est = 330
    core = bar_h + 8 * mm + para_h_est + 6 * mm + bar_h
    pad = (inner_h - core) / 2
    return max(5 * mm, pad)


def build_content(iw):
    story = []
    story.append(Spacer(1, 1))
    story.append(NextPageTemplate('manifest'))
    story.append(PageBreak())
    story.append(Spacer(1, 1))
    story.append(NextPageTemplate('inner'))
    story.append(PageBreak())

    # ── Abertura (antes do sum\u00e1rio), centralizada na p\u00e1gina ───────────────
    _pad_ab = _abertura_vertical_pad_pt()
    story.append(Spacer(1, _pad_ab))
    story.append(AccentBar(iw, GOLD))
    story.append(sp(8))
    story.append(Paragraph(
        'Cada t\u00e9cnica aqui foi escolhida por ser<br/>'
        'f\u00e1cil de incorporar \u00e0 rotina<br/>'
        '\u2014 e por gerar resultados reais.<br/><br/>'
        'Voc\u00ea n\u00e3o precisa acreditar em tudo agora.<br/>'
        'S\u00f3 precisa come\u00e7ar.<br/><br/>'
        'O que transforma n\u00e3o \u00e9 o talento.<br/>'
        'N\u00e3o \u00e9 a sorte.<br/>'
        'N\u00e3o \u00e9 o momento certo.<br/><br/>'
        '\u00c9 a pr\u00e1tica di\u00e1ria.<br/>'
        '\u00c9 a consist\u00eancia.<br/>'
        '\u00c9 voc\u00ea escolhendo a si mesma,<br/>'
        'todos os dias.',
        MANIFESTO))
    story.append(sp(6))
    story.append(AccentBar(iw, GOLD))
    story.append(Spacer(1, _pad_ab))
    story.append(PageBreak())

    # ── Sumário (esta p\u00e1gina: apenas sum\u00e1rio) ───────────────────────────
    story.append(sp(8))
    story.append(Paragraph('<b>S U M \u00c1 R I O</b>',
                           S('toch', fontName='Helvetica-Bold', fontSize=28, leading=34,
                             textColor=TEXT, alignment=TA_LEFT, spaceAfter=6)))
    story.append(AccentBar(iw, GOLD))
    story.append(sp(6))

    toc = [
        ('\u2665', 'T\u00c9CNICA 01', 'Ta\u00e7a de \u00c1gua',
         'Manifesta\u00e7\u00e3o antes de dormir', ROSE),
        ('\u2728', 'T\u00c9CNICA 02', 'Espelho \u2014 EU SOU',
         'Declara\u00e7\u00f5es sagradas no espelho', PURPLE),
        ('\ud83e\udde0', 'T\u00c9CNICA 03', 'Visualiza\u00e7\u00e3o Emocional',
         'Baseada na neuroci\u00eancia de Dr. Joe Dispenza', TEAL),
        ('\u23f1', 'PROTOCOLO', 'Semanal',
         'Como encaixar as 3 t\u00e9cnicas na rotina', MED),
        ('\u2605', 'B\u00d4NUS', 'Pr\u00e1tica da Lua Nova',
         'T\u00e9cnica 369 Lunar + Perfume Energ\u00e9tico', GOLD),
    ]
    for icon, label, title, desc, col in toc:
        hex_str = col.hexval().replace('0x','').replace('#','')
        row = Table(
            [[Paragraph(f'<font color="#{hex_str}"><b>{icon}</b></font>',
                        S('ti', fontName='Helvetica-Bold', fontSize=20, leading=24,
                          textColor=col, alignment=TA_CENTER)),
              [Paragraph(f'<font color="#{hex_str}">{label}</font>',
                         S('tl', fontName='Helvetica-Bold', fontSize=9, leading=12,
                           textColor=col, spaceAfter=1)),
               Paragraph(f'<b>{title}</b>', TOC_T),
               Paragraph(desc, TOC_D)]]],
            colWidths=[16 * mm, iw - 16 * mm],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ])
        )
        story.append(row)
        story.append(AccentBar(iw, LAV, 1))
        story.append(sp(1))

    story.append(PageBreak())

    # ── Introdu\u00e7\u00e3o (p\u00e1gina seguinte ao sum\u00e1rio) ───────────────────
    story.append(sp(8))
    story.append(Paragraph('<b>DESTRAVE SUA ENERGIA</b>',
                           S('introtitle', fontName='Helvetica-Bold', fontSize=22, leading=28,
                             textColor=TEXT, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph(
        'Ta\u00e7a, espelho, visualiza\u00e7\u00e3o, protocolo semanal e b\u00f4nus \u2014 no mesmo tom leve deste guia.',
        S('introsub', fontName='Helvetica-Oblique', fontSize=12, leading=17,
          textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)))
    story.append(AccentBar(iw, ROSE, 2))
    story.append(sp(3))
    story.append(b('Voc\u00ea est\u00e1 prestes a aprender tr\u00eas das pr\u00e1ticas mais poderosas de manifesta\u00e7\u00e3o \u2014 simples, acess\u00edveis e com resultados comprovados por quem pratica com consist\u00eancia.'))
    story.append(b('N\u00e3o \u00e9 misticismo vazio. \u00c9 a uni\u00e3o entre inten\u00e7\u00e3o energ\u00e9tica, neuroci\u00eancia e espiritualidade pr\u00e1tica.'))
    story.append(TipBox(['O segredo de toda pr\u00e1tica de manifesta\u00e7\u00e3o \u00e9 um s\u00f3: CONSIST\u00caNCIA.',
                         'Fa\u00e7a todos os dias. Sem exce\u00e7\u00e3o. A repeti\u00e7\u00e3o \u00e9 o que transforma inten\u00e7\u00e3o em realidade.'],
                        label='LEMBRE SEMPRE'))
    story.append(sp(4))
    story.append(bb('Como usar este ebook (bem simples)'))
    story.append(AccentBar(iw, PURPLE, 2))
    story.append(sp(2))
    story.append(b('1) Leia as <b>tr\u00eas t\u00e9cnicas</b> na ordem (Ta\u00e7a, Espelho, Visualiza\u00e7\u00e3o). Cada uma tem o <b>porqu\u00ea</b> e o <b>passo a passo</b>.'))
    story.append(b('2) Depois abra o cap\u00edtulo <b>Protocolo semanal</b>. L\u00e1 voc\u00ea v\u00ea como juntar tudo no dia a dia.'))
    story.append(b('3) No final, o <b>b\u00f4nus</b> explica a T\u00e9cnica 369 (escrita) e a pr\u00e1tica da Lua Nova. Sem pressa: volte ao b\u00f4nus quando quiser aprofundar.'))
    story.append(b('4) Se ficar em d\u00favida, procure as caixas <b>RESUMO R\u00c1PIDO</b> no fim de cada t\u00e9cnica.'))
    story.append(sp(3))
    story.append(TipBox([
        'Ta\u00e7a de \u00e1gua = pr\u00e1tica da noite + gole pela manh\u00e3.',
        'Espelho = frases EU SOU olhando nos seus olhos.',
        'Visualiza\u00e7\u00e3o = fechar os olhos, sentir como se j\u00e1 tivesse acontecido (com m\u00fasica 528 Hz).',
        '369 = escrever a mesma afirma\u00e7\u00e3o no papel: 3x de manh\u00e3, 6x \u00e0 tarde, 9x \u00e0 noite (detalhes no b\u00f4nus).',
    ], color=PURPLE, bg=LLIGHT, label='O QUE \u00c9 CADA COISA'))

    # ── TÉCNICA 1: Taça de Água ──────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(1, 'Ta\u00e7a de \u00c1gua',
                               'Manifesta\u00e7\u00e3o antes de dormir', 'T\u00c9CNICA 01', ROSE, iw))
    story.append(sp(5))
    story.append(TipBox(['IMPORTANTE: Esta pr\u00e1tica tem que ser feita ANTES DE DORMIR!',
                         'Fez e foi dormir. N\u00e3o \u00e9 pra fazer e ir conversar, sair, assistir...',
                         'N\u00c3O! \u00c9 pra fazer e ir DORMIR!'],
                        color=ROSE, bg=SROSE, label='ATEN\u00c7\u00c3O'))
    story.append(sp(5))

    story.append(bb('Por que funciona \u2014 pela neuroci\u00eancia'))
    story.append(AccentBar(iw, ROSE, 2))
    story.append(sp(3))
    story.append(b('O momento antes de dormir \u00e9 um dos mais poderosos para o seu c\u00e9rebro. Nesse estado, o c\u00e9rebro entra nas ondas Alfa e Teta \u2014 o mesmo estado de relaxamento profundo em que ele \u00e9 mais receptivo a novas informa\u00e7\u00f5es. \u00c9 quando o filtro cr\u00edtico da mente consciente baixa a guarda, e qualquer mensagem que voc\u00ea der ao seu subconsciente \u00e9 absorvida com muito mais intensidade do que durante o dia.'))
    story.append(b('Falar sua inten\u00e7\u00e3o em voz alta, com emo\u00e7\u00e3o e com todos os detalhes, ativa o c\u00f3rtex pr\u00e9-frontal \u2014 a \u00e1rea respons\u00e1vel por criar imagens mentais v\u00edvidas \u2014 e come\u00e7a a reprogramar as cren\u00e7as que guiam suas a\u00e7\u00f5es.'))
    story.append(sp(4))

    story.append(bb('Por que funciona \u2014 pela espiritualidade'))
    story.append(AccentBar(iw, ROSE, 2))
    story.append(sp(3))
    story.append(b('A \u00e1gua \u00e9 considerada, em praticamente todas as tradi\u00e7\u00f5es espirituais, um dos elementos mais receptivos da natureza. Ela carrega mem\u00f3ria, absorve energia e transmite inten\u00e7\u00e3o.'))
    story.append(b('Pesquisas do cientista japon\u00eas Masaru Emoto sugerem que a \u00e1gua responde a palavras, inten\u00e7\u00f5es e emo\u00e7\u00f5es \u2014 formando cristais diferentes de acordo com o que recebe. Quando voc\u00ea fala com a boca dentro do copo, voc\u00ea est\u00e1 carregando essa \u00e1gua com a sua inten\u00e7\u00e3o mais profunda.'))
    story.append(b('Ao beb\u00ea-la, voc\u00ea literalmente internaliza essa energia \u2014 ela entra no seu campo energ\u00e9tico e come\u00e7a a trabalhar de dentro pra fora.'))
    story.append(sp(5))

    story.append(bb('Como fazer:'))
    story.append(AccentBar(iw, ROSE, 2))
    story.append(sp(3))

    story.append(step_row('1', 'Antes de dormir, pegue um copo com \u00e1gua',
        'Use um copo que voc\u00ea possa deixar ao lado da cama durante a noite.', ROSE, iw))
    story.append(sp(2))
    story.append(step_row('2', 'Fale sua inten\u00e7\u00e3o tr\u00eas vezes',
        'Coloque a boca pr\u00f3xima \u00e0 \u00e1gua e fale 3 vezes \u2014 sempre como se j\u00e1 fosse realidade, com todos os detalhes. Exemplo: \u201c\u00c1gua, eu tenho R$ 3.000 na minha conta no dia 10.\u201d', ROSE, iw))
    story.append(sp(2))
    story.append(step_row('3', 'Beba tr\u00eas goles com inten\u00e7\u00e3o',
        'Cada gole com presen\u00e7a, como se voc\u00ea estivesse assimilando o que declarou.', ROSE, iw))
    story.append(sp(2))
    story.append(step_row('4', 'Deixe o restante ao seu lado',
        'Ao acordar, beba o restante do copo assim que abrir os olhos \u2014 esses primeiros instantes tamb\u00e9m s\u00e3o poderosos para o c\u00e9rebro.', ROSE, iw))
    story.append(sp(2))
    story.append(step_row('5', 'V\u00e1 direto dormir',
        'Sem celular, sem conversa. Ap\u00f3s a pr\u00e1tica, encerre o dia e durma com a inten\u00e7\u00e3o.', ROSE, iw))
    story.append(sp(4))
    story.append(QuoteBox(
        '\u00c1gua, eu tenho R$ 3.000 na minha conta no dia 10.',
        'exemplo de frase espec\u00edfica', iw, ROSE, SROSE))
    story.append(sp(3))
    story.append(b('Seja espec\u00edfica: valor, data, detalhes. Quanto mais concreto, mais claro o sinal para o seu sistema nervoso e para a sua inten\u00e7\u00e3o.'))
    story.append(sp(5))

    story.append(RuleBox([
        'Fale dentro da \u00e1gua, com a boca no copo',
        'Pedidos espec\u00edficos com todos os detalhes',
        'Fa\u00e7a TODO DIA',
    ], iw, ROSE))
    story.append(sp(4))
    story.append(TipBox([
        'Noite: copo + falar 3x na \u00e1gua + 3 goles + deixar o resto ao lado da cama.',
        'Manh\u00e3: ao acordar, beber o que sobrou no copo.',
        'Regra de ouro: depois da pr\u00e1tica da noite, ir dormir sem celular.',
    ], color=ROSE, bg=SROSE, label='RESUMO R\u00c1PIDO \u2014 TA\u00c7A'))

    # ── TÉCNICA 2: Espelho ───────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(2, 'Espelho \u2014 EU SOU',
                               'Declara\u00e7\u00f5es sagradas no espelho', 'T\u00c9CNICA 02', PURPLE, iw))
    story.append(sp(5))

    story.append(bb('Por que funciona \u2014 pela neuroci\u00eancia'))
    story.append(AccentBar(iw, PURPLE, 2))
    story.append(sp(3))
    story.append(b('Quando voc\u00ea olha nos pr\u00f3prios olhos e faz uma declara\u00e7\u00e3o em voz alta, seu c\u00e9rebro recebe esse est\u00edmulo de forma muito mais intensa do que um pensamento silencioso. A voz ativa o sistema auditivo, o espelho ativa o sistema visual, e a emo\u00e7\u00e3o que voc\u00ea coloca ativa o sistema l\u00edmbico \u2014 o centro emocional do c\u00e9rebro.'))
    story.append(b('Essa combina\u00e7\u00e3o cria conex\u00f5es neurais novas e poderosas. Com a repeti\u00e7\u00e3o di\u00e1ria, essas conex\u00f5es se fortalecem \u2014 \u00e9 o que a neuroci\u00eancia chama de neuroplasticidade: o c\u00e9rebro literalmente se reconfigura para acreditar no que voc\u00ea declara.'))
    story.append(b('O que voc\u00ea repete, voc\u00ea passa a acreditar. O que voc\u00ea acredita, voc\u00ea passa a agir como se fosse verdade. E o que voc\u00ea age, se torna realidade.'))
    story.append(sp(4))

    story.append(bb('Por que funciona \u2014 pela espiritualidade'))
    story.append(AccentBar(iw, PURPLE, 2))
    story.append(sp(3))
    story.append(b('Quando Mois\u00e9s perguntou a Deus qual era o Seu nome, a resposta foi: \u201cEU SOU O QUE SOU.\u201d Isso n\u00e3o \u00e9 coincid\u00eancia.'))
    story.append(sp(2))
    story.append(QuoteBox('EU SOU O QUE SOU.',
                          'Tradi\u00e7\u00e3o b\u00edblica', iw=iw, color=PURPLE, bg=LLIGHT))
    story.append(sp(3))
    story.append(b('As duas palavras \u201cEU SOU\u201d s\u00e3o consideradas a declara\u00e7\u00e3o mais sagrada que existe. Toda tradi\u00e7\u00e3o espiritual \u2014 do misticismo judaico ao budismo, do hermetismo ao xamanismo \u2014 reconhece o EU SOU como a fonte de toda cria\u00e7\u00e3o.'))
    story.append(b('Quando voc\u00ea usa o EU SOU, voc\u00ea n\u00e3o est\u00e1 pedindo \u2014 voc\u00ea est\u00e1 <b>declarando</b>. E voc\u00ea est\u00e1 invocando a mesma for\u00e7a criadora que existe desde o princ\u00edpio.'))
    story.append(b('O espelho, por sua vez, \u00e9 um portal de autoconhecimento. Olhar nos pr\u00f3prios olhos \u00e9 um ato de coragem espiritual \u2014 \u00e9 dizer ao universo: eu me vejo, eu me reconhe\u00e7o, eu sou isso.'))
    story.append(sp(5))

    story.append(bb('Como fazer:'))
    story.append(AccentBar(iw, PURPLE, 2))
    story.append(sp(3))
    story.append(b('Todo dia, na frente do espelho \u2014 ao escovar os dentes, se arrumar, em qualquer momento \u2014 olhe nos seus pr\u00f3prios olhos e declare em voz alta suas afirma\u00e7\u00f5es com <b>EU SOU</b>.'))
    story.append(sp(4))

    story.append(bb('Exemplos de afirma\u00e7\u00f5es:'))
    affirmations_general = [
        'Eu sou pr\u00f3spera',
        'Eu sou aben\u00e7oada',
        'Eu sou protegida',
        'Eu sou saud\u00e1vel',
        'Eu sou magn\u00e9tica',
    ]
    tbl_data = [[Paragraph(f'\u2728 {a}', S('afr', fontName='Helvetica-Oblique', fontSize=11,
                                             leading=16, textColor=TEXT))] for a in affirmations_general]
    tbl = Table(tbl_data, colWidths=[iw],
                style=TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), LLIGHT),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [LLIGHT, LAV]),
                ]))
    story.append(tbl)
    story.append(sp(4))

    story.append(bb('Se voc\u00ea trabalha com vendas, especifique:'))
    affirmations_sales = [
        'Eu sou a melhor vendedora',
        'Eu sou a vendedora que bateu a meta',
        'Eu sou a vendedora que fecha neg\u00f3cios com facilidade',
    ]
    tbl_data2 = [[Paragraph(f'\u2728 {a}', S('afr2', fontName='Helvetica-Oblique', fontSize=11,
                                              leading=16, textColor=ROSE))] for a in affirmations_sales]
    tbl2 = Table(tbl_data2, colWidths=[iw],
                 style=TableStyle([
                     ('BACKGROUND', (0, 0), (-1, -1), SROSE),
                     ('TOPPADDING', (0, 0), (-1, -1), 5),
                     ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                     ('LEFTPADDING', (0, 0), (-1, -1), 12),
                 ]))
    story.append(tbl2)
    story.append(sp(4))

    story.append(b('Adapte para a sua realidade. Se voc\u00ea trabalha com vendas: \u201cEu sou a vendedora que fecha neg\u00f3cios com facilidade.\u201d Se voc\u00ea quer sa\u00fade: \u201cEu sou um corpo saud\u00e1vel e cheio de energia.\u201d'))
    story.append(sp(4))
    story.append(TipBox(['Regra de ouro: fa\u00e7a TODO DIA, sem exce\u00e7\u00e3o.',
                         'A consist\u00eancia \u00e9 o que transforma afirma\u00e7\u00e3o em realidade.'],
                        color=PURPLE, bg=LLIGHT, label='O SEGREDO'))
    story.append(sp(3))
    story.append(TipBox([
        'Fique de frente para o espelho.',
        'Olhe nos seus pr\u00f3prios olhos.',
        'Fale em voz alta frases que come\u00e7am com EU SOU...',
        '2 minutos j\u00e1 bastam; o importante \u00e9 fazer todo dia.',
    ], color=PURPLE, bg=LLIGHT, label='RESUMO R\u00c1PIDO \u2014 ESPELHO'))

    # ── TÉCNICA 3: Visualização Emocional ────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(3, 'Visualiza\u00e7\u00e3o Emocional',
                               'Baseada na neuroci\u00eancia de Dr. Joe Dispenza', 'T\u00c9CNICA 03', TEAL, iw))
    story.append(sp(5))
    story.append(QuoteBox(
        'O campo qu\u00e2ntico n\u00e3o responde ao que voc\u00ea quer. Ele responde a quem voc\u00ea est\u00e1 sendo.',
        'Dr. Joe Dispenza, neurocientista', iw, TEAL, LTEAL))
    story.append(sp(4))

    story.append(bb('Por que funciona \u2014 pela neuroci\u00eancia'))
    story.append(AccentBar(iw, TEAL, 2))
    story.append(sp(3))
    story.append(b('O Dr. Joe Dispenza \u2014 neurocientista, pesquisador e autor best-seller \u2014 comprovou algo que transforma tudo: o seu c\u00e9rebro n\u00e3o sabe a diferen\u00e7a entre o que \u00e9 real e o que \u00e9 vividamente imaginado.'))
    story.append(b('Quando voc\u00ea visualiza algo com emo\u00e7\u00e3o intensa, seu c\u00e9rebro cria as mesmas conex\u00f5es neurais que criaria se aquilo j\u00e1 estivesse acontecendo de verdade. Voc\u00ea reprograma sua mente para uma nova realidade \u2014 antes mesmo de ela existir no mundo f\u00edsico.'))
    story.append(b('Segundo Dispenza, 95% dos seus pensamentos s\u00e3o subconscientes \u2014 ou seja, a vida que voc\u00ea tem hoje \u00e9 reflexo de cren\u00e7as que voc\u00ea nem escolheu. A boa not\u00edcia? Voc\u00ea pode reescrever esse c\u00f3digo. E a ferramenta \u00e9 a <b>emo\u00e7\u00e3o</b>. Sem emo\u00e7\u00e3o, n\u00e3o h\u00e1 reprograma\u00e7\u00e3o. Com emo\u00e7\u00e3o, o c\u00e9rebro entra no jogo e come\u00e7a a trabalhar a seu favor.'))
    story.append(sp(4))

    story.append(bb('Por que funciona \u2014 pela espiritualidade'))
    story.append(AccentBar(iw, TEAL, 2))
    story.append(sp(3))
    story.append(b('Em todas as tradi\u00e7\u00f5es m\u00edsticas, a visualiza\u00e7\u00e3o \u00e9 uma forma de ora\u00e7\u00e3o ativa. N\u00e3o \u00e9 pedir \u2014 \u00e9 ver, sentir e agir como se j\u00e1 fosse. Os antigos chamavam isso de f\u00e9 com obras: a cren\u00e7a que n\u00e3o espera pela prova para acreditar.'))
    story.append(b('Quando voc\u00ea visualiza com gratid\u00e3o, voc\u00ea est\u00e1 enviando ao campo energ\u00e9tico o sinal de quem j\u00e1 recebeu \u2014 e o universo responde a esse sinal. A f\u00edsica qu\u00e2ntica refor\u00e7a: tudo que existe come\u00e7a como potencial energ\u00e9tico antes de se tornar mat\u00e9ria. Sua visualiza\u00e7\u00e3o intensa \u00e9 literalmente o primeiro passo da cria\u00e7\u00e3o.'))
    story.append(sp(4))

    story.append(TipBox([
        'Antes de come\u00e7ar: coloque uma m\u00fasica de alta frequ\u00eancia.',
        'Sons em 528 Hz \u2014 a "frequ\u00eancia do milagre" \u2014 s\u00e3o ideais.',
        'Pesquise no YouTube/Spotify: "528 Hz manifesta\u00e7\u00e3o" ou "528 Hz Joe Dispenza".',
        'Use fones de ouvido para uma experi\u00eancia mais profunda.',
    ], color=TEAL, bg=LTEAL, label='\ud83c\udfb5 ANTES DE COME\u00c7AR'))

    story.append(sp(4))
    story.append(TipBox(['Fa\u00e7a de manh\u00e3, antes de pegar o celular.',
                         'Ou \u00e0 noite, antes de dormir.'],
                        color=GOLD, bg=LGOLD, label='IMPORTANTE'))
    story.append(sp(4))
    story.append(bb('Como fazer:'))
    story.append(AccentBar(iw, TEAL, 2))
    story.append(sp(3))

    steps3 = [
        ('1', 'Prepare o ambiente',
         'Sente-se confortavelmente, feche os olhos, respire fundo 3 vezes. Solte tudo o que o dia trouxe. (Coloque a m\u00fasica em 528 Hz antes, conforme a dica acima.)'),
        ('2', 'Entre no estado',
         'Foque s\u00f3 na sua respira\u00e7\u00e3o por 2 minutos. Sem pensar em mais nada. S\u00f3 respire. Esse foco ajuda o c\u00e9rebro a entrar em um estado mais receptivo.'),
        ('3', 'Visualize com todos os sentidos',
         'Imagine a vida que voc\u00ea quer. N\u00e3o como um filme distante. Como algo que j\u00e1 aconteceu. Onde voc\u00ea est\u00e1? O que est\u00e1 vestindo? Quem est\u00e1 do seu lado? O que sente no corpo?'),
        ('4', 'Sinta de verdade',
         'Essa \u00e9 a parte mais importante. Sinta gratid\u00e3o, alegria, paz, abund\u00e2ncia. Fique nesse estado por pelo menos 5 a 10 minutos.'),
        ('5', 'Declare e solte',
         'Antes de abrir os olhos, declare: \u201cIsso j\u00e1 \u00e9 meu. Eu j\u00e1 sou essa pessoa. Obrigada, universo.\u201d Depois solte. N\u00e3o force. Confie.'),
    ]
    for num, title, desc in steps3:
        story.append(step_row(num, title, desc, TEAL, iw))
        story.append(sp(2))

    story.append(sp(2))
    story.append(TipBox([
        'Como voc\u00ea se sente tendo isso?',
        'O que voc\u00ea est\u00e1 vestindo?',
        'Onde voc\u00ea est\u00e1?',
        'Quem est\u00e1 do seu lado?',
        'O que voc\u00ea est\u00e1 sentindo no corpo?',
    ], color=TEAL, bg=LTEAL, label='PERGUNTAS PARA A VISUALIZA\u00c7\u00c3O'))
    story.append(sp(4))

    story.append(RuleBox([
        'Coloque sempre a m\u00fasica em 528 Hz antes de come\u00e7ar',
        'Fa\u00e7a TODO DIA \u2014 a repeti\u00e7\u00e3o cria novos caminhos neurais',
        'Sempre SINTA \u2014 sem emo\u00e7\u00e3o n\u00e3o h\u00e1 reprograma\u00e7\u00e3o',
        'Seja espec\u00edfica \u2014 o c\u00e9rebro responde a detalhes',
        'Fa\u00e7a antes de dormir ou ao acordar \u2014 maior receptividade',
    ], iw, TEAL))
    story.append(sp(4))
    story.append(TipBox([
        'Ligar 528 Hz + sentar + respirar.',
        'Imaginar a cena com detalhes (roupa, lugar, pessoas).',
        'Sentir no corpo (gratid\u00e3o, alegria) por v\u00e1rios minutos.',
        'Fechar com uma frase de gratid\u00e3o e soltar.',
    ], color=TEAL, bg=LTEAL, label='RESUMO R\u00c1PIDO \u2014 VISUALIZA\u00c7\u00c3O'))

    story.append(sp(3))
    story.append(Paragraph('Baseado nas pesquisas e ensinamentos do Dr. Joe Dispenza, autor de <i>"Quebre o H\u00e1bito de Ser Voc\u00ea Mesmo"</i> e pesquisador de neuroplasticidade e consci\u00eancia.', SMALL))

    # ── PROTOCOLO SEMANAL ────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(sp(4))
    story.append(Paragraph('<b>PROTOCOLO SEMANAL</b>',
                           S('prot1', fontName='Helvetica-Bold', fontSize=20, leading=24,
                             textColor=TEXT, alignment=TA_LEFT, spaceAfter=4)))
    story.append(Paragraph('Como encaixar as 3 t\u00e9cnicas na sua rotina',
                           S('prot2', fontName='Helvetica-Bold', fontSize=12, leading=16,
                             textColor=MED, spaceAfter=8)))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(4))
    story.append(b('Voc\u00ea n\u00e3o precisa fazer tudo de uma vez. O segredo \u00e9 montar uma rotina <b>simples</b>, que caiba na sua vida, para repetir <b>todo dia</b> sem culpa e sem confus\u00e3o.'))
    story.append(sp(3))
    story.append(TipBox([
        'Este cap\u00edtulo tem 4 blocos: manh\u00e3 na cama, manh\u00e3 no banheiro, visualiza\u00e7\u00e3o (alguns dias) e noite.',
        'Depois vem uma TABELA de segunda a domingo \u2014 \u00e9 s\u00f3 copiar ou adaptar.',
        'Leia a LEGENDA antes da tabela: l\u00e1 cada palavra da tabela est\u00e1 explicada.',
    ], color=GOLD, bg=LGOLD, label='LEIA ANTES'))
    story.append(sp(5))

    story.append(bb('Bloco 1 \u2014 Ao acordar (ainda na cama, sem celular)'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('<b>O que fazer:</b> beber o restante da \u00e1gua que ficou no copo ao lado da cama (final da T\u00e9cnica da Ta\u00e7a, do dia anterior).'))
    story.append(b('<b>Por qu\u00ea:</b> os primeiros segundos do dia ainda s\u00e3o um momento em que o c\u00e9rebro costuma estar mais calmo e receptivo.'))
    story.append(b('<b>Se voc\u00ea usa a T\u00e9cnica 369</b> (explicada no b\u00f4nus): neste mesmo momento, <b>escreva a mesma afirma\u00e7\u00e3o 3 vezes</b> no caderno, antes de pegar o celular.'))
    story.append(sp(5))

    story.append(bb('Bloco 2 \u2014 No banheiro (cerca de 2 minutos)'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('<b>O que fazer:</b> na frente do espelho, olhando nos seus olhos, falar em voz alta suas frases <b>EU SOU</b> (T\u00e9cnica 02). Pode ser enquanto escova os dentes ou se arruma.'))
    story.append(b('<b>Importante:</b> n\u00e3o precisa ser longo. Precisa ser <b>presente</b> \u2014 n\u00e3o no autom\u00e1tico.'))
    story.append(sp(5))

    story.append(bb('Bloco 3 \u2014 Visualiza\u00e7\u00e3o (3 dias na semana, 10 a 15 minutos)'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('<b>O que fazer:</b> sentar com fones, m\u00fasica em 528 Hz, fechar os olhos e seguir o passo a passo da T\u00e9cnica 03 (sentir como se j\u00e1 fosse real).'))
    story.append(b('<b>Sugest\u00e3o de dias:</b> segunda, quarta e sexta. Se outro encaixe melhor na sua vida, troque \u2014 o importante \u00e9 manter os 3 dias por semana.'))
    story.append(sp(5))

    story.append(bb('Bloco 4 \u2014 \u00c0 noite, antes de dormir'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('<b>O que fazer (Ta\u00e7a):</b> copo com \u00e1gua, falar a inten\u00e7\u00e3o 3 vezes com a boca no copo, beber 3 goles, deixar o restante ao lado da cama.'))
    story.append(b('<b>Se usa 369:</b> antes de deitar, <b>escreva a mesma afirma\u00e7\u00e3o 9 vezes</b>. Feche com: \u201cObrigada, universo. Est\u00e1 feito.\u201d'))
    story.append(b('<b>Depois:</b> desligue a tela e v\u00e1 dormir pensando na sua inten\u00e7\u00e3o \u2014 sem ficar no celular.'))
    story.append(sp(5))

    story.append(bb('Exemplo de como fica a semana na pr\u00e1tica'))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(3))
    story.append(TipBox([
        '\u00c1gua (manh\u00e3) = beber o que sobrou no copo da noite.',
        'Espelho = frases EU SOU no espelho.',
        'Visualiza\u00e7\u00e3o = sess\u00e3o com 528 Hz (T\u00e9cnica 03).',
        '369 (6x) = \u00e0 TARDE, escrever a MESMA afirma\u00e7\u00e3o 6 vezes no papel.',
        '\u00c1gua (ta\u00e7a) = \u00e0 NOITE, fazer a Ta\u00e7a completa (falar 3x, 3 goles, copo ao lado).',
        '369 (9x) = na NOITE, depois da ta\u00e7a (ou na sequ\u00eancia), escrever 9 vezes a afirma\u00e7\u00e3o.',
        '\u2014 = neste hor\u00e1rio n\u00e3o h\u00e1 369 nem visualiza\u00e7\u00e3o na sugest\u00e3o (fins de semana).',
    ], color=BLANCH_MAROON, bg=LGOLD, label='LEGENDA \u2014 LEIA PRIMEIRO'))
    story.append(sp(4))
    story.append(Paragraph(
        'A tabela abaixo \u00e9 um <b>modelo</b>. Segunda a sexta inclui 369; s\u00e1bado e domingo s\u00e3o mais leves para voc\u00ea descansar da escrita intensa.',
        S('week_leg', fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT,
          alignment=TA_JUSTIFY, spaceAfter=8)))
    _wc = S('wcell', fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=TEXT, alignment=TA_LEFT)
    _wh = S('whead', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=WHITE, alignment=TA_CENTER)
    w = iw
    cw_dia = 24 * mm
    cw_rest = w - cw_dia
    cw_m = cw_rest * 0.34
    cw_t = cw_rest * 0.22
    cw_n = cw_rest - cw_m - cw_t
    week_rows = [
        [
            Paragraph('<b>Dia</b>', _wh),
            Paragraph('<b>Manh\u00e3</b><br/><i><font size="7">(ordem sugerida)</font></i>', _wh),
            Paragraph('<b>Tarde</b><br/><i><font size="7">(369)</font></i>', _wh),
            Paragraph('<b>Noite</b><br/><i><font size="7">(ta\u00e7a + 369)</font></i>', _wh),
        ],
        [
            Paragraph('<b>Segunda</b>', _wc),
            Paragraph('1) Beber \u00e1gua do copo<br/>2) EU SOU no espelho<br/>3) Visualiza\u00e7\u00e3o 528 Hz', _wc),
            Paragraph('Escrever a frase<br/><b>6 vezes</b>', _wc),
            Paragraph('1) Ta\u00e7a (falar 3x, 3 goles)<br/>2) Escrever a frase <b>9 vezes</b>', _wc),
        ],
        [
            Paragraph('<b>Ter\u00e7a</b>', _wc),
            Paragraph('1) Beber \u00e1gua do copo<br/>2) EU SOU no espelho<br/><i>(sem visualiza\u00e7\u00e3o)</i>', _wc),
            Paragraph('Escrever a frase<br/><b>6 vezes</b>', _wc),
            Paragraph('1) Ta\u00e7a<br/>2) Escrever <b>9 vezes</b>', _wc),
        ],
        [
            Paragraph('<b>Quarta</b>', _wc),
            Paragraph('1) Beber \u00e1gua do copo<br/>2) EU SOU<br/>3) Visualiza\u00e7\u00e3o 528 Hz', _wc),
            Paragraph('Escrever a frase<br/><b>6 vezes</b>', _wc),
            Paragraph('1) Ta\u00e7a<br/>2) Escrever <b>9 vezes</b>', _wc),
        ],
        [
            Paragraph('<b>Quinta</b>', _wc),
            Paragraph('1) Beber \u00e1gua do copo<br/>2) EU SOU<br/><i>(sem visualiza\u00e7\u00e3o)</i>', _wc),
            Paragraph('Escrever a frase<br/><b>6 vezes</b>', _wc),
            Paragraph('1) Ta\u00e7a<br/>2) Escrever <b>9 vezes</b>', _wc),
        ],
        [
            Paragraph('<b>Sexta</b>', _wc),
            Paragraph('1) Beber \u00e1gua do copo<br/>2) EU SOU<br/>3) Visualiza\u00e7\u00e3o 528 Hz', _wc),
            Paragraph('Escrever a frase<br/><b>6 vezes</b>', _wc),
            Paragraph('1) Ta\u00e7a<br/>2) Escrever <b>9 vezes</b>', _wc),
        ],
        [
            Paragraph('<b>S\u00e1bado</b>', _wc),
            Paragraph('1) Beber \u00e1gua do copo<br/>2) EU SOU<br/><i>(descanso da 369 e da visualiza\u00e7\u00e3o)</i>', _wc),
            Paragraph('<b>\u2014</b><br/><i>sem escrita 369</i>', _wc),
            Paragraph('S\u00f3 a <b>ta\u00e7a</b><br/><i>(sem 9x)</i>', _wc),
        ],
        [
            Paragraph('<b>Domingo</b>', _wc),
            Paragraph('1) Beber \u00e1gua do copo<br/>2) EU SOU', _wc),
            Paragraph('<b>\u2014</b>', _wc),
            Paragraph('Ta\u00e7a + revisar a<br/><b>inten\u00e7\u00e3o da semana</b><br/><i>(mentalizar o que deseja na semana seguinte)</i>', _wc),
        ],
    ]
    week_tbl = Table(week_rows, colWidths=[cw_dia, cw_m, cw_t, cw_n], repeatRows=1)
    week_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLANCH_MAROON),
        ('BACKGROUND', (0, 1), (-1, -1), LLIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LLIGHT, colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, LAV),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(week_tbl)
    story.append(sp(3))
    story.append(Paragraph(
        '<b>Fim de semana:</b> a ideia \u00e9 <b>aliviar</b>: voc\u00ea mant\u00e9m o b\u00e1sico (\u00e1gua da manh\u00e3, EU SOU, ta\u00e7a \u00e0 noite) e <b>n\u00e3o</b> precisa da escrita 369 nem da visualiza\u00e7\u00e3o longa, se n\u00e3o quiser.<br/><br/>'
        '<b>Domingo \u00e0 noite:</b> al\u00e9m da ta\u00e7a, reserve um minuto para lembrar <b>o que voc\u00ea quer para a semana que come\u00e7a</b> \u2014 em uma frase, com calma.',
        S('week_note', fontName='Helvetica', fontSize=9, leading=13,
          textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=10)))
    story.append(sp(3))

    story.append(bb('Quanto tempo isso leva?'))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(2))
    story.append(b('Em m\u00e9dia, entre <b>10 e 20 minutos por dia</b>. Nos dias em que tem visualiza\u00e7\u00e3o, pode passar um pouco disso \u2014 tudo bem.'))
    story.append(sp(3))
    story.append(b('N\u00e3o \u00e9 sobre ter o dia livre. \u00c9 sobre <b>escolher</b>, todos os dias, alguns minutos s\u00f3 para voc\u00ea. Isso \u00e9 o mais poderoso: se colocar em primeiro lugar, mesmo com a vida corrida.'))
    story.append(sp(5))

    story.append(TipBox([
        'Ningu\u00e9m \u00e9 perfeita. Esqueceu a \u00e1gua? Fa\u00e7a pelo menos o espelho.',
        'Sem energia para visualizar? Fa\u00e7a s\u00f3 a parte escrita da 369 ou s\u00f3 a ta\u00e7a.',
        'O pior \u00e9 parar 100%. O melhor \u00e9 fazer um pouquinho todo dia.',
        '5 minutos todos os dias vencem 1 hora s\u00f3 no domingo.',
        'A consist\u00eancia \u00e9 a sua maior ferramenta.',
    ], color=MED, bg=LLIGHT, label='SE FICAR DIF\u00cdCIL'))

    # ── BÔNUS ────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    # Header especial bônus
    tbl_bonus = Table(
        [[Paragraph('\u2605  B\u00d4NUS  \u2605', S('bh', fontName='Helvetica-Bold', fontSize=11,
                                                    textColor=TEXT, alignment=TA_CENTER)),
          Paragraph('Pr\u00e1tica de Manifesta\u00e7\u00e3o Poderosa',
                    S('bt2', fontName='Helvetica-Bold', fontSize=18, leading=22,
                      textColor=WHITE, alignment=TA_LEFT))]],
        colWidths=[28 * mm, iw - 28 * mm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), GOLD),
            ('BACKGROUND', (1, 0), (1, 0), BLANCH_MAROON),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
            ('LEFTPADDING', (1, 0), (1, 0), 12),
        ])
    )
    story.append(tbl_bonus)
    story.append(sp(5))
    story.append(b('Esta pr\u00e1tica une escrita, visualiza\u00e7\u00e3o e inten\u00e7\u00e3o energ\u00e9tica. Recomendo realiz\u00e1-la na <b>Lua Nova</b> (para semear) ou na <b>Lua Cheia</b> (para amplificar).'))
    story.append(sp(3))

    # T\u00e9cnica 369 Lunar
    story.append(bb('\u2728 T\u00e9cnica 369 Lunar'))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(3))
    story.append(b('Inspirada na numerologia sagrada e na sabedoria de Nikola Tesla, a t\u00e9cnica 369 usa a repeti\u00e7\u00e3o como forma de programar o subconsciente.'))
    story.append(sp(3))
    story.append(TipBox([
        'Voc\u00ea escolhe UMA \u00fanica frase (afirma\u00e7\u00e3o) e repete ela no papel.',
        '3 = escrever 3 vezes de manh\u00e3 (antes do celular).',
        '6 = escrever 6 vezes \u00e0 tarde (sempre a mesma frase).',
        '9 = escrever 9 vezes \u00e0 noite (mesma frase), antes de dormir.',
        'Sempre a MESMA frase nos tr\u00eas hor\u00e1rios \u2014 isso cria o h\u00e1bito no c\u00e9rebro.',
    ], color=GOLD, bg=LGOLD, label='369 EM UMA FRASE'))

    lunar_steps = [
        ('3', 'MANH\u00c3', GOLD, LGOLD,
         'Ao acordar, antes de olhar o celular, escreva sua afirma\u00e7\u00e3o de desejo 3 vezes.',
         'Eu sou magn\u00e9tica e atraio oportunidades abundantes com facilidade.'),
        ('6', 'TARDE', MED, LLIGHT,
         'No meio do dia, escreva a mesma afirma\u00e7\u00e3o 6 vezes. Sinta cada palavra. Escreva com presen\u00e7a.',
         None),
        ('9', 'NOITE', ROSE, SROSE,
         'Antes de dormir, escreva 9 vezes. Encerre com gratid\u00e3o.',
         'Obrigada, universo. Est\u00e1 feito.'),
    ]
    for num, label, col, bg, desc, example in lunar_steps:
        row = Table(
            [[Paragraph(f'<b>{num}</b>', S(f'ln{num}', fontName='Helvetica-Bold', fontSize=32,
                                           leading=36, textColor=WHITE, alignment=TA_CENTER)),
              [Paragraph(f'<b>{label}</b>', S('ll', fontName='Helvetica-Bold', fontSize=10,
                                              leading=13, textColor=col, spaceAfter=2)),
               Paragraph(desc, BODYL),
               (Paragraph(f'\u201c{example}\u201d', AFF) if example else Spacer(1, 1))]]],
            colWidths=[20 * mm, iw - 20 * mm],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), col),
                ('BACKGROUND', (1, 0), (1, 0), bg),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (1, 0), (1, 0), 8),
            ])
        )
        story.append(row)
        story.append(sp(2))

    story.append(sp(3))
    story.append(TipBox(['Pratique por 33 dias consecutivos, alinhando com o ciclo lunar.',
                         'Se pular um dia, n\u00e3o se puna \u2014 recomece com mais inten\u00e7\u00e3o.',
                         'A consist\u00eancia \u00e9 a magia.'],
                        color=GOLD, bg=LGOLD, label='POR QUANTOS DIAS?'))

    # Perfume Energ\u00e9tico
    story.append(PageBreak())
    story.append(bb('\ud83c\udf19 Passo a Passo do Perfume Energ\u00e9tico'))
    story.append(AccentBar(iw, PURPLE, 2))
    story.append(sp(4))

    story.append(bb('O que voc\u00ea vai precisar:'))
    materiais = [
        'Perfume virgem (nunca usado)',
        'Moeda dourada',
        'L\u00e1pis ou lapiseira',
        'Papel',
        'Sal',
    ]
    for m in materiais:
        story.append(bul(m))
    story.append(sp(3))

    story.append(TipBox([
        'O l\u00e1pis e a lapiseira s\u00e3o feitos de grafite \u2014 um mineral natural da terra.',
        'Escrever com grafite \u00e9 usar a energia da pr\u00f3pria natureza para registrar sua inten\u00e7\u00e3o.',
        'A caneta usa tinta qu\u00edmica que cria uma barreira com os elementos naturais.',
        'Terra + pensamento + palavra = canal muito mais poderoso para a inten\u00e7\u00e3o.',
    ], color=PURPLE, bg=LLIGHT, label='POR QUE USAR L\u00c1PIS?'))
    story.append(sp(4))

    perf_steps = [
        ('1', 'Escreva no papel',
         '"Assim como a Lua cresce no c\u00e9u, cresce meu brilho, cresce meu dinheiro, cresce minha felicidade..." \u2014 coloque o que voc\u00ea quiser.'),
        ('2', 'Dobre o papel',
         'Quando terminar de escrever, dobre o papel 3x virando para voc\u00ea.'),
        ('3', 'Limpe com sal',
         'Pegue o sal e passe ao redor do perfume pedindo que qualquer energia anterior seja neutralizada.'),
        ('4', 'Ative na luz do luar',
         'V\u00e1 para o quintal, janela ou ao ar livre. Passe a moeda ao redor do perfume dizendo: "Eu consagro este perfume \u00e0 energia da Lua Crescente. Que ele carregue prosperidade, fortuna e sorte para quem o usa."'),
        ('5', 'Monte o altar',
         'Coloque a moeda em cima do papel (com o n\u00famero virado pra cima). Depois coloque o perfume em cima e deixe a noite toda na luz do luar.'),
        ('6', 'Na manh\u00e3 seguinte',
         'Pegue o perfume e use normalmente \u2014 nas roupas, sapatos, cama, sof\u00e1... Ao passar, diga: "Eu ativo a energia da lua crescente para que eu tenha muito sucesso, prosperidade, fartura, fortuna, sa\u00fade..."'),
    ]
    for num, title, desc in perf_steps:
        story.append(step_row(num, title, desc, PURPLE, iw))
        story.append(sp(2))

    # P\u00e1gina final
    story.append(PageBreak())
    story.append(sp(20))
    story.append(AccentBar(iw, GOLD))
    story.append(sp(8))
    story.append(Paragraph('\u2728', S('st', fontName='Helvetica-Bold', fontSize=42,
                                        textColor=GOLD, alignment=TA_CENTER, spaceAfter=6)))
    story.append(Paragraph('Voc\u00ea agora tem nas m\u00e3os', CLOSING))
    story.append(Paragraph('Um guia leve para destravar sua energia \u2014 dia ap\u00f3s dia.', CLOSING))
    story.append(Paragraph('Use as t\u00e9cnicas todos os dias.',
                            S('cl2', fontName='Helvetica-Bold', fontSize=15, leading=22,
                              textColor=BLANCH_MAROON, alignment=TA_CENTER, spaceAfter=10)))
    story.append(sp(5))
    story.append(b('O universo responde \u00e0 consist\u00eancia. N\u00e3o \u00e0 perfeic\u00e3o. N\u00e3o ao talento. N\u00e3o \u00e0 sorte. \u00c0 pr\u00e1tica di\u00e1ria, \u00e0 inten\u00e7\u00e3o renovada todos os dias, ao ato de escolher acreditar mesmo antes de ver.'))
    story.append(sp(4))
    story.append(Paragraph('<b>Comece hoje. Agora. Com o que voc\u00ea tem.</b>',
                           S('begin', fontName='Helvetica-Bold', fontSize=13, leading=18,
                             textColor=TEXT, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph('A vida que voc\u00ea sonha est\u00e1 esperando pela sua inten\u00e7\u00e3o.',
                           S('wait', fontName='Helvetica-Oblique', fontSize=12, leading=18,
                             textColor=GRAY, alignment=TA_CENTER)))
    story.append(sp(10))
    story.append(AccentBar(iw, GOLD))

    return story


# ── Build PDF ─────────────────────────────────────────────────────────────────
def build_pdf(output='Destrave_Sua_Energia_ebook.pdf'):
    doc = BaseDocTemplate(
        output, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    inner_frame = Frame(LM, BM, IW, H - TM - BM, id='inner')

    def cover_bg(canvas, doc):
        canvas.saveState()
        draw_cover_blanch(canvas)
        canvas.restoreState()

    def manifest_bg(canvas, doc):
        canvas.saveState()
        draw_consistencia_page(canvas)
        canvas.restoreState()

    def inner_bg(canvas, doc):
        canvas.saveState()
        draw_inner(canvas)
        canvas.restoreState()

    manifest_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                           topPadding=0, bottomPadding=0, id='manifest')
    cover_tpl = PageTemplate(id='cover', frames=[cover_frame], onPage=cover_bg)
    manifest_tpl = PageTemplate(id='manifest', frames=[manifest_frame], onPage=manifest_bg)
    inner_tpl = PageTemplate(id='inner', frames=[inner_frame], onPage=inner_bg)
    doc.addPageTemplates([cover_tpl, manifest_tpl, inner_tpl])

    story = build_content(IW)
    doc.build(story)
    print(f'PDF gerado: {output}')


if __name__ == '__main__':
    build_pdf()
