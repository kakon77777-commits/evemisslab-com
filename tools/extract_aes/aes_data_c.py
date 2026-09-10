# AER-0 experiments (MVP closure + comparison rounds R1–R6) and their key results.
from aes_common import obj, rel, artifact, mtime, OBJECTS

ENV = "Python 3.11+, SQLite; no network, no external database, no LLM API required."
REPRO = "Extract the round's FINAL bundle; python -m pytest -q; python -m examples.research_assistant_demo; python -m benchmarks.<round benchmark>. Checksums in SHA256SUMS.txt."
Z = {
    "mvp": "AER-0_MVP_v0.1_FINAL.zip",
    "r1": "AER-0_MVP_v0.1_Architecture_Comparison_R1.zip",
    "r2": "AER-0_MVP_v0.1_Architecture_Comparison_R2_LangGraph.zip",
    "r3": "AER-0_MVP_v0.1_Architecture_Comparison_R3_ECT.zip",
    "r4": "AER-0_MVP_v0.1_Architecture_Comparison_R4_Policy_Mutation.zip",
    "r5": "AER-0_MVP_v0.1_Architecture_Comparison_R5_Complete_Mediation.zip",
    "r6": "AER-0_MVP_v0.1_Architecture_Comparison_R6_External_Trust_Anchor.zip",
}


def exp(oid, key, label, label_zh, summary, summary_zh, result, *, hypothesis, metrics, interpretation,
        limitations, tests, controls=None, run_count=1, procedure=None, status="STABLE", evidence="E2",
        domain="AI Architecture", domains=("Evaluation", "Agent Systems"), extends=None):
    obj(oid, "experiment", label, label_zh, summary, summary_zh, status, evidence,
        created=mtime(Z[key]), domain=domain, domains=list(domains),
        eml_hypothesis=hypothesis, eml_metrics=metrics, eml_interpretation=interpretation,
        eml_limitations=limitations, eml_controls=controls, eml_run_count=run_count,
        eml_result_type=result, eml_procedure=procedure, eml_software_environment=ENV,
        eml_reproduction_instructions=REPRO, eml_completed_at=mtime(Z[key]), eml_data_basis="DETERMINISTIC RUNTIME")
    rel(oid, "runs_on", "SYS-2026-0001")
    rel(oid, "uses_benchmark", "BEN-2026-0002")
    for t in tests:
        rel(oid, "tests", t)
    if extends:
        rel(oid, "extends", extends)
    rel(oid, "produced", artifact(Z[key], kind="release-bundle", label=Z[key]))
    return oid


def result(oid, exp_id, label, label_zh, observed, observed_zh, rtype, *, metrics, interpretation, limitations=None,
           supports=(), contradicts=(), qualifies=(), statistical_notes=None):
    exp_rec = next(o for o in OBJECTS if o["id"] == exp_id)
    obj(oid, "result", label, label_zh, observed, observed_zh, "STABLE", "E2", created=exp_rec["created_at"],
        domain="Evaluation", eml_data_basis=exp_rec["values"].get("eml_data_basis"),
        eml_result_type=rtype, eml_metrics=metrics, eml_interpretation=interpretation,
        eml_limitations=limitations, eml_statistical_notes=statistical_notes)
    rel(exp_id, "produces", oid)
    for t in supports:
        rel(oid, "supports", t)
    for t in contradicts:
        rel(oid, "contradicts", t)
    for t in qualifies:
        rel(oid, "qualifies", t)
    return oid


