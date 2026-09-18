from typing import List
from agentic_research.core.state import AgentState, ResearchSubtask, AgentStatus


class PlannerNode:
    def execute(self, state: AgentState) -> AgentState:
        state.status = AgentStatus.PLANNING
        subtasks: List[ResearchSubtask] = [
            ResearchSubtask(
                id="task_1",
                query=state.query,
                intent="Core thematic exploration and state-of-the-art definitions"
            ),
            ResearchSubtask(
                id="task_2",
                query=f"{state.query} architecture benchmarks evaluation",
                intent="Quantitative benchmarks, technical tradeoffs and metrics"
            )
        ]
        state.plan = subtasks
        return state
