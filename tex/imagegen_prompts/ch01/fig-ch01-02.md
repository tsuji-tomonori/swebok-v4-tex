$imagegen

目的:
SWEBOK v4.0a 日本語統合 A4 資料に埋め込む図を、gpt-image-2 の生成AI画像として1枚だけ作成する。
この実行では `fig:ch01-02` だけを個別に生成する。HTML/SVG/Canvas/TikZ/スクリーンショット等の決定的レンダリングで代替しない。

重要:
- built-in `image_gen` を Codex から呼び出して、この1枚を新規生成する。
- 生成後、最新の `$CODEX_HOME/generated_images/...` の PNG をプロジェクト側へコピーする。
- コピー先: `/home/t-tsuji/project/swebok-v4-tex/tex/assets/generated_figures/ch01/fig-ch01-02.png`
- このプロンプト: `/home/t-tsuji/project/swebok-v4-tex/tex/imagegen_prompts/ch01/fig-ch01-02.md`
- 成否を `/home/t-tsuji/project/swebok-v4-tex/tex/swebok_v4_ch01_06_ja_imagegen_manifest.tsv` に TSV で1行追記する。形式は `label<TAB>status<TAB>source<TAB>destination<TAB>prompt`。
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
Title: 要求分類の階層図
Layout: 上から下へ意味が積み重なる階層図。
Central concept: ソフトウェア要求

Visible Japanese labels. Use these labels exactly where possible:
- ソフトウェア要求
- ソフトウェア製品要求
- ソフトウェアプロジェクト要求
- 機能要求
- 非機能要求
- 技術制約
- サービス品質制約

Meaning to convey:
温かいオフホワイト背景、控えめなアクセントカラー、A4本文幅に収まる縦長の階層図を作成する。最上位に「ソフトウェア要求」。第2層に「ソフトウェア製品要求」と「ソフトウェアプロジェクト要求」。製品要求から「機能要求」と「非機能要求」へ分岐。非機能要求から「技術制約」と「サービス品質制約」へ分岐。各箱に短い説明を添える。講義ノート風、細線、印刷で読みやすい図。

完了条件:
- `/home/t-tsuji/project/swebok-v4-tex/tex/assets/generated_figures/ch01/fig-ch01-02.png` が存在する。
- `/home/t-tsuji/project/swebok-v4-tex/tex/swebok_v4_ch01_06_ja_imagegen_manifest.tsv` に `fig:ch01-02` の success または failed 行を追記する。
- 最後に保存できたファイルパスだけを報告する。
