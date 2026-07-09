# 作業完了レポート

保存先: `reports/working/20260506-1307-localize-ch05-assets.md`

## 1. 受けた指示

- 主な依頼: asset も各ディレクトリで管理するようにする。
- 成果物: CH05 構造配下の各 `content.tex` と同じディレクトリ配下で管理される画像 asset。

## 2. 要件整理

| 要件ID | 指示・要件 | 重要度 | 対応状況 |
|---|---|---:|---|
| R1 | CH05 構造側の asset を各ディレクトリに配置する | 高 | 対応 |
| R2 | `content.tex` の画像参照をローカル asset 参照にする | 高 | 対応 |
| R3 | 参照先ファイルが存在することを確認する | 中 | 対応 |

## 3. 検討・判断したこと

- 既存の `tex/assets/generated_figures/ch05` は統合文書ビルド用に維持した。
- `tex/swebok_structure` 側では、各 `content.tex` のあるディレクトリに `assets/` を作り、利用している画像だけをコピーした。
- TeX 参照は `assets/generated_figures/ch05/fig-ch05-xx.png` から `assets/fig-ch05-xx.png` へ変更し、構造単位で本文と asset を一緒に確認できるようにした。

## 4. 実施した作業

- CH05 構造配下の `content.tex` から画像参照を抽出した。
- 参照されている `fig-ch05-01.png` から `fig-ch05-15.png` を、該当する `content.tex` と同じディレクトリ配下の `assets/` にコピーした。
- 各 `content.tex` の `\IfFileExists` と `\includegraphics` のパスをローカル `assets/` 参照へ更新した。

## 5. 成果物

| 成果物 | 形式 | 内容 | 指示との対応 |
|---|---|---|---|
| `tex/swebok_structure/CH05.ソフトウェアテスト(Software_Testing)/**/assets/*.png` | PNG | 各構造ディレクトリで管理する CH05 図版 | asset 管理に対応 |
| `tex/swebok_structure/CH05.ソフトウェアテスト(Software_Testing)/**/content.tex` | TeX | ローカル `assets/` 参照へ変更 | 参照整合に対応 |

## 6. 指示へのfit評価

| 評価軸 | 評価 | 理由 |
|---|---:|---|
| 指示網羅性 | 5 | CH05 構造内の全画像参照を各ディレクトリ配下 asset に移した。 |
| 制約遵守 | 5 | 既存ビルド用 asset は壊さず、構造側へコピーした。 |
| 成果物品質 | 5 | 参照先存在確認を行い、古い共有 asset パスが残っていないことも確認した。 |
| 検収容易性 | 5 | `content.tex` と対応画像が同一構造ディレクトリ内で確認できる。 |

総合fit: 5.0 / 5.0（約100%）

理由: 指示された asset のディレクトリ単位管理に対応し、参照先の存在も確認した。

## 7. 検証

- `rg -n 'assets/generated_figures/ch05' 'tex/swebok_structure/CH05.ソフトウェアテスト(Software_Testing)'`: 旧パスなし。
- `find 'tex/swebok_structure/CH05.ソフトウェアテスト(Software_Testing)' -path '*/assets/*' -type f`: 構造配下に 15 件の CH05 画像を確認。
- `content.tex` の `assets/fig-ch05-xx.png` 参照先がすべて存在することを確認。
- `rg -n ' +$' 'tex/swebok_structure/CH05.ソフトウェアテスト(Software_Testing)'`: 末尾空白なし。
