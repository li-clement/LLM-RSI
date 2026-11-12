# Execution 平面：四流水线与五门禁（RSI 适配）

Execution 平面把"这一轮真的变好了吗"变成**可审计证据**。每条流水线有固定触发、固定产物目录；门禁不通过，状态机不许跃迁。

## 四流水线

### P1 Spec 流水线（Spec 仓库 CI）

- **触发**：`specs/**` 或 `knowledge/**` 的任何 PR。
- **阶段**（配置见 [ci/specrepo-ci.yml](ci/specrepo-ci.yml)）：
  1. `tools/check.py --strict`：三平面一致性（ID、引用、TTL、状态机、契约类型必填扩展）；
  2. 契约 lint：JSON Schema / asyncapi 校验；
  3. **兼容性 diff**：数据集与接口 schema 用 json-schema-diff；**`EVAL-BENCH` 任何字段变更自动标红并要求委员会决议编号**（换尺子防线）；
  4. Agent jobs：cycle-summarizer（PR 摘要与波及点名）、contract-impact（数据集/协议变更 → 下游训练配置与在跑循环的波及枚举）。
- **产物**：`reports/<run>/check.json`、`compat.md`、`impact.md`。

### P2 团队开发流水线（两条，各团队自有仓库）

**DATA 数据流水线**（[ci/data-ci.example.yml](ci/data-ci.example.yml)）：
- 每个批次构建：契约场景直译的质量断言（去重率、污染计数、lineage 完备率、合成占比）——**断言即测试**，红灯批次不得发布版本号；
- **遥测义务**：批级 profile 快照 + `DQ-QUALITY` 指标上报（快照与上报缺一即批次无效）。

**MODEL 训练流水线**（[ci/model-ci.example.yml](ci/model-ci.example.yml)）：
- 训练配置必须引用 frozen 契约版本与具体数据集版本（禁止"读最新"）；
- **污染预检**：训练 mix 对 holdout deny-list 的相似度自检（本地通道，P3 审计为终裁）；
- **遥测义务**：run 级 `TRN-HEALTH` 指标自动上报 + 实验指纹登记（`trn_fingerprint_reg_rate == 1.0` 是硬门禁——没指纹的 run 不可比，G3 拒收）。

三层监控、dashboard-as-code 与调优工作流的完整设计见 [observability/README.md](../observability/README.md)。

两个团队共同的跨平面义务：MR 引用知识项 ID 或显式 `knowledge: none`；涉及契约实现变更时自动注入相关 pitfall 清单给评审者与结对 Agent。

### P3 收敛流水线（评测——RSI 的生命线）

- **触发**：契约进入 `frozen` 且 challenger 注册完成。
- **阶段**：装配 frozen 环境 → **污染审计**（n-gram + embedding 双通道，`eval_leak_count == 0`）→ **评测双跑**（按 `EVAL-BENCH.x-protocol`，复现偏差 ≤ 阈值）→ 全量契约场景 + 验收场景执行 → 证据报告（run_id、契约版本指纹、回归矩阵、审计原始输出）。
- **门禁 G3**：三硬条件——污染 = 0、复现达标、场景 100%。**失败循环同样归档完整证据**（负结果是一等产出）。

### P4 发布流水线

- **触发**：G3 绿 + Release Steward 发起 KB。
- **阶段**：champion–challenger 编排草案（release-orchestrator 生成：shadow ≥48h → 灰度阶梯 → 热备期）→ G4 四方联签 → 执行 RB-001 → 观察期探针直接复用契约断言 → **G5 回流检查**（experiment-distiller 候选 ≥1 被 Curator 处置）。
- **回滚**：见 [RB-001](../knowledge/runbooks/RB-001-model-promotion-rollback.md)。

## 五道门禁一览

| 门禁 | 判定 | 证据 | 跃迁 |
|---|---|---|---|
| G1 三平面校验 | check.py 严格模式绿 + eval diff 无未批变更 | CI 日志 | Spec PR 可合并 |
| G2 契约冻结 | 四方联签 + G1 绿 | PR merge commit | 循环开跑（起跑线锁定） |
| G3 收敛全绿 | 污染 = 0 · 评测复现 ≤ ε · 场景 100% | 证据报告 | 允许发起 KB |
| G4 KB 联签 | 四 Steward 签 + PAT-001 三件套 | KB 记录 | 允许 shadow/灰度 |
| G5 观察与回流 | 探针绿 48h + 候选知识被处置（含负结果） | 观察报告 | Feature → `released`（新 champion 转正） |

## 工具占位与替换原则

| 用途 | 示例工具 | 备注 |
|---|---|---|
| 三平面一致性 | `tools/check.py`（自带） | 纯 stdlib，任意 CI |
| 数据集质量断言 | pandera / Great Expectations | S-003 断言直译 |
| schema 兼容性 | json-schema-diff / oasdiff | **工具结论优先于人** |
| 污染审计 | n-gram（MinHash）+ embedding ANN | P3 双通道，deny-list 只在 DATA 侧 |
| 评测执行 | 自有 harness + 实验跟踪（MLflow/W&B 类） | run_id 与契约版本指纹入报告 |
| 模型注册与灰度 | 注册表 + 分流平台 | champion 热备 ≥14 天 |

替换任何工具时保持三条不变：产物落 `reports/<run>/`、门禁语义不变、playbook 输入输出不变。
