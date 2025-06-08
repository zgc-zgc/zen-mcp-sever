#!/usr/bin/env python3
"""
Test script for Gemini MCP Server
"""

import os
import asyncio
import json
from gemini_server import configure_gemini, handle_call_tool, handle_list_tools


async def test_server():
    """Test the server functionality"""
    print("Testing Gemini MCP Server...")
    print("-" * 50)
    
    # Test configuration
    try:
        configure_gemini()
        print("✓ Gemini API configured successfully")
    except Exception as e:
        print(f"✗ Failed to configure Gemini API: {e}")
        return
    
    # Test listing tools
    print("\n1. Testing list_tools...")
    tools = await handle_list_tools()
    print(f"✓ Found {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Test list_models
    print("\n2. Testing list_models tool...")
    models_result = await handle_call_tool("list_models", {})
    print("✓ Available models:")
    print(models_result[0].text)
    
    # Test chat
    print("\n3. Testing chat tool...")
    chat_result = await handle_call_tool("chat", {
        "prompt": "What is the capital of France?",
        "temperature": 0.3,
        "max_tokens": 50
    })
    print("✓ Chat response:")
    print(chat_result[0].text)
    
    # Test chat with system prompt
    print("\n4. Testing chat with system prompt...")
    chat_result = await handle_call_tool("chat", {
        "prompt": "What's 2+2?",
        "system_prompt": "You are a helpful math tutor. Always explain your reasoning step by step.",
        "temperature": 0.3,
        "max_tokens": 200
    })
    print("✓ Chat response with system prompt:")
    print(chat_result[0].text)
    
    print("\n" + "-" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set")
        print("Please set it with: export GEMINI_API_KEY='your-api-key'")
        exit(1)
    
    asyncio.run(test_server())