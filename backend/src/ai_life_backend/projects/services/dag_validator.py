"""DAG (Directed Acyclic Graph) validation service."""

from uuid import UUID


class CycleDetectedError(Exception):
    """Raised when a cycle is detected in a dependency graph."""

    pass


class DagValidator:
    """Validates that dependency graphs are acyclic (DAG)."""

    def has_cycle(self, graph: dict[UUID, list[UUID]]) -> bool:
        """Check if graph contains a cycle using DFS.

        Args:
            graph: Adjacency list where keys are node IDs and values are
                   lists of dependent node IDs

        Returns:
            True if cycle exists, False otherwise
        """
        if not graph:
            return False

        visited: set[UUID] = set()
        rec_stack: set[UUID] = set()

        def dfs(node: UUID) -> bool:
            """Depth-first search to detect cycles."""
            visited.add(node)
            rec_stack.add(node)

            # Check all neighbors
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Back edge found - cycle detected
                    return True

            rec_stack.remove(node)
            return False

        # Check all nodes
        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True

        return False

    def validate(self, graph: dict[UUID, list[UUID]]) -> None:
        """Validate that graph is acyclic.

        Args:
            graph: Adjacency list to validate

        Raises:
            CycleDetectedError: If cycle is detected
        """
        if self.has_cycle(graph):
            cycle_path = self.find_cycle_path(graph)
            path_str = " -> ".join(str(n) for n in cycle_path) if cycle_path else "unknown"
            msg = f"Cycle detected in dependency graph: {path_str}"
            raise CycleDetectedError(msg)

    def find_cycle_path(self, graph: dict[UUID, list[UUID]]) -> list[UUID] | None:
        """Find and return a cycle path if one exists.

        Args:
            graph: Adjacency list

        Returns:
            List of node IDs forming a cycle, or None if no cycle
        """
        visited: set[UUID] = set()
        rec_stack: set[UUID] = set()
        parent: dict[UUID, UUID | None] = {}

        def dfs(node: UUID) -> UUID | None:
            """DFS that returns the node where cycle starts."""
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                parent[neighbor] = node
                if neighbor not in visited:
                    cycle_start = dfs(neighbor)
                    if cycle_start:
                        return cycle_start
                elif neighbor in rec_stack:
                    return neighbor

            rec_stack.remove(node)
            return None

        # Find cycle start
        cycle_start = None
        for node in graph:
            if node not in visited:
                cycle_start = dfs(node)
                if cycle_start:
                    break

        if not cycle_start:
            return None

        # Reconstruct cycle path
        path = [cycle_start]
        current = parent.get(cycle_start)
        while current and current != cycle_start:
            path.append(current)
            current = parent.get(current)
        path.append(cycle_start)

        return list(reversed(path))
