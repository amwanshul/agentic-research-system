from agentic_research.core.state import AgentState, AgentStatus
from agentic_research.tools.search import SearchTool


class ResearcherNode:
    def __init__(self, search_tool: SearchTool = None):
        self.search_tool = search_tool or SearchTool()

    def execute(self, state: AgentState) -> AgentState:
        state.status = AgentStatus.RESEARCHING
        for task in state.plan:
            if not task.completed:
                evidence_items = self.search_tool.search(task.query, top_k=2)
                for item in evidence_items:
                    if not any(e.source_url == item.source_url for e in state.evidence):
                        state.evidence.append(item)
                task.completed = True
        return state
