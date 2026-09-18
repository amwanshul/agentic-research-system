import argparse
import sys
from agentic_research.core.graph import ResearchGraph


def main():
    parser = argparse.ArgumentParser(description="Agentic Research System - Autonomous State Graph Engine")
    parser.add_argument("query", type=str, nargs="?", help="Research topic or query")
    parser.add_argument("--cycles", type=int, default=2, help="Maximum critique & reflection cycles")
    parser.add_argument("--trace-out", type=str, help="Output JSON trace file path")
    args = parser.parse_args()

    if not args.query:
        print("Please specify a research query. Example: python -m agentic_research.cli 'Direct Preference Optimization'")
        sys.exit(1)

    print(f"[*] Initializing Research Graph for query: '{args.query}'...")
    graph = ResearchGraph(max_cycles=args.cycles)

    def on_step(step):
        print(f"  [NODE] {step.node_name:<16} | Duration: {step.duration_seconds*1000:6.1f}ms | Tokens: {step.tokens_used}")

    state, trace = graph.run(args.query, trace_callback=on_step)

    print("\n" + "=" * 60)
    print("RESEARCH BRIEF")
    print("=" * 60)
    print(state.final_report)

    if args.trace_out:
        with open(args.trace_out, "w") as f:
            f.write(trace.to_json())
        print(f"\n[*] Execution trace saved to {args.trace_out}")


if __name__ == "__main__":
    main()
