# PACC-Lab v0.1–v0.13 and PACC-LLM Hybrid v0.1–v0.2 experiments, with key results.
from aes_common import obj, rel, artifact, mtime, OBJECTS

PZ = {i: f"PACC-Lab_v0.{i}_{s}_FINAL.zip" for i, s in [
    (1, "E0-E4"), (2, "N3_Adversarial"), (3, "Learned_Reliability"), (4, "Correlated_Sources"),
    (5, "Representation_Sufficiency"), (6, "Composed_Coordinate"), (7, "Cross_Geometry_Transfer"),
    (8, "Transfer_Basin"), (9, "Coordinate_Atlas"), (10, "Cocycle_Coherence"), (11, "Bidirectional_Groupoid"),
    (12, "Bounded_Nonlinear_Transition"), (13, "Residual_Field")]}
HZ = {1: "PACC-Hybrid-Lab_v0.1_SYNTHETIC_FINAL.zip", 2: "PACC-Hybrid-Lab_v0.2_REAL_LLM_HARNESS_FINAL.zip"}
MODELS = ["MOD-2026-0001", "MOD-2026-0002", "MOD-2026-0003", "MOD-2026-0004", "MOD-2026-0005"]
REPRO_PACC = "Extract the version's FINAL bundle; python -m pytest -q; run the version's primary script with the recorded seed; docs/PACC_LAB_v0.N_RESULTS.md and docs/EXPERIMENT_PROTOCOL_v0.N.md are inside the bundle."


def pacc(v, oid, label, label_zh, summary, summary_zh, result, *, hypothesis, metrics, interpretation, limitations,
         seeds, evidence="E3", models=MODELS):
    z = PZ[v]
    obj(oid, "experiment", label, label_zh, summary, summary_zh, "STABLE", evidence, created=mtime(z),
        domain="Model Representation", domains=["Evaluation", "Formal AI"],
        eml_hypothesis=hypothesis, eml_metrics=metrics, eml_interpretation=interpretation, eml_limitations=limitations,
        eml_random_seeds=seeds, eml_run_count=len(seeds), eml_result_type=result,
        eml_controls=["shuffled-target mapping", "constant prediction", "broken composition (v0.6+)", "target-local refit (v0.7+)"],
        eml_software_environment="Python; deterministic seeded generators; no network, no LLM.",
        eml_reproduction_instructions=REPRO_PACC, eml_completed_at=mtime(z), eml_data_basis="SYNTHETIC",
        eml_model_ids=models, eml_dataset_ids=["DAT-2026-0001"], eml_benchmark_ids=["BEN-2026-0001"])
    rel(oid, "runs_on", "SYS-2026-0002")
    rel(oid, "uses_benchmark", "BEN-2026-0001")
    rel(oid, "uses_dataset", "DAT-2026-0001")
    for m in models:
        rel(oid, "uses_model", m)
    rel(oid, "tests", "THY-2026-0005")
    if v > 1:
        rel(oid, "extends", f"EXP-2026-{7 + v - 1:04d}")
    rel(oid, "produced", artifact(z, kind="release-bundle", label=z))
    return oid


def result(oid, exp_id, label, label_zh, observed, observed_zh, rtype, *, metrics, interpretation, limitations=None,
           supports=(), contradicts=(), qualifies=()):
    exp_rec = next(o for o in OBJECTS if o["id"] == exp_id)
    obj(oid, "result", label, label_zh, observed, observed_zh, "STABLE", "E3", created=exp_rec["created_at"], domain="Evaluation",
        eml_data_basis=exp_rec["values"].get("eml_data_basis"),
        eml_result_type=rtype, eml_metrics=metrics, eml_interpretation=interpretation, eml_limitations=limitations)
    rel(exp_id, "produces", oid)
    for t in supports:
        rel(oid, "supports", t)
    for t in contradicts:
        rel(oid, "contradicts", t)
    for t in qualifies:
        rel(oid, "qualifies", t)


pacc(1, "EXP-2026-0008", "PACC-Lab v0.1 — E0–E4: first micro-witness", "PACC-Lab v0.1——E0–E4：第一個微型見證",
     "Three primitive-level non-probabilistic systems (N0 signed support, N1 ordinal tournament, N2 signed graph) integrate evidence over four hidden hypotheses next to an exact Bayesian reference. All three pass the Level-3 micro criteria — held-out JS ≤ 0.0101, update JS ≤ 0.0042, intervention JS ≤ 0.0058, action agreement ≥ 0.957 — in both uniform and heterogeneous evidence quality, with shuffled-target controls around 0.31–0.33. The redundancy diagnostic collapses N0 and N1 into one exact reparameterization family, leaving two independent families against a PACC-A minimum of three.",
     "三個 primitive 層的非概率系統（N0 帶號支持、N1 序數錦標賽、N2 帶號圖）在四個隱藏假設上整合證據，旁邊是精確的 Bayesian 參考。三者在均勻與異質證據品質下都通過 Level-3 微型準則——held-out JS ≤ 0.0101、更新 JS ≤ 0.0042、干預 JS ≤ 0.0058、行動一致度 ≥ 0.957——shuffled-target 控制組約 0.31–0.33。冗餘診斷把 N0 與 N1 合併為一個精確重參數化家族，獨立家族只剩兩個，未達 PACC-A 最低要求三個。",
     "MIXED", seeds=["20260908", "8 fixed secondary seeds (post-hoc)"],
     hypothesis="A system whose canonical state and update rules do not require probability can converge toward a Bayesian reference in behaviour, held-out state representation and update dynamics.",
     metrics={"verdict": "PRELIMINARY_PACC_B_R_D_MICRO_WITNESS_WITHOUT_STRONG_ATTRACTOR_CLOSURE", "e0_purity": True,
              "uniform": {"N0": {"agreement": 0.983073, "heldout_js": 0.000192, "update_js": 0.000052, "intervention_js": 0.000061, "shuffled_js": 0.322816}, "N1": {"agreement": 0.983073, "heldout_js": 0.000192, "update_js": 0.000052, "intervention_js": 0.000068, "shuffled_js": 0.312444}, "N2": {"agreement": 0.957465, "heldout_js": 0.008053, "update_js": 0.003872, "intervention_js": 0.005756, "shuffled_js": 0.309444}},
              "heterogeneous": {"N0": {"agreement": 0.983073, "heldout_js": 0.002878, "update_js": 0.000559, "intervention_js": 0.000645}, "N2": {"agreement": 0.958767, "heldout_js": 0.010109, "update_js": 0.004186, "intervention_js": 0.004187}},
              "independent_families": 2, "strong_attractor_minimum": 3, "secondary_8_seed_pass_rate": 1.0},
     interpretation="Non-probabilistic primitives can exhibit probability-like state and update structure in controlled micro-tasks; two independent convergent families are not enough to establish a computational attractor. Under uniform reliability additive signed support is closely related to rescaled log-evidence accumulation — the heterogeneous stress makes the result less trivial, not deeply equivalent.",
     limitations=["Does not show probability is false, Bayesian inference unnecessary, LLM internals equivalent, non-probabilistic systems superior, or probability an observer projection.", "E4 dynamic-world numbers are descriptive only (HMM hazard and decay untuned)."])
result("RST-2026-0006", "EXP-2026-0008", "v0.1 primary table: Level 3 for N0/N1/N2, two families", "v0.1 主要表：N0/N1/N2 皆 Level 3，兩個家族",
       "Held-out JS 0.000192 (N0/N1) and 0.008053 (N2) uniform; 0.002878 and 0.010109 heterogeneous; shuffled controls ≈ 0.31–0.33; N0↔N1 agreement 1.000, R² 1.000.",
       "均勻：held-out JS 0.000192（N0/N1）與 0.008053（N2）；異質：0.002878 與 0.010109；shuffled 控制組 ≈ 0.31–0.33；N0↔N1 一致度 1.000、R² 1.000。",
       "MIXED", metrics={"level": {"N0": 3, "N1": 3, "N2": 3}, "families": [["N0", "N1"], ["N2"]]},
       interpretation="PACC-B/R/D supported as a controlled micro-environment witness; PACC-A not yet supported.",
       supports=["THY-2026-0005"], qualifies=["THY-2026-0005"])

