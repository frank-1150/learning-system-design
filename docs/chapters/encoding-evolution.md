---
chapterId: ch04
part: "Part I · 数据系统基础"
order: 4
title: "Ch4 · 编码与演化"
titleZh: "编码与演化"
titleEn: "Encoding and Evolution"
sourcePages: "PDF 133-166"
walkthroughPath: "/chapters/encoding-evolution"
questionPaths:
  - /questions/evolvable-api-events
  - /questions/schema-registry
  - /questions/serialization-rollout-incident
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 4 章交互式中文导读"
---

# Ch4 · 编码与演化

<p class="chapter-subtitle">Encoding and Evolution</p>

> **阅读范围**：DDIA 第一版 Chapter 4，源 PDF 第 133-166 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-4" label="完成本章" />

## 问题背景

系统不会在同一时刻完成升级，因此数据格式必须同时考虑向后兼容和向前兼容。模式不是额外负担，而是把字段含义、默认值和演化规则变成可检查契约。

## 核心模型

- 编码格式是跨时间和跨服务的接口
- 向后兼容让新代码读取旧数据
- 向前兼容让旧代码忽略或保留新字段
- 数据库、RPC 与消息队列具有不同的数据流寿命

<WalkthroughExplorer :chapter="4" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

显式版本字段 → 兼容性规则 → Schema Registry → CI 检查 → 双写/双读迁移 → 废弃观测。发布完成不等于旧格式已经消失。

## 生产案例

订单事件新增货币字段时，新消费者必须为旧事件提供默认语义，旧消费者应忽略未知字段。生产者不能在所有消费者升级前改变既有字段含义。

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

重用已删除的字段编号；把缺失字段与零值混为一谈；只测最新生产者与最新消费者；在消息中发送语言对象序列化结果。

<KnowledgeCheck question="旧代码能读取新代码写出的数据属于哪类兼容？" :options='["向前兼容", "向后兼容", "线性一致"]' :answer="0" explanation="旧读取者面对未来格式，因此这是 forward compatibility。" />

## 本章面试题

1. [设计可演进的公共 API 与事件格式](/questions/evolvable-api-events)
2. [设计 Schema Registry](/questions/schema-registry)
3. [处理滚动发布反序列化故障](/questions/serialization-rollout-incident)

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter 4, PDF pp. 133-166.
- 本文为中文学习笔记与原创交互重构，不替代原书。
