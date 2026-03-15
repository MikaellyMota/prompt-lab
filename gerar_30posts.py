# -*- coding: utf-8 -*-
"""Gerador do Prompt Lab - Crie 30 Posts em 1 Hora com IA (v2)"""
import sys
sys.path.insert(0, r'C:\PromptLab\Lib\site-packages')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                 Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, KeepTogether, NextPageTemplate)
from reportlab.platypus.flowables import Flowable

W, H = A4
LM = RM = 20 * mm
TM = 22 * mm
BM = 20 * mm
CW = W - LM - RM
CH = H - TM - BM

# ─── Paleta ──────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#0D1B2A')
NAVY2     = colors.HexColor('#142030')
PINK      = colors.HexColor('#EC4899')
PINK2     = colors.HexColor('#BE185D')
LIGHT_PINK= colors.HexColor('#FDF2F8')
GOLD      = colors.HexColor('#F4A026')
LIGHT_GOLD= colors.HexColor('#FFF3DC')
PURPLE    = colors.HexColor('#8B5CF6')
BLUE      = colors.HexColor('#1E6FFF')
GREEN     = colors.HexColor('#10B981')
SOFT_GRAY = colors.HexColor('#F5F5F5')
MID_GRAY  = colors.HexColor('#888888')
DARK_TEXT = colors.HexColor('#1A1A1A')
WHITE     = colors.white

ACCENT = PINK   # cor principal deste ebook

# Cores dos 4 tipos de post
TYPE_COLORS = {
    'educativo':   colors.HexColor('#1E6FFF'),
    'engajamento': colors.HexColor('#8B5CF6'),
    'bastidores':  colors.HexColor('#F59E0B'),
    'venda':       colors.HexColor('#EF4444'),
}

def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY   = S('body',  fontName='Helvetica', fontSize=11, leading=17,
           textColor=DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=7)
BODYB  = S('bodyb', fontName='Helvetica-Bold', fontSize=11, leading=17,
           textColor=DARK_TEXT)
INTRO_H = S('introh', fontName='Helvetica-Bold', fontSize=26, leading=32,
            textColor=NAVY, spaceAfter=4)
HIGHLIGHT = S('hl', fontName='Helvetica-Bold', fontSize=11, leading=16,
              textColor=NAVY, leftIndent=8, rightIndent=8)


# ─── FullPage base ────────────────────────────────────────────────────────────
class FullPage(Flowable):
    def wrap(self, avW, avH):
        return avW, avH

    def _c(self):
        c = self.canv
        c.saveState()
        c.resetTransforms()
        return c

    def _done(self):
        self.canv.restoreState()