pacc(2, "EXP-2026-0009", "PACC-Lab v0.2 — third family (N3) and adversarial evidence geometry", "PACC-Lab v0.2——第三個家族（N3）與對抗性證據幾何",
     "Adds N3 constraint competition, a nonlinear constraint-field family, plus an adversarial geometry chosen to break additive/log-odds mappings, keeping every v0.1 threshold. N3 reaches Level 3 in all three geometries; N2 keeps agreement 0.8546 and small update/intervention error but its held-out representation JS 0.053327 crosses the 0.05 gate under adversarial geometry, so it is classified behavioural convergence only. Independent families under the linear diagnostic: {N0, N1}, {N2}, {N3}; robust across all three geometries: two.",
     "加入非線性約束場家族 N3 約束競爭，以及專門用來破壞加性／log-odds 映射的對抗性幾何，所有 v0.1 門檻不變。N3 在三種幾何下都達 Level 3；N2 在對抗幾何下一致度 0.8546、更新／干預誤差仍小，但 held-out 表徵 JS 0.053327 越過 0.05 門檻，歸為僅行為收斂。線性診斷下的獨立家族：{N0, N1}、{N2}、{N3}；三種幾何下都穩健的：兩個。",
     "MIXED", seeds=["20260908", "8 secondary seeds (smaller scale)", "5 adversarial seeds near primary scale"],
     hypothesis="A structurally distinct third family also converges, and convergence survives an evidence geometry designed against additive mappings.",
     metrics={"verdict": "THIRD INDEPENDENT FAMILY CONVERGES; ROBUST PACC-A GATE REMAINS OPEN",
              "adversarial": {"N0": {"agreement": 0.90818, "heldout_js": 0.023921, "level": 3}, "N2": {"agreement": 0.85455, "heldout_js": 0.053327, "level": 1}, "N3": {"agreement": 0.90162, "heldout_js": 0.014454, "level": 3}},
              "five_seed_adversarial_level3_rate": {"N0": 1.0, "N1": 1.0, "N2": 0.6, "N3": 1.0}, "independent_convergent_families": 2, "pacc_a": False},
     interpretation="Probability-like convergence has a nontrivial basin, not a demonstrated universal attractor: the N3 result weakens the 'disguised additive accumulator' explanation, and N2 shows convergence is not guaranteed for every architecture under every geometry.",
     limitations=["Independence is supported under the preregistered linear diagnostic only, not proof of deep nonlinear nonequivalence.", "N2's boundary is adversarial sensitivity around the threshold, not a universal phase boundary."])
result("RST-2026-0007", "EXP-2026-0009", "v0.2 adversarial geometry: N3 converges, N2 crosses the representation gate", "v0.2 對抗幾何：N3 收斂、N2 越過表徵門檻",
       "N3 held-out JS 0.014454 (Level 3); N2 held-out JS 0.053327 > 0.05 (Level 1); N0/N1 0.023921 (Level 3).",
       "N3 held-out JS 0.014454（Level 3）；N2 held-out JS 0.053327 > 0.05（Level 1）；N0/N1 0.023921（Level 3）。",
       "MIXED", metrics={"n2_heldout_js": 0.053327, "gate": 0.05, "n3_heldout_js": 0.014454},
       interpretation="Convergence is basin-dependent; the preregistered threshold did its job without being moved.",
       qualifies=["THY-2026-0005"])

pacc(3, "EXP-2026-0010", "PACC-Lab v0.3 — learned source reliability without an oracle", "PACC-Lab v0.3——無 oracle 的來源可靠度學習",
     "Both sides lose the source-quality oracle: the Bayesian reference learns Beta-Bernoulli source quality; the non-probabilistic systems learn a qualitative reputation (trust, friction, streak, familiarity). Fitted on training worlds and evaluated on unseen source-quality permutations, the reputation state maps to the Beta-Bernoulli state with JS ≈ 0.00714 versus 0.017–0.018 for shuffled/constant controls, and feedback-update commutation ≈ 0.00130 — stable 6/6 across seeds. Task-state convergence is architecture- and seed-sensitive: at exact primary scale N0/N1 4/4, N2 3/4, N3 2/4.",
     "雙方都失去來源品質 oracle：Bayesian 參考學 Beta-Bernoulli 來源品質；非概率系統學定性聲譽（信任、摩擦、連勝、熟悉度）。在訓練世界上擬合、在未見過的來源品質排列上評估，聲譽狀態映射到 Beta-Bernoulli 狀態的 JS ≈ 0.00714，shuffled／constant 控制組為 0.017–0.018，回饋更新交換 ≈ 0.00130——跨 seed 穩定 6/6。任務狀態收斂則依架構與 seed 而異：在主要規模下 N0/N1 4/4、N2 3/4、N3 2/4。",
     "MIXED", seeds=["20260909", "6 secondary seeds (smaller)", "4 seeds at exact primary scale"],
     hypothesis="Convergence survives when source reliability must be learned from delayed feedback rather than given.",
     metrics={"verdict": "RELIABILITY-STATE CONVERGENCE ROBUST; TASK CONVERGENCE PARTIAL / BASIN-SENSITIVE", "primary_scale": "20 worlds / 280 episodes / 28 observations",
              "reliability_mapping_js": 0.007136, "control_js": "0.017–0.018", "feedback_commutation_js": 0.001298, "reliability_independent_families": 1,
              "task_pass_at_primary_scale": {"N0": "4/4", "N1": "4/4", "N2": "3/4", "N3": "2/4"}},
     interpretation="Calibration-state convergence can be robust while task-state convergence has architecture-dependent basins. A first fixed-quality diagnostic was rejected because Beta means became near-constant and shuffled targets fit almost as well — that redesign is part of the evidence.",
     limitations=["All four wrappers share one NonProbReputationLedger, so reliability convergence counts as one family, not four.", "Does not prove Beta-Bernoulli learning and qualitative reputation universally equivalent."])

pacc(4, "EXP-2026-0011", "PACC-Lab v0.4 — correlated sources and dependence geometry", "PACC-Lab v0.4——相關來源與依賴幾何",
     "Sources are grouped into clusters with a latent shared inversion; the correct reference uses the joint likelihood and a naive independent-product Bayes is the negative control (joint beats naive in moderate and high geometry; gap exactly 0 in the independent geometry). Non-probabilistic systems see only cluster membership. Task-state convergence survives: N0/N1/N3 pass in moderate and high correlation (N2 drops to agreement 0.8364 in high). The latent dependence coordinate — the posterior that the cluster is in its corrupted branch — is not recovered by a train-only affine-sigmoid map from any system: real JS ≈ shuffled ≈ constant.",
     "來源分成叢集並帶潛在共同反轉；正確的參考用聯合概似，天真的獨立乘積 Bayes 是負控制（在中、高相關幾何下聯合勝過天真；獨立幾何下差距恰為 0）。非概率系統只看得到叢集歸屬。任務狀態收斂存活：N0/N1/N3 在中、高相關下通過（N2 在高相關下一致度掉到 0.8364）。潛在依賴座標——叢集處於受污染分支的後驗——任何系統的 train-only affine-sigmoid 映射都無法重建：真實 JS ≈ shuffled ≈ constant。",
     "MIXED", seeds=["20260909", "6 secondary seeds", "4 high-correlation seeds at primary scale"],
     hypothesis="Task-state convergence survives dependent evidence, and the non-probabilistic relation state itself maps to the Bayesian common-cause posterior.",
     metrics={"verdict": "TASK-LEVEL CONVERGENCE SURVIVES DEPENDENT EVIDENCE; LATENT DEPENDENCE-STATE CONVERGENCE NOT SUPPORTED",
              "environment": {"joint_vs_naive_logloss": {"independent": [1.245687, 1.245687], "moderate": [1.632599, 1.834445], "high": [1.758082, 2.018617]}},
              "task": {"moderate": {"N0": {"agreement": 0.955247, "D_R": 0.008095}, "N3": {"agreement": 0.942901, "D_R": 0.008234}}, "high": {"N0": {"agreement": 0.861111, "D_R": 0.009827}, "N2": {"agreement": 0.836420, "D_R": 0.017874}}},
              "dependence_coordinate": {"moderate_real_js": 0.0605, "moderate_shuffled": 0.0641, "moderate_constant": 0.0615, "high_real_js": 0.0398, "high_shuffled": 0.0400, "high_constant": 0.0397, "pass": 0}},
     interpretation="A layered picture: a decision-relevant quotient state can converge to a probabilistic coordinate while a deeper latent explanatory variable stays representation-dependent — evidence against the strongest 'everything becomes probability-like' reading.",
     limitations=["A result about the current state representation and frozen readout, not a theorem that no richer relation graph could encode the latent variable.", "Cluster membership is given, not learned."])
result("RST-2026-0008", "EXP-2026-0011", "v0.4: latent dependence coordinate not recovered", "v0.4：潛在依賴座標無法重建",
       "Dependence-coordinate pass count 0 for all four systems in every seed; in high correlation real JS ≈ 0.0398 is below the 0.05 absolute gate but no better than shuffled (≈ 0.0400) or constant (≈ 0.0397).",
       "四個系統在每個 seed 下依賴座標通過數皆為 0；高相關下真實 JS ≈ 0.0398 低於 0.05 絕對門檻，但不比 shuffled（≈ 0.0400）或 constant（≈ 0.0397）好。",
       "NEGATIVE", metrics={"dependence_pass": 0, "systems": 4},
       interpretation="Low absolute error ⇏ meaningful coordinate map; the negative-control gate is what stops a near-baseline predictor from being mislabelled latent-state equivalence.",
       contradicts=["THY-2026-0005"], limitations=["'contradicts' the universal direct-affine reading only; the task-level reading survives."])

