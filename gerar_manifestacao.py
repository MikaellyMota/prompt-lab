# -*- coding: utf-8 -*-
"""Gerador do Ebook Manifestacao v2 - identidade visual espiritualidade/feminino"""
import sys
sys.path.insert(0, r'C:\PromptLab\Lib\site-packages')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                 Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, KeepTogether, NextPageTemplate)
from reportlab.platypus.flowables import Flowable

W, H = A4
LM = RM = 20 * mm
TM = 22 * mm
BM = 20 * mm
IW = W - LM - RM   # inner width

# ─── Paleta ──────────────────────────────────────────────────────────────────
DEEP_PURPLE  = colors.HexColor('#1E0A3C')
PURPLE       = colors.HexColor('#5B2D8E')
MED_PURPLE   = colors.HexColor('#7B4DB5')
LAVENDER     = colors.HexColor('#EDE0FF')
LIGHT_LAV    = colors.HexColor('#F7F0FF')
GOLD         = colors.HexColor('#C9963B')
LIGHT_GOLD   = colors.HexColor('#FFF8E7')
ROSE         = colors.HexColor('#A63D72')
SOFT_ROSE    = colors.HexColor('#FCE8F3')
CREAM        = colors.HexColor('#FFFEF9')
DARK_TEXT    = colors.HexColor('#1A1A2E')
MID_GRAY     = colors.HexColor('#7A7A9A')
WHITE        = colors.white

# ─── Estilos ─────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY = S('body', fontName='Helvetica', fontSize=10.5, leading=17,
         textColor=DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=8)
BODY_L = S('bodyl', fontName='Helvetica', fontSize=10.5, leading=17,
           textColor=DARK_TEXT, alignment=TA_LEFT, spaceAfter=6)
BOLD_BODY = S('boldb', fontName='Helvetica-Bold', fontSize=10.5, leading=17,
              textColor=DARK_TEXT, alignment=TA_LEFT, spaceAfter=6)
BULLET_ST = S('bullet', fontName='Helvetica', fontSize=10.5, leading=16,
              textColor=DARK_TEXT, leftIndent=18, firstLineIndent=-12, spaceAfter=5)
QUOTE_ST = S('quote', fontName='Helvetica-Oblique', fontSize=11, leading=17,
             textColor=PURPLE, alignment=TA_CENTER, spaceAfter=6)
EXERCISE_TITLE = S('extitle', fontName='Helvetica-Bold', fontSize=11, leading=15,
                   textColor=DEEP_PURPLE, alignment=TA_LEFT, spaceAfter=4)
EXERCISE_BODY = S('exbody', fontName='Helvetica', fontSize=10, leading=15,
                  textColor=DARK_TEXT, alignment=TA_LEFT)
SECTION_NUM = S('secnum', fontName='Helvetica-Bold', fontSize=10, leading=14,
                textColor=MED_PURPLE, alignment=TA_LEFT, spaceAfter=2)
STEP_TITLE = S('steptitle', fontName='Helvetica-Bold', fontSize=11, leading=15,
               textColor=DEEP_PURPLE, alignment=TA_LEFT, spaceAfter=3)
AFFIRMATION = S('affirmation', fontName='Helvetica-Oblique', fontSize=11, leading=17,
                textColor=DEEP_PURPLE, alignment=TA_LEFT, spaceAfter=5)
SMALL_LABEL = S('smalllabel', fontName='Helvetica-Bold', fontSize=9, leading=12,
                textColor=WHITE, alignment=TA_CENTER)
TOC_TITLE = S('toctitle', fontName='Helvetica-Bold', fontSize=13, leading=18,
              textColor=DEEP_PURPLE, alignment=TA_LEFT, spaceAfter=3)
TOC_DESC = S('tocdesc', fontName='Helvetica', fontSize=10, leading=14,
             textColor=MID_GRAY, alignment=TA_LEFT, spaceAfter=2)
CLOSING = S('closing', fontName='Helvetica-Oblique', fontSize=13, leading=20,
            textColor=DEEP_PURPLE, alignment=TA_CENTER, spaceAfter=8)


# ─── Flowables customizados ───────────────────────────────────────────────────

class FullPage(Flowable):
    def wrap(self, avW, avH):
        self._avW = avW
        return avW, 0

    def draw(self):
        pass


class CoverPage(FullPage):
    def draw(self):
        c = self.canv
        # Fundo degradê simulado com retangulos
        c.setFillColor(DEEP_PURPLE)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # Overlay degradê roxo
        c.setFillColor(PURPLE)
        c.setFillAlpha(0.35)
        c.rect(0, H * 0.35, W, H * 0.65, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        # Faixa dourada no topo
        c.setFillColor(GOLD)
        c.rect(0, H - 8 * mm, W, 4 * mm, fill=1, stroke=0)
        # Faixa dourada na base
        c.rect(0, 8 * mm, W, 4 * mm, fill=1, stroke=0)
        # Ornamento circular central
        cx, cy = W / 2, H * 0.52
        for r, alpha in [(90, 0.06), (72, 0.09), (55, 0.13)]:
            c.setFillColor(WHITE)
            c.setFillAlpha(alpha)
            c.circle(cx, cy, r * mm, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        # Estrela/ornamento dourado
        c.setFillColor(GOLD)
        c.setFillAlpha(0.9)
        c.circle(cx, cy, 8 * mm, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        # Badge topo
        bw, bh = 80 * mm, 9 * mm
        bx = (W - bw) / 2
        c.setFillColor(GOLD)
        c.roundRect(bx, H - 28 * mm, bw, bh, 4 * mm, fill=1, stroke=0)
        c.setFillColor(DEEP_PURPLE)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, H - 28 * mm + 2.8 * mm, 'GUIA COMPLETO DE MANIFESTA\u00c7\u00c3O')
        # Titulo principal
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 36)
        c.drawCentredString(W / 2, H * 0.68, 'COMO MANIFESTAR')
        c.setFont('Helvetica-Bold', 36)
        c.drawCentredString(W / 2, H * 0.61, 'A VIDA DOS')
        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 42)
        c.drawCentredString(W / 2, H * 0.53, 'SONHOS')
        # Subtitulo
        c.setFillColor(WHITE)
        c.setFillAlpha(0.85)
        c.setFont('Helvetica-Oblique', 13)
        c.drawCentredString(W / 2, H * 0.43,
            'T\u00e9cnicas poderosas de inten\u00e7\u00e3o, f\u00e9 e a\u00e7\u00e3o')
        c.drawCentredString(W / 2, H * 0.40,
            'para co-criar a realidade que voc\u00ea merece')
        c.setFillAlpha(1.0)
        # Linha separadora dourada
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.line(LM + 20 * mm, H * 0.36, W - LM - 20 * mm, H * 0.36)
        # Rodape
        c.setFillColor(WHITE)
        c.setFillAlpha(0.6)
        c.setFont('Helvetica', 10)
        c.drawCentredString(W / 2, 18 * mm, 'Transforme pensamentos em realidade')
        c.setFillAlpha(1.0)


