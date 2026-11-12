# 知识项模板（pattern / pitfall / runbook 通用）

```markdown
---
id: <PAT|PIT|RB|DOM>-<num>
type: pattern            # pattern | pitfall | runbook | glossary
title: <检索友好的名称>
scope: cross-bu          # cross-bu | bu:<code> | team:<name>
confidence: medium       # high（多场景验证过） | medium（单来源） | low（推测）
status: candidate        # Agent 或新人产出一律从 candidate 开始
owner: "@<复核责任人>"
provenance: [<事故/MR/评审标识>]   # 必填，无出处不收
expires: <YYYY-MM-DD>    # 按类型 TTL：RB/glossary 90d，PAT/PIT 180d
---

# <ID> <标题>

## （pattern）何时用 / 怎么做 / 反模式 / 怎么验证
## （pitfall）故事（发生了什么）/ 破坏分类 / 探测：流水线怎么拦 / 预防
## （runbook）触发条件 / 步骤（编号，可直接照做）/ 回滚 / 应急通道
```

## Curator 复核清单（candidate → accepted）

- [ ] 出处可追（链接/编号有效）
- [ ] 与既有知识不重叠（重叠 → 合并并在被合并项留 `见 <ID>`）
- [ ] 不复制 Spec 平面事实（字段、状态机 → 只引用契约 ID）
- [ ] 可消费性：能想到 ≥1 个未来 Feature 会引用它；想不到 → 拒绝
- [ ] 探测/验证方式具体到"哪个流水线的哪个 job 能拦"

## Agent 生成候选的额外要求

`provenance` 追加 `agent:<playbook>@<pipeline-run-id>`；`confidence` 上限 `medium`（Agent 没有跨场景验证的资格，升 high 需人工）。
