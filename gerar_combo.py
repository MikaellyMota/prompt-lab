# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                 Spacer, Paragraph, Table, TableStyle,
                                 HRFlowable, PageBreak, NextPageTemplate)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

W, H = A4

# ── Paleta ──────────────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#0D1B2A")
NAVY2      = colors.HexColor("#1A2E45")
PINK       = colors.HexColor("#EC4899")
PINK2      = colors.HexColor("#BE185D")
PINK_LIGHT = colors.HexColor("#FDF2F8")
PURPLE     = colors.HexColor("#8B5CF6")
GOLD       = colors.HexColor("#F4A026")
GREEN      = colors.HexColor("#10B981")
WHITE      = colors.white
GRAY       = colors.HexColor("#5A6474")
GRAY2      = colors.HexColor("#ECEEF2")
GRAY3      = colors.HexColor("#F7F8FA")


# ── Estilos ──────────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=11, leading=15,
                    textColor=NAVY, spaceAfter=4)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

def P(text, style):
    return Paragraph(text, style)

def Space(h_mm):
    return Spacer(1, h_mm * mm)


# ── Flowable: Full-page canvas drawing ────────────────────────────────────────
class FullPage(Flowable):
    """Flowable que ocupa a pagina inteira e desenha no canvas."""
    def __init__(self, draw_fn, w=W, h=H):
        super().__init__()
        self._draw_fn = draw_fn
        self.width    = w
        self.height   = h

    def draw(self):
        self._draw_fn(self.canv)

    def wrap(self, aw, ah):
        return self.width, self.height


# ── Flowable: Pill button ─────────────────────────────────────────────────────
class PillButton(Flowable):
    def __init__(self, text, width, height=14*mm, bg=PINK, fg=WHITE, font_size=13):
        super().__init__()
        self.text = text
        self.bw   = width
        self.bh   = height
        self.bg   = bg
        self.fg   = fg
        self.fs   = font_size
        self.width  = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.bw, self.bh, self.bh / 2, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont("Helvetica-Bold", self.fs)
        c.drawCentredString(self.bw / 2, self.bh / 2 - 4.5*mm, self.text)
        c.restoreState()

    def wrap(self, aw, ah):
        return self.bw, self.bh


# ── Flowable: Accent bar ──────────────────────────────────────────────────────
class AccentBar(Flowable):
    def __init__(self, width, h=3, color=PINK):
        super().__init__()
        self.bw    = width
        self.bh    = h
        self.color = color
        self.width  = width
        self.height = h

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.bw, self.bh, self.bh / 2, fill=1, stroke=0)
        c.restoreState()

    def wrap(self, aw, ah):
        return self.bw, self.bh


