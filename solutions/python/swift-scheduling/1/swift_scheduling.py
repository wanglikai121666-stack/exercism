import calendar
from datetime import datetime, timedelta


def set_time(value, hour, minute=0):
    """把某个日期的时间设置成指定的时和分。"""
    return value.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )


def first_workday(year, month):
    """返回指定月份第一个工作日的 08:00。"""
    result = datetime(year, month, 1, 8, 0)

    # weekday():
    # 周一到周五是 0～4
    # 周六和周日是 5、6
    while result.weekday() >= 5:
        result += timedelta(days=1)

    return result


def last_workday(year, month):
    """返回指定月份最后一个工作日的 08:00。"""

    # monthrange() 返回：
    # (当月第一天是星期几, 当月总天数)
    # [1] 取第二个元素，也就是当月总天数
    last_day = calendar.monthrange(year, month)[1]

    result = datetime(year, month, last_day, 8, 0)

    # 如果最后一天是周末，就一天一天往前找
    while result.weekday() >= 5:
        result -= timedelta(days=1)

    return result


def delivery_date(start, description):
    # 输入的 start 是字符串，先转成 datetime 对象
    meeting_start = datetime.fromisoformat(start)

    # NOW：会议开始两小时后
    if description == "NOW":
        result = meeting_start + timedelta(hours=2)
        return result.isoformat()

    # ASAP
    if description == "ASAP":
        # 13:00 之前开会：当天 17:00
        if meeting_start.hour < 13:
            result = set_time(meeting_start, 17)
        else:
            # 13:00 或之后开会：第二天 13:00
            tomorrow = meeting_start + timedelta(days=1)
            result = set_time(tomorrow, 13)

        return result.isoformat()

    # EOW
    if description == "EOW":
        weekday = meeting_start.weekday()

        # 星期一、二、三：本周五 17:00
        if weekday <= 2:
            days_until_friday = 4 - weekday
            friday = meeting_start + timedelta(days=days_until_friday)
            result = set_time(friday, 17)

        # 星期四、五：本周日 20:00
        else:
            days_until_sunday = 6 - weekday
            sunday = meeting_start + timedelta(days=days_until_sunday)
            result = set_time(sunday, 20)

        return result.isoformat()

    # <N>M，例如 3M、8M、12M
    if description.endswith("M"):
        # 去掉最后的 M，再转成整数
        target_month = int(description[:-1])

        # 目标月份还没到：使用今年
        if meeting_start.month < target_month:
            target_year = meeting_start.year
        else:
            # 已经进入或超过目标月份：使用明年
            target_year = meeting_start.year + 1

        result = first_workday(target_year, target_month)
        return result.isoformat()

    # Q<N>，例如 Q1、Q2、Q3、Q4
    if description.startswith("Q"):
        # 去掉开头的 Q，再转成整数
        target_quarter = int(description[1:])

        # 根据当前月份计算当前季度
        current_quarter = (meeting_start.month - 1) // 3 + 1

        # 当前在目标季度之前或正处于目标季度：今年
        if current_quarter <= target_quarter:
            target_year = meeting_start.year
        else:
            # 目标季度已经过去：明年
            target_year = meeting_start.year + 1

        # 每个季度最后一个月：
        # Q1 → 3 月，Q2 → 6 月，Q3 → 9 月，Q4 → 12 月
        final_month = target_quarter * 3

        result = last_workday(target_year, final_month)
        return result.isoformat()

    raise ValueError(f"Unknown description: {description}")