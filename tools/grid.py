import itertools
from collections import deque
from typing import Any, Optional, Type

from .position import Position

class GridCell(Position):
    def __init__(self, x: int, y: int, value: str):
        super().__init__(x, y)
        self.value = value
        self.counter = 0
        self.path = ''

    def __repr__(self):
        return f'({self.x},{self.y}):{self.value}'
    
    def __str__(self):
        return self.value

    def pos(self):
        return self.to_tuple()

class Grid:
    def __init__(self, width: int, height: int, default='.', cell_type: Type[GridCell] = GridCell):
        self.cells: dict[tuple[int, int], GridCell] = {}
        self.width = width
        self.height = height
        self.default = default
        self.cell_type = cell_type

    @classmethod
    def from_lists(cls, gridcells:list[list[GridCell]], width=-1, height=-1, default='.') -> 'Grid':
        if width == -1:
            width = max(map(lambda cell: cell.x, itertools.chain.from_iterable(gridcells)))
        if height == -1:
            height = max(map(lambda cell: cell.y, itertools.chain.from_iterable(gridcells)))

        grid = cls(width, height, default)
        for l in gridcells:
            for cell in l:
                grid.set_cell(cell.x, cell.y, cell.value)

        return grid

    def __str__(self) -> str:
        output: list[str] = ['']
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                row += self.at((x, y)).value
            output.append(row)
        return'\n'.join(output)

    def __hash__(self) -> int:
        return hash(str(self))

    def at(self, pos: tuple[int, int]) -> GridCell:
        if self.in_bounds(pos) and pos not in self.cells:
            self.set_cell(pos[0], pos[1], self.default)
        return self.cells[pos]
    
    def value_at(self, pos: tuple[int, int]) -> str:
        if self.in_bounds(pos) and pos not in self.cells:
            return self.default
        return self.cells[pos].value

    def __getitem__(self, index: tuple[int, int]) -> GridCell:
        return self.at(index)

    def set_cell(self, x: int, y: int, value: str) -> bool:
        if not self.in_bounds((x, y)):
            return False
        self.cells[(x, y)] = self.cell_type(x, y, value)
        return True

    def find(self, value: str) -> list[GridCell]:
        result: list[GridCell] = []
        for cell in self.cells.values():
            if cell.value == value:
                result.append(cell)
        return result

    def groups(self, include_values: Optional[list[str]] = None) -> list[list[GridCell]]:
        visited: set[GridCell] = set()
        to_visit: set[GridCell] = set(self.cells.values())

        groups: list[list[GridCell]] = []
        while to_visit:
            cell = to_visit.pop()

            groups.append(self.connected_group(cell, include_values or [cell.value]))
            visited = visited.union(groups[-1])

            to_visit = to_visit.difference(visited)
        return groups

    def connected_group(self, starting: GridCell, include_values: list[str]) -> list[GridCell]:
        visited: dict[GridCell, bool] = {}
        to_visit: list[GridCell] = [starting]
        while to_visit:
            cell = to_visit.pop()
            if cell.value not in include_values:
                continue
            visited[cell] = True
            for neighbor in cell.neighbors():
                #self[neighbor].value == starting.value
                if self.in_bounds(neighbor) and self[neighbor] not in visited and self[neighbor].value in include_values:
                    to_visit.append(self[neighbor])

        # TODO - can this be simplified to use sets? Do we even need the filter?
        return list(map(lambda item: item[0], filter(lambda item: item[1], visited.items())))

    def move(self, cell: GridCell, pos: tuple[int, int], leave_behind='.') -> bool:
        old_pos = cell.to_tuple()
        cell.move(pos)
        is_in_bounds = self.in_bounds(pos)
        if not is_in_bounds:
            self.cells.pop(old_pos) # remove from our cells
        self.set_cell(old_pos[0], old_pos[1], leave_behind) # leave behind the right value

        return True

    def in_bounds(self, pos: tuple[int, int]) -> bool:
        x,y = pos
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def search_from(self, x: int, y: int, length: int, diagonals = False) -> list[str]:
        cell = self[(x,y)]
        result = []
        directions = [GridCell.north, GridCell.east, GridCell.south, GridCell.west]
        if diagonals:
            directions.extend([GridCell.nw, GridCell.ne, GridCell.sw, GridCell.se])
        for direction in directions:
            res = []
            next_cell = cell
            for _ in range(length):
                res.append(next_cell.value)
                try:
                    next_cell = self.at(direction(next_cell))
                except:
                    break
            if len(res) == length:
                result.append(''.join(res))
        return result

    def neighbors_of(self, cell: GridCell, diagonals = False) -> list[GridCell]:
        neighbors = cell.neighbors(diagonals)
        return [self.at(n) for n in neighbors if self.in_bounds(n)]

    def is_enclosed(self, cell: GridCell, wall_values: list[str]) -> bool:
        x_walls = 0
        for x in range(0, cell.x):
            new_pos = (x, cell.y)
            if not self.in_bounds(new_pos):
                break
            x_walls += 1 if self.value_at(new_pos) in wall_values else 0
        return x_walls % 2 != 0

    def is_point_enclosed(self, x: int, y: int, wall_values: list[str]) -> bool:
        """Check if a point is enclosed by walls using ray casting.

        Works efficiently on sparse grids by only checking existing wall cells.
        Uses horizontal ray from point to negative infinity, counting wall crossings.
        Odd crossings = inside, even = outside.
        """
        # Only check walls that exist and are on the same row, to the left
        wall_count = 0
        for pos, cell in self.cells.items():
            if cell.value in wall_values and pos[1] == y and pos[0] < x:
                wall_count += 1

        return wall_count % 2 == 1

    def build_wall_index(self, wall_values: list[str]) -> dict[int, list[int]]:
        """Build an index of wall segment END positions by y-row for faster point-in-polygon checks.

        Returns: dict mapping y -> sorted list of segment end x-coordinates
        Contiguous wall cells are merged into segments, storing only the rightmost x of each segment.
        """
        # First collect all wall positions
        temp_walls: dict[int, list[int]] = {}
        for pos, cell in self.cells.items():
            if cell.value in wall_values:
                y = pos[1]
                if y not in temp_walls:
                    temp_walls[y] = []
                temp_walls[y].append(pos[0])

        # Convert to segment end positions
        wall_index: dict[int, list[int]] = {}
        for y, x_positions in temp_walls.items():
            x_positions.sort()
            segment_ends = []

            if x_positions:
                segment_end = x_positions[0]

                for i in range(1, len(x_positions)):
                    if x_positions[i] == segment_end + 1:
                        # Extend current segment
                        segment_end = x_positions[i]
                    else:
                        # Save current segment end and start new one
                        segment_ends.append(segment_end)
                        segment_end = x_positions[i]

                # Don't forget the last segment
                segment_ends.append(segment_end)

            wall_index[y] = segment_ends

        return wall_index

    def is_point_enclosed_fast(self, x: int, y: int, wall_index: dict[int, list[int]]) -> bool:
        """Fast point-in-polygon check using pre-built wall index.

        Use build_wall_index() first, then call this repeatedly for many points.
        O(log s) per check where s is number of wall segments on the row.
        """
        if y not in wall_index:
            return False

        import bisect
        segment_ends = wall_index[y]

        # Count segments where end < x using binary search
        # bisect_left gives us the insertion point, which equals the count of segments ending before x
        segment_count = bisect.bisect_left(segment_ends, x)

        return segment_count % 2 == 1

    def _fill(self, start: GridCell, filled: set[GridCell], fill_value: str, wall_values: list[str]) -> list[GridCell]:
        if start in filled or start.value in wall_values:
            return list()
        start.value = fill_value
        filled.update([start])
        return self.neighbors_of(start)

    def fill(self, start: GridCell, fill_value: str, wall_values: list[str]) -> None:
        to_fill: set[GridCell] = set([start])
        filled: set[GridCell] = set()
        while len(to_fill) > 0:
            print(len(to_fill))
            cell = to_fill.pop()
            to_fill = to_fill.union(self._fill(cell, filled, fill_value, wall_values)).difference(filled)

    def span_fill(self, start: GridCell, fill_value: str, wall_values: list[str]) -> None:
        """Efficient flood fill using scanline/span algorithm.

        Fills horizontal spans at once, then checks rows above/below for new spans.
        More efficient than cell-by-cell flood fill.
        """
        if start.value in wall_values:
            return

        # Queue of spans to process: (y, x_left, x_right, direction)
        # direction: 1 for down, -1 for up
        spans: deque[tuple[int, int, int, int]] = deque()

        # Start with initial span
        x_left, x_right = self._fill_span(start.y, start.x, fill_value, wall_values)
        spans.append((start.y, x_left, x_right, 1))  # scan down
        spans.append((start.y, x_left, x_right, -1)) # scan up

        while spans:
            y, x_left, x_right, dy = spans.popleft()

            # Check the next row in direction dy
            next_y = y + dy
            if not (0 <= next_y < self.height):
                continue

            # Scan this row for unfilled spans
            x = x_left
            while x <= x_right:
                # Skip over filled cells and walls
                while x <= x_right and (self.at((x, next_y)).value == fill_value or
                                       self.at((x, next_y)).value in wall_values):
                    x += 1

                if x > x_right:
                    break

                # Found start of new span - fill it
                span_left, span_right = self._fill_span(next_y, x, fill_value, wall_values)

                # Add new spans to check rows above/below this span
                spans.append((next_y, span_left, span_right, dy))

                # Also check in opposite direction for this new span
                spans.append((next_y, span_left, span_right, -dy))

                x = span_right + 1

    def _fill_span(self, y: int, x_start: int, fill_value: str, wall_values: list[str]) -> tuple[int, int]:
        """Fill a horizontal span and return its left and right x coordinates."""
        # Fill left from starting point
        x_left = x_start
        while x_left > 0 and self.at((x_left - 1, y)).value not in wall_values and \
              self.at((x_left - 1, y)).value != fill_value:
            x_left -= 1

        # Fill right from starting point
        x_right = x_start
        while x_right < self.width - 1 and self.at((x_right + 1, y)).value not in wall_values and \
              self.at((x_right + 1, y)).value != fill_value:
            x_right += 1

        # Actually fill the span
        for x in range(x_left, x_right + 1):
            self.at((x, y)).value = fill_value

        return x_left, x_right
