#!/usr/bin/env python3
from collections import defaultdict, deque
import cProfile
import os

from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

class ServerRack:
    def __init__(self, servers: dict[str, deque[str]]):
        self.output_map = defaultdict(deque, servers)
        self.input_map: dict[str, deque[str]] = defaultdict(deque)
        for source,destinations in servers.items():
            for destination in destinations:
                self.input_map[destination].append(source)

    def dfs(self, start_key: str = 'you', path: deque[str] = deque()) -> list[deque[str]]:
        if start_key not in self.output_map or not self.output_map[start_key]:
            return [path + deque([start_key])]
        paths: list[deque[str]] = []
        if start_key in path:
            return [] # should not happen, but safety precaution to avoid loops
        for s in self.output_map[start_key]:
            if s in path:
                # avoid loops
                continue
            for p in self.dfs(s, deque(path + deque([start_key]))):
                paths.append(p)
        return paths

def parse(my_input: list[str]) -> ServerRack:
    result: dict[str, deque[str]] = {}
    for line in my_input:
        logger.trace(line)
        try:
            servers = deque(line.split(' '))
            source = servers.popleft()[:-1] # lop off the :
            result[source] = servers
        except BaseException as e:
            logger.error(line)
            raise e
    logger.trace(result)
    return ServerRack(result)

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)
    paths = data.dfs()
    for path in paths:
        logger.debug(path)
    # 523 ✅
    return len(paths)

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
