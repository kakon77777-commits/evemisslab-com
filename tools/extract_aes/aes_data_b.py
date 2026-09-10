# Papers, systems, benchmarks, datasets, models — and their artifacts.
# Paper digests are parsed from the series' own manifest and asserted against
# the bytes on disk, never transcribed by hand.
import hashlib
import re

from aes_common import obj, rel, artifact, mtime, read_text, zip_member, ARTIFACTS

MANIFEST = read_text("Adaptive_Epistemic_Systems_Series_COMPLETE_MANIFEST.md")
MANIFEST_SHA = {int(n): sha for n, sha in re.findall(r"## Paper (\d+)\n- File: `[^`]+`\n- SHA-256: `([0-9a-f]+)`", MANIFEST)}
assert len(MANIFEST_SHA) == 11, MANIFEST_SHA

WP_ZIP = "Adaptive_Epistemic_AI_Runtime_v0.1_Technical_Whitepaper_Source_Package.zip"
WP_DIR = "Adaptive_Epistemic_AI_Technical_Whitepaper_v0.1/"
WP_MANIFEST_SHA = re.search(r"Adaptive_Epistemic_AI_Runtime_Technical_Whitepaper_v0\.1\.md` — `([0-9a-f]{64})`",
                            zip_member(WP_ZIP, WP_DIR + "MANIFEST.md").decode("utf-8")).group(1)
assert hashlib.sha256(zip_member(WP_ZIP, WP_DIR + "Adaptive_Epistemic_AI_Runtime_Technical_Whitepaper_v0.1.md")).hexdigest() == WP_MANIFEST_SHA

SERIES = [  # (n, file, english title, zh title, theories it formalizes)
    (1, "Adaptive_Epistemic_Systems_Series_Paper_01_Asymmetric_Spacetime_Tension_v0.1.md",
     "Dynamic knowledge graphs under asymmetric spacetime tension", "非對稱時空張力下的動態知識圖——自適應世界狀態系統的第一原理框架", ["THY-2026-0001"]),
    (2, "Adaptive_Epistemic_Systems_Series_Paper_02_Freshness_Decay_Update_Tension_v0.1.md",
     "Stability is not a static value: freshness, decay and update tension", "穩定性不是靜態值——知識新鮮度、衰減率與更新張力的動態模型", ["THY-2026-0001"]),
    (3, "Adaptive_Epistemic_Systems_Series_Paper_03_Executable_Symbolic_State_and_Rendering_v0.1.md",
     "From dynamic graph to executable symbolic system: language as rendering, not canonical state", "從動態圖到可執行符號系統——自然語言作為世界狀態的 Rendering，而非 Canonical State", ["THY-2026-0002"]),
    (4, "Adaptive_Epistemic_Systems_Series_Paper_04_Adaptive_Representation_Space_v0.1.md",
     "World-knowledge expansion and the adaptive representation space", "世界知識擴張與自適應表示空間——從節點數量增長到有效結構化資訊的能力擴張", []),
    (5, "Adaptive_Epistemic_Systems_Series_Paper_05_Memory_Algorithms_and_Reusable_Solution_Paths_v0.1.md",
     "Memory, algorithm libraries and reusable solution paths", "記憶、算法庫與可重用問題求解路徑——從世界模型到能力模型的累積式智能架構", ["THY-2026-0007"]),
    (6, "Adaptive_Epistemic_Systems_Series_Paper_06_Substrate_Neutral_Computational_Containers_v0.1.md",
     "Substrate-neutral computational containers", "載體中立的計算容器理論——從算法選擇到異質計算載體聯合調度", ["THY-2026-0007"]),
    (7, "Adaptive_Epistemic_Systems_Series_Paper_07_Blind_Derivation_and_AI_Architecture_Convergence_v0.1.md",
     "Blind-derived AI: do different first principles converge on one engineering form?", "盲推導 AI——不同第一原理是否收斂到同一工程形態？", ["THY-2026-0003"]),
    (8, "Adaptive_Epistemic_Systems_Series_Paper_08_Intelligent_Architecture_Attractors_v0.1.md",
     "Intelligent architecture attractors: at which level does difference live?", "智能架構吸引子——差異究竟存在於哪一層？", ["THY-2026-0003"]),
    (9, "Adaptive_Epistemic_Systems_Series_Paper_09_Probability_Is_Not_Bayesian_v0.1.md",
     "Probability is not Bayesian", "概率不等於貝葉斯——從隨機系統、概率模型到 Bayesian 更新的認識論邊界", ["THY-2026-0004"]),
    (10, "Adaptive_Epistemic_Systems_Series_Paper_10_Bayes_Within_Bayes_Meta_Epistemic_Justification_v0.1.md",
     "Bayes within Bayes: who authorizes the update rule?", "貝葉斯中的貝葉斯——誰授權更新規則？從 Prior、Likelihood 到 Meta-Epistemology 的遞歸問題", ["THY-2026-0004"]),
    (11, "Adaptive_Epistemic_Systems_Series_Paper_11_Final_Experimental_Verdict_v0.1.md",
     "If it is really stronger, I was wrong; if not, what did we find? The final experimental verdict", "如果它真的更強，我錯了；如果沒有，我們又發現了什麼？——自適應認識系統的最終實驗判決與可證偽收束", ["THY-2026-0003"]),
]

