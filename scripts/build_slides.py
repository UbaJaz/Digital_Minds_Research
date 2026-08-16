"""Build the presentation as a single self-contained HTML file — six slides.

Same content and visual language as Digital_Minds_Track3_Slides.pptx: the palette and
typography are carried over from the team's previous hackathon deck (AfriGuard, June 2026)
— dark ground, one amber accent for figures, blue for the external observer, red reserved
for caveats. The deck commits to a dark look deliberately and paints its own background,
so it renders identically whatever the viewer's theme is.

Figures are embedded as data URIs so the file needs no external host.
Every number here comes from 10_report.md. Nothing is computed in this script.

Run:  .venv/Scripts/python scripts/build_slides.py  ->  presentation.html
"""

from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "presentation.html"


def data_uri(name: str) -> str:
    return "data:image/png;base64," + base64.b64encode((FIG / name).read_bytes()).decode("ascii")


F1 = data_uri("fig1_self_vs_surface.png")

CSS = """
:root{
  --ground:#0D1117; --panel:#161B22; --panel2:#1A1F2E; --rule:#2A323C;
  --ink:#E9EEF4; --muted:#98A3B0; --dim:#6B7683;
  --amber:#F0C040; --blue:#4A90D9; --red:#E24A4A; --green:#4A9B4A;
  --green-bg:#1F3324;
  --sans:Calibri,"Segoe UI",system-ui,-apple-system,sans-serif;
  --mono:Consolas,ui-monospace,"SF Mono",Menlo,monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--sans); line-height:1.45; -webkit-font-smoothing:antialiased;
  scroll-snap-type:y mandatory; overflow-y:scroll; height:100vh;
}
.slide{
  min-height:100vh; scroll-snap-align:start;
  padding:clamp(1.5rem,3.6vw,3rem) clamp(1.1rem,3.6vw,3.4rem) 3.2rem;
  display:flex; flex-direction:column; position:relative;
}
.eyebrow{
  font-family:var(--mono); font-size:clamp(.66rem,.82vw,.8rem); letter-spacing:.16em;
  text-transform:uppercase; color:var(--amber); margin:0 0 .9rem;
}
h1{
  font-size:clamp(2.2rem,4.6vw,3.6rem); font-weight:700; line-height:1.04;
  margin:0 0 .3rem; letter-spacing:-.015em; text-wrap:balance;
}
h2{
  font-size:clamp(1.5rem,2.8vw,2.35rem); font-weight:700; line-height:1.1;
  margin:0 0 1rem; letter-spacing:-.012em; text-wrap:balance;
}
p{margin:0 0 .8rem; font-size:clamp(.95rem,1.12vw,1.08rem); color:var(--muted); max-width:96ch}
p strong{color:var(--ink); font-weight:700}
.lede{font-size:clamp(1.05rem,1.35vw,1.3rem); max-width:70ch}
.k-green{color:var(--green); font-weight:700}
.k-amber{color:var(--amber); font-weight:700}
.k-blue{color:var(--blue); font-weight:700}
.k-red{color:var(--red); font-weight:700}
code,.mono{font-family:var(--mono); font-variant-numeric:tabular-nums}
.foot{
  position:absolute; left:clamp(1.1rem,3.6vw,3.4rem); right:clamp(1.1rem,3.6vw,3.4rem);
  bottom:1.15rem; border-top:1px solid var(--rule); padding-top:.5rem;
  font-family:var(--mono); font-size:.74rem; color:var(--dim);
}
.foot b{color:var(--amber)}
.grid{display:grid; gap:1rem}
.cards-3{grid-template-columns:repeat(3,1fr)}
.card{
  background:var(--panel); border:1px solid var(--rule); border-radius:3px;
  padding:1rem 1.1rem;
}
.card h3{margin:0 0 .35rem; font-size:1.02rem; font-weight:700; color:var(--ink)}
.card p{margin:0; font-size:.9rem}
.big{font-family:var(--mono); font-weight:700; line-height:1; font-variant-numeric:tabular-nums}
.rulebar{height:1px; background:var(--rule); margin:1.2rem 0}
/* the report figure is a light-background PNG: mat it on white so it reads as an exhibit,
   and cap its height so the caption can never be pushed into the footer rule */
.figcol{max-width:40rem}
figure{margin:0; background:#fff; padding:.5rem; border-radius:3px}
figure img{width:100%; height:auto; max-height:56vh; object-fit:contain; display:block}
.callout{border:1px solid var(--amber); background:var(--panel); border-radius:3px; padding:.9rem 1rem}
.caveat{border:1px solid var(--red); background:var(--panel); border-radius:3px; padding:.85rem 1rem}
.caveat p, .callout p{margin:0; font-size:.92rem; color:var(--ink)}
.residual{border:1px solid var(--green); background:var(--green-bg); border-radius:3px; padding:.9rem 1.05rem}
.strip{background:var(--panel2); border-radius:3px; padding:.7rem 1rem; font-size:.92rem; color:var(--muted)}
.strip b{color:var(--ink)}
.micro{font-family:var(--mono); font-size:.74rem; color:var(--dim); margin:.55rem 0 0}
table{border-collapse:collapse; width:100%; font-size:.92rem}
th{
  text-align:left; padding:.55rem .7rem; font-family:var(--sans); font-size:.76rem;
  letter-spacing:.04em; color:var(--dim); font-weight:600; border-bottom:2px solid var(--rule);
  vertical-align:bottom;
}
td{padding:.55rem .7rem; border-bottom:1px solid var(--rule); color:var(--ink)}
td.n{font-family:var(--mono); font-variant-numeric:tabular-nums}
tr.hi td{background:var(--panel2); color:var(--amber); font-weight:700}
.scroller{overflow-x:auto}
.track{height:9px; background:var(--panel2); border-radius:2px; margin:.7rem 0 .3rem}
.track span{display:block; height:100%; border-radius:2px}
.axis{display:flex; justify-content:space-between; font-family:var(--mono); font-size:.68rem; color:var(--dim)}
.stage{background:var(--panel); border:1px solid var(--rule); border-radius:3px; padding:0 1.05rem 1.05rem}
.stage .bar{height:4px; margin:0 -1.05rem .9rem; border-radius:3px 3px 0 0}
.stage .num{font-family:var(--mono); font-size:1.35rem; font-weight:700; margin-right:.6rem}
.stage .kick{font-family:var(--mono); font-size:.78rem; letter-spacing:.1em; font-weight:700}
.stage h3{margin:.55rem 0 .5rem; font-size:1rem}
.stage p{font-size:.87rem; margin:0}
.band{border:1px solid var(--amber); background:var(--panel2); border-radius:3px;
      padding:.85rem 1.1rem; font-size:clamp(1rem,1.4vw,1.28rem); font-weight:700; color:var(--amber)}
.authors{display:flex; gap:2.6rem; flex-wrap:wrap; align-items:flex-start}
.authors div{font-size:.95rem}
.authors b{display:block; color:var(--ink); font-size:1.02rem; margin-bottom:.15rem}
.authors span{color:var(--muted); display:block; line-height:1.35}
.spacer{flex:1}
@media (max-width:900px){
  body{scroll-snap-type:none}
  .slide{min-height:auto; padding-bottom:2.4rem}
  .cards-3{grid-template-columns:1fr}
  .split{grid-template-columns:1fr !important}
}
"""


