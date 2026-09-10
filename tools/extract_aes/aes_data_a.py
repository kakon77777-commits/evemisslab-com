# Program, research lines and theories.
from aes_common import obj, rel, mtime

P01 = "Adaptive_Epistemic_Systems_Series_Paper_01_Asymmetric_Spacetime_Tension_v0.1.md"
LAST = "PACC-Lab_v0.13_Residual_Field_FINAL.zip"
D_SERIES = mtime(P01)
D_LAST = mtime(LAST)

obj("PRG-2026-0001", "program",
    "Adaptive Epistemic Systems",
    "自適應世界狀態系統的第一原理框架",
    "A research program that derives an AI runtime from first principles — world knowledge changes at heterogeneous rates, natural language is a rendering rather than the canonical state, capability must be remembered and reused, algorithm and compute substrate are separate — and then forces the derivation into executable reality: the AER-0 reference runtime with six architecture-comparison rounds, and the PACC micro-lab on whether non-probabilistic primitives converge to probability-like structure.",
    "從第一原理推導 AI runtime 的長期研究線：世界知識以不同速率變化、自然語言是 rendering 而非 canonical state、能力必須被記憶與重用、算法與計算載體分離；然後把推導結果逼進可執行的現實——AER-0 參考 runtime 與六輪架構比較，以及檢驗非概率 primitive 是否收斂到概率表象的 PACC 微型實驗室。",
    "ACTIVE", "E2", created=D_SERIES, updated=D_LAST, program=None,
    eml_limitations=[
        "Everything measured so far is synthetic data plus theoretical reasoning, or a deterministic scenario in a reference runtime. Until a real hybrid model exists, an inference is only an inference: theoretically possible is not actually possible.",
    ],
    eml_goals=[
        "Derive an adaptive world-state architecture without starting from existing AI technology names, then test whether its differences survive implementation.",
        "Decide, falsifiably, between Distinct Advantage, Operational Convergence, Behavioral Equivalence Only, Inconclusive and Architecture Worse.",
        "Test the Probabilistic Appearance Convergence Conjecture (PACC) in fully observable micro-environments before touching language models.",
    ],
    eml_open_questions=[
        "PACC-A (architecture attractor) is not closed: only two independent convergent families exist under the preregistered redundancy rule.",
        "Reverse chart transport in the PACC atlas carries a persistent destination bias that neither a bounded quadratic transition nor a base-point residual field explains (v0.12–v0.13); v0.14 tests a sign-free residual subspace.",
        "AER-0 has no executable cross-runtime comparison yet: LangGraph could not be installed in the comparison environment (R2), and R7 (independent witness, transparency proof, signer rotation) is not started.",
        "The real-language-model PACC A/B/C benchmark has a validated harness but has never been executed with a real model.",
    ],
    eml_milestones=[
        "Adaptive Epistemic Systems Series papers 01–11 complete (canonical UTF-8 sources, SHA-256 manifest).",
        "Adaptive Epistemic AI Runtime technical whitepaper v0.1 with schemas, pseudocode and the AER-0 roadmap.",
        "AER-0 MVP v0.1 (Python + SQLite, 25 tests) and comparison rounds R1–R6 (79 tests at R6).",
        "PACC conjecture paper (2026-09-08) and PACC-Lab v0.1–v0.13.",
        "PACC-LLM Hybrid Lab v0.1 (synthetic A/B/C) and v0.2 (real-LLM harness, not yet executed).",
    ])