pacc(5, "EXP-2026-0012", "PACC-Lab v0.5 — does a richer relation state rescue the latent coordinate?", "PACC-Lab v0.5——更豐富的關係狀態能救回潛在座標嗎？",
     "A rich relation graph keeps far more source/pair/pattern information than the compact v0.4 bundle while leaving task actions identical. It does not rescue the frozen direct affine-sigmoid map to the common-cause coordinate: compact 0 and rich 0 robust passes, real/control ratios ≈ 0.96–1.02, and no system rescued in four secondary seeds. Counterfactual source-flip probes often pass alone, showing partial local directional alignment without a globally discriminative coordinate.",
     "豐富的關係圖比 v0.4 的精簡 bundle 保留多得多的來源／成對／模式資訊，且任務行動完全相同。它救不回凍結的 direct affine-sigmoid 到共同因座標的映射：精簡 0、豐富 0 次穩健通過，真實／控制比 ≈ 0.96–1.02，四個次要 seed 也沒有任何系統被救回。反事實來源翻轉探針常單獨通過，顯示局部方向對齊部分存在，但沒有全域可判別的座標。",
     "NEGATIVE", seeds=["20260909", "4 secondary seeds"],
     hypothesis="The v0.4 failure was information loss in the compact state; a richer non-probabilistic relation state admits the direct low-complexity latent coordinate.",
     metrics={"verdict": "RICH_STATE_DOES_NOT_RESCUE_LATENT_DEPENDENCE_COORDINATE", "compact_robust_pass": 0, "rich_robust_pass": 0, "task_action_invariance": True,
              "moderate_N0": {"compact_dependence_js": 0.06050, "rich_dependence_js": 0.06146, "real_over_control": 0.999}},
     interpretation="Richer raw relation state is insufficient for the tested direct low-complexity latent coordinate — not that the coordinate is information-theoretically unrecoverable. Points to a coordinate-composition problem (v0.6).",
     limitations=["A direct affine-sigmoid observer may be too restrictive even when the raw state is informative."])

pacc(6, "EXP-2026-0013", "PACC-Lab v0.6 — hierarchical composed coordinate", "PACC-Lab v0.6——階層式組合座標",
     "A preregistered 95-dimensional composed coordinate — the validated task-state map's held-out decision quotient combined with the current relation pattern and a bounded set of interaction terms — predicts the Bayesian common-cause coordinate for all four families in both geometries: composed latent JS 0.0034–0.0073 versus 0.040–0.062 for shuffled/constant and 0.040–0.060 for a deliberately broken composition; counterfactual JS 0.0018–0.0047; four secondary seeds give direct 0.0 and composed 1.0 pass rates.",
     "一個預登記的 95 維組合座標——已驗證任務狀態映射的 held-out 決策商，結合當前關係模式與有界的交互項——在兩種幾何下對四個家族都預測出 Bayesian 共同因座標：組合潛在 JS 0.0034–0.0073，shuffled／constant 為 0.040–0.062，刻意弄壞的組合為 0.040–0.060；反事實 JS 0.0018–0.0047；四個次要 seed 下 direct 通過率 0.0、composed 1.0。",
     "POSITIVE", seeds=["20260909", "4 secondary seeds"],
     hypothesis="The latent probability coordinate is compositional relative to the non-probabilistic state: decision quotient + relation pattern, not the raw state, maps to the common-cause posterior.",
     metrics={"verdict": "HIERARCHICAL_COMPOSED_COORDINATE_RESCUES_LATENT_DEPENDENCE", "direct_robust": "0/4", "composed_robust": "4/4",
              "moderate_N0": {"composed_latent_js": 0.003603, "best_control": 0.061508, "broken_composition": 0.058196, "counterfactual": 0.002780},
              "high_N0": {"composed_latent_js": 0.003335, "best_control": 0.039730, "broken_composition": 0.041238}},
     interpretation="Destroying the train alignment between task quotient and relation pattern destroys most of the signal, so the rescue is not a snapshot fit. Reinterprets v0.5: the information was present; adding raw coordinates did not make the latent state a direct coordinate.",
     limitations=["Does not show all non-probabilistic states admit such a composition, that the coordinate transfers between geometries without refitting, or that clusters can be discovered unsupervised."])
result("RST-2026-0009", "EXP-2026-0013", "v0.6: composed coordinate 4/4, direct 0/4", "v0.6：組合座標 4/4、直接映射 0/4",
       "Composed latent JS ≪ shuffled/constant and ≪ broken composition for every family and geometry (e.g. 0.003603 vs 0.061508 vs 0.058196, moderate N0).",
       "每個家族與幾何下組合潛在 JS 都 ≪ shuffled／constant 且 ≪ 弄壞的組合（例如中相關 N0：0.003603 vs 0.061508 vs 0.058196）。",
       "POSITIVE", metrics={"composed_pass": "4/4", "direct_pass": "0/4"},
       interpretation="The latent probability coordinate is hierarchical/compositional relative to these non-probabilistic states rather than directly affine in the raw canonical state.",
       supports=["THY-2026-0005"])

pacc(7, "EXP-2026-0014", "PACC-Lab v0.7 — cross-geometry coordinate transfer without refitting", "PACC-Lab v0.7——不重新擬合的跨幾何座標轉移",
     "The v0.6 composed coordinate is frozen on one dependence geometry and applied to the other. N0/N1/N3 transfer bidirectionally on the primary protocol and 4/4 secondary seeds; N2 passes high → moderate but misses the moderate → high task-quotient gate by ≈ 0.0003 on the primary seed (2/4 secondary), while a targeted larger stress passes 3/3. Every target-local refit passes, so N2's failure is not a target-chart failure.",
     "把 v0.6 的組合座標凍結在一種依賴幾何上、套用到另一種。N0/N1/N3 在主要協定與 4/4 次要 seed 下雙向轉移；N2 高 → 中通過，但中 → 高在主要 seed 下以 ≈ 0.0003 之差未達任務商門檻（次要 2/4），而針對性的較大規模壓力測試 3/3 通過。所有目標本地重擬合都通過，因此 N2 的失敗不是目標 chart 的失敗。",
     "MIXED", seeds=["20260909", "4 secondary seeds", "3 targeted N2 seeds at 120 episodes × 20 steps"],
     hypothesis="The composed coordinate is one geometry-invariant coordinate rather than a family of per-geometry local charts.",
     metrics={"verdict": "PARTIAL_CROSS_GEOMETRY_TRANSFER", "moderate_to_high": {"N0": {"task_js": 0.03204, "latent_js": 0.01767, "pass": True}, "N2": {"task_js": 0.05030, "latent_js": 0.02716, "pass": False}, "N3": {"task_js": 0.03699, "pass": True}},
              "high_to_moderate": {"N0": {"task_js": 0.02993, "pass": True}, "N2": {"task_js": 0.03237, "pass": True}}, "secondary": {"N0_N1_N3": "4/4 both directions", "N2": "4/4 high→moderate, 2/4 moderate→high"}},
     interpretation="A shared cross-geometry coordinate with family-specific basin boundaries — neither universal invariance nor separate local charts.",
     limitations=["Not established: a universal geometry-invariant coordinate, transfer across a continuous dependence range, transfer to unseen cluster topology."])

pacc(8, "EXP-2026-0015", "PACC-Lab v0.8 — frozen-coordinate transfer basins over a correlation sweep", "PACC-Lab v0.8——相關度掃描下的凍結座標轉移吸引域",
     "One composed coordinate fitted at q* = 0.20 is applied unchanged across a nine-point sweep q ∈ {0.06 … 0.42} (within-cluster correctness correlation rising from ≈ 0.203 to ≈ 0.502). N0/N1/N3 pass through q = 0.33 and fail from 0.36; N2 passes through 0.30 and fails from 0.33. At the edge the negative-control discrimination margin is lost first while absolute latent error stays small; target-local refit passes 9/9 everywhere. Four secondary seeds reproduce the basin exactly for N0/N1/N3 and a seed-sensitive N2 edge at 0.33.",
     "在 q* = 0.20 擬合的一個組合座標，原封不動地套用到九點掃描 q ∈ {0.06 … 0.42}（叢集內正確性相關從 ≈ 0.203 升到 ≈ 0.502）。N0/N1/N3 通過到 q = 0.33、從 0.36 起失敗；N2 通過到 0.30、從 0.33 起失敗。在邊緣先失去的是負控制判別餘裕，而絕對潛在誤差仍小；目標本地重擬合處處 9/9 通過。四個次要 seed 對 N0/N1/N3 精確重現吸引域，N2 在 0.33 的邊緣對 seed 敏感。",
     "MIXED", seeds=["20260909", "4 secondary seeds"],
     hypothesis="A frozen probability-like coordinate has a finite transfer basin whose width depends on the family.",
     metrics={"verdict": "FAMILY_SPECIFIC_TRANSFER_BASINS", "basins_grid": {"N0_N1_N3": "[0.06, 0.33]", "N2": "[0.06, 0.30]"}, "pass_fraction": {"N0": "7/9", "N2": "6/9", "N3": "7/9"}, "local_refit": "9/9",
              "edge_N0_q0.36": {"task_js": 0.0488, "latent_js": 0.0274, "real_over_control": 0.858, "fails": "negative-control discrimination"}},
     interpretation="An atlas/basin picture: large regions share one low-complexity coordinate; different internal dynamics meet transfer boundaries at different places. High-q failure is not evidence that probability-like coordinates cease to exist there.",
     limitations=["Grid points only, not continuous coverage; no single global coordinate over all dependence strengths."])
