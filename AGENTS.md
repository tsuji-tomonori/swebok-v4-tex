# Repository Agent Instructions

このリポジトリで作業する Codex / AI agent は、以下を守る。

## 共通
- 指定 skill が利用可能一覧に出ない場合も、リポジトリローカルの明示ルールとして該当 `SKILL.md` を読む。
- `git diff`、`git status`、変更ファイル一覧、ステージ済み差分、PR 内容、作業レポートから文面を作る場合も該当 skill を適用する。
- `reports/working/*.md`、`reports/bugs/*.md`、同等の作業・障害レポートが関係する場合は本文を確認し、commit message / PR 本文に要点を反映する。
- 実施していないテスト、確認、検証を実施済みとして書かない。
- TeX 文書の生成・確認では、原則 `python3 tex/build_integrated_document.py` と LuaLaTeX による `tex/swebok_v4_ch01_18_ja_master.tex` のビルド可否を確認する。

## Git Commit Message
- 対象: Git commit message、コミットメッセージ、コミットコメント、git comment、`git commit`。ユーザーの「コメント」も Git 文脈では commit message と扱う。
- 必読: `skills/japanese-git-commit-gitmoji/SKILL.md`
- commit 前に `git diff --cached --name-only` でステージ済みファイルを確認する。
- 変更目的が複数に分かれる場合は、1 commit にまとめず目的別分割を検討する。
- 1 行目は原則 `<emoji> <type>(<scope>): <日本語の要約>`。scope 不要または不明なら省略可。
- 既存 commit message がこの形式でなくても、新規 commit ではこのルールを優先する。

## Pull Request Title and Comment
- 対象: Pull Request、PR、PR タイトル、PR 本文、PR コメント、レビューコメント、`gh pr create`。
- 必読: `skills/japanese-pr-title-comment/SKILL.md`
- PR タイトル、PR 本文、PR コメント、レビューコメントは日本語で書く。
- ブランチ名、ファイルパス、コマンド、API 名、型名、関数名、issue 番号は原文維持可。
- PR テンプレートが存在する場合は、その見出しを優先する。

## Post Task Work Report
- 対象: ファイル編集、コマンド実行、調査、検証、ドキュメント作成など、リポジトリへの実作業。ユーザーが「レポート不要」「reports には出さないで」などと明示した場合のみ省略可。
- 必読: `skills/post-task-fit-report/SKILL.md`
- 主作業完了後かつ最終回答前に、タスクごとに作業完了レポートを 1 件残す。
- 保存先は原則 `reports/working/` の Markdown。なければ作成する。
- ファイル名は `YYYYMMDD-HHMM-<task-summary>.md`。summary は ASCII 小文字とハイフンで短く表す。
- レポートには、受けた指示、要件整理、検討・判断の要約、実施作業、成果物、指示への fit 評価、未対応・制約・リスクを簡潔に含める。
- 最終回答では生成したレポートの保存先パスを明示する。

## Skills And AGENTS Update
- 対象: skill の追加・更新・削除、`skills/` 配下の整理、`AGENTS.md` の更新、ユーザーの「skills update」依頼。
- 必読: `skills/skills_agents_updater/SKILL.md`
- skill 更新時は、追加・変更した skill 名、配置先、AGENTS への反映有無、検証結果を作業レポートに記録する。
- 外部リポジトリから skill を取り込む場合は、取り込み元、対象ディレクトリ、除外した内容を明示する。