obj("RES-2026-0001", "research",
    "Blind derivation of an adaptive epistemic architecture",
    "自適應認識系統的盲推導",
    "Starting only from first principles — temporally heterogeneous world knowledge, canonical symbolic state, adaptive representation space, capability memory, substrate-neutral compute — the eleven-paper series derives a candidate architecture and then asks the uncomfortable question the derivation raised: why does it look so much like modern compound AI, and does any of the difference survive into a runtime?",
    "只從第一原理出發——時間異質的世界知識、canonical 符號狀態、自適應表示空間、能力記憶、載體中立計算——十一篇系列推導出一個候選架構，再面對推導本身冒出的不舒服問題：它為什麼越來越像現代複合 AI？差異有沒有任何一部分能活到 runtime 裡？",
    "ACTIVE", "E2", created=D_SERIES, updated=mtime("AER-0_MVP_v0.1_Architecture_Comparison_R6_External_Trust_Anchor.zip"),
    domain="AI Architecture", domains=["Context & Memory", "Agent Systems", "AI-native Systems"], eml_data_basis="THEORY",
    eml_research_questions=[
        "What does an intelligent system look like when derived from world-state, freshness, memory and reuse requirements rather than from existing AI paradigms?",
        "Which of its architectural semantics — canonical state ownership, candidate→verify→commit, mandatory provenance, tension-scheduled refresh — survive comparison with progressively stronger baselines?",
        "If the differences do not survive, is the convergence itself the phenomenon to explain (an intelligent architecture attractor)?",
    ],
    eml_claims=[
        "World knowledge is temporally heterogeneous; a single global refresh clock is either wasteful or stale.",
        "Natural language should be an interface to canonical state, not the canonical state.",
        "After removing what strong baselines already do, the candidate AER core is: epistemic world-state semantics + candidate/verify/commit authority + mandatory fact provenance + node-local tension refresh + capability/container separation + explicit epistemic-operator routing (R2).",
    ],
    eml_limitations=[
        "No performance, cost or long-horizon comparison against a production agent framework has been run; R2's LangGraph comparison is source-grounded only.",
        "One implementation and one substrate cannot speak for all implementations, benchmarks, model families or substrates (Paper 11 §114).",
    ])

obj("RES-2026-0002", "research",
    "PACC conjecture — do non-probabilistic primitives converge to probability-like structure?",
    "PACC 猜想——非概率 primitive 會不會收斂到概率表象？",
    "Systems whose canonical state and update rules never require probability distributions, Bayesian posteriors or sampling are placed in the same evidence-integration tasks as an exact Bayesian reference. The lab measures whether low-complexity train-only maps carry their states to the Bayesian state, whether the maps commute with updates and survive interventions, and whether independently designed families converge — a four-level ladder (PACC-B, -R, -D, -A) with preregistered falsification conditions.",
    "把 canonical state 與更新規則都不需要概率分布、Bayesian posterior 或抽樣的系統，放進與精確 Bayesian 參考相同的證據整合任務中，量測低複雜度、只在訓練集擬合的映射能否把它們的狀態送到 Bayesian 狀態、映射是否與更新交換並在干預下存活、以及獨立設計的家族是否收斂——四層階梯（PACC-B／R／D／A）與預先登記的否證條件。",
    "EXPERIMENTAL", "E3", created=mtime("PACC_Probability_Appearance_Convergence_Conjecture_v0.1_2026-09-08.md"), updated=D_LAST,
    domain="Model Representation", domains=["Formal AI", "Reasoning", "Evaluation"], eml_data_basis="SYNTHETIC",
    eml_research_questions=[
        "Is probability a necessary ontology of intelligence, an effective representation, an engineering convergence form, or an observer's compression of deeper competitive state?",
        "Can a non-probabilistic state be mapped by a low-complexity map to a Bayesian state on held-out tasks, with the update diagram approximately commuting?",
        "Do three or more independently designed non-probabilistic families converge (PACC-A)?",
    ],
    eml_claims=[
        "Supported as a controlled micro-environment witness: PACC-B, PACC-R and PACC-D for N0/N1, N2 and N3 under uniform and heterogeneous evidence quality (v0.1–v0.2), with shuffled-target controls roughly two orders of magnitude worse.",
        "Convergence has a nontrivial basin, not a demonstrated universal attractor: N2 fails the representation threshold under adversarial geometry, and task-state convergence is architecture- and seed-sensitive once reliability must be learned (v0.2–v0.3).",
        "Decision-level probability coordinates can converge while a latent explanatory variable (common-cause posterior) has no direct low-complexity coordinate; the latent coordinate is hierarchical/compositional (v0.4–v0.6).",
        "Frozen composed coordinates transfer across dependence regimes over finite, family-specific basins; a three-chart atlas covers 8/9 of the sweep; forward cocycle coherence is robust on triple overlap, but reverse transport carries a persistent destination bias (v0.7–v0.13).",
    ],
    eml_limitations=[
        "PACC-A is not supported: N0 and N1 are exact reparameterizations, leaving two independent convergent families against a preregistered minimum of three.",
        "Everything is a transparent synthetic micro-lab; nothing here shows that probability is false, that Bayesian inference is unnecessary, that LLM internals are equivalent, or that probability is an observer projection.",
        "PACC is a conjecture. Its numbers are synthetic data and theoretical reasoning; until a real hybrid model exists, an inference is only an inference — theoretically possible is not actually possible.",
    ])

