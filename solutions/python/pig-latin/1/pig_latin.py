VOWELS="aeiou"
def translate(text):
    words = text.split()
    translatedwords=[]
    for word in words:
        translatedwords.append(translatewords(word))
    return " ".join(translatedwords)
def translatewords(word):
    if startwithvowelsound(word):
        return word+"ay"
    for index in range(len(word)):
        if word[index:index+2]=="qu":
            splitindex=index+2
            return word[splitindex:]+word[:splitindex]+"ay"
        if word[index]=="y"and index>0:
            return word[index:]+word[:index]+"ay"
        if word[index] in VOWELS:
            return word[index:]+word[:index]+"ay"
    return word+"ay"
        
    
def startwithvowelsound(word):
    return (
        word[0] in VOWELS
        or word.startswith("xr")
        or word.startswith("yt")
    )
    