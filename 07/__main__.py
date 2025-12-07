#!/usr/bin/env python3
import cProfile
import os

from tools.grid import Grid
from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

def parse(my_input: list[str]) -> Grid:
    height = len(my_input) - 1
    width = len(my_input[0].strip())
    result = Grid(width, height)
    for row,line in enumerate(my_input):
        logger.trace(line)
        try:
            for col,c in enumerate(line.strip()):
                result.set_cell(col, row, c)

        except BaseException as e:
            logger.error(line)
            raise e
    logger.trace(result)
    return result

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)
    logger.debug(data)
    splits = 0
    for row in range(1, data.height):
        for col in range(data.width):
            cell = data[col, row]
            above_val = data[cell.north()].value
            if above_val in ('|', 'S'):
                if cell.value in ('.', '|'):
                    cell.value = '|'
                elif cell.value == '^':
                    splits += 1
                    data[cell.west()].value = '|'
                    data[cell.east()].value = '|'
    logger.debug(data)

    return splits

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    data = parse(my_input)
    logger.debug(data)

    for row in range(1, data.height):
        for col in range(data.width):
            cell = data[col, row]
            above_val = data[cell.north()].value
            if above_val in ('|', 'S'):
                if cell.value in ('.', '|'):
                    cell.value = '|'
                    cell.counter += 1
                elif cell.value == '^':
                    data[cell.west()].value = '|'
                    data[cell.west()].counter += 1
                    
                    data[cell.east()].value = '|'
                    data[cell.east()].counter += 1

    logger.debug(data)
    for col in range(data.width):
        print(data.at((col, data.height-1)), end='')
    print()

    return -1 # TODO

result: int
def main():
    text = None
    for part in PARTS:
        logger.info(f"---- Part {part} ----")
        for file in FILES:
            filename = file.split('.', maxsplit=1)[0]
            logger.info(f'-- {file} --')
            with open('/'.join([PATH, file]), 'r', encoding='utf-8') as f:
                lines = f.read().strip().split('\n')
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
