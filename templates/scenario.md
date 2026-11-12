# Scenario 模板（验收 / 契约两种）

## 验收场景（端到端循环行为）

````markdown
---
id: S-<num>
kind: acceptance
feature: F-<year>-<num>
status: accepted
executable: true             # false 时 P3 不执行，仅评审用
runner: "<评测/集成套件标识>" # assertion-forge Agent 按此生成骨架
---

# S-<num> <标题>

```gherkin
Feature: <循环规格标题>
  Scenario: 正常循环——挑战者满足三件套转正
  Scenario: 污染阻断——泄漏即出局
  Scenario: 换尺子拦截——阈值/judge 变更未获批
  Scenario: 失败循环也要完整归档（负结果回流）
  Scenario: 灰度熔断与回滚
  Scenario: 自提案治理——只进 draft CR
```

## 覆盖声明
- 覆盖 Feature 验收口径：<引用>
- 依赖知识：<ID 列表>
````

## 契约场景（工件级行为断言）

````markdown
---
id: S-<num>
kind: contract
contract: <ID>.v<N>
status: accepted
executable: true
runner: "<团队仓库中的测试实现路径>"
---

# S-<num> <契约ID> 契约场景（<提供方|消费方>期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | schema：必填/类型/枚举边界 | schema |
| 2 | SLA / 预算：cadence、freshness、体量、时延成本上限 | SLA（dataset/model） |
| 3 | 质量：去重、lineage 完备、合成占比、污染计数=0 | 质量（block 级） |
| 4 | 口径绑定：judge_version / 契约版本指纹随产物传输 | 可复现 |
| 5 | 语义边界：本契约**不负责**什么（写出来防扯皮） | 语义 |
| 6 | 兼容性：新增可选字段不破坏既有消费方；删除/收窄=破坏 | 兼容性 |

## 反例（必须失败）
- 读"最新批次"不引用版本；双跑用不同 judge_version；shadow 期 challenger 接触评测分布……
````

## 编写要点

- 断言写成**可判真伪且机器可执行**的句子；"尽量""明显变好"等词会被评审打回。
- dataset 契约场景必须含污染断言（`eval_leak_count == 0`），这是 RSI 场景的硬性要求。
- 每个契约 ≥1 个契约场景（check.py 强制）；每个 Feature ≥1 个验收场景。
