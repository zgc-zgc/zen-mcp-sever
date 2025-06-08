#!/usr/bin/env python3
"""
Gemini MCP Server - Model Context Protocol server for Google Gemini
Enhanced for large-scale code analysis with 1M token context window
"""

import asyncio
import json
import os
import sys
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
__version__ = "2.3.0"
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

# Extended thinking system prompt for collaborative analysis
EXTENDED_THINKING_PROMPT = """You are a senior development partner collaborating with Claude Code on complex problems. \
Claude has shared their analysis with you for deeper exploration and validation.

Your role is to:
1. Build upon Claude's thinking - identify gaps, extend ideas, and suggest alternatives
2. Challenge assumptions constructively and identify potential issues
3. Provide concrete, actionable insights that complement Claude's analysis
4. Focus on aspects Claude might have missed or couldn't fully explore
5. Suggest implementation strategies and architectural improvements

Key areas to consider:
- Edge cases and failure modes Claude might have overlooked
- Performance implications at scale
- Security vulnerabilities or attack vectors
- Maintainability and technical debt considerations
- Alternative approaches or design patterns
- Integration challenges with existing systems
- Testing strategies for complex scenarios

Be direct and technical. Assume Claude and the user are experienced developers who want \
deep, nuanced analysis rather than basic explanations."""


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


class FileAnalysisRequest(BaseModel):
    """Request model for file analysis"""

    files: List[str] = Field(..., description="List of file paths to analyze")
    question: str = Field(
        ..., description="Question or analysis request about the files"
    )
    system_prompt: Optional[str] = Field(
        None, description="Optional system prompt for context"
    )
    max_tokens: Optional[int] = Field(
        8192, description="Maximum number of tokens in response"
    )
    temperature: Optional[float] = Field(
        0.2,
        description="Temperature for analysis (0-1, default 0.2 for high accuracy)",
    )
    model: Optional[str] = Field(
        DEFAULT_MODEL, description=f"Model to use (defaults to {DEFAULT_MODEL})"
    )


class ExtendedThinkRequest(BaseModel):
    """Request model for extended thinking with Gemini"""

    thought_process: str = Field(
        ..., description="Claude's analysis, thoughts, plans, or outlines to extend"
    )
    context: Optional[str] = Field(
        None, description="Additional context about the problem or goal"
    )
    files: Optional[List[str]] = Field(
        None, description="Optional file paths for additional context"
    )
    focus: Optional[str] = Field(
        None,
        description="Specific focus area: architecture, bugs, performance, security, etc.",
    )
    system_prompt: Optional[str] = Field(
        None, description="Optional system prompt for context"
    )
    max_tokens: Optional[int] = Field(
        8192, description="Maximum number of tokens in response"
    )
    temperature: Optional[float] = Field(
        0.7,
        description="Temperature for creative thinking (0-1, default 0.7 for balanced creativity)",
    )
    model: Optional[str] = Field(
        DEFAULT_MODEL, description=f"Model to use (defaults to {DEFAULT_MODEL})"
    )


