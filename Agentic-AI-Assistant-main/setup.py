"""
setup.py — One-click setup script for Sujith Agentic AI
----------------------------------------------------------
Run this script ONCE after installing requirements to:
1. Check your .env configuration
2. Build the ChromaDB vector store
"""

import os
import sys
from pathlib import Path

# Add project root to path
root = Path(__file__).parent
sys.path.insert(0, str(root))

def check_env():
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        print("[ERROR] GROQ_API_KEY is not set in your .env file!")
        print("   1. Open your .env file in the project folder")
        print("   2. Get your free Groq API key at: https://console.groq.com/keys")
        print("   3. Paste it as: GROQ_API_KEY=your_key_here")
        sys.exit(1)
    print(f"[OK] GROQ_API_KEY found (ends with: ...{api_key[-6:]})")


def build_db():
    print("\n[*] Building vector store from QA datasets...")
    from scripts.build_vector_store import build_vector_store
    build_vector_store()


if __name__ == "__main__":
    print("=" * 60)
    print("  Sujith Agentic AI - Setup")
    print("=" * 60)
    
    check_env()
    build_db()
    
    print("\n" + "=" * 60)
    print("[DONE] Setup Complete! Your project is ready.\n")
    print("To run the full web application:")
    print("  Terminal 1 (API):  python app/api.py")
    print("  Terminal 2 (UI):   streamlit run app/ui.py")
    print("")
    print("To test the agent directly:")
    print("  python graph/agent_graph.py")
    print("=" * 60)