def slide_1() -> str:
    return f"""
<section class="slide">
  <div style="height:5px;background:var(--amber);margin:-1.5rem -3.4rem 1.6rem"></div>
  <p class="eyebrow">Digital Minds Research Sprint &middot; Track 3 &middot; Introspection &amp; Self-Report Reliability</p>
  <div class="spacer"></div>
  <h1>Beaten by Eighteen Features</h1>
  <h2 style="color:var(--amber);font-weight:600;margin-bottom:1.6rem">A Capability-Controlled Test of Privileged Self-Access</h2>
  <div style="width:12rem;height:2px;background:var(--rule);margin:0 0 1.4rem"></div>
  <p class="lede">Does behavioural self-prediction provide information unavailable to an
     external observer?</p>
  <div class="spacer"></div>
  <div class="authors">
    <div><b>Ubayd Hattas</b><span>Computer Science, Statistics &amp; Data Science</span><span>University of Cape Town</span></div>
    <div><b>Jaswin Chinthala</b><span>Electrical Engineering</span><span>University of Cape Town</span></div>
    <div style="margin-left:auto;text-align:right">
      <b class="mono" style="color:var(--amber)">9,269 scored trials &middot; $3.12</b>
      <span class="mono" style="font-size:.82rem">github.com/UbaJaz/Digital_Minds_Research</span>
    </div>
  </div>
  <div class="foot"><b>1</b> / 6 &nbsp;&nbsp;&nbsp; Beaten by Eighteen Features</div>
</section>"""