exp("EXP-2026-0001", "mvp", "AER-0 MVP v0.1 closure: are the invariants executable?", "AER-0 MVP v0.1 收束：不變量能不能被執行？",
    "The approved Python + SQLite runtime was built under mssp-tdd-apr and closed on behavioural, structural and discriminative witnesses: candidate gate, provenance validation, stale-version conflict, stable-vs-volatile scheduling, shock activation, verifier rejection, workflow reuse/adapt/create, model swap, model-free core, end-to-end verified commit. 25 tests; the refresh benchmark selected 2 nodes under fixed TTL versus 1 volatile node under tension scheduling; a clean extracted replay of the sealed archive passed before release.",
    "核准的 Python + SQLite runtime 在 mssp-tdd-apr 下建成，並以行為、結構、判別三類見證收束：candidate gate、provenance 驗證、過期版本衝突、穩定 vs 易變排程、shock 觸發、verifier 拒絕、workflow reuse／adapt／create、模型替換、無模型核心、端到端已驗證 commit。25 個測試；refresh benchmark 在固定 TTL 下選了 2 個節點、在張力排程下只選 1 個易變節點；密封封存包乾淨解壓重播通過後才發布。",
    "POSITIVE",
    hypothesis="The scoped MVP invariants (canonical state ownership, candidate gating, provenance, versioned commit, selective refresh, capability/container separation, workflow reuse, model replaceability) can be implemented with positive and falsifying executable witnesses.",
    metrics={"tests_passed": 25, "refresh_benchmark": {"fixed_6h_ttl_nodes_refreshed": 2, "aer_tension_nodes_refreshed": 1}, "closure": {"behavioral": "PASS", "structural": "PASS", "discriminative": "PASS", "independent_twin": "NotMeasured", "production_readiness": "NotClaimed", "general_ai_superiority": "NotMeasured"}},
    interpretation="A mechanism closure, not a claim of AI superiority: the declared invariants exist in code, are exercised by falsifying witnesses, and survive a fresh-process replay.",
    limitations=["DEGRADED-TWIN: only one live execution context; no simulated independent verdict claimed.", "Not measured: performance against production agent frameworks, live research accuracy, distributed semantics, security hardening, real heterogeneous backends, multi-day drift."],
    tests=["THY-2026-0002", "THY-2026-0001", "THY-2026-0007"],
    procedure="TDD under mssp-tdd-apr; full suite, research-assistant demo and refresh benchmark run before packaging; checksum-verified clean extraction replayed after sealing.")

exp("EXP-2026-0002", "r1", "R1 — deterministic semantics comparison against four baselines", "R1——對四個基線的決定性語義比較",
    "Two facts (one stable, one changing at hours 8 and 16), eight queries over 17 simulated hours. B1 stateless recomputes every query; B2 fixed 6-hour TTL; B3 adds workflow memory; B4 an evented compound agent with event-driven invalidation. AER-0 matches B4 on zero stale answers, zero stable refreshes and workflow reuse, needs one more recomputation (3 vs 2) because its tension policy refreshes proactively, and is alone in blocking a no-provenance fact and catching a conflicting write.",
    "兩個事實（一穩定、一在第 8 與 16 小時改變），17 個模擬小時內 8 次查詢。B1 無狀態每次重算；B2 固定 6 小時 TTL；B3 加 workflow 記憶；B4 是帶事件驅動失效的複合 agent。AER-0 在零過期回答、零穩定節點刷新與 workflow 重用上與 B4 打平，因為張力政策主動刷新而多一次重算（3 vs 2），但只有它擋下無 provenance 的事實並抓到衝突寫入。",
    "MIXED",
    hypothesis="AER's different ownership and update semantics survive into observable runtime behaviour when compared with progressively stronger baselines.",
    metrics={"verdict": "AER_DISTINCT_ON_TESTED_SEMANTICS", "table": {
        "B1_stateless": {"stale": 0, "recomputation": 8, "stable_refresh": 0, "volatile_refresh": 0, "workflow_reuse": 0, "model_swap_preserves_state": False, "blocks_no_provenance": False, "catches_conflict": False},
        "B2_fixed_ttl": {"stale": 2, "recomputation": 4, "stable_refresh": 2, "volatile_refresh": 2, "workflow_reuse": 0, "model_swap_preserves_state": True, "blocks_no_provenance": False, "catches_conflict": False},
        "B3_memory_tools": {"stale": 2, "recomputation": 4, "stable_refresh": 2, "volatile_refresh": 2, "workflow_reuse": 6, "model_swap_preserves_state": True, "blocks_no_provenance": False, "catches_conflict": False},
        "B4_evented_agent": {"stale": 0, "recomputation": 2, "stable_refresh": 0, "volatile_refresh": 2, "workflow_reuse": 6, "model_swap_preserves_state": True, "blocks_no_provenance": False, "catches_conflict": False},
        "AER-0": {"stale": 0, "recomputation": 3, "stable_refresh": 0, "volatile_refresh": 3, "workflow_reuse": 6, "model_swap_preserves_state": True, "blocks_no_provenance": True, "catches_conflict": True}}},
    interpretation="Not a dominance result. Persistent memory across model swap, workflow reuse and selective event-driven refresh are not unique to AER once the baseline is strengthened; the measured difference collapses to state-mutation semantics (provenance gate, optimistic version conflict, candidate/verify/commit authority).",
    limitations=["B4 is a reference implementation of event-driven behaviour, not a real production framework (structural closure PARTIAL).", "Says nothing about intelligence, speed, cost in other environments, or whether an attractor exists."],
    controls=["B4 deliberately stronger than B3 so ordinary event invalidation and external memory are not attributed to AER."],
    tests=["THY-2026-0001", "THY-2026-0002", "THY-2026-0003"], extends="EXP-2026-0001")
