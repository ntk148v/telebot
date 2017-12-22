"""Remind everyone in team to send report
/remind hour:minute reminder - Remind at hour:minute everyday!
"""
import datetime

from telegram import ParseMode

from telebot import emojies


def do_remind(bot, job):
    reminder = '{} `{}` {}' . format(
        emojies.bell, job.context['reminder'],
        emojies.bell)

    chat_id = job.context['chat_id']
    bot.send_message(chat_id=chat_id, text=reminder,
                     parse_mode=ParseMode.MARKDOWN)
    return


def handle(bot, update, args, job_queue, chat_data):
    """Remind something at xx:xx everyday!"""
    chat_id = update.message.chat_id
    context = {}

    try:
        hour, minute = map(int, args.pop(0).split(':'))
        reminder = ' '.join(args)
        context['chat_id'] = chat_id
        context['reminder'] = reminder

        # Add job to queue, run daily
        job = job_queue.run_daily(do_remind,
                                  time=datetime.time(hour=hour, minute=minute),
                                  context=context)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except(IndexError, ValueError):
        update.message.reply_text('Usage: /remind hour:minute reminder')