SUMMARY = {
    1: ("Lifts asymmetry from edge weight to effective time scale: nodes carry stability, decay, tension, impact and local valid time, so refresh is triggered locally instead of by one global clock.",
        "把非對稱性從邊權重提升到有效時間尺度：節點帶有穩定性、衰減、張力、影響度與局部有效時間，刷新由局部觸發而非單一全域時鐘。"),
    2: ("Freshness is decided by world change rate, source reliability, dependency structure, task risk and system impact — with risk-weighted tension, update debt, revalidation radius and event-triggered wake-up.",
        "新鮮度由世界變化速率、來源可靠性、依賴結構、任務風險與系統影響共同決定——含風險加權張力、更新債務、重驗證半徑與事件觸發喚醒。"),
    3: ("Four layers (world state, canonical symbols, executable operations, rendering); natural language is parsed into canonical state and rendered back out, never used as the state itself.",
        "四層結構（世界狀態、canonical 符號、可執行操作、rendering）；自然語言被解析進 canonical state 再 render 出來，永遠不直接當狀態本身。"),
    4: ("Effective structured information, not node count, measures capability growth; split/merge/delete/abstract/bridge keep the representation space adaptive.",
        "以有效結構化資訊而非節點數量衡量能力增長；split／merge／delete／abstract／bridge 讓表示空間持續可重構。"),
    5: ("Algorithms, tools, contracts, costs and outcome history become capability nodes; Reuse ≻ Adapt ≻ Create.",
        "算法、工具、契約、成本與成敗歷史成為能力節點；Reuse ≻ Adapt ≻ Create。"),
    6: ("Any execution environment with representable input, valid transition and readable output is a compute container; algorithms and containers are scheduled jointly.",
        "任何具可表示輸入、有效轉換與可讀輸出的執行環境都是計算容器；算法與容器聯合調度。"),
    7: ("Treats the first six papers as a blind-derivation experiment and proposes a protocol and five levels of similarity for comparing the result with modern AI.",
        "把前六篇視為一次盲推導實驗，提出比較協定與五種相似性層級，用來對照現代 AI。"),
    8: ("Six levels of architectural difference, architecture equivalence classes and attractor basins; the executed architecture is the architecture.",
        "六個架構差異層級、架構等價類與吸引域；被執行的架構才是架構。"),
    9: ("A layered vocabulary from stochastic to generalized Bayesian and a Bayesian authenticity test for updates that are only redescribed as Bayesian.",
        "從 stochastic 到 generalized Bayesian 的分層詞彙，以及檢查「事後被說成 Bayesian」的 Bayesian authenticity test。"),
    10: ("Prior, likelihood and hypothesis space need an authorization Bayes' rule cannot give; meta-epistemic configuration becomes part of the architecture.",
         "Prior、likelihood 與假設空間需要一個 Bayes 公式給不出的授權；meta-epistemic configuration 成為架構的一部分。"),
    11: ("Fixes the verdict map before the runtime exists — Distinct Advantage, Operational Convergence, Behavioral Equivalence Only, Inconclusive, Architecture Worse — with fidelity gates, ablation, equivalence testing and the rule that if every outcome confirms, nothing was explained.",
         "在 runtime 存在之前就固定判決表——Distinct Advantage、Operational Convergence、Behavioral Equivalence Only、Inconclusive、Architecture Worse——附 fidelity gate、消融、等價檢驗，以及「若每種結果都算確認，就什麼都沒解釋」的規則。"),
}

