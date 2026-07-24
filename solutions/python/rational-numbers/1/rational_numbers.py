from math import gcd


class Rational:
    def __init__(self, numer, denom):
        # 分母不能为 0。
        if denom == 0:
            raise ZeroDivisionError("denominator cannot be zero")

        # 计算最大公约数。
        common_divisor = gcd(numer, denom)

        # 分子、分母同时约分。
        numer //= common_divisor
        denom //= common_divisor

        # 标准形式要求分母为正数。
        if denom < 0:
            numer = -numer
            denom = -denom

        self.numer = numer
        self.denom = denom

    def __eq__(self, other):
        """判断两个有理数是否相等。"""
        return (
            self.numer == other.numer
            and self.denom == other.denom
        )

    def __repr__(self):
        """决定 print() 时怎样显示这个有理数。"""
        return f"{self.numer}/{self.denom}"

    def __add__(self, other):
        """有理数加法：a/b + c/d。"""
        new_numer = (
            self.numer * other.denom
            + other.numer * self.denom
        )
        new_denom = self.denom * other.denom

        return Rational(new_numer, new_denom)

    def __sub__(self, other):
        """有理数减法：a/b - c/d。"""
        new_numer = (
            self.numer * other.denom
            - other.numer * self.denom
        )
        new_denom = self.denom * other.denom

        return Rational(new_numer, new_denom)

    def __mul__(self, other):
        """有理数乘法：a/b × c/d。"""
        new_numer = self.numer * other.numer
        new_denom = self.denom * other.denom

        return Rational(new_numer, new_denom)

    def __truediv__(self, other):
        """有理数除法：a/b ÷ c/d。"""
        # 除以 c/d，相当于乘以它的倒数 d/c。
        new_numer = self.numer * other.denom
        new_denom = self.denom * other.numer

        return Rational(new_numer, new_denom)

    def __abs__(self):
        """求有理数的绝对值。"""
        return Rational(
            abs(self.numer),
            abs(self.denom),
        )

    def __pow__(self, power):
        """有理数的整数或浮点数次幂。"""

        # 整数次幂返回 Rational。
        if isinstance(power, int):
            # 非负整数次幂：
            # (a/b)^n = a^n / b^n
            if power >= 0:
                return Rational(
                    self.numer ** power,
                    self.denom ** power,
                )

            # 负整数次幂需要把分子、分母倒过来。
            # (a/b)^-n = b^n / a^n
            magnitude = abs(power)

            return Rational(
                self.denom ** magnitude,
                self.numer ** magnitude,
            )

        # 浮点数次幂返回普通实数。
        return (self.numer / self.denom) ** power

    def __rpow__(self, base):
        """实数的有理数次幂，例如 8 ** Rational(4, 3)。"""
        exponent = self.numer / self.denom
        return base ** exponent