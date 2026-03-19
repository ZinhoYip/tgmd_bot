from http.server import BaseHTTPRequestHandler
import json
import asyncio
from md2tg_bot.bot import build_app
from telegram import Update

# 预初始化机器人实例
app = build_app()

async def process_update(payload):
    """异步处理 Telegram 更新"""
    async with app:
        update = Update.de_json(payload, app.bot)
        await app.process_update(update)

class handler(BaseHTTPRequestHandler):
    """Vercel 原生 Python 处理器类"""

    def do_POST(self):
        """处理 Telegram Webhook"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))

            # 为当前请求创建并运行事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(process_update(payload))
            finally:
                loop.close()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        except Exception as e:
            print(f"Error processing POST: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_GET(self):
        """基础响应，证明服务在线"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Telegram Bot is running via Vercel Webhook!".encode())
