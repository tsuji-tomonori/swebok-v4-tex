$imagegen

目的:
SWEBOK v4.0a 日本語統合 A4 資料に埋め込む図を、gpt-image-2 の生成AI画像として1枚だけ作成する。
この実行では `fig:ch06-08` だけを個別に生成する。HTML/SVG/Canvas/TikZ/スクリーンショット等の決定的レンダリングで代替しない。

重要:
- built-in `image_gen` を Codex から呼び出して、この1枚を新規生成する。
- 生成後、最新の `$CODEX_HOME/generated_images/...` の PNG をプロジェクト側へコピーする。
- コピー先: `/home/t-tsuji/project/swebok-v4-tex/tex/assets/generated_figures/ch06/fig-ch06-08.png`
- このプロンプト: `/home/t-tsuji/project/swebok-v4-tex/tex/imagegen_prompts/ch06/fig-ch06-08.md`
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
Title: ロールバックとデータ移行の時系列
Layout: 左から右へ進む工程図または循環を示すフロー図。
Central concept: 旧版稼働

Visible Japanese labels. Use these labels exactly where possible:
- 旧版稼働
- 新版配備
- データ移行
- 監視
- 異常検知
- ロールバック
- データ復元または補正

Meaning to convey:
横軸を時間とし、「旧版稼働」「新版配備」「データ移行」「監視」「異常検知」「ロールバック」「データ復元または補正」を並べる。ソフトウェア状態とデータ状態の二段で示す。

完了条件:
- `/home/t-tsuji/project/swebok-v4-tex/tex/assets/generated_figures/ch06/fig-ch06-08.png` が存在する。
- `/home/t-tsuji/project/swebok-v4-tex/tex/swebok_v4_ch01_06_ja_imagegen_manifest.tsv` に `fig:ch06-08` の success または failed 行を追記する。
- 最後に保存できたファイルパスだけを報告する。
