---
id: S-014
kind: contract
contract: RL-VERIFIER.v1
status: accepted
executable: true
runner: "eval-repo/contract-tests/rl-verifier"
---

# S-014 RL-VERIFIER 契约场景（RL 循环裁判的可信性）

| # | 断言 | 层级 |
|---|---|---|
| 1 | verifier 发版前必须过 fixture 考卷：precision ≥0.95 / recall ≥0.90，未达标不得部署（DATA 部署，MODEL 只能提议） | 门禁 |
| 2 | fixture 集及其衍生物在 CORP/SFT/RL 题池的泄漏审计 == 0（与 P3 同通道） | 门禁 |
| 3 | verifier 换版 = 尺子级变更：委员会 RES- + 新旧双跑 ≥1 循环，reward 曲线不可跨版直接比 | 治理 |
| 4 | `reward_eval_divergence <= 1.5pp/循环`：reward 涨幅与 EVAL-BENCH 涨幅背离超限 → 冻结 challenger 进 shadow（PIT-002） | 门禁 |
| 5 | 在线分歧率（trn_rl_verifier_disagreement_rate）连续两周期违例 → 自动 pitfall 候选 | 治理 |

**义务**：DATA 维护 verifier 登记表与 fixture 轮换；MODEL 侧不得本地重定义 reward 归一化口径。