obj("RES-2026-0003", "research",
    "Does epistemic governance survive implementation? The AER-0 architecture comparison",
    "認識論治理能不能活過實作？AER-0 架構比較",
    "Six rounds compare the AER-0 runtime with progressively stronger baselines — a stateless recomputer, fixed-TTL state, memory + tools, an evented compound agent, LangGraph 1.2.11 (source-grounded), and finally a centralized application-level gate that is allowed to be as good as AER. Each round narrows the claim: from 'AER is distinct' to 'AER promotes epistemic governance from application convention to a runtime-level canonical-write boundary', with bounded mediation and an external signed authenticity witness, and explicitly no claim of unique computational capability.",
    "六輪把 AER-0 runtime 與越來越強的基線比較——無狀態重算、固定 TTL、記憶 + 工具、事件驅動複合 agent、LangGraph 1.2.11（僅 source-grounded）、最後是一個允許做得跟 AER 一樣好的集中式應用層 gate。每一輪都把主張收窄：從「AER 不一樣」收到「AER 把認識論治理從應用慣例提升為 runtime 層的 canonical-write 邊界」，附有界中介與外部簽章真實性見證，並明確不主張獨特的計算能力。",
    "EXPERIMENTAL", "E2", created=mtime("AER-0_MVP_v0.1_FINAL.zip"), updated=mtime("AER-0_MVP_v0.1_Architecture_Comparison_R6_External_Trust_Anchor.zip"),
    domain="AI Architecture", domains=["Agent Systems", "Evaluation", "AI Infrastructure"], eml_data_basis="DETERMINISTIC RUNTIME",
    eml_research_questions=[
        "When a baseline is given persistent memory, workflow reuse, event invalidation and versioning, how much of AER remains distinct?",
        "Is a mandatory epistemic commit transaction a new computational capability, or the elevation of convergent mechanisms into a runtime primitive?",
        "Can canonical epistemic mutation be completely mediated, and can authenticity be anchored outside the writable database?",
    ],
    eml_claims=[
        "R1: AER-0 is distinct on tested mutation semantics (provenance gate, optimistic version conflict) but not dominant — the evented baseline needs fewer recomputations.",
        "R3: AER-ECT ≈ centralized application gate on tested governance semantics; computational uniqueness NOT SUPPORTED; architectural elevation supported.",
        "R4: centralization reduces policy scattering (O(NR)→O(R)) and migration surface, at the price of a larger blast radius per shared defect.",
        "R5–R6: bounded complete mediation without tamperproofness; an Ed25519-signed external anchor converts a coherent full-DB forgery from undetected to detectable, given a trusted key and latest-head witness.",
    ],
    eml_limitations=[
        "No executable cross-runtime comparison: LangGraph could not be installed (PyPI DNS unavailable) in the R2 environment.",
        "No performance, cost, security-certification or general-intelligence claim; hostile same-process code and a compromised signer remain outside the trusted boundary.",
    ])

