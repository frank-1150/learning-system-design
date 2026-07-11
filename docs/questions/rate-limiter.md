---
chapterId: ch01
part: "Part I · 数据系统基础"
order: 12
title: "设计可扩展限流平台"
questionType: "mechanism"
sourcePages: "PDF 25-48"
walkthroughPath: "/chapters/reliable-scalable-maintainable"
description: "基于 DDIA Chapter 1 的底层机制题完整解答"
---

# 设计可扩展限流平台

<div class="question-meta"><span>Ch1</span><span>底层机制题</span><span>中高级</span></div>

## 题干

设计供数百个微服务共享的限流控制面与本地数据面。

<ProgressToggle id="question-rate-limiter" label="完成本题" />

::: tip 练习方式
先用 5 分钟写出澄清问题和两个关键不变量，再逐步展开答案。面试官关心的是你的决策依据，不是组件数量。
:::

## 参考答案

<AnswerStep title="1. 候选人澄清问题">

明确需要提供的抽象与不变量、故障模型、持久性边界、并发规模，以及调用者是否能够重试。

- 规模基线：100 万规则、峰值 500 万次判定/秒、单次判定 P99 < 2ms。
- 追问数据是否允许丢失、重复或短暂陈旧，以及降级时必须保留的最小体验。

</AnswerStep>

<AnswerStep title="2. 功能与非功能需求">

**功能范围**：提供稳定接口；在节点或进程故障后恢复；支持在线扩容和观测；用测试证明核心不变量。

**非功能目标**：把题目中的规模转成吞吐、存储、带宽、尾延迟和恢复目标；所有目标都标明量级与假设，而不是给出没有依据的精确数字。

</AnswerStep>

<AnswerStep title="3. 容量估算">

以 `100 万规则、峰值 500 万次判定/秒、单次判定 P99 < 2ms` 为容量基线。先按峰均比 5 倍预留入口吞吐，再计算 `日增量 = 峰值写入 × 平均对象大小 × 有效写入秒数`。副本、索引、WAL/日志和压缩前空间分别计入，生产容量至少保留 30% 运维余量。

面试中应明确：缓存按工作集而非全量数据估算；网络同时考虑复制、再均衡和恢复流量；P99 容量不能只用平均 QPS 推导。

</AnswerStep>

<AnswerStep title="4. API 与数据模型">

**核心接口**：Check(key, rule_id, cost)；控制面发布 RuleSnapshot(version, rules)。

**核心数据**：rule(id, scope, algorithm, limit, window, version)；counter(key, bucket, value, expires_at)。

所有修改接口携带 `request_id` 或幂等键；游标包含稳定排序键而不是裸 offset；数据记录保留版本/epoch，便于检测旧写、回放和在线迁移。

</AnswerStep>

<AnswerStep title="5. 高层架构">

1. **管理 API**
2. **版本化规则存储**
3. **配置分发；服务内 sidecar/local library 执行判定，必要时访问分片计数器**

入口层只做鉴权、限流和路由；状态所有权、顺序和提交边界必须在图上标清。异步路径暴露 lag、水位和失败队列，不能用“最终一致”四个字跳过恢复设计。

</AnswerStep>

<AnswerStep title="6. 关键机制">

- Token Bucket 与滑动窗口
- 本地额度租约
- 规则版本与故障时 fail-open/fail-closed

这些机制分别回答三类问题：如何确定顺序或所有权、如何在失败后重试而不重复生效、如何在扩容或迁移期间保持可观测且可回滚。

</AnswerStep>

<AnswerStep title="7. 扩展、故障与恢复">

- 集中计数器过载
- 配置推送延迟
- 时钟窗口边界突刺

故障处理顺序应是：保护正确性 → 限制影响面 → 恢复核心流量 → 修复派生状态 → 完成复盘。为每个异步边界设置积压告警，为每个所有权变更设置 epoch/fencing，为每个重试路径设置预算和幂等性。

</AnswerStep>

<AnswerStep title="8. 核心权衡">

精确全局配额更公平但增加远程协调；本地租约牺牲少量精度换低延迟。

没有“同时最强”的设计。最终选择应回扣题目的 SLO、故障模型、团队运维能力和成本，并说明什么时候需要从当前方案演进到下一阶段。

</AnswerStep>

<AnswerStep title="9. 面试官追问">

- 多地域配额如何分配？
- VIP 用户如何覆盖规则？
- 如何灰度新规则？

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

本题主要对应 Chapter 1 **Reliable, Scalable, and Maintainable Applications**，源 PDF 第 25-48 页。答案结合了原书概念与原创生产化设计，不代表原书提供了该题的唯一解法。
