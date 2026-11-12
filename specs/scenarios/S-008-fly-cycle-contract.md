---
id: S-008
kind: contract
contract: FLY-CYCLE.v1
status: accepted
executable: true
runner: "observability-repo/contract-tests/fly-cycle"
---

# S-008 FLY-CYCLE 契约场景（消费方 MODEL 的期望：飞轮数字可重算）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 全部指标从 P3/P4 证据报告与流水线时间戳**重算**；任何手填数字 = 契约违规（审计对比原始证据） | 真实性 |
| 2 | `fly_target_gain_pp` 仅在 challenger 与 champion 的 judge_version 相同时记录为可比值；否则置空并挂口径 CR 标记 | 可比性 |
| 3 | 失败循环必须产出 `fly_negative_result_published >= 1` 才能关账（G5 量化形态） | 回流 |
| 4 | `fly_recirculate_rate` 按 `episode_id` 归因链路计算：episode → sample_id → 训练 mix 版本，断链即计不转化 | 语义 |
| 5 | 每循环收口快照 reports/<cycle>/flywheel.json 是下一轮 S1 立靶的法定输入（Epic 层面引用） | 闭环 |
| 6 | `fly_respec_count` 长期为 0 触发治理自查（审计可能失效），进委员会月会议程 | 元指标 |

## 消费方（MODEL）义务

- 下一轮循环的目标维度选择必须引用上一轮 flywheel.json 快照 ID，禁止"感觉该优化什么"。