for n, fname, title, title_zh, theories in SERIES:
    pid = f"PAP-2026-{n:04d}"
    aid = artifact(fname, kind="canonical-source", label=f"Adaptive Epistemic Systems Series — Paper {n:02d} (UTF-8 Markdown)")
    got = next(a for a in ARTIFACTS if a["id"] == aid)["values"]["eml_artifact_sha256"]
    assert got == MANIFEST_SHA[n], f"paper {n}: sha256 on disk {got} != series manifest {MANIFEST_SHA[n]}"
    obj(pid, "paper", f"Paper {n:02d} — {title}", title_zh, SUMMARY[n][0], SUMMARY[n][1],
        "STABLE", "E1" if n == 7 else "E0", created=mtime(fname),
        domain="AI Architecture" if n in (1, 2, 3, 4, 7, 8, 11) else ("Computation" if n in (5, 6) else "Formal AI"),
        eml_publication_type="series paper (Adaptive Epistemic Systems Series, 11 papers)", eml_data_basis="THEORY",
        eml_authors=["Neo.K (EveMissLab)"], eml_date=mtime(fname),
        eml_source_artifact=fname, eml_checksums={"sha256": MANIFEST_SHA[n]},
        eml_tags=["zh-TW", "canonical UTF-8 Markdown", f"paper {n}/11"])
    rel(pid, "reports", "RES-2026-0001")
    for t in theories:
        rel(pid, "formalizes", t)
    rel(pid, "packaged_as", aid)

PACC_MD = "PACC_Probability_Appearance_Convergence_Conjecture_v0.1_2026-09-08.md"
aid = artifact(PACC_MD, kind="canonical-source", label="PACC conjecture paper v0.1 (UTF-8 Markdown)")
obj("PAP-2026-0012", "paper", "The Probabilistic Appearance Convergence Conjecture (PACC)",
    "概率表象收斂猜想——非概率式智能計算是否會在有限決策約束下收斂至概率型 AI？",
    "Proposition paper: a system that does not take probability as a first-level primitive may, under finite information, competing candidates, resource limits, repeated update and forced choice, converge to forms that a probability model maps with low complexity. Distinguishes behavioural, representational, dynamical and attractor equivalence, and pre-registers the experiments' falsification conditions.",
    "命題論文：不以概率為第一級 primitive 的系統，在有限資訊、多候選競爭、資源約束、動態更新與必須選擇的條件下，可能收斂到概率模型能以低複雜度映射的形式。區分行為、表徵、動力學與吸引子四種等價，並預先登記實驗的否證條件。",
    "STABLE", "E0", created="2026-09-08", updated=mtime(PACC_MD), domain="Model Representation",
    eml_publication_type="proposition / conjecture paper", eml_data_basis="THEORY", eml_authors=["Neo.K (EveMissLab)"], eml_date="2026-09-08",
    eml_source_artifact=PACC_MD, eml_tags=["zh-TW", "pre-experimental conjecture"])
rel("PAP-2026-0012", "reports", "RES-2026-0002")
rel("PAP-2026-0012", "formalizes", "THY-2026-0005")
rel("PAP-2026-0012", "packaged_as", aid)

aid = artifact(WP_ZIP, kind="source-package", label="Adaptive Epistemic AI Runtime technical whitepaper v0.1 — source package (whitepaper, schemas, pseudocode, roadmap)")
obj("PAP-2026-0013", "paper", "Adaptive Epistemic AI Runtime — technical whitepaper v0.1",
    "Adaptive Epistemic AI Runtime——以非對稱時空張力、Canonical State、能力記憶與載體中立計算開發 AI 的技術白皮書",
    "Compresses the eleven papers into a runtime architecture: AI = persistent world state + adaptive update + executable capability + verified action, with the minimal loop Input → Parse → Retrieve → Refresh → Plan → Select → Execute → Verify → Commit → Render. Ships JSON schemas for canonical nodes, capabilities and compute containers, a pseudocode skeleton and the AER-0 MVP roadmap.",
    "把十一篇壓縮成一套 runtime 架構：AI = 持久世界狀態 + 自適應更新 + 可執行能力 + 已驗證行動，最小迴圈為 Input → Parse → Retrieve → Refresh → Plan → Select → Execute → Verify → Commit → Render。附 canonical node、capability、compute container 的 JSON schema、pseudocode 骨架與 AER-0 MVP 路線圖。",
    "STABLE", "E1", created=mtime(WP_ZIP), domain="AI Architecture",
    eml_publication_type="technical whitepaper (implementation-oriented draft)", eml_data_basis="THEORY", eml_authors=["Neo.K (EveMissLab)"], eml_date=mtime(WP_ZIP),
    eml_source_artifact=WP_ZIP, eml_checksums={"whitepaper.md sha256": WP_MANIFEST_SHA},
    eml_tags=["zh-TW", "schemas", "roadmap"])
