---
chapterId: ch07
part: "Part II · 分布式数据"
order: 7
title: "Ch7 · 事务"
titleZh: "事务"
titleEn: "Transactions"
sourcePages: "PDF 243-294"
walkthroughPath: "/chapters/transactions"
questionPaths:
  - /questions/ticket-booking
  - /questions/mvcc-ssi-engine
  - /questions/write-skew-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 7 章交互式中文导读"
---

# Ch7 · 事务

<p class="chapter-subtitle">Transactions</p>

> **阅读范围**：DDIA 第一版 Chapter 7，源 PDF 第 243-294 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-7" label="完成本章" />

## 问题背景

事务把并发和故障的一组复杂结果压缩成可依赖的保证。隔离级别不是开关，而是允许哪些异常；串行化可以通过串行执行、两阶段锁或 SSI 实现，各自付出不同代价。

## 核心模型

- 原子性主要描述失败时的中止能力
- 快照隔离避免脏读但仍可能 write skew
- MVCC 让读写并发并保存多个版本
- SSI 跟踪危险依赖并中止可能形成环的事务

<WalkthroughExplorer :chapter="7" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

单对象条件写 → 多对象原子事务 → 快照隔离 → 显式约束 → 只为关键路径启用串行化并处理重试。

## 生产案例

票务预订同时修改座位、订单和支付意图。唯一约束防止同一座位重复占用，短事务只负责创建 reservation；外部支付用幂等状态机和补偿处理，不能把长网络调用锁在数据库事务中。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

把 ACID 当作所有数据库相同的保证；在快照隔离下先查再写不相关行；让事务跨越用户思考时间；客户端不重试序列化失败。

<KnowledgeCheck question="快照隔离下两个事务可能同时值班的异常叫什么？" :options='["脏读", "write skew", "丢失网络包"]' :answer="1" explanation="两个事务读取同一快照并更新不同记录，分别看都合法，合并后却破坏跨行约束。" />

## 本章面试题

1. [设计票务预订与支付事务](/questions/ticket-booking)
2. [设计 MVCC 与 SSI](/questions/mvcc-ssi-engine)
3. [排查 Write Skew 与重复预订](/questions/write-skew-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 7, PDF pp. 243-294.
- 本文为中文学习笔记与原创交互重构，不替代原书。