result("RST-2026-0010", "EXP-2026-0015", "v0.8 basin map", "v0.8 吸引域圖",
       "Frozen chart fitted at q* = 0.20: N0/N1/N3 pass on {0.06 … 0.33}, N2 on {0.06 … 0.30}; first failing gate at the edge is negative-control discrimination (ratio ≈ 0.858 at q = 0.36 for N0/N1); local refit 9/9.",
       "在 q* = 0.20 擬合的凍結 chart：N0/N1/N3 在 {0.06 … 0.33} 通過、N2 在 {0.06 … 0.30}；邊緣最先失敗的門檻是負控制判別（N0/N1 在 q = 0.36 比值 ≈ 0.858）；本地重擬合 9/9。",
       "MIXED", metrics={"N0_N1_N3_first_fail_q": 0.36, "N2_first_fail_q": 0.33},
       interpretation="Shared composed coordinate + family-specific finite basins.", qualifies=["THY-2026-0005"])

pacc(9, "EXP-2026-0016", "PACC-Lab v0.9 — a three-anchor probability-coordinate atlas", "PACC-Lab v0.9——三錨點概率座標圖冊",
     "Three preregistered charts at q = 0.12, 0.24, 0.36 give every family the same union {0.06 … 0.36}: 8/9 sweep coverage, stable across three secondary seeds, never covering q = 0.42. Nearest charts (0.12/0.24) agree directly; distant charts (0.12/0.36) do not (task JS ≈ 0.071–0.082), yet low-complexity transition maps calibrated on an independent seed pass 5/6 directions per family on the primary protocol — the weak direction is 0.36 → 0.12 (latent JS ≈ 0.017–0.021 > 0.01). Transition coherence is not robust across secondary seeds (mean pass ≈ 0.53–0.67).",
     "在 q = 0.12、0.24、0.36 的三個預登記 chart 給每個家族相同的聯集 {0.06 … 0.36}：掃描覆蓋 8/9，三個次要 seed 下穩定，永遠蓋不到 q = 0.42。最近的 chart（0.12/0.24）直接一致；相距遠的（0.12/0.36）不一致（任務 JS ≈ 0.071–0.082），但在獨立 seed 上校準的低複雜度轉換映射在主要協定下每個家族 6 個方向通過 5 個——弱方向是 0.36 → 0.12（潛在 JS ≈ 0.017–0.021 > 0.01）。轉換一致性在次要 seed 下不穩健（平均通過 ≈ 0.53–0.67）。",
     "MIXED", seeds=["20260909", "independent calibration seed", "3 secondary seeds"],
     hypothesis="A small multi-anchor atlas covers the sweep and its charts are mutually translatable by low-complexity transitions.",
     metrics={"verdict": "PARTIAL_MULTI_ANCHOR_ATLAS", "coverage": "8/9", "uncovered_q": 0.42, "transition_pass_primary": "5/6 per family", "weak_direction": "0.36→0.12",
              "secondary_transition_pass_rate": {"N0_N1": 0.667, "N2": 0.528, "N3": 0.583}},
     interpretation="Rejects both extremes — one global chart (finite coverage) and unrelated local charts (overlaps translate cheaply) — leaving partially overlapping probability-like charts with finite coverage and nonuniform transition coherence.",
     limitations=["Full atlas coverage, robust transition coherence, cocycle consistency and manifold structure not established."])

pacc(10, "EXP-2026-0017", "PACC-Lab v0.10 — oriented cocycle coherence on frozen triple overlap", "PACC-Lab v0.10——凍結三重重疊上的定向 cocycle 一致性",
     "On the frozen region where charts A, B and C were all valid in the v0.9 atlas, the direct transition A → C and the composed A → B → C agree to ≈ 10⁻⁵ in latent JS (shuffled-pair control ≈ 10⁻¹), while both paths separately stay accurate to chart C (latent JS ≈ 0.0045–0.0054). All four families pass on the primary seed and on four secondary seeds. N2 has only one triple-overlap geometry (q = 0.24), so its witness is narrower.",
     "在 v0.9 圖冊中 A、B、C 三個 chart 都有效的凍結區域上，直接轉換 A → C 與組合 A → B → C 在潛在 JS 上一致到 ≈ 10⁻⁵（shuffled-pair 控制 ≈ 10⁻¹），且兩條路徑各自對 chart C 都準確（潛在 JS ≈ 0.0045–0.0054）。四個家族在主要 seed 與四個次要 seed 下都通過。N2 只有一個三重重疊幾何（q = 0.24），見證較窄。",
     "POSITIVE", seeds=["20260909", "3", "5", "7", "11"],
     hypothesis="T_AC ≈ T_BC ∘ T_AB on held-out triple-overlap data.",
     metrics={"verdict": "ROBUST_ORIENTED_COCYCLE_COHERENCE_ON_FROZEN_TRIPLE_OVERLAP",
              "N0": {"overlap_q": [0.24, 0.30], "direct_vs_composed_latent_js": 3.5e-05, "direct_to_C": 0.004460, "composed_to_C": 0.004627, "real_over_shuffled": 0.000346},
              "N3": {"overlap_q": [0.20, 0.24, 0.30], "direct_vs_composed_latent_js": 2.65e-05}, "secondary_pass_rate": 1.0},
     interpretation="Pairwise transition quality may be uneven globally while cocycle composition is highly coherent locally on triple overlap — consistent with coordinate compatibility being a local overlap property. Too early for a coordinate groupoid or manifold.",
     limitations=["Evidence volume differs by family; N2's triple overlap is a single geometry."])
result("RST-2026-0011", "EXP-2026-0017", "v0.10 cocycle: path disagreement ≈ 10⁻⁵ vs control ≈ 10⁻¹", "v0.10 cocycle：路徑分歧 ≈ 10⁻⁵ vs 控制 ≈ 10⁻¹",
       "Direct-vs-composed latent JS 3.5×10⁻⁵ (N0/N1), 4.0×10⁻⁵ (N2), 2.7×10⁻⁵ (N3); real/shuffled ratio ≈ 3×10⁻⁴; both paths accurate to chart C.",
       "直接 vs 組合的潛在 JS：3.5×10⁻⁵（N0/N1）、4.0×10⁻⁵（N2）、2.7×10⁻⁵（N3）；真實／shuffled 比 ≈ 3×10⁻⁴；兩條路徑對 chart C 都準確。",
       "POSITIVE", metrics={"families_pass": "4/4", "secondary_pass_rate": 1.0},
       interpretation="Forward cocycle coherence is robust where three charts overlap.", supports=["THY-2026-0005"])

pacc(11, "EXP-2026-0018", "PACC-Lab v0.11 — bidirectional cocycle and inverse consistency", "PACC-Lab v0.11——雙向 cocycle 與反向一致性",
     "Separates three properties: forward cocycle composition (survives, all families), round-trip inverse consistency (all pairwise round trips pass on the primary run, recover 3/3 at larger scale, but are sample-sensitive at small scale, weakest on the widest pair AC), and reverse transport fidelity to the destination chart (fails for every family: direct C → A latent fidelity 0.0116–0.0148 > 0.01 while direct and composed reverse paths agree to ≈ 10⁻⁵).",
     "區分三個性質：正向 cocycle 組合（所有家族都存活）、往返反向一致性（主要 run 所有成對往返都通過，在較大規模 3/3 恢復，但小規模下對樣本敏感，最寬的 AC 對最弱），以及反向傳輸對目的 chart 的保真度（所有家族都失敗：直接 C → A 潛在保真度 0.0116–0.0148 > 0.01，而直接與組合反向路徑彼此一致到 ≈ 10⁻⁵）。",
     "MIXED", seeds=["20260909", "4 secondary seeds", "3 primary-scale-ish seeds"],
     hypothesis="The local transitions form a groupoid: forward cocycle, inverse consistency and reverse destination fidelity all hold.",
     metrics={"verdict": "PARTIAL BIDIRECTIONAL COHERENCE WITH REVERSE DESTINATION BIAS", "forward_cocycle": "PASS all families", "inverse_pairs_primary": "PASS all", "inverse_pairs_large_scale": "3/3",
              "reverse_fidelity": {"N0": 0.01162, "N2": 0.01476, "N3": 0.01355, "gate": 0.01}, "reverse_direct_vs_composed_latent_js": "7e-05 to 1e-04", "reverse_pass_rate": "0/4 and 0/3"},
     interpretation="RoundTripInvertibility ⇏ DestinationChartFidelity and PathCoherence ⇏ GroupoidClosure: a directionally coherent calibration structure with a persistent reverse latent bias, not a closed local groupoid under the affine transition class.",
     limitations=["Does not establish nonlinear-transition impossibility, manifold structure or full atlas coverage."])
result("RST-2026-0012", "EXP-2026-0018", "v0.11 reverse destination bias", "v0.11 反向目的偏差",
       "Reverse paths agree with each other (latent JS ≈ 10⁻⁵) but both land ≈ 0.011–0.015 from the true chart-A coordinate, above the 0.01 gate, for every family and at every scale tested.",
       "反向路徑彼此一致（潛在 JS ≈ 10⁻⁵），但兩者都落在離真正 chart-A 座標 ≈ 0.011–0.015 處，高於 0.01 門檻，所有家族、所有測試規模皆然。",
       "MIXED", metrics={"reverse_pass": "0/4 primary+secondary, 0/3 large", "path_coherence": "≈1e-5"},
       interpretation="Path coherence is not enough for atlas closure; the bias is the object v0.12–v0.13 then tried to explain.", qualifies=["THY-2026-0005"])

