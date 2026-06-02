"""
router_agent.py
---------------
Classifies user queries by:
  1. Sentiment: positive | neutral | negative
  2. Department: HR | IT Support | Customer Support | Product & Promotions | unknown
"""

import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

DEPARTMENTS = ["HR", "IT Support", "Customer Support", "Product & Promotions"]

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an intelligent query classifier for Sujith, a retail company.
Your job is to analyze a user's query and return a JSON object with two fields:
  - "sentiment": one of ["positive", "neutral", "negative"]
  - "department": one of ["HR", "IT Support", "Customer Support", "Product & Promotions", "unknown"]

Department Descriptions:
- HR: Internal employee queries about leave, payroll, benefits, policies, grievances, resignation.
- IT Support: Internal employee queries about software, hardware, VPN, passwords, devices, cybersecurity.
- Customer Support: External customer queries about orders, returns, refunds, deliveries, complaints.
- Product & Promotions: External customer queries about discounts, deals, product details, warranty, loyalty points.
- unknown: If the query doesn't clearly belong to any of the above departments.

Sentiment Rules:
- negative: The user is frustrated, angry, complaining aggressively, or using harsh language.
- neutral: A factual or informational query with no strong emotion.
- positive: The user is happy, praising, or expressing satisfaction.

Return ONLY a valid JSON object, no explanation, no markdown.
Example: {{"sentiment": "neutral", "department": "HR"}}
"""),
    ("human", "User query: {query}")
])


def classify_query(query: str) -> dict:
    """
    Classify user query by sentiment and department.
    Returns dict with 'sentiment' and 'department' keys.
    """
    chain = ROUTER_PROMPT | llm
    result = chain.invoke({"query": query})

    try:
        # Extract JSON from response
        content = result.content.strip()
        # Handle potential markdown code blocks
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        classification = json.loads(content.strip())
    except (json.JSONDecodeError, IndexError):
        # Fallback if parsing fails
        classification = {"sentiment": "neutral", "department": "unknown"}

    # Validate values
    if classification.get("sentiment") not in ["positive", "neutral", "negative"]:
        classification["sentiment"] = "neutral"
    if classification.get("department") not in DEPARTMENTS + ["unknown"]:
        classification["department"] = "unknown"

    return classification


if __name__ == "__main__":
    test_queries = [
        "How many leave days do I get per year?",
        "I am furious! My package never arrived and nobody is helping me!",
        "What discounts are available this week?",
        "Can you book me a flight to Paris?",
    ]
    for q in test_queries:
        result = classify_query(q)
        print(f"Query: {q}")
        print(f"  → Sentiment: {result['sentiment']}, Department: {result['department']}\n")
