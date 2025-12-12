#!/usr/bin/env python3
from collections import defaultdict, deque
import cProfile
import os

from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2]# if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

class ServerRack:
    def __init__(self, servers: dict[str, deque[str]]):
        self.output_map = defaultdict(deque, servers)
        self.input_map: dict[str, deque[str]] = defaultdict(deque)
        for source,destinations in servers.items():
            for destination in destinations:
                self.input_map[destination].append(source)
        self.paths: dict[tuple[str, str], set[tuple[str, ...]]] = defaultdict(set)

    def dfs(self, start_key: str = 'you', path: deque[str] = deque(), goal_key: str = 'out') -> list[deque[str]]:
        if start_key == goal_key or start_key not in self.output_map or not self.output_map[start_key]:
            return [path + deque([start_key])]
        paths: list[deque[str]] = []
        if start_key in path:
            return [] # should not happen, but safety precaution to avoid loops
        for s in self.output_map[start_key]:
            if s in path:
                # avoid loops
                continue
            for p in self.dfs(s, deque(path + deque([start_key])), goal_key):
                paths.append(p)
        return paths

    def populate_paths(self, key: str = 'out', terminators: set[str] = set(('you', 'svr'))):
        # populate itself
        self.paths[(key,key)] = {(key,)}
        #self.paths[(key,key)].add((key,))
        print(f'added: {key}')

        to_visit: deque[str] = deque((key,))
        visited: set[str] = set()
        while to_visit:
            print('.', end='', flush=True)
            server = to_visit.popleft()
            if server in visited:
                print(f'skipping {server}')
                continue
            if server in terminators:
                visited.add(server)
                continue
            for s in filter(lambda s: s not in visited, self.input_map[server]):
                print(f'server: {server}, s: {s}, to_visit: {len(to_visit)}')
                # for each server we haven't already visited
                to_visit.append(s)
                print(f'to_visit += {s}')
                for path in self.paths[(server, key)]:
                    #print('-', end='', flush=True)
                    # add each of its paths
                    new_path = ((s,) + path)
                    self.paths[(s, key)].add(new_path)
            visited.add(server)
            to_visit = deque(filter(lambda s: s not in visited, to_visit))

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

def solution1(my_input: list[str], _ = False) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)
    paths = data.dfs()
    for path in paths:
        logger.debug(path)
    # 523 ✅
    return len(paths)

def solution2(my_input: list[str], is_sample = False) -> int:
    global SOLUTION
    SOLUTION = 2
    if is_sample:
        my_input = open('/'.join([PATH, 'sample2.txt']), 'r', encoding='utf-8').read().strip().split('\n')
    data = parse(my_input)
    data.populate_paths('out')
    paths = data.paths[('svr', 'out')]
    print('\n'.join(map(str, paths)))
    required = set(['dac', 'fft'])
    valid_paths = list(filter(lambda path: set(path).intersection(required) == required, paths))
    print('-'*20)
    print('\n'.join(map(str, valid_paths)))
    return len(valid_paths)

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
                cProfile.run(f'result = solution{part}({lines}, {filename == "sample"})', f'{part}-{filename}.pstats')
                logger.info(result)
            if PAUSE:
                text = input('continue? ')
                if text:
                    break
        if PAUSE and text:
            break

if __name__ == '__main__':
    main()
