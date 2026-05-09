# Challenge 2: Adding Tools to Your Agent (Bedrock — Nova Pro) ⭐⭐

## Goal
Give your agent superpowers by adding a calculator and a custom weather tool using Amazon Nova Pro.

## Model: Amazon Nova Pro via Bedrock

## Prerequisites
- AWS account with Bedrock access
- Amazon Nova Pro model enabled
- AWS credentials configured (`aws configure`)

## What You'll Learn
- How to use built-in Strands tools (calculator)
- How to create custom tools with the `@tool` decorator
- How the agent decides which tool to use

## Instructions

1. Open `starter.py`
2. Fill in the `# TODO` sections
3. Run it: `python starter.py`

## Expected Output

```
🧮 Math: 42 * 17 = 714
🌤️ Weather: Weather in Chennai: Partly cloudy, 33°C...
🎂 Age: Age: 25 years old
```

## Hints

- Import `tool` from `strands` to create custom tools
- The `@tool` decorator turns any function into an agent tool
- The agent reads the **docstring** to understand what the tool does
- For weather, use the wttr.in API: `https://wttr.in/{city}?format=j1`
- For age calculator, use `datetime` to calculate the difference

## Bonus Points
- Add a third custom tool (e.g., a unit converter, a joke teller)
- Ask the agent a question that requires multiple tools at once
