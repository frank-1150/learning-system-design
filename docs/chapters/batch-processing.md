---
chapterId: ch10
part: "Part III · 派生数据"
order: 10
title: "Ch10 · 批处理"
titleZh: "批处理"
titleEn: "Batch Processing"
sourcePages: "PDF 407-460"
walkthroughPath: "/chapters/batch-processing"
questionPaths:
  - /questions/batch-crawl-index
  - /questions/distributed-join
  - /questions/batch-straggler-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 10 章交互式中文导读"
---

# Ch10 · 批处理

<p class="chapter-subtitle">Batch Processing</p>

> **阅读范围**：DDIA 第一版 Chapter 10，源 PDF 第 407-460 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-10" label="完成本章" />

## 问题背景

批处理把有界输入转为可重建输出。不可变输入、确定性任务和显式数据流让失败可以通过重跑恢复；MapReduce 的价值不仅是 API，而是把 shuffle、容错和数据局部性标准化。

## 核心模型

- Unix 管道通过统一字节流接口组合小工具
- MapReduce 用 map、shuffle、reduce 重新分组数据
- 分布式 join 可在 reduce 侧或 map 侧完成
- 批处理输出应作为可替换派生数据而非逐条副作用

<WalkthroughExplorer :chapter="10" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

单机脚本 → 分片输入 → 幂等 map → 按 key shuffle → reduce 聚合 → DAG 调度 → 增量化与共享中间结果。

## 生产案例

网页抓取与索引将 URL 清单作为不可变输入，抓取结果写对象存储，解析、去重、倒排索引各自形成 DAG 节点。失败任务重跑到临时输出，只有完整分区成功后才原子发布。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

任务直接更新在线数据库；重试产生重复外部副作用；把所有 join 都做成全量 shuffle；中间文件无版本导致上下游混用。

<KnowledgeCheck question="为什么批处理输出适合写入新目录后原子切换？" :options='["避免任何磁盘写入", "失败不会暴露半成品且可安全重试", "让任务无法并行"]' :answer="1" explanation="临时输出保持不可见，全部完成后发布指针，失败时可删除并重跑。" />

## 本章面试题

1. [设计批量网页抓取与索引流水线](/questions/batch-crawl-index)
2. [设计分布式 Join 与 MapReduce](/questions/distributed-join)
3. [处理 Straggler 与重复输出](/questions/batch-straggler-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 10, PDF pp. 407-460.
- 本文为中文学习笔记与原创交互重构，不替代原书。
