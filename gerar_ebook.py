# -*- coding: utf-8 -*-
"""Gerador do Prompt Lab Ebook v3 - versao para venda na Kiwifi R$19,90"""
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
CONTENT_W = W - LM - RM
CONTENT_H = H - TM - BM

# ─── Paleta ──────────────────────────────────────────────────────────────────
NAVY        = colors.HexColor('#0D1B2A')
NAVY2       = colors.HexColor('#142030')
NAVY3       = colors.HexColor('#1A2E45')
GOLD        = colors.HexColor('#F4A026')
LIGHT_GOLD  = colors.HexColor('#FFF3DC')
BLUE        = colors.HexColor('#1E6FFF')
LIGHT_BLUE  = colors.HexColor('#EBF3FF')
SOFT_GRAY   = colors.HexColor('#F5F5F5')
MID_GRAY    = colors.HexColor('#888888')
DARK_TEXT   = colors.HexColor('#1A1A1A')
WHITE       = colors.white

CAT_HEX = ['#1E6FFF', '#8B5CF6', '#10B981', '#F59E0B', '#EC4899', '#EF4444']
CAT_COLORS = [colors.HexColor(h) for h in CAT_HEX]

# ─── Estilos ─────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY   = S('body',  fontName='Helvetica', fontSize=11, leading=17,
           textColor=DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=7)
BODYB  = S('bodyb', fontName='Helvetica-Bold', fontSize=11, leading=17,
           textColor=DARK_TEXT, alignment=TA_LEFT)
INTRO_H = S('introh', fontName='Helvetica-Bold', fontSize=26, leading=32,
            textColor=NAVY, alignment=TA_LEFT, spaceAfter=4)
HIGHLIGHT = S('hl', fontName='Helvetica-Bold', fontSize=11, leading=16,
              textColor=NAVY, alignment=TA_LEFT, leftIndent=8, rightIndent=8)
BULLET = S('bullet', fontName='Helvetica', fontSize=11, leading=16,
           textColor=DARK_TEXT, leftIndent=16, firstLineIndent=-10, spaceAfter=4)
BONUS_TITLE = S('bt', fontName='Helvetica-Bold', fontSize=15, leading=20,
                textColor=NAVY, alignment=TA_LEFT, spaceAfter=6)
BONUS_BODY  = S('bb', fontName='Helvetica', fontSize=10.5, leading=15,
                textColor=DARK_TEXT, alignment=TA_LEFT)
FORMULA = S('formula', fontName='Helvetica-Bold', fontSize=11, leading=16,
            textColor=NAVY, alignment=TA_CENTER)

# ─── Flowable auxiliar: linha colorida ───────────────────────────────────────
class ColorBar(Flowable):
    def __init__(self, w, color, h=3):
        super().__init__()
        self.width = w
        self.bar_color = color
        self.height = h + 2

    def wrap(self, *a):
        return self.width, self.height

    def draw(self):
        self.canv.setFillColor(self.bar_color)
        self.canv.rect(0, 0, self.width, self.height - 2, fill=1, stroke=0)


# ─── Flowable full-page (usa resetTransforms) ─────────────────────────────────
class FullPage(Flowable):
    """Base para flowables que desenham na pagina inteira."""
    def wrap(self, avW, avH):
        self._avW = avW
        self._avH = avH
        return avW, avH

    def draw(self):
        pass  # subclasses implementam

    def _page_canvas(self):
        """Retorna o canvas com transforms resetados para coordenadas de pagina."""
        c = self.canv
        c.saveState()
        c.resetTransforms()
        return c

    def _done(self):
        self.canv.restoreState()


