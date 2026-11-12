---
id: S-018
kind: contract
contract: PRE-HEALTH.v1
status: accepted
executable: true
runner: "observability-repo/contract-tests/pre-health"
---

# S-018 PRE-HEALTH 契约场景（预训练健康监控可信）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 每个预训练 run（含失败/抢占 run）自动上报全部指标；`pre_data_position_reg_rate == 1.0` | 门禁 |
| 2 | 面板/告警只引用本契约 ID：`pre_loss_zscore` 无第二实现；ckpt 交接快照由 `x-lineage.metric_snapshot_refs` 链接而非复制 | 数据 |
| 3 | 告警路由生效：`pre_restart_loss_events` crit → 值班 + RB-002 通道；连续违例自动 pitfall 候选 | 治理 |
| 4 | `pre_curriculum_adherence == 0 违规`：curriculum 声明与消费顺序对账（PAT-003），差异报告进 run 收口 | 门禁 |
| 5 | MFU 调优实验登记指纹（配置哈希 + 语料批次清单）——无指纹的"提速"不进 KB | 数据 |

**义务**：MODEL 维护采集 hooks；DATA 用同一指标 ID 做集群容量月报（引用 ID，不复述数值）。