rel("PAP-2026-0013", "reports", "RES-2026-0001")
for t in ("THY-2026-0001", "THY-2026-0002", "THY-2026-0007"):
    rel("PAP-2026-0013", "formalizes", t)
rel("PAP-2026-0013", "packaged_as", aid)

# ---- systems ---------------------------------------------------------------
AER_ZIPS = [
    "AER-0_MVP_v0.1_FINAL.zip",
    "AER-0_MVP_v0.1_Architecture_Comparison_R1.zip",
    "AER-0_MVP_v0.1_Architecture_Comparison_R2_LangGraph.zip",
    "AER-0_MVP_v0.1_Architecture_Comparison_R3_ECT.zip",
    "AER-0_MVP_v0.1_Architecture_Comparison_R4_Policy_Mutation.zip",
    "AER-0_MVP_v0.1_Architecture_Comparison_R5_Complete_Mediation.zip",
    "AER-0_MVP_v0.1_Architecture_Comparison_R6_External_Trust_Anchor.zip",
]
obj("SYS-2026-0001", "system", "AER-0 — Adaptive Epistemic Runtime MVP", "AER-0——自適應認識 runtime MVP",
    "A Python + SQLite reference runtime that owns persistent canonical state; a language model is optional and replaceable. Candidate → verify → versioned commit, mandatory provenance for facts and relations, freshness and confidence as separate state, an asymmetric tension scheduler with shock-triggered refresh, capability/container registries, persisted workflow memory (reuse/adapt/create), and a deterministic/rule/Bayesian/heuristic epistemic router. Grown through six comparison rounds into an epistemic commit transaction with SQLite-level mediation, an Ed25519-signed external anchor and a process-separated writer (79 tests at R6). Developed under mssp-tdd-apr as a DEGRADED-TWIN run — no independent twin verification is claimed.",
    "以 Python + SQLite 實作、自己持有持久 canonical state 的參考 runtime；語言模型可有可無、可替換。Candidate → verify → 版本化 commit、fact／relation 強制 provenance、新鮮度與信心分開存放、非對稱張力排程與 shock 觸發刷新、capability／container 註冊表、持久化 workflow 記憶（reuse／adapt／create）、以及 deterministic／rule／Bayesian／heuristic 的認識論 router。經六輪比較長成帶 SQLite 層中介、Ed25519 簽章外部 anchor 與程序分離 writer 的 epistemic commit transaction（R6 時 79 個測試）。在 mssp-tdd-apr 下以 DEGRADED-TWIN 開發——不主張獨立 twin 驗證。",
    "EXPERIMENTAL", "E2", created=mtime(AER_ZIPS[0]), updated=mtime(AER_ZIPS[-1]),
    domain="AI Architecture", domains=["Agent Systems", "AI Infrastructure"],
    eml_purpose="Make the Adaptive Epistemic Systems architecture executable and falsifiable — not to claim AGI.",
    eml_architecture="Input → Parse → Plan → Select capability/container → Execute → Verify → Candidate → Versioned Commit → Render → Learn workflow; refresh runs separately: canonical nodes → TensionScheduler → selected subset → refresh provider → verify → versioned commit. Only the Committer, after a passing Verifier verdict and expected-version check, may mutate canonical state.",
    eml_release=AER_ZIPS,
    eml_known_limitations=["Not implemented: unrestricted generated-code execution, self-modifying runtime, distributed services, real quantum/biological backends, ontology self-rewrite, production authorization/deployment controls."])
for z in AER_ZIPS:
    aid = artifact(z, kind="release-bundle", label=z.replace(".zip", "").replace("_", " "))
    rel("SYS-2026-0001", "released_as", aid)
for t in ("THY-2026-0001", "THY-2026-0002", "THY-2026-0006", "THY-2026-0007"):
    rel("SYS-2026-0001", "implements", t)
rel("SYS-2026-0001", "supports", "RES-2026-0003")

PACC_ZIPS = [f"PACC-Lab_v0.{i}_{s}_FINAL.zip" for i, s in [
    (1, "E0-E4"), (2, "N3_Adversarial"), (3, "Learned_Reliability"), (4, "Correlated_Sources"),
    (5, "Representation_Sufficiency"), (6, "Composed_Coordinate"), (7, "Cross_Geometry_Transfer"),
    (8, "Transfer_Basin"), (9, "Coordinate_Atlas"), (10, "Cocycle_Coherence"), (11, "Bidirectional_Groupoid"),
    (12, "Bounded_Nonlinear_Transition"), (13, "Residual_Field")]]