# ─── CAPA ─────────────────────────────────────────────────────────────────────
class CoverPage(FullPage):
    def draw(self):
        c = self._page_canvas()

        # Fundo
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Decoracao geometrica
        c.setFillColor(NAVY2)
        c.circle(W * 1.05, H * 0.74, W * 0.52, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#0A1825'))
        c.circle(-W * 0.1, H * 0.18, W * 0.38, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#162535'))
        c.circle(W * 0.5, H * 0.95, W * 0.25, fill=1, stroke=0)

        # Linhas douradas topo/rodape
        c.setStrokeColor(GOLD)
        c.setLineWidth(5)
        c.line(0, H - 7, W, H - 7)
        c.line(0, 7, W, 7)

        # Tag premium
        tw, th = 120, 26
        tx = (W - tw) / 2
        ty = H - 54
        c.setFillColor(GOLD)
        c.roundRect(tx, ty, tw, th, 7, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(W / 2, ty + 8, 'E-BOOK PREMIUM')

        # Titulo PROMPT
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 70)
        c.drawCentredString(W / 2, H * 0.67, 'PROMPT')

        # Titulo LAB (dourado)
        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 70)
        c.drawCentredString(W / 2, H * 0.67 - 76, 'LAB')

        # Ponto decorativo
        c.setFillColor(GOLD)
        c.circle(W / 2, H * 0.67 - 94, 4, fill=1, stroke=0)

        # Faixa dourada central
        fy = H * 0.38
        fh = 56
        c.setFillColor(GOLD)
        c.rect(0, fy, W, fh, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 15)
        c.drawCentredString(W / 2, fy + 34, '50 Prompts de IA Prontos para Usar')
        c.setFont('Helvetica', 11)
        c.drawCentredString(W / 2, fy + 16, 'Do Zero ao Resultado  -  Sem Complicacao')

        # Badges de categoria
        cats = ['Trabalho', 'Estudos', 'Financas', 'Organizacao', 'Redes Sociais', 'Negocios']
        by = H * 0.29
        total_w = W - 40
        bw = total_w / len(cats)
        for i, (cat, cc) in enumerate(zip(cats, CAT_HEX)):
            bx = 20 + i * bw
            c.setFillColor(colors.HexColor(cc))
            c.roundRect(bx, by, bw - 5, 22, 5, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 7.5)
            c.drawCentredString(bx + (bw - 5) / 2, by + 7, cat)

        # IAs compativeis
        c.setFillColor(colors.HexColor('#99AABB'))
        c.setFont('Helvetica', 9)
        c.drawCentredString(W / 2, by - 16,
                            'Compativel com ChatGPT  |  Claude  |  Gemini  |  Copilot')

        # Rodape
        c.setFillColor(colors.HexColor('#AABBCC'))
        c.setFont('Helvetica', 10)
        c.drawCentredString(W / 2, 18, 'by Prompt Lab')

        self._done()


# ─── SUMARIO ─────────────────────────────────────────────────────────────────
class TOCPage(FullPage):
    def draw(self):
        c = self._page_canvas()

        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(NAVY2)
        c.circle(W * 0.9, H * 0.15, W * 0.35, fill=1, stroke=0)

        margin = LM
        # Label
        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(margin, H - 30 * mm, 'INDICE DE CONTEUDO')
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(margin, H - 32.5 * mm, W - margin, H - 32.5 * mm)

        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 36)
        c.drawString(margin, H - 52 * mm, 'Sumario')

        cats = [
            ('01', 'Trabalho e Produtividade',    '8 prompts', '#1E6FFF', '04'),
            ('02', 'Estudos e Aprendizado',       '8 prompts', '#8B5CF6', '06'),
            ('03', 'Financas Pessoais',           '8 prompts', '#10B981', '08'),
            ('04', 'Dia a Dia e Organizacao',     '9 prompts', '#F59E0B', '10'),
            ('05', 'Redes Sociais e Conteudo',    '9 prompts', '#EC4899', '12'),
            ('06', 'Negocios e Empreendedorismo', '8 prompts', '#EF4444', '15'),
            ('+',  'Bonus: Como Criar Seus Proprios Prompts', 'Dicas exclusivas', '#F4A026', '17'),
        ]

        y = H - 66 * mm
        row_h = 36
        for num, name, detail, cc, pg in cats:
            # Badge numero
            c.setFillColor(colors.HexColor(cc))
            c.roundRect(margin, y - 4, 30, 24, 5, fill=1, stroke=0)
            c.setFillColor(WHITE if num != '+' else NAVY)
            c.setFont('Helvetica-Bold', 12)
            c.drawCentredString(margin + 15, y + 4, num)

            # Nome
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 13)
            c.drawString(margin + 38, y + 6, name)

            # Detalhe
            c.setFillColor(colors.HexColor(cc))
            c.setFont('Helvetica', 9.5)
            c.drawString(margin + 38, y - 6, detail)

            # Pontos
            c.setStrokeColor(colors.HexColor('#2A3F55'))
            c.setLineWidth(0.5)
            c.setDash(2, 4)
            name_end = margin + 38 + c.stringWidth(name, 'Helvetica-Bold', 13) + 12
            c.line(name_end, y + 10, W - margin - 35, y + 10)
            c.setDash()

            # Pagina
            c.setFillColor(WHITE)
            c.setFont('Helvetica-Bold', 11)
            c.drawRightString(W - margin, y + 6, f'pag. {pg}')

            y -= row_h

        self._done()


