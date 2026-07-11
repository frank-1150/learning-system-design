---
title: 系统设计面试题
description: 36 道产品、机制与事故系统设计题
---

# 36 道系统设计面试题

每章包含一题产品系统、一题底层机制和一题生产事故。答案默认折叠，建议先独立作答。

## Ch1 · 可靠、可扩展与可维护

- [设计短链服务](/questions/url-shortener)
- [设计可扩展限流平台](/questions/rate-limiter)
- [排查流量突增下的 P99 延迟](/questions/p99-latency-incident)
## Ch2 · 数据模型与查询语言

- [设计社交关系与 Feed 数据层](/questions/social-graph-feed)
- [为商品目录选择数据模型](/questions/product-catalog-model)
- [修复反规范化一致性事故](/questions/denormalization-incident)
## Ch3 · 存储与检索

- [设计搜索与自动补全存储层](/questions/search-autocomplete)
- [设计 LSM-Tree KV Store](/questions/lsm-kv-store)
- [排查 Compaction 尾延迟事故](/questions/compaction-incident)
## Ch4 · 编码与演化

- [设计可演进的公共 API 与事件格式](/questions/evolvable-api-events)
- [设计 Schema Registry](/questions/schema-registry)
- [处理滚动发布反序列化故障](/questions/serialization-rollout-incident)
## Ch5 · 复制

- [设计多地域用户数据服务](/questions/multi-region-profile)
- [设计 Leaderless Quorum KV Store](/questions/leaderless-quorum-kv)
- [处理复制延迟与冲突事故](/questions/replication-lag-incident)
## Ch6 · 分区

- [设计海量聊天记录分片](/questions/sharded-chat-history)
- [设计一致性哈希与在线再均衡](/questions/consistent-hash-rebalance)
- [处理热点分片与扩容雪崩](/questions/hot-shard-incident)
## Ch7 · 事务

- [设计票务预订与支付事务](/questions/ticket-booking)
- [设计 MVCC 与 SSI](/questions/mvcc-ssi-engine)
- [排查 Write Skew 与重复预订](/questions/write-skew-incident)
## Ch8 · 分布式系统的麻烦

- [设计带 Lease 的分布式任务调度器](/questions/lease-job-scheduler)
- [设计故障检测与 Fencing](/questions/failure-detector-fencing)
- [处理时钟漂移与 Split-Brain](/questions/clock-split-brain-incident)
## Ch9 · 一致性与共识

- [设计高可用配置与元数据服务](/questions/metadata-service)
- [设计共识日志与 Leader Election](/questions/consensus-log)
- [处理 2PC 协调者故障](/questions/two-phase-commit-incident)
## Ch10 · 批处理

- [设计批量网页抓取与索引流水线](/questions/batch-crawl-index)
- [设计分布式 Join 与 MapReduce](/questions/distributed-join)
- [处理 Straggler 与重复输出](/questions/batch-straggler-incident)
## Ch11 · 流处理

- [设计实时风控与指标平台](/questions/realtime-risk-metrics)
- [设计 Exactly-Once 窗口处理器](/questions/exactly-once-stream)
- [处理迟到数据、回放与背压](/questions/stream-backpressure-incident)
## Ch12 · 数据系统的未来

- [设计统一事件驱动数据平台](/questions/unified-event-platform)
- [用 CDC 构建派生视图](/questions/cdc-derived-views)
- [处理跨系统隐私删除事故](/questions/privacy-deletion-incident)
