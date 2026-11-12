---
id: CARD-001
type: capability
title: 数据团队能力卡
bu: DATA
scope: "bu:DATA"
confidence: high
status: accepted
owner: "@liu-yan"
provenance: [能力盘点-2026-Q4]
expires: 2027-02-15
provides: [DS-TRAINMIX.v1, EVAL-BENCH.v1, DQ-QUALITY.v1, FLY-CYCLE.v1]
consumes: [TRJ-ROLLOUT.v1, TRN-HEALTH.v1]
contact: "#data-rsi-oncall"
---

# DATA（数据团队）能力卡

## 负责什么

- 轨迹清洗、去重、脱敏复核与训练集组装（每周批次，SLA 见契约）；
- 评测执行与污染审计——**循环的裁判**（评测权，ADR-0001）；
- holdout 基准的维护与轮换（45 天），judge 版本登记；
- 数据开发与飞轮指标契约（DQ-QUALITY / FLY-CYCLE）的定义与采集实现（`quality_suite`）。

## 边界与非目标

- 不参与训练配置与超参决策（→ MODEL）；
- 不响应"降一下阈值再看一次"的口头请求——只有委员会可动阈值；
- 不向 MODEL 提供 deny-list 明细（防反向泄漏），只输出审计结论。

## 提供的契约 / 消费的契约

见 frontmatter，事实以 `specs/contracts/` 为准。

## 消费节奏与能力

- 批次窗口：每周四交付训练集版本；评测双跑窗口：G3 前 72h；
- 契约测试：S-003/S-004 已接入 P2/P3（2026-11 起）；
- 值班：`#data-rsi-oncall`，污染告警 30 分钟响应。
