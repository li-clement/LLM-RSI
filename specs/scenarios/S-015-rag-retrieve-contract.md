---
id: S-015
kind: contract
contract: RAG-RETRIEVE.v1
status: accepted
executable: true
runner: "eval-repo/contract-tests/rag-retrieve"
---

# S-015 RAG-RETRIEVE 契约场景（RAG 系统质量裁判）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 探针题集 45 天轮换 ≥20%，旧题归档但不再计入达标（防过拟合题库） | 数据 |
| 2 | embedding/chunking 变更前本协议全量重跑通过才准切换（与 S-012 #1 配对：一个定门禁一个给证据） | 门禁 |
| 3 | 探针题与真值文档在训练通道泄漏审计 == 0（RAG 语料与探针物理隔离的验证） | 门禁 |
| 4 | `rag_groundedness` 的 claim-level judge 版本 pin 进登记表（换 judge = 尺子级，委员会） | 治理 |
| 5 | 在线镜像一致性：RAG-HEALTH.rag_citation_valid_rate 与离线口径偏差 >3pp → 触发口径对账 CR | 数据 |

**义务**：DATA 每循环输出探针分维度报告（时效/拒答/难度分层）；负向结果（降标）同样入库（G5）。