obj("RES-2026-0004", "research",
    "A PACC-style runtime on language models: reasoning, intent and creative breadth",
    "PACC 式 runtime 用在語言模型上：推理、意圖與創造廣度",
    "Does wrapping candidate selection in a canonical hard/derived-constraint commit space change what a generator produces? A synthetic A/B/C witness (generator only / hard verifier / PACC runtime) shows derived coherence and constraint-satisfying novelty up, soft-preference fit slightly down, and a creative-breadth collapse that a post-hoc 'elastic' exploration policy recovers. The real-language-model version of the benchmark has a validated, fail-closed harness but has not been executed.",
    "把候選選擇包進 canonical 硬約束／衍生約束的 commit 空間，會改變生成器的產出嗎？合成的 A/B/C 見證（純生成器／硬驗證器／PACC runtime）顯示衍生一致性與滿足約束的新穎度上升、軟偏好契合略降，以及一個可由事後「elastic」探索策略恢復的創造廣度塌縮。真實語言模型版本的 benchmark 已有驗證過、fail-closed 的 harness，但尚未執行。",
    "ACTIVE", "E2", created=mtime("PACC-Hybrid-Lab_v0.1_SYNTHETIC_FINAL.zip"), updated=mtime("PACC-Hybrid-Lab_v0.2_REAL_LLM_HARNESS_FINAL.zip"),
    domain="Reasoning", domains=["Evaluation", "Agent Systems"], eml_data_basis="SYNTHETIC",
    eml_research_questions=[
        "Is there a reasoning-up / imagination-down trade-off, or is the observed breadth loss a selection-policy artefact separable from the commit constraints?",
        "Will a frontier language model show the same effect as the synthetic witness?",
    ],
    eml_claims=[
        "Within the synthetic witness: reasoning coherence ↑, valid novelty ↑, soft-preference fit slightly ↓, creative breadth ↓ under naive selection and recoverable with exploration separated from commitment (8/8 seeds sign-stable).",
    ],
    eml_limitations=[
        "Zero real LLM calls so far; no claim about real-model reasoning, intent understanding, imagination, hallucination or human-rated usefulness is permitted before a real-model result exists.",
        "The v0.1 numbers are synthetic data and theoretical reasoning; until a real hybrid model exists, an inference is only an inference — theoretically possible is not actually possible.",
    ])

for r in ("RES-2026-0001", "RES-2026-0002", "RES-2026-0003", "RES-2026-0004"):
    rel(r, "belongs_to", "PRG-2026-0001")
rel("RES-2026-0003", "extends", "RES-2026-0001")
rel("RES-2026-0004", "extends", "RES-2026-0002")


def theory(oid, label, label_zh, summary, summary_zh, status, evidence, *, created, updated, domain, domains, research, **f):
    obj(oid, "theory", label, label_zh, summary, summary_zh, status, evidence, created=created, updated=updated,
        domain=domain, domains=domains, eml_data_basis="THEORY", **f)
    for r in research:
        rel(r, "develops", oid)


