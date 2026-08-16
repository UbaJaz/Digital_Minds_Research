"""Build and validate the judge-facing submission report.

  submission_report.md  ->  Submission_Report.docx   (pandoc)
                        ->  Submission_Report.pdf    (headless Chrome, for the page count)

The PDF is what makes "<= 8 rendered pages" a checked fact rather than an estimate: the
markdown is rendered to HTML with an explicit A4 print stylesheet (11pt body, 2 cm margins
-- ordinary academic settings, not a page-count trick), printed by headless Chrome, and the
page count read back off the PDF. The build FAILS if it exceeds PAGE_LIMIT.

Two guards run before anything is written, on both the submission report and the full
technical report:

  * FORBIDDEN -- placeholders and retracted claims that must never reach a submission file.
  * REQUIRED  -- disclosures the 2026-08-16 forensic review (A9) added. If one of these
    stops appearing, an edit has quietly dropped a correction.

Read-only with respect to the markdown sources. No API calls, no new analysis: every number
in submission_report.md is transcribed from 10_report.md.

Run:  .venv/Scripts/python scripts/build_submission.py
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUB_MD = ROOT / "submission_report.md"
FULL_MD = ROOT / "docs" / "10_report.md"
SUB_DOCX = ROOT / "Submission_Report.docx"
SUB_PDF = ROOT / "Submission_Report.pdf"
FULL_DOCX = ROOT / "10_Report.docx"

PAGE_LIMIT = 8

# The submission report sizes its figures with `{width=...}`, which the bare gfm reader
# emits as literal text. The full report carries no such attributes, so it stays on plain
# gfm rather than risking a brace elsewhere being reinterpreted.
SUB_READER = "gfm+attributes"

TITLE = "Beaten by a Cheap Surface Classifier: A Capability-Controlled Test of Privileged Self-Access"
AUTHORS = ["Ubayd Hattas", "Jaswin Chinthala"]

# A placeholder or a retracted claim must never reach a submission file.
FORBIDDEN = [
    "⟦FILL", "not countersigned", "four independent stimulus designs", "A9_DRAFT",
    "never the best", "fully explained by style", "awaiting Jaswin's confirmation",
]

# Disclosures that must survive every edit, per document.
REQUIRED_BOTH = [
    "0.719", "0.808", "0.831", "+0.381", "+0.089", "9,269",
    "post hoc", "shared 200-prompt pool", "necessary but not sufficient",
    "not preregistration", "after the results were known",
    "Ubayd Hattas", "Jaswin Chinthala", "University of Cape Town",
    "github.com/UbaJaz/Digital_Minds_Research",
]
REQUIRED_SUB = REQUIRED_BOTH + [
    "0.364", "0.343", "below the preregistered floor", "substituted after the pilot",
    "different evaluation procedure", "no test is run between them",
]
REQUIRED_FULL = REQUIRED_BOTH + ["substituted an estimand", "below the preregistered floor"]

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "google-chrome", "chromium", "chromium-browser",
]

# 11pt on A4 at 2 cm margins is a normal manuscript setting. The page limit is met by
# writing less, not by shrinking type.
PRINT_CSS = """
@page { size: A4; margin: 18mm 20mm 16mm; }
html { font-size: 11pt; }
body { font-family: Calibri, "Segoe UI", Carlito, sans-serif; line-height: 1.28;
       color: #111; margin: 0; }
h1 { font-size: 1.62rem; line-height: 1.18; margin: 0 0 .45rem; }
h2 { font-size: 1.12rem; margin: .85rem 0 .3rem; border-bottom: 1px solid #bbb;
     padding-bottom: .12rem; page-break-after: avoid; }
p, li { margin: 0 0 .4rem; text-align: justify; hyphens: auto; }
blockquote { margin: .5rem 0; padding: .35rem .8rem; border-left: 3px solid #888;
             background: #f4f4f4; }
blockquote p { margin: 0; }
ul { margin: 0 0 .5rem; padding-left: 1.15rem; }
table { border-collapse: collapse; width: 100%; font-size: .84rem; margin: .45rem 0 .35rem;
        page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: .2rem .35rem; text-align: left;
         vertical-align: top; }
th { background: #eee; }
img { display: block; margin: .5rem auto .25rem; max-width: 100%; height: auto; }
figure, p:has(> img) { page-break-inside: avoid; }
pre { background: #f4f4f4; border: 1px solid #ddd; padding: .4rem .6rem; font-size: .78rem;
      overflow-x: auto; page-break-inside: avoid; }
code { font-family: Consolas, monospace; font-size: .88em; }
/* the reference list, set one step down as reference lists conventionally are */
ol { padding-left: 1.3rem; font-size: .86rem; line-height: 1.22; }
ol li { margin-bottom: .22rem; }
"""


def guard(path: Path, required: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    bad = [f for f in FORBIDDEN if f in text]
    if bad:
        sys.exit(f"FAIL: {path.name} contains {bad}; refusing to build a submission file.")
    missing = [r for r in required if r not in text]
    if missing:
        sys.exit(f"FAIL: {path.name} dropped required disclosures: {missing}")
    return text


def cross_check(sub: str, full: str) -> None:
    """No number may appear in the submission report that is not in the full report."""
    def nums(t: str) -> set[str]:
        return set(re.findall(r"(?<![\w.])[-+−]?\d+\.\d+(?![\w])", t))
    extra = nums(sub) - nums(full)
    if extra:
        sys.exit(f"FAIL: submission report contains numbers absent from 10_report.md: "
                 f"{sorted(extra)}")
    print("cross-check: every decimal in the submission report also appears in 10_report.md")


def pandoc(src: Path, out: Path, title: str, reader: str = "gfm") -> None:
    exe = shutil.which("pandoc")
    if not exe:
        sys.exit("FAIL: pandoc is not on PATH.")
    cmd = [exe, str(src), "-f", reader, "-o", str(out), "--standalone",
           f"--resource-path={ROOT}", "--metadata", f"title={title}"]
    for a in AUTHORS:
        cmd += ["--metadata", f"author={a}"]
    try:
        subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    except PermissionError:
        sys.exit(f"FAIL: cannot write {out.name} — close it and re-run.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"FAIL: pandoc could not build {out.name}\n{e.stderr}")
    print(f"-> {out.name}  ({out.stat().st_size / 1024:.0f} KB, from {src.name})")


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if os.path.sep in c or ":" in c:
            if Path(c).exists():
                return c
        elif shutil.which(c):
            return shutil.which(c)
    sys.exit("FAIL: no Chrome/Chromium found; cannot verify the rendered page count.")


def render_pdf(src: Path, out: Path) -> int:
    """Markdown -> print-styled HTML -> PDF. Returns the rendered page count."""
    exe = shutil.which("pandoc")
    with tempfile.TemporaryDirectory() as td:
        body = Path(td) / "body.html"
        subprocess.run([exe, str(src), "-f", SUB_READER, "-t", "html", "-o", str(body)],
                       cwd=ROOT, check=True, capture_output=True, text=True)
        page = ROOT / "_submission_render.html"          # inside ROOT so figures/ resolves
        page.write_text(f"<!doctype html><meta charset='utf-8'><title>{TITLE}</title>"
                        f"<style>{PRINT_CSS}</style>\n"
                        + body.read_text(encoding="utf-8"), encoding="utf-8")
        try:
            subprocess.run([find_chrome(), "--headless", "--disable-gpu",
                            "--no-pdf-header-footer", f"--print-to-pdf={out}",
                            page.resolve().as_uri()],
                           check=True, capture_output=True, text=True, timeout=180)
        finally:
            page.unlink(missing_ok=True)
    from pypdf import PdfReader
    return len(PdfReader(str(out)).pages)


def main() -> None:
    sub = guard(SUB_MD, REQUIRED_SUB)
    full = guard(FULL_MD, REQUIRED_FULL)
    cross_check(sub, full)

    print(f"submission report: {len(sub.split()):,} words | "
          f"full report: {len(full.split()):,} words")

    pandoc(SUB_MD, SUB_DOCX, TITLE, reader=SUB_READER)
    pandoc(FULL_MD, FULL_DOCX, TITLE)

    pages = render_pdf(SUB_MD, SUB_PDF)
    print(f"-> {SUB_PDF.name}  ({SUB_PDF.stat().st_size / 1024:.0f} KB, "
          f"{pages} rendered pages, limit {PAGE_LIMIT})")
    if pages > PAGE_LIMIT:
        sys.exit(f"FAIL: submission report renders to {pages} pages, over the "
                 f"{PAGE_LIMIT}-page limit. Cut text — do not shrink the type.")
    print("checks passed: no placeholders, all disclosures present, no invented numbers, "
          f"{pages} <= {PAGE_LIMIT} pages")


if __name__ == "__main__":
    main()
