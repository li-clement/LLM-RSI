# 契约变更请求（CR）模板

> PR 标题：`CR-<num>: <契约ID> <一句话变更>`。G1 门禁要求契约文件的任何变更 PR 标题含 CR 编号。

```markdown
## 1. 变更动机
为什么必须变（业务触发点 / 事故 / 技术债），引用 Epic/Feature/事故 ID。

## 2. 变更内容与分类
- 契约：`<ID>.v<N>`，kind/flavor：dataset(schema) / event(asyncapi) / api(openapi) / eval / model
- 分类：**非破坏**（minor/patch 递增） 或 **破坏性**（新 major）
- 破坏性判定不靠自评：附 json-schema-diff / oasdiff 输出（P1 会重跑，工具结论优先）
- **eval 契约例外**：指标定义、阈值、judge 版本、holdout 构成的任何变更一律按破坏性处理，PR 描述必须带治理委员会决议编号（RES-<num>）

## 3. 影响分析（contract-impact Agent 预生成草稿 + 人确认）
| 消费方团队 | 波及系统（管道/训练配置/评测 harness） | 需要改动？ | 在跑循环是否受影响 | 负责人确认 |
|---|---|---|---|---|
| ... | ... | ... | ☐ | ☐ |

## 4. 兼容与迁移方案（破坏性必填）
- 双跑窗口：旧 `v<N>` 标记 deprecated + `sunset: <date>`（≥90 天后）；数据集类变更需给出**旧批次可重放**路径
- 新消费方接入指引；旧版本退场验收标准
- 回滚步骤：链接或更新 RB-xxx

## 5. 测试义务
- [ ] 新/改契约场景（S-xxx）已提交，含兼容性断言
- [ ] test-weaver 生成的消费方 CDC 补丁 PR 已被各消费方合并或显式拒绝

## 6. 批准
- 提供方 Steward（Dataset/Eval/Model 按 kind）：☐
- 每个 consumer 团队代表：☐
- 破坏性变更追加：治理委员会决议编号（RES-<num>）：____
- eval 契约：无论 schema 是否兼容，均按破坏性走委员会

## 7. 知识回流
- [ ] 本 CR 产生的经验已成候选知识项（ID：____，status: candidate）
```

## 状态联动

1. CR 批准 → 契约文件变更合入（`v<N+1>` 新建 + 旧转 deprecated）；
2. 受影响 Feature 的 `contracts:` 引用需要更新（同 PR 或 follow-up PR，check.py 保证引用有效）；
3. CR 关闭 ≠ 结束——`sunset` 之前每季盘点旧版本消费流量（stats 报告点名）。
