#!/usr/bin/env python3
"""Generate the DDIA walkthroughs, interview questions, and site content manifest."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def bullets(value: str) -> str:
    return "\n".join(f"- {item.strip()}" for item in value.split("|") if item.strip())


CHAPTERS = [
    {
        "chapter": 1, "part": "Part I · 数据系统基础", "slug": "reliable-scalable-maintainable",
        "titleZh": "可靠、可扩展与可维护", "titleEn": "Reliable, Scalable, and Maintainable Applications", "pages": "25-48",
        "thesis": "先把可靠性、可扩展性和可维护性变成可测量的目标，再谈技术选型。负载参数描述系统承受什么，延迟百分位描述用户实际看到什么，运维性与可演化性决定系统能否长期生存。",
        "concepts": "可靠性不是永不出错，而是在故障存在时继续正确工作|可扩展性必须绑定具体负载参数与性能指标|P99 比平均延迟更能暴露排队与慢依赖|可维护性由可运维、简单性和可演化性共同构成",
        "evolution": "单实例先验证产品假设 → 增加可观测性形成基线 → 无状态水平扩展 → 拆分状态与计算 → 用故障演练验证降级路径。每一步都由指标触发，而不是为了架构图更复杂。",
        "case": "以短链跳转为例，读请求远多于写请求。缓存和只读副本提升吞吐，但真正的设计起点是跳转延迟 SLO、热点 key 比例、链接不可丢失的可靠性目标，以及值班人员能否快速定位某个地域的错误率。",
        "pitfalls": "只报平均延迟；把加机器当作唯一扩展策略；为理论高可用引入无法运维的组件；没有定义降级时哪些功能必须保留。",
        "check": ["为什么平均延迟不足以描述用户体验？", ["它无法计算吞吐量", "它会掩盖长尾和排队", "它不支持水平扩展"], 1, "少量极慢请求会被平均值稀释，而一次用户操作通常依赖多个请求，长尾会被放大。"],
        "walk": [
            ("请求", "负载参数", "容量模型", "描述负载", "用 QPS、读写比、对象大小与热点比例描述压力，而不是只说用户很多。", "参数选错会让压测结果与生产现实脱节。"),
            ("容量模型", "P50/P95/P99", "SLO", "描述性能", "同时观察吞吐和延迟分布，并明确过载时允许牺牲什么。", "更严格的尾延迟目标意味着更高冗余和成本。"),
            ("SLO", "隔离与冗余", "降级路径", "吸收故障", "用超时、隔离、重试预算和冗余把局部故障限制在边界内。", "重试若无预算会把局部故障放大为全局雪崩。"),
            ("降级路径", "可观测性", "持续演进", "让系统可维护", "把运行手册、指标、变更审计与简单接口当作架构的一部分。", "复杂度预算和机器预算一样有限。"),
        ],
    },
    {
        "chapter": 2, "part": "Part I · 数据系统基础", "slug": "data-models-query-languages",
        "titleZh": "数据模型与查询语言", "titleEn": "Data Models and Query Languages", "pages": "49-90",
        "thesis": "数据模型决定我们能自然表达哪些关系，也决定查询、演化和组织协作的成本。关系、文档和图不是等级关系，而是针对访问模式与关系形态的不同工具。",
        "concepts": "文档模型擅长局部性强的一对多聚合|关系模型通过规范化和 join 管理多对多关系|声明式查询让优化器有重新安排执行计划的空间|图模型把边和遍历提升为一等能力",
        "evolution": "从用户旅程列出读写路径 → 识别实体边界和关系基数 → 为高频路径选择主模型 → 用派生索引服务次要查询 → 通过变更日志保持多模型同步。",
        "case": "商品目录的商品详情适合文档聚合，但库存、订单与商家之间存在强约束和多对多关系。可把交易事实留在关系库，把搜索文档作为可重建派生视图，而不是让两个数据库同时成为真相源。",
        "pitfalls": "从数据库品牌倒推模型；为了避免 join 无限反规范化；忽略关系基数随业务增长变化；让多个存储都接受独立写入而没有冲突规则。",
        "check": ["什么时候图模型通常比文档模型更自然？", ["对象完全独立", "需要多跳遍历且关系本身有属性", "只按主键读取"], 1, "图模型把边作为一等对象，适合动态、多跳且方向丰富的关系查询。"],
        "walk": [
            ("业务问题", "访问路径", "关系基数", "先画访问路径", "列出最常见的写入、点查、范围查询与多跳遍历。", "只看实体名会遗漏真正决定性能的访问模式。"),
            ("关系基数", "主数据模型", "事务边界", "选择主模型", "局部聚合偏文档，复杂关系与约束偏关系，多跳发现偏图。", "跨模型事务会增加协调与恢复成本。"),
            ("主数据模型", "派生索引", "查询体验", "补足次要查询", "通过搜索索引、缓存或图投影服务不同查询，但保留单一真相源。", "派生视图必须能重建并暴露新鲜度。"),
            ("模型变更", "兼容迁移", "长期演化", "为未来留迁移路径", "双读验证、后台回填和版本字段比一次停机迁移更稳健。", "长期双写会制造难以证明的一致性。"),
        ],
    },
    {
        "chapter": 3, "part": "Part I · 数据系统基础", "slug": "storage-retrieval",
        "titleZh": "存储与检索", "titleEn": "Storage and Retrieval", "pages": "91-132",
        "thesis": "存储引擎是在写放大、读放大、空间放大和延迟稳定性之间做交换。LSM-Tree 优化顺序写，B-Tree 优化原地页更新；分析系统则利用列式布局只读取需要的列。",
        "concepts": "日志追加把随机写转为顺序写但需要索引|LSM 通过 memtable、SSTable 与 compaction 组织数据|B-Tree 用固定页和 WAL 提供稳定点查|列式存储通过压缩和向量化服务分析查询",
        "evolution": "追加日志 → 内存哈希索引 → 分段与合并 → 有序 SSTable → 多层 compaction → Bloom Filter 与 block cache。每一步解决前一步暴露的读放大或空间问题。",
        "case": "搜索自动补全需要按前缀读取有序词项并承受持续更新。内存层接收新热词，后台生成不可变有序段，查询合并多个段；压实策略必须避免在高峰期抢占 I/O。",
        "pitfalls": "只比较理论复杂度；忽略 fsync 和页缓存；把 compaction 当作免费后台任务；为所有字段创建索引导致写放大失控。",
        "check": ["LSM-Tree 为什么通常有较高写吞吐？", ["永远不需要磁盘", "把写入批量转为顺序 I/O", "不保存旧版本"], 1, "写先进入内存有序结构和 WAL，再批量刷成 SSTable，避免大量随机页更新。"],
        "walk": [
            ("写请求", "WAL + Memtable", "已确认写入", "接收写入", "先顺序追加 WAL，再更新内存有序结构，确认持久性后返回。", "每次强制刷盘更安全但会限制吞吐。"),
            ("Memtable", "SSTable", "不可变文件", "冻结与刷盘", "达到阈值后冻结内存表并顺序写出有索引的 SSTable。", "文件过多会增加每次读取需要探测的层数。"),
            ("多个 SSTable", "Compaction", "更少层级", "后台压实", "合并有序文件、清除过期版本并维持层级大小约束。", "压实会产生写放大并与前台请求争夺 I/O。"),
            ("读请求", "Bloom + Cache", "最新值", "缩小读放大", "先查内存和缓存，再用 Bloom Filter 跳过不含 key 的文件。", "缓存命中率依赖真实工作集而非总数据量。"),
        ],
    },
    {
        "chapter": 4, "part": "Part I · 数据系统基础", "slug": "encoding-evolution",
        "titleZh": "编码与演化", "titleEn": "Encoding and Evolution", "pages": "133-166",
        "thesis": "系统不会在同一时刻完成升级，因此数据格式必须同时考虑向后兼容和向前兼容。模式不是额外负担，而是把字段含义、默认值和演化规则变成可检查契约。",
        "concepts": "编码格式是跨时间和跨服务的接口|向后兼容让新代码读取旧数据|向前兼容让旧代码忽略或保留新字段|数据库、RPC 与消息队列具有不同的数据流寿命",
        "evolution": "显式版本字段 → 兼容性规则 → Schema Registry → CI 检查 → 双写/双读迁移 → 废弃观测。发布完成不等于旧格式已经消失。",
        "case": "订单事件新增货币字段时，新消费者必须为旧事件提供默认语义，旧消费者应忽略未知字段。生产者不能在所有消费者升级前改变既有字段含义。",
        "pitfalls": "重用已删除的字段编号；把缺失字段与零值混为一谈；只测最新生产者与最新消费者；在消息中发送语言对象序列化结果。",
        "check": ["旧代码能读取新代码写出的数据属于哪类兼容？", ["向前兼容", "向后兼容", "线性一致"], 0, "旧读取者面对未来格式，因此这是 forward compatibility。"],
        "walk": [
            ("领域对象", "Schema", "编码字节", "定义稳定契约", "明确字段编号、类型、可选性与默认语义，而非只定义当前类结构。", "过度严格会阻碍演化，过度宽松会隐藏数据错误。"),
            ("新生产者", "兼容检查", "旧消费者", "验证双向兼容", "在 CI 中用历史 schema 检查新增、删除和类型变化。", "语法兼容不保证业务语义兼容。"),
            ("旧数据", "双读/回填", "新模型", "迁移存量", "读取时升级或后台回填，并记录仍在使用旧格式的比例。", "大规模回填会挤占在线存储吞吐。"),
            ("全链路", "废弃观测", "删除旧路径", "安全收尾", "确认旧生产者、旧数据和旧消费者都清零后再移除兼容代码。", "过早清理会让延迟到达的消息变成毒消息。"),
        ],
    },
    {
        "chapter": 5, "part": "Part II · 分布式数据", "slug": "replication",
        "titleZh": "复制", "titleEn": "Replication", "pages": "167-220",
        "thesis": "复制用冗余换取可用性、读扩展和地理接近性，同时引入复制延迟、冲突与故障切换。单主、多主和无主方案的核心区别是写入排序由谁决定。",
        "concepts": "同步复制保护数据但把远端延迟放进写路径|异步复制降低延迟但故障时可能丢写|读己之写、单调读和一致前缀是常见会话保证|无主复制依赖版本、quorum 和冲突合并",
        "evolution": "单节点 → 同地域异步副本 → 自动故障切换 → 读流量分离 → 多地域读取 → 按业务冲突语义选择多主或无主。",
        "case": "多地域用户资料服务可以让用户写入归属地域的 Leader，并把会话读路由到足够新的副本。跨地域协作字段需显式冲突规则，不能简单用最后写入获胜覆盖并发更新。",
        "pitfalls": "把 quorum 公式当作线性一致保证；故障切换后忽略旧 Leader 复活；用物理时钟做绝对冲突排序；让用户刷新后看到更旧数据。",
        "check": ["异步副本最直接的风险是什么？", ["无法扩展读取", "Leader 故障时已确认写入可能尚未复制", "所有写都需要全体节点确认"], 1, "Leader 可以在副本确认前返回，因此突然故障可能丢失尚未复制的写。"],
        "walk": [
            ("客户端写", "Leader 日志", "本地确认", "建立写入顺序", "Leader 串行化写入并记录复制位置。", "单 Leader 简化冲突，但限制写入可用地域。"),
            ("Leader 日志", "Follower", "复制进度", "传播变更", "Follower 按日志顺序应用变更并报告 offset。", "异步链路会产生可见复制延迟。"),
            ("客户端读", "会话水位", "合格副本", "提供会话保证", "携带最近写入位置，只路由到已追上的副本或回到 Leader。", "更强保证会降低可用副本选择空间。"),
            ("节点故障", "选主与 fencing", "新拓扑", "安全切换", "选取日志足够新的节点，并阻止旧 Leader 继续接受写入。", "错误故障检测可能同时产生两个 Leader。"),
        ],
    },
    {
        "chapter": 6, "part": "Part II · 分布式数据", "slug": "partitioning",
        "titleZh": "分区", "titleEn": "Partitioning", "pages": "221-242",
        "thesis": "分区把超出单机容量的数据和吞吐拆到多个节点。真正困难的不是 hash，而是选择不会制造热点的分区键、维护二级索引，并在扩缩容时安全迁移所有权。",
        "concepts": "范围分区支持区间扫描但易产生顺序热点|哈希分区分布均匀但牺牲相邻性|二级索引可按文档本地化或按词项全局化|再均衡必须控制数据移动和前台延迟",
        "evolution": "固定分片 → 虚拟分区 → 所有权映射 → 后台复制 → 双读校验 → 原子切换路由 → 清理旧副本。",
        "case": "聊天记录可按 conversation_id 哈希分区，并在分区内按消息时间排序。超大群聊会成为热点，需要把时间桶或子分区纳入键，同时保持按会话读取的可预测性。",
        "pitfalls": "直接按用户所在地域分区；使用低基数字段；扩容时一次搬迁全部数据；让客户端长期缓存过期路由。",
        "check": ["为什么 hash(key) % N 不适合频繁扩缩容？", ["无法并行查询", "N 改变会重新映射几乎所有 key", "不能使用副本"], 1, "模数变化导致绝大多数 key 落到不同节点，引发大规模数据移动和缓存失效。"],
        "walk": [
            ("逻辑 key", "分区函数", "逻辑分区", "计算归属", "在稳定的逻辑分区空间中映射 key，避免直接绑定机器数量。", "哈希均匀性会牺牲范围查询局部性。"),
            ("逻辑分区", "所有权表", "存储节点", "解析物理位置", "协调服务维护版本化所有权，路由层缓存并能刷新。", "集中路由信息必须高可用且防止旧版本写入。"),
            ("旧节点", "后台复制", "新节点", "在线迁移", "限速复制快照，再追增量日志，期间旧节点继续服务。", "迁移流量会与线上请求争夺网络和磁盘。"),
            ("路由层", "原子切换", "新所有者", "完成再均衡", "切换 epoch 后用 fencing 拒绝旧所有者写入，最后清理数据。", "没有 epoch 的双写窗口可能产生分叉。"),
        ],
    },
    {
        "chapter": 7, "part": "Part II · 分布式数据", "slug": "transactions",
        "titleZh": "事务", "titleEn": "Transactions", "pages": "243-294",
        "thesis": "事务把并发和故障的一组复杂结果压缩成可依赖的保证。隔离级别不是开关，而是允许哪些异常；串行化可以通过串行执行、两阶段锁或 SSI 实现，各自付出不同代价。",
        "concepts": "原子性主要描述失败时的中止能力|快照隔离避免脏读但仍可能 write skew|MVCC 让读写并发并保存多个版本|SSI 跟踪危险依赖并中止可能形成环的事务",
        "evolution": "单对象条件写 → 多对象原子事务 → 快照隔离 → 显式约束 → 只为关键路径启用串行化并处理重试。",
        "case": "票务预订同时修改座位、订单和支付意图。唯一约束防止同一座位重复占用，短事务只负责创建 reservation；外部支付用幂等状态机和补偿处理，不能把长网络调用锁在数据库事务中。",
        "pitfalls": "把 ACID 当作所有数据库相同的保证；在快照隔离下先查再写不相关行；让事务跨越用户思考时间；客户端不重试序列化失败。",
        "check": ["快照隔离下两个事务可能同时值班的异常叫什么？", ["脏读", "write skew", "丢失网络包"], 1, "两个事务读取同一快照并更新不同记录，分别看都合法，合并后却破坏跨行约束。"],
        "walk": [
            ("事务开始", "一致快照", "读取版本", "建立可见性", "事务读取开始时已提交版本，避免看到中途变化。", "长快照会阻止旧版本清理并放大存储。"),
            ("并发写", "版本/锁", "冲突集合", "检测直接冲突", "同一对象写入用锁、CAS 或版本检查避免丢失更新。", "只检测写写冲突无法发现 write skew。"),
            ("读写依赖", "SSI", "危险结构", "发现序列化风险", "跟踪 rw 反依赖，在可能形成环时中止一个事务。", "误中止提高安全性但要求应用可靠重试。"),
            ("提交请求", "WAL + 原子提交", "可见结果", "持久化或回滚", "所有变更获得同一提交结果，崩溃恢复从日志重放。", "跨服务原子提交会降低可用性并扩大锁范围。"),
        ],
    },
    {
        "chapter": 8, "part": "Part II · 分布式数据", "slug": "distributed-systems-trouble",
        "titleZh": "分布式系统的麻烦", "titleEn": "The Trouble with Distributed Systems", "pages": "295-342",
        "thesis": "分布式系统的核心现实是部分失败：超时不能告诉你请求是否执行，时钟不能提供绝对真相，进程可能在任意位置暂停。正确性需要建立在明确系统模型、quorum 与 fencing 上。",
        "concepts": "网络延迟没有可靠上界，超时只能表达怀疑|单调时钟适合测时长，墙上时钟适合显示时间|进程暂停会让旧持有者误以为 lease 仍有效|多数派与 fencing token 能把过期参与者隔离",
        "evolution": "乐观远程调用 → 超时和重试 → 幂等键 → lease → 单调 fencing token → 下游强制拒绝旧 token → 故障注入验证。",
        "case": "任务调度器给 worker 发放带 token 的 lease。即使 worker 因 GC 暂停到 lease 过期，恢复后携带的旧 token 也会被存储层拒绝，从而避免两个 worker 同时提交同一任务结果。",
        "pitfalls": "把 timeout 当作对端死亡证明；依赖 NTP 时间判断锁归属；只在协调器检查 lease；假设 stop-the-world pause 有最大时长。",
        "check": ["为什么 lease 还需要 fencing token？", ["让时钟更精确", "阻止暂停后恢复的旧持有者继续写", "减少副本数量"], 1, "旧进程不知道自己暂停过；只有下游比较单调 token 才能拒绝过期写入。"],
        "walk": [
            ("Worker", "申请 lease", "协调器", "获得临时所有权", "协调器返回过期时间和单调递增 token。", "lease 依赖时间，必须给时钟误差和网络延迟留余量。"),
            ("协调器", "Token 42", "存储层", "传播 fencing", "所有有副作用的写都携带 token，存储记录已见最大值。", "若下游不校验，token 只是装饰。"),
            ("Worker", "长时间暂停", "Lease 过期", "制造部分失败", "另一个 worker 获得 Token 43 并继续任务。", "超时无法判断旧 worker 当前是否仍在执行。"),
            ("旧 Worker", "Token 42 被拒", "正确状态", "隔离过期参与者", "恢复后的旧写因 token 小于 43 被拒绝并放弃。", "所有写路径都必须执行相同检查。"),
        ],
    },
    {
        "chapter": 9, "part": "Part II · 分布式数据", "slug": "consistency-consensus",
        "titleZh": "一致性与共识", "titleEn": "Consistency and Consensus", "pages": "343-406",
        "thesis": "线性一致提供单副本错觉，因果一致只约束有因果关系的事件。共识让节点对同一顺序或决定达成一致，是 Leader Election、原子广播和高可用协调服务的基础。",
        "concepts": "线性一致要求操作像在调用与返回之间某点原子生效|因果顺序比全序更弱也更可扩展|全序广播等价于持续达成一系列共识|2PC 解决原子提交但协调器故障可能阻塞",
        "evolution": "单节点元数据 → 主从复制 → quorum 共识 → 复制日志 → 快照和成员变更 → 把强一致范围限制在小型控制平面。",
        "case": "配置服务通过共识日志复制少量关键元数据，watch 客户端按 revision 接收变化。大对象存储在外部系统，控制平面只保存引用，以避免把高吞吐数据路径塞进共识组。",
        "pitfalls": "把 eventual consistency 当作唯一弱模型；在网络分区时仍承诺线性读写可用；用 2PC 代替容错共识；让单个共识组承载无限 key。",
        "check": ["线性一致系统在网络分区时通常必须牺牲什么？", ["全部持久性", "至少一侧的可用性", "所有读取"], 1, "无法通信的两侧不能同时接受可能冲突的线性写入，至少一侧需要拒绝或等待。"],
        "walk": [
            ("客户端命令", "Leader", "日志槽位", "提出值", "Leader 为命令分配递增 index 和当前 term。", "Leader 不是永久权威，合法性来自多数派。"),
            ("日志条目", "多数派复制", "Commit index", "达成共识", "多数节点持久化后，条目才能被视为提交。", "等待多数派会把最慢必要副本的延迟放入路径。"),
            ("Commit index", "状态机", "一致状态", "确定性应用", "所有节点按相同顺序执行相同命令。", "状态机包含非确定行为会导致副本分叉。"),
            ("Leader 故障", "新 term 选举", "继续服务", "恢复进展", "拥有足够新日志的候选者赢得多数票并修复落后副本。", "少数派在分区期间必须停止写入。"),
        ],
    },
    {
        "chapter": 10, "part": "Part III · 派生数据", "slug": "batch-processing",
        "titleZh": "批处理", "titleEn": "Batch Processing", "pages": "407-460",
        "thesis": "批处理把有界输入转为可重建输出。不可变输入、确定性任务和显式数据流让失败可以通过重跑恢复；MapReduce 的价值不仅是 API，而是把 shuffle、容错和数据局部性标准化。",
        "concepts": "Unix 管道通过统一字节流接口组合小工具|MapReduce 用 map、shuffle、reduce 重新分组数据|分布式 join 可在 reduce 侧或 map 侧完成|批处理输出应作为可替换派生数据而非逐条副作用",
        "evolution": "单机脚本 → 分片输入 → 幂等 map → 按 key shuffle → reduce 聚合 → DAG 调度 → 增量化与共享中间结果。",
        "case": "网页抓取与索引将 URL 清单作为不可变输入，抓取结果写对象存储，解析、去重、倒排索引各自形成 DAG 节点。失败任务重跑到临时输出，只有完整分区成功后才原子发布。",
        "pitfalls": "任务直接更新在线数据库；重试产生重复外部副作用；把所有 join 都做成全量 shuffle；中间文件无版本导致上下游混用。",
        "check": ["为什么批处理输出适合写入新目录后原子切换？", ["避免任何磁盘写入", "失败不会暴露半成品且可安全重试", "让任务无法并行"], 1, "临时输出保持不可见，全部完成后发布指针，失败时可删除并重跑。"],
        "walk": [
            ("不可变输入", "Map", "键值对", "并行转换", "按输入分片执行确定性函数，失败分片可独立重跑。", "外部副作用会破坏可重放性。"),
            ("键值对", "Shuffle", "同 key 分区", "重新分组", "按 key 分区、排序并跨网络传输到 reducer。", "数据倾斜会让单个 reducer 成为长尾。"),
            ("同 key 记录", "Reduce", "派生分区", "聚合或 join", "对同一 key 的完整记录集执行聚合。", "大 key 可能撑爆单机内存，需要二阶段聚合。"),
            ("临时输出", "原子发布", "新数据集", "提交结果", "所有分区成功后切换版本指针，旧版本保留用于回滚。", "保留过多历史版本会增加存储和治理成本。"),
        ],
    },
    {
        "chapter": 11, "part": "Part III · 派生数据", "slug": "stream-processing",
        "titleZh": "流处理", "titleEn": "Stream Processing", "pages": "461-510",
        "thesis": "流是随时间追加的事件序列。分区日志把消息持久化并允许消费者重放；正确处理事件时间、窗口、状态快照和端到端幂等，才能把实时计算从消息搬运升级为可靠数据系统。",
        "concepts": "日志型 broker 以 offset 表达消费位置并支持重放|CDC 把数据库提交日志转成变更流|事件时间与处理时间会因网络和暂停产生差异|exactly-once 通常来自事务性状态与幂等输出的组合",
        "evolution": "消息队列 → 持久分区日志 → 有状态算子 → watermark 与窗口 → checkpoint → 事务性 sink → 回放和版本化重算。",
        "case": "实时风控按账户分区保持顺序，用事件时间窗口聚合支付行为。规则版本和特征快照与告警一起记录；迟到事件可更新尚未关闭的窗口，超过允许延迟则进入补偿流。",
        "pitfalls": "把 broker 投递一次等同端到端 exactly-once；用处理时间计算业务窗口；提交 offset 后再写 sink；没有回放容量规划。",
        "check": ["watermark 的作用是什么？", ["保证网络没有延迟", "估计事件时间进度并决定何时关闭窗口", "替代所有 checkpoint"], 1, "watermark 表示系统认为不会再看到更早事件的进度估计，并非绝对保证。"],
        "walk": [
            ("事件生产者", "分区日志", "Offset", "持久化事件", "按 key 分区保持局部顺序，日志保留允许消费者重放。", "全局顺序会限制并行度。"),
            ("日志", "状态算子", "窗口状态", "按事件时间计算", "算子更新 keyed state，并用 watermark 管理窗口生命周期。", "允许更晚数据会增加状态保留和结果修正。"),
            ("状态 + Offset", "Checkpoint", "一致快照", "建立恢复点", "同时记录算子状态和输入位置，故障后从同一边界恢复。", "checkpoint 过频会消耗 I/O，过慢则增加恢复重放。"),
            ("计算结果", "幂等/事务 Sink", "外部系统", "端到端提交", "用事务、唯一事件 ID 或 upsert 保证重放不重复生效。", "最弱的 sink 决定端到端语义。"),
        ],
    },
    {
        "chapter": 12, "part": "Part III · 派生数据", "slug": "future-data-systems",
        "titleZh": "数据系统的未来", "titleEn": "The Future of Data Systems", "pages": "511-574",
        "thesis": "未来的数据架构不是一个万能数据库，而是围绕事实日志组合多个专用派生视图。正确性需要端到端审计和约束，数据使用还必须把隐私、目的限制与人的自主权纳入设计。",
        "concepts": "系统记录事实，缓存、索引和数仓是派生视图|CDC 和事件日志可连接异构存储并支持重建|端到端正确性需要审计数据流而非只信任单组件|隐私删除必须传播到所有派生数据和备份策略",
        "evolution": "点对点双写 → 单一事实源 → 变更日志 → 多个可重建投影 → 数据血缘 → 自动对账 → 隐私策略与删除事件贯穿全链路。",
        "case": "统一事件平台保留订单事实，搜索、推荐、分析和缓存各自消费并建立投影。每个投影记录来源 offset、schema 与代码版本，从而支持回放、对账和定向删除。",
        "pitfalls": "把流平台变成新的万能数据库；没有数据血缘；派生系统反向接受业务写入；只从主库删除个人数据却遗忘索引与离线特征。",
        "check": ["派生视图最重要的恢复属性是什么？", ["只能在线更新", "可从事实源重建", "必须与事实源使用同一数据库"], 1, "可重建让缓存、索引和分析表在损坏或模型变化后恢复，而不成为第二真相源。"],
        "walk": [
            ("业务命令", "事实系统", "提交日志", "记录不可争议事实", "事务边界只负责核心状态和变更事件的原子产生。", "事实模型过度承载查询需求会难以演化。"),
            ("提交日志", "CDC/事件总线", "订阅者", "传播变化", "统一顺序与 offset 让多个派生系统独立消费和重放。", "日志保留期限限制最远可恢复时间。"),
            ("订阅者", "确定性投影", "索引/缓存/数仓", "建立专用视图", "每个系统针对自身查询优化，并记录来源版本。", "不可重现的外部调用会让回放结果漂移。"),
            ("审计与删除", "数据血缘", "全链路证明", "验证正确和负责使用", "对账检测丢失更新，删除事件沿血缘传播并留下合规证明。", "删除与不可变日志之间需要密钥擦除或分层保留策略。"),
        ],
    },
]


QUESTION_SETS = {
    1: [
        ("设计短链服务", "url-shortener", "product", "设计一个全球可用的短链创建与跳转服务，重点保证跳转低延迟和链接持久性。", "1 亿月活、每日 2 亿次跳转、读写比约 100:1、P99 < 100ms", "POST /links 创建短链；GET /{code} 返回 301/302；DELETE /links/{code} 撤销", "link(code PK, target_url, owner_id, created_at, expires_at, status)", "边缘 DNS/CDN → 跳转服务 → Redis 缓存 → 分片主存储；异步点击日志进入流平台", "Base62 ID 分配|热点 key 缓存与防击穿|多地域只读副本和会话路由", "缓存与数据库不一致|恶意链接与枚举|单地域故障时跳转降级", "随机 ID 简单但需处理碰撞；发号器无碰撞但引入协调和可预测性。", "自定义短码如何防抢占？|过期链接如何回收？|301 与 302 如何选择？"),
        ("设计可扩展限流平台", "rate-limiter", "mechanism", "设计供数百个微服务共享的限流控制面与本地数据面。", "100 万规则、峰值 500 万次判定/秒、单次判定 P99 < 2ms", "Check(key, rule_id, cost)；控制面发布 RuleSnapshot(version, rules)", "rule(id, scope, algorithm, limit, window, version)；counter(key, bucket, value, expires_at)", "管理 API → 版本化规则存储 → 配置分发；服务内 sidecar/local library 执行判定，必要时访问分片计数器", "Token Bucket 与滑动窗口|本地额度租约|规则版本与故障时 fail-open/fail-closed", "集中计数器过载|配置推送延迟|时钟窗口边界突刺", "精确全局配额更公平但增加远程协调；本地租约牺牲少量精度换低延迟。", "多地域配额如何分配？|VIP 用户如何覆盖规则？|如何灰度新规则？"),
        ("排查流量突增下的 P99 延迟", "p99-latency-incident", "incident", "促销开始后平均延迟正常，但 P99 从 180ms 升到 8s，并出现级联超时。", "入口 20 万 QPS，依赖 5 个下游，线程池利用率 95%，重试流量占 35%", "按 request_id 查询 trace；按 endpoint/region/status 聚合 latency histogram", "incident(timestamp, service, symptom, change_id, mitigation)；保留 RED 指标与依赖 span", "入口限流 → 服务线程池 → 连接池 → 下游；先按排队时间定位瓶颈，再切断重试正反馈", "排队论与利用率拐点|超时预算逐层递减|重试预算、抖动退避和负载隔离", "自动扩容滞后|连接池耗尽|慢请求占住工作线程", "立即降级和限流会牺牲功能完整性，但可保护核心路径并缩短恢复时间。", "如何证明不是 GC？|何时停止重试？|事后如何设计容量演练？"),
    ],
    2: [
        ("设计社交关系与 Feed 数据层", "social-graph-feed", "product", "设计关注关系、用户主页和首页 Feed 的数据层，支持大 V 与普通用户。", "5 亿用户、日活 1 亿、峰值读 100 万 QPS、单个大 V 1 亿粉丝", "POST /follow；DELETE /follow；GET /feed?cursor=；GET /users/{id}/followers", "edge(follower_id, followee_id, created_at)；post(id, author_id, created_at)；feed_item(user_id, rank, post_id)", "关系主库分片 → 事件日志 → fan-out workers → Feed Store；大 V 采用读时合并", "边表双向索引|推拉结合 fan-out|cursor 分页与幂等事件", "大 V 发布造成写放大|取消关注后的旧 Feed|关系事件乱序", "写扩散降低读延迟但成本随粉丝数增长；读扩散节省写入但首页组装更慢。", "屏蔽关系如何生效？|共同关注如何查询？|推荐内容如何混排？"),
        ("为商品目录选择数据模型", "product-catalog-model", "mechanism", "为多品类商品目录设计关系、文档与图模型的组合边界。", "2 亿 SKU、5 万属性、每日 5000 万次搜索、每秒 2 万次库存更新", "PUT /products/{id}；GET /products/{id}；POST /search；GET /recommendations/{id}", "关系库保存 seller/category/sku 约束；文档投影保存商品详情；图投影保存兼容和搭配关系", "Catalog Command → 关系事实库 → CDC → 文档搜索索引与推荐图；库存走独立强一致服务", "聚合边界与规范化|多模型派生视图|Schema-on-write 属性治理", "双写部分失败|属性爆炸|搜索索引新鲜度下降", "单一模型运维简单但查询受限；多模型提高查询质量但必须接受异步投影与重建成本。", "新品类如何上线？|跨 SKU 唯一约束放哪里？|如何回填新索引？"),
        ("修复反规范化一致性事故", "denormalization-incident", "incident", "用户改名后订单、评论和搜索结果显示三个不同名字，批量修复又压垮主库。", "10 亿份冗余文档、每日 100 万次资料变更、修复扫描产生 4GB/s 读流量", "ProfileChanged(user_id, version, fields)；GET /repair/status；POST /repair/ranges", "profile 为事实源；投影保存 source_version；repair_job 记录范围、水位和重试", "资料库事务提交 outbox → 变更日志 → 各投影幂等更新；离线对账发现版本落后并限速修复", "版本化事件与幂等 upsert|Outbox/CDC|按分区水位对账", "事件丢失|旧事件覆盖新值|全表修复争抢 I/O", "读取时 join 保证新鲜但增加耦合；反规范化提高读性能但必须建设可靠传播和对账。", "删除用户如何传播？|如何检测投影静默停滞？|修复期间前台读什么？"),
    ],
    3: [
        ("设计搜索与自动补全存储层", "search-autocomplete", "product", "设计支持前缀联想、热度排序和分钟级更新的自动补全系统。", "10 亿词条、峰值 30 万查询/秒、每次返回 10 条、更新延迟 < 5 分钟", "GET /suggest?q=&locale=；POST /signals 批量上报选择事件", "term(prefix, phrase, locale, score, version)；signal(phrase, count, window)", "查询网关 → 内存 Trie/FST 分片 → 只读段；日志聚合生成增量段并周期合并", "前缀索引压缩|热前缀缓存|不可变段与后台 compaction", "热门前缀单分片过载|合并抖动|过期热词继续出现", "全量内存索引延迟最低但成本高；分层冷热索引节省内存但增加合并逻辑。", "拼写纠错如何加入？|个性化如何不污染公共缓存？|多语言如何分片？"),
        ("设计 LSM-Tree KV Store", "lsm-kv-store", "mechanism", "设计支持持久写入、点查、范围扫描和崩溃恢复的 LSM 存储引擎。", "单节点 2TB、写入 20 万 ops/s、P99 点查 < 10ms、对象均值 1KB", "Put(key,value,seq)；Get(key,snapshot)；Scan(start,end,snapshot)；Delete(key)", "WAL record；Memtable skiplist；SSTable data/index/filter blocks；manifest 保存文件与 level", "写入线程 → WAL → Memtable → flush queue → L0 SSTable → leveled compaction；读取合并内存和各层", "Sequence number 与 tombstone|Bloom Filter/block cache|Leveled compaction 与 snapshot", "WAL 尾部损坏|L0 文件堆积|旧 snapshot 阻止 tombstone 清理", "Size-tiered 写放大较低但读放大高；leveled 读稳定但 compaction 写放大更大。", "如何原子安装新 SSTable？|范围删除如何实现？|如何限速 compaction？"),
        ("排查 Compaction 尾延迟事故", "compaction-incident", "incident", "写入高峰时磁盘带宽打满，L0 文件持续增长，点查 P99 周期性超过 3 秒。", "写 150MB/s、compaction 350MB/s、磁盘上限 450MB/s、L0 从 8 增至 120 个文件", "暴露 level_bytes、pending_compaction_bytes、stall_seconds、read_amplification", "compaction_task(input_files, output_level, bytes, status)；记录每层文件和 key range", "前台读写与后台压实共享 I/O scheduler；先限入站写并提高 L0 紧急度，再重新配置层级和带宽", "Compaction debt|I/O admission control|Subcompaction 与热点 key range", "写停顿阈值过晚|大 compaction 长时间占盘|缓存被扫描污染", "降低压实会暂时保护写延迟但积累读放大；加速压实会抢占前台 I/O，需动态预算。", "如何区分磁盘故障？|为什么加缓存未必有效？|如何做可重复压测？"),
    ],
    4: [
        ("设计可演进的公共 API 与事件格式", "evolvable-api-events", "product", "设计跨团队使用十年的订单 API 与事件契约，允许独立发布和回放历史数据。", "200 个消费者、每日 20 亿事件、历史保留 7 年、每周数十次 schema 变更", "POST /orders v2；OrderCreated schema；GET /schemas/{subject}/versions", "字段使用稳定编号；事件含 event_id、schema_version、occurred_at、aggregate_version", "API Gateway → Order Service/事实库 → Outbox → Event Log → Schema Registry → Consumers", "向前/向后兼容|不可变事件与新事件类型|消费者契约测试", "字段语义变化|默认值歧义|旧消费者无法解析枚举", "新增事件类型更清晰但增加消费者迁移；在旧事件加可选字段更平滑但容易积累含糊语义。", "删除字段的安全条件？|PII 如何处理？|如何支持回放时的旧代码？"),
        ("设计 Schema Registry", "schema-registry", "mechanism", "设计高可用 Schema Registry，阻止不兼容格式进入生产。", "10 万 subject、500 万 schema 版本、发布峰值 1000 次/秒、读取 20 万次/秒", "Register(subject,schema,mode)；CheckCompatibility；GetById；ListVersions", "schema(id, fingerprint, canonical_text)；subject_version(subject, version, schema_id, state)", "无状态 API → 强一致元数据存储 → 缓存/CDN；CI 与 producer SDK 在发布前查询", "Canonicalization 与 fingerprint|兼容规则图|版本状态机和不可复用 ID", "双主分配冲突 ID|缓存旧规则|恶意超大 schema", "中心 Registry 提供统一治理但成为发布依赖；客户端缓存提高可用性但必须有明确过期策略。", "跨地域如何分配 ID？|规则升级如何灰度？|Registry 不可用时能否生产？"),
        ("处理滚动发布反序列化故障", "serialization-rollout-incident", "incident", "新 producer 发布后 8% 的旧消费者进入毒消息重启循环，队列积压迅速增长。", "500 个 consumer 实例、积压每分钟增加 300 万条、最大事件 2MB", "DLQ(topic, partition, offset, schema_id, error)；兼容性审计查询 producer/consumer version", "deployment(version, schema_range)；consumer_capability(group, max_schema_id)；poison_event 记录失败", "暂停新 producer → 隔离毒消息到 DLQ → 恢复旧格式生产 → 修复消费者 → 受控回放", "Consumer capability inventory|DLQ 与跳过策略|Schema gate 和 canary topic", "无限重试阻塞分区|跳过破坏业务顺序|回滚代码但新数据仍存在", "跳过消息可恢复吞吐但可能破坏状态；停分区保护正确性但扩大业务不可用。", "如何确认影响范围？|如何回放保持顺序？|怎样防止再次发生？"),
    ],
    5: [
        ("设计多地域用户数据服务", "multi-region-profile", "product", "设计支持全球低延迟读取、用户资料编辑和地域故障切换的服务。", "10 亿用户、20 万读 QPS、2 万写 QPS、跨洲 RTT 150ms", "PUT /profiles/{id} 带 version；GET /profiles/{id} 带 session watermark", "profile(user_id, version, fields, home_region, updated_at)；replication_log(lsn, mutation)", "Geo Router → home-region Leader → 本地副本；异步复制到其他地域，客户端携带写入 LSN", "Read-your-writes 路由|异步复制与 RPO|故障切换 fencing", "写后读落后|旧 Leader 复活|同用户多地并发写", "单归属地域冲突少但跨地域写慢；多主写可用性高但需要字段级合并语义。", "用户迁移地域如何做？|GDPR 数据驻留？|全地域断网如何降级？"),
        ("设计 Leaderless Quorum KV Store", "leaderless-quorum-kv", "mechanism", "设计 Dynamo 风格的无主复制 KV Store，支持节点故障下读写。", "100 节点、RF=3、100 万 ops/s、对象 4KB、99.99% 可用", "Put(key,value,context) 返回 version；Get(key) 返回 sibling versions；Repair(key)", "value(key, version_vector, payload, tombstone, timestamp)；hint(target_node, mutation)", "Coordinator → preference list 上 N 个副本；并行等待 W 写确认或 R 读响应；后台 repair", "Version Vector|Sloppy quorum 与 hinted handoff|Read repair 与 anti-entropy", "并发 sibling 爆炸|墓碑过早清理导致数据复活|网络分区后冲突", "较小 R/W 提高可用性和延迟，但增加读到旧值和冲突合并概率。", "大对象如何处理？|成员变更如何影响 preference list？|什么时候不能用 LWW？"),
        ("处理复制延迟与冲突事故", "replication-lag-incident", "incident", "主地域网络抖动后跨地域复制延迟 40 分钟，用户编辑被旧值覆盖并看到时间倒退。", "复制日志积压 12TB、峰值恢复带宽 8Gbps、冲突用户 240 万", "查询 replica_lag_lsn；按 user_id 查看 mutation history；冻结高风险字段写入", "mutation(user_id, field, logical_version, region, event_id)；repair_decision 记录合并来源", "先阻止自动 failover → 会话读回主地域 → 限速追日志 → 用版本向量识别并发 → 业务规则合并", "Per-field version|Monotonic session routing|冲突审计与人工恢复", "LWW 时钟漂移|追赶流量压垮主库|缓存继续返回旧值", "强制主读会增加跨洲延迟但恢复一致体验；继续本地读可保性能却扩大用户困惑。", "如何计算可接受 RPO？|何时允许 failover？|修复结果如何通知用户？"),
    ],
    6: [
        ("设计海量聊天记录分片", "sharded-chat-history", "product", "设计长期保存、按会话翻页和支持超大群聊的消息存储。", "5 亿日活、每日 500 亿消息、保留 7 年、普通会话 P99 读 < 150ms", "POST /conversations/{id}/messages；GET ...?before=cursor；DELETE /messages/{id}", "message(conversation_bucket, sequence, message_id, sender, payload, created_at)；cursor 含 shard 与 sequence", "Chat Gateway → sequence allocator → 分片消息库 → 对象存储附件；索引流构建搜索", "conversation_id + time bucket 分区|会话内 sequence|冷热分层与 cursor", "超大群聊热点|跨桶翻页|删除传播到搜索索引", "按会话分区读取简单但大群热点；加入时间桶可扩展写入但增加跨桶读取。", "多设备已读位置？|附件如何去重？|如何做法律保留？"),
        ("设计一致性哈希与在线再均衡", "consistent-hash-rebalance", "mechanism", "设计缓存/存储集群的逻辑分区、路由和无停机再均衡协议。", "1000 节点、65536 虚拟分区、每次扩容 5%、迁移限额 20GB/s", "Locate(key, epoch)；MovePartition(id, from, to)；CommitOwnership(epoch)", "partition(id, owner, next_owner, epoch, state, checkpoint)；node(id, zone, capacity)", "Router 缓存所有权表；Controller 生成迁移计划；Source 快照复制并追增量；共识元数据提交新 epoch", "虚拟分区与加权放置|快照 + 增量追赶|Epoch fencing", "旧路由写错节点|同机架副本|迁移引发缓存雪崩", "更小虚拟分区让均衡细腻但增加元数据和文件碎片；更大分区相反。", "节点突然死亡怎么迁？|异构容量怎么加权？|如何回滚半完成迁移？"),
        ("处理热点分片与扩容雪崩", "hot-shard-incident", "incident", "直播事件让单个分片达到平时 80 倍流量，自动扩容同时触发大量迁移并拖慢整个集群。", "热点 300k QPS、单分片上限 25k、迁移占 70% 网络、错误率 18%", "hot_key dashboard；PauseRebalance；OverrideRoute(key,salt,ttl)", "hotspot(key, qps, shard, detected_at)；override(key, subshards, expires_at)", "入口检测热 key → 临时请求合并/缓存 → key salting 分裂热读 → 暂停全局再均衡 → 稳态后逐步恢复", "热点检测与 heavy hitters|请求合并|临时子分片和迁移 admission control", "扩容控制环震荡|缓存同时失效|写入顺序被 salting 破坏", "局部特殊处理会增加路由复杂度，但比为一个热点移动全局数据更可控。", "写热点怎么拆？|如何避免永久 override？|自动化阈值如何验证？"),
    ],
    7: [
        ("设计票务预订与支付事务", "ticket-booking", "product", "设计演唱会座位选择、短时锁定、支付和超时释放。", "开票峰值 100 万请求/秒、10 万座位、锁定 5 分钟、绝不重复售票", "POST /holds；POST /holds/{id}/confirm；POST /payments/webhook；GET /orders/{id}", "seat(event_id, seat_id, state, version)；hold(id, expires_at, state)；order(id, hold_id, payment_state)", "Edge Queue → Booking Service → 串行化座位分区/强一致 DB → Payment Saga → 超时扫描器", "唯一约束与条件写|Hold 状态机|支付幂等键和补偿", "重复 webhook|锁过期与支付并发|库存缓存陈旧", "严格排队降低峰值吞吐但保护库存正确性；乐观重试吞吐高但冲突时体验差。", "连座如何原子选择？|支付成功但确认超时？|黄牛限流如何做？"),
        ("设计 MVCC 与 SSI", "mvcc-ssi-engine", "mechanism", "为关系数据库设计快照可见性、垃圾回收和 Serializable Snapshot Isolation。", "1TB 热数据、10 万事务/秒、95% 读、最长快照 30 分钟", "Begin() 返回 snapshot；Read(key,snapshot)；Commit(read_set,write_set)", "version(key, xmin, xmax, value)；transaction(id, state, snapshot)；rw_dependency(from,to)", "Transaction Manager 分配时间戳；版本链服务快照读；Commit 检测 ww 冲突和危险 rw 结构；GC 清理不可见版本", "Snapshot visibility|Predicate/范围读跟踪|SSI dangerous structure", "长事务撑爆版本|误中止风暴|索引幻读未跟踪", "精确谓词锁更少误中止但实现复杂；粗粒度范围跟踪简单却降低并发。", "崩溃恢复依赖什么日志？|只读事务如何优化？|分布式 SSI 怎么做？"),
        ("排查 Write Skew 与重复预订", "write-skew-incident", "incident", "两个值班医生同时申请休假，各自看到仍有一人值班并成功提交，最终无人值班；票务也出现类似重复预订。", "异常率 0.02%，只在高并发出现，当前隔离级别 snapshot isolation", "复现事务读写集；查询 overlapping transaction trace；临时启用约束/串行化", "on_call(doctor, shift, enabled)；booking(resource, slot, owner)；记录 transaction_id 与 snapshot", "识别跨行不变量 → 将不变量物化为可锁行或唯一约束 → 关键事务改 SSI/serializable → 客户端重试", "Materialized conflict|SELECT FOR UPDATE|Serializable retry loop", "只加应用锁漏路径|序列化失败未重试|历史脏数据阻塞约束上线", "全局提升隔离简单但吞吐成本大；只保护关键不变量更高效但需完整识别写路径。", "如何在线清理重复数据？|约束如何跨分区？|测试如何稳定复现？"),
    ],
    8: [
        ("设计带 Lease 的分布式任务调度器", "lease-job-scheduler", "product", "设计可重试、避免并发提交并支持 worker 崩溃恢复的任务系统。", "每日 10 亿任务、10 万 worker、任务 100ms 到 2h、至少一次调度", "POST /jobs；Claim(worker,capability)；Heartbeat(job,token)；Complete(job,token,result)", "job(id,state,attempt,lease_until,fencing_token,payload_ref)；result(job_id,token,status)", "API → 分片队列 → Lease Coordinator → Workers → token-aware Result Store；Reaper 回收过期任务", "Lease 续约|单调 fencing token|幂等结果与最大重试", "GC pause 后旧 worker 写入|长任务误回收|毒任务无限重试", "较短 lease 恢复快但心跳和误判多；较长 lease 稳定但故障恢复慢。", "任务依赖 DAG？|取消如何传播？|恰好一次副作用怎么办？"),
        ("设计故障检测与 Fencing", "failure-detector-fencing", "mechanism", "设计集群成员故障检测、lease 授予和资源层 fencing 协议。", "5000 节点、跨 3 可用区、心跳 1 秒、目标检测时间 < 10 秒", "Heartbeat(node,incarnation)；Acquire(resource) 返回 token；Write(resource,token)", "member(node,incarnation,last_seen,status)；lease(resource,holder,token,expires_at)", "Gossip detector 提供 suspicion；quorum 协调器发 lease/token；每个存储资源持久化 max_token", "Phi accrual failure detector|Incarnation number|Quorum lease 与 token 检查", "网络拥塞误判|节点重启复用身份|部分写路径绕过 token", "更激进检测缩短恢复但增加误判；suspicion 阶段可吸收短暂抖动。", "跨区域延迟变化？|Byzantine 节点？|token 溢出如何处理？"),
        ("处理时钟漂移与 Split-Brain", "clock-split-brain-incident", "incident", "NTP 故障和长 GC 让两个控制器都认为自己持有锁，并分别向存储写入配置。", "两控制器时钟相差 90 秒、GC pause 45 秒、错误配置传播到 30% 节点", "冻结控制面写；查询 lease token、term、config revision；按单调 revision 回滚", "config(revision,term,payload,status)；lease(holder,token)；audit(actor,token,operation)", "停止旧 term → 选择多数派提交的最高 revision → 回滚少数派写 → 在所有 sink 强制 token → 故障注入验证", "Monotonic clock 仅测时长|Quorum authority|Term/revision fencing", "依赖墙钟过期|旧 Leader 恢复|缓存接受未提交配置", "停写恢复牺牲短期可用性但保护控制面正确性；继续双主会让损害不可界定。", "如何证明哪份配置有效？|数据面是否继续服务？|怎样监控时钟健康？"),
    ],
    9: [
        ("设计高可用配置与元数据服务", "metadata-service", "product", "设计类似 etcd/ZooKeeper 的小数据强一致服务，支持 watch、租约和成员变更。", "10GB 元数据、5 万写/秒、50 万 watch 客户端、跨 3 AZ", "Put(key,value,precondition)；Range(prefix,revision)；Watch(prefix,from_revision)；LeaseGrant", "revisioned KV；raft_log(index,term,command)；lease(id,ttl,keys)", "Client → 任意节点转 Leader → Raft quorum → MVCC KV；Watch Hub 从提交日志分发", "线性读与 revision|复制状态机|Watch 压缩与慢消费者", "慢 watcher 占内存|Leader 频繁切换|大 value 阻塞日志", "强一致控制面适合小而关键的数据；大对象外置可保护共识延迟但增加引用管理。", "只读如何扩展？|成员替换流程？|租约过期如何确定？"),
        ("设计共识日志与 Leader Election", "consensus-log", "mechanism", "设计基于 term、quorum 和复制日志的容错共识模块。", "5 节点、容忍 2 故障、日志每秒 2 万条、快照 1GB", "RequestVote(term,last_index,last_term)；AppendEntries；InstallSnapshot", "persistent current_term/voted_for/log；volatile commit_index/next_index/match_index", "Follower timeout → Candidate 拉票 → Leader 复制日志 → 多数派提交 → 状态机应用 → 定期快照", "Election safety|Log matching|Commit rule 与 joint consensus", "双候选反复分票|旧 term 条目错误提交|快照安装中断", "更长选举超时稳定但故障切换慢；更短超时恢复快却对网络抖动敏感。", "成员变更为何要 joint consensus？|客户端重试去重？|读如何保证线性？"),
        ("处理 2PC 协调者故障", "two-phase-commit-incident", "incident", "跨库转账在 prepare 后协调者磁盘损坏，参与者持锁等待，交易队列逐步停摆。", "8 个分片、4 万 in-doubt 事务、锁等待 P99 60 秒、无可用协调者副本", "ListPrepared(txn_id)；RecoverDecision(txn_id)；FenceCoordinator(epoch)", "transaction(txn_id,participants,state,decision,coordinator_epoch)；participant prepared_lsn", "隔离旧协调者 → 从持久日志/多数副本恢复决定 → 未知事务保持阻塞或按业务补偿 → 分批释放锁", "Prepare record 持久化|协调者高可用|Presumed abort/commit 与启发式决定", "单点协调日志丢失|参与者超时自行提交|锁扩散导致级联", "保持阻塞保护原子性但降低可用性；启发式中止恢复业务却可能产生需人工修复的不一致。", "为何不能让参与者投票决定？|Saga 是否更合适？|如何缩短 prepare 窗口？"),
    ],
    10: [
        ("设计批量网页抓取与索引流水线", "batch-crawl-index", "product", "设计可重跑、去重并每天构建新搜索索引的批处理平台。", "100 亿 URL、每日抓取 5PB、10 万 worker、索引发布时间 < 12 小时", "SubmitSnapshot(seed_version)；GetJobStatus；PublishIndex(version)；robots fetch", "url_record(url_hash,status,etag,last_fetch)；dataset(version,partitions,checksum)；job_attempt", "Seed → URL frontier → Fetch Map → Object Store → Parse/Dedup → Shuffle → Index Reduce → Atomic Publish", "内容寻址去重|分区级幂等输出|数据局部性和原子版本发布", "抓取风暴伤害站点|单域热点|半成索引被发布", "全量构建简单可验证但成本高；增量构建更快却需要处理删除和版本依赖。", "robots.txt 如何保证？|索引回滚？|重复 URL canonicalization？"),
        ("设计分布式 Join 与 MapReduce", "distributed-join", "mechanism", "设计支持 reduce-side join、map-side join 和倾斜处理的批计算执行器。", "输入 20PB、10 万 task、key 基数 10 亿、最大热 key 占 4%", "SubmitDAG；MapTask(split)；ShuffleFetch(partition)；CommitAttempt", "shuffle_block(job,map,partition,checksum)；task_attempt(state,worker,output)", "Scheduler 数据本地放置 map；分区排序写 shuffle；reducer 拉取同分区；Output Committer 选唯一 attempt", "Partitioner 与外部排序|Broadcast/map-side join|Skew key sampling 与 salting", "热 reducer|重复 attempt 重复发布|shuffle 文件丢失", "Reduce-side join 通用但网络大；map-side join 快但要求输入预分区或小表可广播。", "推测执行如何避免副作用？|Worker 丢失如何恢复？|多阶段 DAG 怎么缓存？"),
        ("处理 Straggler 与重复输出", "batch-straggler-incident", "incident", "99.8% 任务已完成但少数 reducer 持续 4 小时，推测执行又生成重复账单文件。", "5 万 reducer、100 个热 key、重复输出金额 800 万、shuffle 40PB", "查询 task progress/key histogram；暂停 publish；按 attempt token 审计输出", "task_attempt(id,logical_task,token,state)；output_partition(version,partition,winning_token)", "隔离发布 → 选 winning attempt → 清理重复副作用 → 对热 key 二次分片 → 用原子 output committer 重跑", "Speculative execution|Skew sampling|Commit token 与临时目录", "外部 API 非幂等|热 key 单 reducer|慢机器被反复调度", "推测执行缩短硬件长尾，但对数据倾斜无效且会增加资源与副作用风险。", "如何识别慢机还是热 key？|账单如何对账？|何时自动 salting？"),
    ],
    11: [
        ("设计实时风控与指标平台", "realtime-risk-metrics", "product", "设计支付事件的实时风控、分钟指标和可回放审计平台。", "峰值 200 万事件/秒、规则延迟 P99 < 100ms、保留 30 天可回放", "Ingest(event)；UpdateRules(version)；QueryMetric(window)；ExplainDecision(event_id)", "event(event_id,account_id,event_time,payload)；feature(account,window,state)；decision(rule_version,reasons)", "Gateway → 分区日志 → 特征/窗口算子 → 规则引擎 → 决策 sink；原始事件进对象存储", "按账户分区|事件时间 watermark|规则与特征版本化", "迟到交易漏判|规则更新不一致|回放重复告警", "同步风控延迟低但影响支付可用性；异步风控更稳健但只能事后处置部分风险。", "跨账户团伙识别？|规则回滚？|数据隐私如何处理？"),
        ("设计 Exactly-Once 窗口处理器", "exactly-once-stream", "mechanism", "设计有状态流引擎的 checkpoint、窗口、迟到数据和事务性输出。", "1000 万事件/秒、1TB 状态、checkpoint 每 30 秒、恢复 < 5 分钟", "Process(record,offset)；Barrier(checkpoint_id)；CommitSink(checkpoint_id)", "operator_state(key,window,value)；checkpoint(id,input_offsets,state_handles,sink_txn)", "Source 注入 barrier → 算子对齐并快照 → sink 预提交 → coordinator 完成后提交 → 故障从最近完成点恢复", "Chandy-Lamport barrier|Incremental checkpoint|Two-phase sink 或幂等 upsert", "Barrier alignment 背压|状态快照失败|sink 事务超时", "同步 checkpoint 语义清晰但会阻塞；异步快照吞吐高但需处理写时复制和对齐。", "Unaligned checkpoint 何时用？|Rescale 如何迁状态？|迟到数据如何修正？"),
        ("处理迟到数据、回放与背压", "stream-backpressure-incident", "incident", "移动端离线恢复后涌入 6 小时旧事件，窗口状态暴涨，消费者 lag 和背压传播到生产端。", "积压 80 亿事件、状态增长 4TB、watermark 停滞 40 分钟、sink 吞吐下降 60%", "查看 per-partition lag/watermark/state bytes；切换 late-event policy；隔离回放 topic", "late_event(event_id,event_time,arrival_time,reason)；replay_job(range,rate,status)", "限制回放速率 → 旧事件分流 → 延长/关闭部分窗口 → 扩展状态 backend → sink 恢复后逐层解除背压", "Watermark idle partition|Backpressure propagation|Late side output 与补偿计算", "无限 allowed lateness|回放和实时流争资源|checkpoint 随状态变慢", "接受更晚数据提高准确性但增加状态和结果修正；截止更早保护实时 SLA 但需离线补偿。", "如何避免生产端数据丢失？|哪些指标先告警？|回放如何不重复通知？"),
    ],
    12: [
        ("设计统一事件驱动数据平台", "unified-event-platform", "product", "设计以事实日志连接交易库、搜索、推荐、缓存和数仓的数据平台。", "每日 50 万亿事件、5000 topic、2000 消费组、保留 30 天", "Publish(event, schema_id)；Subscribe(topic,offset)；RegisterProjection；Replay(range)", "event_id、aggregate_id/version、schema_id、source_txn、lineage；projection 记录 input offsets/code version", "业务库 + Outbox/CDC → 分区日志 → Schema/Lineage Catalog → 多个投影 → 对账平台", "单一事实源与派生视图|事务 outbox|血缘、版本和可重建性", "循环事件|投影静默落后|重放污染在线结果", "中心事件平台降低点对点耦合，但必须避免把所有业务语义和查询都塞进 broker。", "跨 topic 事务？|成本分摊？|事件保留到期后如何重建？"),
        ("用 CDC 构建派生视图", "cdc-derived-views", "mechanism", "设计从数据库提交日志构建搜索索引、缓存和分析表的 CDC 管道。", "源库 100 万变更/秒、20 个投影、允许 30 秒延迟、全量快照 500TB", "StartSnapshot(lsn)；ReadChanges(from_lsn)；Apply(projection,key,version)", "change(table,pk,op,before,after,commit_lsn)；projection_checkpoint(name,lsn,schema_version)", "一致快照记录起始 LSN → 并行回填 → 缓冲增量 → 按 key/commit 顺序追平 → 原子切换投影别名", "Snapshot + log handoff|幂等版本 upsert|Schema change handling", "快照与日志缝隙|DDL 破坏解析|删除 tombstone 丢失", "直接双写延迟低但原子性差；CDC 可靠解耦但引入异步延迟和日志依赖。", "无主库如何 CDC？|投影校验怎么做？|大事务如何处理？"),
        ("处理跨系统隐私删除事故", "privacy-deletion-incident", "incident", "用户删除请求在主库完成，但搜索、特征库、缓存和备份仍可找到个人数据。", "30 个下游、10PB 派生数据、删除 SLA 30 天、发现 4 个无血缘影子系统", "POST /privacy/deletions；GET /deletions/{id}/proof；各 sink AckDeletion", "deletion_request(subject,scope,deadline)；lineage(dataset,sources,owner)；deletion_ack(system,version,evidence)", "冻结违规访问 → 从目录展开血缘 DAG → 发布版本化删除事件 → 各系统 tombstone/重建/密钥擦除 → 汇总证明并持续扫描", "Data lineage|Crypto-shredding|删除 tombstone 保留与重建过滤", "旧备份恢复数据复活|消费者漏订阅|匿名化可逆", "立即物理删除最直观但对不可变备份昂贵；密钥擦除和保留期策略可操作但需严格证明不可恢复。", "日志本身如何删除？|模型训练数据怎么办？|如何发现未知副本？"),
    ],
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def chapter_markdown(ch: dict) -> str:
    concepts = bullets(ch["concepts"])
    q = ch["check"]
    return f'''---
chapterId: ch{ch['chapter']:02d}
part: "{ch['part']}"
order: {ch['chapter']}
title: "Ch{ch['chapter']} · {ch['titleZh']}"
titleZh: "{ch['titleZh']}"
titleEn: "{ch['titleEn']}"
sourcePages: "PDF {ch['pages']}"
walkthroughPath: "/chapters/{ch['slug']}"
questionPaths:
{chr(10).join('  - /questions/' + item[1] for item in QUESTION_SETS[ch['chapter']])}
visualizationPaths: ["walkthrough-explorer"]
description: "DDIA 第 {ch['chapter']} 章交互式中文导读"
---

# Ch{ch['chapter']} · {ch['titleZh']}

<p class="chapter-subtitle">{ch['titleEn']}</p>

> **阅读范围**：DDIA 第一版 Chapter {ch['chapter']}，源 PDF 第 {ch['pages']} 页。本文为学习导读，概念与图示均应回到原书上下文理解。

<ProgressToggle id="chapter-{ch['chapter']}" label="完成本章" />

## 问题背景

{ch['thesis']}

## 核心模型

{concepts}

<WalkthroughExplorer :chapter="{ch['chapter']}" />

## 工作机制

上面的交互图把本章机制压缩为四个可检查步骤。阅读时不要只记组件名称，而要追问：**状态在哪里、顺序由谁决定、失败后从哪里恢复、哪一条保证会在扩展时最先变贵**。这些问题也是系统设计面试从“画框”进入工程判断的分界线。

## 逐步演进

{ch['evolution']}

## 生产案例

{ch['case']}

## 设计权衡

| 维度 | 应当回答的问题 |
| --- | --- |
| 正确性 | 哪些不变量绝不能破坏？允许多旧的数据？ |
| 性能 | 瓶颈是 CPU、内存、网络、磁盘还是协调？ |
| 可用性 | 分区或依赖失败时，拒绝、等待还是降级？ |
| 运维性 | 如何观测积压、版本、水位和恢复进度？ |
| 演化性 | Schema、分区和拓扑变化能否在线完成？ |

## 常见误区

{ch['pitfalls']}

<KnowledgeCheck question="{q[0]}" :options='{json.dumps(q[1], ensure_ascii=False)}' :answer="{q[2]}" explanation="{q[3]}" />

## 本章面试题

{chr(10).join(f'{i}. [{item[0]}](/questions/{item[1]})' for i, item in enumerate(QUESTION_SETS[ch['chapter']], 1))}

## 来源

- Martin Kleppmann, *Designing Data-Intensive Applications*, First Edition, Chapter {ch['chapter']}, PDF pp. {ch['pages']}.
- 本文为中文学习笔记与原创交互重构，不替代原书。
'''


def question_markdown(ch: dict, item: tuple, index: int) -> str:
    title, slug, mode, scenario, scale, api, model, architecture, mechanisms, risks, tradeoff, followups = item
    mode_name = {"product": "产品系统题", "mechanism": "底层机制题", "incident": "生产事故题"}[mode]
    if mode == "incident":
        clarify = "确认事故开始时间、受影响地域与用户比例；列出最近变更；确定正确性是否已经受损；区分止血目标与根因修复。"
        functional = "恢复核心服务；阻止损害继续扩大；保留审计证据；修复受损数据并建立复发防线。"
    elif mode == "mechanism":
        clarify = "明确需要提供的抽象与不变量、故障模型、持久性边界、并发规模，以及调用者是否能够重试。"
        functional = "提供稳定接口；在节点或进程故障后恢复；支持在线扩容和观测；用测试证明核心不变量。"
    else:
        clarify = "确认核心用户旅程、读写比例、数据保留、地域范围、延迟 SLO、一致性需求，以及哪些功能允许降级。"
        functional = "先覆盖核心写入与读取路径，再加入扩展、治理与恢复能力；非核心功能不应污染第一版关键路径。"
    mechanisms_md = bullets(mechanisms)
    risks_md = bullets(risks)
    followups_md = bullets(followups)
    arch_steps = "\n".join(f"{i}. **{step.strip()}**" for i, step in enumerate(architecture.split("→"), 1))
    return f'''---
chapterId: ch{ch['chapter']:02d}
part: "{ch['part']}"
order: {ch['chapter'] * 10 + index}
title: "{title}"
questionType: "{mode}"
sourcePages: "PDF {ch['pages']}"
walkthroughPath: "/chapters/{ch['slug']}"
description: "基于 DDIA Chapter {ch['chapter']} 的{mode_name}完整解答"
---

# {title}

<div class="question-meta"><span>Ch{ch['chapter']}</span><span>{mode_name}</span><span>中高级</span></div>

## 题干

{scenario}

<ProgressToggle id="question-{slug}" label="完成本题" />

::: tip 练习方式
先用 5 分钟写出澄清问题和两个关键不变量，再逐步展开答案。面试官关心的是你的决策依据，不是组件数量。
:::

## 参考答案

<AnswerStep title="1. 候选人澄清问题">

{clarify}

- 规模基线：{scale}。
- 追问数据是否允许丢失、重复或短暂陈旧，以及降级时必须保留的最小体验。

</AnswerStep>

<AnswerStep title="2. 功能与非功能需求">

**功能范围**：{functional}

**非功能目标**：把题目中的规模转成吞吐、存储、带宽、尾延迟和恢复目标；所有目标都标明量级与假设，而不是给出没有依据的精确数字。

</AnswerStep>

<AnswerStep title="3. 容量估算">

以 `{scale}` 为容量基线。先按峰均比 5 倍预留入口吞吐，再计算 `日增量 = 峰值写入 × 平均对象大小 × 有效写入秒数`。副本、索引、WAL/日志和压缩前空间分别计入，生产容量至少保留 30% 运维余量。

面试中应明确：缓存按工作集而非全量数据估算；网络同时考虑复制、再均衡和恢复流量；P99 容量不能只用平均 QPS 推导。

</AnswerStep>

<AnswerStep title="4. API 与数据模型">

**核心接口**：{api}。

**核心数据**：{model}。

所有修改接口携带 `request_id` 或幂等键；游标包含稳定排序键而不是裸 offset；数据记录保留版本/epoch，便于检测旧写、回放和在线迁移。

</AnswerStep>

<AnswerStep title="5. 高层架构">

{arch_steps}

入口层只做鉴权、限流和路由；状态所有权、顺序和提交边界必须在图上标清。异步路径暴露 lag、水位和失败队列，不能用“最终一致”四个字跳过恢复设计。

</AnswerStep>

<AnswerStep title="6. 关键机制">

{mechanisms_md}

这些机制分别回答三类问题：如何确定顺序或所有权、如何在失败后重试而不重复生效、如何在扩容或迁移期间保持可观测且可回滚。

</AnswerStep>

<AnswerStep title="7. 扩展、故障与恢复">

{risks_md}

故障处理顺序应是：保护正确性 → 限制影响面 → 恢复核心流量 → 修复派生状态 → 完成复盘。为每个异步边界设置积压告警，为每个所有权变更设置 epoch/fencing，为每个重试路径设置预算和幂等性。

</AnswerStep>

<AnswerStep title="8. 核心权衡">

{tradeoff}

没有“同时最强”的设计。最终选择应回扣题目的 SLO、故障模型、团队运维能力和成本，并说明什么时候需要从当前方案演进到下一阶段。

</AnswerStep>

<AnswerStep title="9. 面试官追问">

{followups_md}

</AnswerStep>

<AnswerStep title="10. 评分点">

| 维度 | 合格 | 优秀 |
| --- | --- | --- |
| 需求 | 能确认核心路径与规模 | 主动定义不变量、SLO 与降级边界 |
| 数据 | 给出可用模型与索引 | 解释版本、幂等、迁移和删除 |
| 架构 | 组件能串成完整路径 | 明确状态、顺序、背压和所有权 |
| 分布式权衡 | 知道复制、分区或事务概念 | 能把保证与延迟、可用性、成本对应 |
| 故障处理 | 能列举常见失败 | 有检测、隔离、恢复、对账和演练闭环 |

</AnswerStep>

## 对应 DDIA 知识

本题主要对应 Chapter {ch['chapter']} **{ch['titleEn']}**，源 PDF 第 {ch['pages']} 页。答案结合了原书概念与原创生产化设计，不代表原书提供了该题的唯一解法。
'''


def build_manifest() -> tuple[list[dict], dict]:
    manifest = []
    walks = {}
    for ch in CHAPTERS:
        questions = []
        for item in QUESTION_SETS[ch["chapter"]]:
            questions.append({"title": item[0], "shortTitle": item[0], "slug": item[1], "type": item[2], "path": f"/questions/{item[1]}"})
        manifest.append({
            "chapter": ch["chapter"], "chapterId": f"ch{ch['chapter']:02d}", "part": ch["part"],
            "slug": ch["slug"], "titleZh": ch["titleZh"], "titleEn": ch["titleEn"],
            "sourcePages": ch["pages"], "walkthroughPath": f"/chapters/{ch['slug']}", "questions": questions,
        })
        walks[str(ch["chapter"])] = {
            "title": ch["titleZh"],
            "steps": [{"from": s[0], "focus": s[1], "to": s[2], "label": s[3], "detail": s[4], "tradeoff": s[5]} for s in ch["walk"]],
        }
    return manifest, walks


def main() -> None:
    manifest, walks = build_manifest()
    write(DOCS / ".vitepress/content.mjs", "export const chapters = " + json.dumps(manifest, ensure_ascii=False, indent=2) + "\n\nexport const walkthroughs = " + json.dumps(walks, ensure_ascii=False, indent=2))
    write(ROOT / "data/site-content.json", json.dumps({"chapters": manifest, "walkthroughs": walks}, ensure_ascii=False, indent=2))

    for ch in CHAPTERS:
        write(DOCS / "chapters" / f"{ch['slug']}.md", chapter_markdown(ch))
        for index, item in enumerate(QUESTION_SETS[ch["chapter"]], 1):
            write(DOCS / "questions" / f"{item[1]}.md", question_markdown(ch, item, index))

    chapter_links = "\n".join(f"- [Ch{c['chapter']} · {c['titleZh']}]({c['walkthroughPath']}) — {c['titleEn']}" for c in manifest)
    question_sections = []
    for c in manifest:
        links = "\n".join(f"- [{q['title']}]({q['path']})" for q in c["questions"])
        question_sections.append(f"## Ch{c['chapter']} · {c['titleZh']}\n\n{links}")

    write(DOCS / "index.md", """---
