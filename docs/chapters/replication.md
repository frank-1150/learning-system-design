---
chapterId: ch05
part: "Part II · 分布式数据"
order: 5
title: "Ch5 · 复制"
titleZh: "复制"
titleEn: "Replication"
sourcePages: "PDF 167-220"
walkthroughPath: "/chapters/replication"
questionPaths:
  - /questions/multi-region-profile
  - /questions/leaderless-quorum-kv
  - /questions/replication-lag-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 5 章交互式中文导读"
---

# Ch5 · 复制

<p class="chapter-subtitle">Replication</p>

> **阅读范围**：DDIA 第一版 Chapter 5，源 PDF 第 167-220 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-5" label="完成本章" />

## 问题背景

复制用冗余换取可用性、读扩展和地理接近性，同时引入复制延迟、冲突与故障切换。单主、多主和无主方案的核心区别是写入排序由谁决定。

## 核心模型

- 同步复制保护数据但把远端延迟放进写路径
- 异步复制降低延迟但故障时可能丢写
- 读己之写、单调读和一致前缀是常见会话保证
- 无主复制依赖版本、quorum 和冲突合并

<WalkthroughExplorer :chapter="5" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

单节点 → 同地域异步副本 → 自动故障切换 → 读流量分离 → 多地域读取 → 按业务冲突语义选择多主或无主。

## 生产案例

多地域用户资料服务可以让用户写入归属地域的 Leader，并把会话读路由到足够新的副本。跨地域协作字段需显式冲突规则，不能简单用最后写入获胜覆盖并发更新。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

把 quorum 公式当作线性一致保证；故障切换后忽略旧 Leader 复活；用物理时钟做绝对冲突排序；让用户刷新后看到更旧数据。

<KnowledgeCheck question="异步副本最直接的风险是什么？" :options='["无法扩展读取", "Leader 故障时已确认写入可能尚未复制", "所有写都需要全体节点确认"]' :answer="1" explanation="Leader 可以在副本确认前返回，因此突然故障可能丢失尚未复制的写。" />

## 本章面试题

1. [设计多地域用户数据服务](/questions/multi-region-profile)
2. [设计 Leaderless Quorum KV Store](/questions/leaderless-quorum-kv)
3. [处理复制延迟与冲突事故](/questions/replication-lag-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 5, PDF pp. 167-220.
- 本文为中文学习笔记与原创交互重构，不替代原书。
