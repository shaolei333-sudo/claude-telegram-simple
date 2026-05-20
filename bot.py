import os
import asyncio
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 獲取環境變量
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=CLAUDE_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('你好！Claude 3.7 機器人已在 Railway 雲端成功啟動！')

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1024,
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(response.content[0].text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    
    print("Bot is running...")
    application.run_polling()
