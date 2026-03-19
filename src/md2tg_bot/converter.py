from __future__ import annotations

import re
from dataclasses import dataclass

import telegramify_markdown


@dataclass(frozen=True)
class ConvertResult:
    """转换结果容器"""

    chunks: list[str]


def markdown_to_markdownv2_chunks(
    markdown: str, max_utf16_len: int = 4096
) -> ConvertResult:
    """
    将 Markdown 转换为 Telegram MarkdownV2 格式的块。
    采用了 tg_event.py 中的成熟方案，修复了数学公式和标题转换问题。

    :param markdown: 原始 Markdown 文本
    :param max_utf16_len: 最大长度限制
    :return: ConvertResult 实例
    """
    try:
        # 使用成熟方案中的转换逻辑
        # normalize_whitespace=False 保留原始空白字符，避免破坏 Markdown 格式
        converted_text = telegramify_markdown.markdownify(
            markdown,
            normalize_whitespace=False,
        )
    except Exception:
        # 如果转换失败，降级使用原始文本
        converted_text = markdown

    # 使用基于正则的分割逻辑
    chunks = _split_message(converted_text, max_utf16_len)

    if not chunks:
        chunks = [""]

    return ConvertResult(chunks=chunks)


def _split_message(text: str, max_length: int) -> list[str]:
    """
    参考成熟方案的消息切分逻辑。
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    # 消息分割优先级
    split_patterns = [
        re.compile(r"\n\n"),
        re.compile(r"\n"),
        re.compile(r"[.!?。！？]"),
        re.compile(r"\s"),
    ]

    remaining_text = text
    while remaining_text:
        if len(remaining_text) <= max_length:
            chunks.append(remaining_text)
            break

        split_point = max_length
        segment = remaining_text[:max_length]

        # 尝试按照优先级寻找最近的分割点
        for pattern in split_patterns:
            matches = list(pattern.finditer(segment))
            if matches:
                last_match = matches[-1]
                split_point = last_match.end()
                break

        chunks.append(remaining_text[:split_point])
        remaining_text = remaining_text[split_point:].lstrip()

    return chunks
