#!/usr/bin/env python3
import cProfile
import math
import os

from tools.logger import DebugLogger as logger
from tools.graph3d import Graph3D
from tools.node3d import Node3D

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

def parse(my_input: list[str]) -> list[Node3D]:
    result: list[Node3D] = []
    for line in my_input:
        logger.trace(line)
        try:
            x,y,z = line.split(',')
            result.append(Node3D(int(x), int(y), int(z)))
        except BaseException as e:
            logger.error(line)
            raise e
    logger.trace(result)
    result.sort()
    return result

def solution1(my_input: list[str], realInput=False) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)

    distances = {}
    for idx,node in enumerate(data[:-1]):
        for other in data[idx + 1:]:
            d = node.distance_to(other)
            distances[d] = [node, other]

    num_to_count = 1000 if realInput else 10
    graph = Graph3D(data)
    for distance in sorted(distances)[:num_to_count]:
        a,b = distances[distance]
        graph.connect(a,b)

    biggest = list(reversed(sorted(map(len, graph.networks))))
    return math.prod(biggest[:3])

def solution2(my_input: list[str], realInput=False) -> int:
    global SOLUTION
    SOLUTION = 2
    data = parse(my_input)

    distances = {}
    for idx,node in enumerate(data[:-1]):
        for other in data[idx + 1:]:
            d = node.distance_to(other)
            distances[d] = [node, other]

    graph = Graph3D(data)
    result = -1
    for distance in sorted(distances):
        logger.debug(distance, len(graph.networks))
        a,b = distances[distance]
        graph.connect(a,b)
        if len(graph.networks) == 1:
            result = a.x * b.x
            break


    return result

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
                cProfile.run(f'result = solution{part}({lines}, {filename=="input"})', f'{part}-{filename}.pstats')
                logger.info(result)
            if PAUSE:
                text = input('continue? ')
                if text:
                    break
        if PAUSE and text:
            break

if __name__ == '__main__':
    main()
