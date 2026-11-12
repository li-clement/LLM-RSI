---
id: S-004
kind: contract
contract: PAY-CONFIRM.v1
status: accepted
executable: true
runner: "pay-repo/contract-tests/pay-confirm"
---

# S-004 PAY-CONFIRM 契约场景（消费方 MID 的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 已知 paymentId 必返回 200 且 `status ∈ {succeeded, failed, pending}` | schema |
| 2 | 未知 paymentId 返回 404，不得返回 500 | 行为 |
| 3 | 处理中的支付单返回 408，响应时间 ≤ 2s | 行为 |
| 4 | `confirmedAt` 对终态（succeeded/failed）必填 | schema |
| 5 | 新增可选字段（如 `channelTrace`）不得破坏 MID 既有解析 | 兼容性 |
| 6 | 状态机不可逆：已 `succeeded` 的支付单再次查询不得变为 `pending` | 语义边界 |

## 消费方义务

- MID 必须按 ADR-0001 的退避与上限轮询，不得无限重试；重试必须携带同一 traceId。
