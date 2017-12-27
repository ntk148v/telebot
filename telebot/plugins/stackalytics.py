"""Get report from Stackalytics
/stackalytics - Get report from Stackalytics

- Just type /stackalytics for query stats
- Type /stackalytics report to get report in xlsx format.
- Firstly, need to chat direct with bot and upload config file
with json format:

For e.x:
    {
        "company": "Fujitsu",
        "members": [
            "kiennt26",
            "daidv"
        ],
        "review_target": 6969,
        "commit_target": 696
    }
"""
from datetime import date
from datetime import timedelta
import json
import logging
import urllib.error
import urllib.request

from telegram import ParseMode
import xlsxwriter

from telebot import emojies
from telebot import utils

LOG = logging.getLogger(__name__)


def query(bot, chat_id, user_id=None, company=None):
    """Query to http://stackalytics.com/"""
    url = 'http://stackalytics.com/api/1.0/contribution?'

    if company:
        url += 'company={}' . format(company)
    if user_id:
        url += '&user_id={}' . format(user_id)

    LOG.debug('Query url: {}' . format(url))

    try:
        stats = urllib.request.urlopen(url)
        stats = json.loads(stats.read().decode())
    except ValueError as e:
        msg = 'Error with JSON format: {}' . format(e)
        utils.handle_error(LOG, bot, chat_id, msg)
        return None
    except urllib.error.HTTPError as e:
        msg = 'Error when query member {}\'s stats: {}' . format(user_id, e)
        utils.handle_error(LOG, bot, chat_id, msg)
        return None
    patches = stats['contribution']['patch_set_count']
    commits = stats['contribution']['commit_count']
    reviews = \
        stats['contribution']['marks']['1'] + \
        stats['contribution']['marks']['-1'] + \
        stats['contribution']['marks']['2'] + \
        stats['contribution']['marks']['-2']
    return (patches, commits, reviews)

# Fixme(kiennt): A bunch of hardcode! Ugly, ugly...!


def get_report(workbook, worksheet, member, stats, targets,
               num_members, index, summary=None):
    """Create a new Excel file and add a worksheet"""
    # Extract input
    review_target, commit_target = targets
    reviews, commits = stats

    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    a = date(year, month, day).isocalendar()[1]
    a1 = date(2017, 12, 31).isocalendar()[1]
    b = date(2018, 3, 2).isocalendar()[1]

    if a > b:
        week = (a1 - a) + b
    else:
        week = b - a

    def _range_date_of_week(year, week):
        d = date(year, 1, 1)
        if(d.weekday() > 3):
            d = d + timedelta(7 - d.weekday())
        else:
            d = d - timedelta(d.weekday())
        dlt = timedelta(days=(week - 1) * 7)
        start = str(d + dlt)
        end = str(d + dlt + timedelta(days=4))
        return start, end

    # Widen the first column to make the text clearer.
    worksheet.set_column('E:E', 30)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 15)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': False})
    bold.set_border()
    bold.set_font('Times New Roman')
    bold.set_font_size(13)
    bold_color = workbook.add_format(
        {'bold': False, 'font_color': 'black'})
    bold_color.set_font('Times New Roman')
    bold_color.set_font_size(13)
    bold_color.set_border()
    bold_color.set_pattern(1)
    bold_color.set_bg_color('yellow')
    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font': 'Times New Roman',
        'font_size': 13})

    row = 13 + index * 4
    # Write some simple text.
    if summary:
        worksheet.merge_range('D' + str(row - 5) + ':J' + str(row - 5),
                              'Week (From ' + _range_date_of_week(year, a)[0] +
                              ' to ' + _range_date_of_week(year, a)[1] + ' )', merge_format)
        worksheet.merge_range('D' + str(row - 4) +
                              ':D' + str(row - 2), 'Team', merge_format)
        worksheet.write('E' + str(row - 4), 'R-' + str(week), bold)
        worksheet.write('E' + str(row - 3),
                        'Reviews (Until 2018/02/23)', bold)
        worksheet.write('E' + str(row - 2),
                        'Commits (Until 2018/01/26)', bold)
        worksheet.write('F' + str(row - 4), 'Target', bold)
        worksheet.write('G' + str(row - 4), 'Actual', bold)
        worksheet.write('H' + str(row - 4), 'Target remain', bold)
        worksheet.write('I' + str(row - 4), 'Actual remain', bold)
        worksheet.write('J' + str(row - 4), 'Status', bold)
        worksheet.write('F' + str(row - 3), review_target, bold)
        worksheet.write('F' + str(row - 2), commit_target, bold)
        worksheet.write('G' + str(row - 3), reviews, bold_color)
        worksheet.write('G' + str(row - 2), commits, bold_color)
        m1 = review_target - (review_target / 25) * \
            (26 - week)  # 25 is total week of the cycle
        n1 = commit_target - (commit_target / 21) * \
            (26 - week)  # 21 is the week of RC1
        m2 = review_target - reviews
        n2 = commit_target - commits
        worksheet.write('H' + str(row - 3), round(m1), bold)
        worksheet.write('H' + str(row - 2), round(n1), bold)
        worksheet.write('I' + str(row - 3), m2, bold)
        worksheet.write('I' + str(row - 2), n2, bold)
        worksheet.write('J' + str(row - 3), round(m1 - m2), bold_color)
        worksheet.write('J' + str(row - 2), round(n1 - n2), bold_color)
    else:
        worksheet.merge_range('D' + str(row) + ':D' +
                              str(row + 2), member, merge_format)
        worksheet.write('E' + str(row), '', bold)
        worksheet.write('E' + str(row + 1), 'Reviews', bold)
        worksheet.write('E' + str(row + 2), 'Commits', bold)
        worksheet.write('F' + str(row), 'Target', bold)
        worksheet.write('G' + str(row), 'Actual', bold)
        worksheet.write('H' + str(row), 'Target remain', bold)
        worksheet.write('I' + str(row), 'Actual remain', bold)
        worksheet.write('J' + str(row), 'Status', bold)
        q = review_target / num_members
        p = commit_target / num_members
        q1 = q - (q / 25) * (26 - week)
        p1 = p - (p / 21) * (26 - week)
        q2 = q - reviews
        p2 = p - commits
        worksheet.write('F' + str(row + 1), round(q), bold)
        worksheet.write('F' + str(row + 2), round(p), bold)
        worksheet.write('G' + str(row + 1), reviews, bold_color)
        worksheet.write('G' + str(row + 2), commits, bold_color)
        worksheet.write('H' + str(row + 1), round(q1), bold)
        worksheet.write('H' + str(row + 2), round(p1), bold)
        worksheet.write('I' + str(row + 1), round(q2), bold)
        worksheet.write('I' + str(row + 2), round(p2), bold)
        worksheet.write('J' + str(row + 1), round(q1 - q2), bold_color)
        worksheet.write('J' + str(row + 2), round(p1 - p2), bold_color)


