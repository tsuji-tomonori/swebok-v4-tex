# PDF生成のGitHub Actions化

## 受けた指示
- 生成される全体PDFをコミットしない。
- PDFはGitHub Actionsで生成できるようにする。
- 変更をcommit / pushする。

## 要件整理
- GitHubの100MB制限により、生成PDFをコミットに含める運用は避ける。
- TeXソースと生成手順をリポジトリに残し、PDFはCI成果物として取得できる形にする。
- 既存のTeX生成フローは `python3 tex/build_integrated_document.py` と LuaLaTeX のビルドを使う。

## 検討・判断
- ローカルの未pushコミットに含まれていたPDFはステージ対象から外し、PDFは `.gitignore` で無視する。
- Actionsでは統合TeX生成、不足図版生成、LuaLaTeX 2回実行、artifact upload の順に実行する。
- 旧 master PDF は生成物としてリポジトリから外す方針にした。

## 実施作業
- `.github/workflows/build-pdf.yml` を追加し、`swebok_v4_ch01_18_ja_master.pdf` をGitHub Actions artifactとして生成・アップロードするようにした。
- `.gitignore` にTeXの中間生成物とPDF、TeXキャッシュディレクトリを追加した。
- `tex/generate_missing_figure_assets.py` をコミット対象にし、CI上で不足図版PNGを生成できるようにした。
- `work/*.tex` をコミット対象にし、CI上で統合生成スクリプトが章ソースを読めるようにした。
- PDFを含むローカルコミットを巻き戻し、PDFをコミット対象から外した。
- 初回Actions失敗の原因が `work/` 配下の章ソース不足だったため、follow-up commitで生成入力を追加した。

## 成果物
- `.github/workflows/build-pdf.yml`
- `.gitignore`
- `work/*.tex`
- `tex/generate_missing_figure_assets.py`
- `reports/working/20260517-1848-github-actions-pdf-build.md`

## 検証
- `python3 -m py_compile tex/build_integrated_document.py tex/generate_missing_figure_assets.py`
- `python3 tex/generate_missing_figure_assets.py`
- `git diff --cached --check`

## Fit評価
- 指示適合度: 4.8 / 5
- PDF本体をコミットせず、GitHub ActionsでPDFを生成する構成に変更した。
- GitHub Actions自体の実行結果はpush後のGitHub側で確認が必要。

## 未対応・制約・リスク
- Actionsのaptパッケージ解決やTeX Live環境差分による失敗は、GitHub上の初回実行で確認する必要がある。
- 作業前から存在する未ステージの生成物・未追跡ファイルは、本件に必要なもの以外は触っていない。
