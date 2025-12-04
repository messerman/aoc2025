#!/usr/bin/env python3
import cProfile
import os

from tools.grid import Grid, GridCell

PARTS = [1, 2]
PATH = os.path.dirname(os.path.realpath(__file__))
FILES = ['sample.txt', 'input.txt']
PAUSE = True
SOLUTION = 1

def parse(my_input: list[str]) -> Grid:
    grid = Grid(len(my_input[0]), len(my_input)-1)
    for y,line in enumerate(my_input):
        try:
            if not line:
                continue
            for x,c in enumerate(list(line)):
                grid.set_cell(x, y, c)
        except BaseException as e:
            print(line)
            raise e
    return grid

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    grid = parse(my_input)
    cells: list[GridCell] = []
    for cell in filter(lambda c: c.value == '@', grid.cells.values()):
        neighbors = cell.neighbors(True)
        rolls = [c for c in neighbors if grid.in_bounds(c) and grid[c].value == '@']
        #print(repr(cell), rolls)
        if len(rolls) < 4:
            cells.append(cell)

    return len(cells)

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    grid = parse(my_input)
    total = 0
    while True:
        cells: list[GridCell] = []
        for cell in filter(lambda c: c.value == '@', grid.cells.values()):
            neighbors = cell.neighbors(True)
            rolls = [c for c in neighbors if grid.in_bounds(c) and grid[c].value == '@']
            if len(rolls) < 4:
                cells.append(cell)
        if len(cells) == 0:
            break
        total += len(cells)
        for cell in cells:
            cell.value = '.'

    return total

result: int
def main():
    text = None
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