# ─── CABECALHO DE CATEGORIA (pagina inteira) ──────────────────────────────────
class CatHeaderPage(FullPage):
    def __init__(self, num, title, subtitle, color):
        super().__init__()
        self.num = num
        self.title = title
        self.subtitle = subtitle
        self.color = color

    def draw(self):
        c = self._page_canvas()

        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Barra lateral
        c.setFillColor(self.color)
        c.rect(0, 0, 10, H, fill=1, stroke=0)

        # Circulo decorativo
        c.setFillColor(NAVY2)
        c.circle(W * 0.85, H * 0.5, H * 0.38, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#0A1825'))
        c.circle(W * 0.75, H * 0.15, H * 0.18, fill=1, stroke=0)

        margin = LM + 10

        # Badge numero
        c.setFillColor(self.color)
        c.roundRect(margin, H * 0.56, 44, 44, 10, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(margin + 22, H * 0.56 + 13, self.num)

        # Titulo
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 32)
        c.drawString(margin, H * 0.44, self.title)

        # Linha colorida
        c.setStrokeColor(self.color)
        c.setLineWidth(3)
        title_w = c.stringWidth(self.title, 'Helvetica-Bold', 32)
        c.line(margin, H * 0.41, margin + min(title_w, W - margin * 2), H * 0.41)

        # Subtitulo
        c.setFillColor(colors.HexColor('#AABBCC'))
        c.setFont('Helvetica', 13)
        c.drawString(margin, H * 0.35, self.subtitle)

        # Numero grande decorativo
        c.setFillColor(colors.HexColor('#1A2E45'))
        c.setFont('Helvetica-Bold', 200)
        c.drawCentredString(W * 0.78, H * 0.12, self.num)

        self._done()


# ─── PAGINA DE ENCERRAMENTO ──────────────────────────────────────────────────
class ClosingPageFlow(FullPage):
    def draw(self):
        c = self._page_canvas()

        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(NAVY2)
        c.circle(W * 0.9, H * 0.8, W * 0.4, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#0A1825'))
        c.circle(W * 0.1, H * 0.2, W * 0.3, fill=1, stroke=0)

        # Linhas douradas
        c.setStrokeColor(GOLD)
        c.setLineWidth(5)
        c.line(0, H - 7, W, H - 7)
        c.line(0, 7, W, 7)

        # Circulo check
        c.setFillColor(GOLD)
        c.circle(W / 2, H * 0.75, 32, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 26)
        c.drawCentredString(W / 2, H * 0.75 - 10, '\u2713')

        # Titulo
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 34)
        c.drawCentredString(W / 2, H * 0.63, 'Parabens!')

        c.setFillColor(GOLD)
        c.setFont('Helvetica-Bold', 14)
        c.drawCentredString(W / 2, H * 0.59, 'Voce chegou ao fim do Prompt Lab!')

        # Divisor
        c.setStrokeColor(colors.HexColor('#2A3F55'))
        c.setLineWidth(1)
        c.line(W * 0.2, H * 0.56, W * 0.8, H * 0.56)

        # Texto
        lines = [
            'Agora voce tem 50 prompts prontos para transformar',
            'sua relacao com a Inteligencia Artificial.',
            '',
            'Lembre-se: o segredo e usar, adaptar e criar.',
            'Cada prompt e um ponto de partida, nao um limite.',
        ]
        c.setFillColor(colors.HexColor('#AABBCC'))
        c.setFont('Helvetica', 11.5)
        y = H * 0.50
        for line in lines:
            c.drawCentredString(W / 2, y, line)
            y -= 17

        # CTA box
        cx, cy = W * 0.15, H * 0.29
        cw, ch = W * 0.70, 54
        c.setFillColor(GOLD)
        c.roundRect(cx, cy, cw, ch, 10, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(W / 2, cy + 34, 'Gostou? Compartilhe com alguem')
        c.setFont('Helvetica', 11)
        c.drawCentredString(W / 2, cy + 16, 'que tambem quer dominar a IA!')

        # Logo / preco
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(W / 2, H * 0.15, 'PROMPT LAB')
        c.setFillColor(colors.HexColor('#555555'))
        c.setFont('Helvetica', 8.5)
        c.drawCentredString(W / 2, H * 0.09,
                            '\u00a9 2025 Prompt Lab. Todos os direitos reservados.')

        self._done()


# ─── Decorador de paginas de conteudo ────────────────────────────────────────
def content_page_deco(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 18, W, 18, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(LM, H - 12, 'PROMPT LAB')
    canvas.setFillColor(colors.HexColor('#AAAAAA'))
    canvas.setFont('Helvetica', 7)
    canvas.drawRightString(W - RM, H - 12, '50 Prompts de IA Prontos para Usar')
    # Footer
    canvas.setFillColor(SOFT_GRAY)
    canvas.rect(0, 0, W, 16, fill=1, stroke=0)
    canvas.setFillColor(MID_GRAY)
    canvas.setFont('Helvetica', 7)
    canvas.drawCentredString(W / 2, 5, f'- {doc.page} -')
    canvas.setFillColor(colors.HexColor('#BBBBBB'))
    canvas.setFont('Helvetica', 6.5)
    canvas.drawString(LM, 5, 'promptlab.digital')
    canvas.drawRightString(W - RM, 5, 'promptlab.digital')
    canvas.restoreState()


# ─── Bloco de prompt ────────────────────────────────────────────────────────
def prompt_block(num, prompt_text, tip_text, cat_color):
    col_w = CONTENT_W

    # Linha do prompt
    num_p = Paragraph(
        f'<b>#{num:02d}</b>',
        S('pn', fontName='Helvetica-Bold', fontSize=11, textColor=WHITE,
          alignment=TA_CENTER, leading=14))

    prompt_p = Paragraph(
        f'<i>\u201c{prompt_text}\u201d</i>',
        S('pt', fontName='Helvetica-Oblique', fontSize=10.5, leading=15,
          textColor=DARK_TEXT, alignment=TA_LEFT))

    num_w = 30
    top_row = Table([[num_p, prompt_p]], colWidths=[num_w, col_w - num_w])
    top_row.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), cat_color),
        ('BACKGROUND', (1, 0), (1, 0), LIGHT_BLUE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (0, 0), 4),
        ('RIGHTPADDING', (0, 0), (0, 0), 4),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
    ]))

    # Linha da dica
    tip_label = Paragraph(
        '\u26a1 DICA DE USO:',
        S('tl', fontName='Helvetica-Bold', fontSize=8.5,
          textColor=cat_color, leading=11))
    tip_p = Paragraph(
        tip_text,
        S('tp', fontName='Helvetica', fontSize=9.5, leading=13,
          textColor=colors.HexColor('#444444'), alignment=TA_LEFT))

    tip_row = Table([[tip_label], [tip_p]], colWidths=[col_w])
    tip_row.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SOFT_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    outer = Table([[top_row], [tip_row]], colWidths=[col_w])
    outer.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD')),
    ]))
    return KeepTogether([outer, Spacer(1, 4 * mm)])


