"""
Challenge 3: Agent with Persistent Memory
Give your agent memory that survives restarts using FAISS.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Store some facts, then quit and restart to verify persistence
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Import mem0_memory from strands_tools
# ============================================================
# Hint: from strands_tools import mem0_memory

# Your import here


# ============================================================
# TODO 2: Create an agent with mem0_memory tool
# ============================================================
# Hint: Agent(model=MODEL, tools=[mem0_memory], system_prompt="...")
# System prompt should tell the agent to store and recall user preferences

agent = None  # Replace this line


# ============================================================
# TODO 3: Interactive loop — chat with the memory agent
# ============================================================

print("🧠 Memory Agent Ready!")
print("Try: 'Remember that my name is [your name] and I love [food]'")
print("Then: 'What's my name and what food do I like?'")
print("Type 'quit' to exit.\n")

while True:
    try:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye! 👋")
            break

        # TODO: Send user_input to the agent and print the response
        # Hint: response = agent(user_input)
        print("Agent: [TODO - call the agent here]")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break

print("\n✅ Challenge 3 complete!")
