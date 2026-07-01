def count_words(sentence):
    counts = {}
    cleaned = ""
    for char in sentence.lower():
        if char.isalnum() or char == "'":
            cleaned += char
        else:
            cleaned += " "
    words = cleaned.split()
    for word in words:
        word = word.strip("'")
        if word == "":
            continue
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
        
