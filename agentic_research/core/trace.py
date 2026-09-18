import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TraceStep:
    node_name: str
    input_state_summary: str
    output_summary: str
    start_time: float
    end_time: float
    duration_seconds: float
    tokens_used: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionTrace:
    run_id: str
    initial_query: str
    steps: List[TraceStep] = field(default_factory=list)
    total_duration: float = 0.0
    total_tokens: int = 0
    final_status: str = "PENDING"

    def add_step(self, step: TraceStep) -> None:
        self.steps.append(step)
        self.total_duration += step.duration_seconds
        self.total_tokens += step.tokens_used

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "query": self.initial_query,
            "total_duration_sec": round(self.total_duration, 4),
            "total_tokens": self.total_tokens,
            "final_status": self.final_status,
            "steps_count": len(self.steps),
            "steps": [
                {
                    "node": s.node_name,
                    "duration_sec": round(s.duration_seconds, 4),
                    "tokens": s.tokens_used,
                    "input": s.input_state_summary,
                    "output": s.output_summary,
                    "metadata": s.metadata
                }
                for s in self.steps
            ]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
