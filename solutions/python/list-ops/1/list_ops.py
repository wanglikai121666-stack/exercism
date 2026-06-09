def append(list1, list2):
    result=[]
    for value in list1:
        result.append(value)
    for value in list2:
        result.append(value)
    return result


def concat(lists):
    if lists == []:
        return []
    return append(lists[0],concat(lists[1:]))


def filter(function, list):
    result=[]
    for item in list:
        if function(item):
            result.append(item)
    return result


def length(list):
    count = 0

    for item in list:
        count += 1

    return count


def map(function, list):
    result=[]
    for item in list:
            result.append(function(item))
    return result
            


def foldl(function, list, initial):
    accumulator = initial
    for item in list:
        accumulator = function(accumulator, item)
    return accumulator

def foldr(function, list, initial):
    accumulator = initial
    for item in list[::-1]:
        accumulator = function(accumulator,item)
    return accumulator


def reverse(list):
    result=[]
    for item in list:
        result=[item]+result
    return result
