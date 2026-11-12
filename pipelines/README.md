# Execution 平面：四流水线与五门禁

Execution 平面把"部门间承诺"变成"可审计证据"。每条流水线有固定触发、固定产物目录；**门禁不通过，状态机不许跃迁**。

## 四流水线

### P1 Spec 流水线（Spec 仓库 CI）

- **触发**：`specs/**` 或 `knowledge/**` 的任何 PR。
- **阶段**：
  1. `tools/check.py --strict`（三平面一致性：ID、引用、TTL、状态机合法性）→ 配置见 [ci/specrepo-ci.yml](ci/specrepo-ci.yml)；
  2. 契约 lint（spectral 对 openapi/asyncapi）；
  3. 契约兼容性 diff（oasdiff / json-schema-diff，基线 = main）→ **breaking 检测即拦截，需 CR**；
  4. Agent jobs：spec-summarizer（PR 摘要+影响面）、contract-impact（consumer 波及分析）。
- **产物**：`reports/<run>/check.json`、`compat.md`、`impact.md`。

### P2 BU 开发流水线（各 BU 自有仓库，模板见 [ci/bu-dev-ci.example.yml](ci/bu-dev-ci.example.yml)）

- **触发**：业务仓库 push / MR。
- **必含两个跨平面 job**（接入 TriPlane 的最低义务）：
  1. **契约测试**：从 Spec 仓库拉取相关契约 + 契约场景（S-xxx），跑消费者/提供者验证（Pact 风格或场景直译）；
  2. **知识门禁**：MR 描述必须引用 ≥1 个知识项 ID 或显式 `knowledge: none`；改动涉及契约实现时自动注入对应 pitfall 清单给评审者与 Agent。
- **Agent jobs**：scenario-forge（场景→测试骨架 PR）、test-weaver（契约 CR→消费方测试补丁 PR）。

### P3 集成流水线（跨 BU 汇合）

- **触发**：任一契约进入 `frozen`，或集成窗口手动触发。
- **阶段**：从契约自动装配虚拟化环境（provider 真实 + consumer 打桩 / 双端真实二选一）→ 执行全部 `executable: true` 的 Scenario → 产出**证据报告**（通过率、契约版本指纹、环境清单）。
- **门禁**：G3 = 通过率 100% 且兼容 diff 无未走 CR 的变更。证据报告是 KB 的附件，没有报告不能进 G4。

### P4 发布流水线

- **触发**：G3 绿 + Delivery Steward 发起。
- **阶段**：依赖图排期（release-orchestrator 生成：提供方先/消费方后、major 共存窗口）→ flag 灰度 → 观察期探针（直接复用契约场景断言作线上探针）→ G5 回流检查（distiller 候选 ≥1 被处置）。
- **回滚**：见 [RB-001](../knowledge/runbooks/RB-001-contract-freeze-rollback.md)。

## 五道门禁一览

| 门禁 | 判定 | 证据 | 跃迁 |
|---|---|---|---|
| G1 三平面校验 | check.py 严格模式绿 | CI 日志 | 任何 Spec PR 可合并 |
| G2 契约冻结 | 联签 + G1 绿 | PR merge commit | Feature → `frozen` |
| G3 契约收敛 | P3 场景 100% + 无未审破坏 | 证据报告 | 允许发起 KB |
| G4 KB 联签 | 各 BU Steward 签 + 排期确认 | KB 记录 | 允许 P4 灰度 |
| G5 观察与回流 | 探针绿 48h + 候选知识被处置 | 观察报告 | Feature → `released` |

## 工具占位与替换原则

| 用途 | 示例工具 | 备注 |
|---|---|---|
| 三平面一致性 | `tools/check.py`（自带） | 只依赖 stdlib，可直接进任意 CI |
| 契约 lint | Spectral | 规则包可定制 |
| 兼容性判定 | oasdiff（API）、json-schema-diff（事件/数据） | **工具结论优先于人** |
| 契约测试 | Pact 或场景直译测试 | S-xxx 的 `runner` 字段指向实现 |
| 环境装配 | WireMock/本地 stub，以契约为源 | 契约即 mock——SDD 的红利 |

替换任何工具时保持三条不变：产物落 `reports/<run>/`、门禁语义不变、Agent playbook 的输入输出不变。
