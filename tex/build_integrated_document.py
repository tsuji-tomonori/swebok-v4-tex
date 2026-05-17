#!/usr/bin/env python3
"""Build the integrated SWEBOK Japanese chapter TeX document.

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
MASTER_TEX = OUT_DIR / "swebok_v4_ch01_18_ja_master.tex"
PARTS_DIR = OUT_DIR / "chapters"
MANIFEST = OUT_DIR / "swebok_v4_ch01_06_ja_figures_manifest.tsv"
IMAGE_DIR = OUT_DIR / "assets" / "generated_figures"
PROMPT_DIR = OUT_DIR / "imagegen_prompts"
IMAGEGEN_MANIFEST = OUT_DIR / "swebok_v4_ch01_06_ja_imagegen_manifest.tsv"


TERM_ENGLISH = {
    "ソフトウェア": "Software",
    "要求": "Requirement",
    "利害関係者": "Stakeholder",
    "システム": "System",
    "仕様": "Specification",
    "妥当性確認": "Validation",
    "追跡可能性": "Traceability",
    "ソフトウェア要求": "Software Requirement",
    "ソフトウェア製品要求": "Software Product Requirement",
    "ソフトウェアプロジェクト要求": "Software Project Requirement",
    "製品要求": "Product Requirement",
    "プロジェクト要求": "Project Requirement",
    "機能要求": "Functional Requirement",
    "非機能要求": "Nonfunctional Requirement",
    "技術制約": "Technical Constraint",
    "サービス品質制約": "Quality of Service Constraint",
    "システム要求": "System Requirement",
    "派生要求": "Derived Requirement",
    "要求開発": "Requirements Development",
    "要求管理": "Requirements Management",
    "要求獲得": "Requirements Elicitation",
    "要求分析": "Requirements Analysis",
    "要求仕様化": "Requirements Specification",
    "要求妥当性確認": "Requirements Validation",
    "要求レビュー": "Requirements Review",
    "要求変更管理": "Requirements Change Management",
    "範囲調整": "Scope Adjustment",
    "要求の優先順位付け": "Requirements Prioritization",
    "要求の安定性": "Requirements Stability",
    "変動性": "Variability",
    "機能規模測定": "Functional Size Measurement",
    "要求管理ツール": "Requirements Management Tool",
    "要求モデリングツール": "Requirements Modeling Tool",
    "アーキテクチャ": "Architecture",
    "関心事": "Concern",
    "アーキテクチャ記述": "Architecture Description",
    "ビュー": "Architecture View",
    "ビューポイント": "Architecture Viewpoint",
    "合成的手法": "Synthetic Method",
    "射影的手法": "Projective Method",
    "設計": "Design",
    "ソフトウェア設計": "Software Design",
    "ソフトウェア設計記述": "Software Design Description",
    "設計思考": "Design Thinking",
    "横断的関心事": "Crosscutting Concern",
    "モデルに基づく設計": "Model-Based Design",
    "モデル駆動開発": "Model-Driven Development",
    "構造設計記述": "Structural Design Description",
    "振る舞い設計記述": "Behavioral Design Description",
    "設計パターン": "Design Pattern",
    "スタイル": "Style",
    "領域固有言語": "Domain-Specific Language",
    "設計根拠": "Design Rationale",
    "分割統治": "Divide and Conquer",
    "段階的詳細化": "Stepwise Refinement",
    "機能指向設計": "Function-Oriented Design",
    "構造化設計": "Structured Design",
    "データ中心設計": "Data-Centered Design",
    "オブジェクト指向設計": "Object-Oriented Design",
    "利用者中心設計": "User-Centered Design",
    "構成要素ベース設計": "Component-Based Design",
    "イベント駆動設計": "Event-Driven Design",
    "アスペクト指向設計": "Aspect-Oriented Design",
    "制約に基づく設計": "Constraint-Based Design",
    "ドメイン駆動設計": "Domain-Driven Design",
    "サービス指向設計": "Service-Oriented Design",
    "設計レビュー": "Design Review",
    "設計監査": "Design Audit",
    "測度": "Measure",
    "メトリクス": "Metric",
    "構築": "Construction",
    "ソフトウェア構築": "Software Construction",
    "コーディング": "Coding",
    "デバッグ": "Debugging",
    "単体テスト": "Unit Testing",
    "統合": "Integration",
    "誤り処理": "Error Handling",
    "例外処理": "Exception Handling",
    "耐故障性": "Fault Tolerance",
    "相互運用性": "Interoperability",
    "保証": "Assurance",
    "セキュリティ": "Security",
    "安全性": "Safety",
    "テスト": "Testing",
    "ソフトウェアテスト": "Software Testing",
    "テストケース": "Test Case",
    "テスト技法": "Test Technique",
    "静的テスト": "Static Testing",
    "動的テスト": "Dynamic Testing",
    "レビュー": "Review",
    "欠陥": "Defect",
    "故障": "Failure",
    "誤り": "Error",
    "保守": "Maintenance",
    "ソフトウェア保守": "Software Maintenance",
    "保守性": "Maintainability",
    "保守プロセス": "Maintenance Process",
    "影響分析": "Impact Analysis",
    "変更要求": "Change Request",
    "構成管理": "Configuration Management",
    "ソフトウェア構成管理": "Software Configuration Management",
    "構成品目": "Configuration Item",
    "ソフトウェア構成品目": "Software Configuration Item",
    "基準版": "Baseline",
    "構成識別": "Configuration Identification",
    "構成制御": "Configuration Control",
    "構成状態記録": "Configuration Status Accounting",
    "ソフトウェア構成状態記録・報告": "Software Configuration Status Accounting",
    "構成監査": "Configuration Audit",
    "機能構成監査": "Functional Configuration Audit",
    "物理構成監査": "Physical Configuration Audit",
    "ソフトウェア部品表": "Software Bill of Materials",
    "版記述文書": "Version Description Document",
    "変更管理": "Change Management",
    "変更統制": "Change Control",
    "版管理": "Version Control",
    "リリース管理": "Release Management",
    "ビルド": "Build",
    "継続的統合": "Continuous Integration",
    "継続的デリバリ": "Continuous Delivery",
    "プロジェクト": "Project",
    "プロジェクト計画": "Project Planning",
    "プロジェクト監視": "Project Monitoring",
    "プロジェクト制御": "Project Control",
    "開始": "Initiation",
    "範囲定義": "Scope Definition",
    "実現可能性分析": "Feasibility Analysis",
    "見積り": "Estimation",
    "リスク": "Risk",
    "リスク管理": "Risk Management",
    "測定": "Measurement",
    "情報ニーズ": "Information Need",
    "測定量": "Measure",
    "情報製品": "Information Product",
    "終結": "Closure",
    "成果物": "Deliverable",
    "ライフサイクル": "Life Cycle",
    "予測型ライフサイクル": "Predictive Life Cycle",
    "適応型ライフサイクル": "Adaptive Life Cycle",
    "モデル": "Model",
    "モデリング": "Modeling",
    "構造モデル": "Structural Model",
    "振る舞いモデル": "Behavioral Model",
    "モデルの分析": "Model Analysis",
    "ソフトウェア工学方法": "Software Engineering Method",
    "実体": "Entity",
    "関係": "Relationship",
    "形式手法": "Formal Method",
    "プロトタイピング": "Prototyping",
    "アジャイル方法": "Agile Method",
    "品質": "Quality",
    "ソフトウェア品質": "Software Quality",
    "ソフトウェア製品品質": "Software Product Quality",
    "ソフトウェアプロセス品質": "Software Process Quality",
    "品質要求": "Quality Requirement",
    "ソフトウェア品質コスト": "Cost of Software Quality",
    "適合費用": "Conformance Cost",
    "不適合費用": "Nonconformance Cost",
    "直接ソフトウェア": "Direct Software",
    "間接ソフトウェア": "Indirect Software",
    "保証ケース": "Assurance Case",
    "ディペンダビリティ": "Dependability",
    "完全性レベル": "Integrity Level",
    "ソフトウェア品質マネジメント": "Software Quality Management",
    "品質マネジメントシステム": "Quality Management System",
    "ソフトウェア品質改善": "Software Quality Improvement",
    "品質機能展開": "Quality Function Deployment",
    "個人ソフトウェアプロセス": "Personal Software Process",
    "誤り密度": "Error Density",
    "欠陥密度": "Defect Density",
    "故障率": "Failure Rate",
    "是正処置": "Corrective Action",
    "予防処置": "Preventive Action",
    "根本原因分析": "Root Cause Analysis",
    "ソフトウェア品質保証": "Software Quality Assurance",
    "ソフトウェア品質計画": "Software Quality Plan",
    "ソフトウェア品質保証計画": "Software Quality Assurance Plan",
    "作業成果物": "Work Product",
    "検証": "Verification",
    "独立検証妥当性確認": "Independent Verification and Validation",
    "静的解析": "Static Analysis",
    "動的解析": "Dynamic Analysis",
    "形式的解析": "Formal Analysis",
    "ソフトウェア品質制御": "Software Quality Control",
    "ピアレビュー": "Peer Review",
    "脅威": "Threat",
    "脆弱性": "Vulnerability",
    "攻撃": "Attack",
    "リスク分析": "Risk Analysis",
    "リスク評価": "Risk Evaluation",
    "アクセス制御": "Access Control",
    "認証": "Authentication",
    "認可": "Authorization",
    "暗号": "Cryptography",
    "機密性": "Confidentiality",
    "完全性": "Integrity",
    "可用性": "Availability",
    "専門職実務": "Professional Practice",
    "倫理": "Ethics",
    "専門職責任": "Professional Responsibility",
    "チームワーク": "Teamwork",
    "コミュニケーション": "Communication",
    "経済": "Economics",
    "ソフトウェア工学経済": "Software Engineering Economics",
    "意思決定": "Decision Making",
    "リスク下の意思決定": "Decision Making Under Risk",
    "不確実性下の意思決定": "Decision Making Under Uncertainty",
    "費用便益分析": "Cost-Benefit Analysis",
    "投資収益率": "Return on Investment",
    "正味現在価値": "Net Present Value",
    "内部収益率": "Internal Rate of Return",
    "損益分岐点": "Break-Even Point",
    "無形資産": "Intangible Asset",
    "コンピューティング": "Computing",
    "サブシステム": "Subsystem",
    "モジュール": "Module",
    "コンピュータアーキテクチャ": "Computer Architecture",
    "コンピュータ組織": "Computer Organization",
    "データ構造": "Data Structure",
    "アルゴリズム": "Algorithm",
    "計算量": "Computational Complexity",
    "基本ソフトウェア": "System Software",
    "プロトコル": "Protocol",
    "人間要因": "Human Factors",
    "データベース": "Database",
    "オペレーティングシステム": "Operating System",
    "人工知能": "Artificial Intelligence",
    "機械学習": "Machine Learning",
    "論理": "Logic",
    "命題": "Proposition",
    "述語": "Predicate",
    "集合": "Set",
    "関数": "Function",
    "関係": "Relation",
    "グラフ": "Graph",
    "木": "Tree",
    "有限状態機械": "Finite State Machine",
    "文法": "Grammar",
    "数論": "Number Theory",
    "確率": "Probability",
    "数値精度": "Numerical Precision",
    "代数構造": "Algebraic Structure",
    "微積分": "Calculus",
    "証明": "Proof",
    "公理・仮定": "Axiom and Assumption",
    "定理": "Theorem",
    "補題": "Lemma",
    "系": "Corollary",
    "予想": "Conjecture",
    "直接証明": "Direct Proof",
    "背理法": "Proof by Contradiction",
    "対偶証明": "Proof by Contrapositive",
    "数学的帰納法": "Mathematical Induction",
    "基底段階": "Base Step",
    "帰納法の仮定": "Induction Hypothesis",
    "帰納段階": "Induction Step",
    "形式言語": "Formal Language",
    "工学": "Engineering",
    "工学プロセス": "Engineering Process",
    "工学設計": "Engineering Design",
    "抽象化": "Abstraction",
    "カプセル化": "Encapsulation",
    "階層": "Hierarchy",
    "経験的方法": "Empirical Method",
    "統計分析": "Statistical Analysis",
    "標準": "Standard",
    "インダストリー4.0": "Industry 4.0",
    "不完全性": "Incompleteness",
    "曖昧性": "Ambiguity",
    "方針": "Policy",
    "プロセス": "Process",
    "顧客": "Customer",
    "利用者": "User",
    "業務専門家": "Domain Expert",
    "運用担当": "Operator",
    "サポート担当": "Support Staff",
    "規制当局・専門団体": "Regulatory Authority and Professional Organization",
    "開発者": "Developer",
    "面接": "Interview",
    "会議・討議": "Meeting and Discussion",
    "促進付きワークショップ": "Facilitated Workshop",
    "質問票・市場調査": "Questionnaire and Market Survey",
    "観察": "Observation",
    "徒弟型学習": "Apprenticing",
    "試作": "Prototyping",
    "ユーザーストーリーマッピング": "User Story Mapping",
    "文献・標準調査": "Document and Standard Study",
    "一意に解釈できる": "Unambiguous",
    "テスト可能である": "Testable",
    "拘束力がある": "Binding",
    "原子的である": "Atomic",
    "真のニーズを表す": "Representing Real Needs",
    "利害関係者の語彙を使う": "Using Stakeholder Vocabulary",
    "関係者に受け入れられる": "Acceptable to Stakeholders",
    "簡潔性": "Conciseness",
    "内部整合性": "Internal Consistency",
    "外部整合性": "External Consistency",
    "実現可能性": "Feasibility",
    "失敗点": "Failure Point",
    "完全点": "Saturation Point",
    "形式的分析": "Formal Analysis",
    "製品群開発": "Product Line Development",
    "非構造化自然言語": "Unstructured Natural Language",
    "構造化自然言語": "Structured Natural Language",
    "主体・動作形式": "Subject-Action Form",
    "ユースケース仕様": "Use Case Specification",
    "ユーザーストーリー": "User Story",
    "決定表": "Decision Table",
    "受け入れ基準": "Acceptance Criteria",
    "受け入れテスト駆動開発": "Acceptance Test-Driven Development",
    "振る舞い駆動開発": "Behavior-Driven Development",
    "増分的仕様化": "Incremental Specification",
    "包括的仕様化": "Comprehensive Specification",
    "実行": "Execution",
    "シミュレーション": "Simulation",
    "プロトタイプ": "Prototype",
    "要求整理・削減": "Requirements Scrubbing",
    "分野": "Discipline",
    "活動": "Activity",
    "成果": "Result",
    "アーキテクチャ技術的負債": "Architecture Technical Debt",
    "分析": "Analysis",
    "評価": "Evaluation",
    "アーキテクチャ設計": "Architecture Design",
    "アーキテクチャ実装管理": "Architecture Implementation Management",
    "アーキテクチャ保守": "Architecture Maintenance",
    "アーキテクチャ管理": "Architecture Management",
    "アーキテクチャ知識管理": "Architecture Knowledge Management",
    "要求との関係": "Relationship to Requirements",
    "アーキテクチャとの関係": "Relationship to Architecture",
    "実装との関係": "Relationship to Implementation",
    "テストとの関係": "Relationship to Testing",
    "高水準設計": "High-Level Design",
    "詳細設計": "Detailed Design",
    "生成パターン": "Creational Pattern",
    "構造パターン": "Structural Pattern",
    "振る舞いパターン": "Behavioral Pattern",
    "モデルの種類": "Types of Models",
    "回避": "Avoidance",
    "検出と除去": "Detection and Removal",
    "損害限定": "Damage Limitation",
    "CR": "Change Request",
    "CCB / SCCB": "Configuration Control Board / Software Configuration Control Board",
    "CI": "Configuration Item",
    "SCI": "Software Configuration Item",
    "CM / SCM": "Configuration Management / Software Configuration Management",
    "SCMP": "Software Configuration Management Plan",
    "SCSA": "Software Configuration Status Accounting",
    "FCA / PCA": "Functional Configuration Audit / Physical Configuration Audit",
    "SBOM": "Software Bill of Materials",
    "VDD": "Version Description Document",
    "CAD": "Computer-Aided Design",
    "CMMI": "Capability Maturity Model Integration",
    "PDF": "Probability Density Function",
    "PMF": "Probability Mass Function",
    "RCA": "Root Cause Analysis",
    "SDLC": "Software Development Life Cycle",
}


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
    Chapter(7, "ソフトウェア保守", ROOT / "work" / "swebok_ch07_software_maintenance_ja_regenerated.tex"),
    Chapter(8, "ソフトウェア構成管理", ROOT / "work" / "software_configuration_management_chapter08_ja_A4_regenerated.tex"),
    Chapter(9, "ソフトウェアエンジニアリング管理", ROOT / "work" / "software_engineering_management_chapter09_ja_A4_regenerated.tex"),
    Chapter(10, "ソフトウェア工学プロセス", ROOT / "work" / "software_engineering_process_chapter10_ja_A4_regenerated.tex"),
    Chapter(11, "ソフトウェア工学モデルと方法", ROOT / "work" / "software_models_methods_chapter11_ja_A4_regenerated.tex"),
    Chapter(12, "ソフトウェア品質", ROOT / "work" / "software_quality_chapter12_ja_A4_regenerated.tex"),
    Chapter(13, "ソフトウェアセキュリティ", ROOT / "work" / "software_security_chapter13_ja_A4_final.tex"),
    Chapter(14, "ソフトウェア工学専門職実務", ROOT / "work" / "software_engineering_professional_practice_chapter14_ja_A4.tex"),
    Chapter(15, "ソフトウェア工学経済", ROOT / "work" / "ch15_swebok_ja.tex"),
    Chapter(16, "コンピューティング基礎", ROOT / "work" / "computing_foundations_chapter16_ja_A4.tex"),
    Chapter(17, "数学的基礎", ROOT / "work" / "software_mathematical_foundations_chapter17_ja.tex"),
    Chapter(18, "工学基礎", ROOT / "work" / "engineering_foundations_chapter18_ja_A4.tex"),
]

CHAPTER_RANGE_LABEL = "第 01--18 章"
CHAPTER_EN_LABEL = (
    "Software Requirements / Architecture / Design / Construction / Testing / "
    "Engineering Operations / Maintenance / Configuration Management / "
    "Engineering Management / Engineering Process / Models and Methods / "
    "Software Quality / Software Security / Professional Practice / "
    "Engineering Economics / Computing Foundations / Mathematical Foundations / "
    "Engineering Foundations"
)


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
\usepackage{calc}
\usepackage{enumitem}
\usepackage{indentfirst}
\usepackage{amsmath,amssymb}
\usepackage{xparse}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,fit,shapes.geometric,calc}
\usepackage{titlesec}
\usepackage{hyperref}
\hypersetup{hidelinks,unicode=true,pdftitle={SWEBOK v4.0a 日本語統合まとめ},pdfauthor={OpenAI Codex}}

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
\renewcommand{\thesection}{\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}
\renewcommand{\thefigure}{\thesection.\arabic{figure}}
\renewcommand{\thetable}{\thesection.\arabic{table}}
\numberwithin{figure}{section}
\numberwithin{table}{section}

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
\fancyhead[R]{第 01--18 章}
\fancyfoot[C]{\thepage/\pageref*{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}

\titleformat{\section}{\Large}{\thesection.}{0.8em}{}
\titleformat{\subsection}{\large}{\thesubsection}{0.8em}{}
\titleformat{\subsubsection}{\normalsize}{\thesubsubsection}{0.8em}{}
\titleformat{\paragraph}{\normalsize}{}{0em}{}
\titlespacing*{\section}{0pt}{1.1em}{0.4em}
\titlespacing*{\subsection}{0pt}{0.9em}{0.25em}
\titlespacing*{\subsubsection}{0pt}{0.6em}{0.15em}
\titlespacing*{\paragraph}{0pt}{0.6em}{0.5em}

\newcounter{definition}
\NewDocumentCommand{\boxedblock}{m +m}{%
  \par\smallskip\noindent\makebox[\linewidth][l]{%
    \fbox{%
      \begin{minipage}{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}
      #1\par\smallskip
      #2
      \end{minipage}%
    }%
  }\par\smallskip
}
\NewDocumentEnvironment{statementbox}{m +b}{\boxedblock{#1}{#2}}{}
\NewDocumentEnvironment{plainbox}{+b}{\boxedblock{}{#1}}{}
\NewDocumentEnvironment{keybox}{m +b}{\boxedblock{#1}{#2}}{}
\NewDocumentEnvironment{pointbox}{m +b}{\boxedblock{#1}{#2}}{}
\NewDocumentEnvironment{notebox}{m +b}{\boxedblock{#1}{#2}}{}
\NewDocumentEnvironment{definitionbox}{+b}{\boxedblock{定義 \refstepcounter{definition}\thedefinition}{#1}}{}

\newcommand{\keyterm}[1]{\textbf{#1}}
\NewDocumentCommand{\term}{m g}{\textbf{#1}\IfNoValueF{#2}{（#2）}}
\newcommand{\en}[1]{（#1）}
\newcommand{\eng}[1]{\textsf{#1}}
\newcommand{\swebok}{\textit{SWEBOK Guide v4.0a}}
\newcommand{\Rule}{\par\smallskip\hrule\smallskip}
\newcommand{\MiniBox}[2]{\par\smallskip\begin{statementbox}{#1}#2\end{statementbox}\par\smallskip}
\newcommand{\SmallHead}[1]{\par\smallskip\noindent #1\quad}
""".strip()


