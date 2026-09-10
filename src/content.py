# -*- coding: utf-8 -*-
"""
Content for evemisslab.com — the lab's front door.

The job of this page is to be an index. EveMissLab publishes one site per
thing it builds, and the set keeps growing, so the homepage is designed to
take twenty entries as gracefully as it takes eight.

Every one-line description is taken from that subsite's own meta description
or its own README, not written fresh here. Each entry also carries the accent
colour sampled from that subsite's own stylesheet, which is why this is the
only page in the family where the whole palette appears at once.
"""

SITE = {
    "domain": "evemisslab.com",
    "origin": "https://evemisslab.com",
    "company_en": "EVEMISSLAB Co., Ltd.",
    "company_zh": "一言諾科技有限公司",
    "year": "2026",
}

# --------------------------------------------------------------------------
# The index. `tone` is sampled from each subsite's own CSS custom properties.
# --------------------------------------------------------------------------

GROUPS = {
    "en": [
        {
            "key": "auditable",
            "title": "Auditable computation",
            "note": "Built on one idea: a result is worth less than a result you can re-run, and a claim is worth less than a claim that states its own boundary.",
            "sites": [
                {
                    "host": "sssp", "name": "SSSP", "tone": "sssp",
                    "what": "An AI-native scholarly authoring protocol that separates discussion and rendered views from canonical source, then guards typed mutations with revisions, checksums and validation.",
                    "meta": "Research MVP · MCP v0.2",
                },
                {
                    "host": "mmr", "name": "MMR-Bench", "tone": "mmr",
                    "what": "Three independent readings of every formula cell, signed Ed25519 computation certificates, and exact replay. Engine disagreement never authorizes a formula rewrite.",
                    "meta": "Apache-2.0 · v1.0",
                },
                {
                    "host": "mmlc", "name": "MMLC Runtime", "tone": "mmlc",
                    "what": "An auditable runtime for typed matrix-ledger documents: deterministic and symbolic execution, provenance, constraints, temporal fixed points, counterfactual branches and finite decision analysis in one execution model.",
                    "meta": "Apache-2.0 · v1.0.0",
                },
                {
                    "host": "mlf", "name": "MLF", "tone": "mlf",
                    "what": "An AI-native matrix knowledge format with a reference compiler. Keeps coordinates, regions, roles, formulas, dependency edges and provenance instead of flattening them into one token sequence.",
                    "meta": "Apache-2.0 · MLF 1.0",
                },
                {
                    "host": "dieec", "name": "DIEEC", "tone": "dieec",
                    "what": "A symbolic runtime for dual internal–external expansion computation: a frozen public API, one certificate envelope for every claim, migration for old ledgers, and a release gate that treats passing tests as necessary but not sufficient.",
                    "meta": "Apache-2.0 · v1.0.1",
                },
                {
                    "host": "anla", "name": "ANLA", "tone": "anla",
                    "what": "A lossless archive format an AI can plan and a deterministic, model-independent decoder must restore exactly. The 1.0 draft set itself a rule — nothing frozen until two independent implementations produce byte-identical archives and a differential fuzzer finds no disagreement — and a Python writer and a Rust writer now meet both halves of it.",
                    "meta": "Apache-2.0 · v0.1.0 · 1.0 draft, freeze rule met",
                },
                {
                    "host": "mmpf", "name": "MMPF", "tone": "mmpf",
                    "what": "A route-aware factorization runtime that has to choose before it knows what the choice will cost. Performance mode takes the lowest predicted cost; assurance mode takes the lowest bound it can certify, and is slower on purpose.",
                    "meta": "Apache-2.0 · v1.0.0rc1",
                },
                {
                    "host": "mmrf", "name": "MMRF", "tone": "mmrf",
                    "what": "A public prime dataset defined as much by what it refuses as by what it answers. The query surface is aggregate-only, and the guard that refuses a target-conditioned request runs before any shard is read.",
                    "meta": "Apache-2.0 · v1.0",
                },
                {
                    "host": "utf-8x", "name": "UTF-8X", "tone": "utf8x",
                    "what": "UTF-8 stays the verified semantic anchor while storage, search, editing and inference each get a reversible representation suited to their own costs. AI generates the strategy and is never required to decode.",
                    "meta": "Apache-2.0 · v0.22 baseline",
                },
            ],
        },
        {
            "key": "archives",
            "title": "Research archives",
            "note": "Corpora meant to be read by machines as readily as by people.",
            "sites": [
                {
                    "host": "unboundedaxiom.org", "name": "Logic Matrix", "tone": "logic",
                    "what": "An AI-readable theoretical corpus, with live research programmes running inside it.",
                    "meta": "Corpus",
                },
                {
                    "host": "amral", "name": "AMRAL", "tone": "amral",
                    "what": "Autonomous Mathematical Research Agent Loop — the methodology and a field archive of what the loop actually produced.",
                    "meta": "Archive",
                },
            ],
        },
        {
            "key": "systems",
            "title": "Working systems",
            "note": "Things that run, rather than things that are described.",
            "sites": [
                {
                    "host": "felra", "name": "FELRA", "tone": "felra",
                    "what": "A Python-first academic verification and visualization workbench for GCPR–RWL–FELRA, turning theory and data into reproducible computational evidence.",
                    "meta": "Workbench",
                },
                {
                    "host": "apr", "name": "APR", "tone": "apr",
                    "what": "A runtime for deciding when an agent should observe, what it should read, how deeply it should read, when it must reobserve, and when fresh evidence means it should stop reading.",
                    "meta": "Research MVP · v0.10",
                },
                {
                    "host": "axioglyph", "name": "Axioglyph", "tone": "axioglyph",
                    "what": "A glyph lab where a symbol is more than a picture. Change its form, sound and meaning, then see exactly why the recipe passes or fails.",
                    "meta": "Interactive lab · EMPSL v0.4",
                },
                {
                    "host": "storyforge", "name": "Storyforge", "tone": "storyforge",
                    "what": "An English-first bilingual writing and reading platform for AI-authored fables, fairy tales and classic reinterpretations.",
                    "meta": "Platform",
                },
                {
                    "host": "ai-board", "name": "AI Board", "tone": "aiboard",
                    "what": "A public machine-readable notice board for AI agents, search systems and cognitive-architecture research. It answers browsers in plain text too, because it was not built to be looked at.",
                    "meta": "Protocol · MCP",
                },
                {
                    "host": "drvs", "name": "DRVS", "tone": "drvs",
                    "what": "A corpus-agnostic, mostly client-side search engine. Instead of replacing your page with a result list, it dims what does not match and tells you why what is left is there.",
                    "meta": "MIT · v0.1.0",
                },
                {
                    "host": "ms3e", "name": "MS3E", "tone": "ms3e",
                    "what": "A multilayer nested spectral skeleton state engine. Compiles linear media into an identity skeleton, deformation layers and a spectral decomposition, then reconstructs from a state vector instead of a timestamp. The engine itself runs on the page.",
                    "meta": "Apache-2.0 · v1.0.1",
                },
                {
                    "host": "commoninstant.org", "name": "CTCL", "tone": "ctcl",
                    "what": "A verified reference instant plus heterogeneous time transformation for agents, simulators and persistent AI — over REST or a stateless Remote MCP Gateway. Its Ed25519-signed instants now also serve as an independent, third-party witness for CTCL-ITR's temporal ledger anchors, and back the local-first Temporal Port desktop app.",
                    "meta": "Apache-2.0 · v0.1 · ctcl-app · ctcl-itr",
                },
            ],
        },
    ],
    "zh": [
        {
            "key": "auditable",
            "title": "可稽核的計算",
            "note": "建立在同一個想法上：一個結果的價值低於一個你能重跑的結果，而一項主張的價值低於一項會說出自己邊界的主張。",
            "sites": [
                {
                    "host": "sssp", "name": "SSSP", "tone": "sssp",
                    "what": "一套 AI 原生的學術寫作協定：把討論與渲染視圖和 canonical source 分開，再以 revision、checksum 與 validation 保護具型別 mutation。",
                    "meta": "研究型 MVP · MCP v0.2",
                },
                {
                    "host": "mmr", "name": "MMR-Bench", "tone": "mmr",
                    "what": "對每個公式儲存格取三份獨立讀數、簽署 Ed25519 計算憑證、可完全重播。引擎意見不一致，永遠不構成改寫公式的授權。",
                    "meta": "Apache-2.0 · v1.0",
                },
                {
                    "host": "mmlc", "name": "MMLC Runtime", "tone": "mmlc",
                    "what": "處理具型別矩陣帳本文件的可稽核 Runtime：決定性與符號執行、血緣追蹤、約束、時間固定點、反事實分支與有限決策分析，全部收在同一個執行模型裡。",
                    "meta": "Apache-2.0 · v1.0.0",
                },
                {
                    "host": "mlf", "name": "MLF", "tone": "mlf",
                    "what": "AI 原生的矩陣知識格式，附參考編譯器。保住座標、區域、角色、公式、相依邊與來源歷程，而不是把它們壓平成一條 token 序列。",
                    "meta": "Apache-2.0 · MLF 1.0",
                },
                {
                    "host": "dieec", "name": "DIEEC", "tone": "dieec",
                    "what": "內外雙生展開計算的符號 Runtime：凍結的公開 API、所有宣稱共用一個證書信封、舊帳本可遷移，以及一道把「測試通過」視為必要但不充分的放行閘門。",
                    "meta": "Apache-2.0 · v1.0.1",
                },
                {
                    "host": "anla", "name": "ANLA", "tone": "anla",
                    "what": "一種可由 AI 規劃、但必須由確定性且不依賴模型的解碼器精確還原的無損封裝格式。1.0 草案給自己訂下一條規則——兩套獨立實作產生逐位元相同的封裝、且 differential fuzzer 找不到分歧之前，不凍結任何部分——而一個 Python writer 跟一個 Rust writer 現在同時滿足了它的兩個半部。",
                    "meta": "Apache-2.0 · v0.1.0 · 1.0 草案，凍結規則已達成",
                },
                {
                    "host": "mmpf", "name": "MMPF", "tone": "mmpf",
                    "what": "路徑感知的分解 Runtime，必須在還不知道代價之前就先選。效能模式取預測成本最低的；保證模式取它能證明的上界最低的，而且刻意比較慢。",
                    "meta": "Apache-2.0 · v1.0.0rc1",
                },
                {
                    "host": "mmrf", "name": "MMRF", "tone": "mmrf",
                    "what": "一個公開的質數資料集，它被「拒絕什麼」定義的程度，跟被「回答什麼」定義的一樣多。查詢面只有聚合，而拒絕以目標為條件之請求的守衛，跑在任何分片被讀取之前。",
                    "meta": "Apache-2.0 · v1.0",
                },
                {
                    "host": "utf-8x", "name": "UTF-8X", "tone": "utf8x",
                    "what": "UTF-8 維持為受驗證的語義錨點，儲存、搜尋、編輯與推論各自取得符合自身成本的可逆表示。AI 生成策略，但解碼永遠不需要它。",
                    "meta": "Apache-2.0 · v0.22 基線",
                },
            ],
        },
        {
            "key": "archives",
            "title": "研究封存",
            "note": "設計成讓機器讀起來跟人一樣順的語料庫。",
            "sites": [
                {
                    "host": "unboundedaxiom.org", "name": "Logic Matrix", "tone": "logic",
                    "what": "一個 AI 可讀的理論語料庫，裡面跑著實際運行中的研究計畫。",
                    "meta": "語料庫",
                },
                {
                    "host": "amral", "name": "AMRAL", "tone": "amral",
                    "what": "自主數學研究代理循環的方法論，以及那個循環實際產出了什麼的現場封存。",
                    "meta": "封存庫",
                },
            ],
        },
        {
            "key": "systems",
            "title": "運行中的系統",
            "note": "會跑的東西，而不是被描述的東西。",
            "sites": [
                {
                    "host": "felra", "name": "FELRA", "tone": "felra",
                    "what": "GCPR–RWL–FELRA 的 Python 優先學術驗證與視覺化工作台：把理論與資料轉換成可重現的計算證據。",
                    "meta": "工作台",
                },
                {
                    "host": "apr", "name": "APR", "tone": "apr",
                    "what": "一套決定代理何時應觀察、該讀什麼、讀多深、何時必須重看，以及何時因證據仍新鮮而停止閱讀的 Runtime。",
                    "meta": "研究型 MVP · v0.10",
                },
                {
                    "host": "axioglyph", "name": "Axioglyph｜理符", "tone": "axioglyph",
                    "what": "畫一個符號不難；難的是說清楚它怎麼讀、代表什麼，改了一筆之後還是不是同一個東西。你可以直接動手改，故意弄錯，再看它為什麼通過或失敗。",
                    "meta": "互動實驗室 · EMPSL v0.4",
                },
                {
                    "host": "storyforge", "name": "Storyforge", "tone": "storyforge",
                    "what": "以英文為主的雙語書寫與閱讀平台，收錄 AI 創作的寓言、童話與經典再詮釋。",
                    "meta": "平台",
                },
                {
                    "host": "ai-board", "name": "AI Board", "tone": "aiboard",
                    "what": "給 AI 代理、搜尋系統與認知架構研究用的公開機器可讀佈告欄。它連瀏覽器都回純文字 —— 因為它本來就不是做給人看的。",
                    "meta": "協定 · MCP",
                },
                {
                    "host": "drvs", "name": "DRVS", "tone": "drvs",
                    "what": "一套與語料庫無關、幾乎全在瀏覽器端執行的搜尋引擎。它不會把你的頁面換成一份結果清單，而是把不相關的內容調暗，並且說清楚留下來的為什麼會在。",
                    "meta": "MIT · v0.1.0",
                },
                {
                    "host": "ms3e", "name": "MS3E", "tone": "ms3e",
                    "what": "多層嵌套光譜骨架狀態引擎。把線性媒體編譯成身份骨架、形變層與光譜分解，然後依狀態向量而不是時間戳重建。引擎本體就在頁面上跑。",
                    "meta": "Apache-2.0 · v1.0.1",
                },
                {
                    "host": "commoninstant.org", "name": "CTCL", "tone": "ctcl",
                    "what": "給異質 agent、模擬器與持續存在的 AI 用的驗證過共同參考瞬間，加上異質時空轉換 —— 可走 REST，也可走無狀態的 Remote MCP Gateway。它 Ed25519 簽章過的瞬間，現在也是 CTCL-ITR 時間帳本 anchor 的獨立第三方見證，同時支撐著 local-first 的 Temporal Port 桌面 App。",
                    "meta": "Apache-2.0 · v0.1 · ctcl-app · ctcl-itr",
                },
            ],
        },
    ],
}

