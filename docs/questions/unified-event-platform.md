---
chapterId: ch12
part: "Part III · 派生数据"
order: 121
title: "设计统一事件驱动数据平台"
questionType: "product"
sourcePages: "PDF 511-574"
walkthroughPath: "/chapters/future-data-systems"
description: "基于 DDIA Chapter 12 的产品系统题完整解答"
---

# 设计统一事件驱动数据平台

<div class="question-meta"><span>Ch12</span><span>产品系统题</span><span>中高级</span></div>

## 题干

设计以事实日志连接交易库、搜索、推荐、缓存和数仓的数据平台。

<ProgressToggle id="question-unified-event-platform" label="完成本题" />

::: tip 练习方式
先用 5 分钟写出澄清问题和两个关键不变量，再逐步展开答案。面试官关心的是你的决策依据，不是组件数量。
:::

## 参考答案

<AnswerStep title="1. 候选人澄清问题">

确认核心用户旅程、读写比例、数据保留、地域范围、延迟 SLO、一致性需求，以及哪些功能允许降级。

- 规模基线：每日 50 万亿事件、5000 topic、2000 消费组、保留 30 天。
- 追问数据是否允许丢失、重复或短暂陈旧，以及降级时必须保留的最小体验。

</AnswerStep>

<AnswerStep title="2. 功能与非功能需求">

**功能范围**：先覆盖核心写入与读取路径，再加入扩展、治理与恢复能力；非核心功能不应污染第一版关键路径。

**非功能目标**：把题目中的规模转成吞吐、存储、带宽、尾延迟和恢复目标；所有目标都标明量级与假设，而不是给出没有依据的精确数字。

</AnswerStep>

<AnswerStep title="3. 容量估算">

以 `每日 50 万亿事件、5000 topic、2000 消费组、保留 30 天` 为容量基线。先按峰均比 5 倍预留入口吞吐，再计算 `日增量 = 峰值写入 × 平均对象大小 × 有效写入秒数`。副本、索引、WAL/日志和压缩前空间分别计入，生产容量至少保留 30% 运维余量。

面试中应明确：缓存按工作集而非全量数据估算；网络同时考虑复制、再均衡和恢复流量；P99 容量不能只用平均 QPS 推导。

</AnswerStep>

<AnswerStep title="4. API 与数据模型">

**核心接口**：Publish(event, schema_id)；Subscribe(topic,offset)；RegisterProjection；Replay(range)。

**核心数据**：event_id、aggregate_id/version、schema_id、source_txn、lineage；projection 记录 input offsets/code version。

所有修改接口携带 `request_id` 或幂等键；游标包含稳定排序键而不是裸 offset；数据记录保留版本/epoch，便于检测旧写、回放和在线迁移。

</AnswerStep>

<AnswerStep title="5. 高层架构">

1. **业务库 + Outbox/CDC**
2. **分区日志**
3. **Schema/Lineage Catalog**
4. **多个投影**
5. **对账平台**

入口层只做鉴权、限流和路由；状态所有权、顺序和提交边界必须在图上标清。异步路径暴露 lag、水位和失败队列，不能用“最终一致”四个字跳过恢复设计。

</AnswerStep>

<AnswerStep title="6. 关键机制">

- 单一事实源与派生视图
- 事务 outbox
- 血缘、版本和可重建性

这些机制分别回答三类问题：如何确定顺序或所有权、如何在失败后重试而不重复生效、如何在扩容或迁移期间保持可观测且可回滚。

</AnswerStep>

<AnswerStep title="7. 扩展、故障与恢复">

- 循环事件
- 投影静默落后
- 重放污染在线结果

故障处理顺序应是：保护正确性 → 限制影响面 → 恢复核心流量 → 修复派生状态 → 完成复盘。为每个异步边界设置积压告警，为每个所有权变更设置 epoch/fencing，为每个重试路径设置预算和幂等性。

</AnswerStep>

<AnswerStep title="8. 核心权衡">

中心事件平台降低点对点耦合，但必须避免把所有业务语义和查询都塞进 broker。

没有“同时最强”的设计。最终选择应回扣题目的 SLO、故障模型、团队运维能力和成本，并说明什么时候需要从当前方案演进到下一阶段。

</AnswerStep>

<AnswerStep title="9. 面试官追问">

- 跨 topic 事务？
- 成本分摊？
- 事件保留到期后如何重建？

</AnswerStep>

<AnswerStep title="10. 评分点">

| 维度 | 合格 | 优秀 |
| --- | --- | --- |
| 需求 | 能确认核心路径与规模 | 主动定义不变量、SLO 与降级边界 |
| 数据 | 给出可用模型与索引 | 解释版本、幂等、迁移和删除 |
| 架构 | 组件能串成完整路径 | 明确状态、顺序、背压和所有权 |
| 分布式权衡 | 知道复制、分区或事务概念 | 能把保证与延迟、可用性、成本对应 |
| 故障处理 | 能列举常见失败 | 有检测、隔离、恢复、对账和演练闭环 |

</AnswerStep>

## 对应 DDIA 知识

本题主要对应 Chapter 12 **The Future of Data Systems**，源 PDF 第 511-574 页。答案结合了原书概念与原创生产化设计，不代表原书提供了该题的唯一解法。
