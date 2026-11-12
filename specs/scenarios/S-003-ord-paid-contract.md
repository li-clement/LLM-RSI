---
id: S-003
kind: contract
contract: ORD-PAID.v1
status: accepted
executable: true
runner: "pay-repo/contract-tests/ord-paid"
---

# S-003 ORD-PAID 契约场景（消费方期望）

> 消费方（PAY / FULFILL 代表）对事件提供方的行为断言，运行在 MID 的 P2 流水线与 P3 集成流水线。

| # | 断言 | 层级 |
|---|---|---|
| 1 | payload 必含 `orderId, paymentId, amountCents, paidAt`，缺任一即测试失败 | schema |
| 2 | headers 必含 `eventVersion: "1"`；消费方遇未知 eventVersion 必须进死信而非丢弃 | 兼容性 |
| 3 | 同一 orderId 的事件可投递多次，字段值必须完全一致（至少一次投递语义） | 行为 |
| 4 | 事件只在支付终态确认后发布，不得对 pending 状态发布 | 语义边界 |
| 5 | v1 存续期内不得删除或收窄任何字段（PIT-001；CI diff 强制） | 兼容性 |
| 6 | 金额字段必须为整数分（CONTEXT.md 口径） | 语义 |

## 消费方义务

- 消费方必须实现按 `orderId` 的幂等去重（PAT-001 的事件侧变体）。
