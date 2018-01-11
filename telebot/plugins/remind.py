"""Remind everyone in team
Usage:
/remind set hour:minute reminder- Remind something at hour:minute!
/remind unset - Unset reminder.
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
        action = args.pop(0)

        if action == 'set':
            hour, minute = map(int, args.pop(0).split(':'))
            reminder = ' '.join(args)
            context['chat_id'] = chat_id
            context['reminder'] = reminder

            # Add job to queue, run once
            job = job_queue.run_once(do_remind,
                                    when=datetime.time(hour=hour, minute=minute),
                                    context=context)
            chat_data['job'] = job

            update.message.reply_text('Timer successfully set!')
            return
        elif action == 'unset':
            if 'job' not in chat_data:
                update.message.reply_text('You have no active reminder!')
                return
            job = chat_data['job']
            job.schedule_removal()
            del chat_data['job']

            update.message.reply_text('Timer successfully unset!')
            return
        else:
            raise ValueError
    except(IndexError, ValueError):
        update.message.reply_text(
            'Usage: /remind set hour:minute reminder or /remind unset')
