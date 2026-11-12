---
id: F-2026-001
title: 一个完整的改进循环（工具调用维度）
epic: E-001
status: frozen
frozen_at: 2026-11-10
bu: [DATA, MODEL, AGENT]
contracts: [TRJ-ROLLOUT.v1, DS-TRAINMIX.v1, EVAL-BENCH.v1, MDL-SERVE.v1]
knowledge: [ADR-0001, PAT-001, PIT-001, RB-001, DOM-001, CARD-001, CARD-002, CARD-003]
owner: "@cycle-owner-01（MODEL 轮值）"
---

# F-2026-001 一个完整的改进循环（工具调用维度）

## 循环规格（这就是 RSI 的"这一轮到底要干什么"）

- **目标维度**：工具调用成功率（judge 口径见 [EVAL-BENCH.v1](../contracts/EVAL-BENCH.v1.eval.json)），挑战者须比现任 champion **+3.0pp**。
- **回归地板**：guard 维度（指令遵循、长上下文问答、拒答正确率）回归数 = 0（任一下降 >0.5% 即违规）。
- **预算**：单轮训练算力 ≤ 上轮 1.2×；新模型线上成本 ≤ champion 1.1×；合成数据占比 ≤ 35%。
- **循环期限**：冻结后 21 天（到期未过 G3 → 循环作废归档，契约不延期）。

## 跨团队职责切分

| 工作项 | 责任团队 | 交付物 | 验收锚点 |
|---|---|---|---|
| 轨迹采集与上报 | MODEL（serving 侧埋点） | `TRJ-ROLLOUT.v1` 提供方实现 | S-002 |
| 清洗、去重、组装训练集 | DATA | `DS-TRAINMIX.v1` 提供方实现 | S-003 |
| 评测执行与污染审计 | DATA（Eval Steward） | `EVAL-BENCH.v1` 协议执行 | S-004 |
| challenger 训练与注册 | MODEL | 训练管道 + 模型注册记录 | S-001 |
| 灰度流量与熔断执行 | AGENT | `MDL-SERVE.v1` 消费实现 | S-005 |

> 职责切分表是冻结谈判的核心：先划边界与裁判权，再谈数据格式。

## 契约要点（详情只准引用 ID，不复述字段与阈值）

- [TRJ-ROLLOUT.v1](../contracts/TRJ-ROLLOUT.v1.asyncapi.json)：rollout 轨迹事件流（MODEL→DATA）。
- [DS-TRAINMIX.v1](../contracts/DS-TRAINMIX.v1.schema.json)：训练集记录契约，含 SLA 与污染断言（DATA→MODEL）。
- [EVAL-BENCH.v1](../contracts/EVAL-BENCH.v1.eval.json)：评测协议——**本循环的裁判，阈值只有委员会能动**。
- [MDL-SERVE.v1](../contracts/MDL-SERVE.v1.model.json)：模型服务契约（MODEL→AGENT）。

## 非目标

- 不追求多目标同时改进（一轮只动一个目标维度）。
- 不改评测基准构成（holdout 换血走下一份 `EVAL-BENCH.v2` CR）。
- 不含自动阈值调优——**禁止**。

## 风险与知识消费

- 蒸馏数据含评测题变体是最隐蔽的泄漏 → 强制消费 [PIT-001](../../knowledge/pitfalls/PIT-001-train-eval-contamination.md)。
- 转正与回滚按 [PAT-001](../../knowledge/patterns/PAT-001-champion-challenger.md) champion–challenger 模式。
- 裁判权结构依据 [ADR-0001](../../knowledge/decisions/ADR-0001-eval-authority-separation.md)。
- 上线与熔断操作见 [RB-001](../../knowledge/runbooks/RB-001-model-promotion-rollback.md)。

## 验收

端到端：[S-001](../scenarios/S-001-loop-acceptance.md)；契约断言：[S-002](../scenarios/S-002-trj-rollout-contract.md)、[S-003](../scenarios/S-003-ds-trainmix-contract.md)、[S-004](../scenarios/S-004-eval-bench-contract.md)、[S-005](../scenarios/S-005-mdl-serve-contract.md)。
