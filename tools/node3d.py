import math
from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

@dataclass(frozen=True, order=True)
class Node3D:
    sort_index: float = field(init=False, repr=False)
    x: int
    y: int
    z: int
    value: Any = None

    ORIGIN: ClassVar['Node3D']

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.distance_to())

    def __str__(self) -> str:
        value = f':{self.value}' if self.value else ''
        return f'({self.x}, {self.y}, {self.z}){value}'

    def distance_to(self, other: Optional['Node3D'] = None) -> float:
        if not other and (self.x == 0 and self.y == 0 and self.z == 0):
            return 0
        other = other or self.ORIGIN
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

Node3D.ORIGIN = Node3D(0, 0, 0)
