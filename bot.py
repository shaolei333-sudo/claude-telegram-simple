mport os
import asyncio
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 从 Railway 的 Variables 中读取配置
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")

# 初始化 Claude 客户端
client = anthropic.Anthropic(api_key=CLAUDE_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('你好！雷少的机器人已成功启动！请直接发送问题，我来为你解答。')

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 检查 Key 是否存在
    if not CLAUDE_KEY:
        await update.message.reply_text("错误：Railway 后台没有设置 ANTHROPIC_API_KEY 变量。")
        return
    
    try:
        # 使用最稳定的 3.5 Sonnet 模型，避免 404 报错
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(response.content[0].text)
    except Exception as e:
        # 如果报错，把具体原因发回 Telegram 方便排查
        error_msg = str(e)
        if "401" in error_msg:
            await update.message.reply_text("出错了：401 身份验证失败。请检查 Railway 里的 API Key 是否正确，或是否有空格。")
        elif "404" in error_msg:
            await update.message.reply_text("出错了：404 找不到模型。请确认你的 Anthropic 账号是否有权使用该模型。")
        else:
            await update.message.reply_text(f"Claude 响应出错: {error_msg}")

if __name__ == '__main__':
    # 检查 Token 是否存在
    if not TOKEN:
        print("错误：找不到 TELEGRAM_BOT_TOKEN 变量！")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
        
        print("机器人正在运行中...")
        application.run_polling()
