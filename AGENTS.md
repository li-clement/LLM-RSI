---
id: AGENTS-ENTRY
mode: triplane/0.2
status: accepted
owner: rsi-governance-committee
---

# AGENTS.md — Agent 工作契约

任何 AI Agent（IDE 结对、流水线内嵌、评审助手）进入本仓库前必须读完本文件。本文件定义你在这个模式里的读取路径、产出规则与权限边界。

## 1. 你在哪个模式里

三平面协同模式（见 [MODE.md](MODE.md)，RSI 适配）：Spec 平面承载意图与契约（六类：dataset/event/api/eval/model/**metric**），Knowledge 平面承载经验与决策（含**负结果**），Execution 平面承载证据（含可观测子系统）。三个平面通过 **ID 引用**咬合，通过 `tools/check.py` 校验一致性。

**RSI 项目的特别约定：改进循环自身（模型生成的 mix 提案、训练补丁、接口变更草稿）也是一个 Agent**——同等受本文件三闸门约束，provenance 标注 `model:<version>@<episode>`。允许递归，禁止换尺子。

## 2. 上下文加载顺序（固定，不得跳步）

1. `python3 tools/check.py` —— 先拿三平面一致性报告，带病上下文不可开工。
2. 任务涉及的 **Contract**（`specs/contracts/`，读 `x-contract` 元数据与 schema 本体）。
3. 相关 BU 的 **能力卡**（`knowledge/capabilities/`）与**术语表**（`knowledge/domain/CONTEXT.md`）。
4. 相关 **ADR / pattern / pitfall**（按 Feature 的 `knowledge:` 引用清单加载）。
5. 最后才读业务代码仓库。

## 3. 你可以做的（起草与验证）

- 生成/修改 Feature、Scenario、契约草稿、CR 草稿 → 状态一律 `draft`，开 PR。
- 契约变更影响分析、兼容性 diff 报告（按 [agents/playbooks.md](agents/playbooks.md) 的模板输出）。
- 从 Scenario 生成可执行测试骨架；从 CR 草稿生成契约测试补丁建议。
- 从 diff/事故材料/**循环 run 证据（含失败循环）**抽取**候选**知识项（`status: candidate`，`provenance: agent:<playbook>@<run>`）。
- 代表 RSI 自提案开 **draft CR**（mix 建议、训练配置补丁、接口变更草稿）——只到 CR §1–§3，不得填写批准节。

## 4. 你不可以做的（权限三闸门）

- **不得批准**任何状态跃迁（approved / frozen / accepted / KB）。
- **不得修改** `frozen` 状态的契约本体（只能起草 CR）。
- **不得发布**知识项（只有 Knowledge Curator 可把 candidate 提升为 accepted）。
- **不得修改评测协议（`EVAL-*`）的指标定义与阈值**——任何变更一律破坏性，只有治理委员会可批（ADR-0001）。
- 不得在产出中复制契约事实到知识库正文——只引用 ID（单一事实源）。

## 5. 产出落盘规则

| 你的产出 | 落盘位置 | 命名 |
|---|---|---|
| Feature / Epic 草稿 | `specs/features/` `specs/epics/` | 见 specs/README.md ID 规则 |
| 契约 / CR | `specs/contracts/` | `<域码>-<动作>.v<N>.<flavor>.json` |
| 场景 | `specs/scenarios/` | `S-<num>-*.md` |
| 候选知识 | `knowledge/<type>/` | frontmatter `status: candidate` |
| 分析报告 | PR 评论 / `pipelines/` 产物目录 | 必须引用被分析工件的 ID |

所有 markdown 工件必须带 frontmatter 元数据（模板见 [templates/](templates/)），否则 `check.py` 会拒绝合并。报告中引用监控数字必须解析到 `*.metric.json` 契约的指标 ID，**裸名指标禁止**；仪表盘面板只能引用已注册指标（`observability/dashboards/` 由 check.py 校验）。

## 6. 术语以谁为准

跨 BU 术语歧义时，[knowledge/domain/CONTEXT.md](knowledge/domain/CONTEXT.md) 是唯一仲裁源；它没有的词不要自造，提 CR 给 Curator。
