import os
from telegram.ext import Updater, MessageHandler, Filters
from anthropic import Anthropic

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def reply(update, context):
    user_text = update.message.text

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.content[0].text

    update.message.reply_text(answer)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(
    MessageHandler(Filters.text & ~Filters.command, reply)
)

updater.start_polling()
updater.idle()
