# 🤖 Builders Skill Sprint — April 2026

## Getting Started with AI Agents using Strands SDK

Welcome to the April 2026 Builders Skill Sprint Challenge! In this hands-on challenge, you'll build AI agents step by step — starting locally with Ollama, then scaling to the cloud with Amazon Bedrock.

---

## 🎯 Challenges

| # | Challenge | Model | Difficulty |
|---|-----------|-------|-----------|
| 1 | **First Agent** — Create your first AI agent | Ollama (local) | ⭐ Easy |
| 2 | **Tools** — Add calculator + custom weather tool | Bedrock (Nova Pro) | ⭐⭐ Medium |
| 3 | **Memory** — Add persistent memory with FAISS | Bedrock (Nova Pro) | ⭐⭐ Medium |
| 4 | **Full Agent** — Tools + memory + streaming combined | Bedrock (Nova Pro) | ⭐⭐⭐ Hard |
| 5 | **Innovate: MCP Agent** — Build your own MCP-powered agent (any MCP server!) | Bedrock (Nova Pro) | 🚀 Innovate |

---

## 📋 Prerequisites

- **Python 3.10+** installed
- **Ollama** installed (for Challenge 1)
- **AWS account** with Bedrock access (for Challenges 2-5)
- Basic Python knowledge

---

## 🚀 Setup

### Step 1: Install Ollama (for Challenge 1)

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** Download from [ollama.com/download](https://ollama.com/download)

### Step 2: Pull a Local Model

```bash
ollama serve
# In a new terminal:
ollama pull llama3.2:3b
```

### Step 3: Create Python Environment

```bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux

# Install all dependencies
pip install strands-agents "strands-agents[ollama]" strands-agents-tools faiss-cpu
```

### Step 4: AWS Credentials (for Challenges 2-5)

```bash
aws configure
```

Make sure **Amazon Nova Pro** is enabled in your Bedrock console.

### Step 5: MCP Server (for Challenge 5 only)

```bash
pip install awslabs.aws-documentation-mcp-server
```

---

## 📁 Folder Structure

```
april-2026/
├── README.md                              ← You are here
├── challenge-1-first-agent/
│   ├── README.md                          ← Instructions (Ollama)
│   └── starter.py
├── challenge-2-tools/
│   ├── README.md                          ← Instructions (Bedrock)
│   └── starter.py
├── challenge-3-memory/
│   ├── README.md                          ← Instructions (Bedrock)
│   └── starter.py
├── challenge-4-full-agent/
│   ├── README.md                          ← Instructions (Bedrock)
│   └── starter.py
├── challenge-5-innovate-mcp-chatbot/
│   ├── README.md                          ← Build from scratch (Bedrock)
│   └── starter.py
```

---

## 🏆 Scoring

| Challenge | Points |
|-----------|--------|
| Challenge 1 — First Agent (Ollama) | 25 pts |
| Challenge 2 — Tools (Bedrock) | 25 pts |
| Challenge 3 — Memory (Bedrock) | 25 pts |
| Challenge 4 — Full Agent (Bedrock) | 25 pts |
| Challenge 5 — Innovate: MCP Agent | 🏆 Best agent gets a special shoutout! |

---

## 📝 How to Submit

1. Complete the challenges by filling in the `starter.py` files
2. Take a **screenshot** of your terminal showing the agent's output
3. Submit at [https://www.awsugmdu.in/](https://www.awsugmdu.in/)

---

## 💡 Tips

- Start with Challenge 1 — it's the foundation
- Challenge 1 runs fully offline (Ollama). Challenges 2-5 need AWS.
- If Ollama is slow on first run, wait 10-20 seconds — it's loading the model

---

## 🔗 Resources

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- [Strands Tools (40+ tools)](https://github.com/strands-agents/tools)
- [Strands Documentation](https://strandsagents.com)
- [Ollama](https://ollama.com)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

---

Happy building! 🚀
