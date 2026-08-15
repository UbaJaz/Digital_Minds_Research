"""Build the presentation as a single self-contained HTML file.

Figures are embedded as data URIs because the artifact CSP blocks every external host.
Run:  .venv/Scripts/python scripts/build_slides.py  ->  presentation.html
"""

from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"


def data_uri(name: str) -> str:
    b = (FIG / name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode("ascii")


F1 = data_uri("fig1_self_vs_surface.png")
F2 = data_uri("fig2_leakage_manipulation.png")
F4 = data_uri("fig4_selfprediction.png")

HTML = f"""<title>Beaten by Eighteen Features</title>
<style>
  /* ---- tokens: light is the base; both dark paths redefine the same names ---- */
  :root {{
    --ground:#F6F8FA; --surface:#FFFFFF; --ink:#12171F; --muted:#59636F;
    --rule:#DCE2E8; --accent:#0F6E8C; --accent-soft:#E4EFF4; --flag:#B03A26;
    --shadow:0 1px 2px rgba(18,23,31,.05), 0 8px 24px rgba(18,23,31,.06);
    --serif:"Iowan Old Style",Georgia,"Times New Roman",serif;
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
    --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  }}
  @media (prefers-color-scheme:dark) {{
    :root:not([data-theme="light"]) {{
      --ground:#0D1117; --surface:#161B22; --ink:#E6EAF0; --muted:#96A1AE;
      --rule:#262D36; --accent:#56B4CE; --accent-soft:#15303B; --flag:#E0745C;
      --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.35);
    }}
  }}
  :root[data-theme="dark"] {{
    --ground:#0D1117; --surface:#161B22; --ink:#E6EAF0; --muted:#96A1AE;
    --rule:#262D36; --accent:#56B4CE; --accent-soft:#15303B; --flag:#E0745C;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.35);
  }}

  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--ground); color:var(--ink);
    font-family:var(--sans); line-height:1.55;
    scroll-snap-type:y mandatory; overflow-y:scroll; height:100vh;
  }}
  .slide {{
    min-height:100vh; scroll-snap-align:start; display:grid;
    grid-template-columns:4.5rem 1fr; align-items:center;
    padding:clamp(1.5rem,4vw,4rem) clamp(1rem,4vw,4rem);
    border-bottom:1px solid var(--rule);
  }}
  /* the rail carries the slide number: this is a linear talk, so ordinals are real information */
  .rail {{
    align-self:stretch; display:flex; flex-direction:column; align-items:center;
    padding-top:clamp(1.5rem,6vh,4rem); gap:.75rem;
  }}
  .rail .num {{
    font-family:var(--mono); font-size:.8rem; letter-spacing:.08em;
    color:var(--accent); font-variant-numeric:tabular-nums;
  }}
  .rail .tick {{ flex:1; width:1px; background:var(--rule); }}
  .body {{ max-width:64rem; }}

  .eyebrow {{
    font-family:var(--mono); font-size:.72rem; letter-spacing:.16em;
    text-transform:uppercase; color:var(--muted); margin:0 0 1rem;
  }}
  h1 {{
    font-family:var(--serif); font-weight:600; font-size:clamp(2.1rem,5.4vw,4rem);
    line-height:1.08; margin:0 0 1.25rem; text-wrap:balance; letter-spacing:-.01em;
  }}
  h2 {{
    font-family:var(--serif); font-weight:600; font-size:clamp(1.6rem,3.4vw,2.6rem);
    line-height:1.15; margin:0 0 1.1rem; text-wrap:balance;
  }}
  p {{ margin:0 0 1rem; max-width:60ch; font-size:clamp(1rem,1.35vw,1.15rem); }}
  .lede {{ font-size:clamp(1.1rem,1.7vw,1.4rem); color:var(--muted); max-width:52ch; }}
  strong {{ font-weight:650; }}
  .flag {{ color:var(--flag); }}

  figure {{ margin:1rem 0 0; }}
  figure img {{
    width:100%; max-width:52rem; height:auto; display:block;
    background:#fff; border:1px solid var(--rule); border-radius:3px; box-shadow:var(--shadow);
  }}
  figcaption {{ font-size:.86rem; color:var(--muted); margin-top:.6rem; max-width:58ch; }}

  .stats {{ display:flex; flex-wrap:wrap; gap:1.5rem 2.75rem; margin:.5rem 0 1.25rem; }}
  .stat .v {{
    font-family:var(--mono); font-size:clamp(1.7rem,3.6vw,2.9rem); font-weight:600;
    color:var(--accent); font-variant-numeric:tabular-nums; line-height:1;
  }}
  .stat .v.flag {{ color:var(--flag); }}
  .stat .k {{ font-size:.82rem; color:var(--muted); margin-top:.4rem; max-width:22ch; }}

  .scroller {{ overflow-x:auto; margin:.5rem 0 1rem; }}
  table {{ border-collapse:collapse; font-size:.95rem; min-width:34rem; }}
  th, td {{ text-align:left; padding:.55rem .9rem; border-bottom:1px solid var(--rule); }}
  th {{
    font-family:var(--mono); font-size:.72rem; letter-spacing:.1em;
    text-transform:uppercase; color:var(--muted); font-weight:500;
  }}
  td.n {{ font-family:var(--mono); font-variant-numeric:tabular-nums; }}
  tr.hi td {{ background:var(--accent-soft); }}

  ul {{ margin:0 0 1rem; padding-left:1.1rem; max-width:60ch; }}
  li {{ margin-bottom:.55rem; font-size:clamp(1rem,1.3vw,1.12rem); }}
  li::marker {{ color:var(--accent); }}

  .card {{
    background:var(--surface); border:1px solid var(--rule); border-radius:4px;
    padding:1.1rem 1.3rem; box-shadow:var(--shadow); max-width:34rem;
  }}
  .cards {{ display:flex; flex-wrap:wrap; gap:1rem; margin-top:.5rem; }}
  .card h3 {{ margin:0 0 .4rem; font-size:1.02rem; font-family:var(--sans); }}
  .card code {{ font-family:var(--mono); font-size:.84rem; color:var(--accent); }}
  .card p {{ margin:0; font-size:.94rem; color:var(--muted); }}

  .byline {{ font-size:.95rem; color:var(--muted); margin-top:2rem; }}
  .kbd {{
    position:fixed; right:1rem; bottom:1rem; font-family:var(--mono); font-size:.7rem;
    letter-spacing:.06em; color:var(--muted); background:var(--surface);
    border:1px solid var(--rule); border-radius:3px; padding:.35rem .6rem; opacity:.85;
  }}
  @media (max-width:640px) {{
    .slide {{ grid-template-columns:2.25rem 1fr; }}
    .kbd {{ display:none; }}
  }}
  @media (prefers-reduced-motion:reduce) {{ html {{ scroll-behavior:auto; }} }}
  html {{ scroll-behavior:smooth; }}
</style>

<section class="slide">
  <div class="rail"><span class="num">01</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">Digital Minds Sprint · Track 3 · Introspection &amp; Self-Report Reliability</p>
    <h1>Beaten by eighteen features</h1>
    <p class="lede">Two 70-billion-parameter models were asked to pick out their own writing.
      A logistic regression on eighteen surface features did it better.</p>
    <p class="byline">Ubayd Hattas &amp; Jaswin Chinthala · with Apart Research · August 2026</p>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">02</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">Why it matters</p>
    <h2>Model welfare research runs on self-report</h2>
    <p>When we ask whether a model has preferences, is distressed, or is flourishing, we mostly
      ask <em>the model</em>. That only works if its report about itself carries information an
      outside observer could not get from the same text.</p>
    <p>Binder et al. say models have that privileged access. Song et al. say the apparent effect is
      just behavioural similarity. Settling it decides whether a whole class of welfare
      measurements means anything — and whether we over- or under-attribute moral significance.</p>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">03</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">The design</p>
    <h2>Two confounds, removed by construction</h2>
    <ul>
      <li><strong>Capability.</strong> The "self" model is usually also the smartest model in the
        comparison. We use two models sharing a pretraining base — Llama-3.1-70B and
        Hermes-3-70B — and a crossed 2&times;2, so a general competence edge cancels.</li>
      <li><strong>Surface leakage.</strong> A hidden property is only interesting if a third party
        can't read it off the text. We fit an 18-feature style classifier to every stimulus set
        and gate on it <em>before</em> collecting main data.</li>
    </ul>
    <p>Ground truth is constructed, not elicited: we set which persona writes each text and store
      the label where the prediction code structurally cannot reach it.</p>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">04</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">Finding 1</p>
    <h2>What looked like self-recognition was style-recognition</h2>
    <figure>
      <img src="{F1}" alt="Scatter of self-prediction accuracy against surface-baseline accuracy for ten conditions; points lie on or below the diagonal.">
      <figcaption>Ten conditions across five stimulus designs. Self-prediction tracks the style
        classifier at r = +0.71, and the classifier matches or beats the model in six of ten.
        Two scaffolds built to equalise style (orange) drive both to chance together.</figcaption>
    </figure>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">05</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">Finding 2 · 24 cells · 9,269 trials</p>
    <h2>No self-advantage in any stimulus design</h2>
    <div class="scroller">
      <table>
        <thead><tr><th>Stimulus set</th><th>Surface baseline</th><th>Self-advantage</th><th>Capability-controlled interaction</th></tr></thead>
        <tbody>
          <tr><td>VO-D <span style="color:var(--muted)">style-equalised</span></td><td class="n">0.55 / 0.54</td><td class="n">+0.000 [−0.015, +0.015]</td><td class="n">−0.006 [−0.033, +0.021]</td></tr>
          <tr><td>VO-B</td><td class="n">0.65 / 0.75</td><td class="n">+0.000 [−0.033, +0.035]</td><td class="n">+0.005 [−0.040, +0.050]</td></tr>
          <tr><td>VO-A</td><td class="n">0.66 / 0.75</td><td class="n">+0.020 [−0.015, +0.056]</td><td class="n">−0.030 [−0.079, +0.018]</td></tr>
          <tr class="hi"><td>VO-C <span style="color:var(--muted)">leakiest</span></td><td class="n">0.69 / <strong>0.85</strong></td><td class="n">−0.033 [−0.058, −0.008]</td><td class="n">+0.089 [+0.048, +0.131]</td></tr>
        </tbody>
      </table>
    </div>
    <p>Not one set shows a positive self-advantage excluding zero. The only significant one is
      <strong>negative</strong>, and the only non-zero interaction belongs to the leakiest stimuli
      in the study.</p>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">06</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">Finding 3 · Binder's paradigm, black-box</p>
    <h2>One model really can predict itself. It still loses.</h2>
    <figure>
      <img src="{F4}" alt="Bar chart: Llama-3.1 at 0.447 balanced accuracy, Hermes-3 at 0.719, surface baseline at 0.831.">
      <figcaption>"Which of these two replies would you produce?" Hermes-3 discriminates genuinely
        (+0.437 hit minus false-alarm). Llama-3.1 answers by position and shows none. An 18-feature
        regression does the same job at 0.831.</figcaption>
    </figure>
    <p>Song et al.'s test for introspection is that it must beat an equal-or-lower-cost third
      party. Real self-prediction, and it fails that test.</p>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">07</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">What we release</p>
    <h2>Two checks that cost nothing and changed everything</h2>
    <div class="cards">
      <div class="card">
        <h3>Surface-leakage gate</h3>
        <p><code>gate(texts, labels, groups)</code> — can a trivial style classifier already solve
          your hidden property? If yes, your above-chance result doesn't distinguish self-knowledge
          from style-reading. Cross-validation is grouped by source prompt by default.</p>
      </div>
      <div class="card">
        <h3>Response-bias check</h3>
        <p><code>response_bias(answers)</code> — is the model answering the question, or answering
          by position? It caught two of our own results that would otherwise have published as
          clean nulls.</p>
      </div>
    </div>
    <p style="margin-top:1.25rem">One self-contained file, numpy only.
      <code style="font-family:var(--mono);color:var(--accent)">tools/surface_leakage_gate.py</code></p>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">08</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">What we do not claim</p>
    <h2>The honest boundaries</h2>
    <ul>
      <li>Not a refutation of Binder et al. — they finetune on ~30k examples; we prompt.</li>
      <li>Nothing about consciousness, welfare, or moral status. Prediction happens in a fresh
        session, so nothing here bears even on same-episode memory.</li>
      <li>One lineage, one values dimension, one provider at one quantization.</li>
      <li class="flag">Two of our three self-recognition framings produced degenerate answers.
        We report them as elicitation failures, not as nulls.</li>
      <li>The style-equalised condition leaves everyone near chance — there, "no self-advantage"
        is partly "no signal for anyone."</li>
    </ul>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">09</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">Receipts</p>
    <h2>What it took</h2>
    <div class="stats">
      <div class="stat"><div class="v">9,269</div><div class="k">scored trials across 24 crossed cells</div></div>
      <div class="stat"><div class="v">$3.12</div><div class="k">total API spend, of a $10 ceiling</div></div>
      <div class="stat"><div class="v">0</div><div class="k">malformed predictions</div></div>
      <div class="stat"><div class="v">15</div><div class="k">preregistered decisions, 8 logged amendments</div></div>
      <div class="stat"><div class="v flag">2</div><div class="k">artifacts caught before they became findings</div></div>
    </div>
    <p>Every call logged append-only with returned model, provider, tokens, cost and prompt hash.
      Provider pinned with fallbacks disabled — if generator and self-predictor were served at
      different quantizations, "same weights" would be false.</p>
  </div>
</section>

<section class="slide">
  <div class="rail"><span class="num">10</span><span class="tick"></span></div>
  <div class="body">
    <p class="eyebrow">Takeaway</p>
    <h1>Ask the model. Then ask a regression.</h1>
    <p class="lede">If eighteen surface features beat the model at recognising its own writing,
      an above-chance self-report is not evidence of privileged access.</p>
    <p>Fit the baseline per condition, on the same stimuli. Print the answer distribution next to
      every accuracy. Both are free, and in our hands both were decisive.</p>
  </div>
</section>

<div class="kbd">&uarr; &darr; to navigate</div>
<script>
  document.addEventListener('keydown', function (e) {{
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'PageDown' && e.key !== 'PageUp') return;
    var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    var y = window.scrollY, cur = 0, best = Infinity;
    slides.forEach(function (s, i) {{
      var d = Math.abs(s.offsetTop - y);
      if (d < best) {{ best = d; cur = i; }}
    }});
    var next = (e.key === 'ArrowDown' || e.key === 'PageDown') ? cur + 1 : cur - 1;
    if (next < 0 || next >= slides.length) return;
    e.preventDefault();
    slides[next].scrollIntoView({{ behavior: 'smooth' }});
  }});
</script>
"""

out = ROOT / "presentation.html"
out.write_text(HTML, encoding="utf-8")
print(f"-> {out}  ({out.stat().st_size/1024:.0f} KB)")
