#!/Users/mac/.claude/skills/ppt-clouder/.venv/bin/python3.10
"""
智谱AI 联网搜索脚本 - Frontend Slides 集成版
用于在生成演示文稿时搜索文案素材

用法: python web_search.py "搜索内容" [--engine search_pro] [--recency oneDay] [--count 10]

环境: /Users/mac/.claude/skills/ppt-clouder/.venv (Python 3.10)
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 加载 .env 文件
load_dotenv()


def get_api_key():
    """从环境变量获取 API Key"""
    api_key = os.environ.get("ZHIPU_API_KEY")
    if not api_key:
        raise ValueError(
            "请设置环境变量 ZHIPU_API_KEY\n"
            "获取方式: https://open.bigmodel.cn/usercenter/apikeys"
        )
    return api_key


def extract_sources_from_response(response):
    """
    从响应中提取资料来源信息

    返回:
        list: 包含来源信息的列表，每个元素为 (title, url) 元组
    """
    import re
    from urllib.parse import urlparse, unquote

    sources = []
    seen_urls = set()

    # 尝试从 tool_calls 中提取搜索结果
    if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            if hasattr(tool_call, 'function') and tool_call.function:
                import json
                try:
                    args = json.loads(tool_call.function.arguments)
                    if 'search_result' in args:
                        search_results = args['search_result']
                        # 解析搜索结果中的链接
                        if isinstance(search_results, list):
                            for result in search_results:
                                if isinstance(result, dict):
                                    title = result.get('title', result.get('name', '未知来源'))
                                    url = result.get('url', result.get('link', ''))
                                    if url and url not in seen_urls:
                                        seen_urls.add(url)
                                        sources.append((title, url))
                except (json.JSONDecodeError, TypeError):
                    pass

    # 从响应内容中提取URL链接
    content = response.choices[0].message.content or ""

    # 匹配Markdown格式的链接: [标题](URL)
    md_link_pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)'
    md_matches = re.findall(md_link_pattern, content)
    for title, url in md_matches:
        if url not in seen_urls:
            seen_urls.add(url)
            sources.append((title, url))

    # 匹配纯URL链接
    url_pattern = r'https?://[a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z0-9][-a-zA-Z0-9]*)+(?::\d+)?(?:/[^\s\]\[\)\(\{\}"\'<>]*)?'
    urls = re.findall(url_pattern, content)

    for url in urls:
        url = url.rstrip('.,;:!?\'"')

        if url not in seen_urls:
            seen_urls.add(url)
            try:
                parsed = urlparse(url)
                domain = parsed.netloc
                path = parsed.path.strip('/')
                if path and path != '':
                    path_parts = [unquote(p) for p in path.split('/') if p]
                    if path_parts:
                        title = path_parts[-1].replace('-', ' ').replace('_', ' ').title()
                    else:
                        title = domain
                else:
                    title = domain
                sources.append((title, url))
            except Exception:
                sources.append((url[:50], url))

    return sources


def web_search(
    query, engine="search_pro", recency="noLimit", count=10, content_size="high"
):
    """
    执行联网搜索

    参数:
        query: 搜索内容
        engine: 搜索引擎 (search_std/search_pro/search_pro_sogou/search_pro_quark)
        recency: 时间范围 (oneDay/oneWeek/oneMonth/oneYear/noLimit)
        count: 结果数量 (1-50)
        content_size: 内容详细度 (low/medium/high)

    返回:
        dict: 包含搜索结果和来源信息的字典
    """
    client = ZhipuAI(api_key=get_api_key())

    tools = [
        {
            "type": "web_search",
            "web_search": {
                "enable": "True",
                "search_engine": engine,
                "search_result": "True",
                "search_prompt": "你是一位专业的内容研究员。请根据以下网络搜索结果{search_result}，提供全面、准确且带有来源引用的信息。提取关键要点，按重要性排序，并在回答中明确标注每个信息的来源链接。",
                "count": str(count),
                "content_size": content_size,
                "search_recency_filter": recency,
            },
        }
    ]

    messages = [{"role": "user", "content": query}]

    response = client.chat.completions.create(
        model="glm-4-air", messages=messages, tools=tools, tool_choice="auto"
    )

    content = response.choices[0].message.content
    sources = extract_sources_from_response(response)

    return {
        "content": content,
        "sources": sources,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens if hasattr(response, "usage") else 0,
            "completion_tokens": response.usage.completion_tokens if hasattr(response, "usage") else 0,
            "total_tokens": response.usage.total_tokens if hasattr(response, "usage") else 0,
        }
    }


def search_for_slide_content(topic, slide_type="content", keywords=None):
    """
    专为演示文稿幻灯片搜索内容

    参数:
        topic: 幻灯片主题
        slide_type: 幻灯片类型 (title/content/feature/data/quote)
        keywords: 额外关键词列表

    返回:
        dict: 整理后的幻灯片内容建议
    """
    # 根据幻灯片类型构建搜索查询
    query_parts = [topic]

    if slide_type == "title":
        query_parts.append("核心概念 定义 简介")
    elif slide_type == "content":
        query_parts.append("关键要点 主要优势 特点")
    elif slide_type == "feature":
        query_parts.append("功能特性 产品亮点")
    elif slide_type == "data":
        query_parts.append("数据统计 行业报告 趋势")
    elif slide_type == "quote":
        query_parts.append("名人名言 行业观点")

    if keywords:
        query_parts.extend(keywords)

    query = " ".join(query_parts)

    # 执行搜索
    result = web_search(query, engine="search_pro", content_size="high", count=5)

    return result


def main():
    parser = argparse.ArgumentParser(description="智谱AI联网搜索工具 - Frontend Slides 版")
    parser.add_argument("query", nargs="?", help="搜索内容")
    parser.add_argument(
        "--engine",
        "-e",
        default="search_pro",
        choices=["search_std", "search_pro", "search_pro_sogou", "search_pro_quark"],
        help="搜索引擎 (默认: search_pro)",
    )
    parser.add_argument(
        "--recency",
        "-r",
        default="noLimit",
        choices=["oneDay", "oneWeek", "oneMonth", "oneYear", "noLimit"],
        help="时间范围 (默认: noLimit)",
    )
    parser.add_argument(
        "--count", "-c", type=int, default=10, help="结果数量 1-50 (默认: 10)"
    )
    parser.add_argument(
        "--content-size",
        "-s",
        default="high",
        choices=["low", "medium", "high"],
        help="内容详细度 (默认: high)",
    )
    parser.add_argument(
        "--slide-type",
        "-t",
        default="content",
        choices=["title", "content", "feature", "data", "quote"],
        help="幻灯片类型 (用于优化搜索)"
    )

    args = parser.parse_args()

    if args.query:
        result = search_for_slide_content(
            args.query,
            slide_type=args.slide_type
        )
        print("\n" + "=" * 60)
        print("✅ 搜索结果:")
        print("=" * 60)
        print(result["content"])

        if result["sources"]:
            print("\n" + "-" * 60)
            print("📚 资料来源:")
            print("-" * 60)
            seen_urls = set()
            for i, (title, url) in enumerate(result["sources"], 1):
                if url not in seen_urls:
                    seen_urls.add(url)
                    display_title = title[:50] + "..." if len(title) > 50 else title
                    print(f"  {i}. {display_title}")
                    print(f"     🔗 {url}")

        print("\n" + "=" * 60)
    else:
        print("用法: python web_search.py '搜索内容'")
        print("或使用: python web_search.py --help 查看完整选项")


if __name__ == "__main__":
    main()
