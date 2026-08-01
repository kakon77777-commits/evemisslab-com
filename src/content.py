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
                    "what": "A lossless archive format an AI can plan and a deterministic, model-independent decoder must restore exactly. Two reference implementations, cross-verified byte for byte.",
                    "meta": "Apache-2.0 · v0.1.0 · 1.0 draft",
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
                    "host": "logic", "name": "Logic Matrix", "tone": "logic",
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
                    "what": "一種可由 AI 規劃、但必須由確定性且不依賴模型的解碼器精確還原的無損封裝格式。兩套參考實作，逐位元互相驗證。",
                    "meta": "Apache-2.0 · v0.1.0 · 1.0 草案",
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
                    "host": "logic", "name": "Logic Matrix", "tone": "logic",
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
        "nav": [("#index", "Index"), ("#how", "How this works"), ("#contact", "Contact")],
        "eyebrow": "EveMissLab",
        "display": "One lab. One site per thing it builds.",
        "standfirst": "EveMissLab is a research and engineering lab. Everything it finishes gets published as its own site, under its own domain, with its own source repository — so each piece can be read, checked and used without going through the others.",
        "index_title": "The index",
        "index_note": "Eight sites live today. The list is built to keep growing.",
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
        "nav": [("#index", "索引"), ("#how", "運作方式"), ("#contact", "聯絡")],
        "eyebrow": "EveMissLab",
        "display": "一個實驗室。做完一件事，就給它一個站。",
        "standfirst": "EveMissLab 是一個研究與工程實驗室。每一件做完的東西都會以獨立的網站、獨立的網域、獨立的原始碼倉庫發布 —— 讓每一塊都能被單獨閱讀、檢查與使用，不必先經過其他塊。",
        "index_title": "索引",
        "index_note": "目前八個站在線上。這份清單是為了持續增加而設計的。",
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
