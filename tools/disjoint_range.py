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
        return
        unclean = True
        while unclean:
            to_remove = []
            to_add = []
            for i in range(len(self.ranges) - 1):
                r = self.ranges[i]
                start = r.start
                end = r.stop
                n = self.ranges[i+1]
                n_start = n.start
                n_end = n.stop
                if start == n_start:
                    to_add.append(range(start, max(end, n_end)))


                if n_start == start and n_end == end:
                    # duplicate
                    to_remove.append(i+1)
                elif n_start >= start and n_start <= end:
                    # next start overlaps with current start
                    to_remove.append(i)
                    to_remove.append(i+1)
                    to_add.append(range(start, n_end))

        self.ranges.sort(key=lambda x: x[0])

    def add(self, r: range):
        return self.add_old(r)
        self.ranges.append(r)
        self.cleanup()

    def add_old(self, r: range):
        logger.debug(r)
        start = r.start
        end = r.stop - 1
        contains_start = self.contains(start)
        contains_end = self.contains(end)

        if not contains_start and not contains_end:
            # completely disjoint
            # ??..??..start..end..??..??
            self.ranges.append(r)
            self.cleanup()
            logger.debug('completely disjoint, adding', r)
            return
        '''
        if contains_start and contains_end and self.contains((start + end)//2):
            logger.debug(f'{r} is completely within existing ranges')
            return
        '''

        logger.debug('modify ranges')
        new_start = start
        new_end = end

        new_ranges = []
        to_remove = []
        # assume sorted (since we keep it sorted)
        for i, existing_range in enumerate(self.ranges):
            e_start = existing_range.start
            e_end = existing_range.stop - 1
            update = False
            if new_start <= e_start and new_end >= e_end:
                # start1..start2..end2..end1
                new_ranges.append(range(new_start, new_end + 1))
                logger.debug(f'case 1: {r} + {existing_range} => {new_ranges[-1]}')
                to_remove.append(i)
                continue
            if existing_range.count(start) and existing_range.count(end):
                # start2..start1..end1..end2
                new_ranges.append(existing_range)
                logger.debug(f'case 2: {r} + {existing_range} => {new_ranges[-1]}')
                continue # skip this, it's already fully included
            if new_start <= e_start and existing_range.count(end):
                # start1..start2..end1..end2
                new_ranges.append(range(new_start, e_end + 1))
                logger.debug(f'case 3: {r} + {existing_range} => {new_ranges[-1]}')
                continue
                #logger.trace('updating end:')
                #new_end = e_start - 1
                #logger.trace(end, new_end)
                update = True
            if existing_range.count(start) and new_end >= e_end:
                # start2..start1..end2..end1
                new_ranges.append(range(e_start, new_end + 1))
                logger.debug(f'case 4: {r} + {existing_range} => {new_ranges[-1]}')
                continue
                #logger.trace('updating start:')
                #new_start = e_end + 1
                update = True

            new_ranges.append(existing_range)
            logger.debug(f'case 5: {r} + {existing_range} => {new_ranges[-1]}')

            '''
            if update:
                logger.trace('updating', r, 'because of', existing_range)
                logger.trace(new_start, new_end)
                logger.debug(r, '+', existing_range, '=>', range(new_start, new_end + 1))
            '''
        '''
        for i in to_remove:
            self.ranges.pop(i)
        if new_start <= new_end:
            if self.contains(new_start):
                logger.warn(f'{r} already exists in self, {new_start} found, start is {self.contains(start)} found?')
            new_r = range(new_start, new_end + 1)
            logger.debug('adding:',new_r)
            self.ranges.append(new_r)
        '''
        self.ranges = new_ranges
        self.cleanup()
        print(new_ranges)

    def __len__(self) -> int:
        # TODO - memoize
        count = 0
        for r in self.ranges:
            count += len(r)
        return count