theory("THY-2026-0001", "Asymmetric spacetime tension: temporally heterogeneous world knowledge",
       "非對稱時空張力：時間異質的世界知識",
       "Asymmetry is lifted from edge direction or weight to the effective time scale of nodes and relations. Each node carries stability, information-decay rate, update tension, system impact and local valid time; refresh is triggered by tension, external disturbance, information age, change velocity and event relevance rather than by one global clock, so stable knowledge sleeps, volatile knowledge refreshes often, and a rarely changing high-impact node triggers wide dependency recomputation when it does change.",
       "把非對稱性從邊的方向或權重，提升到節點與關係的有效時間尺度。每個節點帶有穩定性、資訊衰減率、更新張力、系統影響度與局部有效時間；刷新由張力、外部擾動、資訊年齡、變化速度與事件相關性觸發，而不是一個全域時鐘——穩定知識沉睡、快變知識高頻更新、低頻高影響的基礎節點一旦改變就觸發大範圍依賴重算。",
       "EXPERIMENTAL", "E2", created=D_SERIES, updated=mtime("AER-0_MVP_v0.1_Architecture_Comparison_R1.zip"),
       domain="Context & Memory", domains=["Computation", "AI Architecture"], research=["RES-2026-0001"],
       eml_assumptions=["Knowledge stability is highly non-uniform across formal, physical, social and real-time domains.", "Update cost is not free; over-refresh and under-refresh are both failures."],
       eml_claims=["World knowledge is temporally heterogeneous.", "Freshness is not a timestamp: it is decided jointly by world change rate, source reliability, dependency structure, task risk and system impact (Paper 02)."],
       eml_predictions=["Architecture contribution AC(λ=0) ≈ 0 in a static world, while AC(λ_heterogeneous) > 0; a fixed synchronous-refresh baseline should be worse in highly heterogeneous time-scale environments (Paper 11 §80–82)."],
       eml_falsification_conditions=["No measurable staleness/recomputation advantage over fixed-TTL and event-driven refresh under heterogeneous dynamics.", "The tension field is only an LLM guess with no runtime enforcement — then the theory has not been tested (Paper 11 §29)."],
       eml_known_limitations=["R1 found that in an event-rich deterministic world, pure event invalidation is cheaper than tension scheduling (AER 3 recomputations vs 2)."])

theory("THY-2026-0002", "Canonical symbolic state and candidate → verify → commit authority",
       "Canonical 符號狀態與 candidate → verify → commit 權限",
       "Natural language is input and output, never the canonical state. Text is parsed, normalized, semantically bound and source-tagged into comparable, verifiable symbolic structure; output is rendered from that state. Model and tool outputs are candidate evidence, and only a committer, after a passing verifier and an expected-version check, may mutate canonical state.",
       "自然語言是輸入與輸出，永遠不是 canonical state。文字經解析、正規化、語義綁定與來源標記，轉成可比較、可驗證的符號結構；輸出從該狀態 render 出來。模型與工具的輸出是候選證據，只有 committer 在 verifier 通過與 expected-version 檢查後才能改動 canonical state。",
       "EXPERIMENTAL", "E2", created=mtime("Adaptive_Epistemic_Systems_Series_Paper_03_Executable_Symbolic_State_and_Rendering_v0.1.md"),
       updated=mtime("AER-0_MVP_v0.1_Architecture_Comparison_R3_ECT.zip"),
       domain="AI Architecture", domains=["AI-native Systems"], research=["RES-2026-0001", "RES-2026-0003"],
       eml_assumptions=["Ambiguity, synonymy, context dependence and self-contamination make language a poor sole carrier of state."],
       eml_claims=["Text, tables, code, graphs, numbers and actions are different output projections of one canonical state.", "Inference/tool output → Candidate → Verify → Commit, never direct state mutation."],
       eml_predictions=["A no-provenance fact candidate is rejected before commit; two valid candidates on the same base version yield exactly one commit and one VersionConflict."],
       eml_falsification_conditions=["A strengthened baseline with direct mutable memory reproduces the same state-integrity outcomes at lower cost."],
       eml_known_limitations=["A centralized application-level gate reproduces the tested semantics (R3); the remaining difference is where the obligation lives, not what can be computed."])

