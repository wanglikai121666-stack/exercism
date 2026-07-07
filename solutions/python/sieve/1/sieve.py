def primes(limit):
    if limit < 2:
        return []

    is_prime = [True] * (limit + 1)

    is_prime[0] = False
    is_prime[1] = False

    for number in range(2, limit + 1):
        if is_prime[number]:
            for multiple in range(number * 2, limit + 1, number):
                is_prime[multiple] = False

    result = []

    for number in range(2, limit + 1):
        if is_prime[number]:
            result.append(number)

    return result