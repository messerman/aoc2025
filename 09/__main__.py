#!/usr/bin/env python3
import cProfile
import os

from tools.graph3d import Graph3D
from tools.logger import DebugLogger as logger
from tools.node3d import Node3D

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

def parse(my_input: list[str]) -> Graph3D:
    result: Graph3D = Graph3D()
    for line in my_input:
        logger.trace(line)
        try:
            x,y = map(int, line.split(','))
            result.add_node(Node3D(x, y, 0))
        except BaseException as e:
            logger.error(line)
            raise e
    logger.trace(result)
    return result

def rect_area(node1: Node3D, node2: Node3D) -> int:
    assert node1.z == node2.z == 0
    return (abs(node1.x - node2.x) + 1) * (abs(node1.y - node2.y) + 1)

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    graph = parse(my_input)
    max_area = 0
    for idx, node1 in enumerate(graph.nodes[:-1]):
        for node2 in graph.nodes[idx+1:]:
            area = rect_area(node1, node2)
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