# Create the MCP server instance
server: Server = Server("gemini-server")


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
        summary_parts.append(f"Analyzing {len(files)} file(s):")
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
                        summary_parts.append(f"  {file_path} ({size:,} bytes)")
                        if preview.strip():
                            summary_parts.append(f"     Preview: {preview[:50]}...")
                except Exception:
                    summary_parts.append(f"  {file_path} ({size:,} bytes)")
            else:
                summary_parts.append(f"  {file_path} (not found)")

    # Add direct code
    if code:
        formatted_code = (
            f"\n--- BEGIN DIRECT CODE ---\n{code}\n--- END DIRECT CODE ---\n"
        )
        context_parts.append(formatted_code)
        preview = code[:100] + "..." if len(code) > 100 else code
        summary_parts.append(f"Direct code provided ({len(code):,} characters)")
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
            description="Analyze code files or snippets with Gemini's 1M context window. "
            "For large content, use file paths to avoid terminal clutter.",
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
                        "description": "Direct code content to analyze "
                        "(use for small snippets only; prefer files for large content)",
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
        Tool(
            name="analyze_file",
            description="Analyze files with Gemini - always uses file paths for clean terminal output",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of file paths to analyze",
                    },
                    "question": {
                        "type": "string",
                        "description": "Question or analysis request about the files",
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
                        "description": "Temperature for analysis (0-1, default 0.2 for high accuracy)",
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
                "required": ["files", "question"],
            },
        ),
        Tool(
            name="extended_think",
            description="Collaborate with Gemini on complex problems - share Claude's analysis for deeper insights",
            inputSchema={
                "type": "object",
                "properties": {
                    "thought_process": {
                        "type": "string",
                        "description": "Claude's analysis, thoughts, plans, or outlines to extend",
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context about the problem or goal",
                    },
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional file paths for additional context",
                    },
                    "focus": {
                        "type": "string",
                        "description": "Specific focus area: architecture, bugs, performance, security, etc.",
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
                        "description": "Temperature for creative thinking (0-1, default 0.7)",
                        "default": 0.7,
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "model": {
                        "type": "string",
                        "description": f"Model to use (defaults to {DEFAULT_MODEL})",
                        "default": DEFAULT_MODEL,
                    },
                },
                "required": ["thought_process"],
            },
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
            model_name = request.model or DEFAULT_MODEL
            temperature = (
                request.temperature if request.temperature is not None else 0.5
            )
            max_tokens = request.max_tokens if request.max_tokens is not None else 8192

            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
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
        request_analysis = CodeAnalysisRequest(**arguments)

        # Check that we have either files or code
        if not request_analysis.files and not request_analysis.code:
            return [
                TextContent(
                    type="text",
                    text="Error: Must provide either 'files' or 'code' parameter",
                )
            ]

        try:
            # Prepare code context - always use non-verbose mode for Claude Code compatibility
            code_context, summary = prepare_code_context(
                request_analysis.files, request_analysis.code
            )

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
            model_name = request_analysis.model or DEFAULT_MODEL
            temperature = (
                request_analysis.temperature
                if request_analysis.temperature is not None
                else 0.2
            )
            max_tokens = (
                request_analysis.max_tokens
                if request_analysis.max_tokens is not None
                else 8192
            )

            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "candidate_count": 1,
                },
            )

            # Prepare the full prompt with enhanced developer context and clear structure
            system_prompt = request_analysis.system_prompt or DEVELOPER_SYSTEM_PROMPT
            full_prompt = f"""{system_prompt}

=== USER REQUEST ===
{request_analysis.question}
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

            # Create a brief summary for terminal display
            if request_analysis.files or request_analysis.code:
                # Create a very brief summary for terminal
                brief_summary_parts = []
                if request_analysis.files:
                    brief_summary_parts.append(
                        f"Analyzing {len(request_analysis.files)} file(s)"
                    )
                if request_analysis.code:
                    code_preview = (
                        request_analysis.code[:20] + "..."
                        if len(request_analysis.code) > 20
                        else request_analysis.code
                    )
                    brief_summary_parts.append(f"Direct code: {code_preview}")

                brief_summary = " | ".join(brief_summary_parts)
                response_text = f"{brief_summary}\n\nGemini's Analysis:\n{text}"
            else:
                response_text = text

            return [TextContent(type="text", text=response_text)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing code: {str(e)}")]

    elif name == "list_models":
        try:
            # List available models
            models = []
            for model_info in genai.list_models():
                if (
                    hasattr(model_info, "supported_generation_methods")
                    and "generateContent" in model_info.supported_generation_methods
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
            return [TextContent(type="text", text=f"Error listing models: {str(e)}")]

    elif name == "get_version":
        # Return version and metadata information
        version_info = {
            "version": __version__,
            "updated": __updated__,
            "author": __author__,
            "default_model": DEFAULT_MODEL,
            "max_context_tokens": f"{MAX_CONTEXT_TOKENS:,}",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "server_started": datetime.now().isoformat(),
        }

        return [
            TextContent(
                type="text",
                text=f"""Gemini MCP Server v{__version__}
