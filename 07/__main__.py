#!/usr/bin/env python3
import cProfile
import os

from tools.grid import Grid, GridCell
from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

def parse(my_input: list[str]) -> Grid:
    height = len(my_input)
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

def count_paths_to(cell: GridCell, grid: Grid, memo: dict[tuple[int,int], int]={}) -> int:
    if cell.pos() in memo:
        return memo[cell.pos()]
    logger.debug(repr(cell))
    if cell.value == '.':
        logger.trace('--0--')
        memo[cell.pos()] = 0
        return 0
    n = grid[cell.north()] if grid.in_bounds(cell.north()) else None
    e = grid[cell.east()] if grid.in_bounds(cell.east()) else None
    w = grid[cell.west()] if grid.in_bounds(cell.west()) else None
    logger.debug('  ', n,e,w)
    if n and n.value == 'S':
        logger.trace('    found S')
        memo[cell.pos()] = 1
        return 1

    paths_to = 0
    if n and n.value == '|':
        logger.trace('    north')
        paths_to += count_paths_to(n, grid, memo)
    if e and e.value == '^':
        logger.trace('    east')
        paths_to += count_paths_to(e, grid, memo)
    if w and w.value == '^':
        logger.trace('    west')
        paths_to += count_paths_to(w, grid, memo)

    memo[cell.pos()] = paths_to
    return paths_to
    
def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    data = parse(my_input)
    logger.debug(data)

    for row in range(1, data.height):
        for col in range(data.width):
            cell = data[col, row]
            above = data[cell.north()]
            if above.value in ('|', 'S'):
                if cell.value in ('.', '|'):
                    cell.value = '|'
                elif cell.value == '^':
                    data[cell.west()].value = '|'
                    data[cell.east()].value = '|'

    logger.debug(data)

    total = 0
    for col in range(data.width):
        total += count_paths_to(data[col, data.height-1], data)
    return total

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
