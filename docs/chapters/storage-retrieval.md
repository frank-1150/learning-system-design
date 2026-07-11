---
chapterId: ch03
part: "Part I · 数据系统基础"
order: 3
title: "Ch3 · 存储与检索"
titleZh: "存储与检索"
titleEn: "Storage and Retrieval"
sourcePages: "PDF 91-132"
walkthroughPath: "/chapters/storage-retrieval"
questionPaths:
  - /questions/search-autocomplete
  - /questions/lsm-kv-store
  - /questions/compaction-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 3 章交互式中文导读"
---

# Ch3 · 存储与检索

<p class="chapter-subtitle">Storage and Retrieval</p>

> **阅读范围**：DDIA 第一版 Chapter 3，源 PDF 第 91-132 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-3" label="完成本章" />

## 问题背景

存储引擎是在写放大、读放大、空间放大和延迟稳定性之间做交换。LSM-Tree 优化顺序写，B-Tree 优化原地页更新；分析系统则利用列式布局只读取需要的列。

## 核心模型

- 日志追加把随机写转为顺序写但需要索引
- LSM 通过 memtable、SSTable 与 compaction 组织数据
- B-Tree 用固定页和 WAL 提供稳定点查
- 列式存储通过压缩和向量化服务分析查询

<WalkthroughExplorer :chapter="3" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

追加日志 → 内存哈希索引 → 分段与合并 → 有序 SSTable → 多层 compaction → Bloom Filter 与 block cache。每一步解决前一步暴露的读放大或空间问题。

## 生产案例

搜索自动补全需要按前缀读取有序词项并承受持续更新。内存层接收新热词，后台生成不可变有序段，查询合并多个段；压实策略必须避免在高峰期抢占 I/O。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

只比较理论复杂度；忽略 fsync 和页缓存；把 compaction 当作免费后台任务；为所有字段创建索引导致写放大失控。

<KnowledgeCheck question="LSM-Tree 为什么通常有较高写吞吐？" :options='["永远不需要磁盘", "把写入批量转为顺序 I/O", "不保存旧版本"]' :answer="1" explanation="写先进入内存有序结构和 WAL，再批量刷成 SSTable，避免大量随机页更新。" />

## 本章面试题

1. [设计搜索与自动补全存储层](/questions/search-autocomplete)
2. [设计 LSM-Tree KV Store](/questions/lsm-kv-store)
3. [排查 Compaction 尾延迟事故](/questions/compaction-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 3, PDF pp. 91-132.
- 本文为中文学习笔记与原创交互重构，不替代原书。
