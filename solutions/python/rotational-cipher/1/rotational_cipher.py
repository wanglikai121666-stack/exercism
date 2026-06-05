def rotate(text, key):
    result =""
    for char in text:
        if "a"<=char<="z":
            oldindex=ord(char)-ord("a")
            newindex=(key+oldindex)%26
            result+=chr(newindex+ord("a"))
        elif "A"<=char<="Z":
            oldindex=ord(char)-ord("A")
            newindex=(key+oldindex)%26
            result+=chr(newindex+ord("A"))
        else :result+=char
    return result.strip()