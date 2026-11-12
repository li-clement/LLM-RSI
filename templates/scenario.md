# Scenario 模板（验收 / 契约两种）

## 验收场景（端到端业务行为）

````markdown
---
id: S-<num>
kind: acceptance
feature: F-<year>-<num>
status: accepted
executable: true             # false 时 P3 不执行，仅评审用
runner: "<测试套件标识>"     # scenario-forge Agent 按此生成骨架
---

# S-<num> <标题>

```gherkin
Feature: <Feature 标题>
  Scenario: <正常路径>
  Scenario: <幂等/重复提交>
  Scenario: <超时与收敛>
  Scenario: <口径一致性（金额/时间/枚举）>
```

## 覆盖声明
- 覆盖 Feature 验收口径：<引用>
- 依赖知识：<ID 列表>
````

## 契约场景（接口级行为断言）

````markdown
---
id: S-<num>
kind: contract
contract: <ID>.v<N>
status: accepted
executable: true
runner: "<BU 仓库中的测试实现路径>"
---

# S-<num> <契约ID> 契约场景（<提供方|消费方>期望）

| # | 断言 | 层级 |
|---|---|---|
| 1 | schema：必填/类型/边界 | schema |
| 2 | 幂等与重试语义（PAT-001） | 行为 |
| 3 | 错误路径状态码 | 行为 |
| 4 | 语义边界（该契约不应承诺的事） | 语义 |
| 5 | 兼容性：新增可选字段不破坏既有消费方 | 兼容性 |

## 反例（必须失败）
- <常见偷懒实现>
````

## 编写要点

- 断言写成**可判真伪**的句子；"尽量""合理"等词会被评审打回。
- 语义边界行是跨部门防扯皮的关键：明确"这个契约不负责什么"。
- 每个契约 ≥1 个契约场景（check.py 强制）；每个 Feature ≥1 个验收场景。
