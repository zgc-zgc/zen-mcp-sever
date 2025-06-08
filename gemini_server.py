#!/usr/bin/env python3
"""
Gemini MCP Server - Model Context Protocol server for Google Gemini
Enhanced for large-scale code analysis with 1M token context window
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import google.generativeai as genai
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

# Version and metadata
__version__ = "2.2.0"
__updated__ = "2025-06-08"
__author__ = "Fahad Gilani"

# Default to Gemini 2.5 Pro Preview with maximum context
DEFAULT_MODEL = "gemini-2.5-pro-preview-06-05"
MAX_CONTEXT_TOKENS = 1000000  # 1M tokens

# Developer-focused system prompt for Claude Code usage
DEVELOPER_SYSTEM_PROMPT = """You are an expert software developer assistant working alongside Claude Code. \
Your role is to extend Claude's capabilities when handling large codebases or complex analysis tasks.

Core competencies:
- Deep understanding of software architecture and design patterns
- Expert-level debugging and root cause analysis
- Performance optimization and scalability considerations
- Security best practices and vulnerability identification
- Clean code principles and refactoring strategies
- Comprehensive testing approaches (unit, integration, e2e)
- Modern development practices (CI/CD, DevOps, cloud-native)
- Cross-platform and cross-language expertise

Your approach:
- Be precise and technical, avoiding unnecessary explanations
- Provide actionable, concrete solutions with code examples
- Consider edge cases and potential issues proactively
- Focus on maintainability, readability, and long-term sustainability
- Suggest modern, idiomatic solutions for the given language/framework
- When reviewing code, prioritize critical issues first
- Always validate your suggestions against best practices

Remember: You're augmenting Claude Code's capabilities, especially for tasks requiring \
extensive context or deep analysis that might exceed Claude's token limits."""


class GeminiChatRequest(BaseModel):
    """Request model for Gemini chat"""

    prompt: str = Field(..., description="The prompt to send to Gemini")
    system_prompt: Optional[str] = Field(
        None, description="Optional system prompt for context"
    )
    max_tokens: Optional[int] = Field(
        8192, description="Maximum number of tokens in response"
    )
    temperature: Optional[float] = Field(
        0.5,
        description="Temperature for response randomness (0-1, default 0.5 for balanced accuracy/creativity)",
    )
    model: Optional[str] = Field(
        DEFAULT_MODEL, description=f"Model to use (defaults to {DEFAULT_MODEL})"
    )


class CodeAnalysisRequest(BaseModel):
    """Request model for code analysis"""

    files: Optional[List[str]] = Field(
        None, description="List of file paths to analyze"
    )
    code: Optional[str] = Field(None, description="Direct code content to analyze")
    question: str = Field(
        ..., description="Question or analysis request about the code"
    )
    system_prompt: Optional[str] = Field(
        None, description="Optional system prompt for context"
    )
    max_tokens: Optional[int] = Field(
        8192, description="Maximum number of tokens in response"
    )
    temperature: Optional[float] = Field(
        0.2,
        description="Temperature for code analysis (0-1, default 0.2 for high accuracy)",
    )
    model: Optional[str] = Field(
        DEFAULT_MODEL, description=f"Model to use (defaults to {DEFAULT_MODEL})"
    )
    verbose_output: Optional[bool] = Field(
        False, description="Show file contents in terminal output"
    )


# Create the MCP server instance
server = Server("gemini-server")


