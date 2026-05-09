"""
Challenge 1: Your First AI Agent
Build a simple agent using Strands SDK + Ollama (runs locally!)

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Make sure 'ollama serve' is running in another terminal
"""

# TODO 1: Import Agent from strands
# Hint: from strands import Agent


# TODO 2: Import OllamaModel from strands
# Hint: from strands.models.ollama import OllamaModel


# TODO 3: Create an OllamaModel instance
# Hint: Use host="http://localhost:11434" and model_id="llama3.2:3b"
ollama_model = None  # Replace this line


# TODO 4: Create an Agent with the ollama_model
# Hint: Agent(model=..., tools=[], system_prompt="...")
# Use a fun system prompt like "You are a helpful assistant. Be brief."
agent = None  # Replace this line


# TODO 5: Ask the agent a question and print the response
# Hint: response = agent("Your question here")
# Try: "Tell me a fun fact about Python programming"
print("🤖 Agent: ", end="")
# Your code here


print("\n✅ Challenge 1 complete!")
