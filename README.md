# Automating Exploitation with Agentic Systems - Workshop

**This workshop demonstrates Agentic AI in offensive cybersecurity roles solely for educational use and must not be used against any system without explicit permission.**

## Exercise 2 - Automating Recon

This repository demonstrates a collaborative system of agents led by an orchestration agent making decisions based on updated context from the team. 

- **Recon Agents**: Performs reconnaissance against target based on provided goals and overall team goal.
- **Summary**: Provides a concise report of the recon outout.

Outputs summary report consisting of output from Recon agents.

## Tools Used

- Series of MCP connected tools 
- Mixed frontier model use GPT-5.2, Opus-4.5.
- Asynchronous teaming of agents
- Mission Knowledge for overall context
- Pydantic Logfire for observability 

## Purpose

Highlights capabilities of collaborative agents with MCP tool access.

## Installation

**Note Logfire requires an account to use however they have a VERY generous free tier**

1. git clone https://github.com/kwnge/2026-ai-sym-cyber-exercise2.git
2. cd 2026-ai-sym-cyber-exercise2
3. uv sync
4. source .venv/bin/activate
5. logfire auth ## if using logfire
6. Create .env file with API keys to LLM providers
7. uv run main.py

## Usage

1. Initialize your mission dependencies with the target, goal and target information. 
2. The Recon agents will look for public endpoints and authentication vulnerabilities against the target. 
3. A summary is created along with an updated mission context that is all passed to the exploit agent.

## Ethical Considerations

This tool is provided for educational purposes only. It should be used exclusively in controlled lab environments to improve defensive security measures. Unauthorized use on systems without explicit permission is prohibited.

---

*Created for 2026 AI Symposium workshop to highlight agentic capability. Use responsibly.*