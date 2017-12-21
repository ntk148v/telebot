"""Remind everyone in team to send report
/remind thing_to_remind - Run at xx:xx everyday!
"""
import datetime


def do_remind(bot, job, reminder):
    bot.send_message(job.context, text=reminder)
    return


def handle(bot, update, args, job_queue, chat_data):
    """Remind something at xx:xx everyday!"""
    chat_id = update.message.chat_id

    try:
        reminder = args[0]

        # Add job to queue, run daily
        job = job_queue.run_daily(do_remind, reminder,
                                  time=datetime.time('14:32'),
                                  context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except(IndexError, ValueError):
        update.message.reply_text('Usage: /remind thing_to_remind')
