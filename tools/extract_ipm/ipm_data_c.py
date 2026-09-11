# The v0.2 experimental line: the Experiment A protocol, the XA-02…XA-06L
# instrument packages, the synthetic smoke gate, the first real-model pilot and
# its diagnostic, and the declared-but-not-run experiments B–E. Every number in
# the experiment and result records is read from inside the sealed zips; the
# chain of custody the packages declare (XA-04 → XA-02/03, XA-05 → XA-02/03/04,
# XA-06 → XA-02/03/04/05, diagnostic → real-run bundle, bundle manifest →
# member files) is asserted against the bytes in the research folder.
import hashlib
import re

from ipm_common import L, obj, rel, artifact

XA01 = "IPM_v0.2_Experiment_A_Protocol_Package_v0.1.zip"
XA02 = "IPM_v0.2_XA02_30Task_PilotPack_v0.1.zip"
XA03 = "IPM_v0.2_XA03_Reference_Logger_v0.1.zip"
XA04 = "IPM_v0.2_XA04_Model_Runner_v0.1.zip"
XA05 = "IPM_v0.2_XA05_36Trial_SmokeGate_v0.1.zip"
XA06 = "IPM_v0.2_XA06_RealModel_Pilot_Gate_v0.1.zip"
XA06L = "IPM_v0.2_XA06L_Local_Execution_Handoff_v0.1.zip"
REAL = "XA06_REAL_hf.co_empero-ai_Qwythos-9B-v2-GGUF_Q4_K_M_20260903T131913Z.zip"
DIAG = "IPM_XA06_Qwythos9B_FirstRealPilot_Diagnostic_v0.1.zip"
P = {XA02: "IPM_v0.2_XA02_TaskPack_v0.1/", XA03: "IPM_v0.2_XA03_Reference_Logger_v0.1/", XA04: "IPM_v0.2_XA04_Model_Runner_v0.1/",
     XA05: "IPM_v0.2_XA05_36Trial_SmokeGate_v0.1/", XA06: "IPM_v0.2_XA06_RealModel_Pilot_Gate_v0.1/",
     XA06L: "IPM_v0.2_XA06L_Local_Execution_Handoff_v0.1/", REAL: REAL[:-4] + "/", DIAG: DIAG[:-4] + "/"}

# ---- artifacts + the declared chain of custody ---------------------------------
A = {}
A[XA01] = artifact(XA01, kind="experiment-protocol-package", label="EML-IPM-XA-01 v0.1 — Experiment A protocol, run schema and example run")
A[XA02] = artifact(XA02, kind="benchmark-package", label="EML-IPM-XA-02 v0.1 — 30-task pilot pack and reference evaluators (private references separated)")
A[XA03] = artifact(XA03, kind="software-package", label="EML-IPM-XA-03 v0.1 — telemetry and run logger reference implementation")
A[XA04] = artifact(XA04, kind="software-package", label="EML-IPM-XA-04 v0.1 — A0→A5 model runner and scaffold orchestrator")
A[XA05] = artifact(XA05, kind="smoke-gate-package", label="EML-IPM-XA-05 v0.1 — 36-trial end-to-end synthetic smoke gate with canonical scripted run")
A[XA06] = artifact(XA06, kind="software-package", label="EML-IPM-XA-06 v0.1 — real-model pilot gate (READY_FOR_REAL_MODEL, no pilot result inside)")
A[XA06L] = artifact(XA06L, kind="software-package", label="EML-IPM-XA-06L v0.1 — local real-model execution handoff pack (configure → preflight → run → seal)")
A[REAL] = artifact(REAL, kind="results-bundle", label="XA-06 real-model pilot result bundle — Qwythos-9B-v2 Q4_K_M, 36 trials, sealed 2026-09-03 (REAL_MODEL_PILOT_INCOMPLETE)",
                   note="sealed by XA-06L on the executing machine: secrets excluded, absolute paths redacted (redaction_provenance.json), per-file SHA-256 manifest")
A[DIAG] = artifact(DIAG, kind="analysis-package", label="IPM XA-06 first real-model pilot diagnostic v0.1 (2026-09-07) — report, metrics, three figures")

sha = {z: L.artifact_sha(a) for z, a in A.items()}
v04 = L.zip_json(XA04, P[XA04] + "validation_report.json")
assert v04["canonical_dependencies"]["XA02_zip_sha256"] == sha[XA02] and v04["canonical_dependencies"]["XA03_zip_sha256"] == sha[XA03]
readme05 = L.zip_member(XA05, P[XA05] + "README.md").decode("utf-8")
for tag, z in (("XA-02", XA02), ("XA-03", XA03), ("XA-04", XA04)):
    m = re.search(rf"- {tag}: `([0-9a-f]{{64}})`", readme05)
    assert m and m.group(1) == sha[z], f"XA-05 declares a different {tag} package"
v06 = L.zip_json(XA06, P[XA06] + "validation_report.json")
for tag, z in (("XA02", XA02), ("XA03", XA03), ("XA04", XA04), ("XA05", XA05)):
    assert v06["canonical_dependency_package_sha256"][tag] == sha[z], f"XA-06 declares a different {tag} package"
diag_manifest = L.zip_json(DIAG, P[DIAG] + "manifest.json")
DM = L.zip_json(DIAG, P[DIAG] + "diagnostic_metrics.json")
assert diag_manifest["source_zip_sha256"] == DM["source_zip_sha256"] == sha[REAL], "the diagnostic was computed from a different result bundle"
for member, digest in diag_manifest["files"].items():
    assert hashlib.sha256(L.zip_member(DIAG, P[DIAG] + member)).hexdigest() == digest, member
real_manifest = L.zip_json(REAL, P[REAL] + "manifest.json")
for member in ("aggregate.json", "gate_summary.json", "pilot_report.md", "condition_summary.csv", "physical_summary.csv", "protocol_compliance.csv", "xa06.real.redacted.json"):
    assert hashlib.sha256(L.zip_member(REAL, P[REAL] + member)).hexdigest() == real_manifest["files"][member], member

AGG = L.zip_json(REAL, P[REAL] + "aggregate.json")
GATE = L.zip_json(REAL, P[REAL] + "gate_summary.json")
CFG = L.zip_json(REAL, P[REAL] + "xa06.real.redacted.json")
RUN = L.zip_json(REAL, P[REAL] + "pilot_run_summary.json")
SMOKE = L.zip_json(XA05, P[XA05] + "canonical_smoke_run/gate_summary.json")
v03 = L.zip_json(XA03, P[XA03] + "validation_report.json")
v06l = L.zip_json(XA06L, P[XA06L] + "validation_report.json")
m02 = L.zip_json(XA02, P[XA02] + "manifest.json")
tasks02 = L.zip_json(XA02, P[XA02] + "tasks_public.json")["tasks"]
xa01 = L.zip_json(XA01, "IPM_v0.2_Experiment_A_Manifest_v0.1.json")
assert xa01["experiment_id"] == "EML-IPM-XA-01" and xa01["status"] == "READY FOR PILOT"