obj("SYS-2026-0002", "system", "PACC-Lab — micro-lab harness for the convergence conjecture", "PACC-Lab——收斂猜想的微型實驗室",
    "Fully observable evidence-integration environments, four primitive-level non-probabilistic families (N0–N3), exact Bayesian references, train-only low-complexity mappers, shuffled/constant/broken-composition controls, a design-redundancy diagnostic and frozen preregistered thresholds carried unchanged from v0.1 through v0.13. Each release is a sealed FINAL bundle with its protocol, results and next-experiment preregistration.",
    "可完全觀察的證據整合環境、四個 primitive 層非概率家族（N0–N3）、精確 Bayesian 參考、只在訓練集擬合的低複雜度映射器、shuffled／constant／broken-composition 控制組、設計冗餘診斷，以及從 v0.1 到 v0.13 原封不動的預登記門檻。每個版本都是密封的 FINAL 套件，含協定、結果與下一步實驗的預登記。",
    "EXPERIMENTAL", "E3", created=mtime(PACC_ZIPS[0]), updated=mtime(PACC_ZIPS[-1]),
    domain="Model Representation", domains=["Evaluation", "Formal AI"],
    eml_purpose="Test PACC-B/R/D/A with preregistered gates, negative controls and an explicit family-independence rule.",
    eml_release=PACC_ZIPS)
for z in PACC_ZIPS:
    aid = artifact(z, kind="release-bundle", label=z.replace(".zip", "").replace("_", " "))
    rel("SYS-2026-0002", "released_as", aid)
rel("SYS-2026-0002", "supports", "RES-2026-0002")
rel("SYS-2026-0002", "tests", "THY-2026-0005")

HYB_ZIPS = ["PACC-Hybrid-Lab_v0.1_SYNTHETIC_FINAL.zip", "PACC-Hybrid-Lab_v0.2_REAL_LLM_HARNESS_FINAL.zip"]
obj("SYS-2026-0003", "system", "PACC-LLM Hybrid Lab", "PACC-LLM 混合實驗室",
    "An A/B/C harness — generator only, hard verifier, PACC runtime — over shared candidate pools with equal accounted budgets. v0.1 is a synthetic architecture witness (zero LLM calls); v0.2 adds hand-authored natural-language tasks, a condition-blind judge, literal machine checks independent of the judge, fail-closed behaviour without an API key, and frozen-cache replay for exact reproduction after a live run.",
    "A/B/C harness——純生成器、硬驗證器、PACC runtime——在共享候選池與相同計費預算上運行。v0.1 是合成的架構見證（零次 LLM 呼叫）；v0.2 加入手寫自然語言任務、對條件盲的評審、獨立於評審的字面機器檢查、缺 API key 時 fail-closed，以及 live run 後可精確重播的凍結快取。",
    "EXPERIMENTAL", "E2", created=mtime(HYB_ZIPS[0]), updated=mtime(HYB_ZIPS[1]),
    domain="Reasoning", domains=["Evaluation"],
    eml_purpose="Decide whether a PACC-style commit space changes reasoning coherence, intent handling and creative breadth — first synthetically, then on a real language model.",
    eml_release=HYB_ZIPS)
for z in HYB_ZIPS:
    aid = artifact(z, kind="release-bundle", label=z.replace(".zip", "").replace("_", " "))
    rel("SYS-2026-0003", "released_as", aid)
rel("SYS-2026-0003", "supports", "RES-2026-0004")

