---
id: S-020
kind: contract
contract: RAG-HEALTH.v1
status: accepted
executable: true
runner: "observability-repo/contract-tests/rag-health"
---

# S-020 RAG-HEALTH 契约场景（RAG 在线镜像监控可信）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 每次检索查询按 collect 记录（含命中 doc_id 与引用有效性判定），采样率登记在 x-telemetry.collect | 数据 |
| 2 | 在线口径与离线一致：`rag_citation_valid_rate` 与 RAG-RETRIEVE.rag_citation_validity 偏差 >3pp → 口径对账 CR（S-015 #5 的反向） | 门禁 |
| 3 | `rag_version_skew_events == 0`：在线查询向量版本与 RAG-DOCS 索引版本抽样对账，混用即 crit 告警（PIT-003） | 门禁 |
| 4 | `rag_empty_retrieval_rate`/`rag_feedback_edit_rate` 缺口信号自动汇入 FLY-FEEDBACK 处理队列（信息指标也要有去向） | 数据 |
| 5 | SLO 违例路由：freshness/staleness 违例 → DATA 语料管道；recall 下降 → 版本歪斜排查清单（PIT-003） | 治理 |

**义务**：AGENT 维护在线采集；DATA 每周对账在线/离线双轨并出报告（引用 ID）。
