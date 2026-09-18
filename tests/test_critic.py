import pytest
from agentic_research.core.state import AgentState, EvidenceItem
from agentic_research.nodes.critic import CriticNode


def test_critic_flags_insufficient_evidence():
    state = AgentState(query="Quantum Computing Breakthroughs", max_cycles=2)
    state.evidence = [EvidenceItem(source_url="http://example.com", title="Title", content="Short", confidence=0.5)]

    critic = CriticNode(min_evidence_items=3)
    critic.execute(state)

    assert len(state.critique_history) == 1
    critique = state.critique_history[0]
    assert critique.passed is False
    assert len(critique.issues) >= 1
    assert state.cycle_count == 1
    assert len(state.plan) >= 1
