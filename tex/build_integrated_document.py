#!/usr/bin/env python3
"""Build the integrated SWEBOK Japanese chapter 01-06 TeX document.

The root TeX files use different engines and TODO figure macros.  This
generator normalizes them into one LuaLaTeX document and replaces every TODO
figure with a Codex/gpt-image-2-generated PNG asset reference.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "tex"
OUT_TEX = OUT_DIR / "swebok_v4_ch01_06_ja_integrated.tex"
MASTER_TEX = OUT_DIR / "swebok_v4_ch01_06_ja_master.tex"
PARTS_DIR = OUT_DIR / "chapters"
CH01_STRUCTURE_CHAPTER = (
    OUT_DIR
    / "swebok_structure"
    / "CH01.ソフトウェア要求(Software_Requirements)"
    / "1.0.導入(Introduction)"
    / "chapter.tex"
)
MANIFEST = OUT_DIR / "swebok_v4_ch01_06_ja_figures_manifest.tsv"
IMAGE_DIR = OUT_DIR / "assets" / "generated_figures"
PROMPT_DIR = OUT_DIR / "imagegen_prompts"
IMAGEGEN_MANIFEST = OUT_DIR / "swebok_v4_ch01_06_ja_imagegen_manifest.tsv"


@dataclass(frozen=True)
class Chapter:
    no: int
    title: str
    path: Path


@dataclass(frozen=True)
class FigureSpec:
    chapter: int
    index: int
    title: str
    prompt: str
    label: str
    layout: str
    center: str
    items: tuple[str, ...]

    @property
    def filename(self) -> str:
        return f"fig-ch{self.chapter:02d}-{self.index:02d}.png"

    @property
    def image_relpath(self) -> str:
        return f"assets/generated_figures/ch{self.chapter:02d}/{self.filename}"

    @property
    def prompt_relpath(self) -> str:
        return f"imagegen_prompts/ch{self.chapter:02d}/{self.filename.removesuffix('.png')}.md"


CHAPTERS = [
    Chapter(1, "ソフトウェア要求", ROOT / "software_requirements_chapter01_ja_A4_final (1).tex"),
    Chapter(2, "ソフトウェアアーキテクチャ", ROOT / "software_architecture_chapter02_ja_A4_final.tex"),
    Chapter(3, "ソフトウェア設計", ROOT / "software_design_chapter03_ja_A4_final.tex"),
    Chapter(4, "ソフトウェア構築", ROOT / "software_construction_chapter04_ja.tex"),
    Chapter(5, "ソフトウェアテスト", ROOT / "software_testing_chapter05_ja_A4_final.tex"),
    Chapter(6, "ソフトウェアエンジニアリング運用", ROOT / "software_engineering_operations_chapter06_ja.tex"),
]


PREAMBLE = r"""
\documentclass[a4paper,11pt]{ltjsarticle}
\usepackage[haranoaji]{luatexja-preset}
\usepackage{geometry}
\geometry{top=24mm,bottom=24mm,left=24mm,right=24mm,headheight=18pt}
\usepackage{setspace}
\setstretch{1.15}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{multirow}
\usepackage{multicol}
\usepackage{enumitem}
\usepackage{amsmath,amssymb}
\usepackage{xparse}
\usepackage[most]{tcolorbox}
\tcbuselibrary{breakable,skins}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,fit,shapes.geometric,calc}
\usepackage{titlesec}
\usepackage{hyperref}
\hypersetup{hidelinks,unicode=true,pdftitle={SWEBOK v4.0a 01-06 日本語統合まとめ},pdfauthor={OpenAI Codex}}

\setlength{\parindent}{1em}
\setlength{\parskip}{0.3em}
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.2}
\sloppy
\emergencystretch=3em
\setlist[itemize]{leftmargin=2em,itemsep=0.2em,topsep=0.2em}
\setlist[enumerate]{leftmargin=2em,itemsep=0.2em,topsep=0.2em}
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{3}

\renewcommand{\contentsname}{目次}
\renewcommand{\figurename}{図}
\renewcommand{\tablename}{表}
\renewcommand{\thefigure}{\arabic{figure}}
\renewcommand{\thetable}{\arabic{table}}

