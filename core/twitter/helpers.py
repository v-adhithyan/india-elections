from datetime import datetime, date, time, timedelta


def lower_bound(days):
    dt = date.today() + timedelta(days=days)
    return str(datetime.combine(dt, time.min))


def upper_bound(yesterday=False):
    dt = datetime.today()
    if yesterday:
        dt = dt + timedelta(days=-1)
    return str(datetime.combine(dt, time.max))
