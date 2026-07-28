from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Article, Category, Tag


LEGACY_SLUGS = [
    "understanding-solitude",
    "how-my-digital-garden-grows",
    "walking-along-the-coast",
    "reading-as-a-long-conversation",
]

CATEGORY_SLUGS = {
    "AI运维": "aiops",
    "智能自动化": "automation",
    "云原生": "cloud-native",
    "故障复盘": "postmortem",
}

TAG_SLUGS = {
    "LLMOps": "llmops",
    "OpenTelemetry": "opentelemetry",
    "可观测性": "observability",
    "Agent": "agent",
    "SRE": "sre",
    "Kubernetes": "kubernetes",
    "GPU": "gpu",
    "容量规划": "capacity-planning",
    "向量数据库": "vector-database",
    "性能优化": "performance",
}

SAMPLE_ARTICLES = [
    {
        "title": "构建可观测的 LLM 服务：从 Token 到 Trace",
        "slug": "observable-llm-services",
        "excerpt": "只监控接口成功率远远不够。把模型调用、Token 成本、检索链路和用户反馈放进同一条 Trace，才能真正解释一次回答为什么慢、贵或不可靠。",
        "cover": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=85",
        "category": "AI运维",
        "tags": ["LLMOps", "OpenTelemetry", "可观测性"],
        "featured": True,
        "content": """# 构建可观测的 LLM 服务：从 Token 到 Trace

传统 API 通常围绕延迟、错误率和吞吐量建立监控。但在 LLM 应用里，一个返回 200 的请求仍可能是一次失败：答案偏离上下文、检索结果为空，或者为了简单问题消耗了数万 Token。

## 先定义一次请求的完整链路

我们把网关、检索、重排、模型推理和输出校验放进同一个 Trace，并在 Span 上记录模型版本、提示词版本、Token 数量和缓存命中状态。敏感提示词不直接进入日志，只保存脱敏摘要与稳定哈希。

```text
request -> retrieval -> rerank -> inference -> guardrail -> response
```

## 三组真正有用的指标

第一组是用户体验：首 Token 延迟、完整响应时间和中断率。第二组是质量代理指标：无引用回答率、检索空结果率和校验拒绝率。第三组是单位经济性：每次成功回答的 Token 与 GPU 时间。

> 可观测性的目标不是收集更多数据，而是让一次异常回答能够被解释。

当告警能直接跳转到完整 Trace，值班工程师不再需要在五套系统之间拼接请求。平均定位时间因此从四十分钟降到十分钟以内。""",
    },
    {
        "title": "让 AI 接管一线告警，但不替你背锅",
        "slug": "ai-assisted-incident-triage",
        "excerpt": "告警 Agent 最适合做证据收集、上下文关联和处置建议，而不是未经确认地执行高风险变更。边界设计比模型能力更重要。",
        "cover": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1600&q=85",
        "category": "智能自动化",
        "tags": ["Agent", "SRE", "可观测性"],
        "featured": False,
        "content": """# 让 AI 接管一线告警，但不替你背锅

我们曾经把每条告警都推给值班群，结果工程师每天要处理大量重复信息。新的告警 Agent 不直接做决策，它先完成一线响应中最机械的部分。

## Agent 的三层权限

只读层可以查询指标、日志、变更记录和历史事件；建议层可以生成排查步骤与 Runbook 链接；执行层只开放白名单动作，并且必须经过人工确认。

每条结论都要附证据来源和时间范围。找不到证据时，系统必须明确回答“不确定”，而不是补全一个听起来合理的原因。

## 衡量自动化是否有效

我们关注的不是 Agent 回复了多少告警，而是告警去重率、有效证据覆盖率、建议采纳率和平均确认时间。上线后，夜间需要人工打开的告警减少了 43%，但所有生产变更仍保留人在回路中。""",
    },
    {
        "title": "Kubernetes 上的 GPU 推理服务容量规划",
        "slug": "kubernetes-gpu-capacity-planning",
        "excerpt": "GPU 利用率不是容量规划的唯一答案。批处理窗口、显存水位、队列长度和首 Token 延迟共同决定推理集群是否真的健康。",
        "cover": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=85",
        "category": "云原生",
        "tags": ["Kubernetes", "GPU", "容量规划"],
        "featured": False,
        "content": """# Kubernetes 上的 GPU 推理服务容量规划

推理服务最常见的误区，是看到 GPU 利用率没有跑满就继续压缩副本。实际情况往往相反：显存已经接近上限，动态批处理队列也开始累积，而平均利用率仍然不高。

## 从请求形态建立基线

先按输入长度和输出长度对请求分桶，再测量不同批大小下的首 Token 延迟与吞吐量。容量模型至少需要包含峰值并发、P95 上下文长度、KV Cache 占用和模型加载时间。

## 扩缩容需要看队列

GPU 指标适合判断资源状态，队列等待时间更接近用户体验。我们用队列 P95 等待时间触发扩容，同时设置显存水位作为保护条件，并保留一组已经加载模型的热备副本。

最终目标不是让 GPU 看起来更忙，而是在成本边界内稳定兑现延迟 SLO。""",
    },
    {
        "title": "一次向量数据库延迟抖动复盘",
        "slug": "vector-database-latency-postmortem",
        "excerpt": "一次看似随机的检索延迟，最终指向批量导入、索引合并与缓存淘汰的叠加效应。复盘的价值在于把偶发经验固化为系统保护。",
        "cover": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1600&q=85",
        "category": "故障复盘",
        "tags": ["向量数据库", "性能优化", "SRE"],
        "featured": False,
        "content": """# 一次向量数据库延迟抖动复盘

周二下午，RAG 服务的检索 P99 从 180ms 上升到 2.4s，但 CPU、内存和网络都没有明显异常。问题每隔二十分钟出现一次，持续约三分钟后自行恢复。

## 时间线与证据

我们把慢查询 Trace 与平台事件对齐，发现抖动总是发生在批量数据导入之后。后台索引合并占用大量磁盘 I/O，同时触发缓存淘汰，使在线查询不断回源读取。

临时处置是暂停导入任务并限制合并并发。长期修复则把写入窗口与业务高峰隔离，为后台任务设置独立 I/O 配额，并新增索引合并队列长度与缓存命中率告警。

## 真正的根因

根因不只是一个缺少限制的任务，而是容量测试只覆盖了稳定读流量，没有覆盖“持续写入加索引维护”的生产负载。新的压测场景已经成为每次版本升级的准入项。""",
    },
]