result("RST-2026-0001", "EXP-2026-0002", "R1 comparison table", "R1 比較表",
       "AER-0: 0 stale, 3 recomputations, 0 stable refreshes, 6 workflow reuses, blocks the no-provenance fact, catches the conflicting write. B4: 0 stale, 2 recomputations, 0 stable refreshes, 6 reuses, blocks neither.",
       "AER-0：0 過期、3 次重算、0 次穩定節點刷新、6 次 workflow 重用、擋下無 provenance 事實、抓到衝突寫入。B4：0 過期、2 次重算、0 次穩定刷新、6 次重用、兩者都不擋。",
       "MIXED", metrics={"aer_recomputations": 3, "b4_recomputations": 2, "aer_only": ["blocks no-provenance fact", "VersionConflict on stale expected version"]},
       interpretation="Tension scheduling paid one proactive refresh that pure event invalidation did not need in an event-rich world; the surviving distinction is mutation authority, not refresh efficiency.",
       supports=["THY-2026-0002", "THY-2026-0003"], qualifies=["THY-2026-0001"])

exp("EXP-2026-0003", "r2", "R2 — source-grounded structural comparison with LangGraph 1.2.11", "R2——對 LangGraph 1.2.11 的 source-grounded 結構比較",
    "LangGraph 1.2.11 (checkpoint 4.2.0, checkpoint-sqlite 3.1.1) could not be installed — outbound PyPI DNS was unavailable — so the round pins public release/source contracts and compares them with AER-0's executable invariants. Runtime-owned persistent state, checkpoint history, version tracking, long-term stores and TTL memory all converge (LangGraph is richer on resume, time travel, concurrency and delta checkpointing). What remains AER-default-distinct: candidate → verify → commit, mandatory fact provenance, node-level optimistic epistemic commit, task-conditioned tension refresh, capability/container separation, explicit epistemic-operator routing, and the graph meaning an epistemic world representation rather than control flow.",
    "LangGraph 1.2.11（checkpoint 4.2.0、checkpoint-sqlite 3.1.1）裝不起來——對外 PyPI DNS 不可用——因此本輪釘住公開的 release／source 合約，與 AER-0 可執行的不變量比較。runtime 持有的持久狀態、checkpoint 歷史、版本追蹤、長期 store 與 TTL 記憶全部收斂（LangGraph 在 resume、time travel、並行控制與 delta checkpoint 上更豐富）。仍屬 AER 預設獨有的是：candidate → verify → commit、強制 fact provenance、節點層樂觀認識論 commit、任務條件化的張力刷新、capability／container 分離、明示的認識論算子路由，以及「圖」指的是認識論世界表徵而非控制流。",
    "MIXED", run_count=0,
    hypothesis="Against a real stateful agent runtime, some AER semantics remain distinct beyond 'external state outside the model'.",
    metrics={"verdict": "STRONG_CONVERGENCE_WITH_REMAINING_SEMANTIC_CORE", "evidence_mode": "SOURCE_GROUNDED_STRUCTURAL", "executable_langgraph": "NOT_RUN",
             "classification": {"runtime_owned_persistent_state": "CONVERGED", "checkpoint_history": "CONVERGED; LangGraph richer", "version_tracking": "CONVERGED, different granularity", "ttl_memory": "PARTIAL_CONVERGENCE", "tension_refresh": "AER_DEFAULT_DISTINCT", "graph_semantics": "SEMANTICALLY_DISTINCT", "candidate_verify_commit": "AER_DEFAULT_DISTINCT", "mandatory_provenance": "AER_DEFAULT_DISTINCT", "pending_write_resume": "LANGGRAPH_RICHER", "time_travel_fork": "LANGGRAPH_RICHER", "capability_container_separation": "AER_DEFAULT_DISTINCT; not a core LangGraph primitive found", "epistemic_router": "AER_DEFAULT_DISTINCT"}},
    interpretation="The candidate AER core after R2 is epistemic world-state semantics + candidate/verify/commit authority + mandatory fact provenance + node-local tension refresh + capability/container separation + explicit epistemic-operator routing — a major compression of the whitepaper. Everything else is a recurring engineering form.",
    limitations=["Cross-runtime performance, trace and operational equivalence NOT MEASURED; AER side executable, LangGraph side documentary.", "AER-0 is not a 'more advanced runtime' on the available evidence."],
    tests=["THY-2026-0003", "THY-2026-0002", "THY-2026-0007"], extends="EXP-2026-0002",
    procedure="Pin LangGraph release 1.2.11 at commit 644815f (checkpoint base, PregelProtocol, BaseStore, Agent Protocol docs); classify each axis; keep AER invariants covered by the local suite.")
