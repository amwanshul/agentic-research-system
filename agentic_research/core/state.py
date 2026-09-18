from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time


class AgentStatus(str, Enum):
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    RESEARCHING = "RESEARCHING"
    COMPUTING = "COMPUTING"
    REFLECTING = "REFLECTING"
    SYNTHESIZING = "SYNTHESIZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class EvidenceItem:
    source_url: str
    title: str
    content: str
    confidence: float = 1.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class ResearchSubtask:
    id: str
    query: str
    intent: str
    completed: bool = False
    evidence_ids: List[str] = field(default_factory=list)


@dataclass
class CritiqueResult:
    passed: bool
    factuality_score: float  # 0.0 to 1.0
    issues: List[str] = field(default_factory=list)
    suggested_queries: List[str] = field(default_factory=list)


@dataclass
class AgentState:
    query: str
    plan: List[ResearchSubtask] = field(default_factory=list)
    evidence: List[EvidenceItem] = field(default_factory=list)
    computation_results: Dict[str, Any] = field(default_factory=dict)
    draft_findings: List[str] = field(default_factory=list)
    critique_history: List[CritiqueResult] = field(default_factory=list)
    status: AgentStatus = AgentStatus.IDLE
    cycle_count: int = 0
    max_cycles: int = 2
    final_report: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
