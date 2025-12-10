#!/usr/bin/env python3
import cProfile
from collections import deque
import os

from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

class Machine:
    def __init__(self, goal_state: str, buttons: list[list[int]], joltage_requirement: list[int], state: int = 0):
        self.goal = int(goal_state.replace('.','0').replace('#','1'), 2)
        self.num_lights = len(goal_state)
        self.buttons = buttons
        bnum = lambda n,length: 10**(length-n-1)
        bnums = lambda nums,length: int(str(sum([bnum(n,length) for n in nums])),2)
        self.bnums = [bnums(button, self.num_lights) for button in buttons]
        logger.trace(self.bnums)
        self.joltage_requirement = joltage_requirement
        self.state = state
        self.states: dict[int, set[tuple[int,int]]] = {}

    @classmethod
    def get_state(cls, state: int, num_lights: int) -> str:
        return bin(state)[2:].zfill(num_lights).replace('0', '.').replace('1', '#')

    def __str__(self) -> str:
        return self.get_state(self.state, self.num_lights)

    def __repr__(self) -> str:
        return f'Machine({self.get_state(self.goal, self.num_lights)}, {self.buttons}, {self.joltage_requirement}, {self.state})'

    def push(self, button: int) -> bool:
        state = self.state ^ self.bnums[button]
        if state not in self.states:
            self.states[state] = set()
        self.states[state].add((self.state, button))
        self.state = state
        return self.state == self.goal

    def populate_states(self):
        for i in range(2**self.num_lights):
            self.state = i
            for button in range(len(self.buttons)):
                self.push(button)
        self.state = 0

    def goal_path(self) -> list[int]:
        to_visit: deque[list[int]] = deque([[self.goal]])
        visited: deque[tuple[int,int]] = deque()
        while to_visit:
            # logger.debug(len(to_visit), to_visit)
            path = to_visit.popleft()
            #logger.debug(f'  === {path} ===')
            target_state = path[0]
            #logger.debug(' ' * len(path), self.get_state(target_state, self.num_lights))
            possibilities = self.states[target_state]
            for s,b in possibilities:
                if (s,b) in visited:
                    logger.debug(f'({s},{b}) skipped')
                    continue
                visited.append((s,b))
                new_path = [s] + path
                if s == 0:
                    #logger.debug(b, self.get_state(s, self.num_lights))
                    return new_path
                #logger.debug(f'adding {new_path}')
                to_visit.append(new_path)
                
        return []

def parse(my_input: list[str]) -> list[Machine]:
    result: list[Machine] = []
    for line in my_input:
        logger.trace(line)
        try:
            goal_state = ''
            buttons: list[list[int]] = []
            joltage_requirement: list[int] = []
            for thing in line.split(' '):
                if thing[0] == '[':
                    goal_state = thing[1:-1]
                elif thing[0] == '(':
                    buttons.append([int(x) for x in thing[1:-1].split(',')])
                elif thing[0] == '{':
                    joltage_requirement = [int(x) for x in thing[1:-1].split(',')]
                else:
                    assert 'Should never get here!'

            result.append(Machine(goal_state, buttons, joltage_requirement))
        except BaseException as e:
            logger.error(line)
            raise e
    logger.trace(result)
    return result

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)
    logger.trace(data)
    #logger.debug('\n'.join(map(str, data)))
    #logger.info(max([x.num_lights for x in data]))
    for machine in data:
        machine.populate_states()
    counts = []
    for i,machine in enumerate(data):
        logger.debug(f'=== {repr(machine) } ===')
        logger.debug('paths to goal:', machine.states[machine.goal])
        path = machine.goal_path()
        logger.info(f'machine {i}/{len(data)-1}: {len(path)-1}: {path}')
        counts.append(len(path) - 1)
    # 512 ✅
    return sum(counts)

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
