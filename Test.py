from datetime import date
from dateutil import rrule

start_date = date(2017, 1, 1)
end_date = date(2017, 1, 10)

for date in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
    print(date.strftime('%m/%d/%Y'))