DOCUMENT_OPENING = [
    r"\begin{document}",
    r"\thispagestyle{empty}",
    r"\begin{center}",
    r"{\LARGE\bfseries SWEBOK v4.0a 日本語統合まとめ}\par\vspace{1em}",
    rf"{{\Large {CHAPTER_RANGE_LABEL}}}\par\vspace{{0.8em}}",
    rf"{{\large {CHAPTER_EN_LABEL}}}\par\vspace{{1em}}",
    r"{作成日：2026 年 5 月 12 日}\par",
    r"\end{center}",
    r"\vspace{1em}\hrule\vspace{0.8em}",
    r"\tableofcontents",
    r"\clearpage",
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


def clean_heading(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"^\d+(?:\.\d+)*[.\s　]+", "", title)
    return title.strip("。 ")


def latest_heading_before(text: str, position: int) -> str | None:
    candidates = list(
        re.finditer(
            r"\\(?:section|subsection|subsubsection|paragraph)\*?\{([^{}]+)\}",
            text[:position],
        )
    )
    if not candidates:
        return None
    return clean_heading(candidates[-1].group(1))


def first_table_header(text: str, start: int) -> str | None:
    match = re.search(r"\\(?:toprule|hline)\s*\n([^\\]+?)\\\\", text[start:], flags=re.S)
    if not match:
        return None
    cells = [re.sub(r"\s+", " ", cell).strip() for cell in match.group(1).split("&")]
    cells = [cell for cell in cells if cell]
    if len(cells) < 2:
        return None
    return "・".join(cells[:3])


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
    title = tex_escape(clean_title(spec.title))
    missing = rf"\fbox{{\parbox[c][48mm][c]{{0.9\linewidth}}{{\centering 画像生成待ち\\{tex_escape(clean_title(spec.title))}}}}}"
    return "\n".join(
        [
            r"\par\smallskip",
            r"\begin{center}",
            r"\centering",
            rf"\IfFileExists{{{spec.image_relpath}}}{{\includegraphics[width=0.96\linewidth]{{{spec.image_relpath}}}}}{{{missing}}}",
            r"\par\smallskip",
            rf"\refstepcounter{{figure}}\label{{{spec.label}}}図 \thefigure: {title}",
            r"\end{center}",
            rf"図 \thefigure は、{title}を視覚的に整理したものである。",
            r"\par\smallskip",
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
    return f"""$image

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

    def normalize_todo_text(text: str) -> tuple[str, str] | None:
        text = re.sub(r"\\par\b", "\n", text)
        text = re.sub(r"\\(?:smallskip|medskip|vspace\{[^{}]*\})", "\n", text)
        text = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", text)
        text = re.sub(r"\\(?:begin|end)\{center\}", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        match = re.search(r"TODO（図）\s*(.*?)\s*画像生成用プロンプト\s*(.*)", text, flags=re.S)
        if match:
            return match.group(1).strip("。 "), match.group(2).strip()
        match = re.search(r"^(.*?)\s*画像生成用プロンプト\s*(.*)", text, flags=re.S)
        if match:
            return match.group(1).strip("。 "), match.group(2).strip()
        return None

    body = re.sub(
        r"\\(?:TodoFigure|todofig)\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: add(m.group(1), m.group(2)),
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\todobox\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
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
    body = re.sub(
        r"\\begin\{center\}\s*\\fbox\{\\parbox\{[^{}]*\}\{(.*?画像生成用プロンプト.*?)\}\}\s*\\end\{center\}",
        lambda m: add(*normalize_todo_text(m.group(1))) if normalize_todo_text(m.group(1)) else m.group(0),
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\begin\{center\}\s*\\fbox\{\\begin\{minipage\}\{[^{}]*\}(.*?画像生成用プロンプト.*?)\\end\{minipage\}\}\s*\\end\{center\}",
        lambda m: add(*normalize_todo_text(m.group(1))) if normalize_todo_text(m.group(1)) else m.group(0),
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
    body = re.sub(
        r"\\begin\{todobox\}\s*(.*?)\s*\\end\{todobox\}",
        lambda m: add(*normalize_todo_text(m.group(1))) if normalize_todo_text(m.group(1)) else m.group(0),
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
        heading = latest_heading_before(body, match.start())
        header = first_table_header(body, match.end())
        if heading and header:
            caption = f"{heading}における{header}"
        elif heading:
            caption = f"{heading}の整理"
        elif header:
            caption = f"{chapter.title}における{header}"
        else:
            caption = f"{chapter.title}の整理"
        escaped_caption = tex_escape(caption)
        return (
            rf"\par\smallskip\noindent\refstepcounter{{table}}\label{{tab:ch{chapter.no:02d}-{table_index:02d}}}表 \thetable: {escaped_caption}\par\smallskip"
            + "\n"
            + rf"表 \thetable は、{escaped_caption}を比較・確認しやすい形で整理したものである。\par\smallskip"
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


def normalize_section_titles(body: str) -> str:
    return re.sub(
        r"\\(section|subsection|subsubsection|paragraph)(\*?)\{([^{}]+)\}",
        lambda m: rf"\{m.group(1)}{m.group(2)}{{{clean_heading(m.group(3))}}}",
        body,
    )


def normalize_bold_usage(body: str) -> str:
    def table_header_repl(match: re.Match[str]) -> str:
        line = re.sub(r"\\textbf\{([^{}]+)\}", r"\1", match.group(0))
        return line

    body = re.sub(r"(?m)^.*\\textbf\{[^{}]+\}.*\\\\\s*$", table_header_repl, body)
    body = re.sub(
        r"\\textbf\{(到達目標|学習順序|この資料の主張|この資料の読み方|解答の方向性)\}",
        r"\1",
        body,
    )
    body = re.sub(r"\\textbf\{([^{}]+)\}", r"\\keyterm{\1}", body)
    body = re.sub(r"\\noindent(?=[^\s\\{}])", r"\\noindent ", body)
    return body


def term_command(japanese: str, english: str | None = None) -> str:
    japanese = japanese.strip()
    english = (english or TERM_ENGLISH.get(japanese, "")).strip()
    if english:
        return rf"\term{{{japanese}}}{{{english}}}"
    return rf"\keyterm{{{japanese}}}"


def normalize_key_terms(body: str) -> str:
    body = re.sub(
        r"\\keyterm\{([^{}]+)\}\\en\{([^{}]+)\}",
        lambda m: term_command(m.group(1), m.group(2)),
        body,
    )
    body = re.sub(
        r"\\keyterm\{([^{}]+)\}",
        lambda m: term_command(m.group(1)),
        body,
    )
    body = re.sub(
        r"\\term\{([^{}]+)\}(?!\{)",
        lambda m: term_command(m.group(1)),
        body,
    )
    return body


def enrich_term_table_cells(body: str) -> str:
    env_pattern = re.compile(r"\\begin\{(longtable|tabularx|tabular)\}.*?\\end\{\1\}", re.S)

    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        lines = block.splitlines()
        result: list[str] = []
        for line in lines:
            stripped = line.strip()
            if (
                not stripped
                or stripped.startswith("\\")
                or "&" not in line
                or stripped.startswith("用語 ")
                or stripped.startswith("略語 ")
            ):
                result.append(line)
                continue
            first, rest = line.split("&", 1)
            leading = first[: len(first) - len(first.lstrip())]
            cell = first.strip()
            if cell.startswith(r"\term") or cell.startswith(r"\keyterm"):
                result.append(line)
                continue
            english = TERM_ENGLISH.get(cell)
            if not english:
                result.append(line)
                continue
            result.append(f"{leading}{term_command(cell, english)} &{rest}")
        return "\n".join(result)

    return env_pattern.sub(repl, body)


def enrich_plain_term_leads(body: str) -> str:
    terms = sorted(TERM_ENGLISH, key=len, reverse=True)
    particles = ("とは", "は", "では", "には", "を", "に", "が")

    def repl_line(match: re.Match[str]) -> str:
        line = match.group(0)
        stripped = line.lstrip()
        if not stripped or stripped.startswith("\\") or stripped.startswith("%") or "&" in stripped:
            return line
        leading = line[: len(line) - len(stripped)]
        for term in terms:
            if len(term) < 2 or not stripped.startswith(term):
                continue
            rest = stripped[len(term) :]
            if rest.startswith(particles):
                return leading + term_command(term) + rest
        return line

    return re.sub(r"(?m)^[^\n]+", repl_line, body)


def enrich_known_terms(body: str) -> str:
    body = normalize_key_terms(body)
    body = enrich_term_table_cells(body)
    body = enrich_plain_term_leads(body)
    body = normalize_key_terms(body)
    return body


def keep_first_term_occurrences(chapters: list[str]) -> list[str]:
    """Keep term decoration only for the first occurrence in document order."""
    seen: set[str] = set()
    term_pattern = re.compile(r"\\(?:term|keyterm)\{([^{}]+)\}(?:\{([^{}]+)\})?")

    def replace_term(match: re.Match[str]) -> str:
        japanese = match.group(1).strip()
        english = (match.group(2) or "").strip()
        if japanese in seen:
            return japanese
        seen.add(japanese)
        return term_command(japanese, english)

    return [term_pattern.sub(replace_term, chapter) for chapter in chapters]


def normalize_body(chapter: Chapter, figures: list[FigureSpec]) -> str:
    source = chapter.path.read_text(encoding="utf-8")
    begin = source.index(r"\begin{document}") + len(r"\begin{document}")
    end = source.rindex(r"\end{document}")
    body = source[begin:end].strip()
    body = strip_titlepage(body)
    body = re.sub(r"\\maketitle\s*", "", body)
    body = re.sub(r"\\title\{.*?\}\s*", "", body, flags=re.S)
    body = re.sub(r"\\author\{.*?\}\s*", "", body, flags=re.S)
    body = re.sub(r"\\date\{.*?\}\s*", "", body, flags=re.S)
    body = re.sub(r"\\tableofcontents\s*(?:\\clearpage|\\newpage)?", "", body)
    body = re.sub(r"\\setcounter\{page\}\{[^{}]*\}\s*", "", body)
    body = body.replace("leftmargin=2zw", "leftmargin=2em")
    body = body.replace("leftmargin=1zw", "leftmargin=1em")
    body = re.sub(r"^(?:\\clearpage|\\newpage)\s*", "", body)
    body = re.sub(
        r"\\section\*?\{\d*\s*画像\s*TODO\s*一覧\}.*?(?=\\section\{[^{}]*章末確認問題\}|\\section\*\{[^{}]*章末確認問題\}|$)",
        "",
        body,
        flags=re.S,
    )
    body = replace_todo_macros(body, chapter.no, figures)
    body = re.sub(
        r"\\noteBox\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{notebox}{" + m.group(1) + "}" + m.group(2) + r"\end{notebox}",
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\pointbox\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{pointbox}{" + m.group(1) + "}" + m.group(2) + r"\end{pointbox}",
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\boxblock\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{pointbox}{" + m.group(1) + "}" + m.group(2) + r"\end{pointbox}",
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\pointbox\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{pointbox}{" + m.group(1) + "}" + m.group(2) + r"\end{pointbox}",
        body,
        flags=re.S,
    )
    body = body.replace(r"\begin{claimbox}", r"\begin{pointbox}{この資料の主張}")
    body = body.replace(r"\end{claimbox}", r"\end{pointbox}")
    body = re.sub(
        r"\\begin\{importantbox\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{pointbox}{" + m.group(1) + "}",
        body,
        flags=re.S,
    )
    body = body.replace(r"\begin{importantbox}", r"\begin{pointbox}{重要}")
    body = body.replace(r"\end{importantbox}", r"\end{pointbox}")
    body = body.replace(r"\begin{infobox}", r"\begin{notebox}")
    body = body.replace(r"\end{infobox}", r"\end{notebox}")
    body = re.sub(
        r"\\infobox\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{notebox}{" + m.group(1) + "}" + m.group(2) + r"\end{notebox}",
        body,
        flags=re.S,
    )
    body = body.replace(r"\begin{claimbox}", r"\begin{notebox}{要点}")
    body = body.replace(r"\end{claimbox}", r"\end{notebox}")
    body = body.replace(r"\begin{readbox}", r"\begin{notebox}{読み方}")
    body = body.replace(r"\end{readbox}", r"\end{notebox}")
    body = body.replace(r"\begin{examplebox}", r"\begin{notebox}{例}")
    body = body.replace(r"\end{examplebox}", r"\end{notebox}")
    body = body.replace(r"\begin{termnote}", r"\begin{notebox}{用語の見分け方}")
    body = body.replace(r"\end{termnote}", r"\end{notebox}")
    body = re.sub(
        r"\\smallterm\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\keyterm{" + m.group(1) + "}",
        body,
        flags=re.S,
    )
    body = re.sub(
        r"\\begin\{notebox\}(?!\{)",
        r"\\begin{notebox}{注記}",
        body,
    )
    body = re.sub(
        r"\\begin\{defbox\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}",
        lambda m: r"\begin{definitionbox}" + m.group(1) + r"\par\smallskip ",
        body,
        flags=re.S,
    )
    body = body.replace(r"\end{defbox}", r"\end{definitionbox}")
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
    body = normalize_section_titles(body)
    body = normalize_bold_usage(body)
    body = enrich_known_terms(body)
    body = re.sub(
        r"(\\end\{(?:longtable|tabularx|tabular)\})\s*(?=\\begin\{figure\})",
        lambda m: m.group(1) + "\n\n",
        body,
    )
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
            input_lines.append(rf"\input{{{rel}}}")

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
    chapters = keep_first_term_occurrences(chapters)
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
