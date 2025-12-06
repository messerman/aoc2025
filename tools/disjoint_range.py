from .logger import DebugLogger as logger

class DisjointRange:
    def __init__(self, ranges: list[range] | None = None):
        self.ranges: list[range] = []
        list(map(lambda r: self.add(r), ranges or []))

    def count(self, value: int) -> int:
        total = 0
        for r in self.ranges:
            total += r.count(value)
        return total

    def contains(self, value: int) -> bool:
        return self.count(value) > 0

    def find_overlaps(self) -> list[tuple[range, range]]:
        self.ranges.sort(key = lambda x: x[0])
        result: list[tuple[range, range]] = []
        for i in range(len(self.ranges) - 1):
            r1 = self.ranges[i]
            for j in range(i+1, len(self.ranges)):
                r2 = self.ranges[j]
                if r2.start in r1 or r2.stop-1 in r1 or r1.start in r2 or r1.stop-1 in r2:
                    result.append((r1, r2))
        return result

    def cleanup(self):
        self.ranges.sort(key=lambda x: float(f'{x.start}.{x.stop}'))

    def add(self, r: range):
        logger.trace(r)
        start = r.start
        end = r.stop - 1
        contains_start = self.contains(start)
        contains_end = self.contains(end)

        if not contains_start and not contains_end:
            # completely disjoint
            # ??..??..start..end..??..??
            self.ranges.append(r)
            self.cleanup()
            logger.trace('completely disjoint, adding', r)
            return

        new_ranges = []
        # assume sorted (since we keep it sorted)
        for i, existing_range in enumerate(self.ranges):
            e_start = existing_range.start
            e_end = existing_range.stop - 1
            if start <= e_start and end >= e_end:
                # start1..start2..end2..end1
                new_ranges.append(range(start, end + 1))
                logger.trace(f'case 1: {r} + {existing_range} => {new_ranges[-1]}')
                continue
            if existing_range.count(start) and existing_range.count(end):
                # start2..start1..end1..end2
                new_ranges.append(existing_range)
                logger.trace(f'case 2: {r} + {existing_range} => {new_ranges[-1]}')
                continue # skip this, it's already fully included
            if start <= e_start and existing_range.count(end):
                # start1..start2..end1..end2
                new_ranges.append(range(start, e_end + 1))
                logger.trace(f'case 3: {r} + {existing_range} => {new_ranges[-1]}')
                continue
            if existing_range.count(start) and end >= e_end:
                # start2..start1..end2..end1
                new_ranges.append(range(e_start, end + 1))
                logger.trace(f'case 4: {r} + {existing_range} => {new_ranges[-1]}')
                continue

            new_ranges.append(existing_range)
            logger.trace(f'case 5: {r} + {existing_range} => {new_ranges[-1]}')

        self.ranges = new_ranges
        self.cleanup()

    def __len__(self) -> int:
        # TODO - memoize
        count = 0
        for r in self.ranges:
            count += len(r)
        return count

