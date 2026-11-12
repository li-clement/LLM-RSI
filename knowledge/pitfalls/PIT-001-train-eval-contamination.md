---
id: PIT-001
type: pitfall
title: 训练-评测污染与换尺子——RSI 最隐蔽的两类自伤
scope: cross-bu
confidence: high
status: accepted
owner: "@curator-data"
provenance: [RUN-2026-1104, INC-RSI-002]
expires: 2027-05-31
---

# PIT-001 RSI 循环的两类隐形破坏

## 故事

INC-RSI-002：某轮 challenger 报 +5.1pp。事后审计发现三件事同时成立：训练 mix 里 6% 样本是评测题的"改写变体"（蒸馏来源标注为 rollout，lineage 里查不到原型）；判分器上轮从 v2 升到 v3 未登记；guard 维度里"拒答正确率"实际跌了 1.2pp 但没人跑这个维度。循环开始在错误信号上递归。

## 两类隐形破坏（一律按破坏性/事故处理）

**A. 污染（数据面）**
1. 直接泄漏：holdout 样本进训练 mix；
2. 衍生泄漏：改写、蒸馏、同题合成（**最隐蔽**，文本不同但题目同源）；
3. 反向泄漏：challenger 在 shadow 期见过评测分布。

**B. 换尺子（裁判面）**
1. judge 版本升级未走 CR；
2. 指标 `def` 文本微调（"成功率"分母从全量变有效量）；
3. guard 维度悄悄不进评测；
4. 阈值"临时"下调再评。

## 探测：流水线怎么拦

- P3 污染审计（**双通道**）：n-gram 精确重叠 + embedding 相似度阈（对变体）；`eval_leak_count == 0` 是 block 级断言（DS-TRAINMIX.x-quality）；
- lineage 强制：每条样本 `source` + `origin` 可回溯，`distilled` 必须填原型 ID；
- judge_version 绑定：评测报告与数据集版本都登记 judge_version，不一致 → 结果作废（S-004 #5）；
- eval 契约 diff：P1 对 `EVAL-BENCH` 任何字段变更自动标红，要求标题带 CR + 委员会决议编号；
- guard 维度不可减：`metrics` 中 `direction: zero/bounded` 项删除 = 破坏性变更（S-004 场景覆盖）。

## 预防

- 蒸馏/合成管道对 holdout 做生成前检索排除（deny-list 在 DATA 侧，不给 MODEL）；
- 每轮 G3 证据报告必须含污染审计原始输出，不只是 pass/fail；
- 负结果入库：泄漏根因、口径争议写成 pitfall/ADR，下轮循环 S1 必读。
