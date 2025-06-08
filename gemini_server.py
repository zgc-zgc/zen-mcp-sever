#!/usr/bin/env python3
"""
Gemini MCP Server - Model Context Protocol server for Google Gemini
"""

import os
import json
import asyncio
from typing import Optional, Dict, Any, List
from mcp.server.models import InitializationOptions
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field
import google.generativeai as genai


class GeminiChatRequest(BaseModel):
    """Request model for Gemini chat"""
    prompt: str = Field(..., description="The prompt to send to Gemini")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt for context")
    max_tokens: Optional[int] = Field(4096, description="Maximum number of tokens in response")
    temperature: Optional[float] = Field(0.7, description="Temperature for response randomness (0-1)")
    model: Optional[str] = Field("gemini-1.5-pro-latest", description="Model to use (defaults to gemini-1.5-pro-latest)")


# Create the MCP server instance
server = Server("gemini-server")


# Configure Gemini API
def configure_gemini():
    """Configure the Gemini API with API key from environment"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="chat",
            description="Chat with Gemini Pro 2.5 model",
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
                        "default": 4096
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Temperature for response randomness (0-1)",
                        "default": 0.7,
                        "minimum": 0,
                        "maximum": 1
                    },
                    "model": {
                        "type": "string",
                        "description": "Model to use (e.g., gemini-1.5-pro-latest, gemini-2.5-pro-preview-06-05)",
                        "default": "gemini-1.5-pro-latest"
                    }
                },
                "required": ["prompt"]
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
            # Use the specified model or default to 1.5 Pro
            model = genai.GenerativeModel(
                model_name=request.model,
                generation_config={
                    "temperature": request.temperature,
                    "max_output_tokens": request.max_tokens,
                }
            )
            
            # Prepare the prompt
            full_prompt = request.prompt
            if request.system_prompt:
                full_prompt = f"{request.system_prompt}\n\n{request.prompt}"
            
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
    
    elif name == "list_models":
        try:
            # List available models
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append({
                        "name": model.name,
                        "display_name": model.display_name,
                        "description": model.description
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
                server_version="1.0.0",
                capabilities={
                    "tools": {}
                }
            )
        )


if __name__ == "__main__":
    asyncio.run(main())