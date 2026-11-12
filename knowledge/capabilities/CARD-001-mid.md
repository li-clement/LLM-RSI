---
id: CARD-001
type: capability
title: 交易中台部能力卡
bu: MID
scope: "bu:MID"
confidence: high
status: accepted
owner: "@chen-mo"
provenance: [季度能力盘点-2026-Q4]
expires: 2027-02-15
provides: [ORD-CREATE.v1, ORD-PAID.v1]
consumes: [PAY-CONFIRM.v1]
contact: "#trade-mid-oncall"
---

# MID（交易中台部）能力卡

## 负责什么

订单域的创建、状态机、事实事件发布；跨 BU 交易链路的对账凭证源。

## 边界与非目标

- 不管理资金、不接触渠道网关（→ PAY）；
- 不直连仓配系统（→ FULFILL 经事件解耦）；
- 拒绝在订单 API 内嵌支付逻辑的历史请求（2026-10 已仲裁）。

## 提供的契约

见 frontmatter `provides`（事实以 `specs/contracts/` 为准，此处仅引用 ID）。

## 消费节奏与能力

- 发布窗口：每周二/四；紧急走 RB-001 §应急通道。
- 契约测试：P2 流水线已接入 S-002/S-003 运行器（2026-11 起）。
- 值班：`#trade-mid-oncall`，SLA 30 分钟响应。