# ---- benchmark ----------------------------------------------------------------------
obj("BEN-2026-0101", "benchmark", "XA-02 — 30-task pilot pack for the A0→A5 scaffolding response", "XA-02——A0→A5 鷹架響應的 30 題 pilot 任務包",
    f"{m02['task_count']} tasks — {m02['families']['math']} math, {m02['families']['code']} code, {m02['families']['constraint']} constraint — with a public task file (prompt, output contract, pre-registered quality projection), a private reference file that must never enter model context, a deterministic evaluator and a 30/30 self-test. Math and constraint answers are one JSON object; code answers are Python source scored by hidden tests, and code execution is refused unless explicitly enabled inside an external sandbox. The pack's own words: not a general intelligence benchmark but a controlled instrument for measuring scaffolding response under Experiment A.",
    f"{m02['task_count']} 題——數學 {m02['families']['math']}、程式 {m02['families']['code']}、約束 {m02['families']['constraint']}——含公開任務檔（題目、輸出契約、預先登記的品質投影）、絕不可進入模型上下文的私有參考檔、確定性評分器與 30/30 自測。數學與約束題回一個 JSON 物件；程式題回 Python 原始碼、以隱藏測試評分，且除非在外部沙箱明確啟用，否則拒絕執行程式。套件自己的說法：不是通用智能 benchmark，而是 Experiment A 下量測鷹架響應的受控儀器。",
    "STABLE", "E2", created=L.mtime(XA02), domain="Evaluation",
    eml_purpose="Fixed task set with objective, pre-registered quality projections so that the same model can be run from native single pass (A0) to full agentic scaffold (A5) and the quality change attributed to scaffolding rather than to task drift.",
    eml_tasks=[f"{t['id']} ({t['family']}, {t['difficulty']})" for t in tasks02],
    eml_metrics={"math and constraint": "weighted exact fields on one JSON object; constraint tasks satisfied / m with fatal constraints as hard gate", "code": "hidden tests passed / tests (IPM_ALLOW_CODE_EXEC=1 required)", "output contract": "Return only one JSON object. Do not use Markdown fences."},
    eml_evaluation_protocol="evaluate.py is deterministic; reference_private.json is evaluator-private; validation_report.json records the 30/30 package self-test; manifest.json carries per-file SHA-256.",
    eml_baseline_results={"self-test": m02["status"]},
    eml_limitations=["Only three of the thirty tasks (MATH-003, CODE-001, CON-003) have been used, in the 36-trial gate matrices.", "The output contract makes 'quality' depend on format obedience: the first real pilot showed a correct answer scored 0 for not being JSON."],
    eml_tags=["EML-IPM-XA-02", "v0.1", m02["status"]])
rel("BEN-2026-0101", "evaluates", "THY-2026-0109")
rel("BEN-2026-0101", "released_as", A[XA02])

# ---- systems ----------------------------------------------------------------------------
obj("SYS-2026-0101", "system", "XA-03 — telemetry and run logger (physical execution evidence layer)", "XA-03——遙測與執行記錄器（物理執行證據層）",
    f"Provider-agnostic logger that records one benchmark run as append-only events plus telemetry and derives a typed summary deterministically: model-invocation, trajectory, tool-call and verifier spans, candidate created/discarded accounting, wall time, device-time, GPU power integrated to device_energy_j (energy type device_measured, never relabelled as marginal), peak memory and memory residency, with unknowns kept null (Unknown ≠ 0) and forbidden conversions (tokens → J, TDP → J, price → J, GPU-hours → J). Golden fixture 450 J / 1.75 util·s / 12 GB peak / 33 GB·s residency verified; {v03['pytest_output'].strip().splitlines()[-1]}; instrumentation burden is calibrated and reported, not subtracted.",
    f"與模型供應商無關的記錄器：把一次 benchmark 執行記成只增不改的事件流與遙測，再確定性地導出型別化摘要——模型呼叫、軌跡、工具呼叫與驗證器區段，候選建立／丟棄會計，wall time、裝置時間、GPU 功率積分成 device_energy_j（能量型別 device_measured，絕不改標成 marginal）、峰值記憶體與記憶體駐留，未知值保持 null（Unknown ≠ 0），並禁止 tokens → J、TDP → J、price → J、GPU-hours → J 的換算。黃金夾具 450 J／1.75 util·s／12 GB 峰值／33 GB·s 駐留驗證通過；{v03['pytest_output'].strip().splitlines()[-1]}；儀器負擔經校準並報告，不自動扣除。",
    "STABLE", "E2", created=L.mtime(XA03), domain="Computation",
    eml_purpose="Make the physical side of an IPM event (wall time, device energy, memory residency, utilization, operational counts, discarded work) reproducible evidence rather than a claim.",
    eml_architecture="RunSession → EventLogger (paired spans) + TelemetryCollector (Null / System via psutil / NvidiaSmi) → MetricIntegrator (deterministic) → RunSink with atomic finalization (.partial → COMPLETE | ABORTED) and crash recovery that never invents end events; JSON schemas for events, telemetry and run summary.",
    eml_documentation="README.md, SPEC.md (36 sections), IMPLEMENTATION_PLAN.md, validation_report.json inside the package",
    eml_tags=["EML-IPM-XA-03", "v0.1", v03["status"], "Python ≥3.11, no runtime dependencies"])
rel("SYS-2026-0101", "implements", "THY-2026-0105")
rel("SYS-2026-0101", "implements", "THY-2026-0104")
rel("SYS-2026-0101", "supports", "RES-2026-0101")
rel("SYS-2026-0101", "released_as", A[XA03])

obj("SYS-2026-0102", "system", "XA-04 — A0→A5 model runner and scaffold orchestrator", "XA-04——A0→A5 模型執行器與鷹架調度器",
    f"A policy-driven state machine that runs the same TrialExecutor under immutable condition policies: A0 native single pass, A1 extended single trajectory (2× generation budget), A2 eight samples with exact-majority selection, A3 eight samples plus a typed verifier, A4 verifier plus a bounded deterministic tool loop, A5 a bounded PLAN → ACT → OBSERVE → VERIFY → REVISE loop. XA-02 and XA-03 are external canonical dependencies (declared by hash, not vendored); tool actions under A0–A3 are protocol violations; benchmark scoring happens only after the XA-03 run is finalized so scoring cost is never charged to the system; private references are never read by the task loader; no private chain-of-thought is captured. {v04['candidate_clean_package_gate']['pytest']['passed']} tests, status {v04['status']}.",
    f"策略驅動的狀態機，用不可變的條件策略跑同一個 TrialExecutor：A0 原生單次、A1 放大單軌跡（2× 生成預算）、A2 八樣本精確多數決、A3 八樣本加型別化驗證器、A4 驗證器加有界的確定性工具迴圈、A5 有界的 PLAN → ACT → OBSERVE → VERIFY → REVISE 迴圈。XA-02 與 XA-03 是外部 canonical 依賴（以雜湊宣告、不內嵌）；A0–A3 下的工具動作是協定違規；benchmark 評分只在 XA-03 執行封存後進行，評分成本永不計入受測系統；私有參考檔不被任務載入器讀取；不擷取私有思考鏈。{v04['candidate_clean_package_gate']['pytest']['passed']} 個測試，狀態 {v04['status']}。",
    "STABLE", "E2", created=L.mtime(XA04), domain="Agent Systems",
    eml_purpose="Instantiate Paper 09's controlled ablation ladder so that scaffolding gain and scaffolding physical overhead are measured under identical initial information.",
    eml_architecture="ProviderAdapter (Scripted / LocalCommand / OpenAI-compatible) → ConditionPolicy A0–A5 with a BudgetLedger → candidate model → SameModelVerifier (strict JSON parse of an explicit orchestration message) → tool action envelope → EvaluatorBridge to XA-02 → aggregator for SSR / SDR / SCM / marginal yield; all spans recorded through XA-03.",
    eml_documentation="README.md, SPEC.md (27 sections), IMPLEMENTATION_PLAN.md, validation_report.json inside the package",
    eml_tags=["EML-IPM-XA-04", "v0.1", v04["status"], "Policy-Driven State Machine"])