pacc(12, "EXP-2026-0019", "PACC-Lab v0.12 — bounded quadratic transition", "PACC-Lab v0.12——有界二次轉換",
     "Transition capacity rises in one preregistered step from 20 affine to 60 fixed degree-2 coefficients with charts, support, split, controls and thresholds unchanged. No family is rescued: reverse fidelity 0.0111 (N0/N1), 0.0139 (N2), 0.0141 (N3) versus the 0.01 gate, 0/4 secondary and 0/3 at larger scale; forward cocycle and inverse consistency survive the quadratic class. The lab stops here rather than escalating to cubic, quartic or neural transitions after seeing the result.",
     "轉換容量以一個預登記的步驟從 20 個仿射係數升到 60 個固定二次係數，chart、支撐、切分、控制與門檻不變。沒有家族被救回：反向保真度 0.0111（N0/N1）、0.0139（N2）、0.0141（N3），門檻 0.01，次要 0/4、較大規模 0/3；正向 cocycle 與反向一致性在二次類下存活。實驗室在此停止，而不是看到結果後升級到三次、四次或神經轉換。",
     "NEGATIVE", seeds=["20260909", "3", "5", "7", "11", "3 primary-scale-ish seeds"],
     hypothesis="The reverse destination bias is an artefact of the 4-D affine transition class.",
     metrics={"verdict": "REVERSE BIAS PERSISTS UNDER BOUNDED QUADRATIC", "quadratic_reverse_fidelity": {"N0": 0.01108, "N2": 0.01392, "N3": 0.01410}, "gate": 0.01, "quadratic_reverse_pass": "0/4 and 0/3", "forward_cocycle": "PASS", "inverse_pairs": "PASS (N2 2/3 at scale)"},
     interpretation="Rejects the affine-limitation explanation and strengthens a persistent directional/base-point mismatch as the next hypothesis. A sufficiently flexible approximator could fit any finite sample, which is exactly why capacity was bounded in advance.",
     limitations=["Does not prove that no nonlinear transition can remove the bias."])

pacc(13, "EXP-2026-0020", "PACC-Lab v0.13 — reverse residual field / base-point dependence", "PACC-Lab v0.13——反向殘差場／基點依賴",
     "The held-out reverse residual r_CA(S) = Φ_A(S) − T_CA(Φ_C(S)) is measured for mean, covariance, latent-logit energy concentration, between- versus within-stratum variance, direction stability and a train-only per-stratum constant correction against global and shuffled-stratum controls. N0/N1 concentrate 98 % of residual energy on the latent-logit axis, yet the mean direction flips sign across seeds (cross-seed cosine ≈ −1), between-q structure is ≈ 0.1–0.3 % against a 20 % gate, and stratum correction changes held-out fidelity by < 10⁻⁵ — no family passes.",
     "量測 held-out 反向殘差 r_CA(S) = Φ_A(S) − T_CA(Φ_C(S)) 的均值、共變異、潛在 logit 能量集中度、層間 vs 層內變異、方向穩定性，以及只用訓練集的逐層常數校正（對照全域與 shuffled 層控制）。N0/N1 把 98 % 的殘差能量集中在潛在 logit 軸上，但均值方向跨 seed 翻號（跨 seed 餘弦 ≈ −1），層間結構只有 ≈ 0.1–0.3 %（門檻 20 %），逐層校正對 held-out 保真度的改變 < 10⁻⁵——沒有家族通過。",
     "NEGATIVE", seeds=["20260909", "4 secondary seeds", "3 primary-scale-ish seeds"],
     hypothesis="The reverse bias is a base-point-conditioned residual field r(S) ≈ b_q + ε learnable per frozen overlap stratum.",
     metrics={"verdict": "RESIDUAL MOSTLY UNSTRUCTURED", "latent_energy_fraction_affine": {"N0": 0.9845, "N2": 0.7723, "N3": 0.3182}, "between_q_fraction": "0.0012–0.0033 vs gate 0.20",
              "stratum_correction": {"N0_uncorrected": 0.011616, "N0_corrected": 0.011624}, "cross_family_direction_cosine_median": 0.7024, "cross_seed_direction_cosine_N0": -0.9977, "base_point_pass": "0 for every family"},
     interpretation="A stable residual axis is not a stable residual orientation and not a base-point field; the reverse bias contains family-dependent dominant error modes, which weakens the gauge/connection-like reading. Next (v0.14, preregistered): sign-free residual subspace / principal-axis stability, with no q input, no higher degree, no neural mapper.",
     limitations=["Residual unstructuredness is not established in every sign-free or subspace sense — that is the v0.14 question."])

# ---- PACC-LLM Hybrid ------------------------------------------------------------
obj("EXP-2026-0021", "experiment", "PACC-Hybrid v0.1 — synthetic A/B/C architecture witness", "PACC-Hybrid v0.1——合成 A/B/C 架構見證",
    "Over 1,568 identical candidate pools, generator-only (A), hard verifier (B) and PACC runtime (C) are scored on hard adherence, derived coherence, soft-intent satisfaction, long-horizon retention, novelty and pattern entropy. B already saturates literal hard adherence (1.0); C adds derived coherence +0.2085, long-horizon retention +0.0142 and valid novelty +0.1964 over B, loses 0.0076 soft-intent satisfaction, and in the pure-creative control raises pointwise novelty (0.9864 vs 0.8889) while collapsing pattern entropy (0.2284 vs 0.7199). A post-hoc 'elastic' exploration policy (D) restores entropy to 0.7638 with derived coherence still 1.0. Zero real LLM calls; eight seeds sign-stable.",
    "在 1,568 個完全相同的候選池上，純生成器（A）、硬驗證器（B）、PACC runtime（C）以硬約束遵守、衍生一致性、軟意圖滿足、長程保持、新穎度與 pattern entropy 計分。B 已經把字面硬約束遵守飽和到 1.0；C 相對 B 衍生一致性 +0.2085、長程保持 +0.0142、有效新穎度 +0.1964、軟意圖滿足 −0.0076，並在純創意控制組中提高逐點新穎度（0.9864 vs 0.8889）卻讓 pattern entropy 塌縮（0.2284 vs 0.7199）。事後的「elastic」探索策略（D）在衍生一致性仍為 1.0 下把 entropy 恢復到 0.7638。零次真實 LLM 呼叫；八個 seed 符號穩定。",
    "STABLE", "E3", created=mtime(HZ[1]), domain="Reasoning", domains=["Evaluation"],
    eml_hypothesis="A PACC-style commit space changes selection quality beyond what a hard verifier achieves, and any creative-breadth loss is separable from the commit constraints.",
    eml_metrics={"verdict": "SYNTHETIC_PARETO_WITNESS_REASONING_UP_BREADTH_COLLAPSE_MITIGATABLE", "scale": "7 categories × 28 tasks × 8 pools × 112 candidates; 1568 pool instances; 0 LLM calls",
                 "overall": {"A": {"hard": 0.9936, "derived": 0.7902, "soft": 0.7878, "long_horizon": 0.9648, "valid_novelty": 0.5487}, "B": {"hard": 1.0, "derived": 0.7915, "soft": 0.7859, "long_horizon": 0.9676, "valid_novelty": 0.5510}, "C": {"hard": 1.0, "derived": 1.0, "soft": 0.7783, "long_horizon": 0.9818, "valid_novelty": 0.7474}},
                 "pure_creative": {"A": {"raw_novelty": 0.8889, "pattern_entropy": 0.7199}, "C": {"raw_novelty": 0.9864, "pattern_entropy": 0.2284}, "D_elastic_posthoc": {"raw_novelty": 0.9225, "pattern_entropy": 0.7638}},
                 "eight_seed_deltas": {"C_minus_B_derived": {"mean": 0.1865, "sign": "8/8 positive"}, "C_minus_A_pattern_entropy": {"mean": -0.3894, "sign": "8/8 negative"}}, "B_literal_fallback_rate": 0.286},
    eml_interpretation="Not a simple reasoning-up / imagination-down trade-off: coherence and valid novelty rise, soft-preference fit dips slightly, and the breadth tax is a selection-policy effect that separating exploration from commitment recovers. The elastic diagnostic is post-hoc and not part of the primary result.",
    eml_limitations=["Controlled synthetic witness only; does not demonstrate that a frontier LLM shows the same effect."],
    eml_controls=["identical candidate pools for A/B/C", "pure-creative negative control", "post-hoc elastic diagnostic labelled as such"],
    eml_random_seeds=["20260909", "8 fixed secondary seeds"], eml_run_count=9, eml_result_type="MIXED",
    eml_software_environment="Python; synthetic generators and scorers; no network, no LLM.",
    eml_reproduction_instructions="Extract PACC-Hybrid-Lab_v0.1_SYNTHETIC_FINAL.zip; python -m pytest -q; results in results/*.json and docs/PACC_HYBRID_v0.1_RESULTS.md.",
    eml_completed_at=mtime(HZ[1]), eml_data_basis="SYNTHETIC", eml_dataset_ids=["DAT-2026-0002"], eml_benchmark_ids=["BEN-2026-0003"])
