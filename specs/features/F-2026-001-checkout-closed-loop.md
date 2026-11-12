---
id: F-2026-001
title: 下单到支付成功的最小闭环
epic: E-001
status: frozen
frozen_at: 2026-11-10
bu: [MID, PAY]
contracts: [ORD-CREATE.v1, ORD-PAID.v1, PAY-CONFIRM.v1]
knowledge: [ADR-0001, PAT-001, PIT-001, CARD-001, CARD-002, RB-001]
owner: "@chen-mo（MID）"
---

# F-2026-001 下单到支付成功的最小闭环

## 用户故事

作为**买家**，我提交订单并完成支付后，希望立即看到"支付成功、等待发货"；作为**履约侧**，我希望支付成功后 1 秒内拿到可信的订单已支付事实，无需轮询或人工核对。

## 跨 BU 职责切分

| 工作项 | 责任 BU | 交付物 | 验收锚点 |
|---|---|---|---|
| 订单创建与幂等 | MID | `ORD-CREATE.v1` 提供方实现 | S-001 / S-002 |
| 支付单受理与结果查询 | PAY | `PAY-CONFIRM.v1` 提供方实现 | S-004 |
| 支付成功事件发布 | MID（消费：PAY→MID 回执后触发）| `ORD-PAID.v1` 提供方实现 | S-003 |
| 渠道侧集成与重试 | PAY | 消费 `PAY-CONFIRM.v1` 的调用方实现 | S-004 |

> 职责切分表是冻结谈判的核心：先划边界，再谈接口。

## 契约要点（详情只准引用 ID，不复述字段）

- [ORD-CREATE.v1](../contracts/ORD-CREATE.v1.openapi.json)：创建订单，强制幂等键（依据 [ADR-0001](../../knowledge/decisions/ADR-0001-cross-bu-timeout-retry.md)）。
- [ORD-PAID.v1](../contracts/ORD-PAID.v1.asyncapi.json)：支付成功事实事件，消费方 PAY→履约链路与对账。
- [PAY-CONFIRM.v1](../contracts/PAY-CONFIRM.v1.openapi.json)：PAY 提供的支付单确认查询 API。

## 非目标

- 不含退款、部分支付、组合支付（下一 Feature：F-2026-002 起草中）。
- 不承诺跨渠道对账 SLA（由 `RB-001` 覆盖应急路径）。

## 风险与知识消费

- 事件 schema 演进收窄字段曾导致事故 → 强制消费 [PIT-001](../../knowledge/pitfalls/PIT-001-event-field-narrowing.md)。
- 幂等实现模式 → [PAT-001](../../knowledge/patterns/PAT-001-idempotency-key.md)。
- 发布与回滚步骤 → [RB-001](../../knowledge/runbooks/RB-001-contract-freeze-rollback.md)。

## 验收

见场景 [S-002](../scenarios/S-002-ord-create-contract.md)、[S-003](../scenarios/S-003-ord-paid-contract.md)、[S-004](../scenarios/S-004-pay-confirm-contract.md)（契约场景）与 [S-001](../scenarios/S-001-checkout-acceptance.md)（端到端验收场景）。
