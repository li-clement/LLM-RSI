---
id: PAT-003
type: pattern
title: 数据消费位置回放——长周期训练的"可续跑性"是契约属性
scope: MODEL
confidence: high
status: accepted
owner: "@curator-model"
provenance: [PRE-HEALTH v1 冻结, RB-002 演练]
expires: 2027-05-31
---

# PAT-003 位置回放：每个 checkpoint 都能精确接上它吃过的数据

## 问题

预训练/中训练以周计，抢占与故障是常态。不可续跑的 run 不只是浪费算力——**恢复后吃错数据顺序，curriculum 失效，前后指标不可比**，整段训练变成调优黑箱。

## 机制

1. 消费位置指纹 = `sha256(batch_id 顺序清单 + 组内 shuffle seed)`，每个 ckpt 写入 `MDL-CKPT.x-lineage.consumption_position`；
2. 数据装载器按位置清单**重放**（CORP 批次不可变、`batch_id` 版本化是前提——这就是数据集契约 SLA 的存在理由）；
3. 恢复后先跑 sanity：loss 曲线连续性检查（`pre_ckpt_resume_integrity == 1.0`）+ 迷你探针，过了才续训（RB-002）；
4. curriculum 声明与消费顺序对账（`pre_curriculum_adherence`）：顺序即口径，插队喂数 = 违约不是优化。

## 收益判据

- 任意 ckpt 恢复 + 回放 < 30 分钟（MDL-CKPT x-budget）；
- 重启损耗（`pre_restart_loss_events`）可归因到位置错配与否——没有位置指纹时这个数**根本无法计算**。