for p, t in (("runs_on", "SYS-2026-0003"), ("uses_benchmark", "BEN-2026-0003"), ("uses_dataset", "DAT-2026-0002"), ("tests", "THY-2026-0002")):
    rel("EXP-2026-0021", p, t)
rel("EXP-2026-0021", "produced", artifact(HZ[1], kind="release-bundle", label=HZ[1]))
result("RST-2026-0013", "EXP-2026-0021", "Hybrid v0.1 A/B/C deltas", "Hybrid v0.1 A/B/C 差值",
       "C − B: derived coherence +0.2085, long-horizon retention +0.0142, valid novelty +0.1964, soft-intent −0.0076; C − A pattern entropy −0.4915 (pure creative), recovered to 0.7638 by post-hoc elastic selection.",
       "C − B：衍生一致性 +0.2085、長程保持 +0.0142、有效新穎度 +0.1964、軟意圖 −0.0076；C − A pattern entropy −0.4915（純創意），事後 elastic 選擇恢復到 0.7638。",
       "MIXED", metrics={"derived_delta_C_B": 0.2085, "valid_novelty_delta_C_B": 0.1964, "soft_delta_C_B": -0.0076, "entropy_delta_C_A": -0.4915, "elastic_entropy": 0.7638},
       interpretation="Gains come from derived dependency coherence and constraint-satisfying novelty, not from more rejection; the breadth cost is mitigable without relaxing commit constraints.",
       supports=["THY-2026-0002"], limitations=["Synthetic scoring; a real-model result is required before any claim about language models."])

obj("EXP-2026-0022", "experiment", "PACC-Hybrid v0.2 — real-language-model A/B/C harness (not yet executed)", "PACC-Hybrid v0.2——真實語言模型 A/B/C harness（尚未執行）",
    "Sixteen hand-authored natural-language tasks across the preregistered families; A/B/C share one candidate ledger and equal accounted budgets; C receives no gold constraint or supersession metadata; the gold rubric is visible only to a condition-blind judge; literal machine checks are independent of the judge; identical answers reuse one judge cache key; the system fails closed without OPENAI_API_KEY; a frozen-cache replay provider allows exact replay after a live run. 25 tests pass. The execution runtime had no API key, so no real model output exists; the bundled mock smoke file is marked MOCK_ONLY_NOT_REAL_MODEL.",
    "16 個橫跨預登記家族的手寫自然語言任務；A/B/C 共用一本候選帳本與相同計費預算；C 拿不到 gold 約束或 supersession metadata；gold rubric 只有對條件盲的評審看得到；字面機器檢查獨立於評審；相同答案重用同一個評審快取鍵；沒有 OPENAI_API_KEY 時 fail-closed；凍結快取重播提供者讓 live run 後可精確重播。25 個測試通過。執行環境沒有 API key，因此不存在任何真實模型輸出；隨附的 mock smoke 檔標為 MOCK_ONLY_NOT_REAL_MODEL。",
    "ACTIVE", "E1", created=mtime(HZ[2]), domain="Reasoning", domains=["Evaluation"],
    eml_hypothesis="A real language model under the PACC runtime shows the coherence / valid-novelty gains and recoverable breadth loss seen in the synthetic witness.",
    eml_metrics={"verdict": "REAL_LLM_HARNESS_VALIDATED_BUT_REAL_MODEL_NOT_EXECUTED", "execution_status": "NOT_EXECUTED_REAL_MODEL", "tests_passed": 25, "tasks": 16, "real_llm_calls": 0},
    eml_interpretation="Closes the harness, not the scientific question. Next action: a small real smoke (6 tasks × 2 repetitions × 3 candidates), freeze the cache, inspect blind-evaluator consistency, then the full 16-task primary without changing prompts or metrics.",
    eml_limitations=["No claim about real-model reasoning, intent understanding, imagination, human-rated usefulness, cross-model transfer or hallucination is permitted before a real-model result exists.", "A single-model judge is not human evaluation even after a live run."],
    eml_random_seeds=[], eml_run_count=0, eml_result_type="INCONCLUSIVE",
    eml_software_environment="Python; OpenAI API provider (fails closed without key); deterministic fake provider for protocol tests only.",
    eml_reproduction_instructions="Extract PACC-Hybrid-Lab_v0.2_REAL_LLM_HARNESS_FINAL.zip; python -m pytest -q (25 tests); set OPENAI_API_KEY and run the smoke per docs/REPRODUCIBILITY_v0.2.md.",
    eml_data_basis="NOT RUN", eml_benchmark_ids=["BEN-2026-0003"])
for p, t in (("runs_on", "SYS-2026-0003"), ("uses_benchmark", "BEN-2026-0003"), ("extends", "EXP-2026-0021"), ("tests", "THY-2026-0002")):
    rel("EXP-2026-0022", p, t)
rel("EXP-2026-0022", "produced", artifact(HZ[2], kind="release-bundle", label=HZ[2]))

# ---- real local-model run of the v0.2 protocol (Neo.K's authorization, 2026-09-11) ----
# Every number below is read from the run's own result JSON inside the bundle;
# only the interpretation strings are written by hand, after the run.
import json as _json  # noqa: E402
from aes_common import SRC, zip_member  # noqa: E402

