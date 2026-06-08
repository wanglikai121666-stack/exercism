def find_anagrams(word, candidates):
    result = []
    word_lower = word.lower()
    sorted_word = sorted(word_lower) #把字母按照顺序排列
    for candidate in candidates:
        candidate_lower = candidate.lower()
        
        if candidate_lower == word_lower:
            continue
        if sorted(candidate_lower) == sorted_word:
            result.append(candidate)
            
    return result
    
    