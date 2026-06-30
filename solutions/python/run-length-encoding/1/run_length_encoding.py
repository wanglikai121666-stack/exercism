def decode(string):
    result = ""
    number = ""
    for char in string:
        if char.isdigit():
            number = number + char
        else:
            if number == "":
                result = result + char
            else:
                 count = int(number)
                 result = result + char * count
                 number = ""
    return result

def encode(string):
    if string == "":
        return ""
    result = ""
    current_char = string[0]
    count = 1
    for index in range(1, len(string)):
        char = string[index]
        if char == current_char:
            count = count + 1
        else:
            if count > 1:
                result = result + str(count) + current_char
            else:
                result = result + current_char
            current_char = char
            count = 1
    if count > 1:
                result = result + str(count) + current_char
    else:
                result = result + char
    return result