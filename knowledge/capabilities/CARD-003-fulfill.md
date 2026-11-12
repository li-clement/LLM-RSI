---
id: CARD-003
type: capability
title: 履约物流部能力卡
bu: FULFILL
scope: "bu:FULFILL"
confidence: high
status: accepted
owner: "@zhou-k"
provenance: [季度能力盘点-2026-Q4]
expires: 2027-02-15
provides: []
consumes: [ORD-PAID.v1]
contact: "#fulfill-oncall"
---

# FULFILL（履约物流部）能力卡

## 负责什么

履约单生成与仓配调度；以事实事件驱动，不反向写入交易/支付域。

## 边界与非目标

- 不直接查询支付域（资金事实一律经 `ORD-PAID.v1` 事件）；
- 不接受"下单即锁库存"类同步调用请求——只消费支付成功事实（S-003 消费方义务）。

## 提供的契约 / 消费的契约

见 frontmatter，事实以 `specs/contracts/` 为准。

## 消费节奏与能力

- 发布窗口：每周一；
- 契约测试：S-003 消费侧用例已接入（2026-11 起）；
- 值班：`#fulfill-oncall`。