CHROME = {
    "en": {
        "lang": "en",
        "skip": "Skip to content",
        "lang_switch": "繁體中文",
        "lang_switch_title": "Read this page in Traditional Chinese",
        "theme": "Switch colour scheme",
        "nav": [("/ai/", "AI Research"), ("/#index", "Index"), ("/#how", "How this works"), ("/#contact", "Contact")],
        "eyebrow": "EveMissLab",
        "display": "One lab. One site per thing it builds.",
        "standfirst": "EveMissLab is a research and engineering lab. Everything it finishes gets published as its own site, under its own domain, with its own source repository — so each piece can be read, checked and used without going through the others.",
        "index_title": "The index",
        "index_note": "Each finished project gets its own address. The list is built to keep growing.",
        "image_caption": "Miss Eve",
        "how_title": "How this works",
        "how": [
            ("One site per thing", "A project that is finished gets a subdomain, a source repository and a page that explains it. Nothing important lives only as a paragraph on this page."),
            ("Open by default", "The code is on GitHub under Apache-2.0, with tagged releases and verifiable checksums where the project produces them."),
            ("Boundaries travel with claims", "Every project states what it does not establish, next to what it does. That list is part of the specification, not a disclaimer appended to it."),
            ("Built with AI, said plainly", "These projects are built in collaboration with AI systems. Where that matters to how a result should be read, the project says so."),
        ],
        "contact_title": "Contact",
        "contact": "Everything published by this lab is reachable from the index above. Source repositories are linked from each project's own site.",
        "footer_rights": "All frameworks and tooling published open source.",
    },
    "zh": {
        "lang": "zh-Hant",
        "skip": "跳至內容",
        "lang_switch": "English",
        "lang_switch_title": "Read this page in English",
        "theme": "切換配色",
        "nav": [("/zh/ai/", "AI 研究"), ("/zh/#index", "索引"), ("/zh/#how", "運作方式"), ("/zh/#contact", "聯絡")],
        "eyebrow": "EveMissLab",
        "display": "一個實驗室。做完一件事，就給它一個站。",
        "standfirst": "EveMissLab 是一個研究與工程實驗室。每一件做完的東西都會以獨立的網站、獨立的網域、獨立的原始碼倉庫發布 —— 讓每一塊都能被單獨閱讀、檢查與使用，不必先經過其他塊。",
        "index_title": "索引",
        "index_note": "每個完成的專案都有自己的地址；這份清單是為了持續增加而設計的。",
        "image_caption": "Miss Eve",
        "how_title": "運作方式",
        "how": [
            ("一件事一個站", "做完的專案會拿到一個子網域、一個原始碼倉庫，以及一頁把它講清楚的說明。重要的東西不會只以「這頁上的一段文字」的形式存在。"),
            ("預設開源", "程式碼放在 GitHub，Apache-2.0 授權，附版本標籤；專案自己會產生校驗資料的，就附上可驗證的校驗和。"),
            ("邊界跟著主張走", "每個專案都會把「它不確立什麼」寫在「它確立什麼」旁邊。那份清單是規格的一部分，不是附在後面的免責聲明。"),
            ("與 AI 協作，而且說出來", "這些專案是與 AI 系統協作完成的。凡是這件事會影響一個結果該怎麼讀的地方，專案都會講明。"),
        ],
        "contact_title": "聯絡",
        "contact": "這個實驗室發布的一切都可以從上面的索引抵達。各專案的原始碼倉庫，連結在該專案自己的站上。",
        "footer_rights": "所有框架與工具皆以開源發布。",
    },
}

