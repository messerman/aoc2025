#!/usr/bin/env python3
import cProfile
import math
import os

PARTS = [1, 2]
PATH = os.path.dirname(os.path.realpath(__file__))
FILES = ['sample.txt', 'input.txt']
PAUSE = True
SOLUTION = 0

def parse(my_input: list[str]) -> list[[str,str]]:
    result: list['range'] = []
    for line in my_input:
        try:
            if not line:
                continue
            list(map(lambda pair: result.append(pair.split('-')), line.strip().split(',')))
        except BaseException as e:
            print(line)
            raise e
    return result

def repeat_factor(start: int, end: int) -> int:
    if end % start:
        return -1
    result_str = (((start-1) * '0') + '1') * (end//start)
    return int(result_str.lstrip('0'))

def num_digits(val: int) -> int:
    return len(str(val))

def find_invalid(start: str, end: str) -> list[int]:
    slen = len(start)
    elen = len(end)
    offset = elen-slen

    sint = int(start)
    eint = int(end)

    results: list[int] = []
    ranges: list['range'] = []
    current = sint

    while current <= eint:
        range_end = 10**num_digits(current) - 1
        results += find_invalid_eq(current, min(eint, range_end))
        current = min(range_end, eint) + 1

    return list(set(results)) # remove duplicates

def find_invalid_eq(start: int, end: int) -> list[int]:
    assert(num_digits(start) == num_digits(end))
    digits = num_digits(start)

    if SOLUTION == 1 and digits % 2:
        return []

    results: list[int] = []
    sval = 1 if SOLUTION == 2 else digits // 2
    for i in range(sval, digits // 2 + 1):
        factor = repeat_factor(i, digits)
        if factor < 0:
            # print('    unable to comply')
            continue

        s = int(str(start)[:i])
        e = int(str(end)[:i])
        for j in range(int(str(start)[:i]), int(str(end)[:i])+1):
            if j*factor in range(start, end+1):
                results.append(j*factor)

    return results

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)
    results: list[int] = []
    for pair in data:
        r = find_invalid(pair[0], pair[1])
        # print(pair, r)
        results += r

    return sum(results)

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    data = parse(my_input)
    results: list[int] = []
    for pair in data:
        r = find_invalid(pair[0], pair[1])
        # print(pair, r)
        results += r

    return sum(results)

result: int
def main():
    for part in PARTS:
        print(f"---- Part {part} ----")
        for file in FILES:
            filename = file.split('.', maxsplit=1)[0]
            print(f'-- {file} --')
            with open('/'.join([PATH, file]), 'r', encoding='utf-8') as f:
                lines = f.read().split('\n')
                cProfile.run(f'result = solution{part}({lines})', f'{part}-{filename}.pstats')
                print(result)
            if PAUSE:
                text = input('continue? ')
                if text:
                    break
        if PAUSE and text:
            break

if __name__ == '__main__':
    main()
