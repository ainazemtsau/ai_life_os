"""Tests for DAG (Directed Acyclic Graph) validation."""

import pytest
from uuid import uuid4

from ai_life_backend.projects.services.dag_validator import (
    DagValidator,
    CycleDetectedError,
)


class TestDagValidator:
    """Test DAG validation for dependencies."""

    def test_empty_graph_is_valid(self):
        """Test that empty graph has no cycles."""
        validator = DagValidator()
        assert validator.has_cycle({}) is False

    def test_single_node_no_cycle(self):
        """Test single node with no dependencies."""
        validator = DagValidator()
        node_id = uuid4()
        graph = {node_id: []}
        assert validator.has_cycle(graph) is False

    def test_simple_chain_no_cycle(self):
        """Test A -> B -> C (no cycle)."""
        validator = DagValidator()
        a, b, c = uuid4(), uuid4(), uuid4()
        graph = {
            a: [b],
            b: [c],
            c: [],
        }
        assert validator.has_cycle(graph) is False

    def test_simple_cycle_detected(self):
        """Test A -> B -> A (cycle)."""
        validator = DagValidator()
        a, b = uuid4(), uuid4()
        graph = {
            a: [b],
            b: [a],
        }
        assert validator.has_cycle(graph) is True

    def test_self_loop_detected(self):
        """Test A -> A (self-loop)."""
        validator = DagValidator()
        a = uuid4()
        graph = {a: [a]}
        assert validator.has_cycle(graph) is True

    def test_complex_cycle_detected(self):
        """Test A -> B -> C -> D -> B (cycle in middle)."""
        validator = DagValidator()
        a, b, c, d = uuid4(), uuid4(), uuid4(), uuid4()
        graph = {
            a: [b],
            b: [c],
            c: [d],
            d: [b],  # cycle back to B
        }
        assert validator.has_cycle(graph) is True

    def test_diamond_shape_no_cycle(self):
        """Test diamond: A -> B,C; B,C -> D (no cycle)."""
        validator = DagValidator()
        a, b, c, d = uuid4(), uuid4(), uuid4(), uuid4()
        graph = {
            a: [b, c],
            b: [d],
            c: [d],
            d: [],
        }
        assert validator.has_cycle(graph) is False

    def test_validate_raises_on_cycle(self):
        """Test that validate() raises CycleDetectedError."""
        validator = DagValidator()
        a, b = uuid4(), uuid4()
        graph = {
            a: [b],
            b: [a],
        }
        with pytest.raises(CycleDetectedError, match="Cycle detected"):
            validator.validate(graph)

    def test_validate_passes_on_dag(self):
        """Test that validate() passes for valid DAG."""
        validator = DagValidator()
        a, b, c = uuid4(), uuid4(), uuid4()
        graph = {
            a: [b],
            b: [c],
            c: [],
        }
        validator.validate(graph)  # Should not raise

    def test_find_cycle_path(self):
        """Test that cycle path can be identified."""
        validator = DagValidator()
        a, b, c = uuid4(), uuid4(), uuid4()
        graph = {
            a: [b],
            b: [c],
            c: [a],  # cycle: a -> b -> c -> a
        }
        cycle_path = validator.find_cycle_path(graph)
        assert cycle_path is not None
        # Should contain the cycle participants
        assert a in cycle_path or b in cycle_path or c in cycle_path