Updated: {__updated__}
Author: {__author__}

Configuration:
- Default Model: {DEFAULT_MODEL}
- Max Context: {MAX_CONTEXT_TOKENS:,} tokens
- Python: {version_info['python_version']}
- Started: {version_info['server_started']}

For updates, visit: https://github.com/BeehiveInnovations/gemini-mcp-server""",
            )
        ]

    elif name == "analyze_file":
        # Validate request
        request_file = FileAnalysisRequest(**arguments)

        try:
            # Prepare code context from files
            code_context, summary = prepare_code_context(request_file.files, None)

            # Count approximate tokens
            estimated_tokens = len(code_context) // 4
            if estimated_tokens > MAX_CONTEXT_TOKENS:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: File content too large (~{estimated_tokens:,} tokens). "
                        f"Maximum is {MAX_CONTEXT_TOKENS:,} tokens.",
                    )
                ]

            # Use the specified model with optimized settings
            model_name = request_file.model or DEFAULT_MODEL
            temperature = (
                request_file.temperature if request_file.temperature is not None else 0.2
            )
            max_tokens = request_file.max_tokens if request_file.max_tokens is not None else 8192

            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "candidate_count": 1,
                },
            )

            # Prepare prompt
            system_prompt = request_file.system_prompt or DEVELOPER_SYSTEM_PROMPT
            full_prompt = f"""{system_prompt}

=== USER REQUEST ===
{request_file.question}
=== END USER REQUEST ===

=== FILES TO ANALYZE ===
{code_context}
=== END FILES ===

Please analyze the files above and respond to the user's request."""

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

            # Create a brief summary for terminal
            brief_summary = f"Analyzing {len(request_file.files)} file(s)"
            response_text = f"{brief_summary}\n\nGemini's Analysis:\n{text}"

            return [TextContent(type="text", text=response_text)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error analyzing files: {str(e)}")]

    elif name == "extended_think":
        # Validate request
        request_think = ExtendedThinkRequest(**arguments)

        try:
            # Prepare context parts
            context_parts = [
                f"=== CLAUDE'S ANALYSIS ===\n{request_think.thought_process}\n=== END CLAUDE'S ANALYSIS ==="
            ]

            if request_think.context:
                context_parts.append(
                    f"\n=== ADDITIONAL CONTEXT ===\n{request_think.context}\n=== END CONTEXT ==="
                )

            # Add file contents if provided
            if request_think.files:
                file_context, _ = prepare_code_context(request_think.files, None)
                context_parts.append(
                    f"\n=== REFERENCE FILES ===\n{file_context}\n=== END FILES ==="
                )

            full_context = "\n".join(context_parts)

            # Check token limits
            estimated_tokens = len(full_context) // 4
            if estimated_tokens > MAX_CONTEXT_TOKENS:
                return [
                    TextContent(
                        type="text",
                        text=f"Error: Context too large (~{estimated_tokens:,} tokens). "
                        f"Maximum is {MAX_CONTEXT_TOKENS:,} tokens.",
                    )
                ]

            # Use the specified model with creative settings
            model_name = request_think.model or DEFAULT_MODEL
            temperature = (
                request_think.temperature if request_think.temperature is not None else 0.7
            )
            max_tokens = request_think.max_tokens if request_think.max_tokens is not None else 8192

            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "candidate_count": 1,
                },
            )

            # Prepare prompt with focus area if specified
            system_prompt = request_think.system_prompt or EXTENDED_THINKING_PROMPT
            focus_instruction = ""
            if request_think.focus:
                focus_instruction = f"\n\nFOCUS AREA: Please pay special attention to {request_think.focus} aspects."

            full_prompt = f"""{system_prompt}{focus_instruction}

{full_context}

Build upon Claude's analysis with deeper insights, alternative approaches, and critical evaluation."""

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

            # Create response with clear attribution
            response_text = f"Extended Analysis by Gemini:\n\n{text}"

            return [TextContent(type="text", text=response_text)]

        except Exception as e:
            return [
                TextContent(type="text", text=f"Error in extended thinking: {str(e)}")
            ]

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
