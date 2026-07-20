from calendar import monthrange
from datetime import date


class MeetupDayException(ValueError):
    """当请求的 meetup 日期不存在时抛出。"""


WEEKDAYS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


WEEK_INDEXES = {
    "first": 0,
    "second": 1,
    "third": 2,
    "fourth": 3,
    "fifth": 4,
}


def meetup(year, month, week, day_of_week):
    target_weekday = WEEKDAYS[day_of_week]

    # 得到这个月一共有多少天
    days_in_month = monthrange(year, month)[1]

    matching_dates = []

    # 找出这个月所有符合目标星期的日期
    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)

        if current_date.weekday() == target_weekday:
            matching_dates.append(current_date)

    # teenth：目标日期必须在 13～19 日之间
    if week == "teenth":
        for matching_date in matching_dates:
            if 13 <= matching_date.day <= 19:
                return matching_date

    # last：最后一个目标星期
    if week == "last":
        return matching_dates[-1]

    # first、second、third、fourth、fifth
    index = WEEK_INDEXES[week]

    try:
        return matching_dates[index]
    except IndexError:
        raise MeetupDayException("That day does not exist.")