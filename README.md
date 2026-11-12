# TriPlane · 三平面协同模式工具箱

面向**多 BU / 跨部门高效协同开发**的可落地模式：**Spec 平面（SDD）× Knowledge 平面（知识工程）× Execution 平面（流水线与门禁）**，AI Agent 为一等公民。

- 完整设计读 [MODE.md](MODE.md)
- Agent 入口读 [AGENTS.md](AGENTS.md)

## 三平面一图

```
 Spec 平面（意图与边界）──冻结契约──► Execution 平面（验证与交付）
      ▲                                      │
      └────────知识滋养──── Knowledge 平面 ◄───┘（经验回流）
```

## 快速上手（3 步）

```bash
# 1. 校验整个三平面一致性（这也是 CI 门禁 G1 的内容）
python3 tools/check.py

# 2. 看三平面健康度仪表盘（契约/场景覆盖率、知识新鲜度）
python3 tools/check.py stats

# 3. 新建工件：从模板复制，ID 命名规则见 specs/README.md
cp templates/feature-spec.md specs/features/F-2026-002-xxx.md
```

无外部依赖，仅 Python 3.9+ 标准库。

## 目录导航

| 目录 | 内容 | 平面 |
|---|---|---|
| [specs/](specs/README.md) | 工件链规则、状态机、命名、版本策略 + 一套端到端示例 | Spec |
| [knowledge/](knowledge/README.md) | 六类知识资产的元数据 schema、生命周期、回流规则 + 示例 | Knowledge |
| [pipelines/](pipelines/README.md) | 四流水线模型、五道门禁、CI 配置示例 | Execution |
| [agents/playbooks.md](agents/playbooks.md) | 7 个流水线内嵌 Agent 的任务书 | 跨平面 |
| [templates/](templates/) | 六类工件模板 | — |
| [tools/check.py](tools/check.py) | 三平面一致性校验器 | — |

## 示例场景

示例用"下单—支付闭环"跨 `MID`（交易中台部）与 `PAY`（支付部）两个 BU 协作，完整展示 Epic → Feature → 3 个契约 → 3 个场景 → ADR/模式/坑点/Runbook/能力卡 的引用咬合关系，可作为试点第一周的填空范本。
