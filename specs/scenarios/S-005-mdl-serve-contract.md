---
id: S-005
kind: contract
contract: MDL-SERVE.v1
status: accepted
executable: true
runner: "agent-platform-repo/contract-tests/mdl-serve"
---

# S-005 MDL-SERVE 契约场景（消费方 AGENT 的期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | 响应必须携带 `model_version`；缺失即 AGENT 侧拒收（回流与灰度都依赖它归因） | schema |
| 2 | `x-budget` 三项（p99 时延 / 每 ktoken 成本 / 可用性 SLO）持续探针，超基线 2x×5min 触发熔断演练断言 | 预算 |
| 3 | 熔断后 60 秒内流量回到上一 champion（热备期内），探针用本契约断言本身 | 降级（RB-001） |
| 4 | 命中 `x-known_failures` 场景必须按 `x-fallback.out_of_scope` 声明降级，不得静默幻觉补全 | 语义边界 |
| 5 | 接口新增可选参数/响应字段不得破坏 AGENT 解析（回放既有请求样本） | 兼容性 |
| 6 | 删除参数、收窄 `tools` 支持面、更换默认 tokenizer 口径 = 破坏性 → 新 major 双跑 | 兼容性（PIT-001） |

## 消费方（AGENT）义务

- 埋点按 S-002 语义转发轨迹事件，不改写 `terminal_verdict`；
- 灰度流量分配必须可复现（分流规则 + 随机种子记录），否则 G5 观察无效。
