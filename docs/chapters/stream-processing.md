---
chapterId: ch11
part: "Part III · 派生数据"
order: 11
title: "Ch11 · 流处理"
titleZh: "流处理"
titleEn: "Stream Processing"
sourcePages: "PDF 461-510"
walkthroughPath: "/chapters/stream-processing"
questionPaths:
  - /questions/realtime-risk-metrics
  - /questions/exactly-once-stream
  - /questions/stream-backpressure-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 11 章交互式中文导读"
---

# Ch11 · 流处理

<p class="chapter-subtitle">Stream Processing</p>

> **阅读范围**：DDIA 第一版 Chapter 11，源 PDF 第 461-510 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-11" label="完成本章" />

## 问题背景

流是随时间追加的事件序列。分区日志把消息持久化并允许消费者重放；正确处理事件时间、窗口、状态快照和端到端幂等，才能把实时计算从消息搬运升级为可靠数据系统。

## 核心模型

- 日志型 broker 以 offset 表达消费位置并支持重放
- CDC 把数据库提交日志转成变更流
- 事件时间与处理时间会因网络和暂停产生差异
- exactly-once 通常来自事务性状态与幂等输出的组合

<WalkthroughExplorer :chapter="11" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

消息队列 → 持久分区日志 → 有状态算子 → watermark 与窗口 → checkpoint → 事务性 sink → 回放和版本化重算。

## 生产案例

实时风控按账户分区保持顺序，用事件时间窗口聚合支付行为。规则版本和特征快照与告警一起记录；迟到事件可更新尚未关闭的窗口，超过允许延迟则进入补偿流。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

把 broker 投递一次等同端到端 exactly-once；用处理时间计算业务窗口；提交 offset 后再写 sink；没有回放容量规划。

<KnowledgeCheck question="watermark 的作用是什么？" :options='["保证网络没有延迟", "估计事件时间进度并决定何时关闭窗口", "替代所有 checkpoint"]' :answer="1" explanation="watermark 表示系统认为不会再看到更早事件的进度估计，并非绝对保证。" />

## 本章面试题

1. [设计实时风控与指标平台](/questions/realtime-risk-metrics)
2. [设计 Exactly-Once 窗口处理器](/questions/exactly-once-stream)
3. [处理迟到数据、回放与背压](/questions/stream-backpressure-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 11, PDF pp. 461-510.
- 本文为中文学习笔记与原创交互重构，不替代原书。
