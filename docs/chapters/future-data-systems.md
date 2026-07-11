---
chapterId: ch12
part: "Part III · 派生数据"
order: 12
title: "Ch12 · 数据系统的未来"
titleZh: "数据系统的未来"
titleEn: "The Future of Data Systems"
sourcePages: "PDF 511-574"
walkthroughPath: "/chapters/future-data-systems"
questionPaths:
  - /questions/unified-event-platform
  - /questions/cdc-derived-views
  - /questions/privacy-deletion-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 12 章交互式中文导读"
---

# Ch12 · 数据系统的未来

<p class="chapter-subtitle">The Future of Data Systems</p>

> **阅读范围**：DDIA 第一版 Chapter 12，源 PDF 第 511-574 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-12" label="完成本章" />

## 问题背景

未来的数据架构不是一个万能数据库，而是围绕事实日志组合多个专用派生视图。正确性需要端到端审计和约束，数据使用还必须把隐私、目的限制与人的自主权纳入设计。

## 核心模型

- 系统记录事实，缓存、索引和数仓是派生视图
- CDC 和事件日志可连接异构存储并支持重建
- 端到端正确性需要审计数据流而非只信任单组件
- 隐私删除必须传播到所有派生数据和备份策略

<WalkthroughExplorer :chapter="12" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

点对点双写 → 单一事实源 → 变更日志 → 多个可重建投影 → 数据血缘 → 自动对账 → 隐私策略与删除事件贯穿全链路。

## 生产案例

统一事件平台保留订单事实，搜索、推荐、分析和缓存各自消费并建立投影。每个投影记录来源 offset、schema 与代码版本，从而支持回放、对账和定向删除。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

把流平台变成新的万能数据库；没有数据血缘；派生系统反向接受业务写入；只从主库删除个人数据却遗忘索引与离线特征。

<KnowledgeCheck question="派生视图最重要的恢复属性是什么？" :options='["只能在线更新", "可从事实源重建", "必须与事实源使用同一数据库"]' :answer="1" explanation="可重建让缓存、索引和分析表在损坏或模型变化后恢复，而不成为第二真相源。" />

## 本章面试题

1. [设计统一事件驱动数据平台](/questions/unified-event-platform)
2. [用 CDC 构建派生视图](/questions/cdc-derived-views)
3. [处理跨系统隐私删除事故](/questions/privacy-deletion-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 12, PDF pp. 511-574.
- 本文为中文学习笔记与原创交互重构，不替代原书。
