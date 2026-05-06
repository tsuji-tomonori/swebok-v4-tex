# SWEBOK v4 Japanese TeX Materials

This repository was reconstructed from `swebok-v4-tex-transfer.zip`.

## Contents

- `software_*_chapter*.tex`: chapter source files for chapters 01-06.
- `tex/build_integrated_document.py`: generator for the integrated TeX document.
- `tex/swebok_v4_ch01_06_ja_integrated.tex`: integrated one-file TeX output.
- `tex/swebok_v4_ch01_06_ja_master.tex`: split-chapter master TeX output.
- `tex/chapters/`: generated split chapter sections.
- `tex/assets/generated_figures/`: generated PNG figures used by the TeX documents.
- `tex/imagegen_prompts/`: prompts used to generate figure assets.
- `skills/`: local Codex skills used by the project workflow.

## Build

Regenerate the integrated and split TeX sources:

```bash
python3 tex/build_integrated_document.py
```

Build the master PDF with LuaLaTeX:

```bash
cd tex
lualatex swebok_v4_ch01_06_ja_master.tex
lualatex swebok_v4_ch01_06_ja_master.tex
```

The TeX build expects LuaLaTeX and Japanese TeX packages such as `luatexja`.
If LuaLaTeX cannot write its font cache, set writable cache paths:

```bash
mkdir -p /tmp/texmf-var /tmp/texmf-cache
TEXMFVAR=/tmp/texmf-var TEXMFCACHE=/tmp/texmf-cache lualatex swebok_v4_ch01_06_ja_master.tex
```
