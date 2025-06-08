"""
Gemini MCP Server - Main server implementation
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any

import google.generativeai as genai
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from mcp.server.models import InitializationOptions

from config import (
    __version__,
    __updated__,
    __author__,
    DEFAULT_MODEL,
    MAX_CONTEXT_TOKENS,
)
from tools import ThinkDeeperTool, ReviewCodeTool, DebugIssueTool, AnalyzeTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
server: Server = Server("gemini-server")

# Initialize tools
TOOLS = {
    "think_deeper": ThinkDeeperTool(),
    "review_code": ReviewCodeTool(),
    "debug_issue": DebugIssueTool(),
    "analyze": AnalyzeTool(),
}


def configure_gemini():
    """Configure Gemini API with the provided API key"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is required. "
            "Please set it with your Gemini API key."
        )
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available tools with verbose descriptions"""
    tools = []

    for tool in TOOLS.values():
        tools.append(
            Tool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.get_input_schema(),
            )
        )

    # Add utility tools
    tools.extend(
        [
            Tool(
                name="chat",
                description=(
                    "GENERAL CHAT - Have a conversation with Gemini about any development topic. "
                    "Use for explanations, brainstorming, or general questions. "
                    "Triggers: 'ask gemini', 'explain', 'what is', 'how do I'."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Your question or topic",
                        },
                        "context_files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional files for context",
                        },
                        "temperature": {
                            "type": "number",
                            "description": "Response creativity (0-1, default 0.5)",
                            "minimum": 0,
                            "maximum": 1,
                        },
                    },
                    "required": ["prompt"],
                },
            ),
            Tool(
                name="list_models",
                description=(
                    "LIST AVAILABLE MODELS - Show all Gemini models you can use. "
                    "Lists model names, descriptions, and which one is the default."
                ),
                inputSchema={"type": "object", "properties": {}},
            ),
            Tool(
                name="get_version",
                description=(
                    "VERSION & CONFIGURATION - Get server version, configuration details, "
                    "and list of available tools. Useful for debugging and understanding capabilities."
                ),
                inputSchema={"type": "object", "properties": {}},
            ),
        ]
    )

    return tools


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any]
) -> List[TextContent]:
    """Handle tool execution requests"""

    # Handle dynamic tools
    if name in TOOLS:
        tool = TOOLS[name]
        return await tool.execute(arguments)

    # Handle static tools
    elif name == "chat":
        return await handle_chat(arguments)

    elif name == "list_models":
        return await handle_list_models()

    elif name == "get_version":
        return await handle_get_version()

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def handle_chat(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle general chat requests"""
    from utils import read_files
    from config import TEMPERATURE_BALANCED

    prompt = arguments.get("prompt", "")
    context_files = arguments.get("context_files", [])
    temperature = arguments.get("temperature", TEMPERATURE_BALANCED)

    # Build context if files provided
    full_prompt = prompt
    if context_files:
        file_content, _ = read_files(context_files)
        full_prompt = f"{prompt}\n\n=== CONTEXT FILES ===\n{file_content}\n=== END CONTEXT ==="

    try:
        model = genai.GenerativeModel(
            model_name=DEFAULT_MODEL,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 8192,
                "candidate_count": 1,
            },
        )

        response = model.generate_content(full_prompt)

        if response.candidates and response.candidates[0].content.parts:
            text = response.candidates[0].content.parts[0].text
        else:
            text = "Response blocked or incomplete"

        return [TextContent(type="text", text=text)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error in chat: {str(e)}")]


async def handle_list_models() -> List[TextContent]:
    """List available Gemini models"""
    try:
        import json

        models = []

        for model_info in genai.list_models():
            if (
                hasattr(model_info, "supported_generation_methods")
                and "generateContent"
                in model_info.supported_generation_methods
            ):
                models.append(
                    {
                        "name": model_info.name,
                        "display_name": getattr(
                            model_info, "display_name", "Unknown"
                        ),
                        "description": getattr(
                            model_info, "description", "No description"
                        ),
                        "is_default": model_info.name.endswith(DEFAULT_MODEL),
                    }
                )

        return [TextContent(type="text", text=json.dumps(models, indent=2))]

    except Exception as e:
        return [
            TextContent(type="text", text=f"Error listing models: {str(e)}")
        ]


async def handle_get_version() -> List[TextContent]:
    """Get version and configuration information"""
    version_info = {
        "version": __version__,
        "updated": __updated__,
        "author": __author__,
        "default_model": DEFAULT_MODEL,
        "max_context_tokens": f"{MAX_CONTEXT_TOKENS:,}",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "server_started": datetime.now().isoformat(),
        "available_tools": list(TOOLS.keys())
        + ["chat", "list_models", "get_version"],
    }

    text = f"""Gemini MCP Server v{__version__}
Updated: {__updated__}
Author: {__author__}

Configuration:
- Default Model: {DEFAULT_MODEL}
- Max Context: {MAX_CONTEXT_TOKENS:,} tokens
- Python: {version_info['python_version']}
- Started: {version_info['server_started']}

Available Tools:
{chr(10).join(f"  - {tool}" for tool in version_info['available_tools'])}

For updates, visit: https://github.com/BeehiveInnovations/gemini-mcp-server"""

    return [TextContent(type="text", text=text)]


async def main():
    """Main entry point for the server"""
    # Configure Gemini API
    configure_gemini()

    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="gemini",
                server_version=__version__,
                capabilities={"tools": {}},
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
