---
chapterId: ch06
part: "Part II · 分布式数据"
order: 6
title: "Ch6 · 分区"
titleZh: "分区"
titleEn: "Partitioning"
sourcePages: "PDF 221-242"
walkthroughPath: "/chapters/partitioning"
questionPaths:
  - /questions/sharded-chat-history
  - /questions/consistent-hash-rebalance
  - /questions/hot-shard-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 6 章交互式中文导读"
---

# Ch6 · 分区

<p class="chapter-subtitle">Partitioning</p>

> **阅读范围**：DDIA 第一版 Chapter 6，源 PDF 第 221-242 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-6" label="完成本章" />

## 问题背景

分区把超出单机容量的数据和吞吐拆到多个节点。真正困难的不是 hash，而是选择不会制造热点的分区键、维护二级索引，并在扩缩容时安全迁移所有权。

## 核心模型

- 范围分区支持区间扫描但易产生顺序热点
- 哈希分区分布均匀但牺牲相邻性
- 二级索引可按文档本地化或按词项全局化
- 再均衡必须控制数据移动和前台延迟

<WalkthroughExplorer :chapter="6" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

固定分片 → 虚拟分区 → 所有权映射 → 后台复制 → 双读校验 → 原子切换路由 → 清理旧副本。

## 生产案例

聊天记录可按 conversation_id 哈希分区，并在分区内按消息时间排序。超大群聊会成为热点，需要把时间桶或子分区纳入键，同时保持按会话读取的可预测性。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

直接按用户所在地域分区；使用低基数字段；扩容时一次搬迁全部数据；让客户端长期缓存过期路由。

<KnowledgeCheck question="为什么 hash(key) % N 不适合频繁扩缩容？" :options='["无法并行查询", "N 改变会重新映射几乎所有 key", "不能使用副本"]' :answer="1" explanation="模数变化导致绝大多数 key 落到不同节点，引发大规模数据移动和缓存失效。" />

## 本章面试题

1. [设计海量聊天记录分片](/questions/sharded-chat-history)
2. [设计一致性哈希与在线再均衡](/questions/consistent-hash-rebalance)
3. [处理热点分片与扩容雪崩](/questions/hot-shard-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 6, PDF pp. 221-242.
- 本文为中文学习笔记与原创交互重构，不替代原书。
