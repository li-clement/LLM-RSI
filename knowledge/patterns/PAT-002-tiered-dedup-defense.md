---
id: PAT-002
type: pattern
title: 分层去重与污染防线——四道网各有指标，禁止单层裸奔
scope: DATA
confidence: high
status: accepted
owner: "@curator-data"
provenance: [CORP-PRETRAIN v1 冻结, RUN-2026-1109]
expires: 2027-05-31
---

# PAT-002 数据工程通用防线：exact → minhash → embedding → probe 召回

## 适用

所有向模型训练供数的场景（采集入口、预训练语料、后训练样本、RAG 库）——同一骨架，不同阈值。

## 结构

| 层 | 手段 | 抓什么 | 绑定指标/断言 |
|---|---|---|---|
| L1 | hash 精确（content_sha256） | 重复投递、爬虫重拉 | `raw_dedup_rate`（SRC-INGEST） |
| L2 | minhash 近重（阈值 0.85） | 转载、模板文 | `dedup_tier_pass`（CORP-PRETRAIN） |
| L3 | embedding 语义近重（余弦 ≥0.92） | 改写洗稿、蒸馏回声 | `pairwise_dedup_rate`（SFT-PAIRS） |
| L4 | probe 召回审计 | holdout/探针/红队集的**衍生** | `eval_leak_count == 0`（PIT-001 + P3 双通道） |

## 要点

- 每层比率**逐批登记进 manifest**（S-010 #3）：缺层 = 批次不完整，不是"效果差点"；
- L4 用与 L3 不同的模型与阈值（同模型近重有相关性盲区——PIT-001 的教训）；
- 阈值调参是参数级自由，改**分层结构与口径**是口径级走 CR；
- 监控侧只搬运（`dq_dedup_rate`/`dq_eval_leak_count` binds），禁止在 metrics 管道二次实现（S-006 #2）。