class InnerPageBg(FullPage):
    def draw(self):
        c = self.canv
        c.setFillColor(CREAM)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # Barra lateral esquerda sutil
        c.setFillColor(LAVENDER)
        c.rect(0, 0, 4 * mm, H, fill=1, stroke=0)
        # Header roxo escuro
        c.setFillColor(DEEP_PURPLE)
        c.rect(0, H - TM, W, TM, fill=1, stroke=0)
        # Texto do header
        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(LM, H - TM + 7 * mm, 'GUIA DE MANIFESTA\u00c7\u00c3O')
        c.setFillColor(WHITE)
        c.setFillAlpha(0.7)
        c.setFont('Helvetica', 8)
        c.drawRightString(W - RM, H - TM + 7 * mm, 'Como Manifestar a Vida dos Sonhos')
        c.setFillAlpha(1.0)
        # Numero da pagina
        page_num = c.getPageNumber()
        if page_num > 2:
            c.setFillColor(MED_GRAY)
            c.setFont('Helvetica', 8)
            c.drawCentredString(W / 2, 10 * mm, str(page_num - 2))


class ChapterHeader(Flowable):
    def __init__(self, num, title, subtitle, color=PURPLE, iw=IW):
        super().__init__()
        self.num = num
        self.title = title
        self.subtitle = subtitle
        self.color = color
        self.iw = iw
        self.height = 42 * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw
        # Fundo do header do capitulo
        c.setFillColor(self.color)
        c.roundRect(0, 0, iw, self.height, 4 * mm, fill=1, stroke=0)
        # Numero grande transparente de fundo
        c.setFillColor(WHITE)
        c.setFillAlpha(0.08)
        c.setFont('Helvetica-Bold', 80)
        c.drawRightString(iw - 8 * mm, 2 * mm, str(self.num).zfill(2))
        c.setFillAlpha(1.0)
        # Badge capitulo
        c.setFillColor(GOLD)
        c.roundRect(8 * mm, self.height - 14 * mm, 28 * mm, 8 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillColor(DEEP_PURPLE)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(10 * mm, self.height - 14 * mm + 2.5 * mm, f'CAP\u00cdTULO  {str(self.num).zfill(2)}')
        # Titulo
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 22)
        c.drawString(8 * mm, self.height - 26 * mm, self.title)
        # Subtitulo
        c.setFillColor(WHITE)
        c.setFillAlpha(0.75)
        c.setFont('Helvetica-Oblique', 11)
        c.drawString(8 * mm, self.height - 33 * mm, self.subtitle)
        c.setFillAlpha(1.0)


class AccentBar(Flowable):
    def __init__(self, iw=IW, color=GOLD, h=2.5):
        super().__init__()
        self.iw = iw
        self.color = color
        self.bh = h

    def wrap(self, *a):
        return self.iw, self.bh + 4

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 2, self.iw, self.bh, fill=1, stroke=0)


class ExerciseBox(Flowable):
    def __init__(self, title, lines, iw=IW):
        super().__init__()
        self.title = title
        self.lines = lines
        self.iw = iw
        self.height = (14 + len(lines) * 14 + 10) * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw
        h = self.height
        # Fundo lavanda
        c.setFillColor(LAVENDER)
        c.roundRect(0, 0, iw, h, 3 * mm, fill=1, stroke=0)
        # Borda esquerda roxa
        c.setFillColor(PURPLE)
        c.roundRect(0, 0, 3 * mm, h, 1.5 * mm, fill=1, stroke=0)
        # Icone e titulo
        c.setFillColor(DEEP_PURPLE)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(8 * mm, h - 9 * mm, f'\u2728  {self.title}')
        # Linha separadora
        c.setStrokeColor(MED_PURPLE)
        c.setLineWidth(0.5)
        c.line(8 * mm, h - 11 * mm, iw - 5 * mm, h - 11 * mm)
        # Linhas de conteudo
        c.setFillColor(DARK_TEXT)
        c.setFont('Helvetica', 10)
        y = h - 15 * mm
        for line in self.lines:
            c.drawString(8 * mm, y, line)
            y -= 7 * mm


class QuoteBox(Flowable):
    def __init__(self, text, author='', iw=IW):
        super().__init__()
        self.text = text
        self.author = author
        self.iw = iw
        self.height = 30 * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw
        h = self.height
        c.setFillColor(SOFT_ROSE)
        c.roundRect(0, 0, iw, h, 3 * mm, fill=1, stroke=0)
        c.setFillColor(ROSE)
        c.roundRect(0, 0, 3 * mm, h, 1.5 * mm, fill=1, stroke=0)
        # Aspas decorativas
        c.setFillColor(ROSE)
        c.setFillAlpha(0.25)
        c.setFont('Helvetica-Bold', 50)
        c.drawString(4 * mm, h - 16 * mm, '\u201c')
        c.setFillAlpha(1.0)
        c.setFillColor(ROSE)
        c.setFont('Helvetica-Oblique', 11)
        c.drawCentredString(iw / 2, h - 13 * mm, self.text)
        if self.author:
            c.setFillColor(MID_GRAY)
            c.setFont('Helvetica', 9)
            c.drawCentredString(iw / 2, h - 20 * mm, f'\u2014 {self.author}')


