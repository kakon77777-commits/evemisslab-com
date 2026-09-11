# The ten series papers, the canonical index, and their artifacts. Every paper's
# SHA-256 is read from the series' canonical manifest (inside the canonical
# package zip) and from the per-paper manifest inside each paper zip, and both
# are asserted against the bytes on disk — in the paper zip and in the canonical
# package — never transcribed by hand.
import hashlib

from ipm_common import L, obj, rel, artifact

PKG = "IPM_v0.1_Canonical_Series_Package.zip"
CANON = L.zip_json(PKG, "IPM_v0.1_Canonical_Manifest.json")
assert CANON["series_id"] == "EML-IPM" and CANON["all_papers_verified"] and len(CANON["papers"]) == 10, CANON.get("status")
INDEX_MD = CANON["canonical_index"]["file"]
assert hashlib.sha256(L.zip_member(PKG, INDEX_MD)).hexdigest() == CANON["canonical_index"]["sha256"]
D = CANON["date"]  # 2026-09-02

# (n, paper zip, english title, research line, theory it formalizes, domain, tags)
SERIES = [
    (1, "IPM_01_一輪到底是一輪什麼_v0.1.zip", "What is a 'single turn', really? User turns, hidden loops, and the redefinition of single-pass intelligence", "RES-2026-0101", "THY-2026-0101", "Computation"),
    (2, "IPM_02_智能到底算了一次什麼_v0.1.zip", "What does intelligence compute once? A candidate theory of the minimum intelligent semantic execution unit", "RES-2026-0101", "THY-2026-0102", "Cognitive Science"),
    (3, "IPM_03_從認知到神經元_v0.1.zip", "From cognition to neurons: how human intelligence is measured across levels", "RES-2026-0101", "THY-2026-0103", "Cognitive Science"),
    (4, "IPM_04_從神經元到焦耳_v0.1.zip", "From neurons to joules: energy, thermodynamics, and physical lower bounds of intelligent computation", "RES-2026-0101", "THY-2026-0104", "Computation"),
    (5, "IPM_05_計算不是只有FLOPs_v0.1.zip", "Computation is more than FLOPs: memory, interconnect, hardware occupancy, and computational spacetime volume", "RES-2026-0101", "THY-2026-0105", "Computation"),
    (6, "IPM_06_成果品質到底怎麼量_v0.1.zip", "How should output quality be measured? From formal correctness to structured intelligence quality", "RES-2026-0102", "THY-2026-0106", "Evaluation"),
    (7, "IPM_07_不要叫人類替自己的感覺打分數_v0.1.zip", "Do not ask humans to numerically score their own feelings: IBQF binary measurement and low-burden quality evaluation", "RES-2026-0102", "THY-2026-0107", "Cognitive Science"),
    (8, "IPM_08_自然語言圖像與創意如何被量_v0.1.zip", "How can natural language, images, and creative outputs be measured? A structured quality space for high-ambiguity artifacts", "RES-2026-0102", "THY-2026-0108", "Evaluation"),
    (9, "IPM_09_拿掉LOOP還剩多少智能_v0.1.zip", "How much intelligence remains without the loop? Single-pass capability, scaffolding dependence, and hidden computational cost", "RES-2026-0103", "THY-2026-0109", "Evaluation"),
    (10, "IPM_10_一個答案值多少物理世界_v0.1.zip", "How much physical world does an answer cost? A unified metrology framework for intelligence yield", "RES-2026-0103", "THY-2026-0110", "Evaluation"),
]

