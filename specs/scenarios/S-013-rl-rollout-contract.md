---
id: S-013
kind: contract
contract: RL-ROLLOUT.v1
status: accepted
executable: true
runner: "model-repo/contract-tests/rl-rollout"
---

# S-013 RL-ROLLOUT 契约场景（DATA 审计 RL 轨迹的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 每条轨迹 `verifier_result.verifier_version` ∈ RL-VERIFIER 登记表；未登记版本 = 事件拒收 | 门禁 |
| 2 | `task_ref` 通过 holdout deny-list 校验：评测衍生题池禁止进入 RL 题池（PIT-001 的 RL 面） | 门禁 |
| 3 | `ckpt_fingerprint` 可解析到 MDL-CKPT 注册表；孤儿 ckpt 轨迹整组隔离 | 数据 |
| 4 | 同 `group_id` 轨迹组完整（组内 advantage 计算单位）；缺组事件计入 trn_rl_advantage_collapse 上下文 | 数据 |
| 5 | RL 轨迹进入 SFT-PAIRS/蒸馏通道前必须过污染与去重断言（复用 S-011 #4，不另建口径） | 门禁 |

**义务**：MODEL 侧 rollout 采样器必须上报 `run_id` 供 TRN-HEALTH 归因；DATA 每周产出 verifier 分歧抽样复核报告（喂 S-014）。
