#!/usr/bin/env python3
import cProfile
import os

import tools.colors as colors
from tools.grid import GridCell, Grid
from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = -1
ACTIVE_FILE = ''

TIMING = True#False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

RED = colors.highlight(colors.Color.RED, 'R')
GREEN = colors.highlight(colors.Color.GREEN, 'G')

def parse(my_input: list[str]) -> Grid:
    reds: list[tuple[int, int]] = []
    greens: list[tuple[int, int]] = []
    width = 0
    height = 0
    x,y = map(int, my_input[-1].split(','))
    min_x = x
    min_y = y
    previous = (x,y)
    for line in my_input:
        logger.trace(line)
        try:
            x,y = map(int, line.split(','))
            reds.append((x,y))
            if True or SOLUTION == 2:
                if previous:
                    if previous[0] == x: # draw vertical line
                        for v in range(min(previous[1], y)+1, max(previous[1], y)):
                            greens.append((x,v))
                    if previous[1] == y: # draw horizontal line
                        for h in range(min(previous[0], x)+1, max(previous[0], x)):
                            greens.append((h,y))
                previous = ((x,y))
            width = max(width, x)
            height = max(height, y)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
        except BaseException as e:
            logger.error(line)
            raise e
    result: Grid = Grid(width+1, height+1)
    for cell in reds:
        result.set_cell(cell[0], cell[1], RED)
    for cell in greens:
        result.set_cell(cell[0], cell[1], GREEN)
    logger.trace(result)
    return result

def rect_area(cell1: GridCell, cell2: GridCell) -> int:
    return (abs(cell1.x - cell2.x) + 1) * (abs(cell1.y - cell2.y) + 1)

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    grid = parse(my_input)
    if ACTIVE_FILE == 'sample.txt':
        logger.debug(grid)
    max_area = 0
    reds = grid.find(RED)
    for idx, cell1 in enumerate(reds[:-1]):
        for cell2 in reds[idx+1:]:
            area = rect_area(cell1, cell2)
            max_area = max(area, max_area)
    # 7146910476 - too high
    # 4771508457 ✅ - 4,771,508,457
    return max_area

def value_at(grid: Grid, x: int, y: int, wall_index: dict[int, list[int]]) -> str:
    value = grid.value_at((x,y))
    if value in [GREEN, RED]:
        #print(x,y,value)
        return value
    #print(x,y,value, grid.is_point_enclosed_fast(x,y,wall_index))
    return GREEN if grid.is_point_enclosed_fast(x, y, wall_index) else value

def valid_rect(grid: Grid, rect: tuple[GridCell, GridCell], wall_index: dict[int, list[int]]) -> bool:
    #logger.debug(rect)
    x1 = min(rect[0].x, rect[1].x)
    x2 = max(rect[0].x, rect[1].x)

    y1 = min(rect[0].y, rect[1].y)
    y2 = max(rect[0].y, rect[1].y)

    for x in range(x1, x2+1):
        if value_at(grid, x, y1, wall_index) == '.':
            #logger.debug(f'  rejectedy1 at {x},{y1}, {grid.value_at((x, y1))}')
            return False
        if value_at(grid, x, y2, wall_index) == '.':
            #logger.debug(f'  rejectedy2 at {x},{y2}')
            return False
    for y in range(y1, y2+1):
        if value_at(grid, x1, y, wall_index) == '.':
            #logger.debug(f'  rejectedx1 at {x1},{y}')
            return False
        if value_at(grid, x2, y, wall_index) == '.':
            #logger.debug(f'  rejectedx2 at {x2},{y}')
            return False
    return True

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    grid = parse(my_input)
    if ACTIVE_FILE == 'sample.txt':
        logger.debug(grid)

    max_area = 0
    reds = grid.find(RED)
    logger.info(len(reds), 'reds')
    #logger.debug(reds)
    start = reds[0]
    wall_index = grid.build_wall_index([GREEN, RED])
    #print(wall_index)
    #print(grid.is_point_enclosed_fast(8, 3, wall_index))
    for red in reds:
        found = False
        for n in grid.neighbors_of(red):
            print(n)
            if n.value in [GREEN, RED]:
                continue
            if grid.is_point_enclosed_fast(n.x, n.y, wall_index):
                print('found one', n)
                start = n
                found = True
                break
        if found:
            break

        

    print(repr(start))
    #grid.span_fill(start, GREEN, [GREEN, RED])
    #logger.debug(grid)
    for idx, cell1 in enumerate(reds[:-1]):
        print(f'=== {idx} / {len(reds)} ===')
        for cell2 in reds[idx+1:]:
            print('.', end='', flush=True)
            area = rect_area(cell1, cell2)
            if area > max_area and valid_rect(grid, (cell1, cell2), wall_index):
                logger.info(f'updating max_area from {max_area} to {area}')
                max_area = max(area, max_area)

    # 4528112920 - too high (forgot to handle unbounded endpoints)
    # 281473873 - too low
    # 391893113
    # 1539809693 ✅

    return max_area

result: int
def main():
    global ACTIVE_FILE
    text = None
    for part in PARTS:
        logger.info(f"---- Part {part} ----")
        for file in FILES:
            ACTIVE_FILE = file
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
