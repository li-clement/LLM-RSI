---
id: S-011
kind: contract
contract: SFT-PAIRS.v1
status: accepted
executable: true
runner: "data-repo/contract-tests/sft-pairs"
---

# S-011 SFT-PAIRS 契约场景（MODEL 消费后训练样本的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 每条样本 `lineage.origin` 可回溯 episode 或声明合成来源；`source=rollout` 必带 `steps_hash`（回链 TRJ-ROLLOUT） | 门禁 |
| 2 | `reward_verdict.judge_version` 与当期登记一致；旧 verdict 样本复用前须重判或标注 | 数据 |
| 3 | 拒绝采样样本的 `verifier_version` == 被消费时 RL-VERIFIER 当前版（依据失效即重采） | 门禁 |
| 4 | `synthetic_share <= 0.35`、污染 == 0、去重达标（断言即测试，红灯批次不发版） | 门禁 |
| 5 | human_review_coverage ≥10% 抽检分歧率进入知识回流（分歧样本自动成候选 pitfall） | 治理 |

**义务**：mix 配比变更 = 口径级，走 CR；MODEL 侧训练配置必须引用批次版本号清单。
