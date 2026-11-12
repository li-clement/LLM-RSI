---
id: S-019
kind: contract
contract: MID-HEALTH.v1
status: accepted
executable: true
runner: "observability-repo/contract-tests/mid-health"
---

# S-019 MID-HEALTH 契约场景（中训练/长上下文扩展监控可信）

| # | 断言 | 层级 |
|---|---|---|
| 1 | needle 探针按 context 分桶自动随 run 运行，`mid_needle_recall_by_ctx` 达标才可进入下一课程段（分桶阈值随课程收紧属参数级） | 门禁 |
| 2 | `mid_position_scheme_reg_rate == 1.0`：RoPE/外推参数 hash 100% 登记进 MDL-CKPT——换位置方案未登记 = 交接无效 | 门禁 |
| 3 | `mid_data_mix_highq_share` 与 CORP manifest 对账一致（只搬运，不另算——单一事实源） | 数据 |
| 4 | 长短能力保持对账：`mid_shortctx_regression` 违例 → 触发 EVAL-BENCH 短 ctx 维度加测（G3 证据附件） | 治理 |
| 5 | annealing LR/mix 权重调优实验登记指纹；改 mix **定义**走 CR（口径级） | 流程 |

**义务**：MODEL 出 run 级快照 `mid-profile.json`；DATA 将 needle 探针题集纳管（防泄漏进语料）。
