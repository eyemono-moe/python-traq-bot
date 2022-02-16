from traq_bot import TraqBot
import os

bot = TraqBot(os.environ.get("BOT_VERIFICATION_TOKEN"))


@bot.message_created
def say_hello(data):
    channel_id = data["message"]["channel_id"]
    
    pass


if __name__ == '__main__':
    bot.run(8080)
