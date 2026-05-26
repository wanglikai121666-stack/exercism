"""Functions for creating, transforming, and adding prefixes to strings."""


def add_prefix_un(word):
    return "un"+ word

def make_word_groups(vocab_words):
    a=vocab_words[0]
    a=" :: "+a
    return a.join(vocab_words)

def remove_suffix_ness(word):
    word=word[:-4]
    if word[-1]=="i":
        word=word[:-1]+"y"
        return word
        
    return word
        
    
        
    


def adjective_to_verb(sentence, index):
    words=sentence.split()
    word=words[index]
    word=word.strip(".")
    return word+"en"
    
