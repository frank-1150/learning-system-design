---
chapterId: ch10
part: "Part III · 派生数据"
order: 102
title: "设计分布式 Join 与 MapReduce"
questionType: "mechanism"
sourcePages: "PDF 407-460"
walkthroughPath: "/chapters/batch-processing"
description: "基于 DDIA Chapter 10 的底层机制题完整解答"
---

# 设计分布式 Join 与 MapReduce

<div class="question-meta"><span>Ch10</span><span>底层机制题</span><span>中高级</span></div>

## 题干

设计支持 reduce-side join、map-side join 和倾斜处理的批计算执行器。

<ProgressToggle id="question-distributed-join" label="完成本题" />

::: tip 练习方式
先用 5 分钟写出澄清问题和两个关键不变量，再逐步展开答案。面试官关心的是你的决策依据，不是组件数量。
:::

## 参考答案

<AnswerStep title="1. 候选人澄清问题">

明确需要提供的抽象与不变量、故障模型、持久性边界、并发规模，以及调用者是否能够重试。

- 规模基线：输入 20PB、10 万 task、key 基数 10 亿、最大热 key 占 4%。
- 追问数据是否允许丢失、重复或短暂陈旧，以及降级时必须保留的最小体验。

</AnswerStep>

<AnswerStep title="2. 功能与非功能需求">

**功能范围**：提供稳定接口；在节点或进程故障后恢复；支持在线扩容和观测；用测试证明核心不变量。

**非功能目标**：把题目中的规模转成吞吐、存储、带宽、尾延迟和恢复目标；所有目标都标明量级与假设，而不是给出没有依据的精确数字。

</AnswerStep>

<AnswerStep title="3. 容量估算">

以 `输入 20PB、10 万 task、key 基数 10 亿、最大热 key 占 4%` 为容量基线。先按峰均比 5 倍预留入口吞吐，再计算 `日增量 = 峰值写入 × 平均对象大小 × 有效写入秒数`。副本、索引、WAL/日志和压缩前空间分别计入，生产容量至少保留 30% 运维余量。

面试中应明确：缓存按工作集而非全量数据估算；网络同时考虑复制、再均衡和恢复流量；P99 容量不能只用平均 QPS 推导。

</AnswerStep>

<AnswerStep title="4. API 与数据模型">

**核心接口**：SubmitDAG；MapTask(split)；ShuffleFetch(partition)；CommitAttempt。

**核心数据**：shuffle_block(job,map,partition,checksum)；task_attempt(state,worker,output)。

所有修改接口携带 `request_id` 或幂等键；游标包含稳定排序键而不是裸 offset；数据记录保留版本/epoch，便于检测旧写、回放和在线迁移。

</AnswerStep>

<AnswerStep title="5. 高层架构">

1. **Scheduler 数据本地放置 map；分区排序写 shuffle；reducer 拉取同分区；Output Committer 选唯一 attempt**

入口层只做鉴权、限流和路由；状态所有权、顺序和提交边界必须在图上标清。异步路径暴露 lag、水位和失败队列，不能用“最终一致”四个字跳过恢复设计。

</AnswerStep>

<AnswerStep title="6. 关键机制">

- Partitioner 与外部排序
- Broadcast/map-side join
- Skew key sampling 与 salting

这些机制分别回答三类问题：如何确定顺序或所有权、如何在失败后重试而不重复生效、如何在扩容或迁移期间保持可观测且可回滚。

</AnswerStep>

<AnswerStep title="7. 扩展、故障与恢复">

- 热 reducer
- 重复 attempt 重复发布
- shuffle 文件丢失

故障处理顺序应是：保护正确性 → 限制影响面 → 恢复核心流量 → 修复派生状态 → 完成复盘。为每个异步边界设置积压告警，为每个所有权变更设置 epoch/fencing，为每个重试路径设置预算和幂等性。

</AnswerStep>

<AnswerStep title="8. 核心权衡">

Reduce-side join 通用但网络大；map-side join 快但要求输入预分区或小表可广播。

没有“同时最强”的设计。最终选择应回扣题目的 SLO、故障模型、团队运维能力和成本，并说明什么时候需要从当前方案演进到下一阶段。

</AnswerStep>

<AnswerStep title="9. 面试官追问">

- 推测执行如何避免副作用？
- Worker 丢失如何恢复？
- 多阶段 DAG 怎么缓存？

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

本题主要对应 Chapter 10 **Batch Processing**，源 PDF 第 407-460 页。答案结合了原书概念与原创生产化设计，不代表原书提供了该题的唯一解法。