# ─── CAPA ─────────────────────────────────────────────────────────────────────
class CoverPage(FullPage):
    def draw(self):
        c = self._c()
        # Fundo
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # Decoracao
        c.setFillColor(NAVY2)
        c.circle(W * 1.05, H * 0.72, W * 0.52, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#0A1825'))
        c.circle(-W * 0.1, H * 0.18, W * 0.38, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#1A0D20'))
        c.circle(W * 0.5, H * 0.96, W * 0.22, fill=1, stroke=0)
        # Linhas rosa topo/rodape
        c.setStrokeColor(ACCENT)
        c.setLineWidth(5)
        c.line(0, H - 7, W, H - 7)
        c.line(0, 7, W, 7)
        # Badge
        tw, th = 130, 26
        tx = (W - tw) / 2
        ty = H - 54
        c.setFillColor(ACCENT)
        c.roundRect(tx, ty, tw, th, 7, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(W / 2, ty + 8, 'E-BOOK PREMIUM')
        # Numero destaque
        c.setFillColor(ACCENT)
        c.setFont('Helvetica-Bold', 100)
        c.drawCentredString(W / 2, H * 0.64, '30')
        # Titulo
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 36)
        c.drawCentredString(W / 2, H * 0.53, 'POSTS')
        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(W / 2, H * 0.47, 'EM 1 HORA COM IA')
        # Faixa
        fy = H * 0.38
        fh = 52
        c.setFillColor(ACCENT)
        c.rect(0, fy, W, fh, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(W / 2, fy + 32, 'O guia completo para crescer no Instagram')
        c.setFont('Helvetica', 11)
        c.drawCentredString(W / 2, fy + 14, 'sem perder horas criando conteudo')
        # Chips
        chips = ['Prompts Prontos', 'Templates', 'Passo a Passo', 'Bonus']
        chip_colors = [BLUE, PURPLE, GREEN, GOLD]
        total_w = W - 40
        cw2 = total_w / len(chips)
        cy2 = H * 0.29
        for i, (chip, cc) in enumerate(zip(chips, chip_colors)):
            bx = 20 + i * cw2
            c.setFillColor(cc)
            c.roundRect(bx, cy2, cw2 - 6, 22, 5, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 8)
            c.drawCentredString(bx + (cw2 - 6) / 2, cy2 + 7, chip)
        # Compatibilidade
        c.setFillColor(colors.HexColor('#99AABB'))
        c.setFont('Helvetica', 9)
        c.drawCentredString(W / 2, H * 0.24,
                            'Compativel com ChatGPT  |  Claude  |  Gemini  |  Copilot')
        # Rodape
        c.setFillColor(colors.HexColor('#AABBCC'))
        c.setFont('Helvetica', 10)
        c.drawCentredString(W / 2, 18, 'by Prompt Lab')
        self._done()


# ─── SUMARIO ─────────────────────────────────────────────────────────────────
class TOCPage(FullPage):
    def draw(self):
        c = self._c()
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(NAVY2)
        c.circle(W * 0.9, H * 0.12, W * 0.32, fill=1, stroke=0)

        margin = LM
        c.setFillColor(ACCENT)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(margin, H - 30 * mm, 'INDICE DE CONTEUDO')
        c.setStrokeColor(ACCENT)
        c.setLineWidth(2)
        c.line(margin, H - 32.5 * mm, W - margin, H - 32.5 * mm)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 36)
        c.drawString(margin, H - 52 * mm, 'Sumario')

        items = [
            ('01', 'O Metodo dos 30 Posts',           'A estrutura que funciona',       '#EC4899', '04'),
            ('02', 'Prompts para 30 Ideias',          '5 prompts geradores de conteudo','#1E6FFF', '05'),
            ('03', '10 Templates de Legenda',         'Copie, edite e publique',        '#8B5CF6', '06'),
            ('04', 'Passo a Passo: 1 Hora',           'Do zero ao agendado',            '#10B981', '08'),
            ('+',  'Bonus: Nunca Mais Travar',        '4 prompts de emergencia',        '#F4A026', '09'),
        ]
        y = H - 66 * mm
        for num, name, detail, cc, pg in items:
            c.setFillColor(colors.HexColor(cc))
            c.roundRect(margin, y - 4, 30, 24, 5, fill=1, stroke=0)
            c.setFillColor(WHITE if num != '+' else NAVY)
            c.setFont('Helvetica-Bold', 12)
            c.drawCentredString(margin + 15, y + 4, num)
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 13)
            c.drawString(margin + 38, y + 6, name)
            c.setFillColor(colors.HexColor(cc))
            c.setFont('Helvetica', 9.5)
            c.drawString(margin + 38, y - 6, detail)
            c.setStrokeColor(colors.HexColor('#2A3F55'))
            c.setLineWidth(0.5)
            c.setDash(2, 4)
            nw = margin + 38 + c.stringWidth(name, 'Helvetica-Bold', 13) + 12
            c.line(nw, y + 10, W - margin - 35, y + 10)
            c.setDash()
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 11)
            c.drawRightString(W - margin, y + 6, f'pag. {pg}')
            y -= 38
        self._done()


