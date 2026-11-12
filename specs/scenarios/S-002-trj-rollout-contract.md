---
id: S-002
kind: contract
contract: TRJ-ROLLOUT.v1
status: accepted
executable: true
runner: "model-serving-repo/contract-tests/trj-rollout"
---

# S-002 TRJ-ROLLOUT 契约场景（提供方 MODEL 的产出义务）

| # | 断言 | 层级 |
|---|---|---|
| 1 | payload 必含 `episode_id, model_version, task_id, terminal_verdict, pii_stripped, recorded_at` | schema |
| 2 | `pii_stripped == false` 的事件必须在发布侧门禁拦截，不得进入回流通道 | 合规 |
| 3 | `model_version` 必须可在模型注册表解析；未注册版本的事件拒收 | 行为 |
| 4 | `terminal_verdict.judge_version` 必填且与登记口径表一致——judge 换版必须先有 CR（PIT-001 口径漂移探测） | 兼容性 |
| 5 | 同一 `episode_id` 重复投递时字段值必须完全一致（at-least-once 语义） | 行为 |
| 6 | 新增可选字段不得破坏 DATA 清洗管道既有解析 | 兼容性 |
| 7 | 采样率变化（如仅回流成功轨迹）必须走 CR——分布突变 = mix 口径变更 | 语义边界 |

## 消费方（DATA）义务

- 按 `episode_id` 幂等去重；死信队列承接未知 `eventVersion`。