def slide_2() -> str:
    cells = ""
    for pred in ("M", "N", "F"):
        row = f'<div class="mono" style="color:var(--muted);font-size:.86rem;align-self:center">{pred} predicts</div>'
        for col in ("M", "N"):
            self_ = pred == col
            style = ("background:var(--green-bg);border:1px solid var(--green);color:var(--green);font-weight:700"
                     if self_ else "background:var(--panel2);border:1px solid var(--rule);color:var(--muted)")
            row += (f'<div class="mono" style="{style};border-radius:2px;padding:.4rem;'
                    f'text-align:center;font-size:.84rem">{pred}&rarr;{col}'
                    f'{"  self" if self_ else ""}</div>')
        cells += row
    return f"""
<section class="slide">
  <p class="eyebrow">The question, and the design that can answer it</p>
  <h2>Privileged access means beating a cheap observer</h2>
  <p><strong>Two confounds block any black-box test.</strong> The self predictor is usually also
     the strongest model in the comparison, and a hidden property may simply be legible in the
     text. We remove the first by construction and turn the second into a measurement.</p>

  <div class="grid split" style="grid-template-columns:1.55fr 1fr;align-items:start;margin:.6rem 0 1.1rem">
    <div class="grid cards-3">
      <div class="card">
        <p class="mono" style="margin:0 0 .3rem"><span style="color:var(--green);font-size:1.35rem;font-weight:700">M</span>
           <span style="color:var(--dim);font-size:.72rem;letter-spacing:.08em">&nbsp;TARGET</span></p>
        <h3>Llama-3.1-70B</h3><p>generates a column;<br>predicts both</p>
      </div>
      <div class="card">
        <p class="mono" style="margin:0 0 .3rem"><span style="color:var(--blue);font-size:1.35rem;font-weight:700">N</span>
           <span style="color:var(--dim);font-size:.72rem;letter-spacing:.08em">&nbsp;SIBLING</span></p>
        <h3>Hermes-3-70B</h3><p>same pretrained base;<br>different post-training</p>
      </div>
      <div class="card">
        <p class="mono" style="margin:0 0 .3rem"><span style="color:var(--muted);font-size:1.35rem;font-weight:700">F</span>
           <span style="color:var(--dim);font-size:.72rem;letter-spacing:.08em">&nbsp;FAR OBSERVER</span></p>
        <h3>Mistral-Small-24B</h3><p>different organisation,<br>base and family</p>
      </div>
    </div>
    <div>
      <p class="mono" style="color:var(--amber);font-size:.74rem;letter-spacing:.12em;margin:0 0 .5rem">CROSSED 2&times;2 &mdash; 24 CELLS</p>
      <div style="display:grid;grid-template-columns:5.2rem 1fr 1fr;gap:.3rem">
        <div></div>
        <div class="mono" style="color:var(--dim);font-size:.76rem;text-align:center">M's texts</div>
        <div class="mono" style="color:var(--dim);font-size:.76rem;text-align:center">N's texts</div>
        {cells}
      </div>
      <div class="callout" style="margin-top:.5rem;padding:.5rem .7rem">
        <p><span class="mono k-amber">D</span>&nbsp; surface baseline &mdash; the cheap third party</p>
      </div>
    </div>
  </div>

  <p><span class="k-green">Capability cancels.</span> An additive competence edge appears in both of
     M's cells, so it drops out of the interaction
     <code style="color:var(--ink)">(M&rarr;M &minus; N&rarr;M) &minus; (M&rarr;N &minus; N&rarr;N)</code>.</p>
  <p><span class="k-amber">Leakage becomes the variable.</span> Four stimulus constructions on one
     shared 200-prompt pool, spanning surface baselines 0.54&ndash;0.85, with D fit per target
     column and gated on <strong>before</strong> main data is collected.</p>
  <p><span class="k-blue">The criterion.</span> Privileged access requires beating an
     equal-or-lower-cost observer reading the same text &mdash; not merely beating chance.</p>

  <div class="spacer"></div>
  <div class="strip"><b>Ground truth is constructed, not elicited.</b> The label lives where the
     prediction code structurally cannot import it &mdash; no predictor, including Self, ever sees it.</div>
  <div class="foot"><b>2</b> / 6 &nbsp;&nbsp;&nbsp; Question and design</div>
</section>"""


