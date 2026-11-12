---
id: RB-001
type: runbook
title: 契约冻结、发布与回滚 Runbook
scope: cross-bu
confidence: high
status: accepted
owner: "@delivery-steward"
provenance: [首次 KB 演练-2026-11-08]
expires: 2027-02-12
---

# RB-001 跨 BU 发布三步：冻结 → KB → 回滚

## A. 冻结（G2）

1. Spec Owner 提 PR：Feature `approved → frozen`，填 `frozen_at`；
2. 检查 P1 全绿（check.py + 兼容性 diff + 每个契约有契约场景）；
3. 提供方 Steward + 每个 consumer BU 代表在 PR 联签 → 合并；
4. release-orchestrator Agent 自动产出依赖图与影响清单，挂 PR。

## B. KB 发布（G4 → P4）

1. Delivery Steward 发起：所有相关 Feature 状态 `released` 前置检查 → P3 场景通过率 100%；
2. 各 BU Steward 按发布窗口排期：提供方先发（新契约文件），消费方后发；major 共存期两版并跑；
3. flag/灰度：1% → 10% → 100%，每档观察 ≥ 30 分钟（错误率与契约场景探针）；
4. G5：观察期结束后 **48h 内**确认回流——distiller 候选知识 ≥1 条被 Curator 处置（发布或拒绝），否则 KB 记为未完成。

## C. 回滚触发与步骤

- 触发：错误率超基线 2× 持续 5 分钟，或任一契约场景探针失败；
- 步骤：关 flag → 消费方退回上一契约版本（旧文件在 `sunset` 前不会删除）→ 事件通道切回旧版本 header（`eventVersion`）→ 对账走 ADR-0001 §2 人工通道；
- 回滚后 24h 内：事故材料喂给 knowledge-distiller，产出候选 pitfall。

## 应急通道

生产 P0 可先斩后奏，但 48h 内必须补 CR 与场景，否则接口自动进入"孤岛名单"（`check.py stats` 点名，下季度禁止新消费方接入）。