rel("SYS-2026-0102", "implements", "THY-2026-0109")
rel("SYS-2026-0102", "supports", "RES-2026-0103")
rel("SYS-2026-0102", "released_as", A[XA04])

obj("SYS-2026-0103", "system", "XA-06 — real-model pilot gate", "XA-06——真實模型 pilot 閘",
    f"Puts a real model inside the validated XA-01→XA-04 instrument: preflight (one isolated MATH-003/A0 trial through provider, XA-03 and XA-02), the canonical 36-trial matrix (MATH-003, CODE-001, CON-003 × A0…A5 × 2 replicates), gate verification and analysis. Frozen temperature / top-p / seed, the A0/A1 generation-budget multiplier forwarded into the token budget, a calculator tool contract injected only for A4/A5 generator requests, disabled code evaluation treated as quality-unavailable rather than measured zero, and the rule that engineering validation can never be promoted to pilot completion: 'no real model run, no real model claim'. Valid real outcomes explicitly include A0 = A5, A3 < A2, A5 < A0 and SSR = 1. {v06['source_tree_test']['passed']} tests; the package itself contains no pilot result (status {v06['status']}).",
    f"把真實模型放進已驗證的 XA-01→XA-04 儀器：preflight（一次隔離的 MATH-003/A0 試驗走過供應商、XA-03 與 XA-02）、canonical 36 試驗矩陣（MATH-003、CODE-001、CON-003 × A0…A5 × 2 次）、閘驗證與分析。凍結 temperature／top-p／seed，A0/A1 的生成預算倍率轉入 token 預算，計算機工具契約只注入 A4/A5 的生成請求，停用的程式評估視為「品質不可得」而非零分，且工程驗證永遠不能升格為 pilot 完成：「沒跑真模型，就沒有真模型宣稱」。合法的真實結果明文包含 A0 = A5、A3 < A2、A5 < A0 與 SSR = 1。{v06['source_tree_test']['passed']} 個測試；套件本身不含 pilot 結果（狀態 {v06['status']}）。",
    "STABLE", "E2", created=L.mtime(XA06), domain="Evaluation",
    eml_purpose="A gate whose only way to say REAL_MODEL_PILOT_COMPLETE is 36 real-provider terminal trials that pass integrity and protocol checks — without requiring scaffolding to help.",
    eml_architecture="config (provider modes: local OpenAI-compatible / local command / cloud OpenAI-compatible with env-referenced secrets) → preflight → run_real_pilot (fresh provider per trial, XA-04 TrialExecutor, XA-03 spans) → verify_gate → analyze (condition means, SSR/SDR/SCM, marginal yield, physical by condition, protocol compliance, quality availability) → report.",
    eml_documentation="README.md, SPEC.md, STATUS.json, validation_report.json inside the package",
    eml_tags=["EML-IPM-XA-06", "v0.1", v06["status"]])
rel("SYS-2026-0103", "implements", "THY-2026-0109")
rel("SYS-2026-0103", "supports", "RES-2026-0103")
rel("SYS-2026-0103", "released_as", A[XA06])

obj("SYS-2026-0104", "system", "XA-06L — local real-model execution handoff pack", "XA-06L——本地真實模型執行交接包",
    f"The Windows/local handoff from READY_FOR_REAL_MODEL to a sealed result bundle: configure → preflight → run/resume → verify/analyze → seal. Resume skips a matrix point only if its trial result and XA-03 summary exist, both SHA-256 hashes still match, identity matches and the XA-03 state is COMPLETE; a modified point becomes INVALID and is never overwritten silently. Sealing excludes secret values, redacts absolute paths with provenance, makes run directories bundle-relative and re-hashes everything so the bundle can be re-verified on another machine. Software {v06l['candidate_clean_gate']['pytest']}, experiment status in the package: {v06l['real_model_experiment']} — the distinction 'READY_FOR_REAL_MODEL ≠ REAL_MODEL_PILOT_COMPLETE' is the package's stated point.",
    f"從 READY_FOR_REAL_MODEL 到密封結果包的 Windows／本地交接：configure → preflight → run/resume → verify/analyze → seal。resume 只在試驗結果與 XA-03 摘要都在、兩個 SHA-256 仍相符、身分相符且 XA-03 狀態為 COMPLETE 時才跳過該點；被改過的點變成 INVALID，絕不靜默覆寫。封存排除機密值、以來源紀錄遮蔽絕對路徑、把執行目錄改為相對於封存包並全部重新雜湊，讓封存包能在另一台機器上重新驗證。軟體 {v06l['candidate_clean_gate']['pytest']}，套件內的實驗狀態：{v06l['real_model_experiment']}——「READY_FOR_REAL_MODEL ≠ REAL_MODEL_PILOT_COMPLETE」正是套件要說的重點。",
    "STABLE", "E2", created=L.mtime(XA06L), domain="Evaluation",
    eml_purpose="Let a local machine with a GPU execute the canonical 36-trial pilot against an OpenAI-compatible server and hand back a relocatable, hash-sealed bundle — including an honest REAL_MODEL_PILOT_INCOMPLETE when a gate fails.",
    eml_architecture="thin PowerShell wrappers over a cross-platform core: config, preflight, matrix, runner, state (pilot_state.json with per-point hashes), gate, seal; IMPORT_BACK.md defines what to upload for analysis.",
    eml_documentation="README.md, SPEC.md, IMPLEMENTATION_PLAN.md, IMPORT_BACK.md, STATUS.json, validation_report.json inside the package",
    eml_tags=["EML-IPM-XA-06L", "v0.1", v06l["stage"]])
rel("SYS-2026-0104", "extends", "SYS-2026-0103")
rel("SYS-2026-0104", "supports", "RES-2026-0103")
rel("SYS-2026-0104", "released_as", A[XA06L])

