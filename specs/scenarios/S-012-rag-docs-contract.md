---
id: S-012
kind: contract
contract: RAG-DOCS.v1
status: accepted
executable: true
runner: "agent-repo/contract-tests/rag-docs"
---

# S-012 RAG-DOCS 契约场景（AGENT 消费知识库与索引的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 同一索引内 `embedding_version_consistent == 1.0`：换 embedding 版本必须全量重建 + 过 RAG-RETRIEVE 后才切换（PIT-003） | 门禁 |
| 2 | `index_freshness_hours <= 24`（在线镜像见 RAG-HEALTH.rag_freshness_p90_hours） | 门禁 |
| 3 | 每条文档 `valid_through` 存在；过期文档检索可见性按策略降权，不得静默删除（审计留痕） | 数据 |
| 4 | `pii_stripped_rate == 1.0` 且 `source_registered_rate == 1.0`——知识库复用 SRC-INGEST 合规口径（binds，不二次实现） | 门禁 |
| 5 | `chunking_policy` 版本登记；改切块规则 = 破坏性（触发全量重建与评测重跑） | 流程 |

**义务**：DATA 发布索引构建清单（doc 数、版本对账表）；AGENT 检索日志按 RAG-HEALTH.collect 上报。
