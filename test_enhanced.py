#!/usr/bin/env python3
"""
Enhanced test script for Gemini MCP Server with code analysis features
"""

import os
import asyncio
import json
from pathlib import Path
from gemini_server import configure_gemini, handle_call_tool, handle_list_tools


async def test_enhanced_features():
    """Test the enhanced server functionality"""
    print("Testing Enhanced Gemini MCP Server...")
    print("-" * 50)
    
    # Test configuration
    try:
        configure_gemini()
        print("✓ Gemini API configured successfully")
    except Exception as e:
        print(f"✗ Failed to configure Gemini API: {e}")
        return
    
    # Test listing tools (should now include analyze_code)
    print("\n1. Testing list_tools...")
    tools = await handle_list_tools()
    print(f"✓ Found {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Test chat with 2.5 Pro Preview default
    print("\n2. Testing chat with default 2.5 Pro Preview...")
    chat_result = await handle_call_tool("chat", {
        "prompt": "What model are you? Please confirm you're Gemini 2.5 Pro Preview.",
        "temperature": 0.3,
        "max_tokens": 200
    })
    print("✓ Chat response:")
    print(chat_result[0].text[:200] + "..." if len(chat_result[0].text) > 200 else chat_result[0].text)
    
    # Create a test file for code analysis
    test_file = Path("test_sample.py")
    test_code = '''def fibonacci(n):
    """Calculate fibonacci number at position n"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    """Calculate factorial of n"""
    if n <= 1:
        return 1
    return n * factorial(n-1)

# Test the functions
print(f"Fibonacci(10): {fibonacci(10)}")
print(f"Factorial(5): {factorial(5)}")
'''
    
    with open(test_file, 'w') as f:
        f.write(test_code)
    
    # Test analyze_code with file
    print("\n3. Testing analyze_code with file...")
    analysis_result = await handle_call_tool("analyze_code", {
        "files": [str(test_file)],
        "question": "What are the time complexities of these functions? Can you suggest optimizations?",
        "temperature": 0.3,
        "max_tokens": 500
    })
    print("✓ Code analysis response:")
    print(analysis_result[0].text[:400] + "..." if len(analysis_result[0].text) > 400 else analysis_result[0].text)
    
    # Test analyze_code with direct code
    print("\n4. Testing analyze_code with direct code...")
    analysis_result = await handle_call_tool("analyze_code", {
        "code": "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        return self.items.pop() if self.items else None",
        "question": "Is this a good implementation of a stack? What improvements would you suggest?",
        "temperature": 0.3
    })
    print("✓ Direct code analysis response:")
    print(analysis_result[0].text[:400] + "..." if len(analysis_result[0].text) > 400 else analysis_result[0].text)
    
    # Test large context (simulate)
    print("\n5. Testing context size estimation...")
    large_code = "x = 1\n" * 100000  # ~600K characters, ~150K tokens
    analysis_result = await handle_call_tool("analyze_code", {
        "code": large_code,
        "question": "How many assignment statements are in this code?",
        "temperature": 0.1
    })
    print("✓ Large context test:")
    print(analysis_result[0].text[:200] + "..." if len(analysis_result[0].text) > 200 else analysis_result[0].text)
    
    # Clean up test file
    test_file.unlink()
    
    print("\n" + "-" * 50)
    print("All enhanced tests completed!")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set")
        print("Please set it with: export GEMINI_API_KEY='your-api-key'")
        exit(1)
    
    asyncio.run(test_enhanced_features())