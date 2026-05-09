# Challenge 4: The Full Agent — Tools + Memory + Streaming (Bedrock) ⭐⭐⭐

## Goal
Build a full-featured agent that combines everything: tools + memory + streaming.

## Model: Amazon Nova Pro via Bedrock

## What You'll Build
An interactive agent that can:
- 🧮 Do math (calculator)
- 🌤️ Check real weather (custom tool)
- 🎂 Calculate age (custom tool)
- 🧠 Remember your preferences (mem0_memory)
- ⚡ Stream responses in real time (callback handler)

## Instructions

1. Open `starter.py`
2. Fill in ALL the `# TODO` sections
3. Run it: `python starter.py`
4. Have a full conversation — use all the tools!

## Expected Output

```
You: Remember my name is Priya and I'm from Madurai
Agent: ✅ Stored!

You: What's the weather in my city?
Agent: 🔧 Using tool: weather
Weather in Madurai: Sunny, 38°C...

You: How old is someone born on 2002-03-15? Also what's 365 * 24?
Agent: 🔧 Using tool: age_calculator
🔧 Using tool: calculator
24 years old. 365 × 24 = 8,760 hours in a year!

You: What's my name?
Agent: Your name is Priya!
```

## Hints

- Combine all imports from Challenges 1-3
- The streaming callback prints text as it arrives + shows tool usage
- System prompt should mention ALL available tools

## Bonus Points
- Add one more custom tool of your own invention
- Make the agent's personality fun (emojis, humor in system prompt)
