import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent
from strands_tools import mem0_memory

MODEL = "us.amazon.nova-pro-v1:0"

# Agent with persistent memory tool
agent = Agent(
    model=MODEL,
    tools=[mem0_memory],
    system_prompt="""You are a helpful assistant with memory.
Use the mem0_memory tool to:
- STORE important things the user tells you about themselves
- RETRIEVE relevant memories when answering questions
Always check your memory before responding."""
)

print("🧠 Memory Agent — type 'quit' to exit\n")

# Multi-turn conversation loop
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    if not user_input:
        continue
    response = agent(user_input)
    print(f"Agent: {response}\n")

print("\n✅ Challenge 3 complete!")