REAL_ZIP = "PACC-Hybrid-Lab_v0.2_REAL_LOCAL_LLM_RUN_Qwythos-9B-v2_2026-09-11.zip"
REAL_INTERPRETATION = {
    "result_type": "MIXED",
    "verdict": "REAL_LOCAL_9B_MIXED: supersession and repair up, coherence flat, valid novelty slightly down, breadth unmeasurable at two repetitions",
    "summary": "The v0.2 protocol executed for the first time on a real language model — a local open-weight 9B (Qwythos-9B-v2, Q4_K_M, Ollama, thinking off) as generator, selector and judge; 16 tasks × 2 repetitions × 4 candidates, 380 calls, 32 rows per condition. The PACC runtime (C) gains on supersession alignment (+0.031 vs B, +0.097 vs A) and repair success (+0.070 / +0.094), the two axes the canonical-intent compilation step exists for; derived coherence (+0.011) and intent persistence (−0.002) do not move; valid novelty is slightly lower (−0.045 vs B). Most per-task pairs are ties because the 9B judge saturates near 1.0, and with two repetitions per task the judge's free-text pattern labels never repeat, so creative breadth is not measurable. The conditions chose different candidates in 69 % of task × repetition pairs.",
    "summary_zh": "v0.2 協定第一次在真實語言模型上執行——本地開放權重 9B（Qwythos-9B-v2、Q4_K_M、Ollama、關閉思考）同時當生成器、選擇器與評審；16 題 × 2 次 × 4 候選，380 次呼叫，每條件 32 筆。PACC runtime（C）在 supersession 對齊（相對 B +0.031、相對 A +0.097）與修復成功率（+0.070／+0.094）上升——正是 canonical intent 編譯步驟存在的那兩個軸；衍生一致性（+0.011）與意圖持續（−0.002）沒有動；有效新穎度略低（相對 B −0.045）。多數逐題配對是平手，因為 9B 評審在接近 1.0 處飽和；每題只重複兩次，評審的自由文字 pattern 標籤從不重複，所以創造廣度量不出來。三個條件在 69 % 的題 × 次配對中選了不同的候選。",
    "interpretation": "Against the v0.2 predeclared interpretation: the predicted coherence and intent-persistence gains over B are not observed; raw novelty did not decrease (semantic novelty +0.017 vs B); the predicted breadth collapse cannot be tested at this repetition count. What did appear — governance gains on supersession and repair with a valid-novelty cost concentrated in multi_constraint and repair tasks — is mechanism-consistent but small, untested statistically, and runs opposite to the synthetic v0.1 valid-novelty picture (+0.196 there). One model, one run, one same-model judge: a first real data point, not a verdict on the architecture.",
    "interpretation_zh": "對照 v0.2 預先宣告的解讀：預測中 C 相對 B 在一致性與意圖持續上的增益沒有出現；原始新穎度沒有下降（語義新穎度相對 B +0.017）；預測的廣度塌縮在這個重複次數下無法檢驗。真正出現的——supersession 與修復上的治理增益，以及集中在 multi_constraint 與 repair 題的有效新穎度代價——與機制一致但很小、未做統計檢定，而且與合成 v0.1 的有效新穎度圖像（那裡是 +0.196）方向相反。一個模型、一次執行、同一個模型當評審：這是第一個真實數據點，不是對架構的判決。",
    "supports": [], "contradicts": [], "qualifies": ["THY-2026-0002"],
}
if (SRC / REAL_ZIP).exists():
    assert REAL_INTERPRETATION["result_type"], "fill REAL_INTERPRETATION before extracting the real run"
    P = _json.loads(zip_member(REAL_ZIP, "results/pacc_hybrid_v0.2_real_local_primary.json").decode("utf-8"))
    S = _json.loads(zip_member(REAL_ZIP, "results/summary_primary.json").decode("utf-8"))
    lr, proto = P["local_run"], P["protocol"]
    A = ("A_llm_only", "B_hard_verifier", "C_pacc_runtime")
    keys = ("hard_adherence", "derived_coherence", "intent_persistence", "supersession_alignment",
            "repair_success", "usefulness", "semantic_novelty", "valid_novelty", "literal_check_mean",
            "within_task_pattern_entropy_mean")
    overall = {a: {k: round(P["architectures"][a]["overall"][k], 4) for k in keys} for a in A}
    deltas = {d: {k: round(v, 4) for k, v in S["deltas"][d].items() if k in keys} for d in ("C-B", "C-A", "B-A")}
    details = lr.get("model_details") or {}
    obj("MOD-2026-0006", "model", "Qwythos-9B-v2 (Q4_K_M, local, Ollama)", "Qwythos-9B-v2（Q4_K_M，本地，Ollama）",
        f"Open-weight {details.get('parameter_size', '8.95B')} model of the {details.get('family', 'qwen35')} family, GGUF Q4_K_M, served locally by Ollama {lr.get('ollama_version', '')} on an RTX 3070. Used as generator, selector and judge in the real local run of the PACC-Hybrid v0.2 protocol, with thinking disabled.",
        f"{details.get('family', 'qwen35')} 系的開放權重 {details.get('parameter_size', '8.95B')} 模型，GGUF Q4_K_M，由 Ollama {lr.get('ollama_version', '')} 在 RTX 3070 上本地服務。在 PACC-Hybrid v0.2 協定的真實本地執行中同時擔任生成器、選擇器與評審，思考功能關閉。",
        "STABLE", "E2", created="2026-09-11", domain="Evaluation", eml_data_basis="REAL MODEL",
        eml_provider="empero-ai (Hugging Face GGUF) via Ollama", eml_model_version=lr.get("model_digest"),
        eml_access_type="local, loopback only; open weights", eml_context_window=details.get("context_length"),
        eml_configuration_notes=[f"run tag {lr.get('model_tag')} = base hf.co/empero-ai/Qwythos-9B-v2-GGUF:Q4_K_M (digest 5008e78bba127262f3f7ad86425bb49a5e0f47bb1959a4d30bfe17832ec45856) + PARAMETER num_ctx 8192 via scripts/Modelfile.qwythos-ctx8k; Ollama's default 4096 context aborted the first primary attempt after 55 calls",
                                 "reasoning.effort = none (thinking off) for every call", "Ollama /v1/responses, OpenAI-compatible; package provider unchanged"],
        eml_known_behavior_notes=["With thinking enabled, hidden reasoning consumes the protocol's output-token budgets and output_text comes back empty.", "As judge it sometimes returns a rubric sentence as pattern_label, which makes pattern-entropy numbers fragile."],
        eml_canonical_external_reference="https://huggingface.co/empero-ai/Qwythos-9B-v2-GGUF")
    rel("SYS-2026-0003", "uses_model", "MOD-2026-0006")
    obj("EXP-2026-0023", "experiment",
        "PACC-Hybrid v0.2 — first real-model run, on a local 9B open-weight model",
        "PACC-Hybrid v0.2——第一次真實模型執行，本地 9B 開放權重模型",
        REAL_INTERPRETATION["summary"], REAL_INTERPRETATION["summary_zh"],
        "STABLE", "E2", created="2026-09-11", domain="Reasoning", domains=["Evaluation"], eml_data_basis="REAL MODEL",
        eml_hypothesis="A real language model under the PACC runtime shows the coherence / valid-novelty gains and recoverable breadth loss seen in the synthetic witness (v0.2 predeclared interpretation).",
        eml_metrics={"verdict": REAL_INTERPRETATION["verdict"], "execution_status": P["execution_status"],
                     "protocol": {k: proto[k] for k in ("model", "judge_model", "task_count", "repetitions", "candidate_count", "equal_accounted_calls", "architecture_call_counts")},
                     "rows_per_architecture": S["rows_per_architecture"], "overall": overall, "deltas": deltas,
                     "selection_agreement": S["selection_agreement"], "usage": P["usage"], "wall_seconds": lr.get("wall_seconds"),
                     "smoke_run": "6 tasks × 2 × 3 candidates executed first, 128 calls, all outputs parsed; kept in the bundle"},
        eml_interpretation=REAL_INTERPRETATION["interpretation"],
        eml_limitations=["One open-weight 9B model at 4-bit, one run, 32 rows per architecture; no significance or equivalence test — deltas are descriptive.",
                         "Judge = the same 9B model; no human rating, no second judge; pattern labels are noisy, so entropy is fragile.",
                         "Thinking disabled for every call (see docs/REAL_LOCAL_RUN_EVIDENCE_BOUNDARY.md); a thinking-enabled run is a different experiment.",
                         "Says nothing about frontier models."],
        eml_controls=["identical candidate ledger for A/B/C", "equal accounted calls", "condition-blind judge with deduplicated judge calls", "deterministic literal checks"],
        eml_random_seeds=["model nondeterminism, single run; frozen response cache in the bundle for exact replay"], eml_run_count=1,
        eml_result_type=REAL_INTERPRETATION["result_type"],
        eml_procedure="scripts/run_real_local_ollama.py --candidate-count 4 --repetitions 2 (after a 6×2×3 smoke); summary by scripts/summarize_real_local.py; both scripts and both frozen caches are in the bundle.",
        eml_software_environment=f"Python 3.14, openai SDK 3.0.0 against Ollama {lr.get('ollama_version', '')} /v1/responses; PACC-Hybrid-Lab v0.2 package unchanged (25 tests green before the run).",
        eml_reproduction_instructions="Extract the bundle; python -m pytest -q; replay exactly with CachedReplayProvider('.pacc_real_cache_local', reasoning_effort='none'); or rerun scripts/run_real_local_ollama.py against any OpenAI-compatible endpoint serving the same model tag.",
        eml_completed_at="2026-09-11", eml_model_ids=["MOD-2026-0006"], eml_benchmark_ids=["BEN-2026-0003"])
    for p, t in (("runs_on", "SYS-2026-0003"), ("uses_benchmark", "BEN-2026-0003"), ("uses_model", "MOD-2026-0006"),
                 ("extends", "EXP-2026-0022"), ("tests", "THY-2026-0002")):
        rel("EXP-2026-0023", p, t)
    rel("EXP-2026-0023", "produced", artifact(REAL_ZIP, kind="results-bundle", label="PACC-Hybrid v0.2 real local-model run (Qwythos-9B-v2) — results, frozen caches, scripts, docs"))
    result("RST-2026-0014", "EXP-2026-0023", "Real local-model A/B/C table (Qwythos-9B-v2)", "真實本地模型 A/B/C 表（Qwythos-9B-v2）",
           REAL_INTERPRETATION["summary"], REAL_INTERPRETATION["summary_zh"], REAL_INTERPRETATION["result_type"],
           metrics={"overall": overall, "deltas": deltas, "selection_agreement": S["selection_agreement"]},
           interpretation=REAL_INTERPRETATION["interpretation"],
           supports=REAL_INTERPRETATION["supports"], contradicts=REAL_INTERPRETATION["contradicts"], qualifies=REAL_INTERPRETATION["qualifies"],
           limitations=["Descriptive deltas from one local run with a same-model judge."])
    # the harness record is no longer the end of the line
    harness = next(o for o in OBJECTS if o["id"] == "EXP-2026-0022")
    harness["values"]["eml_status"] = "STABLE"
    harness["values"]["eml_limitations"].append("Executed for the first time on 2026-09-11 with a local open-weight model — see EXP-2026-0023.")

