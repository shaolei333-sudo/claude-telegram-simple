import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 初始化客戶端（手動寫死官方地址，防止 404）
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    base_url="https://api.anthropic.com"
)

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        print(f"收到消息: {user_text}")

        # 使用最新版的 API 參數格式
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_text}]
        )
        
        await update.message.reply_text(message.content[0].text)
        
    except Exception as e:
        # 如果出錯，打印詳細信息
        print(f"詳細錯誤: {e}")
        await update.message.reply_text(f"連線成功但發生錯誤: {str(e)}")

if __name__ == '__main__':
    # 啟動機器人
    app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond))
    print("機器人已啟動，雷少請測試！")
    app.run_polling()