# ── Desenhos de capa ──────────────────────────────────────────────────────────
def draw_cover(canvas):
    IW = W - 40*mm

    # Fundo escuro
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # Fundo superior levemente diferente
    canvas.setFillColor(NAVY2)
    canvas.rect(0, H * 0.52, W, H * 0.48, fill=1, stroke=0)

    # Circulos decorativos
    canvas.saveState()
    canvas.setFillColor(PINK)
    canvas.setFillAlpha(0.09)
    canvas.circle(W * 0.88, H * 0.82, 150, fill=1, stroke=0)
    canvas.setFillAlpha(0.06)
    canvas.circle(W * 0.1,  H * 0.18, 110, fill=1, stroke=0)
    canvas.restoreState()

    # Badge "OFERTA ESPECIAL"
    bw, bh = 90*mm, 8*mm
    bx, by = (W - bw) / 2, H - 46*mm
    canvas.setFillColor(colors.HexColor("#1E3A52"))
    canvas.roundRect(bx, by, bw, bh, bh / 2, fill=1, stroke=0)
    canvas.setFillColor(PINK)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawCentredString(W / 2, by + 2*mm, "OFERTA ESPECIAL")

    # Titulo COMBO
    canvas.setFillColor(PINK)
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawCentredString(W / 2, H - 60*mm, "COMBO")

    # IA DO ZERO
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 52)
    canvas.drawCentredString(W / 2, H - 82*mm, "IA DO ZERO")

    # Linha rosa
    lx = (W - IW) / 2
    canvas.setFillColor(PINK)
    canvas.roundRect(lx, H - 88*mm, IW, 3, 1.5, fill=1, stroke=0)

    # Subtitulo
    canvas.setFillColor(colors.HexColor("#CBD5E1"))
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(W / 2, H - 98*mm, "2 e-books. 1 pre\u00e7o.")
    canvas.drawCentredString(W / 2, H - 106*mm,
                              "Tudo que voc\u00ea precisa para dominar a IA.")

    # Cards dos ebooks
    cx = (W - IW) / 2
    col_w = (IW - 6*mm) / 2
    card_y = H - 155*mm
    card_h = 46*mm

    # Card 1
    canvas.setFillColor(colors.HexColor("#1A2E45"))
    canvas.setStrokeColor(colors.HexColor("#334155"))
    canvas.setLineWidth(1.2)
    canvas.roundRect(cx, card_y, col_w, card_h, 8, fill=1, stroke=1)
    canvas.setFillColor(PINK)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawCentredString(cx + col_w / 2, card_y + card_h - 8*mm, "E-BOOK 1")
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 15)
    canvas.drawCentredString(cx + col_w / 2, card_y + card_h - 17*mm, "Prompt Lab")
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(cx + col_w / 2, card_y + card_h - 26*mm,
                              "50 prompts prontos")
    canvas.drawCentredString(cx + col_w / 2, card_y + card_h - 33*mm,
                              "para 6 categorias")

    # Card 2
    c2x = cx + col_w + 6*mm
    canvas.setFillColor(colors.HexColor("#1A1A2E"))
    canvas.roundRect(c2x, card_y, col_w, card_h, 8, fill=1, stroke=1)
    canvas.setFillColor(PURPLE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawCentredString(c2x + col_w / 2, card_y + card_h - 8*mm, "E-BOOK 2")
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(c2x + col_w / 2, card_y + card_h - 17*mm,
                              "30 Posts em 1 Hora")
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(c2x + col_w / 2, card_y + card_h - 26*mm,
                              "Prompts + templates")
    canvas.drawCentredString(c2x + col_w / 2, card_y + card_h - 33*mm,
                              "para Instagram")

    # Box de preco
    px, py = cx, card_y - 28*mm
    canvas.setFillColor(colors.HexColor("#0F2030"))
    canvas.setStrokeColor(colors.HexColor("#334155"))
    canvas.roundRect(px, py, IW, 24*mm, 10, fill=1, stroke=1)

    # Coluna 1: De ...
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(px + IW * 0.2, py + 15*mm, "Se comprar separado")
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawCentredString(px + IW * 0.2, py + 9*mm, "R$ 44,80")

    # Divisoria
    canvas.setStrokeColor(colors.HexColor("#334155"))
    canvas.setLineWidth(0.5)
    canvas.line(px + IW * 0.4, py + 4*mm, px + IW * 0.4, py + 20*mm)

    # Coluna 2: Combo
    canvas.setFillColor(PINK)
    canvas.setFont("Helvetica-Bold", 28)
    canvas.drawCentredString(px + IW * 0.62, py + 9*mm, "R$ 34,90")
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(px + IW * 0.62, py + 5*mm, "pagamento \u00fanico")

    # Divisoria
    canvas.line(px + IW * 0.82, py + 4*mm, px + IW * 0.82, py + 20*mm)

    # Coluna 3: Economia
    canvas.setFillColor(GREEN)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(px + IW * 0.91, py + 13*mm, "R$ 9,90")
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(px + IW * 0.91, py + 9*mm, "de economia")

    # By Prompt Lab
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(W / 2, py - 8*mm, "by Prompt Lab")


# ── Header/Footer das paginas internas ────────────────────────────────────────
def draw_inner_page(canvas, doc):
    canvas.saveState()
    # Top bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - 14*mm, W, 14*mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawCentredString(W / 2, H - 9*mm, "COMBO IA DO ZERO  |  Prompt Lab")
    # Footer line
    canvas.setStrokeColor(GRAY2)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, 14*mm, W - 20*mm, 14*mm)
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(W / 2, 8*mm,
                              "Acesso imediato ap\u00f3s a compra  |  PDF em todas as plataformas")
    canvas.restoreState()


