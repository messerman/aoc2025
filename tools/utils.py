from functools import reduce 

def xor(l: list[int]):
    return reduce(lambda x,y: x^y, l)
