---
id: S-009
kind: contract
contract: SRC-INGEST.v1
status: accepted
executable: true
runner: "data-repo/contract-tests/src-ingest"
---

# S-009 SRC-INGEST 契约场景（采集入口：DATA 对 AGENT 供数的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 任一批次 `pii_stripped_rate == 1.0`：抽样含 PII 原文即整批拒收 | 门禁 |
| 2 | `consent_scope=none/缺失` 的记录 0 条进入 CORP/SFT/RL 任何通道（下游 join 校验） | 门禁 |
| 3 | `source_id` 100% 命中源登记表；未注册源的事件进隔离区不入主流 | 门禁 |
| 4 | `content_sha256` 去重后量 vs 原始量之比可复现（PAT-002 第一层输入） | 数据 |
| 5 | 新增 `event_type/scene` 枚举走非破坏 CR 登记，消费方无感 | 流程 |

**义务**：AGENT 侧投递重试必须幂等（`event_id` 去重主键）；DATA 侧隔离区告警接 `dq_job_success_rate`（DQ-QUALITY）。
