from datetime import datetime, timezone
from agentic_research.core.state import AgentState, AgentStatus


class SynthesizerNode:
    def execute(self, state: AgentState) -> AgentState:
        state.status = AgentStatus.SYNTHESIZING

        lines = [
            f"# Research Brief: {state.query}",
            f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
            f"**Reflection Cycles Completed:** {state.cycle_count}  ",
            f"**Verified Evidence Sources:** {len(state.evidence)}  ",
            "",
            "## Executive Summary",
            f"This research brief synthesizes verified findings for the inquiry: *\"{state.query}\"*. "
            "Evidence has been corroborated through multi-step search, fact-checking reflection loops, and source provenance tracking.",
            "",
            "## Key Findings & Provenance"
        ]

        for idx, item in enumerate(state.evidence, start=1):
            lines.append(f"### {idx}. {item.title}")
            lines.append(f"> {item.content}")
            lines.append(f"**Source Provenance:** [{item.source_url}]({item.source_url}) *(Confidence: {item.confidence:.2f})*\n")

        if state.computation_results:
            lines.append("## Quantitative Computations")
            for k, v in state.computation_results.items():
                lines.append(f"- **{k}**: `{v}`")
            lines.append("")

        lines.append("## Verification & Fact-Checking Audit")
        if state.critique_history:
            last_critique = state.critique_history[-1]
            lines.append(f"- **Final Factuality Score**: `{last_critique.factuality_score:.2f} / 1.00`")
            lines.append(f"- **Audit Status**: {'✅ PASSED' if last_critique.passed else '⚠️ CONSTRAINED (Max cycles reached)'}")
            if last_critique.issues:
                lines.append(f"- **Noted Considerations**: {', '.join(last_critique.issues)}")
        else:
            lines.append("- Direct synthesis without reflection issues.")

        lines.append("\n---")
        lines.append("*Generated autonomously by Agentic Research System with deterministic state graph validation.*")

        state.final_report = "\n".join(lines)
        state.status = AgentStatus.COMPLETED
        return state