result("RST-2026-0002", "EXP-2026-0003", "R2 classification matrix", "R2 分類矩陣",
       "Seven axes CONVERGED or partially converged (four of them LangGraph richer); six axes AER-default-distinct; graph semantics semantically distinct.",
       "七個軸收斂或部分收斂（其中四個 LangGraph 更豐富）；六個軸為 AER 預設獨有；圖語義為語義上不同。",
       "MIXED", metrics={"converged_or_partial": 7, "langgraph_richer": 4, "aer_default_distinct": 6},
       interpretation="Supports the attractor hypothesis for external state, persistence, graph/workflow execution, history and durable recovery; moves the remaining disagreement upward into what state means, who may mutate it and what a mutation requires.",
       supports=["THY-2026-0003"], qualifies=["THY-2026-0002", "THY-2026-0007"],
       limitations=["Documentary evidence on the LangGraph side; no executable replay."])

exp("EXP-2026-0004", "r3", "R3 — epistemic commit transaction vs scattered and centralized application gates", "R3——認識論 commit 交易 vs 分散式與集中式應用 gate",
    "All canonical writes in AER-0 were migrated to an Epistemic Commit Transaction (claim, evidence, provenance, valid/observed time, expected version, operator, verification policy, authority, dependencies, refresh policy); direct candidate commit became a negative path. Three systems ran the same governance witnesses: an application whose policy is scattered across callers, an application with one centralized mandatory gate, and AER-ECT. The centralized application gate matched AER-ECT on every tested property; computational uniqueness is not supported. 48 tests.",
    "AER-0 所有 canonical 寫入遷移到 Epistemic Commit Transaction（claim、evidence、provenance、有效／觀察時間、expected version、算子、驗證政策、權限、依賴、refresh policy）；直接 candidate commit 變成負向路徑。三套系統跑同一組治理見證：政策分散在各 caller 的應用、有單一集中強制 gate 的應用、AER-ECT。集中式應用 gate 在每個測試性質上都追平 AER-ECT；不支持計算獨特性。48 個測試。",
    "MIXED",
    hypothesis="Binding evidence, provenance, verification, authority, expected version, temporal validity, dependencies and refresh policy into one mandatory canonical-mutation boundary is a new computational capability — or only an architectural elevation of existing mechanisms.",
    metrics={"verdict": "ArchitecturalElevation SUPPORTED; ComputationalUniqueness NOT SUPPORTED", "tests_passed": 48,
             "table": {"unprovenanced_write_blocked": {"scattered": "FAIL", "central_gate": "PASS", "aer_ect": "PASS"}, "stale_write_conflict_caught": {"scattered": "FAIL", "central_gate": "PASS", "aer_ect": "PASS"}, "automatic_audit": {"scattered": "FAIL on mutated path", "central_gate": "PASS", "aer_ect": "PASS"}, "single_governance_site": {"scattered": "NO", "central_gate": "YES", "aer_ect": "YES"}, "canonical_node_links_transaction": {"scattered": "N/A", "central_gate": "optional", "aer_ect": "PASS"}},
             "novelty": {"primitive": "WEAK", "transaction": "WEAK", "provenance": "NONE claimed", "versioning": "NONE claimed", "belief_revision": "NONE claimed", "temporal": "NONE claimed", "compositional": "PLAUSIBLE / NOT PROVEN"}},
    interpretation="Prior art (truth maintenance, transaction logic, agent knowledge-base transactions, W3C PROV, bitemporal data, PDP/PEP, age-of-information scheduling) covers every part. The value is 'there is only one legal write path' instead of 'remember to enforce policy everywhere' — an epistemically governed runtime, not a new computational species. A fair application that centralizes the same rules converges to the same form, which is itself an attractor witness.",
    limitations=["General performance, security advantage and real LangGraph executable equivalence NOT MEASURED.", "Not an exhaustive novelty search; establishes no patent or publication novelty."],
    controls=["APP_CENTRALIZED_GATE is the fair strong opponent; APP_SCATTERED_POLICY is a mutation witness, not a claim about all applications."],
    tests=["THY-2026-0006", "THY-2026-0002", "THY-2026-0003"], extends="EXP-2026-0003")
