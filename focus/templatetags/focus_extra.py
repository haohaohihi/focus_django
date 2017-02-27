import datetime
from django import template

register = template.Library()


def strftime(var):
	return datetime.datetime.fromtimestamp(var).strftime('%Y/%m/%d')

register.filter('strftime', strftime)