# ---- Experiment A protocol (declared; the 30-task experiment has not been run) -------
obj("EXP-2026-0101", "experiment", "Experiment A — single-pass vs scaffolded controlled measurement (protocol v0.1)", "Experiment A——單次智能與鷹架增益的受控實驗協定 v0.1",
    "The first v0.2 experiment: for one model and a fixed task set, climb the scaffold ladder A0 native single pass → A1 extended trajectory → A2 multi-sample → A3 verifier → A4 deterministic local tools → A5 bounded full agentic loop, recording quality and physical cost at every level to obtain a scaffolding response curve, SSR/SDR, scaffold cost multipliers and marginal yields. Five hypotheses (H1 gain exists, H2 gain has physical cost, H3 marginal yield is non-constant, H4 native and system capability are distinguishable, H5 models have different scaffolding profiles), pre-registered quality projections, initial-information equality across A0–A3, budget caps, n = 5 pilot / 20 formal replicates, failure classification and the rule that a null result is not an experiment failure. Status READY FOR PILOT; the thirty-task run itself has not been executed — only the three-task instrument gates below.",
    "第一個 v0.2 實驗：對同一模型與固定任務集，沿鷹架階梯 A0 原生單次 → A1 放大軌跡 → A2 多樣本 → A3 驗證器 → A4 確定性本地工具 → A5 有界完整 agentic 迴圈往上爬，每一級同時記品質與物理成本，得出鷹架響應曲線、SSR/SDR、鷹架成本倍率與邊際產率。五個假說（H1 增益存在、H2 增益有物理成本、H3 邊際產率非常數、H4 原生與系統能力可區分、H5 不同模型有不同鷹架剖面）、預先登記的品質投影、A0–A3 初始資訊相等、預算上限、pilot n = 5／正式 n = 20 次重複、失敗分類，以及「null 結果不是實驗失敗」的規則。狀態 READY FOR PILOT；三十題的正式執行尚未進行——只跑過下面的三題儀器閘。",
    "ACTIVE", "E0", created="2026-09-02", updated=L.mtime(XA01), domain="Evaluation", domains=["Agent Systems"], eml_data_basis="NOT RUN",
    eml_hypothesis="H1 Q_A5 > Q_A0 for at least some non-trivial tasks; H2 E, V_C, T rise with it; H3 marginal yield differs by stage; H4 SSR < 1 stably; H5 SSR and SCM differ across models even at equal Q_A5.",
    eml_procedure="30 tasks (10 math, 10 code, 10 constraint; Easy/Medium/Hard predefined) × A0–A5 × n replicates; A2 8 trajectories with deterministic majority; A3 typed verifier (same-model / independent / formal); A4 ≤ 4 deterministic local tool calls; A5 ≤ 16 invocations, ≤ 8 tool calls, ≤ 3 retry cycles with explicit termination; seeds and decoding frozen; warm weights, clean task state; run IDs IPM-XA-{model}-{task}-{condition}-{replicate}; paired within-task statistics with bootstrap CIs and effect sizes.",
    eml_metrics={"planned outputs": ["ΔQ_k = Q_k − Q_0", "SSR = Q_0 / Q_5, SDR = 1 − SSR", "SCM_j = C_5,j / C_0,j per cost axis", "marginal yield Y_k,j", "response curves Q vs T, E, invocations, device-time", "brute-force flag ΔQ < 0.01 with ΔC/C > 0.5 (exploratory thresholds)", "selection waste ratio, discarded work"],
                 "minimum physical telemetry": ["T_wall", "E_device (E-Grade C)", "M_peak", "V_C"], "status": xa01["status"]},
    eml_controls=["identical prompt, initial context, decoding, system instruction and model version across conditions", "initial-information equality A0–A3; external information gain marked for A4/A5", "no cross-condition leakage; budget self-extension forbidden"],
    eml_run_count=0, eml_result_type="INCONCLUSIVE",
    eml_interpretation="A protocol, not a result. Its instrument (XA-02…XA-06L) was validated synthetically and then used once on three easy tasks with a real local model; whether a scaffolding response curve exists on non-trivial tasks is still open.",
    eml_limitations=["Deliberately does not attempt μI identification, lifecycle energy, cross-substrate comparison, high-ambiguity quality, full Shapley attribution or multi-agent settings.", "Pilot budgets are reference values, not IPM standards."],
    eml_software_environment="protocol document + JSON run schema + YAML example run (EML-IPM-XA-01 v0.1)",
    eml_reproduction_instructions="Implement the ladder with XA-04 against XA-02 tasks, log with XA-03, run through XA-06/XA-06L; see EXP-2026-0103 for the first real execution.",
    eml_benchmark_ids=["BEN-2026-0101"])
rel("EXP-2026-0101", "uses_benchmark", "BEN-2026-0101")
rel("EXP-2026-0101", "runs_on", "SYS-2026-0102")
rel("EXP-2026-0101", "tests", "THY-2026-0109")
rel("EXP-2026-0101", "tests", "CLM-2026-0104")
rel("EXP-2026-0101", "produced", A[XA01])

# ---- XA-05 synthetic smoke gate ------------------------------------------------------------
tot = SMOKE["execution_totals"]
obj("EXP-2026-0102", "experiment", "XA-05 — 36-trial end-to-end smoke gate with a scripted provider (synthetic)", "XA-05——以腳本化供應商跑的 36 試驗端到端煙霧閘（合成）",
    f"Runs MATH-003, CODE-001 and CON-003 × A0–A5 × 2 replicates through XA-04 + XA-03 + XA-02 with a ScriptedProvider whose outputs were constructed so the expected quality curve is known in advance (A0 0.30, A1 0.633, A2–A5 1.0 → SSR 0.30 / SDR 0.70 as fixtures). {SMOKE['trial_count']} trials, {tot['model']} invocations, {tot['trajectory']} trajectories, {tot['retry']} retries, {tot['tool']} tool calls, {tot['verifier']} verifier passes; candidates {tot['created']} = {tot['selected']} selected + {tot['discarded']} discarded; {SMOKE['accounting_mismatches']} accounting mismatches, {SMOKE['private_sentinel_leaks']} private-reference leaks; energy null on purpose (NullCollector) to prove Unknown ≠ 0. The package states scientific_interpretation_allowed: false.",
    f"用 ScriptedProvider 把 MATH-003、CODE-001、CON-003 × A0–A5 × 2 次跑過 XA-04 + XA-03 + XA-02，輸出被刻意設計成品質曲線事先已知（A0 0.30、A1 0.633、A2–A5 1.0 → SSR 0.30／SDR 0.70 純屬夾具）。{SMOKE['trial_count']} 次試驗、{tot['model']} 次呼叫、{tot['trajectory']} 條軌跡、{tot['retry']} 次重試、{tot['tool']} 次工具呼叫、{tot['verifier']} 次驗證；候選 {tot['created']} = {tot['selected']} 選中 + {tot['discarded']} 丟棄；會計不符 {SMOKE['accounting_mismatches']} 件、私有參考洩漏 {SMOKE['private_sentinel_leaks']} 件；能量刻意為 null（NullCollector）以證明 Unknown ≠ 0。套件明寫 scientific_interpretation_allowed: false。",
    "STABLE", "E1", created=L.mtime(XA05), domain="Evaluation", domains=["Agent Systems"], eml_data_basis="SYNTHETIC",
    eml_hypothesis="Engineering only: the XA-01→XA-04 pipeline reconstructs a pre-designed A0→A5 quality structure with exact candidate accounting and no private-reference leakage.",
    eml_procedure="python -m pytest under IPM_XA02_ROOT / IPM_XA03_ROOT / IPM_XA04_ROOT; verify_canonical_output('canonical_smoke_run') re-validates the packaged run from the extracted package.",
    eml_metrics={"gate": {k: SMOKE[k] for k in ("trial_count", "all_trials_complete", "accounting_mismatches", "private_sentinel_leaks", "ssr", "sdr", "energy_scm", "scientific_interpretation_allowed")}, "execution_totals": tot},
    eml_controls=["scripted outputs with a known oracle", "NullCollector so no physical number can masquerade as measurement", "dependency packages pinned by SHA-256"],
    eml_run_count=1, eml_result_type="POSITIVE",
    eml_interpretation="The instrument works as an accounting machine: candidate identity 168 = 36 + 132 holds, nothing leaks, the designed curve comes back out. Nothing here is a statement about any model — the package forbids reading it that way, and this record carries the SYNTHETIC badge for the same reason.",
    eml_limitations=["Synthetic fixtures; three tasks; no physical telemetry by design."],
    eml_software_environment="XA-05 v0.1 over XA-02/03/04 (hashes declared in README and asserted by this extractor)",
    eml_reproduction_instructions="Extract XA-02, XA-03, XA-04 and XA-05 as siblings, export the three roots, PYTHONPATH=. python -m pytest -q; or verify the shipped canonical_smoke_run/.",
    eml_benchmark_ids=["BEN-2026-0101"])
