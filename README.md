# TriPlane · 三平面协同模式工具箱（RSI 适配）

面向**跨数据团队（DATA）与模型团队（MODEL）的递归自我改进（RSI）项目**的可落地模式：**Spec 平面（SDD）× Knowledge 平面（知识工程）× Execution 平面（流水线与门禁）**，AI Agent——含 RSI 循环自身的改进提案——为一等公民。

- 模式设计读 [MODE.md](MODE.md)
- **明天怎么开工读 [GUIDE.md](GUIDE.md)**（按角色导航、14 天冷启动、日常操作流、报错对照）
- Agent 入口读 [AGENTS.md](AGENTS.md)

## 三平面一图

```
 Spec 平面（意图与边界）──冻结契约──► Execution 平面（验证与交付）
      ▲                                      │
      └────────知识滋养──── Knowledge 平面 ◄───┘（经验回流）
```

## 快速上手（3 步）

> 正式部署（把示例换成你们团队的真实工件）按 [GUIDE.md §2 冷启动 14 天](GUIDE.md) 操作。

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
| [specs/](specs/README.md) | 工件链规则、状态机、命名、六类契约与版本策略 + 端到端示例 | Spec |
| [knowledge/](knowledge/README.md) | 六类知识资产的元数据 schema、生命周期、回流规则 + 示例 | Knowledge |
| [pipelines/](pipelines/README.md) | 四流水线模型（含 P3 评测收敛）、五道门禁、CI 配置示例 | Execution |
| [observability/](observability/README.md) | 监控体系 + 三层 profiling 调优 + dashboard-as-code | Execution |
| [agents/playbooks.md](agents/playbooks.md) | 8 个流水线内嵌 Agent 的任务书 + RSI 自提案治理 | 跨平面 |
| [templates/](templates/) | 七类工件模板（含 metric 契约） | — |
| [tools/check.py](tools/check.py) | 三平面一致性校验器（含指标/看板引用校验） | — |

## 示例场景

示例用**一个完整的 RSI 改进循环**（目标维度：工具调用成功率）跨 `DATA`（数据团队）/ `MODEL`（模型团队）/ `AGENT`（Agent 平台团队）协作，完整展示：循环规格（Feature）→ 循环四类契约（轨迹事件 / 训练集 / 评测协议 / 模型服务）+ 项目级三指标契约（数据开发 / 模型训练 / 飞轮健康）→ 八个场景（污染阻断、评测复现、champion 转正、熔断回滚、自提案治理、监控可信）→ 三权分立 ADR / champion–challenger 模式 / 污染坑点 / 发布 Runbook / 能力卡的引用咬合关系，可作为试点第一周的填空范本。
