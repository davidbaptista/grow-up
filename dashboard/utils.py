import calendar
import datetime

from dashboard.models import Event


class Calendar(calendar.LocaleHTMLCalendar):
	cssclass_month = 'table'

	def formatday(self, day, events):
		events_per_day = events.filter(start__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li class="calendar_list"> <a href="#"> {day} </a></li>'
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	def formatmonth(self, theyear, themonth, withyear=True):
		events = Event.objects.filter(start__year=theyear, start__month=themonth)
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
			a(self.formatweek(week, events))
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
