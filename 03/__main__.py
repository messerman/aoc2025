#!/usr/bin/env python3
import cProfile
import os

PARTS = [1, 2]
PATH = os.path.dirname(os.path.realpath(__file__))
FILES = ['sample.txt', 'input.txt']
PAUSE = False
SOLUTION = 1

def parse(my_input: list[str]) -> list[list[int]]:
    result: list[list[int]] = []
    for line in my_input:
        if not line:
            continue
        try:
            result.append([int(c) for c in line])
        except BaseException as e:
            print(line)
            raise e
    return result

def find_big(nums: list[int], size: int = 2) -> list[int]:
    assert size <= len(nums)
    if len(nums) <= 0 or len(nums) == size:
        return nums
    if size == 0:
        return []

    biggest = max(nums[:len(nums) - (size-1)])
    idx = nums.index(biggest)
    bigs = find_big(nums[idx+1:], size - 1)
    bigs.insert(0, biggest)

    assert len(bigs) == size
    return bigs

def solution1(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 1
    data = parse(my_input)

    total = 0
    for nums in data:
        bigs = find_big(nums)
        total += int(''.join(map(str, bigs)))

    return total

def solution2(my_input: list[str]) -> int:
    global SOLUTION
    SOLUTION = 2
    data = parse(my_input)

    total = 0
    for nums in data:
        bigs = find_big(nums, 12)
        total += int(''.join(map(str, bigs)))

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
