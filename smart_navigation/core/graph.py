"""Graph model for Smart Navigation System."""


class Graph:
    """Undirected graph represented by adjacency list."""

    def __init__(self):
        self.adj: dict[str, dict[str, dict[str, float]]] = {}

    def add_node(self, node: str) -> None:
        node = node.strip()
        if not node:
            return
        if node not in self.adj:
            self.adj[node] = {}

    def add_edge(self, source: str, target: str, distance: float = 1.0, time: float = 1.0) -> None:
        source = source.strip()
        target = target.strip()
        if not source or not target:
            return

        self.add_node(source)
        self.add_node(target)

        self.adj[source][target] = {"distance": distance, "time": time}
        self.adj[target][source] = {"distance": distance, "time": time}

    def has_node(self, node: str) -> bool:
        return node in self.adj

    def neighbors(self, node: str) -> list[str]:
        return list(self.adj.get(node, {}).keys())

    def get_edge_data(self, source: str, target: str) -> dict[str, float]:
        return self.adj.get(source, {}).get(target, {"distance": 1.0, "time": 1.0})

    def to_display_string(self) -> str:
        if not self.adj:
            return "(graph kosong)"

        lines = []
        for node in sorted(self.adj.keys()):
            neighbors_info = []
            for neighbor in sorted(self.adj[node].keys()):
                data = self.adj[node][neighbor]
                neighbors_info.append(f"{neighbor}(d:{data['distance']}, t:{data['time']})")
            neighbors = ", ".join(neighbors_info)
            lines.append(f"{node} -> [{neighbors}]")
        return "\n".join(lines)
