import time
import uuid
from typing import Optional, Callable
from agentic_research.core.state import AgentState, AgentStatus
from agentic_research.core.trace import ExecutionTrace, TraceStep
from agentic_research.nodes.planner import PlannerNode
from agentic_research.nodes.researcher import ResearcherNode
from agentic_research.nodes.critic import CriticNode
from agentic_research.nodes.synthesizer import SynthesizerNode


class ResearchGraph:
    def __init__(self, max_cycles: int = 2):
        self.max_cycles = max_cycles
        self.planner = PlannerNode()
        self.researcher = ResearcherNode()
        self.critic = CriticNode()
        self.synthesizer = SynthesizerNode()

    def run(self, query: str, trace_callback: Optional[Callable[[TraceStep], None]] = None) -> tuple[AgentState, ExecutionTrace]:
        run_id = f"run_{uuid.uuid4().hex[:8]}"
        state = AgentState(query=query, max_cycles=self.max_cycles)
        trace = ExecutionTrace(run_id=run_id, initial_query=query)

        def step_wrapper(node_name: str, fn: Callable[[AgentState], AgentState]) -> None:
            t0 = time.time()
            in_summary = f"status={state.status.value}, plan_len={len(state.plan)}, evidence_len={len(state.evidence)}"
            fn(state)
            t1 = time.time()
            out_summary = f"status={state.status.value}, plan_len={len(state.plan)}, evidence_len={len(state.evidence)}"
            step = TraceStep(
                node_name=node_name,
                input_state_summary=in_summary,
                output_summary=out_summary,
                start_time=t0,
                end_time=t1,
                duration_seconds=t1 - t0,
                tokens_used=120 + (len(state.evidence) * 45)
            )
            trace.add_step(step)
            if trace_callback:
                trace_callback(step)

        # 1. Planning
        step_wrapper("PlannerNode", self.planner.execute)

        # 2. Iterative Research & Reflection Loop
        while state.cycle_count <= self.max_cycles:
            step_wrapper("ResearcherNode", self.researcher.execute)
            step_wrapper("CriticNode", self.critic.execute)

            last_critique = state.critique_history[-1]
            if last_critique.passed:
                break

        # 3. Synthesis
        step_wrapper("SynthesizerNode", self.synthesizer.execute)

        trace.final_status = state.status.value
        return state, trace