rel("EXP-2026-0102", "extends", "EXP-2026-0101")
rel("EXP-2026-0102", "uses_benchmark", "BEN-2026-0101")
for s in ("SYS-2026-0101", "SYS-2026-0102"):
    rel("EXP-2026-0102", "runs_on", s)
rel("EXP-2026-0102", "produced", A[XA05])

# ---- the first real-model pilot (executed locally 2026-09-03) ------------------------------------
C = AGG["aggregate"]["conditions"]
PH = AGG["physical_by_condition"]
cond = {k: {"quality_mean": round(C[k]["quality_mean"], 4), "quality_n": C[k]["quality_n"], "success_rate": round(C[k]["success_rate"], 4),
            "wall_time_s": round(C[k]["wall_time_mean"], 2), "device_energy_j": round(C[k]["device_energy_mean"], 1),
            "energy_ratio_vs_A0": round(C[k]["device_energy_mean"] / C["A0"]["device_energy_mean"], 3),
            "gpu_peak_memory_gib": round(PH[k]["gpu_peak_memory_mean"] / 2**30, 2),
            "gpu_memory_residency_gib_s": round(PH[k]["gpu_memory_residency_mean"] / 2**30, 1),
            "gpu_utilization_integral_s": round(PH[k]["gpu_utilization_integral_mean"], 2)} for k in ("A0", "A1", "A2", "A3", "A4", "A5")}
scm = AGG["aggregate"]["scm"]
prov = CFG["provider"]
model_id = RUN["model_id"]
assert model_id == "hf.co/empero-ai/Qwythos-9B-v2-GGUF:Q4_K_M"
pilot_summary = (f"The first time a real model was placed inside the IPM instrument: {model_id} served by Ollama on an RTX 3070, run locally on 2026-09-03 by Splice (Claude Code) on Neo.K's authorization through XA-06L — MATH-003, CODE-001, CON-003 × A0–A5 × 2 replicates, {RUN['trial_count']} trials, {DM['operational_totals']['model_invocations']} invocations, {DM['operational_totals']['trajectories']} trajectories, telemetry complete on every trial. "
                 f"Sealed {GATE['status']}: {GATE['verified_complete_count']}/36 complete, three trials aborted because the same-model verifier returned non-JSON to a strict parser (a real model behaviour, deliberately not re-rolled). SSR = {AGG['aggregate']['ssr']:.1f}, SDR = {AGG['aggregate']['sdr']:.1f}: scaffolding brought no measured quality gain on these three easy tasks while A5 used {scm['device_energy_j']:.2f}× the device energy and {scm['wall_time_s']:.2f}× the wall time of A0, and the fixed eight-sample conditions A2–A4 used 7.9–9.3×. "
                 f"The apparent A3/A4 quality rise to 0.667 is a missingness artifact; and for two of the three tasks the recorded 'quality' was output-format compliance, not task correctness (post-hoc: 33/33 completed outputs semantically correct; strict output-contract compliance 12/36).")
pilot_summary_zh = (f"第一次把真實模型放進 IPM 儀器：{model_id} 由 Ollama 在 RTX 3070 上服務，2026-09-03 由 Splice（Claude Code）在 Neo.K 授權下透過 XA-06L 於本地執行——MATH-003、CODE-001、CON-003 × A0–A5 × 2 次，{RUN['trial_count']} 次試驗、{DM['operational_totals']['model_invocations']} 次呼叫、{DM['operational_totals']['trajectories']} 條軌跡，每次試驗遙測完整。"
                    f"封存為 {GATE['status']}：{GATE['verified_complete_count']}/36 完成，三次試驗因同模型驗證器對嚴格解析器回了非 JSON 而中止（真實的模型行為，刻意不重擲）。SSR = {AGG['aggregate']['ssr']:.1f}、SDR = {AGG['aggregate']['sdr']:.1f}：在這三個簡單任務上鷹架沒有帶來可測的品質增益，A5 卻用了 A0 的 {scm['device_energy_j']:.2f}× 裝置能量與 {scm['wall_time_s']:.2f}× wall time，固定八樣本的 A2–A4 用了 7.9–9.3×。"
                    f"A3/A4 看似升到 0.667 是缺值造成的假象；且三個任務裡有兩個，記錄到的「品質」是輸出格式服從性而非任務正確性（事後檢查：33/33 完成的輸出語意正確；嚴格輸出契約合規 12/36）。")