# ---- run 2: four repetitions + label-free breadth (same model, thinking off) ----
RUN2_ZIP = "PACC-Hybrid-Lab_v0.2_REAL_LOCAL_LLM_RUN2_reps4_breadth_Qwythos-9B-v2_2026-09-11.zip"
if (SRC / RUN2_ZIP).exists():
    P2 = _json.loads(zip_member(RUN2_ZIP, "results/pacc_hybrid_v0.2_real_local_reps4.json").decode("utf-8"))
    S2 = _json.loads(zip_member(RUN2_ZIP, "results/summary_reps4.json").decode("utf-8"))
    B2 = _json.loads(zip_member(RUN2_ZIP, "results/breadth_reps4.json").decode("utf-8"))
    lr2, proto2 = P2["local_run"], P2["protocol"]
    A = ("A_llm_only", "B_hard_verifier", "C_pacc_runtime")
    keys = ("hard_adherence", "derived_coherence", "intent_persistence", "supersession_alignment",
            "repair_success", "usefulness", "semantic_novelty", "valid_novelty", "literal_check_mean")
    overall2 = {a: {k: round(P2["architectures"][a]["overall"][k], 4) for k in keys} for a in A}
    deltas2 = {d: {k: round(v, 4) for k, v in S2["deltas"][d].items() if k in keys} for d in ("C-B", "C-A", "B-A")}
    breadth2 = {a: {k: B2["summary"][a][k] for k in ("cluster_entropy_mean", "breadth_ratio_mean", "selected_mean_pairwise_distance_mean")} for a in A}
    run2_summary = ("Same model and settings as the first run, repetitions raised from two to four: 16 tasks × 4 × 4 candidates, 754 unique model requests, 64 rows per condition. "
                    f"The PACC runtime (C) shows no reliable advantage on any judge axis — supersession {deltas2['C-B']['supersession_alignment']:+.4f} and repair {deltas2['C-B']['repair_success']:+.4f} vs B, so the first run's gains did not replicate — and sits a few hundredths below A and B on adherence, coherence and intent persistence. "
                    f"A new label-free breadth measure (local nomic-embed-text embeddings, k-means labels over each task's candidate pool) finds no collapse: C's cluster entropy {breadth2['C_pacc_runtime']['cluster_entropy_mean']:.3f} vs A {breadth2['A_llm_only']['cluster_entropy_mean']:.3f} / B {breadth2['B_hard_verifier']['cluster_entropy_mean']:.3f}, breadth ratio {breadth2['C_pacc_runtime']['breadth_ratio_mean']:.3f} vs {breadth2['A_llm_only']['breadth_ratio_mean']:.3f} / {breadth2['B_hard_verifier']['breadth_ratio_mean']:.3f}. "
                    f"Five selector/judge outputs failed strict JSON parsing and were regenerated under a disclosed retry policy.")
    run2_summary_zh = ("與第一次執行相同的模型與設定，重複次數從 2 提高到 4：16 題 × 4 × 4 候選，754 次唯一模型請求，每條件 64 筆。"
                       f"PACC runtime（C）在任何評審軸上都沒有可靠優勢——supersession 相對 B {deltas2['C-B']['supersession_alignment']:+.4f}、修復 {deltas2['C-B']['repair_success']:+.4f}，第一次執行的增益沒有重現——在遵守、一致性與意圖持續上還比 A、B 低幾個百分點。"
                       f"新的標籤無關廣度指標（本地 nomic-embed-text 嵌入、對每題候選池做 k-means 當標籤）沒有發現塌縮：C 的群熵 {breadth2['C_pacc_runtime']['cluster_entropy_mean']:.3f}，A {breadth2['A_llm_only']['cluster_entropy_mean']:.3f}／B {breadth2['B_hard_verifier']['cluster_entropy_mean']:.3f}；廣度比 {breadth2['C_pacc_runtime']['breadth_ratio_mean']:.3f}，對 {breadth2['A_llm_only']['breadth_ratio_mean']:.3f}／{breadth2['B_hard_verifier']['breadth_ratio_mean']:.3f}。"
                       f"五次 selector／judge 輸出未通過嚴格 JSON 解析，依公開的重試政策重新生成。")
    obj("EXP-2026-0024", "experiment",
        "PACC-Hybrid v0.2 — real-model run 2: four repetitions and label-free creative breadth",
        "PACC-Hybrid v0.2——真實模型第二次執行：四次重複與標籤無關的創造廣度",
        run2_summary, run2_summary_zh,
        "STABLE", "E3", created="2026-09-11", domain="Reasoning", domains=["Evaluation"], eml_data_basis="REAL MODEL",
        eml_hypothesis="With enough repetitions, (a) the first run's supersession/repair gains for the PACC runtime replicate, and (b) creative breadth can be measured — and the predeclared breadth collapse under PACC selection appears.",
        eml_metrics={"verdict": "REAL_LOCAL_9B_NO_RELIABLE_DIFFERENCE_BREADTH_NOT_REDUCED", "execution_status": P2["execution_status"],
                     "protocol": {k: proto2[k] for k in ("model", "judge_model", "task_count", "repetitions", "candidate_count", "equal_accounted_calls", "architecture_call_counts")},
                     "rows_per_architecture": S2["rows_per_architecture"], "overall": overall2, "deltas": deltas2,
                     "selection_agreement": S2["selection_agreement"], "breadth_label_free": breadth2,
                     "breadth_method": f"{B2['embed_model']} embeddings; k-means k={B2['k']} over each task's {proto2['repetitions'] * proto2['candidate_count']}-candidate pool; normalized cluster entropy and mean pairwise cosine distance / pool distance",
                     "retries": [r["purpose"] for r in lr2.get("retries", [])], "usage": P2["usage"], "wall_seconds": lr2.get("wall_seconds")},
        eml_interpretation="Two thinking-off runs on the same 9B model (32 and 64 rows per condition) now disagree on the only gains the first run showed, so those gains were run-to-run variation of a same-model judge, not an effect. The predeclared coherence and intent gains are absent in both runs. The predeclared breadth collapse is not observed by either label-free measure — the shipped C selector prompt already instructs against collapsing, so this tests the shipped prompt, not naive commitment. On this model the three runtime conditions are practically equivalent; nothing is statistically tested; frontier models are not addressed.",
        eml_limitations=["Same-model 9B judge, saturating near 1.0; no human rating, no second judge.",
                         "The breadth measure is supplementary and label-free, not the protocol's judge-label entropy (which stays 1.0 because free-text labels never repeat).",
                         "Retry policy: unparseable selector/judge JSON regenerated at most twice per call, never edited; 5 retries recorded.",
                         "Thinking disabled; one model family; no significance or equivalence test."],
        eml_controls=["identical candidate ledger for A/B/C", "equal accounted calls", "condition-blind judge with deduplicated judge calls", "deterministic literal checks", "pool-relative breadth ratio"],
        eml_random_seeds=["model nondeterminism, single run; frozen response cache and embedding cache in the bundle"], eml_run_count=1,
        eml_result_type="NEGATIVE",
        eml_procedure="scripts/run_real_local_ollama.py --model qwythos-9b-v2-q4km-ctx8k --repetitions 4 --candidate-count 4 (resumed once from cache after a malformed judge JSON aborted the first pass at call 398); scripts/summarize_real_local.py; scripts/breadth_metrics.py.",
        eml_software_environment=f"Python 3.14, openai SDK 3.0.0 against Ollama {lr2.get('ollama_version', '')} /v1/responses (flash attention on, q8_0 KV cache for the resumed pass); nomic-embed-text for breadth; harness package unchanged.",
        eml_reproduction_instructions="Extract the bundle; replay exactly with CachedReplayProvider('.pacc_real_cache_local_reps4', reasoning_effort='none'); python scripts/breadth_metrics.py results/pacc_hybrid_v0.2_real_local_reps4.json --cache-dir .pacc_real_cache_local_reps4 (embeddings cached alongside).",
        eml_completed_at="2026-09-11", eml_model_ids=["MOD-2026-0006"], eml_benchmark_ids=["BEN-2026-0003"])
    for p, t in (("runs_on", "SYS-2026-0003"), ("uses_benchmark", "BEN-2026-0003"), ("uses_model", "MOD-2026-0006"),
                 ("extends", "EXP-2026-0023"), ("tests", "THY-2026-0002"), ("replicates", "EXP-2026-0023")):
        rel("EXP-2026-0024", p, t)
    rel("EXP-2026-0024", "produced", artifact(RUN2_ZIP, kind="results-bundle", label="PACC-Hybrid v0.2 real local-model run 2 (4 repetitions, label-free breadth) — results, frozen caches, scripts, docs"))
    result("RST-2026-0015", "EXP-2026-0024", "Run 2: no reliable condition difference; breadth not reduced (64 rows)", "第二次執行：條件間無可靠差異；廣度未縮減（64 筆）",
           f"C vs B: supersession {deltas2['C-B']['supersession_alignment']:+.4f}, repair {deltas2['C-B']['repair_success']:+.4f}, derived coherence {deltas2['C-B']['derived_coherence']:+.4f}, intent {deltas2['C-B']['intent_persistence']:+.4f}, valid novelty {deltas2['C-B']['valid_novelty']:+.4f}; label-free breadth: cluster entropy C {breadth2['C_pacc_runtime']['cluster_entropy_mean']:.3f} / A {breadth2['A_llm_only']['cluster_entropy_mean']:.3f} / B {breadth2['B_hard_verifier']['cluster_entropy_mean']:.3f}.",
           f"C 相對 B：supersession {deltas2['C-B']['supersession_alignment']:+.4f}、修復 {deltas2['C-B']['repair_success']:+.4f}、衍生一致性 {deltas2['C-B']['derived_coherence']:+.4f}、意圖 {deltas2['C-B']['intent_persistence']:+.4f}、有效新穎度 {deltas2['C-B']['valid_novelty']:+.4f}；標籤無關廣度：群熵 C {breadth2['C_pacc_runtime']['cluster_entropy_mean']:.3f}／A {breadth2['A_llm_only']['cluster_entropy_mean']:.3f}／B {breadth2['B_hard_verifier']['cluster_entropy_mean']:.3f}。",
           "NEGATIVE", metrics={"deltas": deltas2, "breadth_label_free": breadth2, "selection_agreement": S2["selection_agreement"]},
           interpretation="The first run's governance gains did not replicate; the three conditions are practically equivalent on this model, and the PACC runtime does not narrow creative breadth.",
           qualifies=["THY-2026-0002"], contradicts=[],
           limitations=["Descriptive; same-model judge; one model family; thinking off."])
    first = next(o for o in OBJECTS if o["id"] == "EXP-2026-0023")
    first["values"]["eml_limitations"].append("Not replicated: the second run with four repetitions (EXP-2026-0024, 64 rows per condition) shows supersession +0.0005 and repair −0.0125 vs B — the run-1 gains were run-to-run variation.")
    line = next(o for o in OBJECTS if o["id"] == "RES-2026-0004")
    line["values"]["eml_claims"].append("Real local 9B model, thinking off, two runs (32 and 64 rows per condition): the three runtime conditions are practically equivalent on every judge axis, and by label-free measures the PACC runtime does not narrow creative breadth. The synthetic v0.1 prediction did not appear on this model.")
