# Challenge 1: Your First AI Agent (Ollama — Local) ⭐

## Goal
Create a simple AI agent using Strands SDK + Ollama that runs **100% locally** on your machine. No cloud, no API key.

## Model: Ollama (llama3.2:3b)

## What You'll Learn
- How to install and run Ollama
- How to connect Strands to a local model
- How to create an agent with a system prompt
- How to send a question and get a response

## Instructions

1. Open `starter.py`
2. Fill in the `# TODO` sections
3. Run it: `python starter.py`

## Expected Output

```
🤖 Agent: Python is a high-level, interpreted programming language...
```

## Hints

- Import `OllamaModel` from `strands.models.ollama`
- The Ollama host is `http://localhost:11434`
- The model ID is `llama3.2:3b`
- Use `tools=[]` since we're not adding tools yet
- Make sure `ollama serve` is running!

## Bonus Points
- Try changing the `system_prompt` to make the agent respond like a pirate 🏴‍☠️
- Try asking it 3 different questions