result("RST-2026-0003", "EXP-2026-0004", "R3: AER-ECT ≈ centralized application gate", "R3：AER-ECT ≈ 集中式應用 gate",
       "On unprovenanced-write blocking, stale-write conflict, automatic audit, dependency binding and single governance site, the centralized application gate and AER-ECT both PASS; the scattered application fails the omission witnesses.",
       "在擋無 provenance 寫入、過期寫入衝突、自動 audit、依賴綁定與單一治理站點上，集中式應用 gate 與 AER-ECT 都 PASS；分散式應用在遺漏見證上失敗。",
       "NEGATIVE", metrics={"aer_ect_vs_central_gate": "equal on all tested semantics", "scattered_failures": 3},
       interpretation="The most important negative result of the line: what AER-ECT computes can be reproduced by an application; what changes is where the obligation lives.",
       contradicts=["THY-2026-0006"], supports=["THY-2026-0003"],
       limitations=["'contradicts' here means the computational-uniqueness reading of ECT; the architectural-elevation reading survives."])

exp("EXP-2026-0005", "r4", "R4 — policy mutation surface: scattered governance vs one mandatory boundary", "R4——政策變異面：分散治理 vs 單一強制邊界",
    "For N ∈ {1, 4, 16, 64} canonical-write callers and R = 6 governance rules, policy sites and rule placements grow as N and N·R under scattered governance versus 1 and R under either a central application gate or AER-ECT; a new rule needs N caller edits versus one; a 75 % caller-local migration leaves 16 of 64 callers on the old contract. The counterweight is explicit: one omitted local rule has blast radius 1/N, a defect in the shared gate has blast radius 1, and under an equal-p toy omission model the expected exposed-caller fraction is identical for all three systems.",
    "對 N ∈ {1, 4, 16, 64} 個 canonical 寫入 caller 與 R = 6 條治理規則，政策站點與規則放置在分散治理下隨 N 與 N·R 成長，在集中式應用 gate 或 AER-ECT 下固定為 1 與 R；新規則要改 N 個 caller vs 改一處；75 % 的 caller 端遷移仍留下 64 個中的 16 個在舊合約上。反向權衡明說：漏掉一條局部規則的爆炸半徑是 1/N，共享 gate 的缺陷爆炸半徑是 1，而在等 p 的玩具遺漏模型下三套系統的預期受影響 caller 比例相同。",
    "MIXED",
    hypothesis="Elevating epistemic governance into one mandatory boundary reduces policy scattering, migration surface and drift opportunity — without magically reducing expected harm.",
    metrics={"verdict": "CENTRALIZATION_REDUCES_SCATTERING_NOT_COMPUTATIONAL_CAPABILITY", "rules": 6, "callers": [1, 4, 16, 64],
             "at_64_callers": {"scattered": {"policy_sites": 64, "rule_placements": 384, "blast_radius_one_omission": 0.015625, "migration_edits": 64, "vulnerable_after_75pct_migration": 16}, "central_gate_and_aer_ect": {"policy_sites": 1, "rule_placements": 6, "blast_radius_one_omission": 1.0, "migration_edits": 1, "vulnerable_after_75pct_migration": 0}},
             "toy_omission_model_p_0_01": {"P_any_scattered": 0.9789, "P_any_central": 0.0585, "expected_exposed_caller_fraction_all_systems": 0.0585}},
    interpretation="Centralization changes the distribution of failure — fewer opportunities for many small local defects, few opportunities for large shared ones — and makes new business callers free of policy replication. AER-ECT is reference-monitor-like (always invoked on the normal write path), not proven tamperproof.",
    limitations=["A model with an explicit toy assumption, not empirical defect data; 97.89 % is not a real-world defect rate.", "Distributed replica/version skew of the central gate, hostile bypass and tamperproofness not modelled."],
    tests=["THY-2026-0006"], extends="EXP-2026-0004",
    procedure="Deterministic structural benchmark plus executable AER regression; CENTRAL_GATE and AER-ECT predicted and observed identical on policy topology.")

