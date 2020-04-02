import random
import time


dateFormats = ['%d-%m-%y', '%d-%m-%Y' , '%Y-%m-%d', '%Y%m%d', '%y%m%d', '%Y-%d-%m', '%Y.%m.%d', '%Y/%m/%d', '%y.%m.%d', '%y/%m/%d', '%m.%d.%Y', '%m/%d/%y' ]

## Format dd-mm-yy
def getRandomDate():
    date = random_date("1/1/2010 1:30 PM", "1/1/2020 4:50 AM", random.random(), random.choice(dateFormats))
    return date


def str_time_prop(start, end, format, prop, endFormat):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(endFormat, time.localtime(ptime))


def random_date(start, end, prop, endFormat):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop, endFormat)
