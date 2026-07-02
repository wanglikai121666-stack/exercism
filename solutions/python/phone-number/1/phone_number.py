class PhoneNumber:
    def __init__(self, number):
        digits = ""
        for char in number:
            if char.isalpha():
                raise ValueError("letters not permitted")
            if char.isdigit():
                digits += char
            elif char not in " .()-+":
                raise ValueError("punctuations not permitted")
        if len(digits) < 10:
            raise ValueError("must not be fewer than 10 digits")
        if len(digits) > 11:
            raise ValueError("must not be greater than 11 digits")
        if len(digits) == 11:
            if digits[0] != "1":
                raise ValueError("11 digits must start with 1")
            digits = digits[1:]
        if digits[0] == "0":
            raise ValueError("area code cannot start with zero")

        if digits[0] == "1":
            raise ValueError("area code cannot start with one")

        if digits[3] == "0":
            raise ValueError("exchange code cannot start with zero")

        if digits[3] == "1":
            raise ValueError("exchange code cannot start with one")
        self.number = digits
        self.area_code = digits[:3]
    def pretty(self):
        return f"({self.number[:3]})-{self.number[3:6]}-{self.number[6:]}"