# ---- benchmarks ---------------------------------------------------------------
obj("BEN-2026-0001", "benchmark", "PACC micro-lab protocol v0.1 (frozen gates)", "PACC 微型實驗室協定 v0.1（凍結門檻）",
    "The preregistered decision rule reused unchanged from v0.1 to v0.13: E0 purity, held-out representation distance D_R = E[JS(Φ(S_N), S_P)] ≤ 0.05, update commutation D_U ≤ 0.05, off-manifold intervention D_I ≤ 0.08, action agreement ≥ 0.85, a shuffled-target negative control the real map must beat, a design-independence rule (agreement ≥ 0.999 and R² ≥ 0.995 collapse two designs into one family), verdict levels 0–3, and a strong PACC-A gate of at least three independent convergent families.",
    "從 v0.1 到 v0.13 原封重用的預登記判決規則：E0 純度、held-out 表徵距離 D_R = E[JS(Φ(S_N), S_P)] ≤ 0.05、更新交換 D_U ≤ 0.05、離流形干預 D_I ≤ 0.08、行動一致度 ≥ 0.85、真實映射必須勝過的 shuffled-target 負控制、設計獨立規則（一致度 ≥ 0.999 且 R² ≥ 0.995 即視為同一家族）、判決等級 0–3，以及至少三個獨立收斂家族的強 PACC-A 門檻。",
    "STABLE", "E2", created=mtime(PACC_ZIPS[0]), updated=mtime(PACC_ZIPS[-1]), domain="Evaluation", domains=["Model Representation"],
    eml_purpose="Make 'similar' and 'probability-like' non-negotiable after the data are seen.",
    eml_tasks=["Sequential evidence integration over 4 hidden hypotheses × 6 binary prototypes (uniform reliability 0.80; heterogeneous 0.60–0.95 with only ordinal strengths 1–3 given to non-probabilistic systems; adversarial geometry from v0.2).", "Learned source reliability without an oracle (v0.3).", "Correlated source clusters with latent shared inversion, q swept 0.06–0.42 (v0.4–v0.13).", "Dynamic-world regime switches (E4, descriptive only)."],
    eml_metrics=["action agreement", "held-out JS D_R", "update-commutation JS D_U", "intervention JS D_I", "shuffled/constant/broken-composition control JS", "cross-family R²", "basin coverage, transition JS, cocycle path JS, reverse fidelity"],
    eml_evaluation_protocol="Mapper fit on training episodes/worlds only; every gate frozen before the run; secondary multi-seed stresses are labelled post-hoc and never modify the primary decision rule.",
    eml_baseline_models=["Exact Bayesian posterior", "Beta-Bernoulli source-quality reference", "joint-likelihood common-cause reference", "Bayesian HMM (dynamic world)"],
    eml_limitations=["Does not measure LLM equivalence, resource efficiency, hidden-cluster learning, or whether probability is an observer projection; E4 dynamic-world numbers make no superiority claim.",
                     "Synthetic data and theoretical reasoning throughout: theoretically possible is not actually possible."])
rel("BEN-2026-0001", "evaluates", "THY-2026-0005")

obj("BEN-2026-0002", "benchmark", "AER-0 architecture-comparison suite (R1–R6)", "AER-0 架構比較套件（R1–R6）",
    "Deterministic, executable comparisons that grow round by round: R1 — two facts (one stable, one changing at hours 8 and 16), eight queries over 17 simulated hours, baselines B1 stateless / B2 fixed 6-hour TTL / B3 memory + tools / B4 evented compound agent; R3 — scattered policy vs centralized application gate vs AER-ECT on provenance, stale-write, audit and dependency binding; R4 — policy-topology scaling over N ∈ {1, 4, 16, 64} callers × 6 rules; R5 — ten bypass scenarios across five threat layers; R6 — coherent full-DB forgery, anchor mutation, prefix truncation with/without a trusted head, fail-closed anchor, orphan anchor, adapter conformance.",
    "逐輪成長的決定性可執行比較：R1——兩個事實（一穩定、一在第 8 與 16 小時改變）、17 個模擬小時內 8 次查詢，基線 B1 無狀態／B2 固定 6 小時 TTL／B3 記憶 + 工具／B4 事件驅動複合 agent；R3——分散政策 vs 集中式應用 gate vs AER-ECT，比 provenance、stale write、audit 與依賴綁定；R4——N ∈ {1, 4, 16, 64} 個 caller × 6 條規則的政策拓撲縮放；R5——五個威脅層上的十種繞過情境；R6——連貫的整庫偽造、anchor 竄改、有／無可信 head 的前綴截斷、fail-closed anchor、孤兒 anchor、adapter 一致性。",
    "EXPERIMENTAL", "E2", created=mtime(AER_ZIPS[1]), updated=mtime(AER_ZIPS[-1]), domain="Evaluation", domains=["AI Architecture", "Agent Systems"],
    eml_purpose="Ask a narrower question each round: what remains distinct once the baseline is allowed to be as good as AER?",
    eml_metrics=["stale answers", "recomputations", "stable/volatile refreshes", "workflow reuse", "provenance/version-conflict witnesses", "policy sites, rule placements, blast radius, migration edits", "PREVENTED / OPEN_DETECTED / OPEN_UNDETECTED per scenario", "test counts"],
    eml_evaluation_protocol="Baselines are strengthened deliberately (B4 in R1, centralized gate in R3) so ordinary mechanisms are not attributed to AER; every round states supported and not-measured claims separately.",
    eml_limitations=["Not a general-intelligence benchmark; no performance, cost, security-certification or production claim; the LangGraph round is source-grounded, not executed."])
