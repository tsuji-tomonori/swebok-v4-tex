#!/usr/bin/env python3
"""Copy chapter 02 TeX sources into the SWEBOK structure tree.

The structure tree is generated from the SWEBOK table of contents, while the
chapter body is maintained under ``tex/chapters/ch02``.  This script places the
chapter body into the matching CH02 directories as ``source.tex`` files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable

from build_swebok_structure import CHAPTERS, OUT_DIR, ROOT, dir_name


SOURCE_DIR = ROOT / "tex" / "chapters" / "ch02"
TARGET_CHAPTER = 2
SOURCE_FILENAME = "source.tex"


@dataclass(frozen=True)
class Segment:
    level: str
    title: str
    body: str


SECTION_FILES = {
    "2.0": "02_導入：なぜソフトウェアアーキテクチャを独立して学ぶのか.tex",
    "2.1": "03_ソフトウェアアーキテクチャの基礎.tex",
    "2.2": "04_ソフトウェアアーキテクチャ記述.tex",
    "2.3": "05_ソフトウェアアーキテクチャ過程.tex",
    "2.4": "06_ソフトウェアアーキテクチャ評価.tex",
    "2.5": "07_トピックと参考文献の対応.tex",
    "2.6": "08_発展的な読み物.tex",
    "2.7": "09_参考文献.tex",
}

CHAPTER_ROOT_FILES = (
    "00_chapter_opening.tex",
    "01_全体概要：この章で学ぶこと.tex",
)

TITLE_TO_NUMBER = {
    "導入：なぜソフトウェアアーキテクチャを独立して学ぶのか": "2.0",
    "ソフトウェアアーキテクチャの基礎": "2.1",
    "「アーキテクチャ」という語の意味": "2.1.1",
    "利害関係者と関心事": "2.1.2",
    "アーキテクチャの用途": "2.1.3",
    "ソフトウェアアーキテクチャ記述": "2.2",
    "アーキテクチャビューとビューポイント": "2.2.1",
    "アーキテクチャパターン、様式、参照アーキテクチャ": "2.2.2",
    "アーキテクチャ記述言語とアーキテクチャ枠組み": "2.2.3",
    "重要な意思決定としてのアーキテクチャ": "2.2.4",
    "ソフトウェアアーキテクチャ過程": "2.3",
    "文脈の中のアーキテクチャ": "2.3.1",
    "アーキテクチャと設計の関係": "2.3.1.1",
    "アーキテクチャ設計": "2.3.2",
    "アーキテクチャ分析": "2.3.2.1",
    "アーキテクチャ統合": "2.3.2.2",
    "アーキテクチャ評価": "2.3.2.3",
    "アーキテクチャの実践、方法、戦術": "2.3.3",
    "大規模なアーキテクチャ活動": "2.3.4",
    "ソフトウェアアーキテクチャ評価": "2.4",
    "アーキテクチャにおける「よさ」": "2.4.1",
    "アーキテクチャについての推論": "2.4.2",
    "アーキテクチャレビュー": "2.4.3",
    "アーキテクチャ測度": "2.4.4",
    "トピックと参考文献の対応": "2.5",
    "発展的な読み物": "2.6",
    "参考文献": "2.7",
}

HEADING_RE = re.compile(
    r"^\\(?P<level>subsection|subsubsection|paragraph)\*?\{(?P<title>[^{}]+)\}",
    re.MULTILINE,
)


def read_source(name: str) -> str:
    return (SOURCE_DIR / name).read_text(encoding="utf-8").strip() + "\n"


def split_segments(text: str) -> list[Segment]:
    matches = list(HEADING_RE.finditer(text))
    segments: list[Segment] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        segments.append(
            Segment(
                level=match.group("level"),
                title=match.group("title"),
                body=text[match.start() : end].strip() + "\n",
            )
        )
    return segments


def iter_entries(entries) -> Iterable:
    for entry in entries:
        yield entry
        yield from iter_entries(entry.children)


def build_path_map() -> dict[str, Path]:
    chapter = next(chapter for chapter in CHAPTERS if chapter.num == TARGET_CHAPTER)
    chapter_path = OUT_DIR / dir_name(f"CH{chapter.num:02d}", chapter.ja, chapter.en)
    paths = {f"CH{chapter.num:02d}": chapter_path}

    def visit(parent: Path, entries) -> None:
        for entry in entries:
            path = parent / dir_name(entry.num, entry.ja, entry.en)
            paths[entry.num] = path
            visit(path, entry.children)

    visit(chapter_path, chapter.entries)
    return paths


def write_source(path: Path, content: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    path.joinpath(SOURCE_FILENAME).write_text(content, encoding="utf-8")


def main() -> None:
    paths = build_path_map()

    root_body = "\n\n".join(read_source(name).strip() for name in CHAPTER_ROOT_FILES) + "\n"
    stale_root_source = paths["CH02"] / SOURCE_FILENAME
    if stale_root_source.exists():
        stale_root_source.unlink()

    written: set[str] = set()
    for section_num, filename in SECTION_FILES.items():
        text = read_source(filename)
        segments = split_segments(text)
        parent_parts: list[str] = []
        if section_num == "2.0":
            parent_parts.append(root_body.strip())

        for segment in segments:
            target_num = TITLE_TO_NUMBER.get(segment.title)
            if target_num is None:
                parent_parts.append(segment.body.strip())
                continue
            if target_num == section_num:
                parent_parts.append(segment.body.strip())
                continue
            write_source(paths[target_num], segment.body)
            written.add(target_num)

        write_source(paths[section_num], "\n\n".join(parent_parts).strip() + "\n")
        written.add(section_num)

    missing = sorted(set(paths) - written - {"CH02"})
    if missing:
        raise SystemExit(f"missing source for: {', '.join(missing)}")

    print(f"copied CH02 TeX sources into {paths['CH02'].relative_to(ROOT)}")


if __name__ == "__main__":
    main()
