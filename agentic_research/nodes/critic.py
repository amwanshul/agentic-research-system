from agentic_research.core.state import AgentState, CritiqueResult, AgentStatus, ResearchSubtask


class CriticNode:
    def __init__(self, min_evidence_items: int = 2):
        self.min_evidence_items = min_evidence_items

    def execute(self, state: AgentState) -> AgentState:
        state.status = AgentStatus.REFLECTING
        issues = []
        suggested_queries = []

        if len(state.evidence) < self.min_evidence_items:
            issues.append(f"Insufficient evidence count: {len(state.evidence)} < {self.min_evidence_items}")
            suggested_queries.append(f"{state.query} empirical study analysis")

        avg_confidence = (
            sum(e.confidence for e in state.evidence) / len(state.evidence)
            if state.evidence else 0.0
        )
        if avg_confidence < 0.70:
            issues.append("Low average evidence confidence score")
            suggested_queries.append(f"{state.query} benchmark verification")

        passed = len(issues) == 0 or (state.cycle_count >= state.max_cycles)
        factuality_score = max(0.0, 1.0 - (len(issues) * 0.25))

        critique = CritiqueResult(
            passed=passed,
            factuality_score=factuality_score,
            issues=issues,
            suggested_queries=suggested_queries
        )
        state.critique_history.append(critique)

        if not passed and state.cycle_count < state.max_cycles:
            state.cycle_count += 1
            for i, q in enumerate(suggested_queries):
                state.plan.append(ResearchSubtask(
                    id=f"reflect_{state.cycle_count}_{i}",
                    query=q,
                    intent=f"Reflection cycle {state.cycle_count} verification"
                ))

        return state
