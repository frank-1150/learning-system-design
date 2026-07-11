---
chapterId: ch11
part: "Part III · 派生数据"
order: 111
title: "设计实时风控与指标平台"
questionType: "product"
sourcePages: "PDF 461-510"
walkthroughPath: "/chapters/stream-processing"
description: "基于 DDIA Chapter 11 的产品系统题完整解答"
---

# 设计实时风控与指标平台

<div class="question-meta"><span>Ch11</span><span>产品系统题</span><span>中高级</span></div>

## 题干

设计支付事件的实时风控、分钟指标和可回放审计平台。

<ProgressToggle id="question-realtime-risk-metrics" label="完成本题" />

::: tip 练习方式
先用 5 分钟写出澄清问题和两个关键不变量，再逐步展开答案。面试官关心的是你的决策依据，不是组件数量。
:::

## 参考答案

<AnswerStep title="1. 候选人澄清问题">

确认核心用户旅程、读写比例、数据保留、地域范围、延迟 SLO、一致性需求，以及哪些功能允许降级。

- 规模基线：峰值 200 万事件/秒、规则延迟 P99 < 100ms、保留 30 天可回放。
- 追问数据是否允许丢失、重复或短暂陈旧，以及降级时必须保留的最小体验。

</AnswerStep>

<AnswerStep title="2. 功能与非功能需求">

**功能范围**：先覆盖核心写入与读取路径，再加入扩展、治理与恢复能力；非核心功能不应污染第一版关键路径。

**非功能目标**：把题目中的规模转成吞吐、存储、带宽、尾延迟和恢复目标；所有目标都标明量级与假设，而不是给出没有依据的精确数字。

</AnswerStep>

<AnswerStep title="3. 容量估算">

以 `峰值 200 万事件/秒、规则延迟 P99 < 100ms、保留 30 天可回放` 为容量基线。先按峰均比 5 倍预留入口吞吐，再计算 `日增量 = 峰值写入 × 平均对象大小 × 有效写入秒数`。副本、索引、WAL/日志和压缩前空间分别计入，生产容量至少保留 30% 运维余量。

面试中应明确：缓存按工作集而非全量数据估算；网络同时考虑复制、再均衡和恢复流量；P99 容量不能只用平均 QPS 推导。

</AnswerStep>

<AnswerStep title="4. API 与数据模型">

**核心接口**：Ingest(event)；UpdateRules(version)；QueryMetric(window)；ExplainDecision(event_id)。

**核心数据**：event(event_id,account_id,event_time,payload)；feature(account,window,state)；decision(rule_version,reasons)。

所有修改接口携带 `request_id` 或幂等键；游标包含稳定排序键而不是裸 offset；数据记录保留版本/epoch，便于检测旧写、回放和在线迁移。

</AnswerStep>

<AnswerStep title="5. 高层架构">

1. **Gateway**
2. **分区日志**
3. **特征/窗口算子**
4. **规则引擎**
5. **决策 sink；原始事件进对象存储**

入口层只做鉴权、限流和路由；状态所有权、顺序和提交边界必须在图上标清。异步路径暴露 lag、水位和失败队列，不能用“最终一致”四个字跳过恢复设计。

</AnswerStep>

<AnswerStep title="6. 关键机制">

- 按账户分区
- 事件时间 watermark
- 规则与特征版本化

这些机制分别回答三类问题：如何确定顺序或所有权、如何在失败后重试而不重复生效、如何在扩容或迁移期间保持可观测且可回滚。

</AnswerStep>

<AnswerStep title="7. 扩展、故障与恢复">

- 迟到交易漏判
- 规则更新不一致
- 回放重复告警

故障处理顺序应是：保护正确性 → 限制影响面 → 恢复核心流量 → 修复派生状态 → 完成复盘。为每个异步边界设置积压告警，为每个所有权变更设置 epoch/fencing，为每个重试路径设置预算和幂等性。

</AnswerStep>

<AnswerStep title="8. 核心权衡">

同步风控延迟低但影响支付可用性；异步风控更稳健但只能事后处置部分风险。

没有“同时最强”的设计。最终选择应回扣题目的 SLO、故障模型、团队运维能力和成本，并说明什么时候需要从当前方案演进到下一阶段。

</AnswerStep>

<AnswerStep title="9. 面试官追问">

- 跨账户团伙识别？
- 规则回滚？
- 数据隐私如何处理？

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

本题主要对应 Chapter 11 **Stream Processing**，源 PDF 第 461-510 页。答案结合了原书概念与原创生产化设计，不代表原书提供了该题的唯一解法。