def slide_3() -> str:
    return f"""
<section class="slide">
  <p class="eyebrow">Finding 1 &middot; the pilot, five persona pairs, ten generator columns</p>
  <h2>Persona prediction tracks a cheap surface signal</h2>
  <div class="grid split" style="grid-template-columns:1.05fr 1fr;align-items:start">
    <div class="figcol">
      <figure><img src="{F1}" alt="Self-prediction accuracy against surface-baseline accuracy,
        one point per persona pair and generator column."></figure>
      <p class="micro" style="margin-top:.6rem">Points at or below the diagonal: a stylometric
        baseline matches or beats the model.</p>
    </div>
    <div>
      <p class="big" style="font-size:2.5rem;color:var(--amber);margin:0 0 .3rem">r = +0.71</p>
      <p style="margin-bottom:1.1rem">correlation between self-prediction accuracy and the
         18-feature surface baseline, across ten columns</p>
      <p class="big" style="font-size:2.5rem;color:var(--amber);margin:0 0 .3rem">6 / 10</p>
      <p style="margin-bottom:1.1rem">columns where the surface baseline matches or beats the model
         at reading its own persona</p>
      <p class="big" style="font-size:2.5rem;color:var(--blue);margin:0 0 .3rem">0.325</p>
      <p style="margin-bottom:1.3rem">surface baseline on VO-D's M column once style is equalised
         &mdash; and the model falls to 0.500 with it</p>
      <div class="caveat"><p><span class="k-red">Caveat.</span> VO-D also changed the behavioural
        expression of the hidden property, so it is not a clean causal isolation of style: the two
        personas largely converged on the same recommendation.</p></div>
    </div>
  </div>
  <div class="foot"><b>3</b> / 6 &nbsp;&nbsp;&nbsp; Surface leakage</div>
</section>"""