class TipBox(Flowable):
    def __init__(self, text, iw=IW):
        super().__init__()
        self.text = text
        self.iw = iw
        self.height = 22 * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw
        h = self.height
        c.setFillColor(LIGHT_GOLD)
        c.roundRect(0, 0, iw, h, 3 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.roundRect(0, 0, 3 * mm, h, 1.5 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(8 * mm, h - 8 * mm, '\u2605  DICA:')
        c.setFillColor(DARK_TEXT)
        c.setFont('Helvetica', 10)
        c.drawString(8 * mm, h - 15 * mm, self.text)


class DailyRoutineBox(Flowable):
    def __init__(self, iw=IW):
        super().__init__()
        self.iw = iw
        self.height = 120 * mm

    def wrap(self, avW, avH):
        return self.iw, self.height

    def draw(self):
        c = self.canv
        iw = self.iw
        h = self.height
        # Fundo geral
        c.setFillColor(LAVENDER)
        c.roundRect(0, 0, iw, h, 4 * mm, fill=1, stroke=0)
        # Titulo
        c.setFillColor(DEEP_PURPLE)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(iw / 2, h - 12 * mm, '\u2728  SUA ROTINA DI\u00c1RIA DE MANIFESTA\u00c7\u00c3O')
        # Linha
        c.setStrokeColor(PURPLE)
        c.setLineWidth(0.8)
        c.line(10 * mm, h - 15 * mm, iw - 10 * mm, h - 15 * mm)
        # 3 blocos: manha, tarde, noite
        blocks = [
            ('\u2600\ufe0f  MANH\u00c3  (6h \u2013 8h)', GOLD, [
                '\u2605 Ao acordar: 3 respira\u00e7\u00f5es de gratid\u00e3o',
                '\u2605 Escreva sua afirma\u00e7\u00e3o 3 vezes \u2014 T\u00e9cnica 369',
                '\u2605 10\u201315 min de medita\u00e7\u00e3o e visualiza\u00e7\u00e3o',
                '\u2605 Olhe seu vision board por 2 minutos',
            ]),
            ('\u2600  TARDE  (12h \u2013 14h)', MED_PURPLE, [
                '\u2605 Escreva sua afirma\u00e7\u00e3o 6 vezes \u2014 T\u00e9cnica 369',
                '\u2605 Pausa consciente: respira\u00e7\u00e3o + gratid\u00e3o',
                '\u2605 A\u00e7\u00e3o intencional: um passo em dire\u00e7\u00e3o ao objetivo',
            ]),
            ('\ud83c\udf19  NOITE  (21h \u2013 22h)', ROSE, [
                '\u2605 Di\u00e1rio de gratid\u00e3o: 3\u20135 coisas boas do dia',
                '\u2605 Escreva sua afirma\u00e7\u00e3o 9 vezes \u2014 T\u00e9cnica 369',
                '\u2605 Releia seu scripting com emo\u00e7\u00e3o',
                '\u2605 Durma nessa frequ\u00eancia de plenitude',
            ]),
        ]
        bh = 28 * mm
        bw = (iw - 12 * mm) / 3
        bx = 6 * mm
        by = h - 18 * mm - bh
        for title, col, items in blocks:
            c.setFillColor(col)
            c.roundRect(bx, by, bw, bh, 3 * mm, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 8)
            c.drawCentredString(bx + bw / 2, by + bh - 6 * mm, title)
            c.setFont('Helvetica', 7.5)
            ty = by + bh - 12 * mm
            for item in items:
                c.drawString(bx + 3 * mm, ty, item)
                ty -= 5.5 * mm
            bx += bw + 2 * mm

        # Linha de base
        c.setFillColor(DEEP_PURPLE)
        c.setFillAlpha(0.08)
        c.roundRect(6 * mm, 5 * mm, iw - 12 * mm, 22 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        c.setFillColor(PURPLE)
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(iw / 2, 20 * mm, '\u2728  A consist\u00eancia diaria \u00e9 o que separa quem manifesta de quem apenas deseja.')
        c.setFillColor(MID_GRAY)
        c.setFont('Helvetica', 9)
        c.drawCentredString(iw / 2, 13 * mm, 'Comece com uma semana. Depois 21 dias. Depois vai ser natural como respirar.')


# ─── Conteudo dos capitulos ───────────────────────────────────────────────────

CHAPTER_COLORS = [PURPLE, MED_PURPLE, ROSE, PURPLE, MED_PURPLE,
                  ROSE, PURPLE, MED_PURPLE, ROSE, PURPLE]


def b(text):
    return Paragraph(text, BODY)


def bl(text):
    return Paragraph(text, BODY_L)


def bb(text):
    return Paragraph(text, BOLD_BODY)


def bul(text):
    return Paragraph(f'\u2022  {text}', BULLET_ST)


def aff(text):
    return Paragraph(f'\u201c{text}\u201d', AFFIRMATION)


def sp(n=6):
    return Spacer(1, n * mm)


def build_content(iw):
    story = []

    # ── Sumario ──────────────────────────────────────────────────────────────
    story.append(NextPageTemplate('inner'))
    story.append(PageBreak())

    chapters_toc = [
        ('01', 'O Que \u00e9 Manifesta\u00e7\u00e3o?', 'Mente, vibra\u00e7\u00e3o e co-cria\u00e7\u00e3o \u2014 a base de tudo.'),
        ('02', 'Prepare o Terreno Interior', 'Clareza, cren\u00e7as limitantes e frequ\u00eancia emocional.'),
        ('03', 'T\u00e9cnica 369 de Tesla', 'O m\u00e9todo dos n\u00fameros sagrados para reprogramar o subconsciente.'),
        ('04', 'Scripting \u2014 Escrita Criativa', 'Escreva sua vida como se ela j\u00e1 fosse realidade.'),
        ('05', 'Vision Board', 'O painel dos sonhos que ancora sua vis\u00e3o no mundo f\u00edsico.'),
        ('06', 'Afirma\u00e7\u00f5es e Mantras', 'Frases que reprogramam sua mente todos os dias.'),
        ('07', 'Gratid\u00e3o como Combust\u00edvel', 'A pr\u00e1tica mais poderosa da manifesta\u00e7\u00e3o.'),
        ('08', 'Medita\u00e7\u00e3o e Visualiza\u00e7\u00e3o', 'Acesse o estado alfa e sinta seu desejo realizado.'),
        ('09', 'Rotina Di\u00e1ria', 'Monte sua rotina pr\u00e1tica passo a passo.'),
        ('10', 'A\u00e7\u00e3o com Inten\u00e7\u00e3o', 'Como equilibrar manifesta\u00e7\u00e3o e a\u00e7\u00e3o no mundo real.'),
    ]

    story.append(sp(8))
    story.append(Paragraph('<font color="#1E0A3C"><b>S U M \u00c1 R I O</b></font>',
                           S('toch', fontName='Helvetica-Bold', fontSize=28, leading=34,
                             textColor=DEEP_PURPLE, alignment=TA_LEFT, spaceAfter=6)))
    story.append(AccentBar(iw, GOLD))
    story.append(sp(6))

    for num, title, desc in chapters_toc:
        row = Table(
            [[Paragraph(f'<font color="#5B2D8E"><b>{num}</b></font>',
                        S('tocn', fontName='Helvetica-Bold', fontSize=18, leading=22,
                          textColor=PURPLE, alignment=TA_CENTER)),
              [Paragraph(f'<b>{title}</b>', TOC_TITLE),
               Paragraph(desc, TOC_DESC)]]],
            colWidths=[18 * mm, iw - 18 * mm],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ])
        )
        story.append(row)
        story.append(AccentBar(iw, LAVENDER, 1))
        story.append(sp(1))

    # ── Cap 1: O Que é Manifestação ───────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(1, 'O Que \u00e9 Manifesta\u00e7\u00e3o?',
                               'Mente, vibra\u00e7\u00e3o e co-cria\u00e7\u00e3o \u2014 a base de tudo.', CHAPTER_COLORS[0], iw))
    story.append(sp(5))
    story.append(b('Manifestar \u00e9 trazer algo do plano dos pensamentos para a realidade f\u00edsica. \u00c9 um processo consciente pelo qual voc\u00ea se torna a autora da sua pr\u00f3pria vida, focando energia, aten\u00e7\u00e3o e emo\u00e7\u00e3o naquilo que deseja criar.'))
    story.append(b('Somos seres energ\u00e9ticos e nossos pensamentos emitem frequ\u00eancias que ressoam com experi\u00eancias semelhantes ao redor. Quando alinhamos mente, emo\u00e7\u00e3o e a\u00e7\u00e3o em dire\u00e7\u00e3o a um objetivo, abrimos caminho para que ele se materialize.'))
    story.append(sp(3))
    story.append(QuoteBox('Tudo o que a mente pode conceber e acreditar, ela pode alcan\u00e7ar.', 'Napoleon Hill'))
    story.append(sp(5))
    story.append(bb('Os 3 Pilares da Manifesta\u00e7\u00e3o'))
    story.append(AccentBar(iw, PURPLE, 2))
    story.append(sp(3))

    pilares = [
        [Paragraph('\ud83e\udde0  PENSAMENTO', S('ph', fontName='Helvetica-Bold', fontSize=10,
                                                  textColor=WHITE, alignment=TA_CENTER)),
         Paragraph('Tudo come\u00e7a na mente. O que voc\u00ea pensa com frequ\u00eancia e emo\u00e7\u00e3o molda sua realidade. Cultivar pensamentos alinhados com o que deseja \u00e9 o primeiro passo.', BODY_L)],
        [Paragraph('\u2764\ufe0f  EMO\u00c7\u00c3O', S('ph', fontName='Helvetica-Bold', fontSize=10,
                                                 textColor=WHITE, alignment=TA_CENTER)),
         Paragraph('A emo\u00e7\u00e3o \u00e9 o combust\u00edvel. Sentir como se seu desejo j\u00e1 fosse realidade envia ao universo o sinal de que voc\u00ea est\u00e1 pronta para receber.', BODY_L)],
        [Paragraph('\u26a1  A\u00c7\u00c3O', S('ph', fontName='Helvetica-Bold', fontSize=10,
                                              textColor=WHITE, alignment=TA_CENTER)),
         Paragraph('Manifesta\u00e7\u00e3o n\u00e3o \u00e9 passividade. Agir com inten\u00e7\u00e3o \u2014 dando passos na dire\u00e7\u00e3o certa \u2014 cria o canal por onde seus desejos chegam.', BODY_L)],
    ]
    tbl = Table(pilares, colWidths=[32 * mm, iw - 32 * mm],
                style=TableStyle([
                    ('BACKGROUND', (0, 0), (0, 0), PURPLE),
                    ('BACKGROUND', (0, 1), (0, 1), MED_PURPLE),
                    ('BACKGROUND', (0, 2), (0, 2), ROSE),
                    ('ROWBACKGROUNDS', (1, 0), (1, -1), [LIGHT_LAV, LAVENDER, SOFT_ROSE]),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (1, 0), (1, -1), 8),
                    ('ROUNDEDCORNERS', [3, 3, 3, 3]),
                ]))
    story.append(tbl)

    # ── Cap 2: Prepare o Terreno Interior ────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(2, 'Prepare o Terreno Interior',
                               'Clareza, cren\u00e7as limitantes e frequ\u00eancia emocional.', CHAPTER_COLORS[1], iw))
    story.append(sp(5))
    story.append(b('Antes de qualquer t\u00e9cnica, \u00e9 preciso preparar o solo interno. Manifestar sem clareza \u00e9 como plantar sementes em terra pedregosa. Tr\u00eas elementos s\u00e3o fundamentais nessa prepara\u00e7\u00e3o:'))
    story.append(sp(3))

    story.append(bb('1. Clareza Total do Desejo'))
    story.append(b('Seja absolutamente espec\u00edfica. N\u00e3o basta querer \u201cmais dinheiro\u201d ou \u201cum relacionamento\u201d. Defina com precis\u00e3o: quanto dinheiro? At\u00e9 quando? Que tipo de parceria? Quanto mais detalhes, mais poderoso o sinal enviado.'))
    story.append(TipBox('Evite palavras como \u201cquero\u201d ou \u201cpreciso\u201d \u2014 elas refor\u00e7am a aus\u00eancia. Use sempre o presente: \u201cEu tenho\u201d, \u201cEu sou\u201d, \u201cEu recebo\u201d.'))
    story.append(sp(4))

    story.append(bb('2. Identifique Cren\u00e7as Limitantes'))
    story.append(b('Cren\u00e7as como \u201cdinheiro \u00e9 dif\u00edcil\u201d, \u201ceu n\u00e3o mere\u00e7o\u201d ou \u201cnunca vou conseguir\u201d criam bloqueios energ\u00e9ticos poderosos. Observe os pensamentos que surgem quando voc\u00ea imagina seu desejo realizado \u2014 eles revelam seus bloqueios.'))
    story.append(sp(2))
    story.append(ExerciseBox('EXERC\u00cdCIO: Identificando Bloqueios', [
        'Escreva no topo de uma p\u00e1gina em branco:',
        '\u201cQuando imagino meu sonho realizado, o que vem \u00e0 minha mente?\u201d',
        'Anote tudo sem julgamento. Esses pensamentos revelam',
        'exatamente onde est\u00e3o seus bloqueios energ\u00e9ticos.',
    ]))
    story.append(sp(4))

    story.append(bb('3. Eleve Sua Frequ\u00eancia Emocional'))
    story.append(b('Gratid\u00e3o, amor e alegria s\u00e3o as frequ\u00eancias mais altas. Medita\u00e7\u00e3o, exerc\u00edcio, m\u00fasica que voc\u00ea ama e conex\u00f5es genuinamente positivas elevam sua vibra\u00e7\u00e3o naturalmente. Quando voc\u00ea vive nessas frequ\u00eancias, torna-se um \u00edm\u00e3 para experi\u00eancias positivas.'))

    # ── Cap 3: Técnica 369 ────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(3, 'T\u00e9cnica 369 de Tesla',
                               'O m\u00e9todo dos n\u00fameros sagrados para reprogramar o subconsciente.', CHAPTER_COLORS[2], iw))
    story.append(sp(5))
    story.append(b('A T\u00e9cnica 369 foi inspirada em Nikola Tesla, que considerava os n\u00fameros 3, 6 e 9 sagrados. Essa t\u00e9cnica combina repeti\u00e7\u00e3o, foco e inten\u00e7\u00e3o para reprogramar o subconsciente e alinhar sua frequ\u00eancia com o que deseja.'))
    story.append(sp(3))

    steps_369 = [
        ['3', 'MANH\u00c3 \u2014 ao acordar', 'Escreva sua afirma\u00e7\u00e3o 3 vezes num caderno dedicado. Os primeiros minutos do dia s\u00e3o quando o subconsciente est\u00e1 mais receptivo a novas programa\u00e7\u00f5es.', GOLD],
        ['6', 'TARDE \u2014 no meio do dia', 'Escreva a mesma afirma\u00e7\u00e3o 6 vezes. Ao escrever, feche os olhos por alguns segundos e sinta a emo\u00e7\u00e3o de j\u00e1 ter realizado esse desejo.', MED_PURPLE],
        ['9', 'NOITE \u2014 antes de dormir', 'Escreva 9 vezes. Durma carregando essa energia \u2014 o subconsciente continuar\u00e1 processando a inten\u00e7\u00e3o durante o sono.', ROSE],
    ]
    for num, when, desc, col in steps_369:
        row = Table(
            [[Paragraph(f'<b>{num}</b>', S('n369', fontName='Helvetica-Bold', fontSize=28,
                                           leading=32, textColor=WHITE, alignment=TA_CENTER)),
              [Paragraph(f'<b>{when}</b>', S('wh', fontName='Helvetica-Bold', fontSize=11,
                                              leading=14, textColor=col)),
               Paragraph(desc, BODY_L)]]],
            colWidths=[20 * mm, iw - 20 * mm],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), col),
                ('BACKGROUND', (1, 0), (1, 0), LIGHT_LAV),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (1, 0), (1, 0), 8),
            ])
        )
        story.append(row)
        story.append(sp(2))

    story.append(sp(3))
    story.append(bb('Como Formular Sua Afirma\u00e7\u00e3o'))
    story.append(b('Escreva no presente, com gratid\u00e3o e especificidade:'))
    story.append(aff('Sou grata ao universo pela minha sa\u00fade plena e abundante energia todos os dias.'))
    story.append(aff('Recebo com alegria R$ 10.000 mensais atrav\u00e9s do meu trabalho com prop\u00f3sito.'))
    story.append(aff('Vivo em um lar lindo e amoroso, me sinto em paz e plenamente realizada.'))
    story.append(sp(3))
    story.append(TipBox('Pratique por 21 a 33 dias consecutivos. A consist\u00eancia transforma repeti\u00e7\u00e3o em reprograma\u00e7\u00e3o.'))

    # ── Cap 4: Scripting ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(4, 'Scripting \u2014 Escrita Criativa',
                               'Escreva sua vida como se ela j\u00e1 fosse realidade.', CHAPTER_COLORS[3], iw))
    story.append(sp(5))
    story.append(b('Scripting \u00e9 uma das t\u00e9cnicas mais poderosas: voc\u00ea escreve detalhadamente sua vida dos sonhos como se ela j\u00e1 existisse. \u00c9 criar o roteiro de um filme \u2014 e voc\u00ea \u00e9 a protagonista, a diretora e a escritora.'))
    story.append(sp(3))
    story.append(bb('Passo a Passo do Scripting'))
    story.append(AccentBar(iw, PURPLE, 2))
    story.append(sp(3))

    scripting_steps = [
        ('01', 'Escolha um momento tranquilo', 'Manh\u00e3 ou noite, sem distra\u00e7\u00f5es. Coloque uma m\u00fasica suave se quiser criar o ambiente certo.'),
        ('02', 'Escreva no presente', 'Comece com frases como: \u201cHoje acordei e...\u201d ou \u201cEstou t\u00e3o feliz porque...\u201d'),
        ('03', 'Inclua todos os sentidos', 'O que voc\u00ea v\u00ea, sente, cheira e ouve na sua vida dos sonhos? Quanto mais v\u00edvido, melhor.'),
        ('04', 'Adicione emo\u00e7\u00e3o genuinamente', 'Deixe a alegria e a gratid\u00e3o fluirem enquanto escreve. Sinta cada palavra!'),
        ('05', 'Releia com emo\u00e7\u00e3o', 'Reler periodicamente reativa a inten\u00e7\u00e3o e mant\u00e9m sua frequ\u00eancia elevada.'),
    ]
    for num, title, desc in scripting_steps:
        row = Table(
            [[Paragraph(f'<b>{num}</b>', S('sn', fontName='Helvetica-Bold', fontSize=14,
                                           leading=18, textColor=PURPLE, alignment=TA_CENTER)),
              [Paragraph(f'<b>{title}</b>', STEP_TITLE),
               Paragraph(desc, BODY_L)]]],
            colWidths=[14 * mm, iw - 14 * mm],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (1, 0), (1, 0), 6),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, LAVENDER),
            ])
        )
        story.append(row)

    story.append(sp(5))
    story.append(ExerciseBox('EXEMPLO DE SCRIPTING', [
        '\u201cEstou t\u00e3o feliz e grata por viver na casa dos meus sonhos.',
        'Hoje acordei e o sol entrava pela janela do quarto.',
        'Meu neg\u00f3cio floresce, tenho liberdade e paz.',
        'Tudo no lugar certo, no tempo certo.\u201d',
    ]))

    # ── Cap 5: Vision Board ───────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(5, 'Vision Board',
                               'O painel dos sonhos que ancora sua vis\u00e3o no mundo f\u00edsico.', CHAPTER_COLORS[4], iw))
    story.append(sp(5))
    story.append(b('O Vision Board ancora seus desejos no mundo f\u00edsico. Ver imagens que representam seus sonhos diariamente ativa o sistema de ativa\u00e7\u00e3o reticular do c\u00e9rebro \u2014 fazendo voc\u00ea notar oportunidades que antes passavam despercebidas.'))
    story.append(sp(3))
    story.append(bb('Como Criar Seu Vision Board'))
    story.append(AccentBar(iw, ROSE, 2))
    story.append(sp(3))

    vb_items = [
        ('\ud83c\udfaf', 'Defina as \u00e1reas', 'Escolha as categorias: amor, finan\u00e7as, sa\u00fade, carreira, espiritualidade, viagens.'),
        ('\ud83d\uddbc\ufe0f', 'Colete imagens', 'Recorte de revistas ou imprima fotos que representam como voc\u00ea quer cada \u00e1rea.'),
        ('\u270d\ufe0f', 'Adicione palavras', 'Inclua afirma\u00e7\u00f5es e palavras que inspiram: Abund\u00e2ncia, Paz, Amor, Liberdade.'),
        ('\ud83d\udccc', 'Posicione com inten\u00e7\u00e3o', 'Cole em um cartaz e coloque onde voc\u00ea veja todos os dias: quarto, escrit\u00f3rio.'),
        ('\ud83d\ude4f', 'Visualize diariamente', '2 minutos em frente ao painel: imagine-se vivendo aquilo, sentindo as emo\u00e7\u00f5es.'),
    ]
    for icon, title, desc in vb_items:
        story.append(bul(f'<b>{title}</b> \u2014 {desc}'))

    story.append(sp(4))
    story.append(TipBox('Crie seu Vision Board no Pinterest ou Canva e use como papel de parede do celular \u2014 para ver v\u00e1rias vezes ao dia!'))

    # ── Cap 6: Afirmações ─────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(6, 'Afirma\u00e7\u00f5es e Mantras',
                               'Frases que reprogramam sua mente todos os dias.', CHAPTER_COLORS[5], iw))
    story.append(sp(5))
    story.append(b('Afirma\u00e7\u00f5es s\u00e3o frases repetidas para reprogramar o subconsciente. A chave \u00e9 a emo\u00e7\u00e3o: uma afirma\u00e7\u00e3o dita com sentimento genuinamente tem muito mais poder. Escolha frases que fa\u00e7am seu cora\u00e7\u00e3o vibrar.'))
    story.append(sp(4))

    categories = [
        ('\ud83d\udcb0 ABUND\u00c2NCIA', GOLD, LIGHT_GOLD, [
            'Dinheiro chega at\u00e9 mim de formas f\u00e1ceis e inesperadas.',
            'Sou aberta para receber riqueza em todas as suas formas.',
            'Meus ganhos crescem a cada dia de forma natural e sustent\u00e1vel.',
        ]),
        ('\u2764\ufe0f AMOR', ROSE, SOFT_ROSE, [
            'Mere\u00e7o e recebo amor verdadeiro, respeitoso e apaixonado.',
            'Meu cora\u00e7\u00e3o est\u00e1 aberto para dar e receber amor pleno.',
            'Atraio relacionamentos saud\u00e1veis que me elevam.',
        ]),
        ('\ud83c\udf3f SA\u00daDE', MED_PURPLE, LAVENDER, [
            'Meu corpo \u00e9 forte, saud\u00e1vel e cheio de vitalidade.',
            'Cuido do meu corpo com amor e ele me responde com energia.',
            'Cada c\u00e9lula do meu ser vibra em sa\u00fade e bem-estar.',
        ]),
        ('\ud83d\ude80 CARREIRA', PURPLE, LIGHT_LAV, [
            'Meu trabalho me realiza e gera prosperidade crescente.',
            'Sou reconhecida e valorizada pelo que ofere\u00e7o ao mundo.',
            'Oportunidades incr\u00edveis chegam at\u00e9 mim naturalmente.',
        ]),
    ]
    for cat_title, col, bg, affirmations in categories:
        tbl_data = [[Paragraph(f'<b>{cat_title}</b>', S('ct', fontName='Helvetica-Bold', fontSize=11,
                                                         textColor=WHITE, alignment=TA_LEFT)),
                     '']]
        for a_text in affirmations:
            tbl_data.append([Paragraph(f'\u2728 {a_text}', S('af', fontName='Helvetica-Oblique',
                                                               fontSize=10.5, leading=15,
                                                               textColor=DARK_TEXT)),
                             ''])
        tbl = Table(tbl_data, colWidths=[iw, 0],
                    style=TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), col),
                        ('BACKGROUND', (0, 1), (-1, -1), bg),
                        ('TOPPADDING', (0, 0), (-1, -1), 5),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                        ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ]))
        story.append(tbl)
        story.append(sp(3))

    # ── Cap 7: Gratidão ───────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(7, 'Gratid\u00e3o como Combust\u00edvel',
                               'A pr\u00e1tica mais poderosa da manifesta\u00e7\u00e3o.', CHAPTER_COLORS[6], iw))
    story.append(sp(5))
    story.append(b('A gratid\u00e3o \u00e9 considerada a ferramenta mais poderosa de manifesta\u00e7\u00e3o. Quando voc\u00ea \u00e9 genuinamente grata pelo que j\u00e1 tem, envia ao universo a mensagem de que est\u00e1 em abund\u00e2ncia \u2014 e o universo responde enviando mais.'))
    story.append(b('Pesquisas mostram que pessoas que praticam gratid\u00e3o regularmente s\u00e3o mais otimistas, t\u00eam melhor sa\u00fade cardiovascular e relatam maior satisfa\u00e7\u00e3o com a vida.'))
    story.append(sp(3))
    story.append(QuoteBox('A gratid\u00e3o desbloqueia a plenitude da vida. Transforma o que temos em suficiente, e mais.', 'Melody Beattie'))
    story.append(sp(4))
    story.append(bb('Pr\u00e1ticas de Gratid\u00e3o'))
    story.append(AccentBar(iw, GOLD, 2))
    story.append(sp(3))
    story.append(bul('<b>Di\u00e1rio de Gratid\u00e3o</b> \u2014 Antes de dormir, escreva 3 a 5 coisas pelas quais \u00e9 grata no dia. Podem ser pequenas: um caf\u00e9 quente, um abra\u00e7o, uma mensagem carinhosa.'))
    story.append(bul('<b>Gratid\u00e3o Antecipada</b> \u2014 Agrade\u00e7a ANTES de receber, como se j\u00e1 tivesse conquistado. \u201cObrigada, Universo, pela minha casa nova\u201d \u2014 dita com sentimento \u2014 cria a vibra\u00e7\u00e3o da realiza\u00e7\u00e3o.'))
    story.append(bul('<b>Manh\u00e3 de Gratid\u00e3o</b> \u2014 Ao acordar, antes do celular, diga 3 coisas pelas quais \u00e9 grata neste momento. Isso define o tom emocional do seu dia inteiro.'))
    story.append(sp(4))
    story.append(ExerciseBox('EXERC\u00cdCIO: Di\u00e1rio de 7 Dias', [
        'Por 7 dias seguidos, escreva antes de dormir:',
        '1. Algo simples pelo qual sou grata hoje.',
        '2. Uma pessoa que me fez bem esta semana.',
        '3. Uma conquista, por menor que seja.',
        'Observe como sua vibra\u00e7\u00e3o muda ao longo dos dias.',
    ]))

    # ── Cap 8: Meditação ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(8, 'Medita\u00e7\u00e3o e Visualiza\u00e7\u00e3o',
                               'Acesse o estado alfa e sinta seu desejo realizado.', CHAPTER_COLORS[7], iw))
    story.append(sp(5))
    story.append(b('Quando meditamos, o c\u00e9rebro entra no estado alfa \u2014 uma frequ\u00eancia em que o subconsciente fica mais receptivo a novas cren\u00e7as. \u00c9 o momento ideal para a visualiza\u00e7\u00e3o criativa e para plantar sementes poderosas.'))
    story.append(sp(3))
    story.append(bb('Roteiro de Medita\u00e7\u00e3o'))
    story.append(AccentBar(iw, MED_PURPLE, 2))
    story.append(sp(3))

    med_steps = [
        ('1', 'Prepare o ambiente', 'Lugar tranquilo, sem distra\u00e7\u00f5es. Sente-se ou deite-se confortavelmente.'),
        ('2', 'Respire fundo', 'Inspire por 4s, segure 4s, expire em 6s. Repita 5 vezes. Relaxe completamente.'),
        ('3', 'Entre na cena', 'Com olhos fechados, visualize um dia perfeito na sua vida dos sonhos.'),
        ('4', 'Ative todos os sentidos', 'O que voc\u00ea v\u00ea? Que sons h\u00e1? O que sente no corpo? Seja espec\u00edfica e viva.'),
        ('5', 'Sinta a emo\u00e7\u00e3o', 'Deixe surgir alegria, amor, gratid\u00e3o. Sinta-as genuinamente no peito.'),
        ('6', 'Encerre com gratid\u00e3o', '\u201cObrigada por esta vida. \u00c9 minha.\u201d Respire fundo e abra os olhos devagar.'),
    ]
    for num, title, desc in med_steps:
        row = Table(
            [[Paragraph(f'<b>{num}</b>', S('mn', fontName='Helvetica-Bold', fontSize=16,
                                           leading=20, textColor=MED_PURPLE, alignment=TA_CENTER)),
              [Paragraph(f'<b>{title}</b>', STEP_TITLE),
               Paragraph(desc, BODY_L)]]],
            colWidths=[12 * mm, iw - 12 * mm],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (1, 0), (1, 0), 6),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, LAVENDER),
            ])
        )
        story.append(row)

    story.append(sp(4))
    story.append(TipBox('Comece com apenas 10 minutos por dia. O mais importante \u00e9 a regularidade, n\u00e3o a dura\u00e7\u00e3o.'))

    # ── Cap 9: Rotina Diária ──────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(9, 'Rotina Di\u00e1ria de Manifesta\u00e7\u00e3o',
                               'Monte sua rotina pr\u00e1tica passo a passo.', CHAPTER_COLORS[8], iw))
    story.append(sp(5))
    story.append(b('A manifesta\u00e7\u00e3o \u00e9 uma pr\u00e1tica di\u00e1ria. Uma rotina consistente \u00e9 o que separa quem manifesta de quem apenas deseja. Adapte essa sugest\u00e3o \u00e0 sua realidade e comece hoje.'))
    story.append(sp(5))
    story.append(DailyRoutineBox(iw))

    # ── Cap 10: Ação com Intenção ─────────────────────────────────────────────
    story.append(PageBreak())
    story.append(ChapterHeader(10, 'A\u00e7\u00e3o com Inten\u00e7\u00e3o',
                               'Como equilibrar manifesta\u00e7\u00e3o e a\u00e7\u00e3o no mundo real.', CHAPTER_COLORS[9], iw))
    story.append(sp(5))
    story.append(b('Um dos maiores equivos \u00e9 achar que basta visualizar e esperar. A a\u00e7\u00e3o \u00e9 o canal f\u00edsico pelo qual seus desejos chegam. O universo usa caminhos concretos \u2014 e voc\u00ea precisa estar em movimento para reconhec\u00ea-los.'))
    story.append(b('A diferen\u00e7a entre a\u00e7\u00e3o comum e a\u00e7\u00e3o intencional \u00e9 a consci\u00eancia. Voc\u00ea age porque acredita, porque j\u00e1 se sente no caminho certo \u2014 n\u00e3o por ansiedade ou medo.'))
    story.append(sp(4))

    action_items = [
        ('\u2605', 'Um passo por dia', 'N\u00e3o precisa ser enorme. Uma liga\u00e7\u00e3o, um e-mail, uma pesquisa. A consist\u00eancia de pequenas a\u00e7\u00f5es cria um momentum poderoso e impar\u00e1vel.'),
        ('\u2605', 'Solte o controle', 'Manifeste com inten\u00e7\u00e3o, mas sem apego ao \u201ccomo\u201d e ao \u201cquando\u201d. O universo conhece caminhos que voc\u00ea nem imagina existirem.'),
        ('\u2605', 'Reconhe\u00e7a os sinais', 'Sincronicidades, encontros inesperados, ideias repentinas \u2014 s\u00e3o os sinais do universo apontando a dire\u00e7\u00e3o. Esteja atenta.'),
        ('\u2605', 'Confie no processo', 'Algumas manifesta\u00e7\u00f5es chegam r\u00e1pido, outras levam tempo. A semente que voc\u00ea plantou est\u00e1 crescendo, mesmo que ainda n\u00e3o veja.'),
    ]
    for icon, title, desc in action_items:
        story.append(bul(f'<b>{title}</b> \u2014 {desc}'))
        story.append(sp(1))

    story.append(sp(4))
    story.append(QuoteBox('A manifesta\u00e7\u00e3o \u00e9 a dan\u00e7a entre o que voc\u00ea deseja e o que est\u00e1 disposta a fazer para receber.'))

    # ── Pagina final ──────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(sp(20))
    story.append(AccentBar(iw, GOLD))
    story.append(sp(8))
    story.append(Paragraph('\u2728', S('star', fontName='Helvetica-Bold', fontSize=40,
                                        textColor=GOLD, alignment=TA_CENTER, spaceAfter=6)))
    story.append(Paragraph('Voc\u00ea j\u00e1 tem dentro de si', CLOSING))
    story.append(Paragraph('tudo que precisa para criar', CLOSING))
    story.append(Paragraph('a vida dos seus sonhos.', S('closing2', fontName='Helvetica-Bold',
                                                          fontSize=16, leading=22,
                                                          textColor=PURPLE, alignment=TA_CENTER,
                                                          spaceAfter=10)))
    story.append(sp(6))
    story.append(b('As t\u00e9cnicas deste guia s\u00e3o ferramentas \u2014 mas o verdadeiro poder est\u00e1 na sua f\u00e9, na sua consist\u00eancia e na sua disposi\u00e7\u00e3o de agir mesmo sem ver o resultado ainda.'))
    story.append(sp(4))
    story.append(Paragraph('<b>Comece hoje.</b> Com um caderno, uma afirma\u00e7\u00e3o, um momento de sil\u00eancio.',
                           S('begin', fontName='Helvetica-Bold', fontSize=12, leading=18,
                             textColor=DEEP_PURPLE, alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph('A vida que voc\u00ea sonha est\u00e1 esperando por voc\u00ea.',
                           S('wait', fontName='Helvetica-Oblique', fontSize=12, leading=18,
                             textColor=PURPLE, alignment=TA_CENTER)))
    story.append(sp(10))
    story.append(AccentBar(iw, GOLD))

    return story


# ─── Funções de fundo de página ──────────────────────────────────────────────
def draw_cover(c):
    c.setFillColor(DEEP_PURPLE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.setFillAlpha(0.35)
    c.rect(0, H * 0.35, W, H * 0.65, fill=1, stroke=0)
    c.setFillAlpha(1.0)
    c.setFillColor(GOLD)
    c.rect(0, H - 8 * mm, W, 4 * mm, fill=1, stroke=0)
    c.rect(0, 8 * mm, W, 4 * mm, fill=1, stroke=0)
    cx, cy = W / 2, H * 0.52
    for r, alpha in [(90, 0.06), (72, 0.09), (55, 0.13)]:
        c.setFillColor(WHITE)
        c.setFillAlpha(alpha)
        c.circle(cx, cy, r * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)
    c.setFillColor(GOLD)
    c.setFillAlpha(0.9)
    c.circle(cx, cy, 8 * mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)
    bw, bh = 80 * mm, 9 * mm
    bx = (W - bw) / 2
    c.setFillColor(GOLD)
    c.roundRect(bx, H - 28 * mm, bw, bh, 4 * mm, fill=1, stroke=0)
    c.setFillColor(DEEP_PURPLE)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, H - 28 * mm + 2.8 * mm, 'GUIA COMPLETO DE MANIFESTA\u00c7\u00c3O')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 36)
    c.drawCentredString(W / 2, H * 0.68, 'COMO MANIFESTAR')
    c.drawCentredString(W / 2, H * 0.61, 'A VIDA DOS')
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 42)
    c.drawCentredString(W / 2, H * 0.53, 'SONHOS')
    c.setFillColor(WHITE)
    c.setFillAlpha(0.85)
    c.setFont('Helvetica-Oblique', 13)
    c.drawCentredString(W / 2, H * 0.43, 'T\u00e9cnicas poderosas de inten\u00e7\u00e3o, f\u00e9 e a\u00e7\u00e3o')
    c.drawCentredString(W / 2, H * 0.40, 'para co-criar a realidade que voc\u00ea merece')
    c.setFillAlpha(1.0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(LM + 20 * mm, H * 0.36, W - LM - 20 * mm, H * 0.36)
    c.setFillColor(WHITE)
    c.setFillAlpha(0.6)
    c.setFont('Helvetica', 10)
    c.drawCentredString(W / 2, 18 * mm, 'Transforme pensamentos em realidade')
    c.setFillAlpha(1.0)


def draw_inner(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(LAVENDER)
    c.rect(0, 0, 4 * mm, H, fill=1, stroke=0)
    c.setFillColor(DEEP_PURPLE)
    c.rect(0, H - TM, W, TM, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(LM, H - TM + 7 * mm, 'GUIA DE MANIFESTA\u00c7\u00c3O')
    c.setFillColor(WHITE)
    c.setFillAlpha(0.7)
    c.setFont('Helvetica', 8)
    c.drawRightString(W - RM, H - TM + 7 * mm, 'Como Manifestar a Vida dos Sonhos')
    c.setFillAlpha(1.0)
    page_num = c.getPageNumber()
    if page_num > 2:
        c.setFillColor(MID_GRAY)
        c.setFont('Helvetica', 8)
        c.drawCentredString(W / 2, 10 * mm, str(page_num - 2))


# ─── Build PDF ────────────────────────────────────────────────────────────────
def build_pdf(output='ebook_manifestacao_v2.pdf'):
    doc = BaseDocTemplate(
        output,
        pagesize=A4,
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

    story = []
    story += build_content(IW)

    doc.build(story)
    print(f'PDF gerado: {output}')


if __name__ == '__main__':
    build_pdf('ebook_manifestacao_v2.pdf')