SUMMARY = {
    1: ("Separates the chat-interface turn from model invocation, generation trajectory, agent loop and physical computation; defines externally loopless intelligence, a five-kind loop taxonomy and the single-pass condition U=1, G=1, R=1, L=0, S=0; introduces the event vector (Q, U, G, I, L, R, S, T, E, V_CST) and twelve invariants, starting with 'interaction compression ≠ computation compression'.",
        "把聊天介面的一輪從模型呼叫、生成軌跡、agent 迴圈與物理計算中分離；定義外部無迴圈智能、五類 LOOP 分類與 single-pass 條件 U=1、G=1、R=1、L=0、S=0；引入事件向量 (Q, U, G, I, L, R, S, T, E, V_CST) 與十二個不變式，第一條是「互動壓縮 ≠ 計算壓縮」。"),
    2: ("Argues that token, FLOP, neuron activation, layer and 'thought' all fail as units of intelligent work and proposes μI, a resolution-relative semantic state transition with seven conditions, four candidate families, gross/effective counts, a semantic work vector and a cross-level map down to physical trace; explicitly a candidate ontology with no MVP.",
        "論證 token、FLOP、neuron activation、layer 與「想法」都不能當智能工作單位，提出 μI——相對於解析度的語意狀態轉換，帶七個條件、四個候選族、gross／effective 計數、語意工作向量與向下到物理軌跡的跨層映射；明言是候選本體、無 MVP。"),
    3: ("Reads cognitive science and neuroscience for method rather than numbers: Marr's levels extended to five, resource-rational operation costs, diffusion-model latent inference, encoding–decoding duality, population coding, causal perturbation, the 10 bits/s throughput lesson; yields cross-level triangulation and a D–A+ measurement grade for μI.",
        "向認知科學與神經科學借方法而非數字：Marr 三層擴成五層、resource-rational 的操作成本、擴散模型的潛變量推斷、編碼—解碼對偶、群體編碼、因果擾動、10 bits/s 的教訓；得出跨層三角化與 μI 的 D–A+ 測量等級。"),
    4: ("Builds the energy account bottom-up the way neural energetics does (ion flux → ATP → joule), shows that a spike — and therefore a token or a μI — has no fixed energy, types energy as gross/baseline/marginal/attributed with a declared boundary, and keeps Landauer's kT ln 2 as a bound on erasure rather than the price of reasoning.",
        "照神經能量學的方式由下而上建能量帳（離子流 → ATP → 焦耳），說明一個 spike——因此一個 token 或一個 μI——沒有固定能量，把能量分型為 gross／baseline／marginal／attributed 並宣告邊界，Landauer 的 kT ln 2 只是抹除的下界而不是推理的價格。"),
    5: ("Replaces FLOPs with a physical cost vector (typed ops, memory traffic by hierarchy, I/O, interconnect, residency, occupancy, time, energy), defines computational spacetime as a vector-first measure V_CST = ∫ R(t) dt with its own topology and peak footprint, and fixes CST measurement grades and boundaries; roofline and memory-wall results are the engineering backbone.",
        "以物理成本向量（分型運算、按層級的記憶體流量、I/O、互連、駐留、占用、時間、能量）取代 FLOPs，把計算時空定義為向量優先的測度 V_CST = ∫ R(t) dt，附拓撲與峰值占用，並固定 CST 測量等級與邊界；roofline 與 memory wall 是工程骨幹。"),
    6: ("Makes quality a relation Q(Y | task, spec, environment, boundary) measured as a structured vector in three layers (formal, structured, human residual) with hard gates, coverage split three ways, mutation-tested test strength, the specification–verification separation and a quality evidence ladder E–A+; efficiency is kept out of quality unless the specification puts it in.",
        "把品質變成關係 Q(Y | 任務、規格、環境、邊界)，以三層（形式化、結構化、人類殘餘）結構化向量量測，附 hard gate、三向覆蓋率、mutation 測出的測試強度、規格—驗證分離與 E–A+ 品質證據階梯；效率不進品質，除非規格把它放進去。"),
    7: ("Brings EveMissLab's IBQF/FDCS micro-binary idea into IPM as Binary Residual Quality Measurement: humans answer local yes/no or A/B items, Bradley–Terry / IRT-type models reconstruct a latent multidimensional quality, items are chosen adaptively by information gain per human cost, and rater disagreement is kept as structure; the low-burden advantage is stated as a testable hypothesis.",
        "把 EveMissLab 的 IBQF／FDCS 微觀二元想法帶進 IPM，成為二元殘餘品質測量：人只回答局部的是／否或 A／B，Bradley–Terry／IRT 類模型重建潛在多維品質，依每單位人類成本的資訊增益自適應選題，評審分歧當結構保留；低負擔優勢被寫成可檢驗的假說。"),
    8: ("Defines the typed quality space Q[domain, task, context, audience] = core ⊕ domain ⊕ task with construct graphs, the itemization pipeline construct → indicator → item → observation → latent estimate, a construct-validity gate, an open but versioned ontology, multimodal coupling dimensions and the rule that novelty is not creativity; every metric is one projection.",
        "定義有型別的品質空間 Q[領域、任務、情境、受眾] = core ⊕ domain ⊕ task，附構念圖、條目化管線 構念 → 指標 → 題目 → 觀測 → 潛在估計、構念效度閘、開放但有版本的本體、多模態耦合維度，以及「新穎不是創造力」的規則；每個指標都只是一個投影。"),
    9: ("Writes a system as (model, scaffolding vector), defines scaffolding gain, survival ratio SSR, dependence ratio SDR, scaffold cost multiplier SCM and marginal yields along the ablation ladder A0–A5, adds interaction graphs and Shapley-style attribution, hidden-retry and discarded-work accounting, a capability vector and S-grades; loop is not cheating, hiding its cost is.",
        "把系統寫成（模型，鷹架向量），定義鷹架增益、存活率 SSR、依賴率 SDR、鷹架成本倍率 SCM 與消融階梯 A0–A5 上的邊際產率，加上交互作用圖與 Shapley 式歸因、隱藏重試與丟棄工作的會計、能力向量與 S 等級；LOOP 不是作弊，藏成本才是。"),
    10: ("Packs the four measurement objects into the canonical intelligence event, defines the intelligence yield vector and two-stage efficiency, sets Pareto comparison and the no-premature-scalarization principle, names four capability archetypes, fixes the IPM Minimum Reporting Standard v0.1 and restates the five falsifiable claims; IPM is a metrology candidate, not a discovered constant.",
         "把四個測量物件封裝成 canonical intelligence event，定義智能產率向量與兩段效率，訂下 Pareto 比較與不過早純量化原則，命名四種能力原型，固定 IPM 最低報告標準 v0.1 並重述五個可證偽命題；IPM 是計量學候選框架，不是被發現的常數。"),
}

