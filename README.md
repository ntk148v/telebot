# Telebot

A [Telegram](https://telegram.org/) Bot written in Python (Work-In-Progress)

## Installation

1. Clone this repo and install all requirements:

```
$ git clone https://github.com/ntk148v/telebot
$ cd telebot
$ sudo -H pip3 install -r requirements.txt
```

2. [Create a bot user](https://core.telegram.org/bots#3-how-do-i-create-a-bot) if you don't have one yet, and get the API Token

3. Export this TOKEN & some logging configs:

```
$ cp envs.template envs
# Change these configs
$ source envs
```

4. Run!

```
$ makefile run
```

5.  Invite Telebot (with your Bot name) into any groups/channels want it in or
    simply just send it a direct message.

## Troubles?

- Currently, unable to write log to file (as expected).
- Job queue doesn't work correctly.
