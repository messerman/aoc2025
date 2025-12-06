#!/usr/bin/env python3
import cProfile
import os

from tools.disjoint_range import DisjointRange
from tools.logger import DebugLogger as logger


PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

def parse(my_input: list[str]) -> tuple['DisjointRange', list[int]]:
    ranges = DisjointRange()
    ids: list[int] = []
    tmp_ranges = []

    reading_ids = False
    for line in my_input:
        try:
            if reading_ids:
                if not line:
                    continue
                ids.append(int(line))
            else:
                if not line:
                    reading_ids = True
                    continue
                a,b = line.split('-')
                tmp_ranges.append(range(int(a), int(b) +1))
                #ranges.add(range(int(a), int(b) + 1))

        except BaseException as e:
            logger.error(line)
            raise e
    tmp_ranges.sort(key=lambda x: float(f'{x.start}.{x.stop}'))
    for r in tmp_ranges:
        ranges.add(r)
    return (ranges, ids)

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    ranges,ids = parse(my_input)

    fresh_count = 0
    for ingredient in ids:
        if ranges.count(ingredient):
            fresh_count += 1

    return fresh_count

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    ranges = parse(my_input)[0]
    ## 378933199096739 -- too high
    ## 415797806089628 -- without duplicate checking
    ## 343715508272336 -- lower, after double-checking the endpoints, still too high!!!
    ## 343412707577639 -- somehow still too high
    ## 365695132468020 -- nope, still too big - still have overlaps for some reason
    ## 332067203034711 -- woohoo!

    return len(ranges)

result: int
def main():
    text = None
    for part in PARTS:
        logger.info(f"---- Part {part} ----")
        for file in FILES:
            filename = file.split('.', maxsplit=1)[0]
            logger.info(f'-- {file} --')
            with open('/'.join([PATH, file]), 'r', encoding='utf-8') as f:
                lines = f.read().split('\n')
                cProfile.run(f'result = solution{part}({lines})', f'{part}-{filename}.pstats')
                logger.info(result)
            if PAUSE:
                text = input('continue? ')
                if text:
                    break
        if PAUSE and text:
            break

if __name__ == '__main__':
    main()
