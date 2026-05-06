$imagegen

目的:
SWEBOK v4.0a 日本語統合 A4 資料に埋め込む図を、gpt-image-2 の生成AI画像として1枚だけ作成する。
この実行では `fig:ch04-07` だけを個別に生成する。HTML/SVG/Canvas/TikZ/スクリーンショット等の決定的レンダリングで代替しない。

重要:
- built-in `image_gen` を Codex から呼び出して、この1枚を新規生成する。
- 生成後、最新の `$CODEX_HOME/generated_images/...` の PNG をプロジェクト側へコピーする。
- コピー先: `/home/t-tsuji/project/swebok-v4-tex/tex/assets/generated_figures/ch04/fig-ch04-07.png`
- このプロンプト: `/home/t-tsuji/project/swebok-v4-tex/tex/imagegen_prompts/ch04/fig-ch04-07.md`
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
Title: 段階的統合と継続的統合の流れ
Layout: 左から右へ進む工程図または循環を示すフロー図。
Central concept: 部品 A

Visible Japanese labels. Use these labels exactly where possible:
- 部品 A
- 部品 B
- 部品 C
- 段階的統合
- 継続的統合パイプライン
- コミット
- 自動ビルド
- 単体テスト
- 統合テスト

Meaning to convey:
温かいオフホワイト背景、控えめなアクセントカラー、A4 本文幅の工程図を作成する。左側に「部品 A」「部品 B」「部品 C」を個別に描き、中央で「段階的統合」によって順に結合される矢印を示す。右側に「継続的統合パイプライン」として「コミット」「自動ビルド」「単体テスト」「統合テスト」「結果通知」を縦または横に並べる。スタブ、ドライバ、モックを足場として小さく表示する。日本語、講義ノート風。

完了条件:
- `/home/t-tsuji/project/swebok-v4-tex/tex/assets/generated_figures/ch04/fig-ch04-07.png` が存在する。
- `/home/t-tsuji/project/swebok-v4-tex/tex/swebok_v4_ch01_06_ja_imagegen_manifest.tsv` に `fig:ch04-07` の success または failed 行を追記する。
- 最後に保存できたファイルパスだけを報告する。