obj("EXP-2026-0103", "experiment", "XA-06 first real-model pilot — Qwythos-9B-v2 on the A0→A5 ladder (36 trials, 2026-09-03)", "XA-06 第一次真實模型 pilot——Qwythos-9B-v2 走 A0→A5 階梯（36 試驗，2026-09-03）",
    pilot_summary, pilot_summary_zh,
    "STABLE", "E2", created="2026-09-03", updated="2026-09-07", domain="Evaluation", domains=["Agent Systems", "Computation"], eml_data_basis="REAL MODEL",
    eml_ai_collaborators=["Aletheia (GPT-5.6 Sol, OpenAI ChatGPT) — protocol, instrument packages and the 2026-09-07 diagnostic", "Splice (Claude Code, Anthropic) — local execution, sealing and the RESULT note"],
    eml_hypothesis="Experiment A's H1–H4 on the three-task gate matrix: does scaffolding raise quality, at what physical cost, with non-constant marginal yield, and is SSR < 1?",
    eml_model_ids=["MOD-2026-0006"], eml_benchmark_ids=["BEN-2026-0101"],
    eml_hardware="NVIDIA GeForce RTX 3070 (8 GiB VRAM; peak 7.59 GiB used, peak 208.9 W, 73 °C), Windows 10 host; physical boundary local-runner-plus-visible-accelerator; energy type device_measured (E-Grade C, CST-B)",
    eml_software_environment="Ollama serving the model through an OpenAI-compatible endpoint at 127.0.0.1:11434; XA-02/03/04/06/06L v0.1 (hashes verified byte-exact against their manifests before the run); Python 3.14.5; XA-03 collectors system + nvidia_smi at 250 ms target (observed ~335–350 ms)",
    eml_configuration={"provider": {k: prov[k] for k in ("mode", "provider_id", "model_id", "base_max_tokens", "temperature", "top_p", "seed", "budget_control_validated", "auth_mode")},
                       "matrix": {"tasks": RUN["tasks"], "conditions": RUN["conditions"], "replicates": RUN["replicates"]},
                       "allow_code_evaluation": CFG["evaluation"]["allow_code_evaluation"], "telemetry": CFG["telemetry"]},
    eml_procedure="XA-06L configure → preflight (all checks PASS; isolated MATH-003/A0 quality 1.0) → run (36/36 terminal, 0 runtime failures) → verify gate (3 points xa03_not_complete) → analyze → seal. The three aborted points were not re-run with resume --force: re-rolling until the gate turns green would erase a real failure mode.",
    eml_metrics={"gate": {"status": GATE["status"], "verified_complete_count": GATE["verified_complete_count"], "invalid_or_missing": GATE["invalid_or_missing"]},
                 "headline": {"ssr": AGG["aggregate"]["ssr"], "sdr": AGG["aggregate"]["sdr"], "scm_device_energy": round(scm["device_energy_j"], 4), "scm_wall_time": round(scm["wall_time_s"], 4),
                              "protocol_compliance_rate": round(AGG["protocol_compliance_rate"], 4), "quality_available_rate": round(AGG["quality_available_rate"], 4)},
                 "by_condition": cond,
                 "operational_totals": DM["operational_totals"],
                 "verifier_failure": DM["verifier_failure"],
                 "strict_protocol_compliance": DM["strict_protocol_compliance"],
                 "posthoc_semantic_diagnostic (non-canonical)": DM["posthoc_semantic_diagnostic"],
                 "physical_totals": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in DM["physical"].items()},
                 "quality_availability_reporting_inconsistency": DM["quality_availability_reporting"]},
    eml_controls=["fresh provider per trial; frozen temperature 0.2, top-p 1.0, seed 7; base_max_tokens 1024 with validated 2× budget for A1", "identical initial task text across conditions; calculator tool contract only in A4/A5 generator requests", "scoring after XA-03 finalization; private references never in context; code evaluation disabled on the host"],
    eml_random_seeds=["seed 7 (frozen into every HTTP request); model nondeterminism otherwise uncontrolled"], eml_run_count=1,
    eml_result_type="MIXED",
    eml_interpretation="As an instrument gate it did its job: real numbers, full telemetry, a sealed and relocatable bundle, and an honest INCOMPLETE. As science it says three things and no more. (1) On three tasks the native single pass already solves, scaffolding cannot show a quality gain — SSR = 1 is a legal null result, and it cost 3.1× (A5) to 9.3× (A3) the device energy of A0; A5 was cheaper than the fixed eight-sample conditions only because its loop stopped early. (2) The instrument's quality axis conflated output-format obedience with task correctness on CODE-001 (correct code inside a Markdown fence) and CON-003 (correct assignment written as A=X, not JSON) — exactly the SyntacticValidity ≠ SemanticCorrectness split Paper 06 predicts, now observed in the lab's own instrument. (3) The same-model verifier's serialization failed in 3 of 18 verifier trials and discarded eight candidates each time; tool access was enabled but never used, so tool and retry effects are unidentified. The A3/A4 'gain' is survivor bias from the aborted low-format trials. Seven instrument revisions are required before XA-07; the dataset stays immutable.",
    eml_limitations=["Three easy tasks, two replicates, one 9B model at 4-bit, one machine; not a population-level estimate of anything.", "Gate INCOMPLETE (33/36); CODE-001 quality unmeasured (execution disabled) so 12 of 36 trials have no measured quality; quality-availability is reported inconsistently inside the bundle (22/36 vs 33/36).", "Device-measured GPU energy only — not marginal, not whole-system; telemetry sampling itself cost ~24 % of trial wall time.", "Same-model verifier; no independent or formal verifier condition."],
    eml_reproduction_instructions="Unpack XA-02/03/04/06/06L as siblings, .\\configure.ps1 (local_openai_compatible, base_url http://127.0.0.1:11434, the model id above), .\\preflight.ps1, .\\run-pilot.ps1, .\\seal-results.ps1; verify the sealed bundle against its manifest.json (266 files). The bundle's raw events/telemetry/summaries are unchanged by sealing.",
    eml_completed_at="2026-09-03")
for p, t in (("extends", "EXP-2026-0101"), ("extends", "EXP-2026-0102"), ("uses_benchmark", "BEN-2026-0101"), ("uses_model", "MOD-2026-0006"),
             ("runs_on", "SYS-2026-0101"), ("runs_on", "SYS-2026-0102"), ("runs_on", "SYS-2026-0103"), ("runs_on", "SYS-2026-0104"),
             ("tests", "THY-2026-0109"), ("tests", "CLM-2026-0104"), ("tests", "THY-2026-0106"), ("tests", "THY-2026-0105")):
    rel("EXP-2026-0103", p, t)
rel("EXP-2026-0103", "produced", A[REAL])
rel("EXP-2026-0103", "produced", A[DIAG])


def result(oid, label, label_zh, observed, observed_zh, rtype, *, metrics, interpretation, limitations, supports=(), contradicts=(), qualifies=()):
    obj(oid, "result", label, label_zh, observed, observed_zh, "STABLE", "E2", created="2026-09-03", updated="2026-09-07", domain="Evaluation",
        eml_data_basis="REAL MODEL", eml_result_type=rtype, eml_metrics=metrics, eml_interpretation=interpretation, eml_limitations=limitations,
        eml_ai_collaborators=["Aletheia (GPT-5.6 Sol, OpenAI ChatGPT) — 2026-09-07 diagnostic", "Splice (Claude Code, Anthropic) — execution and RESULT note"])
    rel("EXP-2026-0103", "produces", oid)
    for t in supports:
        rel(oid, "supports", t)
    for t in contradicts:
        rel(oid, "contradicts", t)
    for t in qualifies:
        rel(oid, "qualifies", t)


