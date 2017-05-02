import logging
import datetime
from django import template

logger = logging.getLogger("focus")
register = template.Library()


def strftime(var):
    return datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d')


def short_strftime(var):
    this_year = str(datetime.datetime.now().year)
    if datetime.datetime.fromtimestamp(var).strftime('%Y') == this_year:
        return datetime.datetime.fromtimestamp(var).strftime('%m-%d')
    else:
        return datetime.datetime.fromtimestamp(var).strftime('%Y-%m-%d')


def format_title(var):
    if len(var) >= 40:
        return var[0:37] + "..."
    else:
        return var

def format_desc(var):
    if len(var) >= 150:
        return var[0:150] + "..."
    else:
        return var

register.filter('strftime', strftime)
register.filter('short_strftime', short_strftime)
register.filter('format_title', format_title)
register.filter('format_desc', format_desc)