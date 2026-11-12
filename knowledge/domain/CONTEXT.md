---
id: DOM-001
type: glossary
title: RSI 项目统一语言
scope: cross-bu
confidence: high
status: accepted
owner: "@curator-data, @curator-model"
provenance: [S1-立靶工作坊-2026-10-28, RUN-2026-1104-失焦复盘]
expires: 2027-02-01
---

# 跨团队统一语言（术语仲裁唯一源）

"变好了吗"之所以吵不清，多数时候是词没对齐。以下定义**优先于**任何团队内部惯用法；新术语/改定义走 CR 给 Curator，评测口径词必须同时引用契约 ID。

## 团队与域码表

| 代码 | 组织 | 域码 |
|---|---|---|
| DATA | 数据团队 | DS / EVAL |
| MODEL | 模型团队 | TRJ / MDL |
| AGENT | Agent 平台团队 | —（消费方） |

## 术语表

| 术语 | 定义 | 不是什么 | 首次裁定 |
|---|---|---|---|
| 改进循环（cycle） | 一次"回流→组装→训练→评测→转正"的完整递归，= 一个 Feature | 不是实验批次，不是训练 run | E-001 |
| 轨迹（rollout trace） | 一次 agent 任务实例的完整步骤序列 + 终局判分，主键 `episode_id` | 不是会话日志原文（正文走对象存储，哈希入契约） | TRJ-ROLLOUT.v1 |
| 回流 | 轨迹经采样/脱敏进入数据域的过程 | 不是全量复制；采样率变更 = mix 口径变更 | S-002 |
| 训练 mix | 一个数据集版本内各来源（human/rollout/distilled/synthetic）的构成与配比 | 不是超参；配比语义属契约 | DS-TRAINMIX.v1 |
| 污染（contamination） | holdout 及其任何衍生（改写/蒸馏/同题合成）出现在训练 mix | 不只是"同文本重复"——同题变体也算 | ADR-0001 |
| holdout | EVAL-BENCH 引用的基准题集，45 天轮换 | 不是"测试集随手备份" | EVAL-BENCH.v1 |
| champion / challenger | 现任线上基准模型 / 本轮候选 | challenger 赢了才叫 champion，裁判是 EVAL-BENCH | PAT-001 |
| 目标维度 / guard 维度 | 本轮唯一优化指标 / 只许持平的地板指标 | guard 不设防 = 循环失控 | EVAL-BENCH.v1 |
| 换尺子 | 未经委员会的指标定义/阈值/judge 版本变更 | 不是"口径优化"——口径只能走 CR | PIT-001 |
| 判分口径（judge_version） | 判分器实现的登记版本 | judge 升级 = 协议变更（可能破坏可比性） | S-004 |
| 冻结（frozen） | 循环起跑线：契约口径锁定，循环中禁改 | 不是代码冻结 | MODE §3.3 |
| KB（联签） | DATA+MODEL+AGENT 三方 Steward 对转正上线的签核 | 不是单团队上线审批 | G4 |
| 负结果 | challenger 未达标但证据完整的循环产出 | 不是失败废料——必须蒸馏入库 | G5 |
