"""Build the submission slide deck as a .pptx.

Same content as presentation.html, as a real PowerPoint file so it can be opened,
edited and presented locally.

Run:  .venv/Scripts/python scripts/build_pptx.py  ->  Digital_Minds_Track3_Slides.pptx
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "Digital_Minds_Track3_Slides.pptx"

# Palette: cool instrument neutrals, one measured accent, one semantic flag colour.
INK = RGBColor(0x12, 0x17, 0x1F)
MUTED = RGBColor(0x59, 0x63, 0x6F)
ACCENT = RGBColor(0x0F, 0x6E, 0x8C)
FLAG = RGBColor(0xB0, 0x3A, 0x26)
GROUND = RGBColor(0xF6, 0xF8, 0xFA)
RULE = RGBColor(0xDC, 0xE2, 0xE8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

SERIF = "Georgia"
SANS = "Segoe UI"
MONO = "Consolas"

W, H = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.9)
BODY_W = W - MARGIN * 2


def new_deck() -> Presentation:
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    return prs


def blank(prs: Presentation, ground: RGBColor = GROUND):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = ground
    return s


def textbox(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    return tf


def para(tf, text, *, size, font=SANS, color=INK, bold=False, space_after=8,
         first=False, align=PP_ALIGN.LEFT, line=None, caps=False, spacing=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if line:
        p.line_spacing = line
    p.space_after = Pt(space_after)
    r = p.add_run()
    r.text = text.upper() if caps else text
    f = r.font
    f.size, f.name, f.bold = Pt(size), font, bold
    f.color.rgb = color
    if spacing is not None:  # letter-spacing via raw XML (python-pptx has no API for it)
        r.font._rPr.set("spc", str(int(spacing * 100)))
    return p


def eyebrow(slide, text, y=Inches(0.62)):
    tf = textbox(slide, MARGIN, y, BODY_W, Inches(0.4))
    para(tf, text, size=11, font=MONO, color=MUTED, first=True, caps=True, spacing=1.4)


def rail(slide, num):
    """Slide number on a thin rule — this is a linear talk, so the ordinal is real information."""
    tf = textbox(slide, MARGIN, H - Inches(0.75), Inches(2), Inches(0.35))
    para(tf, f"{num:02d}", size=11, font=MONO, color=ACCENT, first=True, spacing=0.8)
    ln = slide.shapes.add_shape(1, MARGIN, H - Inches(0.95), BODY_W, Emu(9525))
    ln.fill.solid(); ln.fill.fore_color.rgb = RULE
    ln.line.fill.background(); ln.shadow.inherit = False


def heading(slide, text, y=Inches(1.05), size=40, w=None):
    tf = textbox(slide, MARGIN, y, w or BODY_W, Inches(1.5))
    para(tf, text, size=size, font=SERIF, color=INK, bold=True, first=True, line=1.05)
    return tf


def body_text(slide, blocks, y, w=None, size=16):
    tf = textbox(slide, MARGIN, y, w or Inches(9.6), H - y - Inches(1.1))
    for i, b in enumerate(blocks):
        if isinstance(b, tuple):
            txt, kw = b
        else:
            txt, kw = b, {}
        para(tf, txt, size=kw.pop("size", size), color=kw.pop("color", INK),
             bold=kw.pop("bold", False), first=(i == 0), space_after=kw.pop("space_after", 12),
             line=1.3, **kw)
    return tf


def bullets(slide, items, y, size=15):
    tf = textbox(slide, MARGIN, y, Inches(10.2), H - y - Inches(1.1))
    for i, (lead, rest, col) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(13); p.line_spacing = 1.3
        r = p.add_run(); r.text = "— "
        r.font.size, r.font.name, r.font.color.rgb = Pt(size), SANS, ACCENT
        if lead:
            r2 = p.add_run(); r2.text = lead
            r2.font.size, r2.font.name, r2.font.bold = Pt(size), SANS, True
            r2.font.color.rgb = col or INK
        r3 = p.add_run(); r3.text = rest
        r3.font.size, r3.font.name = Pt(size), SANS
        r3.font.color.rgb = col or INK


def picture(slide, name, y=Inches(2.0), height=Inches(4.4)):
    img = FIG / name
    pic = slide.shapes.add_picture(str(img), Inches(0), y, height=height)
    pic.left = int((W - pic.width) / 2)
    return pic


def caption(slide, text, y):
    tf = textbox(slide, MARGIN, y, BODY_W, Inches(0.8))
    para(tf, text, size=12, color=MUTED, first=True, line=1.25, align=PP_ALIGN.CENTER)


def build() -> None:
    prs = new_deck()

    # 01 — title
    s = blank(prs, WHITE)
    eyebrow(s, "Digital Minds Sprint  ·  Track 3  ·  Introspection & Self-Report Reliability")
    heading(s, "Beaten by eighteen features", y=Inches(1.5), size=54)
    tf = textbox(s, MARGIN, Inches(3.3), Inches(9.4), Inches(1.6))
    para(tf, "Two 70-billion-parameter models were asked to pick out their own writing. "
             "A logistic regression on eighteen surface features did it better.",
         size=21, color=MUTED, first=True, line=1.3)
    tf2 = textbox(s, MARGIN, Inches(5.6), BODY_W, Inches(0.9))
    para(tf2, "Ubayd Hattas & Jaswin Chinthala", size=15, color=INK, first=True, space_after=2)
    para(tf2, "with Apart Research · August 2026", size=13, color=MUTED)
    rail(s, 1)

    # 02 — why it matters
    s = blank(prs)
    eyebrow(s, "Why it matters")
    heading(s, "Model welfare research runs on self-report")
    body_text(s, [
        "When we ask whether a model has preferences, is distressed, or is flourishing, we mostly "
        "ask the model. That only works if its report about itself carries information an outside "
        "observer could not get from the same text.",
        "Binder et al. say models have that privileged access. Song et al. say the apparent effect "
        "is just behavioural similarity.",
        ("Settling it decides whether a whole class of welfare measurements means anything — and "
         "whether we over- or under-attribute moral significance to AI systems.",
         {"bold": True}),
    ], y=Inches(2.5))
    rail(s, 2)

    # 03 — design
    s = blank(prs)
    eyebrow(s, "The design")
    heading(s, "Two confounds, removed by construction")
    bullets(s, [
        ("Capability. ", "The \"self\" model is usually also the smartest model in the comparison. "
         "We use two models sharing a pretraining base — Llama-3.1-70B and Hermes-3-70B — in a "
         "crossed 2×2, so a general competence edge cancels.", None),
        ("Surface leakage. ", "A hidden property is only interesting if a third party can't read it "
         "off the text. We fit an 18-feature style classifier to every stimulus set and gate on it "
         "before collecting main data.", None),
        ("Ground truth is constructed, not elicited. ", "We set which persona writes each text and "
         "store the label where the prediction code structurally cannot reach it.", None),
    ], y=Inches(2.45))
    rail(s, 3)

    # 04 — finding 1
    s = blank(prs)
    eyebrow(s, "Finding 1")
    heading(s, "What looked like self-recognition was style-recognition", size=34)
    picture(s, "fig1_self_vs_surface.png", y=Inches(2.05), height=Inches(4.0))
    caption(s, "Ten conditions, five stimulus designs. Self-prediction tracks the style classifier "
               "at r = +0.71; the classifier matches or beats the model in six of ten.",
            y=Inches(6.15))
    rail(s, 4)

    # 05 — finding 2 (table)
    s = blank(prs)
    eyebrow(s, "Finding 2  ·  24 cells  ·  9,269 trials  ·  four independent stimulus designs")
    heading(s, "No self-advantage in any design — replicated four times", size=34)

    rows = [
        ("Stimulus set", "Surface baseline", "Self-advantage", "Interaction"),
        ("VO-D  (style-equalised)", "0.55 / 0.54", "+0.000 [−0.015, +0.015]", "−0.006 [−0.033, +0.021]"),
        ("VO-B", "0.65 / 0.75", "+0.000 [−0.033, +0.035]", "+0.005 [−0.040, +0.050]"),
        ("VO-A", "0.66 / 0.75", "+0.020 [−0.015, +0.056]", "−0.030 [−0.079, +0.018]"),
        ("VO-C  (leakiest)", "0.69 / 0.85", "−0.033 [−0.058, −0.008]", "+0.089 [+0.048, +0.131]"),
    ]
    tbl = s.shapes.add_table(len(rows), 4, MARGIN, Inches(2.2), BODY_W, Inches(2.4)).table
    for w, col in zip((Inches(3.3), Inches(2.3), Inches(3.1), Inches(2.9)), tbl.columns):
        col.width = w
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.runs[0]
            r.font.size = Pt(11 if ri else 10)
            r.font.name = MONO if (ri and ci) else SANS
            r.font.bold = (ri == 0) or (ri == 4)
            r.font.color.rgb = MUTED if ri == 0 else INK
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if ri % 2 else RGBColor(0xEE, 0xF3, 0xF6)
    body_text(s, [
        ("Not one set shows a positive self-advantage whose interval excludes zero. The only "
         "significant one is negative, and the only non-zero interaction belongs to the leakiest "
         "stimuli in the study.", {"bold": True}),
    ], y=Inches(5.0), size=15)
    rail(s, 5)

    # 06 — finding 3
    s = blank(prs)
    eyebrow(s, "Finding 3  ·  Binder's paradigm, black-box")
    heading(s, "One model really can predict itself. It still loses.", size=34)
    picture(s, "fig4_selfprediction.png", y=Inches(2.05), height=Inches(3.9))
    caption(s, "“Which of these two replies would you produce?”  Hermes-3 discriminates "
               "genuinely (+0.437 hit minus false-alarm); Llama-3.1 answers by position and shows "
               "none. An 18-feature regression does the same job at 0.831.", y=Inches(6.05))
    rail(s, 6)

    # 07 — released tool
    s = blank(prs)
    eyebrow(s, "What we release")
    heading(s, "Two checks that cost nothing and changed everything")
    for i, (title, code, desc) in enumerate([
        ("Surface-leakage gate", "gate(texts, labels, groups)",
         "Can a trivial style classifier already solve your hidden property? If yes, an "
         "above-chance result does not distinguish self-knowledge from style-reading. "
         "Cross-validation is grouped by source prompt by default."),
        ("Response-bias check", "response_bias(answers)",
         "Is the model answering the question, or answering by position? It caught two of our own "
         "results that would otherwise have published as clean nulls."),
    ]):
        x = MARGIN + i * (Inches(5.75))
        card = s.shapes.add_shape(1, x, Inches(2.4), Inches(5.3), Inches(2.5))
        card.fill.solid(); card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RULE; card.line.width = Pt(0.75); card.shadow.inherit = False
        tf = card.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.28); tf.margin_top = Inches(0.24)
        para(tf, title, size=17, bold=True, first=True, space_after=5)
        para(tf, code, size=12, font=MONO, color=ACCENT, space_after=9)
        para(tf, desc, size=13, color=MUTED, line=1.3)
    body_text(s, [("One self-contained file, numpy only  ·  tools/surface_leakage_gate.py",
                   {"size": 14, "color": ACCENT, "bold": True})], y=Inches(5.25))
    rail(s, 7)

    # 08 — limits
    s = blank(prs)
    eyebrow(s, "What we do not claim")
    heading(s, "The honest boundaries")
    bullets(s, [
        ("", "Not a refutation of Binder et al. — they finetune on ~30k examples; we prompt.", None),
        ("", "Nothing about consciousness, welfare or moral status. Prediction happens in a fresh "
             "session, so nothing here bears even on same-episode memory.", None),
        ("", "One lineage, one values dimension, one provider at one quantization.", None),
        ("", "Two of our three self-recognition framings produced degenerate answers. We report "
             "them as elicitation failures, not as nulls.", FLAG),
        ("", "The style-equalised condition leaves everyone near chance — there, “no "
             "self-advantage” is partly “no signal for anyone.”", None),
    ], y=Inches(2.45), size=14)
    rail(s, 8)

    # 09 — receipts
    s = blank(prs)
    eyebrow(s, "Receipts")
    heading(s, "What it took")
    stats = [("9,269", "scored trials across\n24 crossed cells", ACCENT),
             ("$3.12", "total API spend,\nof a $10 ceiling", ACCENT),
             ("0", "malformed\npredictions", ACCENT),
             ("15", "preregistered decisions,\n8 logged amendments", ACCENT),
             ("2", "artifacts caught before\nthey became findings", FLAG)]
    for i, (v, k, col) in enumerate(stats):
        x = MARGIN + i * Inches(2.35)
        tf = textbox(s, x, Inches(2.5), Inches(2.2), Inches(2.0))
        para(tf, v, size=40, font=MONO, color=col, bold=True, first=True, space_after=6)
        for line_txt in k.split("\n"):
            para(tf, line_txt, size=12, color=MUTED, space_after=1, line=1.2)
    body_text(s, [
        "Every call logged append-only with returned model, provider, tokens, cost and prompt hash. "
        "Provider pinned with fallbacks disabled — if generator and self-predictor were served at "
        "different quantizations, “same weights” would be false.",
    ], y=Inches(5.0), size=14)
    rail(s, 9)

    # 10 — takeaway
    s = blank(prs, WHITE)
    eyebrow(s, "Takeaway")
    heading(s, "Ask the model. Then ask a regression.", y=Inches(1.6), size=48)
    tf = textbox(s, MARGIN, Inches(3.5), Inches(9.8), Inches(2.2))
    para(tf, "If eighteen surface features beat the model at recognising its own writing, an "
             "above-chance self-report is not evidence of privileged access.",
         size=21, color=MUTED, first=True, line=1.3, space_after=18)
    para(tf, "Fit the baseline per condition, on the same stimuli. Print the answer distribution "
             "next to every accuracy. Both are free, and in our hands both were decisive.",
         size=16, color=INK, line=1.35)
    rail(s, 10)

    prs.save(OUT)
    print(f"-> {OUT.name}  ({OUT.stat().st_size/1024:.0f} KB, {len(prs.slides.__iter__.__self__._sldIdLst)} slides)")


if __name__ == "__main__":
    build()
