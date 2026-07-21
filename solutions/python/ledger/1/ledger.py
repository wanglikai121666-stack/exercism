# -*- coding: utf-8 -*-

from datetime import datetime


# ============================================================
# 固定列宽
# ============================================================
#
# 最终表格由三列组成：
#
# 日期列：10 个字符
# 描述列：25 个字符
# 金额列：13 个字符
#
# 把这些数字定义成常量，避免代码中到处出现 10、25、13
# 这种难以理解的“魔法数字”。

DATE_WIDTH = 10
DESCRIPTION_WIDTH = 25
CHANGE_WIDTH = 13


# ============================================================
# 货币配置
# ============================================================
#
# 货币本身只决定符号。
#
# 至于千位分隔符、小数分隔符、负数样式，
# 这些属于地区格式，应当放在 LOCALE_SETTINGS 中。

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
}


# ============================================================
# 地区配置
# ============================================================
#
# 美国和荷兰格式之间真正不同的内容包括：
#
# 1. 表头文字
# 2. 日期顺序和日期分隔符
# 3. 千位分隔符
# 4. 小数分隔符
# 5. 货币符号后面是否有空格
# 6. 负数使用括号还是减号
#
# 将这些区别全部放进配置字典后，
# 主要业务代码就不需要写两个庞大的 if 分支。

LOCALE_SETTINGS = {
    "en_US": {
        "headers": ("Date", "Description", "Change"),

        # 美国日期格式：月 / 日 / 年
        "date_order": ("month", "day", "year"),
        "date_separator": "/",

        # 美国金额格式：1,234.56
        "thousands_separator": ",",
        "decimal_separator": ".",

        # 美国货币符号和金额之间没有空格：$10.00
        "symbol_separator": "",

        # 美国负数使用括号：($10.00)
        "negative_style": "parentheses",
    },

    "nl_NL": {
        "headers": ("Datum", "Omschrijving", "Verandering"),

        # 荷兰日期格式：日 - 月 - 年
        "date_order": ("day", "month", "year"),
        "date_separator": "-",

        # 荷兰金额格式：1.234,56
        "thousands_separator": ".",
        "decimal_separator": ",",

        # 荷兰格式中，货币符号后面有空格：€ 10,00
        "symbol_separator": " ",

        # 荷兰负数使用减号：€ -10,00
        "negative_style": "minus",
    },
}


# ============================================================
# 数据对象
# ============================================================

class LedgerEntry:
    """
    表示账本中的一条记录。

    每条记录包含：
    date：日期对象
    description：账目描述
    change：金额变化，单位为分
    """

    def __init__(self, date=None, description=None, change=None):
        # 参数保留默认值 None，
        # 这样仍然兼容原代码中 LedgerEntry() 的创建方式。
        self.date = date
        self.description = description
        self.change = change


def create_entry(date, description, change):
    """
    根据日期字符串、描述和金额创建一条账目。

    date 的输入格式：
        YYYY-MM-DD

    change 的单位是分：
        1000 代表 10.00
        -1000 代表 -10.00
    """

    # 将字符串日期转换成 datetime 对象，
    # 这样后面可以正确地进行日期排序。
    parsed_date = datetime.strptime(date, "%Y-%m-%d")

    # 创建对象时直接传入完整数据，
    # 不再先创建空对象，然后逐个修改属性。
    return LedgerEntry(
        parsed_date,
        description,
        change,
    )


# ============================================================
# 配置读取与校验
# ============================================================

def _get_locale_settings(locale):
    """
    根据地区代码取得对应配置。

    以下划线开头表示：
    这是模块内部使用的辅助函数。
    """

    if locale not in LOCALE_SETTINGS:
        raise ValueError(f"Unsupported locale: {locale}")

    return LOCALE_SETTINGS[locale]


def _get_currency_symbol(currency):
    """根据货币代码取得货币符号。"""

    if currency not in CURRENCY_SYMBOLS:
        raise ValueError(f"Unsupported currency: {currency}")

    return CURRENCY_SYMBOLS[currency]


# ============================================================
# 排序
# ============================================================

def _sort_entries(entries):
    """
    对账目进行排序。

    排序优先级：
    1. 日期从早到晚
    2. 日期相同时，金额从小到大
    3. 金额也相同时，描述按字母顺序
    """

    return sorted(
        entries,
        key=lambda entry: (
            entry.date,
            entry.change,
            entry.description,
        ),
    )


# ============================================================
# 表头格式化
# ============================================================

def _format_header(settings):
    """根据地区配置生成表头。"""

    date_header, description_header, change_header = settings["headers"]

    # < 表示左对齐。
    #
    # 例如：
    # f"{'Date':<10}"
    #
    # 表示将 Date 放进宽度为 10 的区域，
    # 不足的部分在右边补空格。
    return (
        f"{date_header:<{DATE_WIDTH}} | "
        f"{description_header:<{DESCRIPTION_WIDTH}} | "
        f"{change_header:<{CHANGE_WIDTH}}"
    )


# ============================================================
# 日期格式化
# ============================================================

