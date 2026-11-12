# Agent Playbooks — 三平面中的 7 个一等工作者（RSI 适配）

每个 playbook 是一份**任务书**：使命、触发、输入、步骤、输出、落盘、边界、失败兜底。流水线按此调度（见 `pipelines/ci/` 占位 job）；IDE 结对 Agent 也应以对应 playbook 为角色设定。

通用约束（所有 playbook 继承 AGENTS.md 三闸门）：产出为 `draft`/`candidate`/评论；**不得批准、冻结、发布、上线、改评测阈值**；所有产出必须引用被操作工件的 ID 并带 `agent:<playbook>@<run>` 溯源。

**RSI 自提案 = 第 8 个 Agent**：改进循环自身产出的提案（mix 建议、训练补丁、接口变更草稿、评测题生成）一律按本文件的 playbook 纪律进入——draft CR + provenance `model:<version>@<episode>`，由 Steward 处置。这是"允许递归、禁止换尺子"的执行机制。

---

## 1. cycle-summarizer（Spec PR 摘要与影响面）

- **触发**：Spec 仓库任何 PR（P1）。
- **输入**：PR diff、受影响工件 ID、`check.py` 报告、当前 frozen 循环清单。
- **步骤**：识别变更类型（新增/状态跃迁/契约 diff/**eval 协议 diff**）→ 点名"谁需要读这个 PR"（bu/steward 字段）→ 标出是否触及在跑循环的冻结基线。
- **输出**：PR 首条评论（≤30 行）：`变更摘要 / 波及清单 / 待签人 / G1 状态 / 是否触碰尺子`。
- **边界**：不评判方案好坏，只做定位与广播。

## 2. contract-impact（契约变更影响分析）

- **触发**：契约文件变更或 CR 提交（P1）。
- **输入**：新旧契约文件、json-schema-diff/oasdiff 原始输出、能力卡、训练配置中对数据集版本的引用清单（模型注册表）、评测历史。
- **步骤**：工具 diff 结论 → 映射到每个 consumer 团队的仓库与在跑循环 → 区分影响类型（适配 / 重跑评测 / 无感）→ **eval 契约变更自动升格为"换尺子风险"并附历史可比性影响清单**。
- **输出**：CR §3 预填草稿（表格）+ PR 评论。
- **边界**：兼容性判定以 diff 工具为准；不得输出"应该不算破坏"。

## 3. assertion-forge（场景 → 可执行断言）

- **触发**：Scenario `executable: true` 且其 `runner` 套件缺实现（P2/P3）。
- **输入**：Scenario 断言表/Gherkin、对应契约 JSON、目标仓库测试框架约定（读该仓库 AGENTS.md）。
- **步骤**：数据质量断言直译为 pandera/GX 规则；行为断言直译为集成测试骨架；反例节转负向测试；评测协议 metrics 直译为 harness 配置。
- **输出**：目标团队仓库的 **draft PR**，frontmatter 回填 `runner` 确认。
- **边界**：不写业务实现；不合并 PR；生成的 judge 配置必须 pin `judge_version`。

## 4. compat-reviewer（schema 演进与口径漂移副驾）

- **触发**：契约 PR 评审（P1，供 Steward 调用）。
- **输入**：契约 diff、同 ID 全部历史 major、相关 pitfall（PIT-001）。
- **步骤**：核对兼容性声明 vs 工具判定 → 扫描隐形破坏（字段删除/枚举收窄/必填新增/**judge_version 变更**/**采样率变更**）→ 检查契约场景是否同步更新。
- **输出**：评审意见草稿（引用断言编号），标记 `blocking?` 供 Steward 决定。
- **边界**：建议权，无决定权。

## 5. test-weaver（CR → 消费方测试补丁）

- **触发**：CR 获批、契约新版本落地（P2/P4 交界）。
- **输入**：新旧契约、CR §3 波及清单、各 consumer 既有契约测试。
- **步骤**：为每个 consumer 生成最小测试补丁（新字段透传、共存期双版本兼容、mix 口径变更的语义断言）。
- **输出**：每个 consumer 一个 draft PR；标题含 `CR-<num>`。
- **边界**：只改测试代码；provider 实现问题开 issue 不开 PR。

## 6. release-orchestrator（champion–challenger 编排草案）

- **触发**：G3 绿、Release Steward 发起 KB（P4）。
- **输入**：P3 证据报告、PAT-001 三件套数据、模型注册表状态（热备期）、AGENT 灰度能力。
- **步骤**：生成 shadow/灰度阶梯排期（mermaid）→ 熔断条件与探针清单（直接引用 S-xxx 断言编号）→ 回滚点与旧 champion 退役窗口。
- **输出**：KB 文档草稿（G4 附件）。
- **边界**：Go/No-Go 只属于 Release Steward；不触发任何切流命令。

## 7. experiment-distiller（循环经验回流候选生成）

- **触发**：三种回流事件——**循环 run 结束（无论成败）**、CR 关闭、事故复盘完成（P4/G5）。
- **输入**：P3 证据报告与回归矩阵、实验跟踪记录、CR diff 与讨论、`check.py stats` 知识缺口报告。
- **步骤**：抽取可泛化结论（**负结果优先**：哪条路不通、哪种 mix 无效、哪个口径有歧义）→ 查重 → 按 `templates/knowledge-item.md` 生成候选（`status: candidate, confidence: medium`）。
- **输出**：`knowledge/<type>/` 新文件 draft PR，或建议合并进既有 ID 的评论。
- **边界**：永不直接置 `accepted`；评测口径类候选一律路由 Eval Steward + 委员会，不得作为"下轮自动调参"的依据。

---

## 运行台账与元指标

各 playbook 运行写入统一台账（PR 标签 `agent:<playbook>` + `reports/<run>/agent.json`）。治理委员会月度看四个数：

1. **采纳率**：draft PR（含自提案）被合并（含小改）比例——低 → Spec/知识质量差，先修平面再换模型；
2. **人工改写率**：合并前改动行数占比——高 → playbook 输入不足；
3. **候选转正率**：distiller 候选被接受比例——低 → 回流在制造噪音；
4. **换尺子拦截数**：eval diff 标红且未获委员会批准的比例——这是 RSI 治理的**心电图**，非零是常态，全零要警惕审计失效。
