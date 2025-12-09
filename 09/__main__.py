#!/usr/bin/env python3
import cProfile
import os

import tools.colors as colors
from tools.grid import GridCell, Grid
from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

RED = colors.highlight(colors.Color.RED, 'R')
def parse(my_input: list[str]) -> Grid:
    cells: list[tuple[int, int]] = []
    width = 0
    height = 0
    for line in my_input:
        logger.trace(line)
        try:
            x,y = map(int, line.split(','))
            cells.append((x,y))
            width = max(width, x)
            height = max(height, y)
        except BaseException as e:
            logger.error(line)
            raise e
    result: Grid = Grid(width+1, height+1)
    for cell in cells:
        result.set_cell(cell[0], cell[1], RED)
    logger.trace(result)
    return result

def rect_area(cell1: GridCell, cell2: GridCell) -> int:
    return (abs(cell1.x - cell2.x) + 1) * (abs(cell1.y - cell2.y) + 1)

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    grid = parse(my_input)
    max_area = 0
    reds = grid.find(RED)
    for idx, cell1 in enumerate(reds[:-1]):
        for cell2 in reds[idx+1:]:
            area = rect_area(cell1, cell2)
            max_area = max(area, max_area)
    # 7146910476 - too high!?
    # 4771508457 ✅
    return max_area

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    data = parse(my_input)
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
