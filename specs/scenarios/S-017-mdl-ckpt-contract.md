---
id: S-017
kind: contract
contract: MDL-CKPT.v1
status: accepted
executable: true
runner: "model-repo/contract-tests/mdl-ckpt"
---

# S-017 MDL-CKPT 契约场景（阶段交接的硬通货）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 注册表中 100% ckpt 带完整 x-lineage（stage、数据集版本清单、评测协议版本、消费位置、指标快照链接）——孤儿 ckpt 不得进评测/部署 | 门禁 |
| 2 | 交接验证：按 `consumption_position` 恢复训练，loss 连续性检查通过（`pre_ckpt_resume_integrity == 1.0` 的证据源） | 可复现 |
| 3 | `ckpt_fingerprint` 全局唯一且被 RL-ROLLOUT/MDL-SERVE 等工件成功解析（引用完整性） | 数据 |
| 4 | 架构/tokenizer/位置方案任一变化 → fingerprint 必变且触发模型契约 major（防"偷偷换底模"） | 门禁 |
| 5 | AGENT 部署只从注册表按 fingerprint 拉取；serving 版本 ↔ ckpt 映射可审计回训练数据清单 | 治理 |

**义务**：MODEL 每 run 收口时写交接单；DATA 对进入评测的 ckpt 做 lineage 抽查（每月 ≥3 个）。
