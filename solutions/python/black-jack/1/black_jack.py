"""Functions to help play and score a game of blackjack.

How to play blackjack:    https://bicyclecards.com/how-to-play/blackjack/
"Standard" playing cards: https://en.wikipedia.org/wiki/Standard_52-card_deck
"""


def value_of_card(card):
    if card=="A":
        return 1
    if card in {"Q","J","K"}:
        return 10
    else : return int(card)


def higher_card(card_one, card_two):
    card_one1=value_of_card(card_one)
    card_two1=value_of_card(card_two)
    if card_one1>card_two1:
        return card_one
    elif  card_two1>card_one1:    
        return card_two
    else :return card_one,card_two
        
    

def value_of_ace(card_one, card_two):
    if "A" in (card_one,card_two):
        return 1
    else:
        card_one1=value_of_card(card_one)
        card_two1=value_of_card(card_two)
        if card_one1+card_two1+11 <=21:
            return 11
        return 1
        


def is_blackjack(card_one, card_two):
    if "A" in {card_one,card_two}:
        card_one1=value_of_card(card_one)
        card_two1=value_of_card(card_two)
        if card_one1==10 or card_one1+card_two1+10==21:
            return True
    return  False
            
        
    

def can_split_pairs(card_one, card_two):
    card_one1=value_of_card(card_one)
    card_two1=value_of_card(card_two) 
    if card_one1==card_two1:
        return True
    return False


def can_double_down(card_one, card_two):
    card_one1=value_of_card(card_one)
    card_two1=value_of_card(card_two) 
    total=card_one1+card_two1
    if 9<=total<=11 :
        return True
    return False