---
id: RB-002
type: runbook
title: 预训练/中训练断点恢复——先验证身世，再接续火
scope: MODEL
confidence: high
status: accepted
owner: "@curator-model"
provenance: [PAT-003 演练 2026-11-11, PRE-HEALTH S-018]
expires: 2027-05-31
---

# RB-002 长周期训练中断恢复 Runbook

## 触发

抢占/硬件故障/管道中断导致 run 停止；或 `pre_restart_loss_events` 告警。

## 步骤（顺序不可乱）

1. **定位**：从 MDL-CKPT 注册表按 run_id 取最新**已验证** ckpt（未验证的最后一个分片直接放弃，宁丢一小时不接脏段）；
2. **验身世**：`ckpt_fingerprint` 三 hash（arch/tokenizer/pos）与当期契约一致——不一致即 PIT-003 同款事故，冻结排查，禁止强行续训；
3. **位置回放**：按 `x-lineage.consumption_position` 重放数据装载（PAT-003），确认 `pre_data_position_reg_rate` 账实相符；
4. **Sanity 门**：续跑前 200 step 内 loss 连续性检查（对 pre_restart 前窗口 z-score ≤3）+ 迷你探针集；不过 → 回退一个 ckpt 重试，两次不过升事故；
5. **记账**：恢复时长、丢弃步数、`pre_restart_loss_events` 补记；中断 >4h 写 pitfall 候选（同因连续两周期 → 自动升级）。

## 反模式

- "看起来 loss 正常就继续"——没做位置回放的续跑，之后所有 A/B 全部作废；
- 手工挑"最好的 ckpt"——只认注册表按 lineage 的下一个，挑拣 = 制造孤儿 ckpt。
