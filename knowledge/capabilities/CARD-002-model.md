---
id: CARD-002
type: capability
title: 模型团队能力卡
bu: MODEL
scope: "bu:MODEL"
confidence: high
status: accepted
owner: "@zhao-qi"
provenance: [能力盘点-2026-Q4]
expires: 2027-02-15
provides: [TRJ-ROLLOUT.v1, RL-ROLLOUT.v1, MDL-CKPT.v1, MDL-SERVE.v1, TRN-HEALTH.v1, PRE-HEALTH.v1, MID-HEALTH.v1]
consumes: [CORP-PRETRAIN.v1, SFT-PAIRS.v1, EVAL-BENCH.v1, RL-VERIFIER.v1, POST-EVAL.v1, DQ-QUALITY.v1, FLY-CYCLE.v1]
contact: "#model-rsi-oncall"
---

# MODEL（模型团队）能力卡

## 负责什么

- 预训练（PRE-HEALTH + CORP 消费）、中训练（MID-HEALTH：长上下文扩展/annealing）、后训练与 RL（TRN-HEALTH + RL-ROLLOUT 产出）；
- checkpoint 阶段交接按 MDL-CKPT（lineage/消费位置/指标快照齐全才算交接完成，PAT-003）；
- serving 侧轨迹埋点与合规发布（TRJ-ROLLOUT，脱敏 + judge_version 绑定）；
- 模型注册表与 champion 热备管理（PAT-001 第 4/5 步的执行方）。

## 边界与非目标

- 不自建评测集、不自行判分——转正只认 EVAL-BENCH（ADR-0001）；
- 不直连数据源库：数据只经 CORP-PRETRAIN / SFT-PAIRS 契约版本 pin 交付；
- 自提案（mix 建议/训练补丁）只能以 draft CR 形式进入，同等三闸门。

## 提供的契约 / 消费的契约

见 frontmatter，事实以 `specs/contracts/` 为准。

## 消费节奏与能力

- 训练窗口：G2 后 14 天内产出 challenger；shadow 双跑资源已排期；
- 契约测试：S-002/S-005 提供侧用例已接入 P2；
- 值班：`#model-rsi-oncall`，serving 熔断 5 分钟响应。