layout: page
title: DDIA 系统设计学习站
description: 12 章交互式导读与 36 道系统设计面试题
---

<LearningDashboard />
""")
    write(DOCS / "chapters/index.md", f"""---
title: 章节导读
description: DDIA 第一版 12 章交互式中文 walkthrough
---

# 章节导读

从数据系统基础，到分布式数据，再到派生数据。每章包含机制步进、生产案例、权衡和知识检查。

{chapter_links}
""")
    write(DOCS / "questions/index.md", f"""---
title: 系统设计面试题
description: 36 道产品、机制与事故系统设计题
---

# 36 道系统设计面试题

每章包含一题产品系统、一题底层机制和一题生产事故。答案默认折叠，建议先独立作答。

{chr(10).join(question_sections)}
""")
    write(DOCS / "about.md", """---
title: 关于本站
---

# 关于本站

本站以 Martin Kleppmann 的 *Designing Data-Intensive Applications* 第一版为阅读主线，用中文交互式导读和系统设计面试题连接书中原理与生产工程判断。

原书 PDF 与拆分文件仅用于私人学习，不进入 Git 仓库或 GitHub Pages。引用的书中图示会标注章节和页码，其版权归原作者及 O'Reilly Media 所有。本站的中文笔记、题目与交互实现不替代原书。

## 内容边界

- 12 章 walkthrough 对应当前 PDF 的物理页码。
- 36 道题为原创练习，答案是一条可辩护的设计路径，而非唯一标准答案。
- 学习进度只保存在当前浏览器的 `localStorage`，不会上传。
""")
    print(f"Generated {len(CHAPTERS)} walkthroughs and {sum(len(v) for v in QUESTION_SETS.values())} questions")


if __name__ == "__main__":
    main()
