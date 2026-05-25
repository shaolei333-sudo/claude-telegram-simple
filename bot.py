import os
import anthropic
import base64
import aiohttp
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
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_text}]
        )
        
        await update.message.reply_text(message.content[0].text)
        
    except Exception as e:
        # 如果出錯，打印詳細信息
        print(f"詳細錯誤: {e}")
        await update.message.reply_text(f"連線成功但發生錯誤: {str(e)}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # 获取图片信息
        photo = update.message.photo[-1]  # 最高质量的图片
        file = await context.bot.get_file(photo.file_id)
        
        # 下载图片
        file_url = file.file_path
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                image_data = await resp.read()
        
        # Base64 编码
        image_base64 = base64.standard_b64encode(image_data).decode("utf-8")
        
        # 获取 caption（如果有的话）
        caption = update.message.caption or "分析这张图片"
        
        print(f"收到图片，Caption: {caption}")
        
        # 调用 Claude Vision API
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": caption
                        }
                    ],
                }
            ],
        )
        
        await update.message.reply_text(message.content[0].text)
        
    except Exception as e:
        print(f"处理图片出错: {e}")
        await update.message.reply_text(f"处理图片失败: {str(e)}")

if __name__ == '__main__':
    # 啟動機器人
    app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))  # 添加图片处理
    print("機器人已啟動，雷少請測試！")
    app.run_polling()
