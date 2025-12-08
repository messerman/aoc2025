from dataclasses import dataclass, field

from .logger import DebugLogger as logger
from .node3d import Node3D

@dataclass(frozen=True, order=True)
class Connection:
    weight: float = field(init=False)
    node1: Node3D
    node2: Node3D

    def __post_init__(self):
        object.__setattr__(self, 'weight', self.node1.distance_to(self.node2))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Connection) and ((self.node1 == other.node1 and self.node2 == other.node2) or self.node1 == other.node2 and self.node2 == other.node1)

class Graph3D:
    def __init__(self, nodes: list[Node3D] = [], connections: list[Connection] = []):
        self.nodes = nodes
        self.networks: list[set[Node3D]] = [set([node]) for node in self.nodes]
        self.connections: list[Connection] = []
        for connection in connections:
            self.connect(connection.node1, connection.node2)

    def connect(self, node1: Node3D, node2: Node3D):
        assert node1 in self.nodes and node2 in self.nodes
        connection = Connection(node1,node2)

        if connection in self.connections:
            return

        self.connections.append(connection)
        my_network: set[Node3D] = set()
        networks_to_remove: list[set[Node3D]] = []
        for network in self.networks:
            if node1 in network or node2 in network:
                my_network = my_network.union(network)
                networks_to_remove.append(network)

        if not my_network:
            my_network = set([node1,node2])
        for network in networks_to_remove:
            self.networks.remove(network)
        self.networks.append(my_network)
