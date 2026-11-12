---
id: ADR-0001
type: decision
title: 评测权独立——训练权、评测权、阈值冻结权三权分立
scope: cross-bu
confidence: high
status: accepted
date: 2026-10-30
owner: "@rsi-governance-committee"
provenance: [RUN-2026-1104-失焦复盘, E-001 冻结评审]
---

# ADR-0001 RSI 循环的裁判权结构

## 背景

试点前最后一轮人工评审（RUN-2026-1104）：MODEL 汇报"+4.2pp"，DATA 复核发现其中 1.7pp 来自判分器升级（口径变化）、0.8pp 样本与 holdout 同题。两个团队都没撒谎——**但没有任何机制能证明"变好了"**。自进化系统最贵的事故不是算力浪费，而是循环在错误的反馈信号上递归放大。

## 决策

1. **三权分立**：训练权归 MODEL；评测执行与隔离审计归 DATA（Eval Steward）；指标定义与阈值的变更权归 RSI 治理委员会（`EVAL-BENCH` 契约 `approval: committee`）。
2. **评测单一源**：challenger 转正只认 `EVAL-BENCH` 协议执行结果；MODEL 团队不得建立私下评测集，"再跑个子集看看"不构成证据也不构成否决。
3. **污染零预算**：holdout 及其衍生进入训练 mix 的泄漏计数必须为 0，由 P3 机器审计（n-gram + embedding 双通道）阻断，不靠自觉。
4. **judge 换版 = 协议变更**：判分器版本必须与评测结果绑定登记（judge_version），未走 CR 的 judge 升级 → 该轮评测作废。

## 代价与后果

- DATA 承担裁判负载：评测双跑 + 审计进入每周批次成本（已排班）；
- MODEL 迭代速度受限：想改口径必须先赢 CR——这是故意设计；
- 委员会每月固定 1 小时处置 eval CR（阈值只允许升不允许降，除非基准换血走新 major）。

## 被取代条件

若公司级独立评测机构成立并接管 holdout 与判分器，本 ADR 标记 `superseded` 并链接新 ADR。
