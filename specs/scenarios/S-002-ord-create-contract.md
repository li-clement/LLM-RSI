---
id: S-002
kind: contract
contract: ORD-CREATE.v1
status: accepted
executable: true
runner: "mid-repo/contract-tests/ord-create"
---

# S-002 ORD-CREATE 契约场景（提供方期望）

> 契约场景 = 该契约必须满足的行为断言，运行在提供方 BU（MID）的 P2 流水线，以及集成流水线的虚拟化环境中。

| # | 断言 | 层级 |
|---|---|---|
| 1 | 缺失 `Idempotency-Key` 请求头必须 4xx，不得创建订单 | schema |
| 2 | 相同幂等键 + 相同请求体 → 返回首次响应（201，同 orderId） | 行为 |
| 3 | 相同幂等键 + 不同请求体 → 409 | 行为 |
| 4 | `amountCents < 1` → 422 并带 `OrderError.code` | 行为 |
| 5 | 响应 `status` 恒为 `created`（支付状态不出现在此契约） | 语义边界 |
| 6 | 新增请求/响应可选字段不得使既有 consumer（FRONT 声明版本）失败 | 兼容性 |

## 反例（必须失败）

- 用时间戳代替幂等键去重；
- 409 场景下仍创建了订单再回滚（副作用泄漏）。
