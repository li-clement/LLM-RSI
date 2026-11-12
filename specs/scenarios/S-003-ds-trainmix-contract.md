---
id: S-003
kind: contract
contract: DS-TRAINMIX.v1
status: accepted
executable: true
runner: "data-pipeline-repo/contract-tests/ds-trainmix"
---

# S-003 DS-TRAINMIX 契约场景（消费方 MODEL 的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 每周批次满足 `x-sla`：cadence=weekly、freshness<=7d、min_count>=20000，缺任一批次告警并阻断训练 | SLA |
| 2 | `eval_leak_count == 0`：与 EVAL-BENCH holdout 及其衍生零重叠（n-gram + embedding 双通道） | 污染（block） |
| 3 | `pairwise_dedup_rate >= 0.995` | 质量（block） |
| 4 | `synthetic_share <= 0.35`，超标即 block | 预算（block） |
| 5 | `lineage_complete_rate == 1.0`：每条样本可回溯到 `episode_id` 或声明来源；`source=rollout` 时 `lineage.steps_hash` 必填 | 可追溯（block） |
| 6 | `source` / `license` 枚举不得收窄或删除；新增需 CR | 兼容性（PIT-001） |
| 7 | 批次交付必须携带数据集版本号与契约版本引用（`DS-TRAINMIX.vN`），MODEL 训练配置据此锁定 | 语义 |

## 消费方（MODEL）义务

- 训练配置必须引用具体数据集版本；不得"就地读取最新批次"（可比性前提）。
- mix 口径变更（组间配比、来源定义）需 CR——这不是字段变化但改变语义。
