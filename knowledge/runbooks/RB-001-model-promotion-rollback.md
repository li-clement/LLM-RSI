---
id: RB-001
type: runbook
title: 新模型转正、灰度与回滚 Runbook
scope: cross-bu
confidence: high
status: accepted
owner: "@release-steward"
provenance: [首次 KB 演练-2026-11-08]
expires: 2027-02-12
---

# RB-001 循环 S5 三步：G4 联签 → 灰度转正 → 熔断回滚

## A. G4 联签（KB）

1. Release Steward 发起，附件必须齐：P3 证据报告（污染审计原始输出、评测双跑差值、回归矩阵）+ PAT-001 三件套 + 契约版本指纹；
2. Dataset Steward、Eval Steward、Model Steward、AGENT 代表四方签署；
3. cycle-summarizer Agent 自动核对"报告里的数字是否都来自 frozen 契约版本"，对不上即拒绝受理。

## B. 灰度转正（P4）

1. Shadow 双跑 ≥48h（challenger 只产事件不对客）；
2. 1% → 10% → 100%，每档 ≥30 分钟；每档探针 = S-005 断言 #2/#3；
3. 每档放量前核对：错误率、时延 p99、成本/ktoken 均在 `MDL-SERVE.x-budget`；
4. 转正完成：注册表标记新 champion + 其契约版本指纹；旧 champion 转热备（≥14 天，不得提前退役）。

## C. 熔断与回滚

- 触发：错误率超基线 2× 持续 5 分钟；`target_gain` 线上探针转负；任一 guard 维度线上代理指标异常；
- 步骤：切流回旧 champion（<60s，热备在位是前提）→ 冻结本轮循环（Feature 回退 `frozen`，不追加临时变更）→ 保留 challenger 全部工件待审计 → 24h 内事故材料喂 experiment-distiller 产候选 pitfall；
- 严禁：现场调阈值"再看一次"（委员会权限）、把线上流量样本补进本轮训练集（污染）。

## D. 应急通道

生产 P0（如完全不可用）可先切回旧 champion 再补手续，但 48h 内必须补 CR + 场景，否则该接口进入孤岛名单（`check.py stats` 点名，下季禁止新消费方接入）。
