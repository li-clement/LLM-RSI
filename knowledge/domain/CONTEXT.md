---
id: DOM-001
type: glossary
title: 交易域统一语言
scope: cross-bu
confidence: high
status: accepted
owner: "@curator-mid, @curator-pay"
provenance: [S1-共创工作坊-2026-10-28, INC-2025-118]
expires: 2027-02-01
---

# 跨 BU 统一语言（术语仲裁唯一源）

歧义是跨部门协同最贵的税。以下定义**优先于**任何 BU 内部惯用法；新术语/改定义走 CR 给 Curator。

## BU 代码表

| 代码 | 组织 | 域码 |
|---|---|---|
| MID | 交易中台部 | ORD |
| PAY | 支付部 | PAY |
| FULFILL | 履约物流部 | FUL |

## 术语表

| 术语 | 定义 | 不是什么 | 首次裁定 |
|---|---|---|---|
| 订单（Order） | 买家一次购买意图的 MID 域凭证，生命周期由 ORD 契约定义 | 不是支付单，不是履约单 | ADR-0001 |
| 支付单（Payment） | PAY 域对一次资金收付的凭证，以 `paymentId` 标识 | 不含购物车信息 | PAY-CONFIRM.v1 |
| 支付成功（succeeded） | PAY 域终态：资金已收妥且不可自动回滚 | 不等于"订单已支付"——后者须 MID 发布 ORD-PAID.v1 后成立 | ADR-0001 |
| 幂等键（Idempotency-Key） | 调用方生成、服务端保存的请求去重凭证，见 PAT-001 | 不是 traceId，不是订单号 | ADR-0001 |
| 金额（amountCents） | 以最小货币单位计的 64 位整数 | 禁止浮点、禁止字符串金额 | CONTEXT 决议 2026-10 |
| 终态（terminal state） | 不可再迁移的状态 | pending 不是终态 | S-004 |
| 冻结（frozen） | Feature/契约状态：此后变更只能走 CR | 不是"不能提 PR" | MODE §3.2 |
| KB（跨 BU 联签） | 各 BU Steward 对发布签核的合称 | 不是部门内上线审批 | G4 |
| 事实事件（fact event） | 对已发生事实的记录，消费方按至少一次设计 | 不是命令 | ORD-PAID.v1 |
