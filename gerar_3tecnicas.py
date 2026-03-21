# -*- coding: utf-8 -*-
"""Gerador do Ebook: 3 Tecnicas de Manifestacao"""
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

W, H = A4
LM = RM = 20 * mm
TM = 22 * mm
BM = 20 * mm
IW = W - LM - RM

# ── Paleta ─────────────────────────────────────────────────────────────────
DEEP    = colors.HexColor('#1E0A3C')
PURPLE  = colors.HexColor('#5B2D8E')
MED     = colors.HexColor('#7B4DB5')
LAV     = colors.HexColor('#EDE0FF')
LLIGHT  = colors.HexColor('#F7F0FF')
GOLD    = colors.HexColor('#C9963B')
LGOLD   = colors.HexColor('#FFF8E7')
ROSE    = colors.HexColor('#A63D72')
SROSE   = colors.HexColor('#FCE8F3')
TEAL    = colors.HexColor('#1A7A6E')
LTEAL   = colors.HexColor('#E0F5F2')
CREAM   = colors.HexColor('#FFFEF9')
TEXT    = colors.HexColor('#1A1A2E')
GRAY    = colors.HexColor('#7A7A9A')
WHITE   = colors.white

TECH_COLORS = [ROSE, PURPLE, TEAL]
TECH_BG     = [SROSE, LLIGHT, LTEAL]

def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY    = S('body',   fontName='Helvetica', fontSize=10.5, leading=17, textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=8)
BODYL   = S('bodyl',  fontName='Helvetica', fontSize=10.5, leading=17, textColor=TEXT, alignment=TA_LEFT, spaceAfter=6)
BOLDB   = S('boldb',  fontName='Helvetica-Bold', fontSize=10.5, leading=17, textColor=TEXT, spaceAfter=6)
BULLET  = S('bul',    fontName='Helvetica', fontSize=10.5, leading=16, textColor=TEXT, leftIndent=16, firstLineIndent=-10, spaceAfter=5)
QUOTE   = S('quote',  fontName='Helvetica-Oblique', fontSize=11.5, leading=18, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=6)
STEP_T  = S('stept',  fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=DEEP, spaceAfter=3)
GOLD_T  = S('goldt',  fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=GOLD, spaceAfter=3)
AFF     = S('aff',    fontName='Helvetica-Oblique', fontSize=11, leading=17, textColor=DEEP, spaceAfter=5)
TOC_T   = S('toct',   fontName='Helvetica-Bold', fontSize=13, leading=18, textColor=DEEP, spaceAfter=3)
TOC_D   = S('tocd',   fontName='Helvetica', fontSize=10, leading=14, textColor=GRAY, spaceAfter=2)
SMALL   = S('small',  fontName='Helvetica', fontSize=9, leading=13, textColor=GRAY, spaceAfter=4)
CLOSING = S('cl',     fontName='Helvetica-Oblique', fontSize=14, leading=22, textColor=DEEP, alignment=TA_CENTER, spaceAfter=8)


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
        # Fundo
        c.setFillColor(self.color)
        c.roundRect(0, 0, iw, h, 4 * mm, fill=1, stroke=0)
        # Numero fantasma
        c.setFillColor(WHITE)
        c.setFillAlpha(0.07)
        c.setFont('Helvetica-Bold', 90)
        c.drawRightString(iw - 6 * mm, 0 * mm, str(self.num))
        c.setFillAlpha(1.0)
        # Badge
        c.setFillColor(GOLD)
        c.roundRect(8 * mm, h - 14 * mm, 32 * mm, 8 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillColor(DEEP)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(10 * mm, h - 14 * mm + 2.5 * mm, self.badge)
        # Titulo
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 20)
        c.drawString(8 * mm, h - 26 * mm, self.title)
        # Subtitulo
        c.setFillColor(WHITE)
        c.setFillAlpha(0.75)
        c.setFont('Helvetica-Oblique', 11)
        c.drawString(8 * mm, h - 33 * mm, self.subtitle)
        c.setFillAlpha(1.0)


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

