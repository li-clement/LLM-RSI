---
id: S-006
kind: contract
contract: DQ-QUALITY.v1
status: accepted
executable: true
runner: "observability-repo/contract-tests/dq-quality"
---

# S-006 DQ-QUALITY 契约场景（消费方 MODEL 的期望：数据侧监控可信）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 每个指标 ID 必须能解析到一个采集器实现（binding 表），CI 缺绑定即红 | 可观测性 |
| 2 | 带 `binds` 的指标（如 `dq_eval_leak_count`）必须搬运 CORP-PRETRAIN / SFT-PAIRS 断言的原始输出，**不得二次计算**（双实现必然漂移） | 单一事实源 |
| 3 | 每个指标要么有 `slo` 要么标 `informational: true`——没有阈值的指标只是数字 | 语义 |
| 4 | 告警路由（alert）与能力卡 contact 一致；crit 级告警自动挂到 G3 证据 | 门禁联动 |
| 5 | 指标定义文本或 slo 变更的 PR：标题必须含 CR-，minor 递增；删除指标 = 破坏性 | 兼容性 |
| 6 | board 面板引用的每个 metric 必须在本契约注册（check.py 自动校验） | 仪表盘 |

## 消费方（MODEL）义务

- 训练配置引用的数据质量结论必须来自本契约指标 ID（如按 `dq_dedup_rate` 决定过滤），不得读批次目录里的自由格式报告。
