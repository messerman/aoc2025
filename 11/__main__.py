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

    def count_paths_with_required(self, start: str, goal: str, required: set[str]) -> int:
        ########
        # NOTE # this function was generated using Claude Code, to replace my reverse BFS algo that wasn't efficient enough
        ########
        """
        Count paths from start to goal that pass through ALL nodes in required set.
        Uses DP with state: (current_node, frozenset of required nodes visited)
        """
        # State: (node, visited_required_nodes) -> count of paths
        from functools import lru_cache

        required_frozen = frozenset(required)

        @lru_cache(maxsize=None)
        def count(node: str, visited_required: frozenset) -> int:
            # Update visited_required if current node is in required set
            if node in required_frozen:
                visited_required = visited_required | frozenset([node])

            # Base case: reached goal
            if node == goal:
                # Only count if we've visited all required nodes
                return 1 if visited_required == required_frozen else 0

            # No outgoing edges
            if node not in self.output_map or not self.output_map[node]:
                return 0

            # Recursive case: sum paths through all neighbors
            total = 0
            for neighbor in self.output_map[node]:
                total += count(neighbor, visited_required)

            return total

        return count(start, frozenset())

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

    # Count paths from 'svr' to 'out' that include both 'dac' and 'fft'
    required = set(['dac', 'fft'])
    count = data.count_paths_with_required('svr', 'out', required)

    logger.info(f'Paths from svr to out containing both dac and fft: {count}')
    # 517315308154944 ✅ *(had Claude help)
    return count

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
