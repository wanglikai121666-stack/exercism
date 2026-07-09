class Clock:
    def __init__(self, hour, minute):
          # 一天总共有 24 * 60 = 1440 分钟
        minutes_per_day = 24 * 60

        # 先把 hour 和 minute 统一换算成“总分钟”
        # 再对 1440 取模，让时间永远落在 00:00 到 23:59 之间
        self.total_minutes = (hour * 60 + minute) % minutes_per_day

        # 用总分钟还原小时和分钟
        # // 60 得到小时
        # % 60 得到剩余分钟
        self.hour = self.total_minutes // 60
        self.minute = self.total_minutes % 60

    def __repr__(self):
         return f"Clock({self.hour}, {self.minute})"

    def __str__(self):
         # 给用户看的时间格式
        # :02d 表示补成两位数字
        # 8 -> 08
        # 0 -> 00
        return f"{self.hour:02d}:{self.minute:02d}"

    def __eq__(self, other):
        return self.total_minutes == other.total_minutes

    def __add__(self, minutes):
        return Clock(0, self.total_minutes + minutes)


    def __sub__(self, minutes):
        return Clock(0, self.total_minutes - minutes)
