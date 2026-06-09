def square_of_sum(number):
    total=sum(range(1,number+1))
    return total**2


def sum_of_squares(number):
    total=0
    for value in range(1,number+1):
        total+=value**2
    return total

def difference_of_squares(number):
    return square_of_sum(number)-sum_of_squares(number)
