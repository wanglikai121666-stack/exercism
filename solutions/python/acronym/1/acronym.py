def abbreviate(words):
    words = words.replace("-", " ")
    cleaned = ""
    for char in words:
        if char.isalnum() or char.isspace():
            cleaned += char
    word_list = cleaned.split()
    acronym = ""
    for word in word_list:
         first_letter = word[0]
         acronym = acronym + first_letter.upper()
    return acronym