\definecolor{mainblue}{HTML}{000000}
\definecolor{lightblue}{HTML}{FFFFFF}
\definecolor{darkgray}{HTML}{333333}
\definecolor{lightgray}{HTML}{F5F5F5}
\definecolor{midgray}{HTML}{777777}
\definecolor{figbg}{HTML}{F7F5F2}
\definecolor{figsurface}{HTML}{FFFFFF}
\definecolor{figink}{HTML}{17211B}
\definecolor{figmuted}{HTML}{5B6470}
\definecolor{figteal}{HTML}{0F766E}
\definecolor{figgreen}{HTML}{2F7D4A}
\definecolor{figblue}{HTML}{2C7FB8}
\definecolor{figgold}{HTML}{E0A11B}
\definecolor{figred}{HTML}{D65A3A}
\definecolor{figline}{HTML}{CBD5E1}

\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{SWEBOK v4.0a 日本語統合まとめ}
\fancyhead[R]{第 01--06 章}
\fancyfoot[C]{\thepage/\pageref{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}

\titleformat{\section}{\Large\bfseries}{\thesection.}{0.8em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{0.8em}{}
\titleformat{\subsubsection}{\normalsize\bfseries}{\thesubsubsection}{0.8em}{}
\titleformat{\paragraph}{\normalsize\bfseries}{}{0em}{}
\titlespacing*{\section}{0pt}{1.1em}{0.4em}
\titlespacing*{\subsection}{0pt}{0.9em}{0.25em}
\titlespacing*{\subsubsection}{0pt}{0.6em}{0.15em}
\titlespacing*{\paragraph}{0pt}{0.6em}{0.5em}

\newtcolorbox{statementbox}[1]{enhanced,breakable,colback=white,colframe=black,boxrule=0.6pt,arc=0mm,left=1mm,right=1mm,top=1mm,bottom=1mm,title=\textbf{#1},fonttitle=\normalsize,coltitle=black,colbacktitle=white,attach boxed title to top left={xshift=1mm,yshift=-1mm},boxed title style={colback=white,colframe=white,arc=0mm,boxrule=0pt}}
\newtcolorbox{plainbox}{breakable,colback=white,colframe=black,boxrule=0.5pt,sharp corners,left=5pt,right=5pt,top=5pt,bottom=5pt}
\newtcolorbox{keybox}[1]{breakable,colback=white,colframe=black,boxrule=0.5pt,sharp corners,left=5pt,right=5pt,top=5pt,bottom=5pt,before upper={\textbf{#1}\par\smallskip}}
\newtcolorbox{pointbox}[1]{breakable,colback=white,colframe=black,title={#1},fonttitle=\bfseries,coltitle=black,colbacktitle=white,left=1.5mm,right=1.5mm,top=1mm,bottom=1mm,boxrule=0.5pt}
\newtcolorbox{notebox}[1]{breakable,colback=white,colframe=black,title={#1},fonttitle=\bfseries,coltitle=black,colbacktitle=white,left=1.5mm,right=1.5mm,top=1mm,bottom=1mm,boxrule=0.4pt}

\newcounter{definition}
\newtcolorbox{definitionbox}{enhanced,breakable,colback=white,colframe=black,boxrule=0.6pt,arc=0mm,left=1.5mm,right=1.5mm,top=1mm,bottom=1mm,title={定義 \refstepcounter{definition}\thedefinition},fonttitle=\bfseries,coltitle=black,colbacktitle=white}

\newcommand{\keyterm}[1]{\textbf{#1}}
\NewDocumentCommand{\term}{m g}{\textbf{#1}\IfNoValueF{#2}{（#2）}}
\newcommand{\en}[1]{（#1）}
\newcommand{\eng}[1]{\textsf{#1}}
\newcommand{\swebok}{\textit{SWEBOK Guide v4.0a}}
\newcommand{\Rule}{\par\smallskip\hrule\smallskip}
\newcommand{\MiniBox}[2]{\par\smallskip\begin{statementbox}{#1}#2\end{statementbox}\par\smallskip}
\newcommand{\SmallHead}[1]{\par\smallskip\noindent\textbf{#1}\quad}
""".strip()


DOCUMENT_OPENING = [
    r"\begin{document}",
    r"\thispagestyle{empty}",
    r"\begin{center}",
    r"{\LARGE\bfseries SWEBOK v4.0a 日本語統合まとめ}\par\vspace{1em}",
    r"{\Large 第 01--06 章}\par\vspace{0.8em}",
    r"{\large Software Requirements / Architecture / Design / Construction / Testing / Engineering Operations}\par\vspace{1em}",
    r"{作成日：2026 年 5 月 5 日}\par",
    r"\end{center}",
    r"\vspace{1em}\hrule\vspace{0.8em}",
    r"\tableofcontents",
]


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


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"を入れる。?$", "", title)
    title = re.sub(r"図を入れる。?$", "図", title)
    return title.strip("。 ")


def extract_quoted(text: str) -> list[str]:
    values = re.findall(r"「([^」]{1,28})」", text)
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = re.sub(r"\s+", " ", value).strip()
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def choose_layout(title: str, prompt: str) -> str:
    haystack = title + prompt
    if any(word in haystack for word in ("マトリクス", "比較表", "対応図", "分類図")):
        return "matrix"
    if any(word in haystack for word in ("時系列", "左から", "流れ", "パイプライン", "サイクル", "ループ")):
        return "flow"
    if any(word in haystack for word in ("層", "積み上げ", "三層", "四層", "階層")):
        return "stack"
    if any(word in haystack for word in ("中央に", "周囲", "放射状", "マップ", "地図")):
        return "radial"
    return "cards"


def build_items(title: str, prompt: str) -> tuple[str, tuple[str, ...]]:
    quoted = extract_quoted(prompt)
    cleaned = clean_title(title)
    center = quoted[0] if quoted else cleaned
    items = quoted[1:] if len(quoted) > 1 else []
    if not items:
        base = re.split(r"[、。，．・\s]+", re.sub(r"[「」]", "", prompt))
        items = [x for x in base if 2 <= len(x) <= 16 and not x.startswith("A4")]
    if not items:
        items = [cleaned]
    return center, tuple(items[:8])


def render_figure(spec: FigureSpec) -> str:
    missing = rf"\fbox{{\parbox[c][48mm][c]{{0.9\linewidth}}{{\centering 画像生成待ち\\{tex_escape(clean_title(spec.title))}}}}}"
    return "\n".join(
        [
            r"\begin{figure}[htbp]",
            r"\centering",
            rf"\IfFileExists{{{spec.image_relpath}}}{{\includegraphics[width=0.96\linewidth]{{{spec.image_relpath}}}}}{{{missing}}}",
            rf"\caption{{{tex_escape(clean_title(spec.title))}}}",
            rf"\label{{{spec.label}}}",
            r"\end{figure}",
        ]
    )


def imagegen_prompt(spec: FigureSpec) -> str:
    image_abs = OUT_DIR / spec.image_relpath
    manifest_abs = IMAGEGEN_MANIFEST
    prompt_abs = OUT_DIR / spec.prompt_relpath
    visible_labels = "\n".join(f"- {item}" for item in (spec.center, *spec.items))
    source_prompt = spec.prompt
    source_prompt = source_prompt.replace("白背景、モノクロ、", "温かいオフホワイト背景、控えめなアクセントカラー、")
    source_prompt = source_prompt.replace("白背景、モノクロ", "温かいオフホワイト背景、控えめなアクセントカラー")
    source_prompt = source_prompt.replace("モノクロ、", "控えめなカラー、")
    source_prompt = source_prompt.replace("モノクロ", "控えめなカラー")
    source_prompt = source_prompt.replace("白黒", "控えめなカラー")
    layout_instruction = {
        "radial": "中央に主概念を置き、周辺に関連項目を配置する放射状の図解。",
        "flow": "左から右へ進む工程図または循環を示すフロー図。",
        "stack": "上から下へ意味が積み重なる階層図。",
        "matrix": "比較しやすい 2x3 または 2x4 のマトリクス図。",
        "cards": "中心概念と複数カードを組み合わせた整理図。",
    }[spec.layout]
    return f"""$imagegen

目的:
SWEBOK v4.0a 日本語統合 A4 資料に埋め込む図を、gpt-image-2 の生成AI画像として1枚だけ作成する。
この実行では `{spec.label}` だけを個別に生成する。HTML/SVG/Canvas/TikZ/スクリーンショット等の決定的レンダリングで代替しない。

重要:
- built-in `image_gen` を Codex から呼び出して、この1枚を新規生成する。
- 生成後、最新の `$CODEX_HOME/generated_images/...` の PNG をプロジェクト側へコピーする。
- コピー先: `{image_abs}`
- このプロンプト: `{prompt_abs}`
- 成否を `{manifest_abs}` に TSV で1行追記する。形式は `label<TAB>status<TAB>source<TAB>destination<TAB>prompt`。
- 既存の TeX、SVG、TikZ、他章の画像を上書きしない。

共通デザイン:
- A4 横幅に入る 16:9 横長の日本語教育図解。高解像度 PNG。
- 背景 `#F7F5F2`、カード `#FFFFFF`、本文 `#0F172A`、補足 `#475569`、アクセント `#0F766E`、罫線 `#CBD5E1`。
- 静かで読みやすいスライド風デザイン。ただしスライド番号、ページ番号、ロゴ、透かしは入れない。
- 色合いは白黒に限定しない。本文資料の枠線は黒基調だが、図の中は上記パレットの控えめな色を使う。
- Noto Sans JP 風。日本語文字を最優先で正確・鮮明にする。
- タイトルは短く上部に配置し、本文はカードやラベル中心にする。長文段落は禁止。
- 装飾だけのアイコン、3D、強い影、グラデーション過多は禁止。

生成対象:
Title: {clean_title(spec.title)}
Layout: {layout_instruction}
Central concept: {spec.center}

Visible Japanese labels. Use these labels exactly where possible:
{visible_labels}

Meaning to convey:
{source_prompt}

完了条件:
- `{image_abs}` が存在する。
- `{manifest_abs}` に `{spec.label}` の success または failed 行を追記する。
- 最後に保存できたファイルパスだけを報告する。
"""


def write_imagegen_prompts(figures: list[FigureSpec]) -> None:
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for chapter in CHAPTERS:
        prompt_chapter_dir = PROMPT_DIR / f"ch{chapter.no:02d}"
        image_chapter_dir = IMAGE_DIR / f"ch{chapter.no:02d}"
        prompt_chapter_dir.mkdir(parents=True, exist_ok=True)
        image_chapter_dir.mkdir(parents=True, exist_ok=True)
        for existing in prompt_chapter_dir.glob("*.md"):
            existing.unlink()

    for spec in figures:
        prompt_path = OUT_DIR / spec.prompt_relpath
        prompt_path.write_text(imagegen_prompt(spec), encoding="utf-8")


def make_spec(chapter: int, index: int, title: str, prompt: str) -> FigureSpec:
    title = re.sub(r"\s+", " ", title).strip()
    prompt = re.sub(r"\s+", " ", prompt).strip()
    layout = choose_layout(title, prompt)
    center, items = build_items(title, prompt)
    return FigureSpec(
        chapter=chapter,
        index=index,
        title=title,
        prompt=prompt,
        label=f"fig:ch{chapter:02d}-{index:02d}",
        layout=layout,
        center=center,
        items=items,
    )


def replace_todo_macros(body: str, chapter: int, figures: list[FigureSpec]) -> str:
    def add(title: str, prompt: str) -> str:
        spec = make_spec(chapter, len([f for f in figures if f.chapter == chapter]) + 1, title, prompt)
        figures.append(spec)
        return render_figure(spec)

    body = re.sub(
        r"\\(?:TodoFigure|todofig)\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: add(m.group(1), m.group(2)),
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\begin\{todobox\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\s*\\end\{todobox\}",
        lambda m: add(m.group(1), m.group(2)),
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\todoprompt\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: add(m.group(1), m.group(2)),
        body,
        flags=re.S,
    )

    def ch3_repl(match: re.Match[str]) -> str:
        return add(match.group(1), match.group(2))

    body = re.sub(
        r"\\begin\{todobox\}\s*(.*?)\s*\\end\{todobox\}\s*\\begin\{promptbox\}\s*(.*?)\s*\\end\{promptbox\}",
        ch3_repl,
        body,
        flags=re.S,
    )

    def ch4_repl(match: re.Match[str]) -> str:
        prompt = re.sub(r"\\textbf\{画像生成用プロンプト\}", "", match.group(2))
        return add(match.group(1), prompt)

    body = re.sub(
        r"\\begin\{todobox\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\s*(.*?)\s*\\end\{todobox\}",
        ch4_repl,
        body,
        flags=re.S,
    )
    return body


def number_tables(body: str, chapter: Chapter) -> str:
    table_index = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal table_index
        table_index += 1
        env = match.group(1)
        caption = f"第{chapter.no:02d}章 {chapter.title} 表{table_index:02d}"
        return (
            rf"\par\smallskip\noindent\refstepcounter{{table}}\label{{tab:ch{chapter.no:02d}-{table_index:02d}}}\textbf{{表 \thetable: {tex_escape(caption)}}}\par\smallskip"
            + "\n"
            + rf"\begin{{{env}}}"
        )

    return re.sub(r"\\begin\{(longtable|tabularx|tabular)\}", repl, body)


def strip_chapter_cover(body: str) -> str:
    body = re.sub(r"\\thispagestyle\{empty\}\s*", "", body)
    body = re.sub(r"\\thispagestyle\{plain\}\s*", "", body)
    body = re.sub(r"\\begin\{center\}.*?\\end\{center\}", "", body, count=1, flags=re.S)
    body = re.sub(r"\\Rule\s*", "", body)
    body = re.sub(r"\\vspace\{[^{}]*\}\s*\\hrule\s*\\vspace\{[^{}]*\}\s*", "", body)
    body = re.sub(r"\\vspace\{[^{}]*\}\s*", "", body, count=2)
    return body.strip()


def strip_titlepage(body: str) -> str:
    match = re.search(r"\\begin\{titlepage\}(.*?)\\end\{titlepage\}", body, flags=re.S)
    if not match:
        return strip_chapter_cover(body)

    titlepage = match.group(1)
    kept_boxes = re.findall(r"\\begin\{pointbox\}\{この資料の(?:主張|読み方)\}.*?\\end\{pointbox\}", titlepage, flags=re.S)
    kept = "\n\n".join(kept_boxes).strip()
    return (kept + "\n\n" + body[match.end() :]).strip()


def demote_sectioning(body: str) -> str:
    body = re.sub(r"\\addcontentsline\{toc\}\{subsection\}", r"\\addcontentsline{toc}{subsubsection}", body)
    body = re.sub(r"\\addcontentsline\{toc\}\{section\}", r"\\addcontentsline{toc}{subsection}", body)
    body = re.sub(r"\\subsubsection(\*?)\{", r"\\paragraph\1{", body)
    body = re.sub(r"\\subsection(\*?)\{", r"\\subsubsection\1{", body)
    body = re.sub(r"\\section(\*?)\{", r"\\subsection\1{", body)
    return body


def normalize_body(chapter: Chapter, figures: list[FigureSpec]) -> str:
    source = chapter.path.read_text(encoding="utf-8")
    begin = source.index(r"\begin{document}") + len(r"\begin{document}")
    end = source.rindex(r"\end{document}")
    body = source[begin:end].strip()
    body = strip_titlepage(body)
    body = re.sub(r"\\tableofcontents\s*(?:\\clearpage|\\newpage)?", "", body)
    body = re.sub(r"^(?:\\clearpage|\\newpage)\s*", "", body)
    body = re.sub(
        r"\\section\{画像\s*TODO\s*一覧\}.*?(?=\\section\{章末確認問題\}|\\section\*\{章末確認問題\}|$)",
        "",
        body,
        flags=re.S,
    )
    body = replace_todo_macros(body, chapter.no, figures)
    body = body.replace(r"\begin{statementbox}{定義}", r"\begin{definitionbox}")
    body = body.replace(r"\end{statementbox}", r"\end{statementbox}")
    body = re.sub(
        r"\\begin\{definitionbox\}(.*?)\\end\{statementbox\}",
        lambda m: r"\begin{definitionbox}" + m.group(1) + r"\end{definitionbox}",
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\MiniBox\{定義\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{definitionbox}" + m.group(1) + r"\end{definitionbox}",
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\begin\{pointbox\}\{定義\}(.*?)\\end\{pointbox\}",
        lambda m: r"\begin{definitionbox}" + m.group(1) + r"\end{definitionbox}",
        body,
        flags=re.S,
    )
    body = number_tables(body, chapter)
    body = demote_sectioning(body)
    return "\n".join(
        [
            rf"\section{{第{chapter.no:02d}章 {chapter.title}}}",
            body,
        ]
    )


def section_filename(index: int, section_source: str) -> str:
    match = re.match(r"\\subsection\*?\{([^{}]+)\}", section_source.strip())
    if not match:
        return f"{index:02d}_chapter_opening.tex"
    title = match.group(1)
    safe = re.sub(r"[\\/:*?\"<>|{}]+", "", title)
    safe = re.sub(r"\s+", "_", safe).strip("_.。・、，,.")
    if not safe:
        safe = "section"
    return f"{index:02d}_{safe[:48]}.tex"


def split_chapter_body(body: str) -> list[str]:
    matches = list(re.finditer(r"(?m)^\\subsection\*?\{", body))
    if not matches:
        return [body]
    parts: list[str] = []
    if matches[0].start() > 0:
        parts.append(body[: matches[0].start()].strip())
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        parts.append(body[match.start() : end].strip())
    return [part for part in parts if part]


def write_split_document(chapters: list[str]) -> None:
    input_lines: list[str] = []
    for chapter, body in zip(CHAPTERS, chapters, strict=True):
        chapter_dir = PARTS_DIR / f"ch{chapter.no:02d}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        for existing in chapter_dir.glob("*.tex"):
            existing.unlink()
        for index, part in enumerate(split_chapter_body(body)):
            filename = section_filename(index, part)
            path = chapter_dir / filename
            path.write_text(part + "\n", encoding="utf-8")
            rel = path.relative_to(OUT_DIR).as_posix()
            if chapter.no != 1:
                input_lines.append(rf"\input{{{rel}}}")
        if chapter.no == 1:
            if CH01_STRUCTURE_CHAPTER.exists():
                rel = CH01_STRUCTURE_CHAPTER.relative_to(OUT_DIR).as_posix()
                input_lines.append(rf"\input{{{rel}}}")
            else:
                input_lines.extend(
                    rf"\input{{{path.relative_to(OUT_DIR).as_posix()}}}"
                    for path in sorted(chapter_dir.glob("*.tex"))
                )

    master = "\n\n".join(
        [
            PREAMBLE,
            *DOCUMENT_OPENING,
            *input_lines,
            r"\end{document}",
            "",
        ]
    )
    MASTER_TEX.write_text(master, encoding="utf-8")


def main() -> None:
    figures: list[FigureSpec] = []
    chapters = [normalize_body(chapter, figures) for chapter in CHAPTERS]
    document = "\n\n".join(
        [
            PREAMBLE,
            *DOCUMENT_OPENING,
            *chapters,
            r"\end{document}",
            "",
        ]
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_TEX.write_text(document, encoding="utf-8")
    write_split_document(chapters)
    write_imagegen_prompts(figures)
    lines = ["chapter\tindex\tlabel\tlayout\timage_path\tprompt_path\ttitle\tcenter\titems"]
    for f in figures:
        lines.append(
            "\t".join(
                [
                    f"{f.chapter:02d}",
                    f"{f.index:02d}",
                    f.label,
                    f.layout,
                    f.image_relpath,
                    f.prompt_relpath,
                    clean_title(f.title),
                    f.center,
                    " / ".join(f.items),
                ]
            )
        )
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_TEX}")
    print(f"wrote {MASTER_TEX}")
    print(f"wrote {PARTS_DIR}")
    print(f"wrote {MANIFEST}")
    print(f"wrote {PROMPT_DIR}")
    print(f"figures: {len(figures)}")


if __name__ == "__main__":
    main()
