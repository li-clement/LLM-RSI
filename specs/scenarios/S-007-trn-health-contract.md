---
id: S-007
kind: contract
contract: TRN-HEALTH.v1
status: accepted
executable: true
runner: "observability-repo/contract-tests/trn-health"
---

# S-007 TRN-HEALTH 契约场景（消费方 DATA 的期望：训练侧透明可审计）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 每个训练 run（含失败 run）自动上报全部非 informational 指标；缺报即 run 无效 | 完整性 |
| 2 | `trn_fingerprint_reg_rate == 1.0`：run 必须登记契约版本指纹（数据集版本 + EVAL 协议版本 + TRJ 版本），否则评测拒绝其 challenger 身份 | 可比性 |
| 3 | `trn_kl_drift` 超阈 → 自动触发 guard 维度加测并通知 Eval Steward（不自动 kill 训练，但影响 G3） | 门禁联动 |
| 4 | `trn_reward_hacking_flags > 0` 的 run 不得进入 shadow 双跑，直到归因关闭 | 语义 |
| 5 | run 级 profile 快照保留 ≥ 90 天，供 experiment-distiller 消费 | 证据 |
| 6 | 指标口径变更走 CR；影响与评测可比性的（如 KL 估计器换版）需 DATA 侧 Steward 会签 | 兼容性 |

## 消费方（DATA）义务

- 评测排期与污染审计资源按 `trn_tokens_per_hr` 趋势预测，不靠口头产能承诺。
