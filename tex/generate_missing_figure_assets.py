#!/usr/bin/env python3
"""Generate missing integrated-document figure PNGs with LuaLaTeX/TikZ.

This is a project-local fallback for figure assets already normalized into
``swebok_v4_ch01_06_ja_figures_manifest.tsv``.  It keeps the same quiet visual
style as the integrated document and only creates files that do not exist yet.
"""

from __future__ import annotations

import csv
import os
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX_DIR = ROOT / "tex"
MANIFEST = TEX_DIR / "swebok_v4_ch01_06_ja_figures_manifest.tsv"
TMP_DIR = TEX_DIR / ".figure-build"


def tex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def split_items(raw: str) -> list[str]:
    items = [item.strip() for item in raw.split(" / ") if item.strip()]
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        item = re.sub(r"\s+", " ", item)
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result[:8]


def node_grid(items: list[str]) -> str:
    if not items:
        return ""
    positions = [
        (-4.7, 1.2),
        (-2.35, 1.2),
        (0.0, 1.2),
        (2.35, 1.2),
        (4.7, 1.2),
        (-3.5, -1.1),
        (0.0, -1.1),
        (3.5, -1.1),
    ]
    lines: list[str] = []
    for idx, (item, (x, y)) in enumerate(zip(items, positions, strict=False), start=1):
        lines.append(
            rf"\node[card] (n{idx}) at ({x},{y}) {{\small {tex_escape(item)}}};"
        )
    for idx in range(1, len(items) + 1):
        lines.append(rf"\draw[link] (center) -- (n{idx});")
    return "\n".join(lines)


def figure_tex(title: str, center: str, items: list[str], layout: str) -> str:
    escaped_title = tex_escape(title)
    escaped_center = tex_escape(center)
    subtitle = {
        "radial": "中心概念と周辺要素の関係",
        "flow": "左から右へ読む流れ",
        "stack": "階層として読む整理",
        "matrix": "比較して読む整理",
        "cards": "要点をカードで整理",
    }.get(layout, "要点を整理")
    return rf"""
\documentclass[border=0pt]{{ltjsarticle}}
\usepackage[paperwidth=160mm,paperheight=90mm,margin=0mm]{{geometry}}
\usepackage[haranoaji]{{luatexja-preset}}
\usepackage{{tikz}}
\usetikzlibrary{{arrows.meta,positioning,calc}}
\pagestyle{{empty}}
\definecolor{{figbg}}{{HTML}}{{F7F5F2}}
\definecolor{{figsurface}}{{HTML}}{{FFFFFF}}
\definecolor{{figink}}{{HTML}}{{0F172A}}
\definecolor{{figmuted}}{{HTML}}{{475569}}
\definecolor{{figteal}}{{HTML}}{{0F766E}}
\definecolor{{figline}}{{HTML}}{{CBD5E1}}
\begin{{document}}
\noindent
\begin{{tikzpicture}}[
  x=1cm,y=1cm,
  card/.style={{draw=figline, fill=figsurface, rounded corners=2pt, line width=0.5pt,
    align=center, text=figink, minimum width=2.0cm, minimum height=0.82cm,
    text width=2.0cm, inner sep=4pt}},
  centerbox/.style={{draw=figteal, fill=figsurface, rounded corners=3pt, line width=0.9pt,
    align=center, text=figink, minimum width=3.2cm, minimum height=1.1cm,
    text width=3.2cm, inner sep=5pt, font=\bfseries}},
  link/.style={{draw=figteal!75, line width=0.65pt, -{{Stealth[length=2mm]}}}}
]
\fill[figbg] (-8,-4.5) rectangle (8,4.5);
\node[anchor=west, text=figink, font=\Large\bfseries] at (-7.25,3.65) {{{escaped_title}}};
\node[anchor=west, text=figmuted, font=\small] at (-7.25,3.15) {{{tex_escape(subtitle)}}};
\draw[figteal, line width=1.0pt] (-7.25,2.85) -- (7.25,2.85);
\node[centerbox] (center) at (0,0) {{{escaped_center}}};
{node_grid(items)}
\node[anchor=east, text=figmuted, font=\scriptsize] at (7.25,-3.9) {{SWEBOK v4.0a 日本語統合まとめ}};
\end{{tikzpicture}}
\end{{document}}
""".strip()


def render_one(row: dict[str, str]) -> bool:
    out_path = TEX_DIR / row["image_path"]
    if out_path.exists():
        return False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    stem = out_path.stem
    workdir = TMP_DIR / f"{row['chapter']}-{row['index']}-{stem}"
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    tex_path = workdir / f"{stem}.tex"
    tex_path.write_text(
        figure_tex(row["title"], row["center"], split_items(row["items"]), row["layout"]),
        encoding="utf-8",
    )
    env = os.environ.copy()
    texmfvar = TMP_DIR / "texmf-var"
    texmfvar.mkdir(exist_ok=True)
    env["TEXMFVAR"] = str(texmfvar)
    subprocess.run(
        ["lualatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=workdir,
        check=True,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["pdftoppm", "-png", "-singlefile", "-r", "180", f"{stem}.pdf", stem],
        cwd=workdir,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.copy2(workdir / f"{stem}.png", out_path)
    return True


def main() -> None:
    with MANIFEST.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    created = 0
    for row in rows:
        if render_one(row):
            created += 1
    old_cache = ROOT / ".texmf-var"
    if old_cache.exists():
        shutil.rmtree(old_cache)
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    print(f"created {created} missing figure asset(s)")


if __name__ == "__main__":
    main()