rel("BEN-2026-0002", "evaluates", "THY-2026-0006")
rel("BEN-2026-0002", "evaluates", "THY-2026-0002")

obj("BEN-2026-0003", "benchmark", "PACC-LLM Hybrid A/B/C benchmark", "PACC-LLM 混合 A/B/C benchmark",
    "Three conditions over identical candidate pools: A generator-only, B hard verifier, C PACC runtime (plus post-hoc D 'elastic'). v0.1: 7 categories × 28 tasks × 8 pools × 112 candidates (1,568 shared pool instances). Metrics: explicit hard adherence, derived coherence, soft-intent satisfaction, long-horizon retention, raw and valid novelty, pattern entropy. v0.2: 16 hand-authored natural-language tasks, equal accounted budgets, gold rubric visible only to a condition-blind judge.",
    "三種條件跑在完全相同的候選池上：A 純生成器、B 硬驗證器、C PACC runtime（另有事後的 D「elastic」）。v0.1：7 類 × 28 題 × 8 池 × 112 候選（1,568 個共享池實例）。指標：明示硬約束遵守、衍生一致性、軟意圖滿足、長程保持、原始與有效新穎度、pattern entropy。v0.2：16 個手寫自然語言任務、相同計費預算、只有對條件盲的評審看得到 gold rubric。",
    "EXPERIMENTAL", "E2", created=mtime(HYB_ZIPS[0]), updated=mtime(HYB_ZIPS[1]), domain="Evaluation", domains=["Reasoning"],
    eml_purpose="Separate 'more rejection' from genuine gains in derived dependency coherence, intent handling and constraint-satisfying novelty.",
    eml_metrics=["explicit hard adherence", "derived coherence", "soft-intent satisfaction", "long-horizon retention", "raw novelty", "valid novelty", "pattern entropy"],
    eml_limitations=["A single-model judge is not human evaluation; nothing about real models is measured until a live run exists."])
rel("BEN-2026-0003", "evaluates", "THY-2026-0005")

# ---- datasets -------------------------------------------------------------
obj("DAT-2026-0001", "dataset", "PACC synthetic evidence worlds", "PACC 合成證據世界",
    "Deterministically generated micro-environments: 4 hidden hypotheses × 6 binary prototypes with per-feature reliabilities; source-quality worlds for learned reliability (20 worlds / 280 episodes / 28 observations at primary scale); correlated-cluster worlds with latent shared inversion at q ∈ {0.06 … 0.42}; and regime-switching dynamic worlds. Primary seeds 20260908 (v0.1) and 20260909 (v0.3+); secondary seeds are labelled post-hoc.",
    "決定性生成的微型環境：4 個隱藏假設 × 6 個二元原型與逐特徵可靠度；學習可靠度用的來源品質世界（主要規模 20 個世界／280 回合／28 次觀察）；q ∈ {0.06 … 0.42} 帶潛在共同反轉的相關來源叢集世界；以及 regime 切換的動態世界。主要 seed 20260908（v0.1）與 20260909（v0.3 起）；次要 seed 標為事後。",
    "STABLE", "E2", created=mtime(PACC_ZIPS[0]), updated=mtime(PACC_ZIPS[-1]), domain="Evaluation", eml_data_basis="SYNTHETIC",
    eml_description="Generators and result JSON live inside each PACC-Lab FINAL bundle; environments are regenerated from seed, not stored as static tables.",
    eml_generation_method="Seeded synthetic generation with preregistered structural checks (e.g. joint-vs-naive Bayes log-loss gap = 0 in independent geometry, > 0 in correlated geometry).",
    eml_format="Python generators + JSON result files", eml_known_bias=["Fully observable and synthetic by design; no natural data."])
rel("DAT-2026-0001", "supports", "RES-2026-0002")

