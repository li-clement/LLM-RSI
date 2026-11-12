---
id: S-001
kind: acceptance
feature: F-2026-001
status: accepted
executable: true
runner: "integration-suite/checkout"
---

# S-001 下单到支付成功端到端验收场景

> 本文件是 P3 集成流水线的可执行输入：Gherkin 步骤映射到 `integration-suite/checkout` 的 step definitions，由 scenario-forge Agent 维护骨架。

```gherkin
Feature: 下单到支付成功的最小闭环（F-2026-001）

  Background:
    Given BU "MID" 与 BU "PAY" 的契约环境按 specs/contracts 冻结版本装配

  Scenario: 正常路径——下单并支付成功
    When 买家以幂等键 "K-001" 通过 ORD-CREATE.v1 创建订单
    And PAY 侧支付单进入 succeeded 终态
    Then 1 秒内收到 ORD-PAID.v1 事件
    And 通过 PAY-CONFIRM.v1 查询该 paymentId 返回 status=succeeded

  Scenario: 幂等——同一幂等键重复提交
    When 买家以相同幂等键 "K-001" 重复提交相同请求体 3 次
    Then 3 次返回同一 orderId
    And 只存在一张订单与一个支付单

  Scenario: 幂等冲突——同键不同体
    When 买家以 "K-001" 提交与首次不同的请求体
    Then ORD-CREATE.v1 返回 409
    And 首次订单不受影响

  Scenario: 支付超时后收敛
    When PAY-CONFIRM.v1 首次返回 408
    Then 按 ADR-0001 的退避策略（1s/3s/9s，上限 5 分钟）轮询
    And 最终收敛到 ORD-PAID.v1 事件或终态 failed

  Scenario: 事件至少一次投递的幂等消费
    Given ORD-PAID.v1 对同一 orderId 投递两次
    When 履约侧消费
    Then 只产生一次履约动作

  Scenario: 金额口径一致性
    When 端到端传递金额
    Then 全链路使用 amountCents 整数最小货币单位（CONTEXT.md）
    And 任何浮点数金额出现在契约层即视为违约
```

## 覆盖声明

- 覆盖 Feature：F-2026-001 全部验收口径（E-001 §Epic 级验收）。
- 依赖知识：ADR-0001、PAT-001、PIT-001、RB-001。
