# Multi-Step-Reasoning-Agent-with-Self-Checking-with-LLM
a small “reasoning agent” that can solve structured problems in multiple  steps, check its own work, and only show the final answer to the user. LLM API you like (OpenAI, Anthropic, Gemini etc.) and any  programming language.
project/
│
├── app.py            # Streamlit UI
├── agent.py          # Reasoning Agent (Planner → Executor → Verifier)
├── llm_client.py     # Together API client (API key INSIDE)
└── requirements.txt

