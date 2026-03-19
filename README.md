# Telegram MarkdownV2 Bot (Python)

轻量部署的 Telegram 机器人，用于把标准 Markdown 转成 Telegram MarkdownV2，并将 LaTeX 公式转为 Unicode 近似。

## 功能

- 将标准 Markdown 转成 Telegram MarkdownV2
- 自动将 LaTeX `\(...\)` / `\[...\]` 转成 Unicode 近似
- 自动拆分超长消息（按 Telegram UTF-16 长度限制）

## 依赖

- Python 3.10+
- telegramify-markdown
- python-telegram-bot

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 配置

在环境变量中提供 Telegram Bot Token：

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
```

也可以创建 `.env` 文件：

```env
TELEGRAM_BOT_TOKEN=YOUR_TOKEN
```

## 运行

```bash
PYTHONPATH=src python -m md2tg_bot.bot
```

## 使用

发送任意 Markdown 文本给机器人即可。
例如：

```
**Bold** and `code`
\(\alpha + 1\)
```

## 参考

- https://github.com/sudoskys/telegramify-markdown
- https://github.com/yym68686/md2tgmd
