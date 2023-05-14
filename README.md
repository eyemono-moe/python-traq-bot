[![Downloads](https://static.pepy.tech/badge/traq-bot)](https://pepy.tech/project/traq-bot)

# traQ BOTサーバーライブラリ

PythonでtraQ BOTサーバーを簡単に作るためのライブラリです。

`traQ->BOTサーバー`へのイベントの受け取り部分を補助します。`BOTサーバー->traQ`へのリクエストを行うためのAPIクライアントは含んでいません。[motoki317/traq-py](https://github.com/motoki317/traq-py)等を利用してください。

## インストール

```bash
pip install traq-bot
```

## サンプル

```py
from traq_bot import TraqBot
import os


bot = TraqBot(os.environ.get("BOT_VERIFICATION_TOKEN"))

@bot.message_created
def print_message_data(data: dict):
    print(data)


if __name__ == '__main__':
    bot.run(8080)
```
