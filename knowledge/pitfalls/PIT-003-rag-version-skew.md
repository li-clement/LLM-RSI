---
id: PIT-003
type: pitfall
title: RAG 版本歪斜三角——语料×索引×模型三角里每一边都有版本号
scope: cross-bu
confidence: high
status: accepted
owner: "@curator-agent"
provenance: [RUN-2026-1109 RAG 召回假性下跌复盘, RAG-DOCS v1 冻结]
expires: 2027-03-31
---

# PIT-003 RAG 版本歪斜：召回下降常常不是"模型退步"

## 形态

RAG 质量是 **语料(RAG-DOCS) × 索引(embedding/chunking 版本) × 消费模型(MDL-CKPT/SERVE)** 的系统属性。三角任一角单独升级而其余没对齐时：

- 换 embedding 模型但旧 chunk 未全量重建 → 新旧向量混检，`rag_recall_at_k` 假性暴跌（或更糟：**虚高**——近重复互相召回）；
- chunking 策略改了但探针评测未重跑 → 离线达标、在线 `rag_citation_valid_rate` 下滑；
- 模型换代但知识库 rights/valid_through 口径未复核 → 新模型更"自信"地引用过期文档（`rag_stale_citation_rate` 升）。

## 探测

- `rag_version_skew_events == 0`（RAG-HEALTH，在线抽样对账查询向量版本 vs 索引版本）；
- 离线/在线双轨偏差 >3pp 触发口径对账（S-015 #5 / S-020 #2）；
- 归因顺序铁律：先查三角版本对账，再看模型指标——顺序反了会做出错误的回滚。

## 预防

- embedding/chunking 变更 = 破坏性契约变更：全量重建 + RAG-RETRIEVE 重跑 + 委员会知会（S-012 #1）；
- MDL-CKPT 交接单记录消费侧绑定的索引版本；索引发布物记录 embedding 模型 fingerprint。
