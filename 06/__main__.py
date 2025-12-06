#!/usr/bin/env python3
import cProfile
import math
import os

from tools.logger import DebugLogger as logger

PATH = os.path.dirname(os.path.realpath(__file__))
SOLUTION = 1

TIMING = False
PARTS = [2] if TIMING else [1, 2]
FILES = ['input.txt'] if TIMING else ['sample.txt', 'input.txt']
PAUSE = not TIMING

class SquidMath:
    def __init__(self, operation: str, operands: list[int]):
        assert operation in ['*', '+']
        self.op_code = operation
        self.operation = sum if operation == '+' else math.prod
        self.operands = operands

    @classmethod
    def create(cls, operation: str, columns: list[str]) -> 'SquidMath':
        operands: list[int] = []
        for column in reversed(columns):
            logger.debug(column)
            operands.append(int(column))
            logger.debug(operands[-1])
        return cls(operation, operands)
    def __str__(self) -> str:
        return self.op_code.join(map(str, self.operands))

    def __repr__(self) -> str:
        return str(self)

    def calculate(self) -> int:
        return self.operation(self.operands)

def parse(my_input: list[str]) -> list[SquidMath]:
    result: list[SquidMath] = []
    my_input = list(filter(lambda line: line, my_input))
    if SOLUTION == 1:
        columns: list[list[str]] = [[] for _ in range(len(my_input[0].split()))]
    else:
        columns: list[list[str]] = [[] for _ in list(my_input[0])]
    for line in my_input:
        logger.trace(line)
        if not line:
            continue
        try:
            chars = line.split() if SOLUTION == 1 else list(line)
            chars += ' ' * (len(columns) - len(chars))
            column = 0
            for column,val in enumerate(chars):
                columns[column].append(val)

        except BaseException as e:
            logger.error(line)
            raise e
    logger.debug(columns)

    if SOLUTION==1:
        for column in columns:
            result.append(SquidMath(column[-1], list(map(int, column[:-1]))))
            logger.trace(result[-1])
    else:
       operation = ''
       nums: list[int] = []
       for column in columns:
           if len(list(filter(lambda c: c != ' ', column))) == 0:
               result.append(SquidMath(operation, nums))
               logger.trace(result[-1])
               nums = []
               operation = ''
               continue

           operation = operation if column[-1] == ' ' else column[-1]
           num = int(''.join(column[:-1]))
           nums.append(num)
       result.append(SquidMath(operation, nums))
       logger.trace(result[-1])
    
    logger.trace(result)
    return result

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)
    logger.debug(data)
    return sum(map(lambda x: x.calculate(), data))

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    data = parse(my_input)
    logger.debug(data)
    return sum(map(lambda x: x.calculate(), data))

result: int
def main():
    text = None
    for part in PARTS:
        logger.info(f"---- Part {part} ----")
        for file in FILES:
            filename = file.split('.', maxsplit=1)[0]
            logger.info(f'-- {file} --')
            with open('/'.join([PATH, file]), 'r', encoding='utf-8') as f:
                lines = f.read().split('\n')
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
