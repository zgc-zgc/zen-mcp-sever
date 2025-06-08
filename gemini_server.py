#!/usr/bin/env python3
"""
Gemini MCP Server - Model Context Protocol server for Google Gemini
Enhanced for large-scale code analysis with 1M token context window
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field
import google.generativeai as genai


# Default to Gemini 2.5 Pro Preview with maximum context
DEFAULT_MODEL = "gemini-2.5-pro-preview-06-05"
MAX_CONTEXT_TOKENS = 1000000  # 1M tokens

# Developer-focused system prompt for Claude Code usage
DEVELOPER_SYSTEM_PROMPT = """You are an expert software developer assistant working alongside Claude Code. Your role is to extend Claude's capabilities when handling large codebases or complex analysis tasks.

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

Remember: You're augmenting Claude Code's capabilities, especially for tasks requiring extensive context or deep analysis that might exceed Claude's token limits."""


class GeminiChatRequest(BaseModel):
    """Request model for Gemini chat"""
    prompt: str = Field(..., description="The prompt to send to Gemini")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt for context")
    max_tokens: Optional[int] = Field(8192, description="Maximum number of tokens in response")
    temperature: Optional[float] = Field(0.5, description="Temperature for response randomness (0-1, default 0.5 for balanced accuracy/creativity)")
    model: Optional[str] = Field(DEFAULT_MODEL, description=f"Model to use (defaults to {DEFAULT_MODEL})")


class CodeAnalysisRequest(BaseModel):
    """Request model for code analysis"""
    files: Optional[List[str]] = Field(None, description="List of file paths to analyze")
    code: Optional[str] = Field(None, description="Direct code content to analyze")
    question: str = Field(..., description="Question or analysis request about the code")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt for context")
    max_tokens: Optional[int] = Field(8192, description="Maximum number of tokens in response")
    temperature: Optional[float] = Field(0.2, description="Temperature for code analysis (0-1, default 0.2 for high accuracy)")
    model: Optional[str] = Field(DEFAULT_MODEL, description=f"Model to use (defaults to {DEFAULT_MODEL})")


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
    """Read content from a file with error handling"""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"Error: File not found: {file_path}"
        if not path.is_file():
            return f"Error: Not a file: {file_path}"
        
        # Read the file
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"=== File: {file_path} ===\n{content}\n"
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"


def prepare_code_context(files: Optional[List[str]], code: Optional[str]) -> str:
    """Prepare code context from files and/or direct code"""
    context_parts = []
    
    # Add file contents
    if files:
        for file_path in files:
            context_parts.append(read_file_content(file_path))
    
    # Add direct code
    if code:
        context_parts.append("=== Direct Code ===\n" + code + "\n")
    
    return "\n".join(context_parts)


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
                        "description": "The prompt to send to Gemini"
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional system prompt for context"
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum number of tokens in response",
                        "default": 8192
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Temperature for response randomness (0-1, default 0.5 for balanced accuracy/creativity)",
                        "default": 0.5,
                        "minimum": 0,
                        "maximum": 1
                    },
                    "model": {
                        "type": "string",
                        "description": f"Model to use (defaults to {DEFAULT_MODEL})",
                        "default": DEFAULT_MODEL
                    }
                },
                "required": ["prompt"]
            }
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
                        "description": "List of file paths to analyze"
                    },
                    "code": {
                        "type": "string",
                        "description": "Direct code content to analyze (alternative to files)"
                    },
                    "question": {
                        "type": "string",
                        "description": "Question or analysis request about the code"
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional system prompt for context"
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum number of tokens in response",
                        "default": 8192
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Temperature for code analysis (0-1, default 0.2 for high accuracy)",
                        "default": 0.2,
                        "minimum": 0,
                        "maximum": 1
                    },
                    "model": {
                        "type": "string",
                        "description": f"Model to use (defaults to {DEFAULT_MODEL})",
                        "default": DEFAULT_MODEL
                    }
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="list_models",
            description="List available Gemini models",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
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
                }
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
                finish_reason = response.candidates[0].finish_reason if response.candidates else "Unknown"
                text = f"Response blocked or incomplete. Finish reason: {finish_reason}"
            
            return [TextContent(
                type="text",
                text=text
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error calling Gemini API: {str(e)}"
            )]
    
    elif name == "analyze_code":
        # Validate request
        request = CodeAnalysisRequest(**arguments)
        
        # Check that we have either files or code
        if not request.files and not request.code:
            return [TextContent(
                type="text",
                text="Error: Must provide either 'files' or 'code' parameter"
            )]
        
        try:
            # Prepare code context
            code_context = prepare_code_context(request.files, request.code)
            
            # Count approximate tokens (rough estimate: 1 token ≈ 4 characters)
            estimated_tokens = len(code_context) // 4
            if estimated_tokens > MAX_CONTEXT_TOKENS:
                return [TextContent(
                    type="text",
                    text=f"Error: Code context too large (~{estimated_tokens:,} tokens). Maximum is {MAX_CONTEXT_TOKENS:,} tokens."
                )]
            
            # Use the specified model with optimized settings for code analysis
            model = genai.GenerativeModel(
                model_name=request.model,
                generation_config={
                    "temperature": request.temperature,
                    "max_output_tokens": request.max_tokens,
                    "candidate_count": 1,
                }
            )
            
            # Prepare the full prompt with enhanced developer context
            system_prompt = request.system_prompt or DEVELOPER_SYSTEM_PROMPT
            full_prompt = f"{system_prompt}\n\nCode to analyze:\n\n{code_context}\n\nQuestion/Request: {request.question}"
            
            # Generate response
            response = model.generate_content(full_prompt)
            
            # Handle response
            if response.candidates and response.candidates[0].content.parts:
                text = response.candidates[0].content.parts[0].text
            else:
                finish_reason = response.candidates[0].finish_reason if response.candidates else "Unknown"
                text = f"Response blocked or incomplete. Finish reason: {finish_reason}"
            
            return [TextContent(
                type="text",
                text=text
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error analyzing code: {str(e)}"
            )]
    
    elif name == "list_models":
        try:
            # List available models
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append({
                        "name": model.name,
                        "display_name": model.display_name,
                        "description": model.description,
                        "is_default": model.name == DEFAULT_MODEL
                    })
            
            return [TextContent(
                type="text",
                text=json.dumps(models, indent=2)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error listing models: {str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


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
                server_version="2.0.0",
                capabilities={
                    "tools": {}
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(main())