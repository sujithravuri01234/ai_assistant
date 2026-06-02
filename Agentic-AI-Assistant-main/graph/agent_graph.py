"""
agent_graph.py
--------------
LangGraph workflow for Sujith Agentic AI.

Routing:
- negative sentiment -> escalation
- otherwise -> rag (with internal AI cascade fallback inside rag_agent)
"""

from typing import TypedDict, Optional, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START

from agents.router_agent import classify_query
from agents.rag_agent import retrieve_and_answer
from agents.escalation_agent import escalate_to_human

load_dotenv()


class AgentState(TypedDict):
    query: str
    sentiment: Optional[str]
    department: Optional[str]
    response: Optional[str]
    route: Optional[str]
    user_name: Optional[str]
    user_email: Optional[str]
    user_phone: Optional[str]
    requires_form: Optional[bool]


def classify_node(state: AgentState) -> AgentState:
    print(f"\n[Router] Classifying query: '{state['query']}'")

    classification = classify_query(state["query"])
    sentiment = classification["sentiment"]
    department = classification["department"]

    print(f"[Router] -> Sentiment: {sentiment}, Department: {department}")

    # Unknown department should still attempt AI answer through RAG cascade.
    route = "escalation" if sentiment == "negative" else "rag"

    print(f"[Router] -> Route: {route}")

    return {
        **state,
        "sentiment": sentiment,
        "department": department,
        "route": route,
    }


def rag_node(state: AgentState) -> AgentState:
    print(f"\n[RAG Agent] Generating answer for dept: '{state['department']}'")

    answer = retrieve_and_answer(state["query"], state.get("department") or "unknown")

    print(f"[RAG Agent] -> Answer generated ({len(answer)} chars)")

    return {
        **state,
        "response": answer,
        "requires_form": False,
    }


def escalation_node(state: AgentState) -> AgentState:
    reason = "negative_sentiment"
    print(f"\n[Escalation Agent] Escalating - Reason: {reason}")

    result = escalate_to_human(
        query=state["query"],
        reason=reason,
        user_name=state.get("user_name"),
        user_email=state.get("user_email"),
        user_phone=state.get("user_phone"),
    )

    return {
        **state,
        "response": result["message"],
        "requires_form": result.get("requires_form", False),
    }


def route_after_classify(state: AgentState) -> Literal["rag_node", "escalation_node"]:
    if state["route"] == "rag":
        return "rag_node"
    return "escalation_node"


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classify_node", classify_node)
    workflow.add_node("rag_node", rag_node)
    workflow.add_node("escalation_node", escalation_node)

    workflow.add_edge(START, "classify_node")

    workflow.add_conditional_edges(
        "classify_node",
        route_after_classify,
        {
            "rag_node": "rag_node",
            "escalation_node": "escalation_node",
        },
    )

    workflow.add_edge("rag_node", END)
    workflow.add_edge("escalation_node", END)

    return workflow.compile()


_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def run_agent(
    query: str,
    user_name: str = None,
    user_email: str = None,
    user_phone: str = None,
) -> dict:
    graph = get_graph()

    initial_state: AgentState = {
        "query": query,
        "sentiment": None,
        "department": None,
        "response": None,
        "route": None,
        "user_name": user_name,
        "user_email": user_email,
        "user_phone": user_phone,
        "requires_form": False,
    }

    final_state = graph.invoke(initial_state)
    return final_state