def _format_date(date, settings):
    """
    根据地区配置格式化日期。

    en_US：
        07/21/2026

    nl_NL：
        21-07-2026
    """

    # :02d 表示至少显示两位数字，不足时在左边补 0。
    #
    # 例如：
    # 7 -> "07"
    day = f"{date.day:02d}"
    month = f"{date.month:02d}"

    # 年份至少显示四位。
    year = f"{date.year:04d}"

    date_parts = {
        "day": day,
        "month": month,
        "year": year,
    }

    # 根据配置决定日期顺序。
    #
    # en_US：
    # ("month", "day", "year")
    #
    # nl_NL：
    # ("day", "month", "year")
    ordered_parts = [
        date_parts[part_name]
        for part_name in settings["date_order"]
    ]

    # 使用地区对应的分隔符连接日期。
    return settings["date_separator"].join(ordered_parts)


# ============================================================
# 描述格式化
# ============================================================

def _format_description(description):
    """
    将描述处理为固定的 25 个字符。

    超过 25 个字符：
        保留前 22 个字符，再加 ...

    不足 25 个字符：
        在右边补空格
    """

    if len(description) > DESCRIPTION_WIDTH:
        # 需要给三个点留出三个字符。
        visible_length = DESCRIPTION_WIDTH - 3

        return description[:visible_length] + "..."

    # < 表示左对齐，空余位置在右边补空格。
    return f"{description:<{DESCRIPTION_WIDTH}}"


# ============================================================
# 金额数字部分格式化
# ============================================================

def _format_whole_units(whole_units, thousands_separator):
    """
    给金额的整数部分添加千位分隔符。

    例如：
        1234567 -> 1,234,567
        1234567 -> 1.234.567
    """

    # Python默认使用逗号进行千位分组。
    grouped = f"{whole_units:,}"

    # 荷兰格式需要把逗号替换成点。
    if thousands_separator != ",":
        grouped = grouped.replace(",", thousands_separator)

    return grouped


def _format_absolute_amount(change, settings):
    """
    格式化金额的绝对值部分。

    本函数不处理：
    - 正负号
    - 括号
    - 货币符号

    只负责生成：
        1,234.56
    或：
        1.234,56
    """

    # 金额原本以“分”为单位。
    #
    # 例如：
    # 123456 分
    #
    # divmod(123456, 100) 得到：
    # whole_units = 1234
    # cents = 56
    absolute_change = abs(change)
    whole_units, cents = divmod(absolute_change, 100)

    grouped_whole_units = _format_whole_units(
        whole_units,
        settings["thousands_separator"],
    )

    # cents:02d 保证分始终有两位。
    #
    # 例如：
    # 5 -> 05
    return (
        f"{grouped_whole_units}"
        f"{settings['decimal_separator']}"
        f"{cents:02d}"
    )


# ============================================================
# 货币符号和负数样式
# ============================================================

def _decorate_amount(number, change, currency_symbol, settings):
    """
    给金额数字加上：

    - 货币符号
    - 正负号或括号
    - 必要的结尾空格
    """

    symbol_separator = settings["symbol_separator"]

    # 美国格式
    if settings["negative_style"] == "parentheses":
        amount = f"{currency_symbol}{symbol_separator}{number}"

        if change < 0:
            # 美国负数：
            # ($10.00)
            return f"({amount})"

        # 美国正数末尾需要保留一个空格。
        return amount + " "

    # 荷兰格式
    if settings["negative_style"] == "minus":
        sign = "-" if change < 0 else ""

        # 荷兰格式：
        # € 10,00
        # € -10,00
        return (
            f"{currency_symbol}"
            f"{symbol_separator}"
            f"{sign}"
            f"{number} "
        )

    # 配置错误时主动抛出异常，
    # 避免返回一个不完整的金额。
    raise ValueError(
        f"Unsupported negative style: "
        f"{settings['negative_style']}"
    )


def _format_change(change, currency_symbol, settings):
    """
    完整格式化金额，并将其右对齐到金额列中。
    """

    number = _format_absolute_amount(change, settings)

    decorated_amount = _decorate_amount(
        number,
        change,
        currency_symbol,
        settings,
    )

    # > 表示右对齐。
    #
    # 金额列固定占 13 个字符，
    # 空余位置在金额左边补空格。
    return f"{decorated_amount:>{CHANGE_WIDTH}}"


# ============================================================
# 单行账目格式化
# ============================================================

def _format_entry(entry, currency_symbol, settings):
    """
    将一条 LedgerEntry 转换成表格中的一行。
    """

    date = _format_date(entry.date, settings)
    description = _format_description(entry.description)
    change = _format_change(
        entry.change,
        currency_symbol,
        settings,
    )

    return f"{date} | {description} | {change}"


# ============================================================
# 对外主函数
# ============================================================

def format_entries(currency, locale, entries):
    """
    将账目列表格式化为完整的账本表格。

    参数：
        currency：USD 或 EUR
        locale：en_US 或 nl_NL
        entries：LedgerEntry 对象列表

    返回：
        完整的表格字符串
    """

    # 读取地区和货币配置。
    settings = _get_locale_settings(locale)
    currency_symbol = _get_currency_symbol(currency)

    # 使用列表保存每一行。
    #
    # 相比在循环中不断使用 table +=，
    # 这种方式更清晰，也避免反复创建新字符串。
    rows = [
        _format_header(settings)
    ]

    # sorted() 返回一个新的列表，
    # 不会像原代码的 pop() 那样清空传入的 entries。
    sorted_entries = _sort_entries(entries)

    for entry in sorted_entries:
        row = _format_entry(
            entry,
            currency_symbol,
            settings,
        )

        rows.append(row)

    # 使用换行符连接表头和所有账目行。
    return "\n".join(rows)