def draw_cover(c):
    c.setFillColor(DEEP)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Circulo decorativo no canto superior direito — longe do texto
    cx, cy = W * 0.82, H * 0.80
    for r, alpha in [(75, 0.05), (58, 0.08), (42, 0.12)]:
        c.setFillColor(GOLD)
        c.setFillAlpha(alpha)
        c.circle(cx, cy, r * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)
    c.setFillColor(GOLD)
    c.setFillAlpha(0.85)
    c.circle(cx, cy, 7 * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)
    # Faixas ouro topo/base
    c.setFillColor(GOLD)
    c.rect(0, H - 8 * mm, W, 4 * mm, fill=1, stroke=0)
    c.rect(0, 8 * mm, W, 4 * mm, fill=1, stroke=0)
    # Badge topo
    bw = 72 * mm
    c.setFillColor(ROSE)
    c.roundRect((W - bw) / 2, H - 28 * mm, bw, 9 * mm, 4 * mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, H - 28 * mm + 3 * mm, 'T\u00c9CNICAS DE MANIFESTA\u00c7\u00c3O')
    # Titulo principal
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 52)
    c.drawCentredString(W / 2, H * 0.74, '3 T\u00c9CNICAS')
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 36)
    c.drawCentredString(W / 2, H * 0.66, 'DE MANIFESTA\u00c7\u00c3O')
    # Separador
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(LM + 10 * mm, H * 0.62, W - LM - 10 * mm, H * 0.62)
    # Lista de tecnicas — alinhada à esquerda com badge colorido
    tecnicas = [
        ('T\u00c9CNICA 01', 'Ta\u00e7a de \u00c1gua', ROSE),
        ('T\u00c9CNICA 02', 'Espelho \u2014 EU SOU', MED),
        ('T\u00c9CNICA 03', 'Visualiza\u00e7\u00e3o \u2014 Dr. Joe Dispenza', TEAL),
    ]
    y = H * 0.575
    for label, name, col in tecnicas:
        c.setFillColor(col)
        c.roundRect(LM + 5 * mm, y - 2.5 * mm, 24 * mm, 6.5 * mm, 2.5 * mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawString(LM + 6.5 * mm, y + 0.5 * mm, label)
        c.setFillColor(WHITE)
        c.setFillAlpha(0.9)
        c.setFont('Helvetica', 12)
        c.drawString(LM + 32 * mm, y + 0.5 * mm, name)
        c.setFillAlpha(1.0)
        y -= 12 * mm
    # Bonus badge
    c.setFillColor(PURPLE)
    c.setFillAlpha(0.9)
    bw2 = 68 * mm
    c.roundRect(LM + 5 * mm, y - 2 * mm, bw2, 8 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(LM + 8 * mm, y + 1.5 * mm, '\u2605  B\u00d4NUS: Pr\u00e1tica da Lua Nova')
    # Rodape
    c.setFillColor(WHITE)
    c.setFillAlpha(0.5)
    c.setFont('Helvetica', 9)
    c.drawCentredString(W / 2, 16 * mm, 'Transforme inten\u00e7\u00e3o em realidade')
    c.setFillAlpha(1.0)


def draw_inner(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(LAV)
    c.rect(0, 0, 3 * mm, H, fill=1, stroke=0)
    c.setFillColor(DEEP)
    c.rect(0, H - TM, W, TM, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(LM, H - TM + 7 * mm, '3 T\u00c9CNICAS DE MANIFESTA\u00c7\u00c3O')
    c.setFillColor(WHITE)
    c.setFillAlpha(0.65)
    c.setFont('Helvetica', 8)
    c.drawRightString(W - RM, H - TM + 7 * mm, 'Pr\u00e1ticas Poderosas para Co-Criar sua Realidade')
    c.setFillAlpha(1.0)
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

def build_content(iw):
    story = []
    story.append(NextPageTemplate('inner'))
    story.append(PageBreak())

    # ── Sumário ──────────────────────────────────────────────────────────────
    story.append(sp(8))
    story.append(Paragraph('<b>S U M \u00c1 R I O</b>',
                           S('toch', fontName='Helvetica-Bold', fontSize=28, leading=34,
                             textColor=DEEP, alignment=TA_LEFT, spaceAfter=6)))
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

    # ── Introdução ───────────────────────────────────────────────────────────
    story.append(sp(8))
    story.append(Paragraph('<b>3 T\u00c9CNICAS DE MANIFESTA\u00c7\u00c3O</b>',
                           S('introtitle', fontName='Helvetica-Bold', fontSize=22, leading=28,
                             textColor=DEEP, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph('Transforme inten\u00e7\u00e3o em realidade',
                           S('introsub', fontName='Helvetica-Oblique', fontSize=13, leading=18,
                             textColor=PURPLE, alignment=TA_CENTER, spaceAfter=10)))
    story.append(AccentBar(iw, ROSE, 2))
    story.append(sp(3))
    story.append(b('Voc\u00ea est\u00e1 prestes a aprender tr\u00eas das pr\u00e1ticas mais poderosas de manifesta\u00e7\u00e3o \u2014 simples, acess\u00edveis e com resultados comprovados por quem pratica com consist\u00eancia.'))
    story.append(b('N\u00e3o \u00e9 misticismo vazio. \u00c9 a uni\u00e3o entre inten\u00e7\u00e3o energ\u00e9tica, neuroci\u00eancia e espiritualidade pr\u00e1tica. Cada t\u00e9cnica foi escolhida por ser f\u00e1cil de incorporar \u00e0 rotina \u2014 e por gerar resultados reais.'))
    story.append(TipBox(['O segredo de toda pr\u00e1tica de manifesta\u00e7\u00e3o \u00e9 um s\u00f3: CONSIST\u00caNCIA.',
                         'Fa\u00e7a todos os dias. Sem exce\u00e7\u00e3o. A repeti\u00e7\u00e3o \u00e9 o que transforma inten\u00e7\u00e3o em realidade.'],
                        label='LEMBRE SEMPRE'))

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
                                             leading=16, textColor=DEEP))] for a in affirmations_general]
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

    story.append(sp(3))
    story.append(Paragraph('Baseado nas pesquisas e ensinamentos do Dr. Joe Dispenza, autor de <i>"Quebre o H\u00e1bito de Ser Voc\u00ea Mesmo"</i> e pesquisador de neuroplasticidade e consci\u00eancia.', SMALL))

    # ── PROTOCOLO SEMANAL ────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(sp(4))
    story.append(Paragraph('<b>PROTOCOLO SEMANAL</b>',
                           S('prot1', fontName='Helvetica-Bold', fontSize=20, leading=24,
                             textColor=DEEP, alignment=TA_LEFT, spaceAfter=4)))
    story.append(Paragraph('Como encaixar as 3 t\u00e9cnicas na sua rotina',
                           S('prot2', fontName='Helvetica-Bold', fontSize=12, leading=16,
                             textColor=MED, spaceAfter=8)))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(4))
    story.append(b('Voc\u00ea n\u00e3o precisa fazer tudo de uma vez. O segredo \u00e9 criar uma rotina que caiba na sua vida \u2014 e que voc\u00ea consiga manter todos os dias, sem se sobrecarregar.'))
    story.append(sp(5))

    story.append(bb('Toda manh\u00e3 \u2014 antes de pegar o celular'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('Acorde. Antes de olhar qualquer notifica\u00e7\u00e3o, beba o restante da \u00e1gua que deixou ao seu lado na noite anterior (T\u00e9cnica da Ta\u00e7a). Esses primeiros segundos do dia s\u00e3o poderosos \u2014 seu c\u00e9rebro ainda est\u00e1 em estado Alfa, receptivo e aberto. Aproveite.'))
    story.append(b('Se voc\u00ea estiver aplicando a <b>T\u00e9cnica 369</b> (passo a passo completo no b\u00f4nus deste ebook), escreva sua afirma\u00e7\u00e3o 3 vezes agora.'))
    story.append(sp(5))

    story.append(bb('Toda manh\u00e3 \u2014 no banheiro'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('Na frente do espelho, enquanto escova os dentes ou se arruma, olhe nos seus pr\u00f3prios olhos e declare suas afirma\u00e7\u00f5es <b>EU SOU</b> em voz alta. N\u00e3o precisa de mais do que 2 minutos. Mas fa\u00e7a com presen\u00e7a \u2014 n\u00e3o no autom\u00e1tico.'))
    story.append(sp(5))

    story.append(bb('3x por semana \u2014 manh\u00e3 ou noite'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('Separe de 10 a 15 minutos para a visualiza\u00e7\u00e3o emocional. Coloque sua m\u00fasica em 528 Hz, feche os olhos e sinta a vida que voc\u00ea est\u00e1 criando. Sugerimos segunda, quarta e sexta \u2014 mas escolha os dias que funcionam melhor para voc\u00ea.'))
    story.append(sp(5))

    story.append(bb('Toda noite \u2014 antes de dormir'))
    story.append(AccentBar(iw, MED, 2))
    story.append(sp(2))
    story.append(b('Pegue seu copo de \u00e1gua. Fale sua inten\u00e7\u00e3o 3 vezes, beba 3 goles, deixe ao seu lado (T\u00e9cnica da Ta\u00e7a). Se estiver na T\u00e9cnica 369, escreva sua afirma\u00e7\u00e3o 9 vezes antes de deitar. Encerre com: \u201cObrigada, universo. Est\u00e1 feito.\u201d'))
    story.append(b('Desligue a tela. Durma com a inten\u00e7\u00e3o.'))
    story.append(sp(5))

    story.append(bb('Exemplo de como fica a semana na pr\u00e1tica'))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(3))
    story.append(Paragraph(
        'Use esta tabela como <b>modelo</b> (segunda a domingo). '
        '<b>\u00c1gua</b> de manh\u00e3 = beber o restante do copo da noite anterior; '
        '<b>Espelho</b> = afirma\u00e7\u00f5es EU SOU; '
        '<b>Visualiza\u00e7\u00e3o</b> = pr\u00e1tica com 528 Hz; '
        '<b>369</b> = t\u00e9cnica do b\u00f4nus (3x manh\u00e3, 6x tarde, 9x noite).',
        S('week_leg', fontName='Helvetica', fontSize=9, leading=13, textColor=TEXT,
          alignment=TA_JUSTIFY, spaceAfter=8)))
    _wc = S('wcell', fontName='Helvetica', fontSize=8, leading=11, textColor=TEXT, alignment=TA_LEFT)
    _wh = S('whead', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=WHITE, alignment=TA_CENTER)
    w = iw
    cw_dia = 22 * mm
    cw_rest = w - cw_dia
    cw_m = cw_rest * 0.36
    cw_t = cw_rest * 0.26
    cw_n = cw_rest - cw_m - cw_t
    week_rows = [
        [
            Paragraph('<b>Dia</b>', _wh),
            Paragraph('<b>Manh\u00e3</b>', _wh),
            Paragraph('<b>Tarde</b>', _wh),
            Paragraph('<b>Noite</b>', _wh),
        ],
        [
            Paragraph('<b>Segunda</b>', _wc),
            Paragraph('\u00c1gua + Espelho + Visualiza\u00e7\u00e3o', _wc),
            Paragraph('369 (6x)', _wc),
            Paragraph('\u00c1gua (ta\u00e7a) + 369 (9x)', _wc),
        ],
        [
            Paragraph('<b>Ter\u00e7a</b>', _wc),
            Paragraph('\u00c1gua + Espelho', _wc),
            Paragraph('369 (6x)', _wc),
            Paragraph('\u00c1gua (ta\u00e7a) + 369 (9x)', _wc),
        ],
        [
            Paragraph('<b>Quarta</b>', _wc),
            Paragraph('\u00c1gua + Espelho + Visualiza\u00e7\u00e3o', _wc),
            Paragraph('369 (6x)', _wc),
            Paragraph('\u00c1gua (ta\u00e7a) + 369 (9x)', _wc),
        ],
        [
            Paragraph('<b>Quinta</b>', _wc),
            Paragraph('\u00c1gua + Espelho', _wc),
            Paragraph('369 (6x)', _wc),
            Paragraph('\u00c1gua (ta\u00e7a) + 369 (9x)', _wc),
        ],
        [
            Paragraph('<b>Sexta</b>', _wc),
            Paragraph('\u00c1gua + Espelho + Visualiza\u00e7\u00e3o', _wc),
            Paragraph('369 (6x)', _wc),
            Paragraph('\u00c1gua (ta\u00e7a) + 369 (9x)', _wc),
        ],
        [
            Paragraph('<b>S\u00e1bado</b>', _wc),
            Paragraph('\u00c1gua + Espelho', _wc),
            Paragraph('\u2014', _wc),
            Paragraph('\u00c1gua (ta\u00e7a)', _wc),
        ],
        [
            Paragraph('<b>Domingo</b>', _wc),
            Paragraph('\u00c1gua + Espelho', _wc),
            Paragraph('\u2014', _wc),
            Paragraph('\u00c1gua (ta\u00e7a) + inten\u00e7\u00e3o da semana', _wc),
        ],
    ]
    week_tbl = Table(week_rows, colWidths=[cw_dia, cw_m, cw_t, cw_n], repeatRows=1)
    week_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP),
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
        '<i>Nos fins de semana, pausa na 369 e na visualiza\u00e7\u00e3o guiada \u2014 '
        'mantenha \u00e1gua + espelho e a ta\u00e7a \u00e0 noite. No domingo \u00e0 noite, '
        'reforce a inten\u00e7\u00e3o geral da semana que vem.</i>',
        S('week_note', fontName='Helvetica-Oblique', fontSize=8.5, leading=12,
          textColor=GRAY, alignment=TA_JUSTIFY, spaceAfter=10)))
    story.append(sp(3))

    story.append(bb('Tempo total por dia'))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(2))
    story.append(b('Entre <b>10 e 20 minutos</b>, dependendo do dia (nos dias de visualiza\u00e7\u00e3o, um pouco mais).'))
    story.append(sp(3))
    story.append(b('N\u00e3o \u00e9 sobre ter horas livres. \u00c9 sobre escolher, todos os dias, dedicar alguns minutos para si mesma. Essa \u00e9 a pr\u00e1tica mais poderosa de todas: a de se colocar em primeiro lugar.'))
    story.append(sp(5))

    story.append(TipBox([
        'N\u00e3o tente ser perfeita. Se um dia voc\u00ea esquecer a \u00e1gua, fa\u00e7a o espelho.',
        'Se n\u00e3o tiver energia para a visualiza\u00e7\u00e3o, fa\u00e7a s\u00f3 a 369 (se estiver no b\u00f4nus) ou o m\u00ednimo poss\u00edvel.',
        'O que n\u00e3o pode \u00e9 parar completamente.',
        'Uma pr\u00e1tica pequena feita todos os dias vale muito mais que uma pr\u00e1tica intensa feita uma vez por semana.',
        'A consist\u00eancia \u00e9 a sua maior ferramenta.',
    ], color=MED, bg=LLIGHT, label='UMA DICA IMPORTANTE'))

    # ── BÔNUS ────────────────────────────────────────────────────────────────
    story.append(PageBreak())
    # Header especial bônus
    tbl_bonus = Table(
        [[Paragraph('\u2605  B\u00d4NUS  \u2605', S('bh', fontName='Helvetica-Bold', fontSize=11,
                                                    textColor=DEEP, alignment=TA_CENTER)),
          Paragraph('Pr\u00e1tica de Manifesta\u00e7\u00e3o Poderosa',
                    S('bt2', fontName='Helvetica-Bold', fontSize=18, leading=22,
                      textColor=WHITE, alignment=TA_LEFT))]],
        colWidths=[28 * mm, iw - 28 * mm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), GOLD),
            ('BACKGROUND', (1, 0), (1, 0), DEEP),
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
    story.append(Paragraph('3 pr\u00e1ticas poderosas de manifesta\u00e7\u00e3o.', CLOSING))
    story.append(Paragraph('Use-as todos os dias.',
                            S('cl2', fontName='Helvetica-Bold', fontSize=15, leading=22,
                              textColor=PURPLE, alignment=TA_CENTER, spaceAfter=10)))
    story.append(sp(5))
    story.append(b('O universo responde \u00e0 consist\u00eancia. N\u00e3o \u00e0 perfeic\u00e3o. N\u00e3o ao talento. N\u00e3o \u00e0 sorte. \u00c0 pr\u00e1tica di\u00e1ria, \u00e0 inten\u00e7\u00e3o renovada todos os dias, ao ato de escolher acreditar mesmo antes de ver.'))
    story.append(sp(4))
    story.append(Paragraph('<b>Comece hoje. Agora. Com o que voc\u00ea tem.</b>',
                           S('begin', fontName='Helvetica-Bold', fontSize=13, leading=18,
                             textColor=DEEP, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph('A vida que voc\u00ea sonha est\u00e1 esperando pela sua inten\u00e7\u00e3o.',
                           S('wait', fontName='Helvetica-Oblique', fontSize=12, leading=18,
                             textColor=PURPLE, alignment=TA_CENTER)))
    story.append(sp(10))
    story.append(AccentBar(iw, GOLD))

    return story


# ── Build PDF ─────────────────────────────────────────────────────────────────
def build_pdf(output='3_Tecnicas_Manifestacao_v2.pdf'):
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
        draw_cover(canvas)
        canvas.restoreState()

    def inner_bg(canvas, doc):
        canvas.saveState()
        draw_inner(canvas)
        canvas.restoreState()

    cover_tpl = PageTemplate(id='cover', frames=[cover_frame], onPage=cover_bg)
    inner_tpl = PageTemplate(id='inner', frames=[inner_frame], onPage=inner_bg)
    doc.addPageTemplates([cover_tpl, inner_tpl])

    story = build_content(IW)
    doc.build(story)
    print(f'PDF gerado: {output}')


if __name__ == '__main__':
    build_pdf()
