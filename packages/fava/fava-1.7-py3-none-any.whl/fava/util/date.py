"""Date-related functionality.

Note:
    Date ranges are always tuples (start, end) from the (inclusive) start date
    to the (exclusive) end date.
"""

import re
import datetime

IS_RANGE_RE = re.compile(r'(.*?)(?:-|to)(?=\s*\d{4})(.*)')

# these match dates of the form 'year-month-day'
# day or month and day may be omitted
YEAR_RE = re.compile(r'^\d{4}$')
MONTH_RE = re.compile(r'^(\d{4})-(\d{2})$')
DAY_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')

# this matches a week like 2016-W02 for the second week of 2016
WEEK_RE = re.compile(r'^(\d{4})-w(\d{2})$')

# this matches a quarter like 2016-Q1 for the first quarter of 2016
QUARTER_RE = re.compile(r'^(\d{4})-q(\d)$')

VARIABLE_RE = re.compile(
    r'\(?(year|quarter|month|week|day)(?:([-+])(\d+))?\)?')


def get_next_interval(date, interval):
    """Get the start date of the next interval.

    Args:
        date: A date.
        interval: A string specifying the interval.

    Returns:
        The start date of the next `interval` after `date`.

    """
    if interval == 'year':
        return datetime.date(date.year + 1, 1, 1)
    elif interval == 'quarter':
        for i in [4, 7, 10]:
            if date.month < i:
                return datetime.date(date.year, i, 1)
        return datetime.date(date.year + 1, 1, 1)
    elif interval == 'month':
        month = (date.month % 12) + 1
        year = date.year + (date.month + 1 > 12)
        return datetime.date(year, month, 1)
    elif interval == 'week':
        return date + datetime.timedelta(7 - date.weekday())
    elif interval == 'day':
        return date + datetime.timedelta(1)
    else:
        raise NotImplementedError


def interval_ends(first, last, interval):
    """List intervals.

    Args:
        first: A datetime.date.
        last: A datetime.date.
        interval: A string specifying the interval.

    Yields:
        Dates corresponding to the starts/ends of intervals between `first` and
        `last`.
    """
    while first < last:
        yield first
        first = get_next_interval(first, interval)

    yield last


def substitute(string):
    """Replace variables referring to the current day.

    Args:
        string: A string, possibly containing variables for today.

    Returns:
        A string, where variables referring to the current day, like 'year' or
        'week' have been replaced by the corresponding string understood by
        :func:`parse_date`.  Can compute addition and subtraction.
    """
    today = datetime.date.today()

    for match in VARIABLE_RE.finditer(string):
        complete_match, interval, plusminus, mod = match.group(0, 1, 2, 3)
        mod = int(mod) if mod else 0
        plusminus = 1 if plusminus == '+' else -1
        if interval == 'year':
            year = today.year + plusminus * mod
            string = string.replace(complete_match, str(year))
        if interval == 'quarter':
            quarter_today = (today.month - 1) // 3 + 1
            year = today.year + (quarter_today + plusminus * mod - 1) // 4
            quarter = (quarter_today + plusminus * mod - 1) % 4 + 1
            string = string.replace(
                complete_match, '{}-Q{}'.format(year, quarter))
        if interval == 'month':
            year = today.year + (today.month + plusminus * mod - 1) // 12
            month = (today.month + plusminus * mod - 1) % 12 + 1
            string = string.replace(
                complete_match, '{}-{:02}'.format(year, month))
        if interval == 'week':
            delta = datetime.timedelta(plusminus * mod * 7)
            string = string.replace(
                complete_match, (today + delta).strftime('%Y-W%W'))
        if interval == 'day':
            delta = datetime.timedelta(plusminus * mod)
            string = string.replace(
                complete_match, (today + delta).isoformat())
    return string


def parse_date(string):  # pylint: disable=too-many-return-statements
    """Parse a date.

    Example of supported formats:

    - 2010-03-15, 2010-03, 2010
    - 2010-W01, 2010-Q3

    Ranges of dates can be expressed in the following forms:

    - start - end
    - start to end

    where start and end look like one of the above examples

    Args:
        string: A date(range) in our custom format.

    Returns:
        A tuple (start, end) of dates.

    """
    string = string.strip().lower()
    if not string:
        return None, None

    string = substitute(string)

    match = IS_RANGE_RE.match(string)
    if match:
        return (parse_date(match.group(1))[0],
                parse_date(match.group(2))[1])

    match = YEAR_RE.match(string)
    if match:
        year = int(match.group(0))
        start = datetime.date(year, 1, 1)
        return start, get_next_interval(start, 'year')

    match = MONTH_RE.match(string)
    if match:
        year, month = map(int, match.group(1, 2))
        start = datetime.date(year, month, 1)
        return start, get_next_interval(start, 'month')

    match = DAY_RE.match(string)
    if match:
        year, month, day = map(int, match.group(1, 2, 3))
        start = datetime.date(year, month, day)
        return start, get_next_interval(start, 'day')

    match = WEEK_RE.match(string)
    if match:
        year, week = match.group(1, 2)
        date_str = '{}{}1'.format(year, week)
        first_week_day = datetime.datetime.strptime(date_str, '%Y%W%w').date()
        return first_week_day, get_next_interval(first_week_day, 'week')

    match = QUARTER_RE.match(string)
    if match:
        year, quarter = map(int, match.group(1, 2))
        quarter_first_day = datetime.date(year, (quarter - 1) * 3 + 1, 1)
        return quarter_first_day, get_next_interval(quarter_first_day,
                                                    'quarter')
    return None, None


def days_in_daterange(start_date, end_date):
    """Yield a datetime for every day in the specified interval.

    Args:
        start_date: A start date.
        end_date: An end date (exclusive).

    Returns:
        An iterator yielding all days between `start_date` to `end_date`.

    """
    for diff in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(diff)


def number_of_days_in_period(period, date_):
    """Returns the days in the specified `period` and `date_`."""

    if period == 'daily':
        return 1
    if period == 'weekly':
        return 7
    if period == 'monthly':
        date_ = datetime.date(date_.year, date_.month, 1)
        return (get_next_interval(date_, 'month') - date_).days
    if period == 'quarterly':
        quarter = (date_.month - 1) / 3 + 1
        date_ = datetime.date(date_.year, int(quarter) * 3 - 2, 1)
        return (get_next_interval(date_, 'quarter') - date_).days
    if period == 'yearly':
        date_ = datetime.date(date_.year, 1, 1)
        return (get_next_interval(date_, 'year') - date_).days
    else:
        raise NotImplementedError