theory("THY-2026-0003", "Intelligent architecture attractor",
       "智能架構吸引子",
       "Different first principles may compile into the same small family of computational forms. The comparison framework separates six levels of difference — code, primitive, computation trace, architectural state semantics, observable behaviour, resource efficiency — and asks who owns state, what may rewrite canonical state, and whether dynamics are preserved under low-cost mapping. The series ends with a fixed verdict map: Distinct Advantage, Operational Convergence, Behavioral Equivalence Only, Inconclusive, Architecture Worse.",
       "不同的第一原理可能編譯成同一小族計算形態。比較框架區分六個差異層級——程式碼、primitive、計算軌跡、架構狀態語義、可觀測行為、資源效率——並追問誰持有狀態、什麼可以改寫 canonical state、動態結構在低成本映射下是否保持。系列以固定的判決表結束：Distinct Advantage、Operational Convergence、Behavioral Equivalence Only、Inconclusive、Architecture Worse。",
       "EXPERIMENTAL", "E2", created=mtime("Adaptive_Epistemic_Systems_Series_Paper_07_Blind_Derivation_and_AI_Architecture_Convergence_v0.1.md"),
       updated=mtime("AER-0_MVP_v0.1_Architecture_Comparison_R3_ECT.zip"),
       domain="AI Architecture", domains=["Evaluation", "Formal AI"], research=["RES-2026-0001", "RES-2026-0003", "RES-2026-0002"],
       eml_assumptions=["The executed architecture is the architecture (runtime-truth principle); spec cannot defend runtime."],
       eml_claims=["Theory difference matters only insofar as it survives into measurable state, computation, behaviour or resource use; if it does not survive, the convergence itself becomes the phenomenon to explain.", "If every possible outcome is interpreted as confirmation, the theory has explained nothing."],
       eml_predictions=["Independent architectures' ablation cores intersect (an attractor core) if the attractor is real."],
       eml_falsification_conditions=["Distinct Advantage: stable multidimensional advantage over baselines across models, seeds, tasks and horizons weakens the convergence suspicion.", "Architecture Worse: added structure is operationally unnecessary or harmful."],
       eml_known_limitations=["One implementation provides at most candidate evidence for convergence; an attractor study needs n ≫ 2 independent starting points (Paper 11 §53)."])

theory("THY-2026-0004", "Probability is not Bayesian; Bayes cannot self-authorize its premises",
       "概率不等於貝葉斯；貝葉斯不能自我授權前提",
       "A system can be stochastic, probabilistic or probability-shaped without performing Bayesian conditionalization, and can look Bayesian without a real prior, likelihood or posterior. A layered vocabulary (stochastic, probabilistic, Bayesian-like, exact, approximate, generalized Bayesian) and a Bayesian authenticity test check whether an update is substantively Bayesian or merely redescribed as such; and the update rule itself — prior, likelihood, hypothesis space — needs a justification that Bayes' rule does not supply (Papers 09–10).",
       "一個系統可以是隨機的、概率的或概率形狀的，卻沒有做 Bayesian conditionalization；也可以看起來像 Bayesian，卻沒有真正的 prior、likelihood 或 posterior。一套分層詞彙（stochastic、probabilistic、Bayesian-like、exact、approximate、generalized Bayesian）與「Bayesian authenticity test」檢查一次更新是實質 Bayesian 還是事後被重新描述成 Bayesian；而更新規則本身——prior、likelihood、假設空間——需要一個 Bayes 公式給不出的授權（第 9–10 篇）。",
       "PRELIMINARY", "E0", created=mtime("Adaptive_Epistemic_Systems_Series_Paper_09_Probability_Is_Not_Bayesian_v0.1.md"),
       updated=mtime("Adaptive_Epistemic_Systems_Series_Paper_10_Bayes_Within_Bayes_Meta_Epistemic_Justification_v0.1.md"),
       domain="Formal AI", domains=["Reasoning"], research=["RES-2026-0001", "RES-2026-0002"],
       eml_claims=["'This is a probabilistic system' and 'this is a Bayesian system' are not equivalent statements.", "Bayesian updating is one belief-revision operator among several; the epistemic router should choose the operator explicitly and record its provenance."],
       eml_predictions=["An adaptive epistemic router beats AlwaysBayes, AlwaysLogic and AlwaysRobust across mixed domains only if operator choice is explicit and traced (Paper 11 §86)."],
       eml_falsification_conditions=["Fixed Bayesian updating dominates every mixed-domain test at equal cost."],
       eml_known_limitations=["Formal/conceptual so far; the AER-0 router implements four operators but no mixed-domain routing benchmark has been run."])

