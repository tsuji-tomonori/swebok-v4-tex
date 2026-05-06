#!/usr/bin/env python3
"""Generate a SWEBOK-PDF-aligned bilingual directory structure.

The source TeX files are organized for the generated Japanese document.  This
script creates a separate navigation tree that follows the SWEBOK Guide v4.0a
PDF table of contents for chapters 01-06, using Japanese and English labels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "tex" / "swebok_structure"
MANIFEST = ROOT / "tex" / "swebok_structure_manifest.tsv"
CHAPTERS_DIR = ROOT / "tex" / "chapters"


@dataclass(frozen=True)
class Entry:
    num: str
    ja: str
    en: str
    children: tuple["Entry", ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Chapter:
    num: int
    ja: str
    en: str
    entries: tuple[Entry, ...]


def e(num: str, ja: str, en: str, children: tuple[Entry, ...] = ()) -> Entry:
    return Entry(num, ja, en, children)


CHAPTERS = (
    Chapter(
        1,
        "ソフトウェア要求",
        "Software Requirements",
        (
            e("1.0", "導入", "Introduction"),
            e(
                "1.1",
                "ソフトウェア要求の基礎",
                "Software Requirements Fundamentals",
                (
                    e("1.1.1", "ソフトウェア要求の定義", "Definition of a Software Requirement"),
                    e("1.1.2", "ソフトウェア要求の分類", "Categories of Software Requirements"),
                    e("1.1.3", "ソフトウェア製品要求とソフトウェアプロジェクト要求", "Software Product Requirements and Software Project Requirements"),
                    e("1.1.4", "機能要求", "Functional Requirements"),
                    e("1.1.5", "非機能要求", "Nonfunctional Requirements"),
                    e("1.1.6", "技術制約", "Technology Constraints"),
                    e("1.1.7", "サービス品質制約", "Quality of Service Constraints"),
                    e("1.1.8", "なぜこのように要求を分類するのか", "Why Categorize Requirements This Way"),
                    e("1.1.9", "システム要求とソフトウェア要求", "System Requirements and Software Requirements"),
                    e("1.1.10", "派生要求", "Derived Requirements"),
                    e("1.1.11", "ソフトウェア要求活動", "Software Requirements Activities"),
                ),
            ),
            e("1.2", "要求獲得", "Requirements Elicitation", (e("1.2.1", "要求の源泉", "Requirements Sources"), e("1.2.2", "一般的な要求獲得技法", "Common Requirements Elicitation Techniques"))),
            e("1.3", "要求分析", "Requirements Analysis", (e("1.3.1", "基本的な要求分析", "Basic Requirements Analysis"), e("1.3.2", "サービス品質制約の経済性", "Economics of Quality of Service Constraints"), e("1.3.3", "形式的分析", "Formal Analysis"), e("1.3.4", "要求における衝突への対応", "Addressing Conflict in Requirements"))),
            e("1.4", "要求仕様化", "Requirements Specification", (e("1.4.1", "非構造化自然言語による要求仕様化", "Unstructured Natural Language Requirements Specification"), e("1.4.2", "構造化自然言語による要求仕様化", "Structured Natural Language Requirements Specification"), e("1.4.3", "受け入れ基準に基づく要求仕様化", "Acceptance Criteria-Based Requirements Specification"), e("1.4.4", "モデルに基づく要求仕様化", "Model-Based Requirements Specification"), e("1.4.5", "要求の追加属性", "Additional Attributes of Requirement"), e("1.4.6", "増分的要求仕様化と包括的要求仕様化", "Incremental and Comprehensive Requirements Specification"))),
            e("1.5", "要求妥当性確認", "Requirements Validation", (e("1.5.1", "要求レビュー", "Requirements Reviews"), e("1.5.2", "シミュレーションと実行", "Simulation and Execution"), e("1.5.3", "プロトタイピング", "Prototyping"))),
            e("1.6", "要求管理活動", "Requirements Management Activities", (e("1.6.1", "要求整理・削減", "Requirements Scrubbing"), e("1.6.2", "要求変更管理", "Requirements Change Control"), e("1.6.3", "範囲調整", "Scope Matching"))),
            e("1.7", "実務上の考慮", "Practical Considerations", (e("1.7.1", "要求プロセスの反復性", "Iterative Nature of the Requirements Process"), e("1.7.2", "要求の優先順位付け", "Requirements Prioritization"), e("1.7.3", "要求の追跡可能性", "Requirements Tracing"), e("1.7.4", "要求の安定性と変動性", "Requirements Stability and Volatility"), e("1.7.5", "要求の測定", "Measuring Requirements"), e("1.7.6", "要求プロセスの品質と改善", "Requirements Process Quality and Improvement"))),
            e("1.8", "ソフトウェア要求ツール", "Software Requirements Tools", (e("1.8.1", "要求管理ツール", "Requirements Management Tools"), e("1.8.2", "要求モデリングツール", "Requirements Modeling Tools"), e("1.8.3", "機能テストケース生成ツール", "Functional Test Case Generation Tools"))),
            e("1.9", "トピックと参考文献の対応", "Matrix of Topics vs Reference Material"),
            e("1.10", "発展的な読み物", "Further Readings"),
            e("1.11", "参考文献", "References"),
        ),
    ),
    Chapter(
        2,
        "ソフトウェアアーキテクチャ",
        "Software Architecture",
        (
            e("2.0", "導入", "Introduction"),
            e("2.1", "ソフトウェアアーキテクチャの基礎", "Software Architecture Fundamentals", (e("2.1.1", "「アーキテクチャ」という語の意味", "The Senses of Architecture"), e("2.1.2", "利害関係者と関心事", "Stakeholders and Concerns"), e("2.1.3", "アーキテクチャの用途", "Uses of Architecture"))),
            e("2.2", "ソフトウェアアーキテクチャ記述", "Software Architecture Description", (e("2.2.1", "アーキテクチャビューとビューポイント", "Architecture Views and Viewpoints"), e("2.2.2", "アーキテクチャパターン・様式・参照アーキテクチャ", "Architecture Patterns Styles and Reference Architectures"), e("2.2.3", "アーキテクチャ記述言語とアーキテクチャ枠組み", "Architecture Description Languages and Architecture Frameworks"), e("2.2.4", "重要な意思決定としてのアーキテクチャ", "Architecture as Significant Decisions"))),
            e("2.3", "ソフトウェアアーキテクチャ過程", "Software Architecture Process", (e("2.3.1", "文脈の中のアーキテクチャ", "Architecture in Context", (e("2.3.1.1", "アーキテクチャと設計の関係", "Relation of Architecture to Design"),)), e("2.3.2", "アーキテクチャ設計", "Architectural Design", (e("2.3.2.1", "アーキテクチャ分析", "Architecture Analysis"), e("2.3.2.2", "アーキテクチャ統合", "Architecture Synthesis"), e("2.3.2.3", "アーキテクチャ評価", "Architecture Evaluation"))), e("2.3.3", "アーキテクチャの実践・方法・戦術", "Architecture Practices Methods and Tactics"), e("2.3.4", "大規模なアーキテクチャ活動", "Architecting in the Large"))),
            e("2.4", "ソフトウェアアーキテクチャ評価", "Software Architecture Evaluation", (e("2.4.1", "アーキテクチャにおける「よさ」", "Goodness in Architecture"), e("2.4.2", "アーキテクチャについての推論", "Reasoning about Architectures"), e("2.4.3", "アーキテクチャレビュー", "Architecture Reviews"), e("2.4.4", "アーキテクチャ測度", "Architecture Metrics"))),
            e("2.5", "トピックと参考文献の対応", "Matrix of Topics vs Reference Material"),
            e("2.6", "発展的な読み物", "Further Readings"),
            e("2.7", "参考文献", "References"),
        ),
    ),
    Chapter(
        3,
        "ソフトウェア設計",
        "Software Design",
        (
            e("3.0", "導入", "Introduction"),
            e("3.1", "ソフトウェア設計の基礎", "Software Design Fundamentals", (e("3.1.1", "設計思考", "Design Thinking"), e("3.1.2", "ソフトウェア設計の文脈", "Context of Software Design"), e("3.1.3", "ソフトウェア設計の主要論点", "Key Issues in Software Design"), e("3.1.4", "ソフトウェア設計原則", "Software Design Principles"))),
            e("3.2", "ソフトウェア設計プロセス", "Software Design Processes", (e("3.2.1", "高水準設計", "High-Level Design"), e("3.2.2", "詳細設計", "Detailed Design"))),
            e("3.3", "ソフトウェア設計品質", "Software Design Qualities", (e("3.3.1", "並行性", "Concurrency"), e("3.3.2", "制御とイベント処理", "Control and Event Handling"), e("3.3.3", "データ永続化", "Data Persistence"), e("3.3.4", "構成要素の分散", "Distribution of Components"), e("3.3.5", "誤り・例外処理と耐故障性", "Errors and Exception Handling Fault Tolerance"), e("3.3.6", "統合と相互運用性", "Integration and Interoperability"), e("3.3.7", "保証・セキュリティ・安全性", "Assurance Security and Safety"), e("3.3.8", "変動性", "Variability"))),
            e("3.4", "ソフトウェア設計の記録", "Recording Software Designs", (e("3.4.1", "モデルに基づく設計", "Model-Based Design"), e("3.4.2", "構造設計記述", "Structural Design Descriptions"), e("3.4.3", "振る舞い設計記述", "Behavioral Design Descriptions"), e("3.4.4", "設計パターンとスタイル", "Design Patterns and Styles"), e("3.4.5", "専用言語と領域固有言語", "Specialized and Domain-Specific Languages"), e("3.4.6", "設計根拠", "Design Rationale"))),
            e("3.5", "ソフトウェア設計戦略と方法", "Software Design Strategies and Methods", (e("3.5.1", "一般戦略", "General Strategies"), e("3.5.2", "機能指向・構造化設計", "Function-Oriented or Structured Design"), e("3.5.3", "データ中心設計", "Data-Centered Design"), e("3.5.4", "オブジェクト指向設計", "Object-Oriented Design"), e("3.5.5", "利用者中心設計", "User-Centered Design"), e("3.5.6", "構成要素ベース設計", "Component-Based Design CBD"), e("3.5.7", "イベント駆動設計", "Event-Driven Design"), e("3.5.8", "アスペクト指向設計", "Aspect-Oriented Design AOD"), e("3.5.9", "制約に基づく設計", "Constraint-Based Design"), e("3.5.10", "ドメイン駆動設計", "Domain-Driven Design"), e("3.5.11", "その他の方法", "Other Methods"))),
            e("3.6", "ソフトウェア設計品質分析と評価", "Software Design Quality Analysis and Evaluation", (e("3.6.1", "設計レビューと監査", "Design Reviews and Audits"), e("3.6.2", "品質属性", "Quality Attributes"), e("3.6.3", "品質分析・評価技法", "Quality Analysis and Evaluation Techniques"), e("3.6.4", "測度とメトリクス", "Measures and Metrics"), e("3.6.5", "検証・妥当性確認・認証", "Verification Validation and Certification"))),
            e("3.7", "トピックと参考文献の対応", "Matrix of Topics vs Reference Material"),
            e("3.8", "発展的な読み物", "Further Readings"),
            e("3.9", "参考文献", "References"),
        ),
    ),
    Chapter(
        4,
        "ソフトウェア構築",
        "Software Construction",
        (
            e("4.0", "導入", "Introduction"),
            e("4.1", "ソフトウェア構築の基礎", "Software Construction Fundamentals", (e("4.1.1", "複雑さの最小化", "Minimizing Complexity"), e("4.1.2", "変化を予期し受け入れる", "Anticipating and Embracing Change"), e("4.1.3", "検証しやすく構築する", "Constructing for Verification"), e("4.1.4", "資産の再利用", "Reusing Assets"), e("4.1.5", "構築における標準の適用", "Applying Standards in Construction"))),
            e("4.2", "構築の管理", "Managing Construction", (e("4.2.1", "ライフサイクルモデルにおける構築", "Construction in Life Cycle Models"), e("4.2.2", "構築計画", "Construction Planning"), e("4.2.3", "構築測定", "Construction Measurement"), e("4.2.4", "依存関係の管理", "Managing Dependencies"))),
            e("4.3", "実務上の考慮", "Practical Considerations", (e("4.3.1", "構築設計", "Construction Design"), e("4.3.2", "構築言語", "Construction Languages"), e("4.3.3", "コーディング", "Coding"), e("4.3.4", "構築テスト", "Construction Testing"), e("4.3.5", "構築における再利用", "Reuse in Construction"), e("4.3.6", "構築品質", "Construction Quality"), e("4.3.7", "統合", "Integration"), e("4.3.8", "クロスプラットフォーム開発と移行", "Cross-Platform Development and Migration"))),
            e("4.4", "構築技術", "Construction Technologies", (e("4.4.1", "API の設計と利用", "API Design and Use"), e("4.4.2", "オブジェクト指向の実行時問題", "Object-Oriented Runtime Issues"), e("4.4.3", "パラメータ化・テンプレート・総称", "Parameterization Templates and Generics"), e("4.4.4", "表明・契約による設計・防御的プログラミング", "Assertions Design by Contract and Defensive Programming"), e("4.4.5", "エラー処理・例外処理・フォールトトレランス", "Error Handling Exception Handling and Fault Tolerance"), e("4.4.6", "実行可能モデル", "Executable Models"), e("4.4.7", "状態に基づく構築技法と表駆動構築技法", "State-Based and Table-Driven Construction Techniques"), e("4.4.8", "実行時設定と国際化", "Runtime Configuration and Internationalization"), e("4.4.9", "文法に基づく入力処理", "Grammar-Based Input Processing"), e("4.4.10", "並行処理の基本部品", "Concurrency Primitives"), e("4.4.11", "ミドルウェア", "Middleware"), e("4.4.12", "分散およびクラウド基盤ソフトウェアの構築方法", "Construction Methods for Distributed and Cloud-Based Software"), e("4.4.13", "異種システムの構築", "Constructing Heterogeneous Systems"), e("4.4.14", "性能分析とチューニング", "Performance Analysis and Tuning"), e("4.4.15", "プラットフォーム標準", "Platform Standards"), e("4.4.16", "テストファーストプログラミング", "Test-First Programming"), e("4.4.17", "構築のためのフィードバックループ", "Feedback Loop for Construction"))),
            e("4.5", "ソフトウェア構築ツール", "Software Construction Tools", (e("4.5.1", "開発環境", "Development Environments"), e("4.5.2", "視覚的プログラミングとローコード・ゼロコードプラットフォーム", "Visual Programming and Low-Code Zero-Code Platforms"), e("4.5.3", "単体テストツール", "Unit Testing Tools"), e("4.5.4", "プロファイリング・性能分析・スライシングツール", "Profiling Performance Analysis and Slicing Tools"))),
            e("4.6", "トピックと参考文献の対応", "Matrix of Topics vs Reference Material"),
            e("4.7", "発展的な読み物", "Further Readings"),
            e("4.8", "参考文献", "References"),
        ),
    ),
    Chapter(
        5,
        "ソフトウェアテスト",
        "Software Testing",
        (
            e("5.0", "導入", "Introduction"),
            e("5.1", "ソフトウェアテストの基礎", "Software Testing Fundamentals", (e("5.1.1", "欠陥と障害", "Faults vs Failures"), e("5.1.2", "主要論点", "Key Issues"), e("5.1.3", "テストと他の活動との関係", "Relationship of Testing to Other Activities"))),
            e("5.2", "テストレベル", "Test Levels", (e("5.2.1", "テスト対象", "The Target of the Test"), e("5.2.2", "テスト目的", "Objectives of Testing"))),
            e("5.3", "テスト技法", "Test Techniques", (e("5.3.1", "仕様ベース技法", "Specification-Based Techniques"), e("5.3.2", "構造ベーステスト技法", "Structure-Based Test Techniques"), e("5.3.3", "経験ベース技法", "Experience-Based Techniques"), e("5.3.4", "欠陥ベース技法とミューテーション技法", "Fault-Based and Mutation Techniques"), e("5.3.5", "利用ベース技法", "Usage-Based Techniques"), e("5.3.6", "アプリケーションの性質に基づく技法", "Techniques Based on the Nature of the Application"), e("5.3.7", "技法の選択と組合せ", "Selecting and Combining Techniques"), e("5.3.8", "派生知識に基づく技法", "Techniques Based on Derived Knowledge"))),
            e("5.4", "テスト関連測度", "Test-Related Measures", (e("5.4.1", "SUT の評価", "Evaluation of the SUT"), e("5.4.2", "実施したテストの評価", "Evaluation of the Tests Performed"))),
            e("5.5", "テストプロセス", "Test Process", (e("5.5.1", "実務上の考慮", "Practical Considerations"), e("5.5.2", "テストサブプロセスと活動", "Test Sub-Processes and Activities"), e("5.5.3", "人員配置", "Staffing"))),
            e("5.6", "開発プロセスと適用領域におけるソフトウェアテスト", "Software Testing in the Development Processes and the Application Domains", (e("5.6.1", "ソフトウェア開発プロセス内のテスト", "Testing Inside Software Development Processes"), e("5.6.2", "適用領域におけるテスト", "Testing in the Application Domains"))),
            e("5.7", "新興技術のテストと新興技術によるテスト", "Testing of and Testing Through Emerging Technologies", (e("5.7.1", "新興技術をテストする", "Testing of Emerging Technologies"), e("5.7.2", "新興技術を使ってテストする", "Testing Through Emerging Technologies"))),
            e("5.8", "ソフトウェアテストツール", "Software Testing Tools", (e("5.8.1", "テストツール支援と選択", "Testing Tool Support and Selection"), e("5.8.2", "ツールの分類", "Categories of Tools"))),
            e("5.9", "トピックと参考文献の対応", "Matrix of Topics vs Reference Material"),
            e("5.10", "参考文献", "References"),
        ),
    ),
    Chapter(
        6,
        "ソフトウェアエンジニアリング運用",
        "Software Engineering Operations",
        (
            e("6.0", "導入", "Introduction"),
            e("6.1", "ソフトウェアエンジニアリング運用の基礎", "Software Engineering Operations Fundamentals", (e("6.1.1", "ソフトウェアエンジニアリング運用の定義", "Definition of Software Engineering Operations"), e("6.1.2", "ソフトウェアエンジニアリング運用プロセス", "Software Engineering Operations Processes"), e("6.1.3", "ソフトウェア導入", "Software Installation"), e("6.1.4", "スクリプト化と自動化", "Scripting and Automating"), e("6.1.5", "効果的なテストとトラブルシューティング", "Effective Testing and Troubleshooting"), e("6.1.6", "性能・信頼性・負荷分散", "Performance Reliability and Load Balancing"))),
            e("6.2", "ソフトウェアエンジニアリング運用計画", "Software Engineering Operations Planning", (e("6.2.1", "運用計画と供給者管理", "Operations Plan and Supplier Management", (e("6.2.1.1", "運用計画", "Operations Plan"), e("6.2.1.2", "供給者管理", "Supplier Management"))), e("6.2.2", "開発環境と運用環境", "Development and Operational Environments"), e("6.2.3", "ソフトウェア可用性・継続性・サービス水準", "Software Availability Continuity and Service Levels"), e("6.2.4", "ソフトウェア容量管理", "Software Capacity Management"), e("6.2.5", "バックアップ・災害復旧・フェイルオーバー", "Software Backup Disaster Recovery and Failover"), e("6.2.6", "ソフトウェアとデータの安全性・セキュリティ・完全性・保護・統制", "Software and Data Safety Security Integrity Protection and Controls"))),
            e("6.3", "ソフトウェアエンジニアリング運用提供", "Software Engineering Operations Delivery", (e("6.3.1", "運用テスト・検証・受け入れ", "Operational Testing Verification and Acceptance"), e("6.3.2", "配備・リリース工学", "Deployment Release Engineering"), e("6.3.3", "ロールバックとデータ移行", "Rollback and Data Migration"), e("6.3.4", "問題解決", "Problem Resolution"))),
            e("6.4", "ソフトウェアエンジニアリング運用制御", "Software Engineering Operations Control", (e("6.4.1", "インシデント管理", "Incident Management"), e("6.4.2", "変更管理", "Change Management"), e("6.4.3", "監視・測定・追跡・レビュー", "Monitor Measure Track and Review"), e("6.4.4", "運用支援", "Operations Support"), e("6.4.5", "サービス報告", "Service Reporting"))),
            e("6.5", "実務上の考慮", "Practical Considerations", (e("6.5.1", "インシデントと問題の予防", "Incident and Problem Prevention"), e("6.5.2", "運用リスク管理", "Operational Risk Management"), e("6.5.3", "ソフトウェアエンジニアリング運用の自動化", "Automating Software Engineering Operations"), e("6.5.4", "小規模組織におけるソフトウェアエンジニアリング運用", "Software Engineering Operations for Small Organizations"))),
            e("6.6", "ソフトウェアエンジニアリング運用ツール", "Software Engineering Operations Tools", (e("6.6.1", "コンテナと仮想化", "Containers and Virtualization"), e("6.6.2", "配備", "Deployment"), e("6.6.3", "自動テスト", "Automated Test"), e("6.6.4", "監視とテレメトリ", "Monitoring and Telemetry"))),
            e("6.7", "トピックと参考文献の対応", "Matrix of Topics vs Reference Material"),
            e("6.8", "参考文献", "References"),
        ),
    ),
)


def slug_en(value: str) -> str:
    value = value.replace("&", "and")
    value = re.sub(r"[“”\"']", "", value)
    value = value.replace("/", "_")
    value = re.sub(r"[^A-Za-z0-9()._-]+", "_", value.strip())
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def safe_ja(value: str) -> str:
    value = value.replace("/", "・").replace(":", "：").replace("\\", "・")
    return re.sub(r"\s+", "", value)


def dir_name(prefix: str, ja: str, en: str) -> str:
    return f"{prefix}.{safe_ja(ja)}({slug_en(en)})"


def write_readme(path: Path, title: str, ja: str, en: str, children: tuple[Entry, ...]) -> None:
    lines = [
        f"# {title}",
        "",
        f"- 日本語: {ja}",
        f"- English: {en}",
        "",
    ]
    if children:
        lines.append("## 下位構成")
        lines.append("")
        for child in children:
            child_dir = dir_name(child.num, child.ja, child.en)
            lines.append(f"- [{child.num} {child.ja} ({child.en})](./{child_dir}/)")
        lines.append("")
    path.joinpath("README.md").write_text("\n".join(lines), encoding="utf-8")


def write_entry(parent: Path, entry: Entry, chapter: Chapter, rows: list[str]) -> None:
    path = parent / dir_name(entry.num, entry.ja, entry.en)
    path.mkdir(parents=True, exist_ok=True)
    write_readme(path, f"{entry.num}. {entry.ja} ({entry.en})", entry.ja, entry.en, entry.children)
    rows.append(
        "\t".join(
            [
                f"CH{chapter.num:02d}",
                entry.num,
                entry.ja,
                entry.en,
                path.relative_to(ROOT).as_posix(),
            ]
        )
    )
    for child in entry.children:
        write_entry(path, child, chapter, rows)


def chapter_path(chapter: Chapter) -> Path:
    return OUT_DIR / dir_name(f"CH{chapter.num:02d}", chapter.ja, chapter.en)


def entry_path(chapter: Chapter, entry_num: str) -> Path:
    def search(parent: Path, entries: tuple[Entry, ...]) -> Path | None:
        for entry in entries:
            path = parent / dir_name(entry.num, entry.ja, entry.en)
            if entry.num == entry_num:
                return path
            found = search(path, entry.children)
            if found:
                return found
        return None

    found = search(chapter_path(chapter), chapter.entries)
    if not found:
        raise KeyError(f"entry not found: CH{chapter.num:02d} {entry_num}")
    return found


def strip_first_heading(text: str) -> str:
    text = re.sub(r"\A\\(?:subsection|subsubsection)\*?\{[^{}]+\}\n", "", text)
    text = re.sub(r"\A\\addcontentsline\{toc\}\{[^{}]+\}\{[^{}]+\}\n", "", text)
    return text.strip()


def split_subsubsections(text: str) -> tuple[str, list[tuple[str, str]]]:
    text = strip_first_heading(text)
    matches = list(re.finditer(r"(?m)^\\subsubsection\{([^{}]+)\}\n", text))
    if not matches:
        return text.strip(), []
    lead = text[: matches[0].start()].strip()
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1), text[match.end() : end].strip()))
    return lead, sections


def generated_tex(source: Path, body: str) -> str:
    rel = source.relative_to(ROOT).as_posix()
    return "\n".join([f"% Generated by tex/build_swebok_structure.py from {rel}", body.strip(), ""])


def write_content(path: Path, source: Path, body: str) -> None:
    path.joinpath("content.tex").write_text(generated_tex(source, body), encoding="utf-8")


def mirror_chapter01_content() -> None:
    chapter = CHAPTERS[0]
    root = chapter_path(chapter)
    source_dir = CHAPTERS_DIR / "ch01"

    opening = source_dir / "00_chapter_opening.tex"
    overview = strip_first_heading((source_dir / "01_全体概要：この章で学ぶこと.tex").read_text(encoding="utf-8"))
    introduction = strip_first_heading((source_dir / "02_導入：要求が重要な理由.tex").read_text(encoding="utf-8"))
    introduction_path = entry_path(chapter, "1.0")
    write_content(
        introduction_path,
        source_dir / "02_導入：要求が重要な理由.tex",
        "\n\n".join(
            [
                opening.read_text(encoding="utf-8").strip(),
                r"\subsection{導入}",
                r"\paragraph{全体概要：この章で学ぶこと}",
                overview,
                r"\paragraph{要求が重要な理由}",
                introduction,
            ]
        ),
    )

    structured_sources = [
        (
            "1.1",
            source_dir / "03_ソフトウェア要求の基礎.tex",
            {
                "なぜこのように分類するのか": ("1.1.8", "なぜこのように要求を分類するのか"),
            },
        ),
        (
            "1.2",
            source_dir / "04_要求獲得.tex",
            {
                "要求獲得技法": ("1.2.2", "一般的な要求獲得技法"),
            },
        ),
        (
            "1.3",
            source_dir / "05_要求分析.tex",
            {
                "要求の性質": ("1.3.1", "基本的な要求分析"),
                "サービス品質要求の経済性": ("1.3.2", "サービス品質制約の経済性"),
                "要求の衝突への対応": ("1.3.4", "要求における衝突への対応"),
            },
        ),
        (
            "1.4",
            source_dir / "06_要求仕様化.tex",
            {
                "増分的仕様化と包括的仕様化": ("1.4.6", "増分的要求仕様化と包括的要求仕様化"),
            },
        ),
        ("1.5", source_dir / "07_要求妥当性確認.tex", {}),
        ("1.6", source_dir / "08_要求管理活動.tex", {}),
        ("1.7", source_dir / "09_実務上の考慮.tex", {}),
        ("1.8", source_dir / "10_ソフトウェア要求ツール.tex", {}),
    ]

    chapter_entries = {entry.num: entry for entry in chapter.entries}
    for parent_num, source, title_overrides in structured_sources:
        parent = chapter_entries[parent_num]
        lead, sections = split_subsubsections(source.read_text(encoding="utf-8"))
        write_content(entry_path(chapter, parent_num), source, "\n\n".join([rf"\subsection{{{parent.ja}}}", lead]).strip())

        child_by_ja = {child.ja: child for child in parent.children}
        for original_title, body in sections:
            override = title_overrides.get(original_title)
            if override:
                child_num, child_title = override
            else:
                child = child_by_ja[original_title]
                child_num, child_title = child.num, child.ja
            write_content(entry_path(chapter, child_num), source, "\n\n".join([rf"\subsubsection{{{child_title}}}", body]))

    whole_file_targets = [
        ("1.9", source_dir / "11_トピックと参考文献の対応.tex"),
        ("1.10", source_dir / "12_発展的な読み物.tex"),
        ("1.11", source_dir / "13_参考文献.tex"),
    ]
    for entry_num, source in whole_file_targets:
        entry = chapter_entries[entry_num]
        body = "\n\n".join([rf"\subsection{{{entry.ja}}}", strip_first_heading(source.read_text(encoding="utf-8"))])
        write_content(entry_path(chapter, entry_num), source, body)

    inputs = [introduction_path / "content.tex"]
    for entry in chapter.entries:
        if entry.num == "1.0":
            continue
        inputs.append(entry_path(chapter, entry.num) / "content.tex")
        for child in entry.children:
            child_path = entry_path(chapter, child.num)
            content = child_path / "content.tex"
            if content.exists():
                inputs.append(content)

    introduction_path.joinpath("chapter.tex").write_text(
        "\n".join(
            [
                "% Generated by tex/build_swebok_structure.py.",
                *[rf"\input{{{path.relative_to(ROOT / 'tex').as_posix()}}}" for path in inputs],
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    rows = ["chapter\tnumber\tjapanese\tenglish\tpath"]

    root_lines = [
        "# SWEBOK v4.0a PDF-Aligned Structure",
        "",
        "このディレクトリは `.working/swebok-v4.pdf` の目次に合わせた、章 01-06 の日英併記ディレクトリ構成です。",
        "英語名の空白は `_` で接続しています。PDF で番号がない Introduction は `N.0.導入(Introduction)` として新設しています。",
        "",
        "## Chapters",
        "",
    ]

    for chapter in CHAPTERS:
        chapter_name = dir_name(f"CH{chapter.num:02d}", chapter.ja, chapter.en)
        chapter_path = OUT_DIR / chapter_name
        chapter_path.mkdir(parents=True)
        write_readme(chapter_path, f"CH{chapter.num:02d}. {chapter.ja} ({chapter.en})", chapter.ja, chapter.en, chapter.entries)
        root_lines.append(f"- [CH{chapter.num:02d}. {chapter.ja} ({chapter.en})](./{chapter_name}/)")
        rows.append(
            "\t".join(
                [
                    f"CH{chapter.num:02d}",
                    f"CH{chapter.num:02d}",
                    chapter.ja,
                    chapter.en,
                    chapter_path.relative_to(ROOT).as_posix(),
                ]
            )
        )
        for entry in chapter.entries:
            write_entry(chapter_path, entry, chapter, rows)

    root_lines.append("")
    OUT_DIR.joinpath("README.md").write_text("\n".join(root_lines), encoding="utf-8")
    MANIFEST.write_text("\n".join(rows) + "\n", encoding="utf-8")
    mirror_chapter01_content()
    print(f"wrote {OUT_DIR}")
    print(f"wrote {MANIFEST}")


if __name__ == "__main__":
    main()
