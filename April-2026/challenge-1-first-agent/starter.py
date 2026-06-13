from strands import Agent
from strands.models.ollama import OllamaModel

# Connect to local Ollama instance
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:3b"
)

# Create the agent
agent = Agent(
    model=ollama_model,
    tools=[],
    system_prompt="You are a helpful assistant. Be brief."
)

# Ask a question
response = agent("Tell me a fun fact about Python programming")

print("🤖 Agent: ", end="")
print(response)

print("\n✅ Challenge 1 complete!")