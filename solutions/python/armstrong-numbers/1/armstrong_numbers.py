def is_armstrong_number(number):
    a=str(number)
    p=len(a)
    total=0
    for pp in a :
        total+= int(pp)**p
    return total == number