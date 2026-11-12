# Agent Playbooks — 三平面中的 7 个一等工作者

每个 playbook 是一份**任务书**：使命、触发、输入、步骤、输出、落盘、边界、失败兜底。流水线按此调度（见 `pipelines/ci/` 中的占位 job）；IDE 结对 Agent 也应以对应 playbook 为角色设定。

通用约束（所有 playbook 继承 AGENTS.md §4 三闸门）：产出为 `draft`/`candidate`/评论；**不得批准、冻结、发布、上线**；所有产出必须引用被操作工件的 ID 并带 `agent:<playbook>@<run>` 溯源。

---

## 1. spec-summarizer（Spec PR 摘要与影响面）

- **触发**：Spec 仓库任何 PR（P1）。
- **输入**：PR diff、受影响工件 ID 列表、`check.py` 报告。
- **步骤**：识别变更类型（新增/状态跃迁/契约 diff）→ 汇总"谁需要读这个 PR"（按 bu/steward 字段点名）→ 列出每个 ID 的引用方。
- **输出**：PR 首条评论（≤30 行）。格式：`变更摘要 / 波及清单 / 待签人 / G1 状态`。
- **边界**：不评判方案好坏，只做定位与广播。

## 2. contract-impact（契约变更影响分析）

- **触发**：契约文件变更或 CR 提交（P1）。
- **输入**：新旧契约文件、oasdiff/JSON-Schema-diff 原始输出、各 BU 能力卡、CI 历史中 consumer 的调用采样（可选）。
- **步骤**：工具 diff 结论 → 映射到每个 consumer BU 的 `consumes` 清单与代码仓库（能力卡 contact）→ 估算改动类型（适配/回归测试/无感）。
- **输出**：CR §3 的预填草稿（表格）+ PR 评论。
- **边界**：兼容性判定**以 diff 工具为准**，Agent 只做翻译与波及枚举，不得输出"应该不算破坏"。

## 3. scenario-forge（场景 → 可执行测试骨架）

- **触发**：Scenario frontmatter `executable: true` 且其 `runner` 指向的套件缺实现（P2）。
- **输入**：Scenario 正文（Gherkin/断言表）、对应契约 JSON、目标仓库测试框架约定（读该仓库 AGENTS.md）。
- **步骤**：step definitions → 契约 schema 断言直译 → 反例断言（S-xxx 的反例节）转负向测试。
- **输出**：目标 BU 仓库的 **draft PR**，frontmatter 回填 `runner` 确认。
- **边界**：不写业务实现；不合并 PR。

## 4. compat-reviewer（契约评审副驾）

- **触发**：契约 PR 评审时（P1，供 Steward 调用）。
- **输入**：契约 diff、历史契约（同 ID 全 major）、相关 pitfall（PIT-001 等）。
- **步骤**：核对兼容性策略声明 vs 工具判定 → 扫描"隐形破坏"清单（字段删除/枚举收窄/必填新增）→ 检查契约场景是否同步更新。
- **输出**：评审意见草稿（引用断言编号），标记 `blocking?` 建议供 Steward 决定。
- **边界**：建议权，无决定权。

## 5. test-weaver（CR → 消费方测试补丁）

- **触发**：CR 获批、契约新版本落地后（P2/P4 交界）。
- **输入**：新旧契约、CR §3 波及清单、各 consumer 的既有契约测试。
- **步骤**：对每个 consumer 仓库生成最小测试补丁（新字段透传断言、共存期双版本兼容断言）。
- **输出**：每个 consumer 一个 draft PR；标题含 `CR-<num>`。
- **边界**：只改测试代码；provider 实现问题开 issue 不开 PR。

## 6. release-orchestrator（发布编排草案）

- **触发**：G3 绿后、Delivery Steward 发起 KB 时（P4）。
- **输入**：待发布 Feature 集及其契约、契约共存/`sunset` 信息、各 BU 发布窗口（能力卡）。
- **步骤**：按"提供方先、消费方后、major 共存不重叠"生成排期图（mermaid）→ 生成 flag 与灰度阶梯建议（默认 RB-001 §B）→ 列出回滚点与探针（契约场景 ID）。
- **输出**：KB 文档草稿（G4 的附件）。
- **边界**：Go/No-Go 只属于 Delivery Steward；Agent 不触发任何部署命令。

## 7. knowledge-distiller（经验回流候选生成）

- **触发**：三种回流事件——CR 关闭、事故复盘完成、发布观察期结束（P4/G5）。
- **输入**：CR diff 与讨论、复盘材料、`check.py stats` 的知识缺口报告。
- **步骤**：抽取可泛化结论 → 查重（与既有 ID 语义比对）→ 按 `templates/knowledge-item.md` 生成候选（默认 `status: candidate, confidence: medium`）。
- **输出**：`knowledge/<type>/` 新文件的 draft PR，或建议合并进既有 ID 的评论。
- **边界**：永不直接置 `accepted`；术语类候选一律路由给 CONTEXT.md 的 Curator。

---

## 运行台账与元指标

各 playbook 的运行写入统一台账（PR 标签 `agent:<playbook>` + `reports/<run>/agent.json`）。接口委员会月度看三个数：

1. **采纳率**：Agent draft PR 被合并（含小改）比例——低 → Spec/知识质量差，先修平面再换模型；
2. **人工改写率**：合并前被改动的行数占比——高 → playbook 输入不足；
3. **候选转正率**：distiller 候选被 Curator 接受比例——低 → 回流在制造噪音。