theory("THY-2026-0005", "PACC conjecture — the four-level convergence ladder",
       "PACC 猜想——四層收斂階梯",
       "PACC-B (behavioural: D_B ≤ ε), PACC-R (representational: a low-complexity map Φ: S_N → S_P valid on held-out tasks, K(Φ) ≤ κ), PACC-D (dynamical: Φ∘U_N ≈ U_P∘Φ) and PACC-A (architecture attractor across ≥3 independent designs). The conjecture pre-registers its own failure modes F1–F6 — behavioural divergence, no low-complexity map, update diagram fails, intervention divergence, architecture diverges under scale, probability-specific advantage persists — so that 'similar' and 'probability' cannot be redefined after the fact.",
       "PACC-B（行為：D_B ≤ ε）、PACC-R（表徵：在 held-out 任務上仍有效的低複雜度映射 Φ: S_N → S_P，K(Φ) ≤ κ）、PACC-D（動力學：Φ∘U_N ≈ U_P∘Φ）與 PACC-A（≥3 個獨立設計的架構吸引子）。猜想預先登記自己的失敗模式 F1–F6——行為分歧、無低複雜度映射、更新圖失敗、干預分歧、規模下架構分歧、概率特有優勢持續——讓「相似」與「概率」不能事後重新定義。",
       "EXPERIMENTAL", "E3", created=mtime("PACC_Probability_Appearance_Convergence_Conjecture_v0.1_2026-09-08.md"), updated=D_LAST,
       domain="Model Representation", domains=["Formal AI", "Reasoning"], research=["RES-2026-0002"],
       eml_definitions=["Primitive-level non-probabilistic system: canonical state and required updates do not need distributions, Kolmogorov semantics, Bayesian posteriors, a probability-simplex container or sampling; raw weights, orders, signed relations, tensions and constraints are allowed.", "Probability-like representation: a low-complexity map to the simplex that roughly preserves ranking, choice, relative strength and evidence response."],
       eml_assumptions=["Intelligence constraints: partial observation, competing alternatives, finite resources, repeated update, action selection, changing environment."],
       eml_claims=["Probability may emerge from competition without being the original semantics of competition.", "AI's feasible computational forms may be far fewer than the theories that describe them."],
       eml_predictions=["Outcome I behavioural equivalence only → multiple realizability; II representational duality; III dynamical equivalence → alternative coordinates of a common computation; IV computational attractor."],
       eml_falsification_conditions=["F1 D_B ≫ ε_B; F2 no generalizing low-complexity Φ; F3 D_U large; F4 intervention divergence; F5 D_A rises with scale; F6 probability-specific advantage from the update itself."],
       eml_known_limitations=["PACC-A cannot pass with two independent families; the strongest current statement is a nontrivial convergence basin with an atlas of partially overlapping probability-like charts, not a universal attractor.",
                              "A conjecture, tested so far only on synthetic data with theoretical reasoning: theoretically possible is not actually possible."])

