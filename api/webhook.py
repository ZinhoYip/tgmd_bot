import os
import json
import asyncio
from telegram import Update
from md2tg_bot.bot import build_app

# 初始化 app
# 注意：在 Vercel 中，我们需要确保 build_app 能够正确读取环境变量
app = build_app()

async def process_update(update_json):
    """异步处理 Telegram 更新"""
    async with app:
        update = Update.de_json(update_json, app.bot)
        await app.process_update(update)

def handler(request):
    """Vercel Python 函数入口"""
    if request.method == "POST":
        try:
            # 解析请求体
            payload = json.loads(request.body.decode("utf-8"))
            
            # 运行异步任务
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(process_update(payload))
            finally:
                loop.close()
                
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'ok'})
            }
        except Exception as e:
            print(f"Error processing update: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    return {
        'statusCode': 200,
        'body': 'Bot is running!'
    }
