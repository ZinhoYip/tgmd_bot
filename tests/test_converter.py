from md2tg_bot.converter import markdown_to_markdownv2_chunks


def test_basic_conversion() -> None:
    result = markdown_to_markdownv2_chunks("**Bold** and `code`", max_utf16_len=4096)
    assert result.chunks
    assert "*Bold*" in result.chunks[0]


def test_latex_unicode_approximation() -> None:
    result = markdown_to_markdownv2_chunks("\\(\\alpha + 1\\)")
    combined = "".join(result.chunks)
    assert "α" in combined
