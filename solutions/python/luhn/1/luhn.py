class Luhn:
    def __init__(self, card_num):
        self.card_num = card_num

    def valid(self):
        number = self.card_num.replace(" ", "")
        if len(number) <= 1:
            return False

        if not number.isdigit():
            return False
        total = 0
        reverse_digits = number[::-1]
        for index, char in enumerate(reverse_digits):
            digit = int(char)
            if index % 2 == 1:
                digit = digit * 2
                if digit > 9:
                    digit = digit - 9
            total += digit
        return total % 10 == 0
