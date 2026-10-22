"""LangGraph wiring of the requirements-refinement network (ANS5).

    START
      |
    loader ............................ deterministic
      |  Send() x documents  (parallel fan-out)
    extractor ......................... LLM  (gpt-5-mini)
      |  (branches joined; candidates appended by reducer)
    prededup .......................... deterministic
      |
    planner ........................... LLM  (gpt-5.6-luna) + deterministic repair
      |  Send() x topic batches  (parallel fan-out)
    consolidator ...................... LLM  (gpt-5.6-luna)
      |  (branches joined; batch results appended by reducer)
    assembler ......................... deterministic
      |
    validator  <-------------------+    deterministic
      |                            |
    reviewer                       |    LLM  (gpt-6-luna)
      |  "revise"                  |
      +------> reviser ------------+    LLM  (gpt-5.6-luna)   feedback loop (ANS3)
      |  "finish" (approved / max rounds / nothing left to fix)
    renderer .......................... deterministic
      |
     END
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from nodes.deterministic import (assembler_node, loader_node, prededup_node,
                                 renderer_node, validator_node)
from nodes.llm import (consolidator_node, extractor_node, planner_node, reviewer_node,
                       reviser_node)
from state import GraphState


def fan_out_documents(state: GraphState) -> list[Send]:
    """One parallel Extractor branch per document."""
    return [Send("extractor", {"document": d, "cache_dir": state.get("cache_dir"),
                               "cache_readonly": state.get("cache_readonly", False)})
            for d in state["documents"]]


def fan_out_topics(state: GraphState):
    """One parallel Consolidator branch per topic batch."""
    topics = state.get("topics", [])
    if not topics:
        return "assembler"
    by_id = {c.cand_id: c for c in state.get("candidates", [])}
    all_topics = list(dict.fromkeys(f"{t.name}: {t.scope}" for t in topics))
    return [Send("consolidator", {
        "batch_topic": t,
        "batch_candidates": [by_id[i] for i in t.candidate_ids],
        "batch_documents": state["documents"],
        "batch_glossary": state.get("plan_glossary", []),
        "batch_all_topics": all_topics}) for t in topics]


def route_after_review(state: GraphState) -> str:
    """Feedback-loop decision (deterministic)."""
    review = state.get("review")
    if state.get("halt"):
        print(f"[router] {state['halt']} -> finish")
        return "finish"
    if review is not None and review.approved:
        print("[router] approved -> finish")
        return "finish"
    if state.get("round", 0) >= state.get("max_rounds", 3):
        print(f"[router] max rounds ({state.get('max_rounds', 3)}) reached -> finish")
        return "finish"
    print(f"[router] changes requested -> revision {state.get('round', 0)}")
    return "revise"


def build_graph():
    g = StateGraph(GraphState)
    g.add_node("loader", loader_node)
    g.add_node("extractor", extractor_node)
    g.add_node("prededup", prededup_node)
    g.add_node("planner", planner_node)
    g.add_node("consolidator", consolidator_node)
    g.add_node("assembler", assembler_node)
    g.add_node("validator", validator_node)
    g.add_node("reviewer", reviewer_node)
    g.add_node("reviser", reviser_node)
    g.add_node("renderer", renderer_node)

    g.add_edge(START, "loader")
    g.add_conditional_edges("loader", fan_out_documents, ["extractor"])
    g.add_edge("extractor", "prededup")
    g.add_edge("prededup", "planner")
    g.add_conditional_edges("planner", fan_out_topics, ["consolidator", "assembler"])
    g.add_edge("consolidator", "assembler")
    g.add_edge("assembler", "validator")
    g.add_edge("validator", "reviewer")
    g.add_conditional_edges("reviewer", route_after_review,
                            {"revise": "reviser", "finish": "renderer"})
    g.add_edge("reviser", "validator")
    g.add_edge("renderer", END)
    return g.compile()
