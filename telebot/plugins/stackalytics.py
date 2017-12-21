from datetime import datetime
import json
from urllib import request


def query(user_id=None, company=None, release='queens'):
    """Query to http://stackalytics.com/"""
    url = 'http://stackalytics.com/api/1.0/contribution?release=queens' . \
            format(release)

    if company:
        url += '&company={}' . format(company)
    if user_id:
        url += '&user_id={}' . format(user_id)

    stats = urllib.request.urlopen(url)
    try:
        stats = json.loads(stats.read())
    except ValueError as e:
        LOG.error('Error when execute query: {}' . format(e))
        return None
    patches = stats['contribution']['patch_set_count']
    commits = stats['contribution']['commit_set_count']
    reviews = \
            stats['contribution']['marks']['1'] + \
            stats['contribution']['marks']['-1'] + \
            stats['contribution']['marks']['2'] + \
            stats['contribution']['marks']['-2']
    return (patches, commits, reviews)

def handle(bot, update):
    pass
