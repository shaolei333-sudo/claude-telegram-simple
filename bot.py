import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from anthropic import Anthropic

# 启用日志，方便我们在 Railway 看到报错
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 从环境变量读取密钥
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

# 初始化 Claude 客户端
client = Anthropic(api_key=ANTHROPIC_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # 打印一下收到消息，证明机器人活着
    print(f"收到雷少的消息: {user_text}")
    
    try:
        # 调用 Claude API
        message = client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_text}
            ]
        )
        
        # 把 Claude 的回答发回给 Telegram
        await update.message.reply_text(message.content[0].text)
        
    except Exception as e:
        print(f"出错了: {e}")
        await update.message.reply_text("哎呀，脑子卡住了，请稍后再试。")

if __name__ == '__main__':
    # 启动 Telegram 机器人
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(echo_handler)
    
    print("机器人已启动，雷少请出车！")
    application.run_polling()