# Configure Gemini API
def configure_gemini():
    """Configure the Gemini API with API key from environment"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)


def read_file_content(file_path: str) -> str:
    """Read content from a file with error handling - for backward compatibility"""
    return read_file_content_for_gemini(file_path)


def read_file_content_for_gemini(file_path: str) -> str:
    """Read content from a file with proper formatting for Gemini"""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"\n--- FILE NOT FOUND: {file_path} ---\nError: File does not exist\n--- END FILE ---\n"
        if not path.is_file():
            return f"\n--- NOT A FILE: {file_path} ---\nError: Path is not a file\n--- END FILE ---\n"

        # Read the file
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Format with clear delimiters for Gemini
        return f"\n--- BEGIN FILE: {file_path} ---\n{content}\n--- END FILE: {file_path} ---\n"
    except Exception as e:
        return f"\n--- ERROR READING FILE: {file_path} ---\nError: {str(e)}\n--- END FILE ---\n"


def prepare_code_context(
    files: Optional[List[str]], code: Optional[str]
) -> Tuple[str, str]:
    """Prepare code context from files and/or direct code
    Returns: (context_for_gemini, summary_for_terminal)
    """
    context_parts = []
    summary_parts = []

    # Add file contents
    if files:
        summary_parts.append(f"📁 Analyzing {len(files)} file(s):")
        for file_path in files:
            # Get file content for Gemini
            file_content = read_file_content_for_gemini(file_path)
            context_parts.append(file_content)

            # Create summary with small excerpt for terminal
            path = Path(file_path)
            if path.exists() and path.is_file():
                size = path.stat().st_size
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        # Read first few lines for preview
                        preview_lines = []
                        for i, line in enumerate(f):
                            if i >= 3:  # Show max 3 lines
                                break
                            preview_lines.append(line.rstrip())
                        preview = "\n".join(preview_lines)
                        if len(preview) > 100:
                            preview = preview[:100] + "..."
                        summary_parts.append(f"  📄 {file_path} ({size:,} bytes)")
                        if preview.strip():
                            summary_parts.append(f"     Preview: {preview[:50]}...")
                except Exception:
                    summary_parts.append(f"  📄 {file_path} ({size:,} bytes)")
            else:
                summary_parts.append(f"  ❌ {file_path} (not found)")

    # Add direct code
    if code:
        formatted_code = (
            f"\n--- BEGIN DIRECT CODE ---\n{code}\n--- END DIRECT CODE ---\n"
        )
        context_parts.append(formatted_code)
        preview = code[:100] + "..." if len(code) > 100 else code
        summary_parts.append(f"💻 Direct code provided ({len(code):,} characters)")
        summary_parts.append(f"     Preview: {preview}")

    full_context = "\n\n".join(context_parts)
    summary = "\n".join(summary_parts)

    return full_context, summary


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="chat",
            description="Chat with Gemini (optimized for 2.5 Pro with 1M context)",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to send to Gemini",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional system prompt for context",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum number of tokens in response",
                        "default": 8192,
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Temperature for response randomness (0-1, default 0.5 for "
                        "balanced accuracy/creativity)",
                        "default": 0.5,
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "model": {
                        "type": "string",
                        "description": f"Model to use (defaults to {DEFAULT_MODEL})",
                        "default": DEFAULT_MODEL,
                    },
                },
                "required": ["prompt"],
            },
        ),
        Tool(
            name="analyze_code",
            description="Analyze code files or snippets with Gemini's 1M context window",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of file paths to analyze",
                    },
                    "code": {
                        "type": "string",
                        "description": "Direct code content to analyze (alternative to files)",
                    },
                    "question": {
                        "type": "string",
                        "description": "Question or analysis request about the code",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional system prompt for context",
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum number of tokens in response",
                        "default": 8192,
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Temperature for code analysis (0-1, default 0.2 for high accuracy)",
                        "default": 0.2,
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "model": {
                        "type": "string",
                        "description": f"Model to use (defaults to {DEFAULT_MODEL})",
                        "default": DEFAULT_MODEL,
                    },
                },
                "required": ["question"],
            },
        ),
        Tool(
            name="list_models",
            description="List available Gemini models",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_version",
            description="Get the version and metadata of the Gemini MCP Server",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool execution requests"""

    if name == "chat":
        # Validate request
        request = GeminiChatRequest(**arguments)

        try:
            # Use the specified model with optimized settings
            model = genai.GenerativeModel(
                model_name=request.model,
                generation_config={
                    "temperature": request.temperature,
                    "max_output_tokens": request.max_tokens,
                    "candidate_count": 1,
                },
            )

            # Prepare the prompt with automatic developer context if no system prompt provided
            if request.system_prompt:
                full_prompt = f"{request.system_prompt}\n\n{request.prompt}"
            else:
                # Auto-inject developer system prompt for better Claude Code integration
                full_prompt = f"{DEVELOPER_SYSTEM_PROMPT}\n\n{request.prompt}"

            # Generate response
            response = model.generate_content(full_prompt)

            # Handle response based on finish reason
            if response.candidates and response.candidates[0].content.parts:
                text = response.candidates[0].content.parts[0].text
            else:
                # Handle safety filters or other issues
                finish_reason = (
                    response.candidates[0].finish_reason
                    if response.candidates
                    else "Unknown"
                )
                text = f"Response blocked or incomplete. Finish reason: {finish_reason}"

            return [TextContent(type="text", text=text)]

        except Exception as e:
            return [
                TextContent(type="text", text=f"Error calling Gemini API: {str(e)}")
            ]

    elif name == "analyze_code":
        # Validate request
        request = CodeAnalysisRequest(**arguments)

        # Check that we have either files or code
        if not request.files and not request.code:
            return [
                TextContent(
                    type="text",
                    text="Error: Must provide either 'files' or 'code' parameter",
                )
            ]

        try:
            # Prepare code context - always use non-verbose mode for Claude Code compatibility
            code_context, summary = prepare_code_context(request.files, request.code)

            # Count approximate tokens (rough estimate: 1 token ≈ 4 characters)
            estimated_tokens = len(code_context) // 4
            if estimated_tokens > MAX_CONTEXT_TOKENS:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: Code context too large (~{estimated_tokens:,} tokens). "
                        f"Maximum is {MAX_CONTEXT_TOKENS:,} tokens.",
                    )
                ]

            # Use the specified model with optimized settings for code analysis
            model = genai.GenerativeModel(
                model_name=request.model,
                generation_config={
                    "temperature": request.temperature,
                    "max_output_tokens": request.max_tokens,
                    "candidate_count": 1,
                },
            )

            # Prepare the full prompt with enhanced developer context and clear structure
            system_prompt = request.system_prompt or DEVELOPER_SYSTEM_PROMPT
            full_prompt = f"""{system_prompt}

=== USER REQUEST ===
{request.question}
=== END USER REQUEST ===

=== CODE TO ANALYZE ===
{code_context}
=== END CODE TO ANALYZE ===

Please analyze the code above and respond to the user's request. The code files are clearly \
marked with their paths and content boundaries."""

            # Generate response
            response = model.generate_content(full_prompt)

            # Handle response
            if response.candidates and response.candidates[0].content.parts:
                text = response.candidates[0].content.parts[0].text
            else:
                finish_reason = (
                    response.candidates[0].finish_reason
                    if response.candidates
                    else "Unknown"
                )
                text = f"Response blocked or incomplete. Finish reason: {finish_reason}"

            # Always return response with summary for Claude Code compatibility
            if request.files or request.code:
                response_text = f"{summary}\n\n🤖 Gemini's Analysis:\n{text}"
            else:
                response_text = text

            return [TextContent(type="text", text=response_text)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing code: {str(e)}")]

    elif name == "list_models":
        try:
            # List available models
            models = []
            for model in genai.list_models():
                if "generateContent" in model.supported_generation_methods:
                    models.append(
                        {
                            "name": model.name,
                            "display_name": model.display_name,
                            "description": model.description,
                            "is_default": model.name == DEFAULT_MODEL,
                        }
                    )

            return [TextContent(type="text", text=json.dumps(models, indent=2))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error listing models: {str(e)}")]

    elif name == "get_version":
        # Return version and metadata information
        version_info = {
            "version": __version__,
            "updated": __updated__,
            "author": __author__,
            "default_model": DEFAULT_MODEL,
            "max_context_tokens": f"{MAX_CONTEXT_TOKENS:,}",
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "server_started": datetime.now().isoformat(),
        }
        
        return [TextContent(
            type="text",
            text=f"""🤖 Gemini MCP Server v{__version__}
Updated: {__updated__}
Author: {__author__}

Configuration:
• Default Model: {DEFAULT_MODEL}
• Max Context: {MAX_CONTEXT_TOKENS:,} tokens
• Python: {version_info['python_version']}
• Started: {version_info['server_started']}

For updates, visit: https://github.com/BeehiveInnovations/gemini-mcp-server"""
        )]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


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
                server_name="gemini", server_version="2.0.0", capabilities={"tools": {}}
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
