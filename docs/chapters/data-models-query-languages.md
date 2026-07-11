---
chapterId: ch02
part: "Part I · 数据系统基础"
order: 2
title: "Ch2 · 数据模型与查询语言"
titleZh: "数据模型与查询语言"
titleEn: "Data Models and Query Languages"
sourcePages: "PDF 49-90"
walkthroughPath: "/chapters/data-models-query-languages"
questionPaths:
  - /questions/social-graph-feed
  - /questions/product-catalog-model
  - /questions/denormalization-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 2 章交互式中文导读"
---

# Ch2 · 数据模型与查询语言

<p class="chapter-subtitle">Data Models and Query Languages</p>

> **阅读范围**：DDIA 第一版 Chapter 2，源 PDF 第 49-90 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-2" label="完成本章" />

## 问题背景

数据模型决定我们能自然表达哪些关系，也决定查询、演化和组织协作的成本。关系、文档和图不是等级关系，而是针对访问模式与关系形态的不同工具。

## 核心模型

- 文档模型擅长局部性强的一对多聚合
- 关系模型通过规范化和 join 管理多对多关系
- 声明式查询让优化器有重新安排执行计划的空间
- 图模型把边和遍历提升为一等能力

<WalkthroughExplorer :chapter="2" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

从用户旅程列出读写路径 → 识别实体边界和关系基数 → 为高频路径选择主模型 → 用派生索引服务次要查询 → 通过变更日志保持多模型同步。

## 生产案例

商品目录的商品详情适合文档聚合，但库存、订单与商家之间存在强约束和多对多关系。可把交易事实留在关系库，把搜索文档作为可重建派生视图，而不是让两个数据库同时成为真相源。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

从数据库品牌倒推模型；为了避免 join 无限反规范化；忽略关系基数随业务增长变化；让多个存储都接受独立写入而没有冲突规则。

<KnowledgeCheck question="什么时候图模型通常比文档模型更自然？" :options='["对象完全独立", "需要多跳遍历且关系本身有属性", "只按主键读取"]' :answer="1" explanation="图模型把边作为一等对象，适合动态、多跳且方向丰富的关系查询。" />

## 本章面试题

1. [设计社交关系与 Feed 数据层](/questions/social-graph-feed)
2. [为商品目录选择数据模型](/questions/product-catalog-model)
3. [修复反规范化一致性事故](/questions/denormalization-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 2, PDF pp. 49-90.
- 本文为中文学习笔记与原创交互重构，不替代原书。