# ─── Cabecalho inline da secao ───────────────────────────────────────────────
def section_inline_header(num_str, title, color, n_prompts):
    num_p = Paragraph(f'<b>{num_str}</b>',
                       S('sin', fontName='Helvetica-Bold', fontSize=12,
                         textColor=WHITE, alignment=TA_CENTER))
    title_p = Paragraph(f'<b>{title}</b>',
                         S('sit', fontName='Helvetica-Bold', fontSize=16,
                           textColor=WHITE))
    detail_p = Paragraph(f'{n_prompts} prompts',
                          S('sid', fontName='Helvetica', fontSize=10, textColor=WHITE))
    t = Table([[num_p, [title_p, detail_p]]], colWidths=[32, CONTENT_W - 32])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('LEFTPADDING', (0, 0), (0, 0), 6),
        ('RIGHTPADDING', (0, 0), (0, 0), 6),
        ('LEFTPADDING', (1, 0), (1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


# ─── Pagina de introducao ───────────────────────────────────────────────────
def intro_story():
    s = []
    s.append(Spacer(1, 8 * mm))
    s.append(Paragraph('Bem-vindo ao Prompt Lab', INTRO_H))
    s.append(ColorBar(CONTENT_W, GOLD, 3))
    s.append(Spacer(1, 6 * mm))

    s.append(Paragraph(
        'Voce ja tentou usar o ChatGPT e sentiu que as respostas eram vagas ou genericas? '
        'Saiba que o problema <b>nunca e a ferramenta</b>. O problema e saber exatamente o que pedir.',
        BODY))

    s.append(Paragraph(
        'E exatamente isso que o <b>Prompt Lab</b> resolve.',
        BODY))

    hl = Table([[Paragraph(
        '&#9733;  Um <b>prompt</b> e a mensagem que voce digita para a IA. '
        'Quanto mais claro e especifico for o prompt, '
        '<b>mais poderosa e precisa sera a resposta.</b>',
        HIGHLIGHT)]], colWidths=[CONTENT_W])
    hl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GOLD),
        ('BOX', (0, 0), (-1, -1), 2, GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    s.append(hl)
    s.append(Spacer(1, 5 * mm))

    s.append(Paragraph(
        'Neste e-book voce vai encontrar <b>50 prompts avancados, prontos para copiar e usar</b>, '
        'organizados em 6 categorias do dia a dia. Cada prompt foi pensado para entregar um '
        'resultado especifico e poderoso, nao respostas genericas.',
        BODY))

    s.append(Paragraph(
        'Voce nao precisa ser tecnico. Basta copiar, colar, adaptar ao seu contexto '
        'e colher os resultados.',
        BODY))

    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph('<b>Funciona com todas as principais IAs:</b>', BODYB))
    s.append(Spacer(1, 3 * mm))

    tools = [
        ('ChatGPT', 'chat.openai.com', '#1E6FFF'),
        ('Claude', 'claude.ai', '#8B5CF6'),
        ('Gemini', 'gemini.google.com', '#1A73E8'),
        ('Copilot', 'copilot.microsoft.com', '#00897B'),
    ]
    cw = CONTENT_W / 4
    cells = []
    for name, url, tc in tools:
        cells.append([
            Paragraph(f'<b>{name}</b>',
                       S('tc', fontName='Helvetica-Bold', fontSize=11,
                         textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(url,
                       S('tc2', fontName='Helvetica', fontSize=8,
                         textColor=colors.HexColor('#CCDDFF'), alignment=TA_CENTER)),
        ])
    tool_t = Table([
        [cells[i][0] for i in range(4)],
        [cells[i][1] for i in range(4)],
    ], colWidths=[cw] * 4, rowHeights=[26, 18])
    ts = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])
    for i, (_, _, tc) in enumerate(tools):
        ts.add('BACKGROUND', (i, 0), (i, 1), colors.HexColor(tc))
    tool_t.setStyle(ts)
    s.append(tool_t)

    s.append(Spacer(1, 7 * mm))
    s.append(Paragraph(
        '<i>Bons prompts geram resultados extraordinarios. Vamos comecar.</i>',
        S('ic', fontName='Helvetica-Oblique', fontSize=12,
          textColor=MID_GRAY, alignment=TA_CENTER)))
    s.append(PageBreak())
    return s


# ─── Bonus ──────────────────────────────────────────────────────────────────
def bonus_story():
    s = []
    s.append(Spacer(1, 8 * mm))

    hdr = Table([[
        Paragraph('<b>BONUS EXCLUSIVO</b>',
                   S('bh1', fontName='Helvetica-Bold', fontSize=9,
                     textColor=GOLD, leading=12)),
        Paragraph('Como Criar Seus Proprios Prompts',
                   S('bh2', fontName='Helvetica-Bold', fontSize=20,
                     textColor=WHITE, leading=26)),
        Paragraph('O metodo dos 5 elementos para prompts irresistiveis',
                   S('bh3', fontName='Helvetica', fontSize=10,
                     textColor=colors.HexColor('#AABBCC'), leading=14)),
    ]], colWidths=[CONTENT_W])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    s.append(hdr)
    s.append(Spacer(1, 5 * mm))

    s.append(Paragraph(
        'Depois de usar os 50 prompts deste e-book, voce vai querer criar os seus proprios. '
        'Aqui esta o metodo que os especialistas usam:',
        BODY))

    elements = [
        ('1. FUNCAO  \u2014  Quem a IA deve ser',
         'Comece com "Aja como..." ou "Voce e um especialista em..."\n'
         '<i>Exemplo: "Aja como um copywriter especialista em e-commerce..."</i>'),
        ('2. CONTEXTO  \u2014  Qual e a situacao',
         'Explique o cenario com o maximo de detalhes relevantes.\n'
         '<i>Exemplo: "...estou lancando um curso online de fotografia para iniciantes..."</i>'),
        ('3. TAREFA  \u2014  O que voce quer',
         'Seja claro e direto sobre o resultado desejado.\n'
         '<i>Exemplo: "...crie 5 titulos irresistiveis para a pagina de vendas..."</i>'),
        ('4. FORMATO  \u2014  Como quer receber',
         'Especifique o formato de saida: lista, tabela, paragrafo, topicos.\n'
         '<i>Exemplo: "...no formato de lista com bullet points, maximo 10 palavras cada."</i>'),
        ('5. RESTRICOES  \u2014  O que evitar',
         'Diga o que NAO quer na resposta para refinar o resultado.\n'
         '<i>Exemplo: "Evite cliches. Use linguagem direta e objetiva."</i>'),
    ]

    for title_e, desc_e in elements:
        t = Table([
            [Paragraph(f'<b>{title_e}</b>',
                        S('et', fontName='Helvetica-Bold', fontSize=10.5,
                          textColor=NAVY, leading=14))],
            [Paragraph(desc_e, BONUS_BODY)],
        ], colWidths=[CONTENT_W])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), LIGHT_GOLD),
            ('BACKGROUND', (0, 1), (0, 1), WHITE),
            ('BOX', (0, 0), (-1, -1), 1, GOLD),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        s.append(t)
        s.append(Spacer(1, 3 * mm))

    s.append(Spacer(1, 3 * mm))
    formula = Table([[Paragraph(
        '<b>FORMULA:</b> "Aja como [FUNCAO]. [CONTEXTO]. [TAREFA]. '
        'Formato: [FORMATO]. Evite: [RESTRICOES]."',
        FORMULA)]], colWidths=[CONTENT_W])
    formula.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GOLD),
        ('BOX', (0, 0), (-1, -1), 2.5, GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    s.append(formula)
    s.append(PageBreak())
    return s


# ─── Dados das categorias ────────────────────────────────────────────────────
CATEGORIES = [
    {
        'num': '01', 'title': 'Trabalho e Produtividade',
        'subtitle': '8 prompts para turbinar sua carreira e comunicacao',
        'color': CAT_COLORS[0],
        'prompts': [
            (1,
             'Voce e um assistente executivo especialista em comunicacao corporativa. Leia o texto abaixo e entregue: 1) Resumo em exatamente 5 topicos objetivos com linguagem formal, 2) Campo "Pontos de acao" listando cada tarefa pendente com responsavel e prazo sugerido, 3) Campo "Decisoes tomadas" com o que ja foi definido. Texto: [cole aqui]',
             'Cole qualquer e-mail longo, ata de reuniao ou relatorio e receba um documento executivo estruturado em segundos, pronto para repassar a equipe.'),
            (2,
             'Escreva um e-mail profissional solicitando extensao de prazo para o projeto [nome do projeto]. Tom: proativo e responsavel, nunca defensivo. Estrutura obrigatoria: 1) Abertura reconhecendo o compromisso original, 2) Causa raiz do atraso (sem desculpas), 3) O que ja foi entregue e o percentual concluido, 4) Novo prazo com data exata e justificativa realista, 5) Paragrafo de comprometimento com as acoes preventivas para garantir a entrega no novo prazo.',
             'Demonstra maturidade profissional e responsabilidade. A diferenca entre um e-mail que gera desconfianca e um que fortalece sua reputacao.'),
            (3,
             'Aja como um coach de produtividade. Com base nas tarefas abaixo, crie um plano semanal usando a matriz de Eisenhower (urgente/importante). Classifique cada tarefa e sugira em qual dia executar: [liste as tarefas]',
             'Semana organizada por prioridade real, nao por urgencia falsa. Ideal para usar toda segunda-feira de manha.'),
            (4,
             'Voce e um editor profissional. Corrija gramatica, melhore a clareza e torne este texto mais direto e impactante sem alterar meu estilo pessoal. Apos a versao corrigida, explique as 3 principais melhorias feitas: [cole o texto]',
             'Texto melhorado mais aprendizado sobre sua propria escrita. Use para relatorios, e-mails e apresentacoes.'),
            (5,
             'Crie uma pauta completa para uma reuniao de 45 minutos sobre [tema]. Inclua: objetivo da reuniao, topicos com tempo estimado, responsavel por cada ponto e campo para anotacoes. Formato: tabela.',
             'Exemplo: tema = lancamento de produto. Voce recebe a pauta pronta com cronometro para cada topico.'),
            (6,
             'Transforme as anotacoes abaixo em um documento executivo organizado com: resumo em 3 linhas, topicos principais, decisoes tomadas e proximos passos com responsaveis e prazos: [cole as anotacoes]',
             'Rascunho de reuniao vira documento profissional em segundos. Excelente para enviar apos calls.'),
            (7,
             'Aja como especialista em produtividade baseado nos principios de Cal Newport e James Clear. Meu principal obstaculo no trabalho remoto e [ex: distracao com celular / procrastinacao / falta de foco]. Crie um protocolo em 3 blocos: BLOCO 1 - Rotina diaria com horarios especificos e sessoes de foco cronometradas; BLOCO 2 - Top 5 ferramentas com instrucao pratica de como usar cada uma contra esse obstaculo; BLOCO 3 - Os 3 gatilhos mentais que causam esse problema e a tecnica exata para neutralizar cada um.',
             'Preencha o obstaculo com o que mais te paralisa hoje. O resultado e um protocolo cirurgico, nao uma lista generica de "dicas de produtividade".'),
            (8,
             'Voce e um especialista em comunicacao nao-violenta. Escreva uma resposta profissional e empatica para este e-mail dificil, preservando o relacionamento sem ceder a pressao: [cole o e-mail]. Tom: firme, respeitoso e solucionador.',
             'Ideal para responder cobrancas, criticas ou conflitos no trabalho sem criar mais atritos.'),
        ]
    },
    {
        'num': '02', 'title': 'Estudos e Aprendizado',
        'subtitle': '8 prompts para aprender mais rapido e com mais profundidade',
        'color': CAT_COLORS[1],
        'prompts': [
            (9,
             'Explique [tema] usando uma analogia do cotidiano para alguem que nunca teve contato com o assunto. Depois, de 3 exemplos praticos do mundo real onde esse conceito aparece.',
             'Exemplo: tema = juros compostos. Voce recebe uma analogia com bola de neve e 3 exemplos financeiros reais.'),
            (10,
             'Crie uma prova simulada com 10 questoes de multipla escolha sobre [tema], com 4 alternativas cada. Apos as questoes, adicione o gabarito comentado explicando por que cada resposta esta certa ou errada.',
             'Material de revisao completo com explicacoes. Perfeito para concursos, vestibulares e certificacoes.'),
            (11,
             'Crie um mapa mental em formato de topicos e subtopicos sobre [assunto]. Organize do conceito mais amplo para os detalhes. Inclua exemplos praticos em cada subtopico principal.',
             'Visao completa do assunto em estrutura organizada. Cole no Notion, Obsidian ou imprima para revisar.'),
            (12,
             'Explique a diferenca entre [conceito A] e [conceito B] usando: 1) definicao simples de cada um, 2) uma analogia pratica, 3) quando usar cada um, 4) erro mais comum de quem confunde os dois.',
             'Exemplo: renda fixa x renda variavel. Explicacao completa com analogia de aluguel vs. ser socio de empresa.'),
            (13,
             'Crie um plano de estudos de 30 dias para aprender [habilidade] do zero. Divida em 4 semanas tematicas. Para cada semana: objetivo, recursos gratuitos recomendados, exercicio pratico e como medir o progresso.',
             'Roadmap completo com metricas de evolucao incluidas. Funciona para idiomas, programacao, marketing e mais.'),
            (14,
             'Aja como professor especialista em [tema]. Me de os 5 conceitos fundamentais que todo iniciante precisa dominar antes de qualquer outro. Para cada conceito: o que e, por que e essencial e um exercicio para fixar.',
             'Base solida antes de avancar para conteudos mais complexos. Evita o erro de comecar pela parte errada.'),
            (15,
             'Crie 3 analogias diferentes para explicar [conceito dificil]. Uma usando esportes, uma usando culinaria e uma usando tecnologia. Depois me diga qual das tres e mais eficaz para memorizar e por que.',
             'Pelo menos uma das analogias vai grudar na sua memoria. Otimo para explicar conceitos a outras pessoas.'),
            (16,
             'Transforme o conteudo abaixo em 10 flashcards no formato: FRENTE (pergunta ou termo) | VERSO (resposta ou definicao). Priorize os conceitos mais importantes e use linguagem simples: [cole o conteudo]',
             'Material pronto para revisar no Anki, Quizlet ou qualquer app de flashcards. Metodo comprovado para retencao.'),
        ]
    },
    {
        'num': '03', 'title': 'Financas Pessoais',
        'subtitle': '8 prompts para organizar, economizar e investir melhor',
        'color': CAT_COLORS[2],
        'prompts': [
            (17,
             'Aja como planejador financeiro pessoal. Com base na renda de R$[valor] e nas despesas abaixo, crie um orcamento mensal usando o metodo 50/30/20 (necessidades/desejos/investimentos). Aponte onde estou gastando alem do ideal: [liste as despesas]',
             'Diagnostico financeiro completo mais plano de acao personalizado. Ideal para comecar o mes organizado.'),
            (18,
             'Explique [investimento] para alguem que nunca investiu. Inclua: como funciona, riscos envolvidos, rentabilidade esperada, valor minimo para comecar e para qual perfil de investidor e mais indicado.',
             'Exemplo: CDB. Explicacao completa com comparacao ao rendimento da poupanca em linguagem acessivel.'),
            (19,
             'Liste os 7 erros mais comuns de quem comeca a investir. Para cada erro: 1) Por que ele acontece (a psicologia por tras), 2) Como evita-lo com uma acao pratica imediata, 3) Um exemplo com numeros reais mostrando o impacto financeiro desse erro ao longo de 10 anos (ex: quanto dinheiro se perde ou deixa de ganhar). Use simulacoes com valores como R$300/mes investidos.',
             'Os numeros concretos sao o que realmente choca e motiva a mudanca de comportamento. Muito mais eficaz do que alertas vagos sobre "riscos".'),
            (20,
             'Aja como consultor financeiro. Analise meu perfil de gastos abaixo e me de 5 estrategias praticas e especificas para economizar pelo menos 20% da minha renda sem comprometer minha qualidade de vida: [descreva seus gastos principais]',
             'Cortes cirurgicos e inteligentes, nao sacrificios desnecessarios. A IA identifica os maiores vazamentos.'),
            (21,
             'Crie um plano detalhado para quitar R$[valor em dividas] em [X meses] com renda liquida de R$[valor]. Use o metodo da bola de neve. Inclua: ordem de pagamento, valor mensal para cada divida e quanto economizo em juros.',
             'Plano de quitacao com data de conclusao e economia total calculada. Motivador e extremamente pratico.'),
            (22,
             'Compare renda fixa e renda variavel usando uma tabela com: definicao, risco, retorno esperado, liquidez, indicado para qual perfil e exemplo de produto. Ao final, me diga qual escolher com base no perfil conservador, moderado ou arrojado.',
             'Guia de decisao claro para sua primeira aplicacao financeira. Sem jargoes, sem enrolacao.'),
            (23,
             'Analise a lista de gastos abaixo e: 1) identifique os 3 maiores viloes financeiros, 2) sugira alternativas mais baratas para cada um, 3) calcule quanto eu economizaria por ano fazendo essas trocas: [cole seus gastos mensais]',
             'Economia concreta em reais, nao promessas vagas. Voce ve exatamente o impacto anual de cada mudanca.'),
            (24,
             'Crie um plano de investimento progressivo para quem comeca com R$100 por mes. Mostre a evolucao mes a mes por 12 meses com reinvestimento dos rendimentos. Inclua onde investir cada valor e quanto terei ao final de 1, 5 e 10 anos.',
             'Prova concreta de que R$100 por mes pode virar patrimonio real. Excelente para se motivar a comecar.'),
        ]
    },
    {
        'num': '04', 'title': 'Dia a Dia e Organizacao',
        'subtitle': '9 prompts para simplificar e otimizar sua rotina',
        'color': CAT_COLORS[3],
        'prompts': [
            (25,
             'Crie uma lista de compras semanal equilibrada para [numero] pessoas com orcamento de R$[valor]. Inclua: cafe da manha, almoco, jantar e lanches. Priorize alimentos versateis que sirvam para mais de uma refeicao.',
             'Lista estrategica que evita desperdicio e estica o orcamento ao maximo. Teste no proximo sabado.'),
            (26,
             'Crie uma rotina matinal de 60 minutos para alguem que quer [objetivo: ex. ter mais energia / ser mais produtivo / perder peso]. Divida em blocos de tempo, explique o beneficio de cada atividade e de dicas para manter a consistencia.',
             'Rotina com proposito e ciencia por tras, nao apenas a sugestao generica de "acordar mais cedo".'),
            (27,
             'Com os ingredientes abaixo, crie um cardapio para 5 dias que: aproveite ao maximo cada ingrediente sem repetir pratos, seja pratico (ate 30 min de preparo) e seja nutritivamente equilibrado. Ingredientes: [liste o que tem em casa]',
             'Zero desperdicio e refeicoes variadas sem precisar ir ao mercado. Economiza tempo e dinheiro.'),
            (28,
             'Aja como organizador profissional. Crie um plano de organizacao para [comodo] em 3 etapas: 1) o que descartar, 2) o que reorganizar e 3) sistemas para manter organizado. Inclua produtos simples que facilitam a organizacao.',
             'Metodo profissional de organizacao sem contratar ninguem. Funciona para qualquer comodo da casa.'),
            (29,
             'Crie uma checklist detalhada para [evento/situacao] em 3 fases: ANTES (com indicacao de quantos dias/horas de antecedencia cada item deve ser feito), NO DIA (em ordem cronologica) e DEPOIS. Para cada item inclua: a tarefa especifica e por que ela e critica. Destaque em negrito os 5 itens que as pessoas mais esquecem e que causam os maiores problemas. Formato: tabela com colunas Fase | Tarefa | Por que importa | [ ] Feito.',
             'Pronto para imprimir ou copiar para o Notion. Muito mais util do que uma lista simples porque explica o motivo de cada item.'),
            (30,
             'Voce e especialista em comunicacao nao-violenta. Para a seguinte situacao: [ex: cobrar divida de amigo / recusar convite / comunicar uma ma noticia a familiar], escreva 2 versoes de mensagem: VERSAO 1 - Tom formal (para contextos profissionais ou pessoas com quem voce tem menos intimidade), VERSAO 2 - Tom informal (para amigos proximos ou familiares). Ambas devem: dizer o necessario com clareza, preservar o relacionamento e nao deixar margem para interpretacoes erradas.',
             'Ter 2 versoes prontas permite escolher o tom certo para cada relacao. Elimina o travamento de "nao sei como falar isso".'),
            (31,
             'Crie um protocolo noturno de 45 minutos para quem tem dificuldade com [ex: ansiedade / vicio em celular / pensamentos acelerados]. Apresente no formato de blocos de horario (ex: 22h00 - 22h10: ...). Para cada atividade inclua: o que fazer exatamente, a explicacao cientifica em 1 frase (com o mecanismo biologico envolvido), e o que evitar nesse mesmo horario e por que. Finalize com uma lista de "preparacao do ambiente" com temperatura, iluminacao e sons ideais.',
             'O formato com horarios especificos transforma uma ideia em acao real. Voce nao precisa "criar uma rotina", so seguir o protocolo.'),
            (32,
             'Crie um programa de 30 dias para desenvolver o habito de [habito]. Baseie-se na tecnica de James Clear do livro Habitos Atomicos. Inclua: gatilho, rotina, recompensa, como medir o progresso e o que fazer quando falhar.',
             'Metodo comprovado para criar habitos de verdade, nao apenas forca de vontade que dura uma semana.'),
            (33,
             'Sugira 7 ideias de presentes criativos e memoraveis para [perfil da pessoa: ex. mae de 50 anos que ama jardim] com orcamento de R$[valor]. Para cada sugestao: onde encontrar, por que essa pessoa vai amar e como personalizar.',
             'Presente que emociona e surpreende, nao o de sempre. Perfeito para qualquer data especial.'),
        ]
    },
    {
        'num': '05', 'title': 'Redes Sociais e Conteudo',
        'subtitle': '9 prompts para crescer, engajar e vender nas redes',
        'color': CAT_COLORS[4],
        'prompts': [
            (34,
             'Aja como estrategista de conteudo para Instagram. Crie 5 ideias de posts para um perfil de [nicho] voltado para [publico-alvo]. Para cada ideia: tema, gancho de abertura, estrutura do conteudo e chamada para acao.',
             'Posts com estrategia real por tras, nao so inspiracao do momento. Cada ideia vem com estrutura pronta.'),
            (35,
             'Escreva 3 versoes de legenda para um post sobre [tema/foto]: uma emocional, uma educativa e uma com humor. Cada legenda deve ter: gancho forte na primeira linha, desenvolvimento e CTA. Maximo 150 palavras cada.',
             'Voce escolhe o tom certo para cada momento. Nunca mais passe em branco na hora de legendar.'),
            (36,
             'Sugira 15 hashtags estrategicas para um post sobre [tema] no Instagram. Divida em 3 grupos: 5 grandes (1M+), 5 medias (100K-1M) e 5 pequenas (10K-100K). Explique por que essa combinacao aumenta o alcance.',
             'Estrategia de hashtag que realmente funciona para crescimento organico e descoberta por novos seguidores.'),
            (37,
             'Crie um roteiro completo para um Reels de 30 segundos sobre [tema]. Inclua: cena por cena, legenda de cada cena, sugestao de musica, texto na tela e gancho nos primeiros 3 segundos para prender a atencao.',
             'Roteiro pronto para gravar sem precisar improvisar nada. So ligar a camera e seguir o script.'),
            (38,
             'Analise esta legenda e reescreva de 3 formas diferentes melhorando: o gancho inicial, a conexao emocional e o CTA. Apos as versoes, explique o que estava fraco no original: [cole a legenda]',
             'Legenda melhorada mais aprendizado sobre o que faz uma legenda converter. Melhora com cada uso.'),
            (39,
             'Crie 3 versoes de bio para Instagram de um perfil de [nicho], respeitando o limite real de 150 caracteres do Instagram. Cada versao deve comunicar: quem e voce, o que voce oferece, para quem, um diferencial ou prova social, e um CTA. Versao 1: focada em autoridade e resultado, Versao 2: focada em emocao e identificacao do publico, Versao 3: direta e focada em acao imediata. Mostre a contagem de caracteres ao lado de cada versao.',
             '3 versoes porque o tom certo depende do seu posicionamento. Mostrar a contagem garante que cabe no limite real do Instagram.'),
            (40,
             'Crie um calendario editorial de 7 dias para um perfil de [nicho]. Para cada dia: formato (carrossel, reels, foto, stories), tema, objetivo do post (educar, engajar, vender, entreter) e horario ideal para publicar.',
             'Semana de conteudo totalmente planejada em menos de 5 minutos. Nunca mais fique sem ideia.'),
            (41,
             'Crie um carrossel de 7 slides sobre [tema] para Instagram. Slide 1: gancho irresistivel. Slides 2-6: um ponto por slide com exemplo pratico. Slide 7: conclusao mais CTA. Linguagem simples e direta para iniciantes.',
             'Carrossel completo pronto para diagramar no Canva. O formato que mais salva, compartilha e gera seguidores.'),
            (42,
             'Aja como especialista em crescimento organico no Instagram. Crie um plano de 30 dias para aumentar o engajamento de um perfil de [nicho] sem anuncios. Inclua: frequencia de posts, estrategia de stories, como usar o algoritmo a seu favor e metricas para acompanhar.',
             'Estrategia real de crescimento organico com acoes diarias concretas, nao dicas vagas e genericas.'),
        ]
    },
    {
        'num': '06', 'title': 'Negocios e Empreendedorismo',
        'subtitle': '8 prompts para vender mais, se destacar e crescer',
        'color': CAT_COLORS[5],
        'prompts': [
            (43,
             'Aja como especialista em branding e naming. Crie 10 opcoes de nome para um negocio de [segmento] voltado para [publico-alvo]. Para cada nome entregue: 1) O conceito ou significado por tras da escolha, 2) Por que ressoa com esse publico especifico, 3) Sugestao de dominio .com.br compativel com o nome, 4) Nota de 1 a 5 para memorabilidade e 1 a 5 para posicionamento de mercado. Ao final, recomende os 3 melhores e justifique a escolha.',
             'O ranking ao final e o diferencial: voce nao precisa escolher sozinho entre 10 opcoes. A IA ja filtra e justifica as melhores por voce.'),
            (44,
             'Escreva uma descricao de produto persuasiva para [produto] usando o framework PAS (Problema, Agitacao, Solucao). Inclua: beneficios emocionais, beneficios praticos, para quem e indicado e uma chamada para acao irresistivel.',
             'Descricao que vende ativamente, nao apenas informa. Ideal para paginas de vendas, Shopee e Mercado Livre.'),
            (45,
             'Crie um plano de divulgacao de 30 dias para um negocio de [segmento] com orcamento zero. Inclua: canais a usar, tipo de conteudo para cada canal, frequencia e como medir se esta funcionando. Foco em estrategias que geram resultado rapido.',
             'Plano de marketing gratuito, acionavel e com metricas claras. Excelente para quem esta comecando sem verba.'),
            (46,
             'Escreva uma proposta comercial profissional para o servico de [servico] com valor de R$[valor]. Inclua: apresentacao, problema que resolve, como funciona, entregaveis, prazo, investimento e garantia. Tom: confiante e orientado a resultado.',
             'Proposta que fecha vendas e transmite profissionalismo. A diferenca entre "vou pensar" e "quero contratar".'),
            (47,
             'Aja como especialista em customer success. Situacao: [descreva o problema do cliente]. Escreva uma resposta que: 1) Abra reconhecendo a experiencia do cliente (sem assumir culpa excessiva nem ser defensivo), 2) Explique o que aconteceu de forma transparente e em linguagem simples, 3) Apresente a solucao concreta com prazo definido, 4) Oferte um gesto de reconciliacao (desconto, bonus, atendimento prioritario) proporcional ao transtorno causado, 5) Feche com um compromisso claro de melhoria. Tom: humano, responsavel e orientado a solucao.',
             'O gesto de reconciliacao no item 4 e o que transforma um cliente frustrado em defensor da marca. Pesquisas mostram que clientes bem atendidos apos uma falha ficam mais leais do que clientes que nunca tiveram problemas.'),
            (48,
             'Crie uma lista com as 10 perguntas essenciais que devo fazer antes de fechar [tipo de parceria: ex. revenda / sociedade / afiliacao]. Para cada pergunta: por que ela e importante e qual resposta seria um sinal de alerta.',
             'Due diligence simples e eficaz que evita parcerias ruins. Aprenda a identificar sinais de alerta antes de assinar.'),
            (49,
             'Escreva 3 versoes de descricao para minha loja de [tipo de negocio] no WhatsApp Business, respeitando o limite de 512 caracteres do app. Cada versao deve cobrir: o que vendo, principal diferencial competitivo, formas de pagamento aceitas, horario de atendimento e uma chamada para acao. Versao 1: tom profissional e formal, Versao 2: tom descontraido e proximo, Versao 3: tom de urgencia focado em oferta ou beneficio imediato. Mostre a contagem de caracteres de cada versao.',
             'O limite real do WhatsApp Business e 512 caracteres. As 3 versoes permitem testar qual tom gera mais contatos e conversoes para o seu negocio.'),
            (50,
             'Aja como especialista em marketing sazonal. Crie 5 ideias de promocoes criativas para [segmento] durante [epoca: ex. Dia das Maes / Black Friday]. Para cada promocao: mecanica, como divulgar, estimativa de aumento nas vendas e custo estimado.',
             'Promocoes estrategicas com estimativa de retorno financeiro. Pare de inventar promocoes e comece a planejar.'),
        ]
    },
]


# ─── Montagem do documento ───────────────────────────────────────────────────
def build_pdf():
    output = r'c:\PromptLab\Prompt_Lab_Ebook_v4.pdf'

    doc = BaseDocTemplate(
        output,
        pagesize=A4,
        title='Prompt Lab - 50 Prompts de IA Prontos para Usar',
        author='Prompt Lab',
        subject='Guia de Prompts para Inteligencia Artificial',
        keywords='prompts ia chatgpt claude gemini inteligencia artificial',
    )

    # Frames
    full_frame    = Frame(0, 0, W, H,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='full')
    content_frame = Frame(LM, BM, CONTENT_W, CONTENT_H,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='normal')

    doc.addPageTemplates([
        PageTemplate('cover',   [full_frame]),
        PageTemplate('toc',     [full_frame]),
        PageTemplate('cat',     [full_frame]),
        PageTemplate('content', [content_frame], onPage=content_page_deco),
        PageTemplate('closing', [full_frame]),
    ])

    story = []

    # ── Capa ──
    story.append(CoverPage())
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    # ── Introducao ──
    story += intro_story()

    # ── Sumario ──
    story.append(NextPageTemplate('toc'))
    story.append(PageBreak())
    story.append(TOCPage())
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    # ── Categorias ──
    for cat in CATEGORIES:
        # Pagina de cabecalho da categoria
        story.append(NextPageTemplate('cat'))
        story.append(PageBreak())
        story.append(CatHeaderPage(
            cat['num'], cat['title'], cat['subtitle'], cat['color']))

        # Paginas de prompts
        story.append(NextPageTemplate('content'))
        story.append(PageBreak())
        story.append(section_inline_header(
            cat['num'], cat['title'], cat['color'], len(cat['prompts'])))
        story.append(Spacer(1, 5 * mm))

        for num, prompt_text, tip_text in cat['prompts']:
            story.append(prompt_block(num, prompt_text, tip_text, cat['color']))

        story.append(PageBreak())

    # ── Bonus ──
    story += bonus_story()

    # ── Encerramento ──
    story.append(NextPageTemplate('closing'))
    story.append(PageBreak())
    story.append(ClosingPageFlow())

    doc.build(story)
    print(f'PDF gerado com sucesso: {output}')


if __name__ == '__main__':
    build_pdf()