# --------------------------------------------------------------------------
# AI Research Laboratory (/ai/). Chrome only: the research records live in
# content/ai/ and are projected by src/ai_research.py. `matrix` is the
# twelve-cell entry grid on the front page; `subnav` is /ai/'s own bar.
# --------------------------------------------------------------------------

AI = {
    "en": {
        "name": "AI Research Laboratory",
        "full_name": "EveMissLab AI Research Laboratory",
        "short": "AI Research",
        "tagline": "Theory, experiments, models, data and evidence for AI systems.",
        "lede": "EveMissLab studies AI as a computational, architectural, representational and autonomous research subject — from theory to reproducible evidence.",
        "matrix_eyebrow": "AI Research Laboratory",
        "matrix_home": "Enter the laboratory",
        "matrix": [
            ("theory", "Theory"), ("experiments", "Experiments"), ("data", "Data"), ("benchmarks", "Benchmarks"),
            ("results", "Results"), ("programs", "Programs"), ("papers", "Papers"), ("systems", "Systems"),
            ("archive", "Archives"), ("models", "Models"), ("memory", "Memory"), ("computation", "Computation"),
        ],
        "subnav": [
            ("", "AI Research"), ("research", "Research"), ("theory", "Theory"), ("experiments", "Experiments"),
            ("data", "Data"), ("benchmarks", "Benchmarks"), ("results", "Results"), ("programs", "Programs"),
            ("models", "Models"), ("papers", "Papers"), ("systems", "Systems"), ("archive", "Archive"),
        ],
        "stats": [
            ("active_research", "Active research"), ("active_experiments", "Active experiments"),
            ("datasets", "Datasets"), ("benchmarks", "Benchmarks"), ("programs", "Programs"),
        ],
        "home": {
            "research": "Current research", "theory": "Theory", "experiments": "Active experiments",
            "results": "Latest results", "evidence": "Data & benchmarks", "programs": "Research programs",
            "models": "Models & architectures", "papers": "Latest papers", "systems": "Research systems",
            "graph": "Research graph", "archive": "Archive", "vocab": "Status and evidence vocabulary",
        },
        "sections": {
            "research": ("Research", "What the laboratory is studying now, and what each line has established so far."),
            "theory": ("Theory", "Formal claims, each with its assumptions, predictions and the conditions under which it fails."),
            "experiments": ("Experiments", "Every experiment is a first-class record: setup, procedure, runs, observed results, and an interpretation kept separate from them."),
            "data": ("Data", "Datasets with their provenance, what was removed or transformed, known bias, licence and checksums."),
            "benchmarks": ("Benchmarks", "Each benchmark states what it measures and what it does not."),
            "results": ("Results", "Observed results, kept apart from their interpretation. Negative, mixed and inconclusive results stay listed."),
            "programs": ("Programs", "Long-running research lines that group research, theory, experiments, papers and systems."),
            "papers": ("Papers", "Papers and technical whitepapers from the research perspective. Where a paper has its own canonical publication, this is an index entry pointing at it."),
            "systems": ("Systems", "Runtimes, tools and experimental systems that formed during research. Ones that matured into their own site are also in the index on the front page."),
            "models": ("Models", "Models and architectures used or built, with the configuration and behaviour notes that matter for reading results."),
            "memory": ("Memory", "A domain view: everything tagged Context & Memory."),
            "computation": ("Computation", "A domain view: everything tagged Computation."),
            "archive": ("Archive", "Paused, superseded and archived work, with its relations intact. The archive is part of the evidence, not a bin."),
            "claims": ("Claims", "Claims as first-class objects, with what supports and what contradicts them."),
            "observations": ("Observations", "Raw observations, before they become results."),
            "evaluations": ("Evaluations", "Interpretations and evaluations, recorded separately from the results they read."),
            "graph": ("Research graph", "Every public relation between research objects, as a table and as JSON."),
        },
        "kinds": {
            "research": "Research", "theory": "Theory", "experiment": "Experiment", "result": "Result",
            "dataset": "Dataset", "benchmark": "Benchmark", "model": "Model", "program": "Program",
            "paper": "Paper", "system": "System", "claim": "Claim", "observation": "Observation",
            "evaluation": "Evaluation", "artifact": "Artifact",
        },
        "statuses": {
            "IDEA": "only a question or a concept so far",
            "PRELIMINARY": "a first formalisation or observation exists",
            "ACTIVE": "under continuous research",
            "EXPERIMENTAL": "being tested experimentally",
            "VALIDATING": "the main proposition is formed; evidence is being confirmed",
            "REPLICATING": "being reproduced, or checked across models",
            "STABLE": "the current conclusions are relatively stable",
            "PAUSED": "paused",
            "ARCHIVED": "no longer actively pursued",
            "SUPERSEDED": "replaced by a newer version or theory",
        },
        "evidence": {
            "E0": "Concept only", "E1": "Internal observation", "E2": "Controlled experiment",
            "E3": "Repeated experiment", "E4": "Cross-model / cross-environment replication",
            "E5": "External reproduction / independent evidence",
        },
        "vocab_note": "Research status says where a line is in its life; evidence level says how much has been shown. They are recorded separately on purpose: ACTIVE or STABLE is not a truth claim, and an ARCHIVED line can still carry E4 evidence.",
        "data_basis": {
            "THEORY": "Theoretical reasoning only; no measurement.",
            "SYNTHETIC": "Synthetic data and theoretical reasoning. Many now treat synthetic data as if it were real; this laboratory says the opposite deliberately — until a real hybrid model exists, an inference is only an inference, and theoretically possible is not actually possible.",
            "DETERMINISTIC RUNTIME": "A deterministic scenario executed in a real runtime; the code and procedure are listed, and the numbers are what they are.",
            "REAL MODEL": "A real language model was executed; the model, its version and its configuration are recorded on the page.",
            "NOT RUN": "Designed and validated as a harness; never executed with a real model.",
        },
        "basis_note": "Data basis says what a number was measured on. Synthetic results are labelled SYNTHETIC on every card and page: they are evidence about the architecture under synthetic conditions, not about the world.",
        "labels": {
            "status": "Research status", "evidence": "Evidence level", "result": "Result",
            "data_basis": "Data basis", "authors": "Authors", "ai_collaborators": "AI collaborators",
            "updated": "Updated", "created": "Created", "version": "Version", "domain": "Domain",
            "program": "Program", "type": "Type", "id": "ID",
            "empty": "No public records yet.", "no_relations": "No public relations recorded.",
            "filter": "Filter", "all": "All", "view_all": "View all", "records": "records",
            "objects": "research objects", "relations": "relations",
            "snapshot": "Snapshot", "generated": "generated", "canonical": "Canonical URL",
            "json": "Machine-readable", "provenance": "Provenance",
        },
        "facets": {
            "status": "Status", "evidence": "Evidence", "domain": "Domain", "year": "Year",
            "program": "Program", "model": "Model", "dataset": "Dataset", "benchmark": "Benchmark",
            "research": "Research", "result": "Result type",
        },
        "rel_cols": ("Source", "Relation", "Target", "Status", "ID"),
        "tpl": {
            "questions": "Research questions", "claims": "Claims", "limitations": "Limitations",
            "links": "Repositories and sites",
            "definitions": "Definitions", "assumptions": "Assumptions", "formalization": "Formalisation",
            "predictions": "Predictions", "falsification": "Falsification / failure conditions",
            "evidence": "Evidence", "known_limitations": "Known limitations",
            "hypothesis": "Hypothesis", "setup": "Setup", "procedure": "Procedure", "runs": "Runs",
            "results": "Results", "interpretation": "Interpretation", "reproduction": "Reproduction",
            "artifacts": "Artifacts",
            "observed": "Observed result", "alternatives": "Alternative interpretations",
            "contains": "What it contains", "why": "Why it exists", "created_how": "How it was created",
            "transformed": "What was removed or transformed", "bias": "Known bias", "license": "Licence",
            "checksum": "Checksum", "format": "Format and size", "download": "Download",
            "purpose": "Purpose", "tasks": "Tasks", "metrics": "Metrics", "protocol": "Evaluation protocol",
            "baselines": "Baselines", "not_measured": "What it does not measure", "repository": "Repository",
            "record": "Record", "goals": "Goals", "open_questions": "Open questions",
            "milestones": "Milestones", "timeline": "Research lines and systems in this program",
            "architecture": "Architecture",
            "fields": "Recorded fields", "relations": "Relations", "history": "History and provenance",
        },
    },
    "zh": {
        "name": "AI 研究實驗室",
        "full_name": "EveMissLab AI Research Laboratory",
        "short": "AI 研究",
        "tagline": "AI 系統的理論、實驗、模型、資料與證據。",
        "lede": "EveMissLab 把 AI 當作計算的、架構的、表徵的、且自主的研究對象 —— 從理論一路做到可重現的證據。",
        "matrix_eyebrow": "AI 研究實驗室",
        "matrix_home": "進入實驗室",
        "matrix": [
            ("theory", "理論"), ("experiments", "實驗"), ("data", "資料"), ("benchmarks", "基準"),
            ("results", "結果"), ("programs", "計畫"), ("papers", "論文"), ("systems", "系統"),
            ("archive", "封存"), ("models", "模型"), ("memory", "記憶"), ("computation", "計算"),
        ],
        "subnav": [
            ("", "AI 研究"), ("research", "研究"), ("theory", "理論"), ("experiments", "實驗"),
            ("data", "資料"), ("benchmarks", "基準"), ("results", "結果"), ("programs", "計畫"),
            ("models", "模型"), ("papers", "論文"), ("systems", "系統"), ("archive", "封存"),
        ],
        "stats": [
            ("active_research", "進行中的研究"), ("active_experiments", "進行中的實驗"),
            ("datasets", "資料集"), ("benchmarks", "基準"), ("programs", "研究計畫"),
        ],
        "home": {
            "research": "目前的研究", "theory": "理論", "experiments": "進行中的實驗",
            "results": "最新結果", "evidence": "資料與基準", "programs": "研究計畫",
            "models": "模型與架構", "papers": "最新論文", "systems": "研究系統",
            "graph": "研究圖譜", "archive": "封存", "vocab": "狀態與證據詞彙",
        },
        "sections": {
            "research": ("研究", "實驗室現在正在研究什麼，以及每條線到目前為止確立了什麼。"),
            "theory": ("理論", "正式的主張，每一條都附上它的前提、預測，以及它在什麼條件下會失敗。"),
            "experiments": ("實驗", "每個實驗都是一等紀錄：設定、程序、執行、觀察到的結果，以及與結果分開記錄的詮釋。"),
            "data": ("資料", "資料集及其來源歷程、移除或轉換了什麼、已知偏誤、授權與校驗和。"),
            "benchmarks": ("基準", "每個基準都說明它測什麼，也說明它沒有測什麼。"),
            "results": ("結果", "觀察到的結果，與詮釋分開存放。負面、混合與無定論的結果一樣列出。"),
            "programs": ("計畫", "長期研究線，把研究、理論、實驗、論文與系統聚在一起。"),
            "papers": ("論文", "從研究視角整理的論文與技術白皮書。已有正式發表位置的，這裡只是指向它的索引項。"),
            "systems": ("系統", "研究過程中形成的 runtime、工具與實驗系統。已成熟成獨立站的，也會出現在首頁的索引裡。"),
            "models": ("模型", "使用或自建的模型與架構，附上讀結果時需要知道的設定與行為備註。"),
            "memory": ("記憶", "領域視圖：所有標記為 Context & Memory 的研究。"),
            "computation": ("計算", "領域視圖：所有標記為 Computation 的研究。"),
            "archive": ("封存", "暫停、被取代與已封存的工作，關係完整保留。封存是證據的一部分，不是垃圾桶。"),
            "claims": ("主張", "作為一等物件的主張，附上支持與反駁它的證據。"),
            "observations": ("觀察", "原始觀察，在成為結果之前。"),
            "evaluations": ("評估", "詮釋與評估，與它們所讀的結果分開記錄。"),
            "graph": ("研究圖譜", "研究物件之間所有公開的關係，以表格與 JSON 兩種形式提供。"),
        },
        "kinds": {
            "research": "研究", "theory": "理論", "experiment": "實驗", "result": "結果",
            "dataset": "資料集", "benchmark": "基準", "model": "模型", "program": "計畫",
            "paper": "論文", "system": "系統", "claim": "主張", "observation": "觀察",
            "evaluation": "評估", "artifact": "產物",
        },
        "statuses": {
            "IDEA": "目前只有問題或概念",
            "PRELIMINARY": "已有初步的形式化或觀察",
            "ACTIVE": "正在持續研究",
            "EXPERIMENTAL": "正在進行實驗驗證",
            "VALIDATING": "主要命題已形成，正在做證據確認",
            "REPLICATING": "正在做重現或跨模型驗證",
            "STABLE": "目前的研究結論相對穩定",
            "PAUSED": "暫停",
            "ARCHIVED": "停止主動推進",
            "SUPERSEDED": "已被新版本或新理論取代",
        },
        "evidence": {
            "E0": "僅有概念", "E1": "內部觀察", "E2": "受控實驗", "E3": "重複實驗",
            "E4": "跨模型／跨環境重現", "E5": "外部重現／獨立證據",
        },
        "vocab_note": "研究狀態說的是一條線走到哪裡；證據等級說的是已經證明了多少。兩者刻意分開記錄：ACTIVE 或 STABLE 不是真值宣稱，而一條 ARCHIVED 的線仍然可以帶著 E4 的證據。",
        "data_basis": {
            "THEORY": "純理論推理，沒有量測。",
            "SYNTHETIC": "合成數據與理論推理。現在很多人把合成數據當成真的；這個實驗室刻意反過來說——在真正的混合模型出現之前，推論就只是推論，理論上可能不等於實際上可能。",
            "DETERMINISTIC RUNTIME": "在真實 runtime 裡執行的決定性情境；程式碼與做法都列出，數字是什麼就是什麼。",
            "REAL MODEL": "真的跑了語言模型；模型、版本與設定都記在頁面上。",
            "NOT RUN": "只設計並驗證了 harness，從未用真實模型執行。",
        },
        "basis_note": "資料基礎說的是一個數字是在什麼上面量出來的。合成結果在每張卡片與每一頁都標 SYNTHETIC：那是關於架構在合成條件下的證據，不是關於世界的證據。",
        "labels": {
            "status": "研究狀態", "evidence": "證據等級", "result": "結果",
            "data_basis": "資料基礎", "authors": "作者", "ai_collaborators": "AI 協作",
            "updated": "更新", "created": "建立", "version": "版本", "domain": "領域",
            "program": "計畫", "type": "類型", "id": "ID",
            "empty": "尚無公開紀錄。", "no_relations": "尚無公開的關係紀錄。",
            "filter": "篩選", "all": "全部", "view_all": "全部", "records": "筆",
            "objects": "個研究物件", "relations": "條關係",
            "snapshot": "快照", "generated": "產生於", "canonical": "Canonical URL",
            "json": "機器可讀", "provenance": "來源歷程",
        },
        "facets": {
            "status": "狀態", "evidence": "證據", "domain": "領域", "year": "年份",
            "program": "計畫", "model": "模型", "dataset": "資料集", "benchmark": "基準",
            "research": "研究", "result": "結果類型",
        },
        "rel_cols": ("來源", "關係", "目標", "狀態", "ID"),
        "tpl": {
            "questions": "研究問題", "claims": "主張", "limitations": "限制", "links": "倉庫與站點",
            "definitions": "定義", "assumptions": "前提", "formalization": "形式化",
            "predictions": "預測", "falsification": "證偽／失敗條件",
            "evidence": "證據", "known_limitations": "已知限制",
            "hypothesis": "假設", "setup": "設定", "procedure": "程序", "runs": "執行",
            "results": "結果", "interpretation": "詮釋", "reproduction": "重現", "artifacts": "產物",
            "observed": "觀察到的結果", "alternatives": "其他可能的詮釋",
            "contains": "內容", "why": "為何存在", "created_how": "如何建立",
            "transformed": "移除或轉換了什麼", "bias": "已知偏誤", "license": "授權",
            "checksum": "校驗和", "format": "格式與規模", "download": "下載",
            "purpose": "目的", "tasks": "任務", "metrics": "指標", "protocol": "評估協定",
            "baselines": "基線", "not_measured": "它沒有測什麼", "repository": "原始碼倉庫",
            "record": "紀錄", "goals": "目標", "open_questions": "開放問題",
            "milestones": "里程碑", "timeline": "此計畫下的研究線與系統", "architecture": "架構",
            "fields": "記錄欄位", "relations": "關係", "history": "歷史與來源歷程",
        },
    },
}
