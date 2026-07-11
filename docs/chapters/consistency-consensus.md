---
chapterId: ch09
part: "Part II · 分布式数据"
order: 9
title: "Ch9 · 一致性与共识"
titleZh: "一致性与共识"
titleEn: "Consistency and Consensus"
sourcePages: "PDF 343-406"
walkthroughPath: "/chapters/consistency-consensus"
questionPaths:
  - /questions/metadata-service
  - /questions/consensus-log
  - /questions/two-phase-commit-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 9 章交互式中文导读"
---

# Ch9 · 一致性与共识

<p class="chapter-subtitle">Consistency and Consensus</p>

> **阅读范围**：DDIA 第一版 Chapter 9，源 PDF 第 343-406 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-9" label="完成本章" />

## 问题背景

线性一致提供单副本错觉，因果一致只约束有因果关系的事件。共识让节点对同一顺序或决定达成一致，是 Leader Election、原子广播和高可用协调服务的基础。

## 核心模型

- 线性一致要求操作像在调用与返回之间某点原子生效
- 因果顺序比全序更弱也更可扩展
- 全序广播等价于持续达成一系列共识
- 2PC 解决原子提交但协调器故障可能阻塞

<WalkthroughExplorer :chapter="9" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

单节点元数据 → 主从复制 → quorum 共识 → 复制日志 → 快照和成员变更 → 把强一致范围限制在小型控制平面。

## 生产案例

配置服务通过共识日志复制少量关键元数据，watch 客户端按 revision 接收变化。大对象存储在外部系统，控制平面只保存引用，以避免把高吞吐数据路径塞进共识组。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

把 eventual consistency 当作唯一弱模型；在网络分区时仍承诺线性读写可用；用 2PC 代替容错共识；让单个共识组承载无限 key。

<KnowledgeCheck question="线性一致系统在网络分区时通常必须牺牲什么？" :options='["全部持久性", "至少一侧的可用性", "所有读取"]' :answer="1" explanation="无法通信的两侧不能同时接受可能冲突的线性写入，至少一侧需要拒绝或等待。" />

## 本章面试题

1. [设计高可用配置与元数据服务](/questions/metadata-service)
2. [设计共识日志与 Leader Election](/questions/consensus-log)
3. [处理 2PC 协调者故障](/questions/two-phase-commit-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 9, PDF pp. 343-406.
- 本文为中文学习笔记与原创交互重构，不替代原书。
