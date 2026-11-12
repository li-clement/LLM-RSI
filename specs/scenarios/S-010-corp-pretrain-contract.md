---
id: S-010
kind: contract
contract: CORP-PRETRAIN.v1
status: accepted
executable: true
runner: "data-repo/contract-tests/corp-pretrain"
---

# S-010 CORP-PRETRAIN 契约场景（MODEL 消费预训练语料的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 批次携带 mix manifest：域×语言占比与声明偏差 ≤2pp，缺 manifest 拒收 | 门禁 |
| 2 | `eval_leak_count == 0` 由 P3 双通道审计（n-gram + embedding），MODEL 侧只做搬运监控（dq_eval_leak_count） | 门禁 |
| 3 | 去重分层比率（exact/minhash/embedding）逐批登记，任一层缺失 = 批次不完整 | 数据 |
| 4 | tokenizer 指纹与 MDL-CKPT.x-signature 一致才可装载（换 tokenizer = 新 major 契约） | 门禁 |
| 5 | 任意 checkpoint 可按 `batch_id` 顺序回放到训练位置（PAT-003 / pre_data_position_reg_rate） | 可复现 |

**义务**：DATA 每批发布版本号 + manifest 哈希；MODEL 消费必须 pin 版本号（禁止"读最新"）。
