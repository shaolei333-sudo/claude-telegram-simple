import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import anthropic

# 环境变量
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=CLAUDE_KEY)

async def start(update: Update, context):
    await update.message.reply_text('你好！Claude 3.7 已经就绪，请提问。')

async def chat(update: Update, context):
    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1024,
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(response.content[0].text)
    except Exception as e:
        await update.message.reply_text(f"出错啦: {str(e)}")

if __name__ == '__main__':
    # 使用最新的 Application 架构，解决你日志里的 AttributeError
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    application.run_polling()