obj("DAT-2026-0002", "dataset", "PACC-Hybrid v0.1 shared candidate pools", "PACC-Hybrid v0.1 共享候選池",
    "1,568 candidate-pool instances (7 categories × 28 tasks × 8 repetitions, 112 candidates each) generated synthetically and given identically to all A/B/C conditions, with primary, multiseed and elastic-diagnostic result JSON. No language-model output is included.",
    "1,568 個候選池實例（7 類 × 28 題 × 8 次重複，每池 112 個候選），合成生成並一模一樣地提供給 A/B/C 三個條件，附 primary、multiseed 與 elastic 診斷的結果 JSON。不含任何語言模型輸出。",
    "STABLE", "E2", created=mtime(HYB_ZIPS[0]), domain="Evaluation", eml_data_basis="SYNTHETIC",
    eml_description="pacc_hybrid_v0.1_primary.json, pacc_hybrid_v0.1_multiseed.json, pacc_hybrid_v0.1_elastic_multiseed.json, pacc_hybrid_v0.1_elastic_diagnostic.json inside the v0.1 bundle.",
    eml_generation_method="Seeded synthetic candidate generation (seed 20260909 primary; 8 fixed secondary seeds).", eml_format="JSON",
    eml_known_bias=["Synthetic candidates and synthetic scoring; a real-model pool is the v0.2 open item."])
rel("DAT-2026-0002", "supports", "RES-2026-0004")

# ---- models (the architectures under test) ---------------------------------
MODELS = [
    ("MOD-2026-0001", "N0 — signed support", "N0——帶號支持",
     "Additive signed evidence support per hypothesis; under uniform reliability it is closely related to rescaled log-evidence accumulation, which is why the heterogeneous and adversarial stresses exist.",
     "每個假設的加性帶號證據支持；在均勻可靠度下它與重縮放的 log-evidence 累積關係密切——這正是異質與對抗壓力測試存在的原因。",
     "Exact reparameterization of N1 (agreement 1.000, R² 1.000): counted as one family with N1."),
    ("MOD-2026-0002", "N1 — ordinal tournament", "N1——序數錦標賽",
     "Pairwise ordinal competition between hypotheses; behaviourally and linearly identical to N0 on every tested trajectory.",
     "假設之間的成對序數競爭；在所有測過的軌跡上，行為與線性關係都與 N0 相同。",
     "Exact reparameterization of N0: never counted as an independent confirmation."),
    ("MOD-2026-0003", "N2 — signed graph", "N2——帶號圖",
     "Signed relation graph over hypotheses with graph dynamics; the basin-boundary family — fails the representation threshold under adversarial geometry (v0.2), is less stable under high correlation (v0.4), and has the narrowest, seed-sensitive transfer basin (v0.8).",
     "假設之間的帶號關係圖與圖動力學；吸引域邊界家族——在對抗幾何下未達表徵門檻（v0.2）、高相關下較不穩定（v0.4）、轉移吸引域最窄且對 seed 敏感（v0.8）。",
     "Independent family under the preregistered linear diagnostic."),
    ("MOD-2026-0004", "N3 — constraint competition", "N3——約束競爭",
     "A nonlinear constraint-field system added in v0.2 as the third structurally distinct family; converges bidirectionally across geometries (v0.7) and shares the wider N0/N1 basin (v0.8).",
     "v0.2 加入的非線性約束場系統，作為第三個結構相異的家族；跨幾何雙向收斂（v0.7），與 N0/N1 共享較寬的吸引域（v0.8）。",
     "Independent family under the preregistered linear diagnostic (R² < 0.995 against N0)."),
    ("MOD-2026-0005", "Bayesian reference (exact posterior / Beta-Bernoulli / joint common-cause / HMM)", "Bayesian 參考（精確後驗／Beta-Bernoulli／聯合共同因／HMM）",
     "The probabilistic side of every comparison: exact posteriors with numerical reliabilities, Beta-Bernoulli source-quality learning, the joint-likelihood common-cause model for correlated clusters (and its naive-independence negative control), and a Bayesian HMM for regime switches.",
     "每次比較的概率端：帶數值可靠度的精確後驗、Beta-Bernoulli 來源品質學習、相關叢集的聯合概似共同因模型（及其天真獨立負控制），以及 regime 切換用的 Bayesian HMM。",
     "Reference, not a competitor; hazard and decay are not exhaustively tuned, so no superiority claim in either direction."),
]
for oid, label, label_zh, summary, summary_zh, note in MODELS:
    obj(oid, "model", label, label_zh, summary, summary_zh, "STABLE", "E2", created=mtime(PACC_ZIPS[0]), updated=mtime(PACC_ZIPS[-1]),
        domain="Model Representation", eml_data_basis="SYNTHETIC", eml_provider="EveMissLab (PACC-Lab)", eml_access_type="source inside the PACC-Lab FINAL bundles",
        eml_known_behavior_notes=[note])
    rel("SYS-2026-0002", "contains", oid)