# ─── CABECALHO DE SECAO ───────────────────────────────────────────────────────
class SectionHeader(FullPage):
    def __init__(self, num, title, subtitle, color):
        super().__init__()
        self.num = num
        self.title = title
        self.subtitle = subtitle
        self.color = color

    def draw(self):
        c = self._c()
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(self.color)
        c.rect(0, 0, 10, H, fill=1, stroke=0)
        c.setFillColor(NAVY2)
        c.circle(W * 0.85, H * 0.5, H * 0.38, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#0A1825'))
        c.circle(W * 0.75, H * 0.15, H * 0.18, fill=1, stroke=0)
        margin = LM + 10
        c.setFillColor(self.color)
        c.roundRect(margin, H * 0.56, 44, 44, 10, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(margin + 22, H * 0.56 + 13, self.num)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 32)
        c.drawString(margin, H * 0.44, self.title)
        c.setStrokeColor(self.color)
        c.setLineWidth(3)
        tw = c.stringWidth(self.title, 'Helvetica-Bold', 32)
        c.line(margin, H * 0.41, margin + min(tw, W - margin * 2), H * 0.41)
        c.setFillColor(colors.HexColor('#AABBCC'))
        c.setFont('Helvetica', 13)
        c.drawString(margin, H * 0.35, self.subtitle)
        c.setFillColor(colors.HexColor('#1A2E45'))
        c.setFont('Helvetica-Bold', 160)
        c.drawCentredString(W * 0.8, H * 0.14, self.num)
        self._done()


# ─── ENCERRAMENTO ─────────────────────────────────────────────────────────────
class ClosingPage(FullPage):
    def draw(self):
        c = self._c()
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(NAVY2)
        c.circle(W * 0.9, H * 0.8, W * 0.4, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#0A1825'))
        c.circle(W * 0.1, H * 0.2, W * 0.3, fill=1, stroke=0)
        c.setStrokeColor(ACCENT)
        c.setLineWidth(5)
        c.line(0, H - 7, W, H - 7)
        c.line(0, 7, W, 7)
        # Icone
        c.setFillColor(ACCENT)
        c.circle(W / 2, H * 0.75, 32, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 26)
        c.drawCentredString(W / 2, H * 0.75 - 10, '\u2713')
        # Titulo
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 30)
        c.drawCentredString(W / 2, H * 0.63, 'Voce nunca mais vai travar!')
        c.setFillColor(ACCENT)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(W / 2, H * 0.58, '30 posts. 1 hora. Toda semana.')
        c.setStrokeColor(colors.HexColor('#2A3F55'))
        c.setLineWidth(1)
        c.line(W * 0.2, H * 0.55, W * 0.8, H * 0.55)
        # Texto
        lines = [
            'A IA faz o trabalho pesado.',
            'Voce so decide, edita e publica.',
            '',
            'Consistencia e o segredo do crescimento',
            '— e agora voce nao tem mais desculpa.',
        ]
        c.setFillColor(colors.HexColor('#AABBCC'))
        c.setFont('Helvetica', 11.5)
        y = H * 0.50
        for line in lines:
            c.drawCentredString(W / 2, y, line)
            y -= 17
        # CTA
        cx, cy2 = W * 0.15, H * 0.29
        cw2, ch = W * 0.70, 54
        c.setFillColor(ACCENT)
        c.roundRect(cx, cy2, cw2, ch, 10, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(W / 2, cy2 + 34, 'Compartilhe com alguem que precisa disso!')
        c.setFont('Helvetica', 11)
        c.drawCentredString(W / 2, cy2 + 16, 'Ajude mais pessoas a crescerem no Instagram.')
        # Logo
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(W / 2, H * 0.15, 'PROMPT LAB')
        c.setFillColor(colors.HexColor('#555555'))
        c.setFont('Helvetica', 8.5)
        c.drawCentredString(W / 2, H * 0.09,
                            '\u00a9 2025 Prompt Lab. Todos os direitos reservados.')
        self._done()


# ─── Decorador paginas de conteudo ───────────────────────────────────────────
def page_deco(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 18, W, 18, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(LM, H - 12, 'PROMPT LAB')
    canvas.setFillColor(colors.HexColor('#AAAAAA'))
    canvas.setFont('Helvetica', 7)
    canvas.drawRightString(W - RM, H - 12, 'Crie 30 Posts em 1 Hora com IA')
    canvas.setFillColor(SOFT_GRAY)
    canvas.rect(0, 0, W, 16, fill=1, stroke=0)
    canvas.setFillColor(MID_GRAY)
    canvas.setFont('Helvetica', 7)
    canvas.drawCentredString(W / 2, 5, f'- {doc.page} -')
    canvas.setFillColor(colors.HexColor('#BBBBBB'))
    canvas.setFont('Helvetica', 6.5)
    canvas.drawString(LM, 5, 'promptlab.digital')
    canvas.restoreState()


# ─── Bloco de prompt ─────────────────────────────────────────────────────────
def prompt_block(num_str, title, prompt_text, tip_text, color=ACCENT):
    col_w = CW
    num_p = Paragraph(f'<b>{num_str}</b>',
                       S('pn', fontName='Helvetica-Bold', fontSize=11,
                         textColor=WHITE, alignment=TA_CENTER, leading=14))
    title_p = Paragraph(f'<b>{title}</b>',
                         S('pt', fontName='Helvetica-Bold', fontSize=11,
                           textColor=color, leading=14))
    prompt_p = Paragraph(
        f'<i>\u201c{prompt_text}\u201d</i>',
        S('pp', fontName='Helvetica-Oblique', fontSize=10.5, leading=15,
          textColor=DARK_TEXT))

    num_w = 30
    top = Table([[num_p, [title_p, Spacer(1, 3), prompt_p]]],
                colWidths=[num_w, col_w - num_w])
    top.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), color),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#FDF2F8')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (0, 0), 4),
        ('RIGHTPADDING', (0, 0), (0, 0), 4),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
    ]))

    tip_l = Paragraph('\u26a1 DICA DE USO:',
                       S('tl', fontName='Helvetica-Bold', fontSize=8.5,
                         textColor=color, leading=11))
    tip_p2 = Paragraph(tip_text,
                        S('tp', fontName='Helvetica', fontSize=9.5,
                          textColor=colors.HexColor('#444444'), leading=13))
    tip = Table([[tip_l], [tip_p2]], colWidths=[col_w])
    tip.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SOFT_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    outer = Table([[top], [tip]], colWidths=[col_w])
    outer.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD')),
    ]))
    return KeepTogether([outer, Spacer(1, 5 * mm)])