exp("EXP-2026-0006", "r5", "R5 — complete mediation and bypass resistance", "R5——完全中介與繞過抗性",
    "An adversarial boundary test across five threat layers, after adding a SQLite authorizer on managed connections, trigger guards on the five protected tables, verifier-only verification-state recording, BEGIN IMMEDIATE commit serialization, and reference-monitor / canonical-integrity audits. Ten scenarios: five PREVENTED (managed direct write, foreign raw write with intact schema, post-verification tamper, fabricated verdict, managed guard drop), three OPEN_DETECTED (foreign guard drop, post-guard-removal node forge, hostile same-process disable), one OPEN_UNDETECTED (full-DB writer forging node and backing candidate consistently), one same-base two-process race SERIALIZED_TO_SEMANTIC_CONFLICT.",
    "橫跨五個威脅層的對抗性邊界測試，前提是加入受管連線的 SQLite authorizer、五張受保護表的 trigger guard、只有 verifier 能寫的驗證狀態、BEGIN IMMEDIATE 的 commit 序列化，以及 reference-monitor／canonical-integrity 稽核。十種情境：五種 PREVENTED（受管直接寫、schema 完整的外部原始寫、驗證後竄改、偽造 verdict、受管移除 guard）、三種 OPEN_DETECTED（外部移除 guard、移除 guard 後偽造節點、同程序敵意停用）、一種 OPEN_UNDETECTED（整庫寫入者一致地偽造節點與其 backing candidate）、一種同基底雙程序競賽 SERIALIZED_TO_SEMANTIC_CONFLICT。",
    "MIXED",
    hypothesis="Canonical epistemic mutation can be completely mediated when callers try to bypass ECT — for a bounded trust boundary.",
    metrics={"verdict": "BOUNDED_COMPLETE_MEDIATION_WITHOUT_TAMPERPROOFNESS", "scenarios": {"PREVENTED": 5, "OPEN_DETECTED": 3, "OPEN_UNDETECTED": 1, "SERIALIZED_TO_SEMANTIC_CONFLICT": 1},
             "reference_monitor": {"complete_mediation": "SUPPORTED IN BOUNDED SCOPE", "tamperproof": "NOT SUPPORTED", "small_analyzable": "PARTIAL"}},
    interpretation="Internal consistency ≠ tamper evidence against a full DB writer: an attacker who removes the triggers and rewrites node, candidate and audit records consistently passes an audit whose entire trust base lives in the same writable database. Hostile same-process Python code is outside the trusted boundary. Stronger than a voluntary ECT API, far weaker than a security kernel.",
    limitations=["Python's sqlite3.create_function() cannot tag the trigger-invoked authorization function DIRECTONLY/INNOCUOUS; no hardened-schema safety claimed.", "Alternate storage adapters, OS privilege isolation and general performance NOT MEASURED."],
    tests=["THY-2026-0006"], extends="EXP-2026-0005")
result("RST-2026-0004", "EXP-2026-0006", "R5 ten-scenario tally", "R5 十情境統計",
       "5 PREVENTED / 3 OPEN_DETECTED / 1 OPEN_UNDETECTED / 1 SERIALIZED_TO_SEMANTIC_CONFLICT; the undetected case is the coherent full-database forgery.",
       "5 PREVENTED／3 OPEN_DETECTED／1 OPEN_UNDETECTED／1 SERIALIZED_TO_SEMANTIC_CONFLICT；未偵測的那一例是連貫的整庫偽造。",
       "MIXED", metrics={"prevented": 5, "open_detected": 3, "open_undetected": 1, "serialized": 1},
       interpretation="No external trust anchor ⇒ no full-DB tamperproof claim — a structural result that defines R6.",
       supports=["THY-2026-0006"], limitations=["Retained negative witnesses are part of the verdict, not implementation accidents."])