theory("THY-2026-0006", "AER-ECT: a mandatory epistemic commit transaction boundary",
       "AER-ECT：強制的認識論 commit 交易邊界",
       "Every canonical knowledge mutation must pass one mandatory epistemic transaction boundary binding claim, evidence, provenance, valid and observed time, expected version, epistemic operator, verification policy, authority, dependencies and refresh policy: Propose → Verify → Authorize → CompareAndCommit → BindDependencies → Audit. Its parts are not new (truth maintenance, transaction logic, PROV, bitemporal state, PDP/PEP); the hypothesis is that the tuple is mandatory at the canonical write boundary — an epistemic reference-monitor-like boundary, not a proven tamperproof monitor.",
       "每一次 canonical knowledge 的改動都必須通過一個強制的認識論交易邊界，綁定 claim、evidence、provenance、有效時間與觀察時間、expected version、認識論算子、驗證政策、權限、依賴與 refresh policy：Propose → Verify → Authorize → CompareAndCommit → BindDependencies → Audit。零件都不新（truth maintenance、transaction logic、PROV、bitemporal state、PDP/PEP）；假說是這個 tuple 在 canonical write 邊界上是強制的——一個類 reference-monitor 的認識論邊界，而非已證明 tamperproof 的 monitor。",
       "EXPERIMENTAL", "E2", created=mtime("AER-0_MVP_v0.1_Architecture_Comparison_R3_ECT.zip"),
       updated=mtime("AER-0_MVP_v0.1_Architecture_Comparison_R6_External_Trust_Anchor.zip"),
       domain="AI Infrastructure", domains=["AI Architecture", "Agent Systems"], research=["RES-2026-0003"],
       eml_claims=["Architectural elevation = same semantic capability + smaller policy-scattering surface + mandatory canonical boundary; not computational uniqueness.", "When accepted knowledge has operational consequences, epistemic governance may deserve the architectural status that transaction boundaries have in databases."],
       eml_predictions=["Policy sites and rule placements scale O(NR) when scattered versus O(R) under one gate; a new caller does not require new policy placement.", "Internal consistency ≠ authenticity: without an external trust anchor a coherent full-DB forgery passes internal audit."],
       eml_falsification_conditions=["Bypass is easy under accidental or adversarial pressure — then ECT is merely a convenient API.", "Hostile same-process code or a full DB writer defeats local controls (accepted: tamperproofness is not claimed)."],
       eml_known_limitations=["Primitive, transaction, provenance, versioning, belief-revision and temporal novelty are weak or not claimed (R3 novelty verdict); OS privilege isolation, signer compromise and cross-resource ACID are not measured (R6)."])

theory("THY-2026-0007", "Capability memory and substrate-neutral compute: Reuse ≻ Adapt ≻ Create",
       "能力記憶與載體中立計算：Reuse ≻ Adapt ≻ Create",
       "Beyond facts, the system keeps the algorithms, tools, execution contracts, costs, versions, applicability conditions and success/failure history it has used, and prefers reusing a known solution path over adapting one over creating one. Algorithms and compute containers are different layers: any environment that accepts representable input, performs a valid state transition and returns readable output is a container with its own cost, latency, error and availability model, so algorithm/container pairs are selected jointly.",
       "除了事實之外，系統也保存用過的算法、工具、執行契約、成本、版本、適用條件與成敗歷史，並且偏好重用已知求解路徑，勝過調整，再勝過重造。算法與計算容器是不同層：任何能接受可表示輸入、執行有效狀態轉換並回傳可讀輸出的環境都是一個容器，各有自己的成本、延遲、誤差與可用性模型，因此算法／容器成對聯合選擇。",
       "EXPERIMENTAL", "E2", created=mtime("Adaptive_Epistemic_Systems_Series_Paper_05_Memory_Algorithms_and_Reusable_Solution_Paths_v0.1.md"),
       updated=mtime("AER-0_MVP_v0.1_FINAL.zip"),
       domain="Computation", domains=["AI Architecture", "AI Infrastructure"], research=["RES-2026-0001"],
       eml_claims=["Reuse ≻ Adapt ≻ Create.", "Algorithm ≠ container; a capability/container pair is the unit of selection and of execution trace."],
       eml_predictions=["Planning cost falls with repeated related tasks; ReuseGain grows with task similarity within the applicability range, and constraint mismatch produces measurable false reuse (Paper 11 §83–84)."],
       eml_falsification_conditions=["No planning-cost reduction with experience; negative transfer dominates."],
       eml_known_limitations=["R1/R2: persistent workflow memory outside the model is not unique to AER; the capability/container separation was 'AER default distinct' only because no core LangGraph primitive was found, not because it cannot be built there."])
