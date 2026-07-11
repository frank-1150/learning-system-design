---
chapterId: ch08
part: "Part II · 分布式数据"
order: 8
title: "Ch8 · 分布式系统的麻烦"
titleZh: "分布式系统的麻烦"
titleEn: "The Trouble with Distributed Systems"
sourcePages: "PDF 295-342"
walkthroughPath: "/chapters/distributed-systems-trouble"
questionPaths:
  - /questions/lease-job-scheduler
  - /questions/failure-detector-fencing
  - /questions/clock-split-brain-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 8 章交互式中文导读"
---

# Ch8 · 分布式系统的麻烦

<p class="chapter-subtitle">The Trouble with Distributed Systems</p>

> **阅读范围**：DDIA 第一版 Chapter 8，源 PDF 第 295-342 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-8" label="完成本章" />

## 问题背景

分布式系统的核心现实是部分失败：超时不能告诉你请求是否执行，时钟不能提供绝对真相，进程可能在任意位置暂停。正确性需要建立在明确系统模型、quorum 与 fencing 上。

## 核心模型

- 网络延迟没有可靠上界，超时只能表达怀疑
- 单调时钟适合测时长，墙上时钟适合显示时间
- 进程暂停会让旧持有者误以为 lease 仍有效
- 多数派与 fencing token 能把过期参与者隔离

<WalkthroughExplorer :chapter="8" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

乐观远程调用 → 超时和重试 → 幂等键 → lease → 单调 fencing token → 下游强制拒绝旧 token → 故障注入验证。

## 生产案例

任务调度器给 worker 发放带 token 的 lease。即使 worker 因 GC 暂停到 lease 过期，恢复后携带的旧 token 也会被存储层拒绝，从而避免两个 worker 同时提交同一任务结果。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

把 timeout 当作对端死亡证明；依赖 NTP 时间判断锁归属；只在协调器检查 lease；假设 stop-the-world pause 有最大时长。

<KnowledgeCheck question="为什么 lease 还需要 fencing token？" :options='["让时钟更精确", "阻止暂停后恢复的旧持有者继续写", "减少副本数量"]' :answer="1" explanation="旧进程不知道自己暂停过；只有下游比较单调 token 才能拒绝过期写入。" />

## 本章面试题

1. [设计带 Lease 的分布式任务调度器](/questions/lease-job-scheduler)
2. [设计故障检测与 Fencing](/questions/failure-detector-fencing)
3. [处理时钟漂移与 Split-Brain](/questions/clock-split-brain-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 8, PDF pp. 295-342.
- 本文为中文学习笔记与原创交互重构，不替代原书。
