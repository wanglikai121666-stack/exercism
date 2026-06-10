def sum_of_multiples(limit, multiples):
    seen=set()
    for number in range(limit):
        for multiple in multiples:
            if multiple !=0 and number%multiple==0:
                seen.add(number)
                
    return sum(seen)