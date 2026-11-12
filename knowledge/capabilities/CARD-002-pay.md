---
id: CARD-002
type: capability
title: 支付部能力卡
bu: PAY
scope: "bu:PAY"
confidence: high
status: accepted
owner: "@liu-xiang"
provenance: [季度能力盘点-2026-Q4]
expires: 2027-02-15
provides: [PAY-CONFIRM.v1]
consumes: [ORD-PAID.v1]
contact: "#pay-oncall"
---

# PAY（支付部）能力卡

## 负责什么

支付单生命周期、渠道网关对接、资金安全与对账源数据。

## 边界与非目标

- 不感知购物车与营销（→ MID 订单域）；
- 不提供"发起扣款"的跨 BU 直接调用（异步事件 + 查询是唯一模式，ADR-0001）；
- 渠道回调不去重由消费方负责——但 PAY 保证幂等查询语义（S-004）。

## 提供的契约 / 消费的契约

见 frontmatter，事实以 `specs/contracts/` 为准。

## 消费节奏与能力

- 发布窗口：每周三（灰度 1%→10%→100%，flag 控制）；
- 契约测试：S-003（事件消费）、S-004（查询提供）已在 P2 接入；
- 值班：`#pay-oncall`，资金类告警 5 分钟响应。