# ─── Bloco de template ───────────────────────────────────────────────────────
def template_block(num, title, lines, color):
    col_w = CW
    header = Table([[
        Paragraph(f'<b>T{num}</b>',
                   S('tn', fontName='Helvetica-Bold', fontSize=12,
                     textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(f'<b>{title}</b>',
                   S('tt', fontName='Helvetica-Bold', fontSize=13,
                     textColor=WHITE)),
    ]], colWidths=[32, col_w - 32])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('LEFTPADDING', (0, 0), (0, 0), 6),
        ('RIGHTPADDING', (0, 0), (0, 0), 6),
        ('LEFTPADDING', (1, 0), (1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    content_rows = []
    for line in lines:
        content_rows.append([Paragraph(
            line,
            S('tl2', fontName='Helvetica-Oblique' if line.startswith('[') else 'Helvetica',
              fontSize=10.5, leading=15,
              textColor=colors.HexColor('#555555') if line.startswith('[') else DARK_TEXT)
        )])

    content = Table(content_rows, colWidths=[col_w])
    content.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SOFT_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))

    outer = Table([[header], [content]], colWidths=[col_w])
    outer.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD')),
    ]))
    return KeepTogether([outer, Spacer(1, 4 * mm)])


# ─── Secao inline header ──────────────────────────────────────────────────────
def sec_header(num, title, color):
    num_p = Paragraph(f'<b>{num}</b>',
                       S('sh', fontName='Helvetica-Bold', fontSize=12,
                         textColor=WHITE, alignment=TA_CENTER))
    title_p = Paragraph(f'<b>{title}</b>',
                         S('sht', fontName='Helvetica-Bold', fontSize=16,
                           textColor=WHITE))
    t = Table([[num_p, title_p]], colWidths=[32, CW - 32])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('LEFTPADDING', (0, 0), (0, 0), 6),
        ('LEFTPADDING', (1, 0), (1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def highlight_box(text, border_color=ACCENT):
    t = Table([[Paragraph(text, HIGHLIGHT)]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GOLD),
        ('BOX', (0, 0), (-1, -1), 2, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    return t


# ─── Conteudo ─────────────────────────────────────────────────────────────────
def intro_story():
    s = []
    s.append(Spacer(1, 8 * mm))
    s.append(Paragraph('Chega de travar na hora de postar.', INTRO_H))

    bar = Flowable.__new__(Flowable)

    class Bar(Flowable):
        def __init__(self, w, col, h=3):
            super().__init__()
            self.width = w
            self.col = col
            self.height = h + 2
        def wrap(self, *a): return self.width, self.height
        def draw(self):
            self.canv.setFillColor(self.col)
            self.canv.rect(0, 0, self.width, self.height - 2, fill=1, stroke=0)

    s.append(Bar(CW, ACCENT, 3))
    s.append(Spacer(1, 6 * mm))

    s.append(Paragraph(
        'Voce ja ficou travado na frente do celular sem saber o que postar? '
        'Abriu o Instagram, fechou, abriu de novo e nao publicou nada?',
        BODY))
    s.append(Paragraph('<b>Isso acaba aqui.</b>', BODYB))
    s.append(Spacer(1, 3 * mm))

    s.append(highlight_box(
        '\u2605  Com Inteligencia Artificial, voce consegue criar '
        '<b>30 posts completos — com texto, legenda e hashtags — em menos de 1 hora.</b> '
        'Nao importa se voce e empreendedor, criador de conteudo ou quer crescer seu perfil pessoal.',
        ACCENT))
    s.append(Spacer(1, 5 * mm))

    s.append(Paragraph(
        'Neste guia voce vai encontrar prompts prontos para gerar ideias, '
        'templates de legendas editaveis e um passo a passo completo para '
        '<b>nunca mais ficar sem conteudo.</b>',
        BODY))

    # Grid do que voce recebe
    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph('<b>O que voce vai receber:</b>', BODYB))
    s.append(Spacer(1, 3 * mm))

    items = [
        ('📋', 'Prompts Prontos', 'Para gerar 30 ideias em minutos', BLUE),
        ('✏️', '10 Templates', 'Copie, edite e publique', PURPLE),
        ('⏱️', 'Passo a Passo', 'Do zero ao agendado em 1 hora', GREEN),
        ('🎁', 'Bonus', '4 prompts para nunca mais travar', GOLD),
    ]
    cw_each = CW / 4
    cells = [[
        Paragraph(f'<b>{em}</b>',
                   S('gi', fontName='Helvetica-Bold', fontSize=18,
                     textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(f'<b>{name}</b>',
                   S('gn', fontName='Helvetica-Bold', fontSize=10,
                     textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(desc,
                   S('gd', fontName='Helvetica', fontSize=8.5,
                     textColor=colors.HexColor('#DDDDFF'), alignment=TA_CENTER)),
    ] for em, name, desc, col in items]

    grid = Table(
        [[cells[i][0] for i in range(4)],
         [cells[i][1] for i in range(4)],
         [cells[i][2] for i in range(4)]],
        colWidths=[cw_each] * 4,
        rowHeights=[28, 22, 20]
    )
    ts = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ])
    for i, (_, _, _, col) in enumerate(items):
        ts.add('BACKGROUND', (i, 0), (i, 2), col)
    grid.setStyle(ts)
    s.append(grid)

    s.append(Spacer(1, 7 * mm))
    s.append(Paragraph(
        '<i>Menos tempo criando. Mais tempo crescendo.</i>',
        S('ic', fontName='Helvetica-Oblique', fontSize=12,
          textColor=MID_GRAY, alignment=TA_CENTER)))
    s.append(PageBreak())
    return s


def metodo_story():
    s = []
    s.append(sec_header('01', 'O Metodo dos 30 Posts', ACCENT))
    s.append(Spacer(1, 5 * mm))

    s.append(Paragraph(
        'Todo perfil de sucesso no Instagram usa 4 tipos de post. '
        'Antes de qualquer prompt, entenda a estrutura e distribua seus '
        '<b>30 posts mensais</b> assim:',
        BODY))
    s.append(Spacer(1, 3 * mm))

    rows = [
        (colors.HexColor('#1E6FFF'), '12', 'Posts Educativos',
         'Ensinam algo util para seu publico. Geram salvamentos e constroem autoridade. '
         'Sao os posts que fazem as pessoas te seguirem por mais.'),
        (colors.HexColor('#8B5CF6'), '8', 'Posts de Engajamento',
         'Geram comentarios, enquetes e interacoes. Alimentam o algoritmo e '
         'aumentam o alcance organico de todos os seus outros posts.'),
        (colors.HexColor('#F59E0B'), '6', 'Posts de Bastidores',
         'Mostram quem voce e por tras da tela. Geram conexao emocional, '
         'confianca e fazem o seguidor se identificar com voce.'),
        (colors.HexColor('#EF4444'), '4', 'Posts de Venda',
         'Oferecem seu produto ou servico de forma natural e estrategica. '
         'Com apenas 4 posts de venda, voce nao parece chato — parece profissional.'),
    ]

    for col, num, title2, desc in rows:
        num_p = Paragraph(f'<b>{num}</b>',
                           S('mn', fontName='Helvetica-Bold', fontSize=22,
                             textColor=WHITE, alignment=TA_CENTER, leading=26))
        title_p2 = Paragraph(f'<b>{title2}</b>',
                              S('mt', fontName='Helvetica-Bold', fontSize=13,
                                textColor=WHITE, leading=16))
        desc_p = Paragraph(desc,
                            S('md', fontName='Helvetica', fontSize=10.5,
                              textColor=WHITE, leading=14))
        row_t = Table([[num_p, [title_p2, Spacer(1, 4), desc_p]]],
                      colWidths=[48, CW - 48])
        row_t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), col),
            ('LEFTPADDING', (0, 0), (0, 0), 8),
            ('RIGHTPADDING', (0, 0), (0, 0), 8),
            ('LEFTPADDING', (1, 0), (1, 0), 14),
            ('RIGHTPADDING', (1, 0), (1, 0), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        s.append(KeepTogether([row_t, Spacer(1, 4 * mm)]))

    s.append(Spacer(1, 2 * mm))
    s.append(highlight_box(
        'Essa distribuicao mantem seu perfil <b>ativo, humano e lucrativo</b> ao mesmo tempo. '
        'Agora vamos para os prompts que geram tudo isso automaticamente.',
        ACCENT))
    s.append(PageBreak())
    return s


def prompts_story():
    s = []
    s.append(sec_header('02', 'Prompts para Gerar 30 Ideias', BLUE))
    s.append(Spacer(1, 5 * mm))
    s.append(Paragraph(
        'Use estes 5 prompts no ChatGPT, Claude ou Gemini. '
        'Em menos de 10 minutos voce tem ideias suficientes para o mes inteiro.',
        BODY))
    s.append(Spacer(1, 4 * mm))

    prompts = [
        ('01', 'Gerador de ideias em massa',
         'Voce e um estrategista de conteudo especialista em Instagram. Crie 30 ideias de posts para um perfil de [seu nicho] voltado para [seu publico]. Distribua em 4 categorias: 12 educativos, 8 de engajamento, 6 de bastidores e 4 de venda. Para cada ideia: escreva o tema em uma linha, o tipo de post entre parenteses e o formato ideal (foto, carrossel, reels ou stories).',
         'Cole no ChatGPT com seu nicho preenchido. Voce recebe 30 ideias formatadas e categorizadas em segundos. So escolher as melhores.'),

        ('02', 'Transformar ideia em post completo',
         'Pegue a ideia "[cole a ideia escolhida]" e desenvolva um post completo para Instagram com: gancho poderoso na primeira linha (max. 10 palavras), desenvolvimento em 3 topicos curtos com 1 linha cada, chamada para acao clara no final e sugestao de 1 emoji estrategico para o gancho. Tom: [informal/formal/inspirador]. Adapte para o formato [foto/carrossel/reels].',
         'Use este prompt logo apos o Prompt 1. Transforma qualquer ideia em rascunho completo pronto para editar. Especificar o tom e o formato muda completamente o resultado.'),

        ('03', 'Criar serie de conteudo',
         'Crie uma serie de 5 posts conectados sobre [tema], onde cada post funciona sozinho mas juntos contam uma historia ou aprofundam um assunto. Para cada post inclua: o gancho de abertura, o ponto principal em 2 linhas e uma frase de transicao que incentive o seguidor a acompanhar o proximo post da serie.',
         'Series criam antecipacao e aumentam o tempo de visita no perfil. O seguidor que acompanha uma serie tem 3x mais chance de se tornar cliente.'),

        ('04', 'Gerar debate nos comentarios',
         'Crie um post de opiniao sobre [tema] que gere debate saudavel nos comentarios sem ser polemico ou ofensivo. O post deve: defender um ponto de vista claro e especifico, apresentar 2 argumentos objetivos, antecipar 1 contraargumento e terminar com uma pergunta aberta que convide respostas. Tom: confiante mas respeitoso.',
         'Posts de opiniao bem estruturados geram em media 3x mais comentarios. A pergunta no final e o que transforma leitura em interacao.'),

        ('05', 'Post carrossel completo',
         'Crie um carrossel de 7 slides sobre [tema] para Instagram. Slide 1: titulo com gancho irresistivel que faca o usuario querer arrastar (use numeros ou promessa de revelacao). Slides 2 a 6: um ponto por slide com titulo em negrito, explicacao em 2 linhas e um exemplo pratico em 1 linha. Slide 7: conclusao com o insight principal e CTA especifico (ex: "salva esse post" ou "comenta aqui"). Linguagem direta para iniciantes.',
         'Carrosseis tem a maior taxa de salvamento do Instagram — otimos para crescimento organico. O gancho do Slide 1 e o que decide se o usuario arrasta ou ignora.'),
    ]

    for num, title2, text, tip in prompts:
        s.append(prompt_block(num, title2, text, tip, BLUE))

    s.append(PageBreak())
    return s


def templates_story():
    s = []
    s.append(sec_header('03', '10 Templates de Legenda', PURPLE))
    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph(
        'Copie o template, substitua os colchetes com seu conteudo e publique. '
        'Os textos em <i>italico</i> sao os campos que voce edita.',
        BODY))
    s.append(Spacer(1, 4 * mm))

    TEMPL_COLORS = [
        colors.HexColor('#1E6FFF'),  # T1
        colors.HexColor('#8B5CF6'),  # T2
        colors.HexColor('#10B981'),  # T3
        colors.HexColor('#F59E0B'),  # T4
        colors.HexColor('#EC4899'),  # T5
        colors.HexColor('#EF4444'),  # T6
        colors.HexColor('#1E6FFF'),  # T7
        colors.HexColor('#8B5CF6'),  # T8
        colors.HexColor('#10B981'),  # T9
        colors.HexColor('#F59E0B'),  # T10
    ]

    templates = [
        ('1', 'Educativo',
         ['Voce sabia que [fato surpreendente]?',
          'A maioria das pessoas faz [erro comum] sem perceber.',
          '',
          'O que funciona de verdade e [solucao simples].',
          '',
          'Salva esse post para nao esquecer. \u2193']),

        ('2', 'Lista',
         ['[Numero] coisas que [seu publico] precisa parar de fazer agora:',
          '',
          '\u2192 [item 1]',
          '\u2192 [item 2]',
          '\u2192 [item 3]',
          '\u2192 [item 4]',
          '',
          'Qual desses voce se identificou? Comenta aqui \u2193']),

        ('3', 'Storytelling',
         ['Ha [tempo], eu [situacao dificil].',
          'Parecia que [o problema].',
          '',
          'Ate que eu descobri [virada].',
          '',
          'Hoje [resultado positivo].',
          '',
          'Se voce tambem [identificacao com o publico], esse post e pra voce.']),

        ('4', 'Pergunta de Engajamento',
         ['Responde com honestidade:',
          '',
          'Voce prefere [opcao A] ou [opcao B]?',
          '',
          'Nao tem resposta certa \u2014 so quero entender melhor',
          'quem me acompanha.',
          '',
          'Comenta aqui \u2193']),

        ('5', 'Bastidores',
         ['O que ninguem mostra sobre [sua area]:',
          '',
          '\u2022 [Verdade 1 que surpreende]',
          '\u2022 [Verdade 2 que surpreende]',
          '\u2022 [Verdade 3 que surpreende]',
          '',
          'Agora voce sabe. Compartilha com alguem que precisa ver isso.']),

        ('6', 'Dica Rapida',
         ['Dica de [tema] que mudou meu jogo:',
          '',
          '[Dica em 2 linhas simples e diretas]',
          '',
          'Simples assim. Salva e aplica hoje. \u2193']),

        ('7', 'Mito vs. Verdade',
         ['MITO: [crenca errada comum no seu nicho]',
          '',
          'VERDADE: [o que realmente funciona]',
          '',
          'A maioria ainda acredita no mito',
          '\u2014 e perde [resultado concreto] por isso.',
          '',
          'Marca alguem que precisa saber disso \u2193']),

        ('8', 'Resultado',
         ['Em [periodo de tempo], eu consegui [resultado especifico].',
          'Sem [obstaculo que as pessoas temem].',
          '',
          'O que fiz foi [metodo simples em 1 linha].',
          '',
          'Quer saber o passo a passo completo?',
          'Comenta SIM aqui \u2193']),

        ('9', 'Venda Sutil',
         ['Se voce pudesse [beneficio desejado] em [prazo curto], faria?',
          '',
          'E exatamente isso que [seu produto/servico] entrega.',
          'Sem [principal dor ou obstaculo].',
          '',
          'Link na bio para saber mais. \u2192']),

        ('10', 'Frase de Impacto',
         ['"[Frase poderosa e original sobre seu nicho]"',
          '',
          'Para quem ainda acha que [crenca limitante do seu publico].',
          '',
          'Salva isso e rele quando precisar. \u2764']),
    ]

    for i, (num, title2, lines) in enumerate(templates):
        s.append(template_block(num, title2, lines, TEMPL_COLORS[i]))

    s.append(PageBreak())
    return s


def passoapasso_story():
    s = []
    s.append(sec_header('04', 'Passo a Passo: 30 Posts em 1 Hora', GREEN))
    s.append(Spacer(1, 5 * mm))

    steps = [
        (GREEN, '0\u201310 min', 'Geracao de Ideias',
         'Cole o Prompt 1 no ChatGPT com seu nicho preenchido. Voce recebe 30 ideias completas, '
         'ja categorizadas por tipo. Escolha as melhores, descarte as que nao fazem sentido '
         'e salve a lista no Notion ou bloco de notas.'),

        (BLUE, '10\u201335 min', 'Criacao das Legendas',
         'Para cada post: use o Prompt 2 para desenvolver o conteudo OU escolha um dos '
         '10 templates e edite com seu contexto. Em media leva 1 a 2 minutos por legenda. '
         'Em 25 minutos voce tem 30 legendas prontas.'),

        (PURPLE, '35\u201350 min', 'Hashtags Estrategicas',
         'Para cada post, use este prompt:\n'
         '"Sugira 15 hashtags para um post sobre [tema]: '
         '5 grandes (1M+), 5 medias (100K-500K) e 5 pequenas (10K-50K). '
         'Explique por que essa combinacao aumenta o alcance organico."\n'
         'Cole as hashtags no final de cada legenda.'),

        (ACCENT, '50\u201360 min', 'Revisao e Agendamento',
         'Releia rapidamente cada post, ajuste o tom se necessario e agende '
         'pelo proprio Instagram, Meta Business Suite ou agendadores como Buffer ou Later. '
         'Pronto: 30 posts agendados em 1 hora.'),
    ]

    for col, time, title2, desc in steps:
        time_p = Paragraph(f'<b>{time}</b>',
                            S('tp2', fontName='Helvetica-Bold', fontSize=11,
                              textColor=WHITE, alignment=TA_CENTER, leading=14))
        title_p2 = Paragraph(f'<b>{title2}</b>',
                              S('stp', fontName='Helvetica-Bold', fontSize=13,
                                textColor=WHITE, leading=16))
        desc_p2 = Paragraph(desc.replace('\n', '<br/>'),
                             S('std', fontName='Helvetica', fontSize=10.5,
                               textColor=WHITE, leading=14))
        row = Table([[time_p, [title_p2, Spacer(1, 5), desc_p2]]],
                    colWidths=[52, CW - 52])
        row.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), col),
            ('LEFTPADDING', (0, 0), (0, 0), 6),
            ('RIGHTPADDING', (0, 0), (0, 0), 6),
            ('LEFTPADDING', (1, 0), (1, 0), 14),
            ('RIGHTPADDING', (1, 0), (1, 0), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        s.append(KeepTogether([row, Spacer(1, 4 * mm)]))

    s.append(Spacer(1, 2 * mm))
    s.append(highlight_box(
        'Dica: use um timer. Sabendo que tem 10 minutos para ideias e 25 para legendas, '
        'voce foca e para de procrastinar. A restricao de tempo e uma aliada.',
        GREEN))
    s.append(PageBreak())
    return s


def bonus_story():
    s = []
    s.append(sec_header('+', 'Bonus: Nunca Mais Travar', GOLD))
    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph(
        'Guarde estes 4 prompts para os momentos de bloqueio criativo. '
        'Cada um resolve uma situacao especifica.',
        BODY))
    s.append(Spacer(1, 4 * mm))

    bonus = [
        ('B1', 'Quando nao souber o que postar',
         'Quais sao os 10 maiores medos, duvidas e frustracoes de [seu publico ideal] '
         'relacionados a [seu nicho]? Para cada um: sugira o formato de post ideal '
         '(carrossel, reels, foto ou stories), o gancho de abertura e por que esse tema '
         'gera engajamento com esse publico.',
         'Use sempre que a inspiracao acabar. Funciona para qualquer nicho porque parte '
         'das dores reais do seu publico, nao de suposicoes suas.'),

        ('B2', 'Quando quiser viralizar',
         'Analise os formatos de post que mais viralizam atualmente no Instagram para o '
         'nicho de [nicho]. Para cada formato: explique a estrutura que faz ele funcionar, '
         'o tipo de emocao que ele desperta (surpresa, identificacao, inspiracao) e crie '
         'um exemplo completo pronto para publicar adaptado ao meu publico de [publico].',
         'Nao coloque um ano especifico neste prompt — deixe a IA usar o conhecimento mais '
         'atual que ela tem. Atualize o nicho e o publico a cada vez que usar.'),

        ('B3', 'Quando quiser vender sem parecer chato',
         'Crie 3 formas diferentes de mencionar [produto/servico] em um post de Instagram '
         'sem soar como propaganda direta. Use estas 3 abordagens: '
         '1) Educativa (ensine algo e mencione o produto como ferramenta), '
         '2) Prova social (use resultado de cliente real ou hipotetico), '
         '3) Storytelling (conte uma historia onde o produto foi a virada). '
         'Para cada abordagem, entregue o post pronto para publicar.',
         'Ideal para quem tem medo de postar sobre venda e afastar seguidores. '
         'Com 4 posts de venda no mes, esse prompt gera os 3 de forma completamente diferente.'),

        ('B4', 'Quando quiser crescer rapido com alcance organico',
         'Crie um post de colaboracao para Instagram onde convido minha audiencia a marcar '
         'um amigo que [situacao especifica que identifica o publico, ex: quer aprender a '
         'investir / tem um pequeno negocio / esta aprendendo a cozinhar]. '
         'O post deve ser curto (max. 5 linhas), ter um elemento emocional ou de humor, '
         'e terminar com um CTA claro para marcar o amigo. Crie 3 versoes com tons diferentes.',
         'Posts de "marca um amigo" sao um dos metodos mais eficazes de alcance organico '
         'porque cada marcacao notifica uma nova pessoa. 3 versoes permitem testar qual tom '
         'funciona melhor para o seu publico.'),
    ]

    for num, title2, text, tip in bonus:
        s.append(prompt_block(num, title2, text, tip, GOLD))

    s.append(PageBreak())
    return s


# ─── Build ────────────────────────────────────────────────────────────────────
def build_pdf():
    output = r'c:\PromptLab\Prompt_Lab_30Posts_v2.pdf'

    doc = BaseDocTemplate(
        output,
        pagesize=A4,
        title='Prompt Lab - Crie 30 Posts em 1 Hora com IA',
        author='Prompt Lab',
        subject='Guia completo de conteudo para Instagram com IA',
        keywords='instagram posts prompts ia chatgpt conteudo redes sociais',
    )

    full_frame    = Frame(0, 0, W, H,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='full')
    content_frame = Frame(LM, BM, CW, CH,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='normal')

    doc.addPageTemplates([
        PageTemplate('cover',   [full_frame]),
        PageTemplate('toc',     [full_frame]),
        PageTemplate('sec',     [full_frame]),
        PageTemplate('content', [content_frame], onPage=page_deco),
        PageTemplate('closing', [full_frame]),
    ])

    story = []

    # Capa
    story.append(CoverPage())
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    # Intro
    story += intro_story()

    # Sumario
    story.append(NextPageTemplate('toc'))
    story.append(PageBreak())
    story.append(TOCPage())
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    # Secoes
    sections = [
        ('01', 'O Metodo dos 30 Posts', 'A estrutura que todo perfil de sucesso usa', ACCENT, metodo_story),
        ('02', 'Prompts para 30 Ideias', '5 prompts geradores de conteudo', BLUE, prompts_story),
        ('03', '10 Templates de Legenda', 'Copie, edite e publique', PURPLE, templates_story),
        ('04', 'Passo a Passo: 1 Hora', 'Do zero ao agendado em 60 minutos', GREEN, passoapasso_story),
        ('+',  'Bonus: Nunca Mais Travar', '4 prompts de emergencia criativa', GOLD, bonus_story),
    ]

    for num, title2, subtitle, col, func in sections:
        story.append(NextPageTemplate('sec'))
        story.append(PageBreak())
        story.append(SectionHeader(num, title2, subtitle, col))
        story.append(NextPageTemplate('content'))
        story.append(PageBreak())
        story += func()

    # Encerramento
    story.append(NextPageTemplate('closing'))
    story.append(PageBreak())
    story.append(ClosingPage())

    doc.build(story)
    print(f'PDF gerado: {output}')


if __name__ == '__main__':
    build_pdf()
