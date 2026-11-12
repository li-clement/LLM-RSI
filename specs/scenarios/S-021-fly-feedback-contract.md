---
id: S-021
kind: contract
contract: FLY-FEEDBACK.v1
status: accepted
executable: true
runner: "agent-repo/contract-tests/fly-feedback"
---

# S-021 FLY-FEEDBACK 契约场景（飞轮进料的质量门）

| # | 断言 | 层级 |
|---|---|---|
| 1 | `episode_ref` 断链的信号不进 `fly_recirculate_rate` 分子（口径防稀释，FLY-CYCLE 对账） | 门禁 |
| 2 | 反馈 verdict 只作**筛选线索**：进入训练前必须过 RL-VERIFIER/评测仲裁补真值——用户说对 ≠ 对 | 治理 |
| 3 | `experiment_bucket` 缺失的反馈只进观察池不做归因（防灰度污染因果结论） | 数据 |
| 4 | 信号 → 候选样本 → 入 mix 的转化率按周可算（分母=有效信号数，口径写死在 FLY-CYCLE） | 数据 |
| 5 | edit/regenerate 高密度信号自动开 SFT-PAIRS 候选（带 lineage.origin=feedback@episode） | 流程 |

**义务**：AGENT 保证信号不重复投递（feedback_id 幂等）；DATA 每周发布缺口报告（empty_retrieval + 负反馈聚类 → 下轮 S1 立靶输入）。
