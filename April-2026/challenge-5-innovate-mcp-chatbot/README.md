# Challenge 5 (Innovate): Build Your Own MCP-Powered Agent 🚀

## Goal
Build an **innovative agent from scratch** that connects to any MCP server and solves a real problem. The most creative and useful agent gets a **special shoutout!** 🏆

## Rules
- Must use **Strands Agents SDK**
- Must use **at least one MCP server**
- Must use **Amazon Nova Pro** (or any Bedrock model)
- Must have an **interactive chat loop**
- Must be **your own idea** — be creative!

## Example: AWS Documentation Chatbot

Here's one example to inspire you — a chatbot connected to the AWS Documentation MCP server:

```bash
pip install awslabs.aws-documentation-mcp-server
```

```python
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client

aws_docs_mcp = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(command="awslabs.aws-documentation-mcp-server")
    )
)

with aws_docs_mcp:
    tools = aws_docs_mcp.list_tools_sync()
    agent = Agent(model="us.amazon.nova-pro-v1:0", tools=tools)
    # ... interactive chat loop
```

**But don't just copy this — build something unique!**

## MCP Servers You Can Use

| MCP Server | What It Does | Install |
|------------|-------------|---------|
| AWS Documentation | Search & read AWS docs | `pip install awslabs.aws-documentation-mcp-server` |
| AWS CDK | CDK best practices & patterns | `uvx awslabs.cdk-mcp-server@latest` |
| AWS Cost Analysis | AWS pricing info | `uvx awslabs.cost-analysis-mcp-server@latest` |
| GitHub | Search repos, read code | Community MCP servers |
| Filesystem | Read/write local files | Built into many MCP packages |

Browse more at: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

## Ideas to Get You Started

- 🔍 **AWS Docs Expert** — Search and summarize any AWS service documentation
- 💰 **AWS Cost Advisor** — Help estimate costs for AWS architectures
- 🏗️ **CDK Helper** — Generate CDK code following best practices
- 📚 **Study Buddy** — Connect to a docs MCP + memory to remember what you've studied
- 🤖 **Multi-MCP Agent** — Connect to 2+ MCP servers at once for a super-agent
- 🔧 **DevOps Assistant** — Combine AWS docs + CDK for infrastructure help

## Judging Criteria

| Criteria | Weight |
|----------|--------|
| **Creativity** — How unique is your idea? | ⭐⭐⭐ |
| **Working Demo** — Does it actually run? | ⭐⭐⭐ |
| **MCP Usage** — How well do you use MCP tools? | ⭐⭐ |
| **Code Quality** — Clean, readable, well-structured | ⭐ |
| **Bonus** — Memory, streaming, multiple MCP servers | ⭐ |

## How to Submit

1. Put your complete code in `starter.py` (or create your own `.py` file)
2. Take a **screenshot** of your agent in action
3. Write a **2-3 line description** of what your agent does
4. Submit at [https://www.awsugmdu.in/](https://www.awsugmdu.in/)

## Resources

- [Strands MCP Docs](https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/)
- [MCP Server List](https://github.com/modelcontextprotocol/servers)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [Strands SDK](https://strandsagents.com)

**Build something that makes us go "whoa!" 🚀**