result("RST-2026-0101", "Scaffolding response on three easy tasks: SSR = 1.0, 3.1× device energy at A5, 7.9–9.3× at A2–A4",
       "三個簡單任務上的鷹架響應：SSR = 1.0，A5 的裝置能量 3.1×、A2–A4 7.9–9.3×",
       f"Condition means (quality over available trials / wall s / device J): A0 {cond['A0']['quality_mean']} / {cond['A0']['wall_time_s']} / {cond['A0']['device_energy_j']}; A1 {cond['A1']['quality_mean']} / {cond['A1']['wall_time_s']} / {cond['A1']['device_energy_j']}; A2 {cond['A2']['quality_mean']} / {cond['A2']['wall_time_s']} / {cond['A2']['device_energy_j']}; A3 {cond['A3']['quality_mean']} / {cond['A3']['wall_time_s']} / {cond['A3']['device_energy_j']}; A4 {cond['A4']['quality_mean']} / {cond['A4']['wall_time_s']} / {cond['A4']['device_energy_j']}; A5 {cond['A5']['quality_mean']} / {cond['A5']['wall_time_s']} / {cond['A5']['device_energy_j']}. Energy ratio vs A0: A1 {cond['A1']['energy_ratio_vs_A0']}, A2 {cond['A2']['energy_ratio_vs_A0']}, A3 {cond['A3']['energy_ratio_vs_A0']}, A4 {cond['A4']['energy_ratio_vs_A0']}, A5 {cond['A5']['energy_ratio_vs_A0']}. Total measured GPU energy {DM['physical']['total_measured_gpu_energy_kwh']:.4f} kWh over {DM['physical']['summed_trial_wall_time_min']:.1f} min of trial time; memory residency rises from {cond['A0']['gpu_memory_residency_gib_s']} GiB·s (A0) to {cond['A3']['gpu_memory_residency_gib_s']} GiB·s (A3).",
       f"各條件平均（可用試驗的品質／wall 秒／裝置焦耳）：A0 {cond['A0']['quality_mean']}／{cond['A0']['wall_time_s']}／{cond['A0']['device_energy_j']}；A1 {cond['A1']['quality_mean']}／{cond['A1']['wall_time_s']}／{cond['A1']['device_energy_j']}；A2 {cond['A2']['quality_mean']}／{cond['A2']['wall_time_s']}／{cond['A2']['device_energy_j']}；A3 {cond['A3']['quality_mean']}／{cond['A3']['wall_time_s']}／{cond['A3']['device_energy_j']}；A4 {cond['A4']['quality_mean']}／{cond['A4']['wall_time_s']}／{cond['A4']['device_energy_j']}；A5 {cond['A5']['quality_mean']}／{cond['A5']['wall_time_s']}／{cond['A5']['device_energy_j']}。能量相對 A0：A1 {cond['A1']['energy_ratio_vs_A0']}、A2 {cond['A2']['energy_ratio_vs_A0']}、A3 {cond['A3']['energy_ratio_vs_A0']}、A4 {cond['A4']['energy_ratio_vs_A0']}、A5 {cond['A5']['energy_ratio_vs_A0']}。36 次試驗共量得 GPU 能量 {DM['physical']['total_measured_gpu_energy_kwh']:.4f} kWh、試驗時間 {DM['physical']['summed_trial_wall_time_min']:.1f} 分鐘；記憶體駐留從 A0 的 {cond['A0']['gpu_memory_residency_gib_s']} GiB·s 升到 A3 的 {cond['A3']['gpu_memory_residency_gib_s']} GiB·s。",
       "MIXED", metrics={"ssr": AGG["aggregate"]["ssr"], "sdr": AGG["aggregate"]["sdr"], "scm": {"device_energy_j": round(scm["device_energy_j"], 4), "wall_time_s": round(scm["wall_time_s"], 4)}, "by_condition": cond, "marginal_yield": AGG["aggregate"]["marginal_yield"]},
       interpretation="The cost side of the scaffolding response curve is real and steep; the quality side is flat because the tasks were already solved at A0 and because the quality axis was confounded (RST-2026-0102). This is one point on the 'no gap' side of F4 with almost no weight: it neither supports nor refutes the scaffolding-separation hypothesis on non-trivial tasks. The A3/A4 0.667 is not a gain: the aborted CON-003 trials dropped out of the quality denominator and the surviving mean rose.",
       limitations=["quality_n is 4 (A0–A2, A5) or 3 (A3, A4) per condition because CODE-001 quality is unavailable and three trials aborted — means over 3–4 values.", "Device-measured GPU energy at ~24 % sampling overhead; not marginal energy."],
       qualifies=["THY-2026-0109", "CLM-2026-0104"])

result("RST-2026-0102", "Diagnostic: the measured 'quality' was format compliance on 2 of 3 tasks; verifier serialization failed 3/18; the A3/A4 rise is a missingness artifact",
       "診斷：三題中兩題量到的「品質」是格式服從性；驗證器序列化失敗 3/18；A3/A4 的上升是缺值假象",
       f"Strict output-contract compliance {DM['strict_protocol_compliance']['count']}/{DM['strict_protocol_compliance']['total']} (MATH-003 12/12, CODE-001 0/12, CON-003 0/12), but the non-canonical post-hoc check finds every completed selected output correct — math {DM['posthoc_semantic_diagnostic']['math']}, code {DM['posthoc_semantic_diagnostic']['code']}, constraint {DM['posthoc_semantic_diagnostic']['constraint']} — {DM['posthoc_semantic_diagnostic']['completed_selected_outputs_correct']} overall. Verifier-enabled trials {DM['verifier_failure']['verifier_enabled_trials']}, verifier-protocol failures {DM['verifier_failure']['count']} (A3 {DM['verifier_failure']['by_condition']['A3']}, A4 {DM['verifier_failure']['by_condition']['A4']}, A5 {DM['verifier_failure']['by_condition']['A5']}), each after eight candidates had been generated. Tool calls {DM['operational_totals']['tool_calls']}, retries {DM['operational_totals']['retries']}; {DM['operational_totals']['candidates_abandoned_on_abort']} candidates abandoned on abort are neither selected nor discarded in the schema. Quality availability is reported as 22/36 in the aggregate and 33/36 in protocol_compliance.csv. Telemetry sampling wall fraction {DM['physical']['mean_sampling_call_wall_fraction']:.3f}.",
       f"嚴格輸出契約合規 {DM['strict_protocol_compliance']['count']}/{DM['strict_protocol_compliance']['total']}（MATH-003 12/12、CODE-001 0/12、CON-003 0/12），但非 canonical 的事後檢查發現所有完成的選中輸出都正確——數學 {DM['posthoc_semantic_diagnostic']['math']}、程式 {DM['posthoc_semantic_diagnostic']['code']}、約束 {DM['posthoc_semantic_diagnostic']['constraint']}——整體 {DM['posthoc_semantic_diagnostic']['completed_selected_outputs_correct']}。啟用驗證器的試驗 {DM['verifier_failure']['verifier_enabled_trials']} 次，驗證器協定失敗 {DM['verifier_failure']['count']} 次（A3 {DM['verifier_failure']['by_condition']['A3']}、A4 {DM['verifier_failure']['by_condition']['A4']}、A5 {DM['verifier_failure']['by_condition']['A5']}），每次都在已生成八個候選之後。工具呼叫 {DM['operational_totals']['tool_calls']} 次、重試 {DM['operational_totals']['retries']} 次；{DM['operational_totals']['candidates_abandoned_on_abort']} 個在中止時被拋棄的候選在 schema 裡既非選中也非丟棄。品質可得率在聚合檔報 22/36、在 protocol_compliance.csv 報 33/36。遙測取樣占 wall time 的 {DM['physical']['mean_sampling_call_wall_fraction']:.3f}。",
       "NEGATIVE", metrics={"strict_protocol_compliance": DM["strict_protocol_compliance"], "posthoc_semantic_diagnostic": DM["posthoc_semantic_diagnostic"], "verifier_failure": DM["verifier_failure"], "operational_totals": DM["operational_totals"], "quality_availability_reporting": DM["quality_availability_reporting"], "instrumentation": {"mean_sampling_call_wall_fraction": round(DM["physical"]["mean_sampling_call_wall_fraction"], 4), "target_sampling_ms": 250, "observed_cadence_ms": "335–350"},
                            "instrument_revisions_required_before_XA-07": ["R1 typed subject/system failure is valid data, separate from instrument failure", "R2 split task_semantic_quality / output_contract_compliance / system_completion_reliability / verifier_protocol_reliability", "R3 failure-aware aggregation (no survivor means)", "R4 abandoned-candidate accounting", "R5 preserve verifier parse diagnostics", "R6 cheaper telemetry (persistent nvidia-smi / NVML)", "R7 tool-trigger tasks"]},
       interpretation="Negative for the instrument, informative for the theory. Task semantic quality ≠ protocol/serialization compliance — the model solved everything it completed and was scored 0.5 on average for not obeying a JSON/no-fence contract; same-model verification reduced system reliability rather than raising quality; tool access ≠ tool utilization (enabled, never used). The bundle stays immutable as XA-06 empirical v0.1; the next step is to revise the instrument and re-run a small validation set, not to re-roll failures until they disappear.",
       limitations=["The post-hoc semantic check is explicitly non-canonical and does not make the strict outputs compliant.", "One model; whether stronger models obey the output contract is unknown."],
       supports=["THY-2026-0106"], qualifies=["RST-2026-0101", "THY-2026-0109"])

