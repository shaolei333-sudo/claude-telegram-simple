import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)
from anthropic import Anthropic

# =========================
# 日志配置
# =========================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# =========================
# 环境变量
# =========================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
print("TOKEN:", TELEGRAM_TOKEN)
print("CLAUDE:", ANTHROPIC_API_KEY)
# =========================
# Claude 客户端
# =========================
client = Anthropic(
    api_key=ANTHROPIC_API_KEY
)

# =========================
# 处理消息
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 获取用户消息
    user_text = update.message.text or ""
    print(f"收到消息: {user_text}")

    try:

        # 调用 Claude API
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        # Claude 回复
        reply = message.content[0].text

        # 防止 Telegram 超长报错
        reply = reply[:4000]

        # 回复 Telegram
        await update.message.reply_text(reply)

    except Exception as e:

        print(f"Claude Error: {e}")

        await update.message.reply_text(
            f"完整错误: {str(e)}"
        )

# =========================
# 主程序
# =========================
def main():
    # 创建 Telegram Bot
    application = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    # 添加消息监听
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("机器人已启动，雷少请出车！")

    # 开始运行
    application.run_polling()

if __name__ == '__main__':
    main()
