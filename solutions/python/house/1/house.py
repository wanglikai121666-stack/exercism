SUBJECTS = [
    "the house that Jack built.",
    "the malt",
    "the rat",
    "the cat",
    "the dog",
    "the cow with the crumpled horn",
    "the maiden all forlorn",
    "the man all tattered and torn",
    "the priest all shaven and shorn",
    "the rooster that crowed in the morn",
    "the farmer sowing his corn",
    "the horse and the hound and the horn",
]

ACTIONS = [
    "",
    "that lay in",
    "that ate",
    "that killed",
    "that worried",
    "that tossed",
    "that milked",
    "that kissed",
    "that married",
    "that woke",
    "that kept",
    "that belonged to",
]

def verse(number):
    lines = [f"This is {SUBJECTS[number - 1]}"]
    for index in range(number - 1, 0, -1):
        lines.append(f"{ACTIONS[index]} {SUBJECTS[index - 1]}")
    return " ".join(lines)
    
def recite(start_verse, end_verse):
    result = []
    for number in range(start_verse, end_verse + 1):
         result.append(verse(number))
    return result
