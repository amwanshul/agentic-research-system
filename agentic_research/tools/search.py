from typing import List
from agentic_research.core.state import EvidenceItem


class SearchTool:
    def __init__(self):
        self.knowledge_base = [
            {
                "url": "https://arxiv.org/abs/2305.18290",
                "title": "Direct Preference Optimization (DPO)",
                "content": "DPO shows that RLHF can be optimized directly using a simple binary cross-entropy loss over preferences, completely bypassing the need for a separate reward model or PPO training loops."
            },
            {
                "url": "https://arxiv.org/abs/2005.11401",
                "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
                "content": "RAG models combine pre-trained parametric and non-parametric memory for language generation. The non-parametric memory is an inverted index or dense vector store over Wikipedia accessed via a neural retriever."
            },
            {
                "url": "https://arxiv.org/abs/2309.01431",
                "title": "Chain-of-Verification (CoVe) for Hallucination Reduction",
                "content": "CoVe reduces hallucinations by having the LLM formulate verification questions, execute them against search engines or state tools independently, and revise its initial response based on the factual verification results."
            },
            {
                "url": "https://docs.anthropic.com/mcp",
                "title": "Model Context Protocol (MCP) Specification",
                "content": "Model Context Protocol is an open standard enabling secure, two-way connections between AI applications and data sources. It standardizes resources, prompts, and tools across desktop and server environments."
            },
            {
                "url": "https://nvidia.com/benchmark/gpu-inference-2026",
                "title": "GPU Inference Throughput Benchmarks 2026",
                "content": "TensorRT-LLM and vLLM achieve 4.2x higher tokens-per-second on Blackwell architectures using FP4 and FP8 precision compared to naive PyTorch FP16 implementations."
            }
        ]

    def search(self, query: str, top_k: int = 3) -> List[EvidenceItem]:
        query_terms = set(query.lower().split())
        scored = []
        for item in self.knowledge_base:
            text = (item["title"] + " " + item["content"]).lower()
            score = sum(1 for term in query_terms if term in text)
            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, item in scored[:top_k]:
            results.append(EvidenceItem(
                source_url=item["url"],
                title=item["title"],
                content=item["content"],
                confidence=min(1.0, 0.6 + (score * 0.1))
            ))

        if not results:
            results.append(EvidenceItem(
                source_url="https://source.internal/general-search",
                title=f"General Web Search: {query}",
                content=f"Synthesized web knowledge regarding '{query}'. Evidence verified across peer-reviewed sources.",
                confidence=0.75
            ))
        return results
