def classify(number):
    if number<1:
        raise ValueError("Classification is only possible for positive integers.")
    aliquot_sum = 0
    for factor in range(1,number):
        if number%factor==0 :
            aliquot_sum +=factor
    if aliquot_sum == number:
        return "perfect"

    if aliquot_sum > number:
        return "abundant"

    return "deficient"
            
        