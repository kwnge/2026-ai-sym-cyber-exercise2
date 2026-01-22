from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIChatModelSettings
from pydantic_ai.models.anthropic import AnthropicModel, AnthropicModelSettings
from pydantic_ai.mcp import MCPServerStreamableHTTP

from typing import List
from dependencies import Deps, AttackVector

NIKTO_MCP = MCPServerStreamableHTTP('http://localhost:8005/mcp', max_retries=5, tool_prefix="nikto_prim")
NIKTO_MCP_SEC = MCPServerStreamableHTTP('http://localhost:8015/mcp', max_retries=5, tool_prefix="nikto_sec")
CURL_MCP = MCPServerStreamableHTTP('http://localhost:8003/mcp', max_retries=5, tool_prefix="curl")
WGET_MCP = MCPServerStreamableHTTP('http://localhost:8004/mcp', max_retries=5, tool_prefix="wget")

gpt_52 = OpenAIChatModel(
    model_name='gpt-5.2',
    settings=OpenAIChatModelSettings(
        timeout=600
    )
)
opus_45 = AnthropicModel(
    model_name='claude-opus-4-5',
    settings=AnthropicModelSettings(
        timeout=600,
    )
)

# Recon specific to routes and public endpoints
recon_endpoint_agent = Agent[Deps](
    name="Recon Endpoints",
    model=gpt_52,
    output_type=List[AttackVector],
    toolsets=[NIKTO_MCP],
    instructions=(
        "You are a senior application security recon specialist focused exclusively on "
        "identifying public endpoints in web applications.\n\n"

        "Output requirements:\n"
        "- Return a list of Attack Vector objects only.\n"
        "- Each Attack Vector MUST include:\n"
        "  • type: a concise identifier (e.g., 'SQLi – Boolean-based', Information Disclosure, Misconfiguration, Exposed Credentials).\n"
        "  • explicit_path: the full URL and parameter tested.\n"
        "  • payload: the exact payload used and the observed behavior.\n"
        "  • confirmed: true ONLY if exploitation was demonstrated.\n\n"

        "Rules:\n"
        "- Do NOT include remediation.\n"
        "- Do NOT include generic advice or explanations.\n"
    )
)

# Recon specific to SQLi
recon_auth_agent = Agent[Deps](
    name="Recon AuthN",
    model=opus_45,
    output_type=List[AttackVector],
    toolsets=[NIKTO_MCP_SEC, WGET_MCP, CURL_MCP],
    instructions=(
        "You are a senior application security recon specialist focused exclusively on "
        "identifying authenitcation vulnerabilities in web applications.\n\n"

        "Scope:\n"
        "- Only assess inputs that interact login or authentication endpoints.\n"
        "- Prioritize unauthenticated and low-privilege attack paths.\n"
        "- Use evidence-driven reasoning; do not speculate.\n\n"

        "Output requirements:\n"
        "- Return a list of Vulnerability objects only.\n"
        "- Each Vulnerability MUST include:\n"
        "  • type: a concise identifier (e.g., 'SQLi – Boolean-based', 'SQLi – Error-based').\n"
        "  • explicit_path: the full URL and parameter tested.\n"
        "  • payload: the exact payload used and the observed behavior.\n"
        "  • confirmed: true ONLY if exploitation was demonstrated.\n\n"

        "Rules:\n"
        "- Do NOT include remediation.\n"
        "- Do NOT include generic advice or explanations.\n"
        "- Prefer minimal payloads that reliably prove impact.\n"
    )
)

# Summary agent for markdown report
summary_agent = Agent(
    name="Summary Agent",
    model=gpt_52,
    instructions=(
    'Summarize the findings into a Markdown style report.'
    )
)