def slide_4() -> str:
    rows = [
        ("VO-D  style-equalised", "0.55 / 0.54", "+0.000 [−0.015, +0.015]", "−0.006 [−0.033, +0.021]", False),
        ("VO-B  original", "0.65 / 0.75", "+0.000 [−0.033, +0.035]", "+0.005 [−0.040, +0.050]", False),
        ("VO-A  original", "0.66 / 0.75", "+0.020 [−0.015, +0.056]", "−0.030 [−0.079, +0.018]", False),
        ("VO-C  leakiest", "0.69 / 0.85", "−0.033 [−0.058, −0.008]", "+0.089 [+0.048, +0.131]", True),
    ]
    body = "".join(
        f'<tr class="{"hi" if hi else ""}"><td>{a}</td><td class="n">{b}</td>'
        f'<td class="n">{c}</td><td class="n">{d}</td></tr>'
        for a, b, c, d, hi in rows)
    return f"""
<section class="slide">
  <p class="eyebrow">Finding 2 &middot; 24 cells &middot; 9,269 scored trials &middot; zero malformed</p>
  <h2>No self-advantage on the target column &mdash; and one positive interaction</h2>
  <div class="grid split" style="grid-template-columns:2.6fr 1fr;align-items:start;margin-bottom:1rem">
    <div class="scroller">
      <table>
        <thead><tr><th>Stimulus set</th><th>Surface D<br>(M / N col)</th>
          <th>Self-advantage<br>M&rarr;M &minus; N&rarr;M</th>
          <th>Capability-controlled<br>interaction</th></tr></thead>
        <tbody>{body}</tbody>
      </table>
    </div>
    <div class="callout">
      <p class="big" style="font-size:2.1rem;color:var(--amber);margin-bottom:.25rem">+0.089</p>
      <p class="mono" style="font-size:.78rem;color:var(--muted);margin-bottom:.55rem">[+0.048, +0.131]</p>
      <p style="font-size:.9rem">The originally preregistered interaction &mdash; positive, on the
         leakiest set in the study. We report it rather than bury it.</p>
    </div>
  </div>
  <p><strong>Not one construction shows a positive M-target self-advantage whose interval excludes
     zero.</strong> The single significant value on that contrast is <span class="k-red">negative</span>
     &mdash; and on VO-C's M column the self model is the worst of the three predictors of its own
     output (M&rarr;M 0.603, below N&rarr;M 0.636 and F&rarr;M 0.628).</p>
  <p><span class="k-amber">Positive interaction, but predictor-by-column differences prevent it from
     uniquely identifying privileged access.</span> It is positive because M <strong>under</strong>-performs
     on N's column, not because it over-performs on its own &mdash; and the estimator cancels only
     the additive part.</p>
  <div class="spacer"></div>
  <div class="strip"><b>Four stimulus constructions &middot; shared 200-prompt pool</b>
     &nbsp;&nbsp;&nbsp;<span style="color:var(--dim);font-size:.82rem">Preregistered floor 500/cell;
     achieved ~400; VO-D N = 323. Prompt-clustered bootstrap throughout.</span></div>
  <div class="foot"><b>4</b> / 6 &nbsp;&nbsp;&nbsp; Crossed design</div>
</section>"""


def slide_5() -> str:
    lo, hi = 0.50, 0.90
    bars = [
        ("Hermes-3 self-prediction", "0.719",
         "balanced accuracy [0.675, 0.762]<br>discrimination +0.437", "var(--green)", 0.719),
        ("Length-only observer", "0.808", "&ldquo;pick the longer reply&rdquo;<br>one feature, no training", "var(--blue)", 0.808),
        ("18-feature surface classifier", "0.831", "supervised single-text<br>authorship labelling", "var(--amber)", 0.831),
    ]
    cards = "".join(
        f"""<div class="card">
          <h3>{t}</h3>
          <p class="big" style="font-size:2.9rem;color:{c};margin:.3rem 0 .5rem">{v}</p>
          <p>{note}</p>
          <div class="track"><span style="width:{(val - lo) / (hi - lo) * 100:.1f}%;background:{c}"></span></div>
          <div class="axis"><span>0.50 chance</span><span>0.90</span></div>
        </div>""" for t, v, note, c, val in bars)
    return f"""
<section class="slide">
  <p class="eyebrow">Finding 3 &middot; &ldquo;which of these two replies would you produce?&rdquo; &middot; 391 pairs</p>
  <h2>Hermes-3 can predict itself. A cheaper observer still does better.</h2>
  <div class="grid cards-3" style="margin-bottom:.9rem">{cards}</div>
  <p style="font-size:.92rem">Only the length rule is matched to the model's task item-for-item
     <code style="color:var(--ink)">(paired difference +0.095 [+0.036, +0.155], McNemar p = 0.0018)</code>.
     The classifier is a different evaluation procedure &mdash; a cost criterion, not a matched score.</p>
  <div class="grid split" style="grid-template-columns:1.9fr 1fr;align-items:stretch;margin:.3rem 0 .9rem">
    <div class="residual">
      <p style="color:var(--ink);font-weight:700;margin-bottom:.25rem">Hermes still discriminates
         where the length cue points away from its own reply:</p>
      <p class="big" style="font-size:1.7rem;color:var(--green);margin:0 0 .4rem">+0.381 [0.188, 0.566]</p>
      <p style="font-size:.88rem;margin:0">75 pairs where a pure length strategy is actively wrong.
         This study cannot name the residual.</p>
    </div>
    <div class="card">
      <h3>Llama-3.1: no self-prediction</h3>
      <p>Discrimination &minus;0.107 [&minus;0.166, &minus;0.048]; 89.7% &ldquo;A&rdquo;.
         One model's ability, not a property of language models.</p>
    </div>
  </div>
  <div class="spacer"></div>
  <div class="band" style="color:var(--ink);background:var(--ground)">
    <span class="k-amber">Self-prediction is possible.</span> Privileged self-access is not thereby demonstrated.
  </div>
  <p class="micro">post hoc analyses &middot; 0.719 and 0.831 are different evaluation procedures,
     and no statistical test is run between them</p>
  <div class="foot"><b>5</b> / 6 &nbsp;&nbsp;&nbsp; Self-prediction</div>
</section>"""


