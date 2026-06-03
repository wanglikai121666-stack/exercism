def response(hey_bob):
    text=hey_bob.strip()
    if text=="":
        return "Fine. Be that way!"
    judge=text
    if hey_bob.isupper():
        if judge[-1]=="?":
            return "Calm down, I know what I'm doing!"
        return "Whoa, chill out!"
    if judge[-1]=="?":
        return "Sure."
    return "Whatever."
        
    
