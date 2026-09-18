import pytest
from agentic_research.core.graph import ResearchGraph
from agentic_research.core.state import AgentStatus


def test_research_graph_end_to_end():
    graph = ResearchGraph(max_cycles=2)
    state, trace = graph.run("Direct Preference Optimization benchmarks")

    assert state.status == AgentStatus.COMPLETED
    assert len(state.evidence) >= 1
    assert state.final_report is not None
    assert "Direct Preference Optimization" in state.final_report
    assert len(trace.steps) >= 3
    assert trace.final_status == "COMPLETED"
    assert trace.total_tokens > 0


def test_trace_serialization():
    graph = ResearchGraph(max_cycles=1)
    state, trace = graph.run("RAG hallucination reduction")
    data = trace.to_dict()

    assert data["query"] == "RAG hallucination reduction"
    assert "steps" in data
    assert len(data["steps"]) >= 3
    assert data["total_duration_sec"] >= 0.0
