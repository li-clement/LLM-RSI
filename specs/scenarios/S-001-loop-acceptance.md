---
id: S-001
kind: acceptance
feature: F-2026-001
status: accepted
executable: true
runner: "p3-convergence/loop-suite"
---

# S-001 改进循环端到端验收场景

> P3 收敛流水线的可执行输入：Gherkin 步骤映射到 `p3-convergence/loop-suite`，骨架由 assertion-forge Agent 维护。

```gherkin
Feature: 一个完整的改进循环（F-2026-001）

  Background:
    Given 本轮循环的八个循环契约按 frozen_at 时点版本装配（TRJ-ROLLOUT.v1 / SFT-PAIRS.v1 / RL-ROLLOUT.v1 / RL-VERIFIER.v1 / EVAL-BENCH.v1 / POST-EVAL.v1 / MDL-CKPT.v1 / MDL-SERVE.v1）

  Scenario: 正常循环——挑战者转正
    When DATA 按 SFT-PAIRS.v1 交付本周后训练样本版本
    And MODEL 基于该版本产出 challenger 并注册
    Then P3 污染审计 eval_leak_count == 0
    And 按 EVAL-BENCH.v1 双跑评测，reproducibility_gap <= 0.3pp
    And target_gain >= +3.0pp 且 regression_dims == 0
    And 进入 G4 联签与 P4 灰度

  Scenario: 污染阻断——泄漏即出局
    Given challenger 训练 mix 中检出与 holdout 相似度超阈的衍生样本
    When P3 审计执行
    Then 本轮 G3 判负，challenger 不得进入 KB
    And 泄漏样本清单与根因自动成候选知识（status: candidate）

  Scenario: 换尺子拦截——阈值变更未获批
    Given 某 PR 修改了 EVAL-BENCH 的 target_gain 阈值且标题不含 CR-
    When P1 执行 eval 协议 diff
    Then 门禁标红失败，并点名需治理委员会决议编号

  Scenario: 失败循环也要完整归档
    When challenger 未达 target_gain
    Then 回归矩阵与证据报告仍归档为 G3 产物
    And experiment-distiller 必须产出 ≥1 条负结果候选知识

  Scenario: 灰度熔断与回滚
    Given 新 champion 灰度 10% 时错误率达熔断条件
    When RB-001 执行
    Then 60 秒内切回上一 champion（仍在热备期）
    And 本轮循环状态回退，契约保持 frozen，不追加临时变更

  Scenario: 自提案治理
    Given RSI 系统自身提出新的 mix 配比方案
    When 提案进入 Spec 仓库
    Then 只能是 draft CR（provenance 标注 model:<version>@<episode>）
    And 未经 Steward 处置不得进入任何冻结状态
```

## 覆盖声明

- 覆盖 F-2026-001 全部验收口径（目标/地板/预算/期限）与 E-001 Epic 级口径。
- 依赖知识：ADR-0001、PAT-001、PIT-001、RB-001。
