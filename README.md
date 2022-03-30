# Telegram Bot Template

### Useful and multifunction bot template, which use aiogram and pyrogram libraries

![Telegram](https://img.shields.io/badge/Telegram-blue?style=flat&logo=telegram)
[![DeepSource](https://deepsource.io/gh/fast-geek/telegram-bot-template.svg/?label=resolved+issues&show_trend=true&token=xT19E0s_Ut8tM94CcpLA9exx)](https://deepsource.io/gh/fast-geek/telegram-bot-template/?ref=repository-badge)
![CodeStyle](https://img.shields.io/badge/code%20style-black-black)
![PythonVersions](https://img.shields.io/pypi/pyversions/aiogram)

## Features

* ![aiogram 3](https://img.shields.io/badge/dev--3.x-aiogram-blue) as a main library
* ![pyrogram](https://img.shields.io/badge/latest-pyrogram-orange) (Optional) for MTProto requests, such as bulk delete,
  resolve by username and list participants in a group
* ![aiogram-dialog](https://img.shields.io/badge/beta--2.x-aiogram__dialog-green) (Optional) for creating multi-step
  dialogs
* ☁️ Webhook and long polling with local Bot API server support
* 🎨 Beautiful and informative colored logs
* 🛠 Throttling and db middlewares by default
* 📝 Changing UI commands
* 👨🏻‍💻 Owner filter
* ℹ️ Demo usage of dialogs and inline queries

## Usage

* 📌 [Create](https://github.com/fast-geek/telegram-bot-template/generate) and clone repo from this template
* 🔑 Change bot settings in `config.toml`
* 📎 Install requirements from `requirements.txt`
* 🚀 Run bot via `python -m app`