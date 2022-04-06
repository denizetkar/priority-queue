import math

from priority_queue import PriorityQueue


class EdgePointer:
    def __init__(self, idx, weight):
        self.idx = idx
        self.weight = weight

    def __hash__(self) -> int:
        return hash(self.idx)

    def __eq__(self, other: "EdgePointer") -> bool:
        return self.idx == other.idx

    def __repr__(self) -> str:
        return repr((self.idx, self.weight))


class Graph:
    def __init__(self, n):
        self.adjacencies = [set() for _ in range(n)]

    def connect(self, i, j, weight=6):
        self.adjacencies[i].add(EdgePointer(j, weight))
        self.adjacencies[j].add(EdgePointer(i, weight))

    def dijkstra_shortest_dist(self, start_idx):
        dists = [float("inf")] * len(self.adjacencies)
        dists[start_idx] = 0
        visited_nodes = set()
        node_q = PriorityQueue([(dist, node_idx) for node_idx, dist in enumerate(dists)])
        while len(node_q) > 0:
            dist, node_idx = node_q.pop()
            dists[node_idx] = dist
            visited_nodes.add(node_idx)
            neighbors = self.adjacencies[node_idx]
            for neighbor in neighbors:
                if neighbor.idx in visited_nodes:
                    continue
                if dists[node_idx] + neighbor.weight < dists[neighbor.idx]:
                    node_q.update_elem(neighbor.idx, (dists[node_idx] + neighbor.weight, neighbor.idx))
                    dists[neighbor.idx] = dists[node_idx] + neighbor.weight
        return dists

    def find_all_distances(self, start_idx):
        shortest_dists = self.dijkstra_shortest_dist(start_idx)
        for i in range(len(shortest_dists)):
            if math.isinf(shortest_dists[i]):
                shortest_dists[i] = -1
        print(" ".join(str(dist) for dist in shortest_dists[:start_idx] + shortest_dists[start_idx + 1 :]))

    def __repr__(self) -> str:
        return repr(self.adjacencies)