# ── Pagina 2 — Beneficios ─────────────────────────────────────────────────────
def page2_story(IW):
    story = []

    story.append(Space(4))
    story.append(AccentBar(IW, 3, PINK))
    story.append(Space(4))
    story.append(P("Por que escolher o Combo IA do Zero?",
        S("sec", fontName="Helvetica-Bold", fontSize=15, leading=20,
          textColor=NAVY, alignment=TA_CENTER, spaceAfter=10)))

    story.append(P(
        "A maioria das pessoas usa a Intelig\u00eancia Artificial de forma errada \u2014 "
        "digita qualquer coisa e fica frustrada com os resultados m\u00e9diocres.",
        S("b1", fontSize=11, leading=17, textColor=GRAY,
          alignment=TA_JUSTIFY, spaceAfter=6)))

    story.append(P(
        "O problema nunca \u00e9 a ferramenta. \u00c9 saber o que pedir e como usar.",
        S("b2", fontName="Helvetica-Bold", fontSize=12, leading=18,
          textColor=NAVY, alignment=TA_CENTER, spaceAfter=8)))

    story.append(P(
        "O Combo IA do Zero resolve isso de vez. Com os dois e-books juntos, voc\u00ea vai "
        "de completo iniciante a usu\u00e1rio avan\u00e7ado de IA em poucos dias \u2014 "
        "usando os prompts certos, criando conte\u00fado de qualidade e economizando "
        "horas toda semana.",
        S("b3", fontSize=11, leading=17, textColor=GRAY,
          alignment=TA_JUSTIFY, spaceAfter=10)))

    story.append(HRFlowable(width=IW, thickness=1, color=GRAY2, spaceAfter=8))

    # Cards de beneficios
    cw = (IW - 6*mm) / 2

    def check_item(text, color=NAVY):
        return P(f"<b>\u2713</b>  {text}",
                 S("ci", fontSize=10, leading=16, textColor=color, spaceAfter=3))

    eb1_items = [
        P("E-book 1 \u2014 Prompt Lab",
          S("et1", fontName="Helvetica-Bold", fontSize=12, textColor=PINK,
            alignment=TA_CENTER, spaceAfter=8)),
        check_item("50 prompts detalhados com exemplos pr\u00e1ticos"),
        check_item("6 categorias: Trabalho, Estudos, Finan\u00e7as,\nOrganiza\u00e7\u00e3o, Redes Sociais e Neg\u00f3cios"),
        check_item("Resultado esperado e dica de uso em cada prompt"),
        check_item("Funciona no ChatGPT, Copilot, Gemini e qualquer IA"),
    ]
    eb2_items = [
        P("E-book 2 \u2014 30 Posts em 1 Hora",
          S("et2", fontName="Helvetica-Bold", fontSize=12, textColor=PURPLE,
            alignment=TA_CENTER, spaceAfter=8)),
        check_item("M\u00e9todo dos 30 posts com distribui\u00e7\u00e3o estrat\u00e9gica"),
        check_item("5 prompts poderosos para gerar 30 ideias em minutos"),
        check_item("10 templates de legenda prontos para editar e publicar"),
        check_item("Passo a passo: do zero ao post agendado em 1 hora"),
        check_item("B\u00f4nus: 4 prompts para nunca mais travar"),
    ]

    max_r = max(len(eb1_items), len(eb2_items))
    while len(eb1_items) < max_r: eb1_items.append(Space(1))
    while len(eb2_items) < max_r: eb2_items.append(Space(1))

    rows = [[eb1_items[i], eb2_items[i]] for i in range(max_r)]
    tbl = Table(rows, colWidths=[cw, cw])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, -1), PINK_LIGHT),
        ("BACKGROUND",    (1, 0), (1, -1), colors.HexColor("#F5F3FF")),
        ("BOX",           (0, 0), (0, -1), 1.5, PINK),
        ("BOX",           (1, 0), (1, -1), 1.5, PURPLE),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(tbl)
    story.append(Space(8))

    # Para quem e
    story.append(HRFlowable(width=IW, thickness=1, color=GRAY2, spaceAfter=6))
    story.append(P("Para quem \u00e9 esse combo?",
        S("sq", fontName="Helvetica-Bold", fontSize=14, textColor=NAVY,
          alignment=TA_CENTER, spaceAfter=10)))

    audience = [
        ("\U0001f4a1 Iniciantes em IA",
         "Que querem aprender a usar o ChatGPT de forma pr\u00e1tica e imediata."),
        ("\U0001f4f1 Donos de perfil no Instagram",
         "Que ficam travados sem saber o que postar toda semana."),
        ("\U0001f9e0 Empreendedores e aut\u00f4nomos",
         "Que querem economizar tempo em tarefas repetitivas usando IA."),
        ("\U0001f680 Quem quer come\u00e7ar a vender online",
         "E precisa de conte\u00fado profissional sem contratar ningu\u00e9m."),
    ]

    aud_rows = [[
        P(f"<b>{t}</b>",
          S(f"at{i}", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY,
            leading=14, spaceAfter=0)),
        P(d, S(f"ad{i}", fontSize=10, textColor=GRAY, leading=15, spaceAfter=0)),
    ] for i, (t, d) in enumerate(audience)]

    aud_tbl = Table(aud_rows, colWidths=[62*mm, IW - 62*mm])
    aud_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS",  (0, 0), (-1, -1), [GRAY3, WHITE]),
        ("TOPPADDING",      (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",   (0, 0), (-1, -1), 8),
        ("LEFTPADDING",     (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",    (0, 0), (-1, -1), 10),
        ("VALIGN",          (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW",       (0, 0), (-1, -2), 0.5, GRAY2),
    ]))
    story.append(aud_tbl)

    return story


# ── Pagina 3 — Preco + Garantia + CTA ────────────────────────────────────────
def page3_story(IW):
    story = []

    story.append(Space(4))
    story.append(AccentBar(IW, 3, PINK))
    story.append(Space(6))

    story.append(P("N\u00e3o compre separado.",
        S("don", fontName="Helvetica-Bold", fontSize=20, leading=26,
          textColor=NAVY, alignment=TA_CENTER, spaceAfter=14)))

    # Tabela de comparacao
    comp_data = [
        [
            P("Se comprar separado",
              S("ch1", fontName="Helvetica-Bold", fontSize=11,
                textColor=WHITE, alignment=TA_CENTER, spaceAfter=0)),
            P("Com o Combo IA do Zero",
              S("ch2", fontName="Helvetica-Bold", fontSize=11,
                textColor=WHITE, alignment=TA_CENTER, spaceAfter=0)),
        ],
        [
            P("Prompt Lab: R$ 19,90<br/>+ 30 Posts: R$ 24,90<br/><b>= R$ 44,80</b>",
              S("cv1", fontSize=12, leading=20, textColor=NAVY,
                alignment=TA_CENTER, spaceAfter=0)),
            P("Tudo por <b>R$ 34,90</b><br/><br/>Economia de <b>R$ 9,90</b>",
              S("cv2", fontName="Helvetica-Bold", fontSize=14, leading=22,
                textColor=PINK2, alignment=TA_CENTER, spaceAfter=0)),
        ],
    ]
    cw = IW / 2 - 3*mm
    comp_tbl = Table(comp_data, colWidths=[cw, cw])
    comp_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0), NAVY),
        ("BACKGROUND",    (1, 0), (1, 0), PINK2),
        ("BACKGROUND",    (0, 1), (0, 1), GRAY3),
        ("BACKGROUND",    (1, 1), (1, 1), PINK_LIGHT),
        ("BOX",           (0, 0), (-1, -1), 1.5, GRAY2),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, GRAY2),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(comp_tbl)
    story.append(Space(10))

    # Garantia
    gar_data = [[
        P("\U0001f6e1",
          S("gi", fontSize=24, alignment=TA_CENTER, spaceAfter=0)),
        [
            P("Garantia de 7 dias",
              S("gtit", fontName="Helvetica-Bold", fontSize=13,
                textColor=NAVY, spaceAfter=4)),
            P("Se por qualquer motivo voc\u00ea n\u00e3o ficar satisfeito, basta entrar em "
              "contato em at\u00e9 7 dias ap\u00f3s a compra e devolvemos 100% do seu "
              "dinheiro. Sem perguntas.",
              S("gd", fontSize=10, textColor=GRAY, leading=15, spaceAfter=0)),
        ],
    ]]
    gar_tbl = Table(gar_data, colWidths=[22*mm, IW - 22*mm])
    gar_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
        ("BOX",           (0, 0), (-1, -1), 1.5, GREEN),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(gar_tbl)
    story.append(Space(8))

    # Badges de seguranca
    badges = [
        [
            P("\U0001f512 Pagamento\nseguro",
              S("bd1", fontSize=9, textColor=GRAY, alignment=TA_CENTER,
                leading=14, spaceAfter=0)),
            P("\U0001f4c4 PDF\nimediato",
              S("bd2", fontSize=9, textColor=GRAY, alignment=TA_CENTER,
                leading=14, spaceAfter=0)),
            P("\u2705 Kiwify",
              S("bd3", fontSize=9, textColor=GRAY, alignment=TA_CENTER,
                leading=14, spaceAfter=0)),
            P("\U0001f4f1 Celular,\ntablet e PC",
              S("bd4", fontSize=9, textColor=GRAY, alignment=TA_CENTER,
                leading=14, spaceAfter=0)),
        ],
    ]
    badges_tbl = Table(badges, colWidths=[IW/4]*4)
    badges_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GRAY3),
        ("BOX",           (0, 0), (-1, -1), 1, GRAY2),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, GRAY2),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(badges_tbl)
    story.append(Space(10))

    # Botao CTA
    story.append(PillButton(
        "QUERO O COMBO IA DO ZERO  \u2014  R$ 34,90",
        IW, 14*mm, PINK, WHITE, 13,
    ))
    story.append(Space(4))
    story.append(P("Acesso imediato ap\u00f3s a compra. Entrega em PDF.",
        S("ac", fontSize=10, textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)))

    story.append(HRFlowable(width=IW, thickness=1, color=GRAY2, spaceAfter=4))
    story.append(P("<b>PROMPT LAB</b>  \u2014  Aprenda IA do jeito certo.",
        S("fb", fontName="Helvetica-Bold", fontSize=11,
          textColor=NAVY, alignment=TA_CENTER, spaceAfter=2)))
    story.append(P("promptlab.com.br",
        S("fu", fontSize=9, textColor=GRAY, alignment=TA_CENTER)))

    return story


