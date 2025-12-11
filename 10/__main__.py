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
        self.jnum = sum([joltage_requirement[i] * 1000**(len(joltage_requirement)-i-1) for i in range(len(joltage_requirement))])
        self.jbuttons = [sum([1000**b for b in button]) for button in buttons]
        print(self.jnum)

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
            path = to_visit.popleft()
            target_state = path[0]
            possibilities = self.states[target_state]
            for s,b in possibilities:
                if (s,b) in visited:
                    logger.debug(f'({s},{b}) skipped')
                    continue
                visited.append((s,b))
                new_path = [s] + path
                if s == 0:
                    return new_path
                to_visit.append(new_path)
                
        return []

    def joltage_valid(self, joltage: tuple[int, ...]) -> bool:
        for i in range(len(self.joltage_requirement)):
            if joltage[i] < 0 or joltage[i] > self.joltage_requirement[i]:
                return False
        return True

    '''
    def joltage_path(self) -> list[int]:
        initial_joltage_state = tuple(self.joltage_requirement)
        to_visit: deque[tuple[tuple[int, ...], list[int]]] = deque()
        to_visit.append((initial_joltage_state, []))
        visited: dict[tuple[int, ...], bool] = {}
        zero_joltage = tuple([0 for _ in self.joltage_requirement])
        while len(to_visit) > 0:
            logger.debug(len(to_visit))#, to_visit)
            #logger.debug('.', end='', flush=True)
            jstate,path = to_visit.popleft()
            visited[jstate] = True
            for idx in range(len(self.buttons)):
                update = tuple(self.decrement_joltages(jstate, idx))
                new_path = [idx] + path
                if update == zero_joltage:
                    return path
                if not update in visited and self.joltage_valid(update):
                    to_visit.append((update, new_path))
                    logger.debug(f'adding {update}')
                elif not self.joltage_valid(update):
                    logger.debug(f'invalid: {update}')
                else:
                    logger.debug(f'already have: {update}')
        return []

    def joltage_stages(self):
        zero_joltage = tuple([0 for _ in self.joltage_requirement])
        to_visit: deque[tuple[tuple[int, ...], list[int]]] = deque()
        to_visit.append((zero_joltage, []))
        visited: dict[tuple[int, ...], list[list[int]]] = {}
        while len(to_visit) > 0:
            logger.debug(len(to_visit))#, to_visit)
            jstate,path = to_visit.popleft()
            if not jstate in visited:
                visited[jstate] = []
            visited[jstate].append(path)
            for idx in range(len(self.buttons)):
                update = tuple(self.increment_joltages(jstate, idx))
                new_path = path + [idx]
                if not self.joltage_valid(update):
                    #logger.debug(f'invalid: {update}')
                    pass
                elif update in visited:
                    #logger.debug(f'already have {update}')
                    pass
                else:
                    #logger.debug(f'adding {update}')
                    to_visit.append((update, new_path))
        print(visited)
    '''
    def joltage_stages(self):
        jstages = {}
        for num in range(1000):#self.jnum): # way too big
            print('.', end='', flush=True)
            for j,button in enumerate(self.jbuttons):
                new_j = num + button
                if new_j not in jstages:
                    jstages[new_j] = []
                jstages[new_j].append((num, j))
            if self.jnum in jstages:
                break
        print(jstages[self.jnum])



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
    logger.trace(data)
    for machine in data:
        machine.populate_states()
    data = parse(my_input)
    counts = []
    for i,machine in enumerate(data):
        logger.debug(f'=== Machine({i}/{len(data)-1}) -- {repr(machine)} ===')
        machine.joltage_stages()
        #logger.debug('paths to goal:', machine.states[machine.goal])
        '''
        path = machine.joltage_path()
        logger.info(f'machine {i}/{len(data)-1}: {len(path)-1}: {path}')
        counts.append(len(path) - 1)
        '''

        break

    return sum(counts)

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
