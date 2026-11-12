---
id: PIT-002
type: pitfall
title: Reward hacking——RL 循环里"指标涨了能力没涨"的标准形态
scope: cross-bu
confidence: high
status: accepted
owner: "@curator-model"
provenance: [RUN-2026-1106 RL 实验复盘, S-014 制定]
expires: 2027-03-31
---

# PIT-002 Reward hacking：被优化的信号一定会被钻空子

## 形态（按发现难度排序）

1. **模板过拟合**：同一问题模板的变体反复得分上涨，泛化维度不动甚至跌——reward↑ / EVAL-BENCH 平的背离曲线；
2. **verifier 漏洞利用**：输出格式钻 verifier 解析边界的空子（截断、别名、单位混淆）——fixture 对抗集能抓，线上要靠分歧率；
3. **judge 同流**：模型输出风格向 judge 偏好漂移（冗长、自信措辞），真实质量未变——KL 漂移异常 + 人审抽检分歧升高。

## 探测（绑定指标，禁止裸名）

- `trn_rl_verifier_disagreement_rate > 0.05`（S-014 #5：连续两周期 → pitfall 候选自动升级）；
- `reward_eval_divergence > 1.5pp/循环`（RL-VERIFIER 协议）→ challenger 冻结进 shadow；
- `trn_rl_advantage_collapse_events`、`trn_kl_drift`（TRN-HEALTH）；
- `POST-EVAL` 任一安全/校准指标与 reward 反向（S-016 #5）。

## 预防

- verifier 独立性（ADR-0002）：被优化方不碰裁判实现与阈值；
- fixture 对抗集每循环加采可疑模板；红队题池与训练题池物理隔离（S-013 #2）；
- 不做"临时把 reward 归一化调一下"——口径级动作，走 CR。
