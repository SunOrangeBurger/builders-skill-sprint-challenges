# Challenge 3: Agent with Persistent Memory (Bedrock — Nova Pro) ⭐⭐

## Goal
Give your agent persistent memory using FAISS so it remembers facts across messages.

## Model: Amazon Nova Pro via Bedrock

## Prerequisites
- AWS account with Bedrock access
- `pip install faiss-cpu`

## What You'll Learn
- The difference between conversation history and persistent memory
- How to use `mem0_memory` with FAISS (local vector store)
- How to store and recall information

## Instructions

1. Open `starter.py`
2. Fill in the `# TODO` sections
3. Run it: `python starter.py`

## Expected Output

```
You: Remember that my name is Ravi and I love biryani
Agent: ✅ I'll remember that!

You: What's my name and what food do I like?
Agent: Your name is Ravi and you love biryani!
```

## Two Types of Memory

| Type | How It Works | Persists After Quit? |
|------|-------------|---------------------|
| **Conversation History** | Strands sends all previous messages to the model each time | ❌ No |
| **mem0_memory (FAISS)** | Stores facts as vectors on disk | ✅ Yes |

## Hints

- Import `mem0_memory` from `strands_tools`
- FAISS stores data locally — no cloud needed for storage
- The agent automatically decides when to store vs recall memories

## Bonus Points
- Store 3 different preferences, then ask the agent to list all of them
- Quit the program, restart it, and verify the memories persist