exp("EXP-2026-0007", "r6", "R6 — external trust anchor, process-separated writer, adapter conformance", "R6——外部信任 anchor、程序分離 writer、adapter 一致性",
    "Every externally anchored commit binds a digest over the accepted transition into an Ed25519-signed hash chain with an optional out-of-band latest-head receipt; signing authority moves into a child writer process that never returns the private key; a behavioural conformance harness defines what any future state adapter must pass. The R5 coherent full-DB forgery stays OPEN_UNDETECTED for the internal audit and becomes OPEN_DETECTED under the external anchor audit; anchor mutation is DETECTED; valid-prefix truncation is undetected without a trusted head and detected with one; a required-anchor failure fails closed on the tested path; an orphan anchor is detected; the SQLite adapter passes the contract and a deliberately broken adapter is rejected. 79 tests.",
    "每次外部錨定的 commit 都把已接受轉換的 digest 綁進 Ed25519 簽章的 hash chain，並可選帶外的最新 head 收據；簽章權限移入永不回傳私鑰的子 writer 程序；行為一致性 harness 定義未來任何 state adapter 必須通過的合約。R5 的連貫整庫偽造在內部稽核下仍是 OPEN_UNDETECTED，在外部 anchor 稽核下變成 OPEN_DETECTED；anchor 竄改 DETECTED；有效前綴截斷在無可信 head 時未偵測、有 head 時偵測；必要 anchor 失敗時在測試路徑上 fail-closed；孤兒 anchor 被偵測；SQLite adapter 通過合約，刻意弄壞的 adapter 被拒。79 個測試。",
    "MIXED",
    hypothesis="Canonical-state authenticity can be anchored outside the writable database, signing authority can leave the caller process, and adapters can be tested against semantic invariants rather than trusted by API shape.",
    metrics={"verdict": "EXTERNAL_TRUST_ANCHOR_CONVERTS_FULL_DB_FORGERY_FROM_UNDETECTED_TO_DETECTABLE", "tests_passed": 79,
             "scenarios": {"full_db_forgery_internal_audit": "OPEN_UNDETECTED", "full_db_forgery_external_anchor_audit": "OPEN_DETECTED", "signed_entry_mutation": "DETECTED", "prefix_truncation_no_head": "OPEN_UNDETECTED", "prefix_truncation_with_head": "OPEN_DETECTED", "live_signer_extends_truncated_log": "PREVENTED_DURING_PROCESS_LIFETIME", "required_anchor_unavailable": "FAIL_CLOSED", "orphan_anchor": "DETECTED", "writer_private_key_visible_to_parent": "PREVENTED_BY_PROCESS_TOPOLOGY", "sqlite_adapter_contract": "PASS", "broken_adapter": "REJECTED"}},
    interpretation="Authentic(DB) = VerifyChain(PK, L) ∧ MatchDigest(DB, L) ∧ Head(L) = H*: a signed chain is not the freshest chain without an external head witness. AER after R6 = epistemic transaction boundary + bounded mediation + external signed authenticity witness + process-separated signing authority — still governance and verifiability, not unique computational capability.",
    limitations=["Not proven: OS-level writer isolation, signer/key compromise resistance, rollback safety without a trusted head, cross-resource ACID between SQLite and the anchor, split-view resistance, key lifecycle, PostgreSQL/D1 conformance, production security certification."],
    tests=["THY-2026-0006"], extends="EXP-2026-0006",
    procedure="Repeat the R5 forgery under both audits; mutate/truncate the anchor log with and without a head receipt; inject anchor failure inside the open SQLite transaction; run the adapter conformance harness against the SQLite adapter and a broken subclass.")
result("RST-2026-0005", "EXP-2026-0007", "R6: forgery detection flips under an external anchor", "R6：外部 anchor 下偽造偵測翻轉",
       "The same coherent full-DB forgery: internal audit OPEN_UNDETECTED, external anchor audit OPEN_DETECTED; prefix truncation: undetected without a trusted head, detected with one.",
       "同一個連貫整庫偽造：內部稽核 OPEN_UNDETECTED、外部 anchor 稽核 OPEN_DETECTED；前綴截斷：無可信 head 未偵測、有則偵測。",
       "POSITIVE", metrics={"forgery_internal": "OPEN_UNDETECTED", "forgery_external": "OPEN_DETECTED", "truncation_without_head": "OPEN_UNDETECTED", "truncation_with_head": "OPEN_DETECTED"},
       interpretation="Detection, not prevention; and only under the stated key and head trust assumptions.",
       supports=["THY-2026-0006"],
       limitations=["Not a Certificate Transparency or Rekor implementation; a smaller signed hash chain with an optional head receipt."])
