import calendar
import datetime


class Calendar(calendar.LocaleHTMLCalendar):
	cssclass_month = 'table'


def previous_date(d):
	first = d.replace(day=1)
	previous_month = first - datetime.timedelta(days=1)
	month = 'date=' + str(previous_month.year) + '-' + str(previous_month.month)
	return month

def next_date(d):
	days_in_month = calendar.monthrange(d.year, d.month)[1]
	last = d.replace(day=days_in_month)
	next_month = last + datetime.timedelta(days=1)
	month = 'date=' + str(next_month.year) + '-' + str(next_month.month)
	return month

def get_date(req_day):
	if req_day:
		year, month = (int(x) for x in req_day.split('-'))
		return datetime.date(year, month, day=1)
	return datetime.date.today()
