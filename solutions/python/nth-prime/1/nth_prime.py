def is_prime(candidate):
    if candidate < 2:
        return False

    divisor = 2
    while divisor * divisor <= candidate:
        if candidate % divisor == 0:
            return False
        divisor = divisor + 1
    return True

def prime(number):
    if number < 1:
        raise ValueError("there is no zeroth prime")
    count = 0
    candidate = 2
    while True:
        if is_prime(candidate):
            count = count + 1
            if count == number:
                return candidate
        candidate = candidate + 1