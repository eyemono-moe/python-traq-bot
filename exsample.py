from traq_bot import TraqBot
import os


bot = TraqBot(os.environ.get("BOT_VERIFICATION_TOKEN"))

@bot.message_created
def print_message_data(data: dict):
    print(data)


if __name__ == '__main__':
    bot.run(8080)
