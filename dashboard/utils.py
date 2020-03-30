import calendar
import datetime


class Calendar(calendar.LocaleHTMLCalendar):
	cssclass_month = 'table'

	def formatday(self, theyear, themonth, day, events):
		events_per_day = None

		if events:
			events_per_day = events.filter(start__day=day)

		if events_per_day and events_per_day.all().count() > 0 and day != 0:
			return f"<td><span class='date'><a href='/dashboard-reservations/?date={theyear}-{themonth}&day={day}'" \
			       f"class='btn btn-secondary'>{day}</a></span></td>"
		elif day != 0:
			return f"<td><span class='date btn btn-light'>{day}</span></td>"
		return '<td></td>'

	def formatweek(self, theyear, themonth, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(theyear, themonth, d, events)
		return f'<tr> {week} </tr>'

	def formatmonth(self, theyear, themonth, events, withyear=True):
		v = []
		a = v.append
		a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
			self.cssclass_month))
		a('\n')
		a(self.formatmonthname(theyear, themonth, withyear=withyear))
		a('\n')
		a(self.formatweekheader())
		a('\n')
		for week in self.monthdays2calendar(theyear, themonth):
			a(self.formatweek(theyear, themonth, week, events))
			a('\n')
		a('</table>')
		a('\n')
		return ''.join(v)


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
