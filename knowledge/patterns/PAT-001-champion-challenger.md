---
id: PAT-001
type: pattern
title: Champion–Challenger 转正模式
scope: cross-bu
confidence: high
status: accepted
owner: "@curator-model"
provenance: [RUN-2026-1104, MDL-SERVE.v1 CR-2]
expires: 2027-06-30
---

# PAT-001 Champion–Challenger 转正模式

## 何时用

每一轮改进循环的 S5（转正与回流）。判定口诀：**现任是基准，挑战者只靠 frozen 协议赢上位**。

## 怎么做

1. **Shadow 双跑**：challenger 在真实流量影子镜像上跑 ≥ 48h，产出 TRJ 事件但不对客；
2. **转正条件三件套**（全部来自 frozen 契约，不许临时加戏）：`target_gain` 达标、`regression_dims == 0`、成本/时延在 `x-budget` 内；
3. **灰度阶梯**：1% → 10% → 100%，每档观察 ≥ 30 分钟，探针直接用契约场景断言（S-005 #2/#3）；
4. **热备退役**：旧 champion 热备 ≥14 天（回滚 SLA <60s 的前提），期满才从注册表退役；
5. **循环身份**：每代 champion 在注册表登记其消费的契约版本指纹（DS 数据集版本 + EVAL 协议版本）——"它是在什么尺子下赢的"必须可查。

## 反模式

- 双跑时让 challenger 用不同 judge_version 对比（换尺子的变体）；
- 灰度期间同时开新 mix 训练下一轮（两循环在契约上串轨）——并行循环必须各自 frozen 各自的契约版本；
- challenger 失败后原地调阈值再评一次（委员会权限）。

## 怎么验证

P4 编排检查第 2/3/4/5 步证据齐全；G4 联签附件 = 三件套报告 + 契约版本指纹。
