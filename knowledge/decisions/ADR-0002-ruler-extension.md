---
id: ADR-0002
type: decision
title: 裁判外延——reward/verifier、检索 judge、安全套件一律等同评测协议
scope: cross-bu
confidence: high
status: accepted
date: 2026-11-12
owner: "@rsi-governance-committee"
provenance: [契约族场景化评审, RL-VERIFIER v1 冻结辩论]
---

# ADR-0002 所有"运行时裁判"适用三权分立

## 背景

ADR-0001 把评测权从训练权手里拿走，但场景化后出现多个**分散的裁判**：RL 的 reward/verifier（RL-VERIFIER）、RAG 的 claim judge（RAG-RETRIEVE）、对齐安全的红队与拒答口径（POST-EVAL）。被优化的信号就是尺子——优化哪个，哪个就有权定义"好"。

## 决策

1. 凡被训练/调优**直接优化或强依赖**的质量信号，其契约 kind 必须是 `eval` 且 `x-contract.approval: committee`——不设"轻量版 verifier"例外；
2. 裁判的实现与部署归 DATA（或其对应独立方），被优化方（MODEL/AGENT）只能提 draft CR；
3. 裁判换版 = 尺子级变更：委员会决议 + 新旧双跑 ≥1 循环；reward/分数曲线**不可跨裁判版本直接比较**；
4. 裁判自身的考卷（fixture/探针/红队集）纳入污染审计同一通道（S-014 #2、S-015 #3、S-016 #3）。

## 后果

- DATA 评测线负载增加：四把尺子（EVAL-BENCH / RL-VERIFIER / RAG-RETRIEVE / POST-EVAL）都需要 fixture 维护与轮换预算——已写进 CARD-001；
- MODEL 侧失去"顺手改 reward"的自由——这是目的不是代价；
- 委员会决议量上升：`fly_respec_count`（换尺子 CR 数）从治理心电图变为**排班表**，月会需预留尺子评审时段。