# artifact for the canonical package first, so it sits at ART-2026-0101
PKG_ART = artifact(PKG, kind="canonical-series-package", label="EML-IPM v0.1 canonical series package — 10 papers + canonical index + SHA-256 manifest (UTF-8 Markdown)")
rel("PRG-2026-0101", "released_as", PKG_ART)

by_n = {int(p["paper"]): p for p in CANON["papers"]}
for n, zname, title, line, theory, domain in SERIES:
    entry = by_n[n]
    md = entry["file"]
    per = L.zip_json(zname, f"IPM_{n:02d}_manifest.json")
    assert per["series_id"] == "EML-IPM" and per["paper"] == f"{n:02d}/10" and per["version"] == "v0.1", per
    got_zip = hashlib.sha256(L.zip_member(zname, md)).hexdigest()
    got_pkg = hashlib.sha256(L.zip_member(PKG, md)).hexdigest()
    assert got_zip == entry["expected_sha256"] == per["sha256"], f"paper {n}: zip {got_zip} manifest {entry['expected_sha256']} per-paper {per['sha256']}"
    assert got_pkg == got_zip, f"paper {n}: canonical package copy differs from the paper zip"
    aid = artifact(zname, kind="canonical-source-package", label=f"EML-IPM Paper {n:02d} — canonical UTF-8 Markdown + manifest (zip)")
    pid = f"PAP-2026-{100 + n:04d}"
    obj(pid, "paper", f"Paper {n:02d} — {title}", entry["title"], SUMMARY[n][0], SUMMARY[n][1],
        "STABLE", "E0", created=D, updated=L.mtime(zname), domain=domain,
        eml_publication_type="series paper (Intelligence Physical Metrology series, 10 papers); 公開純理論論文, 無 MVP",
        eml_data_basis="THEORY", eml_date=D, eml_doi_or_external_id=f"EML-IPM-{n:02d}",
        eml_source_artifact=f"{zname}!/{md}", eml_checksums={"paper .md sha256": got_zip},
        eml_tags=["zh-TW", "canonical UTF-8 Markdown", f"paper {n}/10", f"role: {entry['role']}"])
    rel(pid, "reports", line)
    rel(pid, "formalizes", theory)
    rel(pid, "packaged_as", aid)
    rel(pid, "packaged_as", PKG_ART)

# the canonical index: series overview, unified notation, v0.2 experimental entry point
obj("PAP-2026-0111", "paper",
    "IPM v0.1 canonical index — series overview, unified notation and the v0.2 experimental entry point",
    "IPM v0.1 Canonical Index：智能物理計量學系列總論、統一符號表與 v0.2 實驗入口",
    "The series' entry point: the canonical intelligence event, the dependency graph of the ten papers in three lines, a unified symbol table (turn/execution, semantic work, cross-level realization, energy, physical computation, computational spacetime and topology, quality, IBQF/BRQM, scaffolding, yield), the no-premature-scalarization principle, Pareto comparison, the 36-field minimum reporting standard, the ten-step comparison protocol, the series' core invariants, the five falsifiable propositions F1–F5, the v0.2 experiments A–E with the recommended order A → D → B → C → E, a minimal run schema and the versioning rule.",
    "系列入口：canonical intelligence event、十篇論文分三條線的依賴圖、統一符號表（回合／執行、語意工作、跨層實現、能量、物理計算、計算時空與拓撲、品質、IBQF／BRQM、鷹架、產率）、不過早純量化原則、Pareto 比較、36 欄最低報告標準、十步比較協定、系列核心不變式、五個可證偽命題 F1–F5、v0.2 實驗 A–E 與建議順序 A → D → B → C → E、最小 run schema 與版本規則。",
    "STABLE", "E0", created=D, updated=L.mtime(PKG), domain="Evaluation",
    eml_publication_type="canonical series index (theory series entry point)", eml_data_basis="THEORY", eml_date=D,
    eml_doi_or_external_id="EML-IPM v0.1 Canonical Index", eml_source_artifact=f"{PKG}!/{INDEX_MD}",
    eml_checksums={"index .md sha256": CANON["canonical_index"]["sha256"]},
    eml_tags=["zh-TW", "canonical UTF-8 Markdown", "unified notation", "v0.2 experimental entry point"])
for line in ("RES-2026-0101", "RES-2026-0102", "RES-2026-0103"):
    rel("PAP-2026-0111", "reports", line)
rel("PAP-2026-0111", "formalizes", "THY-2026-0110")
for c in ("CLM-2026-0101", "CLM-2026-0102", "CLM-2026-0103", "CLM-2026-0104", "CLM-2026-0105"):
    rel("PAP-2026-0111", "formalizes", c)
    rel("PAP-2026-0110", "formalizes", c)
rel("PAP-2026-0111", "packaged_as", PKG_ART)
