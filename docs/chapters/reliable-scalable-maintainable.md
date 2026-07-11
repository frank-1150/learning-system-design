---
chapterId: ch01
part: "Part I · 数据系统基础"
order: 1
title: "Ch1 · 可靠、可扩展与可维护"
titleZh: "可靠、可扩展与可维护"
titleEn: "Reliable, Scalable, and Maintainable Applications"
sourcePages: "PDF 25-48"
walkthroughPath: "/chapters/reliable-scalable-maintainable"
questionPaths:
  - /questions/url-shortener
  - /questions/rate-limiter
  - /questions/p99-latency-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 1 章交互式中文导读"
---

# Ch1 · 可靠、可扩展与可维护

<p class="chapter-subtitle">Reliable, Scalable, and Maintainable Applications</p>

> **阅读范围**：DDIA 第一版 Chapter 1，源 PDF 第 25-48 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-1" label="完成本章" />

## 问题背景

先把可靠性、可扩展性和可维护性变成可测量的目标，再谈技术选型。负载参数描述系统承受什么，延迟百分位描述用户实际看到什么，运维性与可演化性决定系统能否长期生存。

## 核心模型

- 可靠性不是永不出错，而是在故障存在时继续正确工作
- 可扩展性必须绑定具体负载参数与性能指标
- P99 比平均延迟更能暴露排队与慢依赖
- 可维护性由可运维、简单性和可演化性共同构成

<WalkthroughExplorer :chapter="1" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

单实例先验证产品假设 → 增加可观测性形成基线 → 无状态水平扩展 → 拆分状态与计算 → 用故障演练验证降级路径。每一步都由指标触发，而不是为了架构图更复杂。

## 生产案例

以短链跳转为例，读请求远多于写请求。缓存和只读副本提升吞吐，但真正的设计起点是跳转延迟 SLO、热点 key 比例、链接不可丢失的可靠性目标，以及值班人员能否快速定位某个地域的错误率。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

只报平均延迟；把加机器当作唯一扩展策略；为理论高可用引入无法运维的组件；没有定义降级时哪些功能必须保留。

<KnowledgeCheck question="为什么平均延迟不足以描述用户体验？" :options='["它无法计算吞吐量", "它会掩盖长尾和排队", "它不支持水平扩展"]' :answer="1" explanation="少量极慢请求会被平均值稀释，而一次用户操作通常依赖多个请求，长尾会被放大。" />

## 本章面试题

1. [设计短链服务](/questions/url-shortener)
2. [设计可扩展限流平台](/questions/rate-limiter)
3. [排查流量突增下的 P99 延迟](/questions/p99-latency-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 1, PDF pp. 25-48.
- 本文为中文学习笔记与原创交互重构，不替代原书。
