---
id: S-004
kind: contract
contract: EVAL-BENCH.v1
status: accepted
executable: true
runner: "data-eval-repo/protocol-tests/eval-bench"
---

# S-004 EVAL-BENCH 契约场景（消费方 MODEL 的期望：裁判必须可信）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 四个 metric 全部有可执行实现且与 `def` 文本一致（实现回归测试随协议版本走） | 协议 |
| 2 | `thresholds` 的值必须被评测代码读取自本契约文件，**不允许硬编码副本**（CI grep 检查） | 单一事实源 |
| 3 | 同一 (model, dataset, seed 策略) 双跑 `reproducibility_gap <= 0.3pp`，超差即本轮评测无效重跑 | 可复现 |
| 4 | holdout 每次使用后进入复用记录，`rotation_days` 内不得重复用于同一 challenger 家族 | 隔离 |
| 5 | `judge_version` 变更记录必须存在且可回溯；judge 换版而未走 CR → 评测结果作废 | 口径 |
| 6 | 评测运行报告必含：run_id、契约版本指纹、回归矩阵、污染审计输出 | 证据 |

## 语义边界（本协议不负责什么）

- 不承诺"模型通用能力"结论——只裁决本轮冻结的目标维度与 guard 维度。
- 不接受任何形式的"再跑一个子集看看"：未列入 metrics 的维度不构成转正依据，也不构成否决依据（要加就 CR 到下一轮）。