def _get_category(db: Session, cache: dict[str, Category], name: str) -> Category:
    if name not in cache:
        cache[name] = db.scalar(select(Category).where(Category.name == name)) or Category(
            name=name, slug=CATEGORY_SLUGS[name]
        )
        db.add(cache[name])
    return cache[name]


def _get_tag(db: Session, cache: dict[str, Tag], name: str) -> Tag:
    if name not in cache:
        cache[name] = db.scalar(select(Tag).where(Tag.name == name)) or Tag(name=name, slug=TAG_SLUGS[name])
        db.add(cache[name])
    return cache[name]


def seed_database(db: Session) -> None:
    existing_articles = db.scalars(select(Article).order_by(Article.id)).all()
    legacy_articles = [article for article in existing_articles if article.slug in LEGACY_SLUGS]

    # Preserve databases that already contain user-authored content and no legacy demo data.
    if existing_articles and not legacy_articles:
        return

    category_cache: dict[str, Category] = {}
    tag_cache: dict[str, Tag] = {}
    for index, item in enumerate(SAMPLE_ARTICLES):
        article = legacy_articles[index] if index < len(legacy_articles) else Article()
        article.title = item["title"]
        article.slug = item["slug"]
        article.excerpt = item["excerpt"]
        article.content = item["content"]
        article.cover = item["cover"]
        article.featured = item["featured"]
        article.published = True
        article.category = _get_category(db, category_cache, item["category"])
        article.tags = [_get_tag(db, tag_cache, name) for name in item["tags"]]
        db.add(article)

    db.flush()
    for category in db.scalars(select(Category)).all():
        if not category.articles:
            db.delete(category)
    for tag in db.scalars(select(Tag)).all():
        if not tag.articles:
            db.delete(tag)
    db.commit()
