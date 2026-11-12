---
id: CARD-003
type: capability
title: Agent 平台团队能力卡
bu: AGENT
scope: "bu:AGENT"
confidence: high
status: accepted
owner: "@sun-lei"
provenance: [能力盘点-2026-Q4]
expires: 2027-02-15
provides: [SRC-INGEST.v1, FLY-FEEDBACK.v1, RAG-HEALTH.v1]
consumes: [MDL-SERVE.v1, MDL-CKPT.v1, RAG-DOCS.v1, RAG-RETRIEVE.v1]
contact: "#agent-platform-oncall"
---

# AGENT（Agent 平台团队）能力卡

## 负责什么

任务分发、线上流量与灰度执行、熔断开关；轨迹数据的源头场景定义（task 分类口径）。

## 边界与非目标

- 不改写 `terminal_verdict`，只按 S-005 义务转发埋点事件；
- 不在灰度期混用两代契约版本的分流规则（循环串轨是 PIT-001 变体）。

## 提供的契约 / 消费的契约

见 frontmatter，事实以 `specs/contracts/` 为准。

## 消费节奏与能力

- 发布窗口：随 P4 编排（RB-001）；分流规则 + 种子可复现；
- 契约测试：S-005 消费侧回放已接入（2026-11 起）。