def handle(bot, update):
    chat_id = update.message.chat_id
    try:
        config = json.load(open('/tmp/stackalyticsconfig.json'))
    except FileNotFoundError:
        msg = 'Config file doesn\' exist! Type /hep stackalytics again to \
               check usage!'
        utils.handle_error(LOG, bot, chat_id, msg)
        return
    except json.decoder.JSONDecodeError:
        msg = 'Wrong format! Type /hep stackalytics again to \
              check right format!'
        utils.handle_error(LOG, bot, chat_id, msg)
        return

    args = update.message.text.split(' ')
    report = False
    if len(args) > 2:
        update.message.reply_text('Wrong number of options! '
                                  'Please type /help stackalytics for usage.')
        return
    elif len(args) == 2 and args[1] != 'report':
        update.message.reply_text('Wrong option! '
                                  'Please type /help stackalytics for usage.')
        return
    else:
        report = True

    update.message.reply_text('Please wait for seconds! '
                              'Query members stats from Stackalytics...')

    text = '{} *Report:*\n' . format(emojies.point_right)
    template = '- Member `{}`: `{}` patches, `{}` commits, `{}` reviews.\n'

    targets = (int(config['review_target']), int(config['commit_target']))
    report_file = \
        'FVL_UC_Contribution_Summarization.xlsx'
    workbook = xlsxwriter.Workbook(report_file)
    num_members = len(config['members'])
    team_stats_patches = 0
    team_stats_commits = 0
    team_stats_reviews = 0
    worksheet = workbook.add_worksheet()

    for index, member in enumerate(config['members']):
        results = query(bot, chat_id,
                        user_id=member,
                        company=config['company'])
        if not results:
            continue

        patches, commits, reviews = results
        team_stats_commits += commits
        team_stats_patches += patches
        team_stats_reviews += reviews

        # Bad performance, condition in loop (Fixme)
        if report:
            get_report(workbook, worksheet, member, (reviews, commits),
                       targets, num_members, index)
            if index == num_members:
                get_report(workbook, worksheet, 'Team',
                           (team_stats_reviews, team_stats_commits),
                           num_members, targets, 0, summary=True)

        text += template.format(member, patches, commits, reviews)

    workbook.close()

    bot.send_message(chat_id=chat_id,
                     text=text,
                     parse_mode=ParseMode.MARKDOWN)
    if report:
        bot.send_document(chat_id=chat_id,
                          document=open(report_file, 'rb'),
                          caption='Report')
    return