# ── Build documento ───────────────────────────────────────────────────────────
def build_pdf(output="Combo_IA_do_Zero_v2.pdf"):
    M = 20*mm
    IW = W - 2 * M

    # Cover frame ocupa a pagina toda
    cover_frame = Frame(0, 0, W, H,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id="cover")

    # Inner frames com margens
    inner_frame = Frame(M, M + 4*mm, W - 2*M, H - 2*M - 18*mm,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id="inner")

    def noop(c, d): pass  # cover bg eh desenhado dentro do FullPage flowable

    cover_tpl = PageTemplate(id="cover", frames=[cover_frame], onPage=noop)
    inner_tpl = PageTemplate(id="inner", frames=[inner_frame],
                              onPage=draw_inner_page)

    doc = BaseDocTemplate(
        output,
        pagesize=A4,
        pageTemplates=[cover_tpl, inner_tpl],
        leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
        title="Combo IA do Zero \u2014 Prompt Lab",
        author="Prompt Lab",
    )

    story = []

    # ── PAGINA 1: Capa ──
    story.append(FullPage(draw_cover))
    story.append(NextPageTemplate("inner"))
    story.append(PageBreak())

    # ── PAGINA 2: Beneficios ──
    story.extend(page2_story(IW))
    story.append(NextPageTemplate("inner"))
    story.append(PageBreak())

    # ── PAGINA 3: Preco + CTA ──
    story.extend(page3_story(IW))

    doc.build(story)
    print(f"PDF gerado com sucesso: {output}")


if __name__ == "__main__":
    build_pdf()
