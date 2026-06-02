"""
api.py — FastAPI Backend for Sujith Agentic AI (Stretch Goal 4)
------------------------------------------------------------------
Exposes REST endpoints for the chat agent and escalation form.

Run with: uvicorn app.api:app --reload --port 8000
"""

import sys
import os
from pathlib import Path

# Ensure the project root is on the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from graph.agent_graph import run_agent

# ─── App Init ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Sujith Agentic AI API",
    description="Intelligent AI Assistant for Sujith retail company powered by LangGraph + Gemini",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ─────────────────────────────────────────────────
class ChatRequest(BaseModel):
    query: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sentiment: str
    department: str
    route: str
    requires_form: bool
    ticket_id: Optional[str] = None


class EscalationFormRequest(BaseModel):
    query: str
    user_name: str
    user_email: str
    user_phone: str


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "Sujith Agentic AI API is running!",
        "endpoints": {
            "/chat": "POST — Send a query to the AI assistant",
            "/escalate": "POST — Submit escalation form with contact details",
            "/health": "GET — Health check",
            "/docs": "GET — Interactive API documentation"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Sujith Agentic AI"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint. Accepts user query and optional contact details.
    Routes to RAG agent or escalation agent based on sentiment + department.
    """
    result = run_agent(
        query=request.query,
        user_name=request.user_name,
        user_email=request.user_email,
        user_phone=request.user_phone
    )
    
    return ChatResponse(
        response=result["response"],
        sentiment=result.get("sentiment", "neutral"),
        department=result.get("department", "unknown"),
        route=result.get("route", "rag"),
        requires_form=result.get("requires_form", False)
    )


@app.post("/escalate", response_model=ChatResponse)
def escalate(request: EscalationFormRequest):
    """
    Escalation endpoint — used when the user fills in the contact form.
    Re-runs the agent with contact details to confirm escalation.
    """
    result = run_agent(
        query=request.query,
        user_name=request.user_name,
        user_email=request.user_email,
        user_phone=request.user_phone
    )
    
    return ChatResponse(
        response=result["response"],
        sentiment=result.get("sentiment", "negative"),
        department=result.get("department", "unknown"),
        route="escalation",
        requires_form=False
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
