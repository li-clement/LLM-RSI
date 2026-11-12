---
id: CARD-004
type: capability
title: 前端渠道组能力卡
bu: FRONT
scope: "team:front"
confidence: high
status: accepted
owner: "@xu-lan"
provenance: [季度能力盘点-2026-Q4]
expires: 2027-02-15
provides: []
consumes: [ORD-CREATE.v1]
contact: "#front-channel"
---

# FRONT（前端渠道组）能力卡

## 负责什么

app / web / mini 三端下单体验；幂等键的生成方与重试策略的执行方（PAT-001 调用侧）。

## 边界与非目标

- 不做订单状态机（→ MID），不在前端推断支付成功（必须等 ORD-PAID.v1 事实）；
- 不直连 PAY 域接口。

## 提供的契约 / 消费的契约

见 frontmatter，事实以 `specs/contracts/` 为准。

## 消费节奏与能力

- 发布窗口：随渠道班车（双周）；契约升级需过 S-002 消费侧回放。
