import math


class ComplexNumber:
    def __init__(self, real, imaginary):
        # 保存复数的实部和虚部
        self.real = real
        self.imaginary = imaginary

    def _convert_other(self, other):
        # 如果已经是复数对象，直接返回
        if isinstance(other, ComplexNumber):
            return other

        # 普通数字 n 可以看成 n + 0i
        if isinstance(other, (int, float)):
            return ComplexNumber(other, 0)

        # 其他类型无法参与运算
        return NotImplemented

    def __eq__(self, other):
        # 支持复数与普通实数比较
        other = self._convert_other(other)

        if other is NotImplemented:
            return NotImplemented

        return (
            self.real == other.real
            and self.imaginary == other.imaginary
        )

    def __add__(self, other):
        # self + other
        other = self._convert_other(other)

        if other is NotImplemented:
            return NotImplemented

        return ComplexNumber(
            self.real + other.real,
            self.imaginary + other.imaginary
        )

    def __radd__(self, other):
        # other + self
        # 加法可以交换顺序
        return self.__add__(other)

    def __sub__(self, other):
        # self - other
        other = self._convert_other(other)

        if other is NotImplemented:
            return NotImplemented

        return ComplexNumber(
            self.real - other.real,
            self.imaginary - other.imaginary
        )

    def __rsub__(self, other):
        # other - self
        # 减法不能直接交换顺序
        other = self._convert_other(other)

        if other is NotImplemented:
            return NotImplemented

        return ComplexNumber(
            other.real - self.real,
            other.imaginary - self.imaginary
        )

    def __mul__(self, other):
        # (a + bi)(c + di)
        # = (ac - bd) + (ad + bc)i
        other = self._convert_other(other)

        if other is NotImplemented:
            return NotImplemented

        new_real = (
            self.real * other.real
            - self.imaginary * other.imaginary
        )

        new_imaginary = (
            self.real * other.imaginary
            + self.imaginary * other.real
        )

        return ComplexNumber(new_real, new_imaginary)

    def __rmul__(self, other):
        # other * self
        # 乘法可以交换顺序
        return self.__mul__(other)

    def __truediv__(self, other):
        # self / other
        other = self._convert_other(other)

        if other is NotImplemented:
            return NotImplemented

        denominator = (
            other.real ** 2
            + other.imaginary ** 2
        )

        if denominator == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        new_real = (
            self.real * other.real
            + self.imaginary * other.imaginary
        ) / denominator

        new_imaginary = (
            self.imaginary * other.real
            - self.real * other.imaginary
        ) / denominator

        return ComplexNumber(new_real, new_imaginary)

    def __rtruediv__(self, other):
        # other / self
        other = self._convert_other(other)

        if other is NotImplemented:
            return NotImplemented

        # 转换后相当于：
        # ComplexNumber(other, 0) / self
        return other.__truediv__(self)

    def __abs__(self):
        # |a + bi| = sqrt(a² + b²)
        return math.sqrt(
            self.real ** 2
            + self.imaginary ** 2
        )

    def conjugate(self):
        # a + bi 的共轭是 a - bi
        return ComplexNumber(
            self.real,
            -self.imaginary
        )

    def exp(self):
        # e^(a + bi)
        # = e^a × (cos(b) + i × sin(b))
        factor = math.exp(self.real)

        return ComplexNumber(
            factor * math.cos(self.imaginary),
            factor * math.sin(self.imaginary)
        )