# ---- experiments B–E: declared in the canonical index, not run ------------------------------
for oid, label, label_zh, summary, summary_zh, hyp, proc, tests in (
    ("EXP-2026-0104", "Experiment B — binary vs numeric human measurement (declared)", "Experiment B——二元 vs 數值的人類測量（已宣告）",
     "Compare direct 0–10 rating, structured yes/no items and adaptive pairwise comparison on response time, missingness, inconsistency, test–retest, predictive validity and fatigue, with participants randomized across formats. Declared in the canonical index as the third v0.2 experiment; not designed in detail and not run.",
     "比較直接 0–10 評分、結構化是／否題與自適應成對比較在反應時間、缺答、不一致、重測、預測效度與疲勞上的表現，受試者隨機分配到不同格式。canonical index 宣告為 v0.2 第三個實驗；尚未細部設計、尚未執行。",
     "F3: well-designed binary/pairwise protocols beat direct numeric rating on at least one of response time, consistency, dropout, predictive validity or fatigue.",
     "Randomize participants across the three formats on the same artifacts; estimate latent quality with Bradley–Terry / IRT models; report measurement-process metrics alongside the estimates.", ["CLM-2026-0103", "THY-2026-0107"]),
    ("EXP-2026-0105", "Experiment C — μI operational identification (declared)", "Experiment C——μI 的操作性辨識（已宣告）",
     "On proof steps, code repair and constraint puzzles, construct candidate semantic transitions, then test them by ablation and counterfactual replacement to see whether an effective semantic count N_μ can be identified and whether it predicts anything. Declared as the fourth v0.2 experiment; not run.",
     "在證明步驟、程式修復與約束謎題上建構候選語意轉換，再以消融與反事實替換檢驗，看有效語意計數 N_μ 能否被辨識、能否預測任何事。宣告為 v0.2 第四個實驗；尚未執行。",
     "F5: adding N_μ improves prediction or explanation of efficiency, error paths, scaffold gain or cross-architecture comparison over physical cost → quality alone.",
     "Candidate transition construction → ablation / counterfactual replacement → contribution test Q(Y | μ) > Q(Y | do(μ = 0)) → utility test against direct physical-cost models.", ["CLM-2026-0105", "THY-2026-0102"]),
    ("EXP-2026-0106", "Experiment D — physical trace alignment (declared)", "Experiment D——物理軌跡對齊（已宣告）",
     "On one machine, align GPU power telemetry, latency, peak memory, memory bandwidth and device occupancy with execution events — the telemetry side that XA-03 already provides — before any claim about data-center energy. Declared as the second v0.2 experiment in the recommended order; the pilot's XA-03 traces are its first raw material, but the alignment study itself has not been run.",
     "在同一台機器上把 GPU 功率遙測、延遲、峰值記憶體、記憶體頻寬與裝置占用對齊到執行事件——XA-03 已提供的遙測面——在任何資料中心能源宣稱之前先做。建議順序中的第二個 v0.2 實驗；pilot 的 XA-03 軌跡是它的第一批原料，但對齊研究本身尚未執行。",
     "F2 (partial): with operations controlled, time, energy, memory traffic and residency still vary independently; device-level traces can be aligned to semantic-level events.",
     "Same hardware, matched workloads differing in memory pattern; XA-03 telemetry at reduced instrument cost (NVML) aligned to trajectory/tool/verifier spans.", ["CLM-2026-0102", "THY-2026-0105", "THY-2026-0104"]),
    ("EXP-2026-0107", "Experiment E — token / FLOPs proxy failure test (declared)", "Experiment E——token／FLOPs 代理量失效檢驗（已宣告）",
     "Executions of the same task quality under different languages, verbosity, context lengths and memory pressure, comparing token count, FLOPs, energy, time, memory traffic and N_μ^eff to see where token and FLOPs stop tracking cost and work. Declared as the last v0.2 experiment; not run.",
     "在相同任務品質下用不同語言、冗長度、上下文長度與記憶體壓力執行，比較 token 數、FLOPs、能量、時間、記憶體流量與 N_μ^eff，看 token 與 FLOPs 在哪裡不再追蹤成本與工作。宣告為 v0.2 最後一個實驗；尚未執行。",
     "F1 and F2: N_μ^eff per token drifts across phrasings/languages, and same-FLOPs executions differ in T, E, B_M, V_M.",
     "Matched-quality executions varied in language, verbosity, context and memory pressure; record TokenCount, FLOPs, E, T, B_M, N_μ^eff.", ["CLM-2026-0101", "CLM-2026-0102"]),
):
    obj(oid, "experiment", label, label_zh, summary, summary_zh, "IDEA", "E0", created="2026-09-02", domain="Evaluation", eml_data_basis="NOT RUN",
        eml_hypothesis=hyp, eml_procedure=proc, eml_run_count=0, eml_result_type="INCONCLUSIVE",
        eml_interpretation="Declared, not run; listed so the program's falsifiable propositions each have their intended test on record.",
        eml_limitations=["No protocol package exists yet; the canonical index gives the design in one paragraph."])
    for t in tests:
        rel(oid, "tests", t)
