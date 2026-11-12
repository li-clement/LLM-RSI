# Knowledge 平面规则

Knowledge 平面承载**组织记忆**：术语、能力边界、决策、模式、坑点、操作步骤。它不是 wiki 的替代品，而是**可被人和 Agent 按 ID 检索、有生命周期、有消费责任**的结构化资产。

## 目录与类型

| 目录 | type | 说明 |
|---|---|---|
| `domain/` | `glossary` | 跨 BU 统一语言（CONTEXT.md），术语仲裁唯一源 |
| `capabilities/` | `capability` | BU 能力卡：提供哪些契约、边界、非目标 |
| `decisions/` | `decision` | ADR：为什么这样选。不可过期，只能被取代 |
| `patterns/` | `pattern` | 可复用解法 |
| `pitfalls/` | `pitfall` | 已知陷阱 + 探测法 + 预防（流水线怎么拦） |
| `runbooks/` | `runbook` | 可照做的步骤（发布、应急、回滚） |

## Frontmatter 元数据 schema（check.py 强制）

```yaml
id: PAT-001            # <类型码>-<num>：ADR/PAT/PIT/RB/CARD/DOM
type: pattern          # 与目录对应
title: Champion–Challenger 转正模式
scope: cross-bu        # cross-bu | bu:<code> | team:<name>
confidence: high       # high（多循环验证过） | medium（单来源） | low（推测）
status: accepted       # candidate | accepted | retired
owner: "@curator-model" # 复核责任人（Curator 或领域负责人）
provenance: [RUN-2026-1104, INC-RSI-002]   # 出处，必须有
expires: 2027-06-30    # TTL；decision 无此字段，用 status: superseded
```

## 生命周期

```
（人/Agent 产生）candidate ──Curator 复核──► accepted ──┬──到期──► 重新复核（复核前 check 报错）
                                                       └──被取代──► retired/superseded
```

- **TTL 默认**：glossary/capability/runbook 90 天；pattern/pitfall 180 天；decision 无 TTL。
- **消费即续约**：被新冻结的 Feature 引用的知识项，复核时默认延长一个 TTL。
- **无消费则点名**：`check.py stats` 报告 90 天内未被任何 Spec 工件引用的 accepted 知识项。
- **单一事实源**：契约字段、状态机细节一律引用 ID（如"幂等语义见 ADR-0001"），不得复制正文。违反会被评审打回。

## Agent 与知识

- Agent 执行前必须加载 Feature `knowledge:` 清单中的全部条目（AGENTS.md §2）。
- Agent 只能产出 `status: candidate`，`provenance` 标注 `agent:<playbook>@<run>`；转正需 Curator。
- 度量：知识新鲜度（未过期占比 ≥90%）、知识消费率、Agent 候选知识采纳率——见 MODE.md §8。