def slide_6() -> str:
    stages = [
        ("1", "DISSOCIATE", "var(--green)", "Self-preference vs self-prediction",
         "Re-run the probe on the same pairs under two questions &mdash; &ldquo;which would you "
         "produce?&rdquo; against &ldquo;which is better?&rdquo;. A residual as large under the "
         "quality question reads as self-preference; one specific to the prediction framing is the "
         "discriminating outcome. Needs a behavioural manipulation check run before collection."),
        ("2", "AUDIT", "var(--blue)", "Apply the controls to existing claims",
         "Take the leakage gate and the response-bias check to published behavioural introspection "
         "results, and ask how many survive controls this cheap. No new model runs; it tests "
         "whether the framework generalises beyond our stimuli."),
        ("3", "TEST", "var(--amber)", "Stronger causal ground truth &mdash; conditional",
         "Only if a residual survives Stage 1 and audited effects do not dissolve: a "
         "training-relationship ladder against our one-lineage limit, activation steering or an "
         "independently planted property so ground truth is verified rather than assumed, and an "
         "incremental-validity test against an observer's features."),
    ]
    cards = "".join(
        f"""<div class="stage">
          <div class="bar" style="background:{c}"></div>
          <span class="num" style="color:{c}">{n}</span><span class="kick" style="color:{c}">{k}</span>
          <h3>{t}</h3><p>{b}</p>
        </div>""" for n, k, c, t, b in stages)
    return f"""
<section class="slide">
  <p class="eyebrow">Where this goes next</p>
  <h2>A decision tree, not a schedule</h2>
  <p class="lede">One question is left open by our own data: <strong>what is the model-specific
     residual that survives control of cheap surface cues, and can a behavioural test be built in
     which a positive privileged-access result would be identifiable?</strong></p>
  <div class="grid cards-3" style="margin:.9rem 0 1rem;align-items:stretch">{cards}</div>
  <p class="micro" style="font-size:.82rem">If Stage 1 dissolves the residual, that is the result
     and Stage 3 does not run. The bottleneck is breadth and experimental design, not implementation.</p>
  <div class="spacer"></div>
  <div class="band">Can behavioural self-prediction ever provide evidence unavailable to an
     external observer?</div>
  <div class="foot"><b>6</b> / 6 &nbsp;&nbsp;&nbsp; Future work</div>
</section>"""


def build() -> str:
    return ("<title>Beaten by Eighteen Features</title>\n"
            f"<style>{CSS}</style>\n"
            + slide_1() + slide_2() + slide_3() + slide_4() + slide_5() + slide_6() + "\n")


if __name__ == "__main__":
    html = build()
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"-> {OUT.name}  ({len(html.encode('utf-8')) / 1024:.0f} KB, 6 slides)")
