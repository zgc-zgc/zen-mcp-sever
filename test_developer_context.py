#!/usr/bin/env python3
"""
Test script to verify developer context is properly injected
"""

import os
import asyncio
from gemini_server import configure_gemini, handle_call_tool


async def test_developer_context():
    """Test the developer context system prompt"""
    print("Testing Developer Context in Gemini MCP Server...")
    print("-" * 50)
    
    # Test configuration
    try:
        configure_gemini()
        print("✓ Gemini API configured successfully")
    except Exception as e:
        print(f"✗ Failed to configure Gemini API: {e}")
        return
    
    # Test 1: Chat without explicit system prompt (should use developer prompt)
    print("\n1. Testing chat WITHOUT system prompt (should auto-inject developer context)...")
    result = await handle_call_tool("chat", {
        "prompt": "Write a Python function to reverse a linked list. Include comments.",
        "temperature": 0.3,
        "max_tokens": 500
    })
    print("Response preview:")
    print(result[0].text[:400] + "..." if len(result[0].text) > 400 else result[0].text)
    
    # Test 2: Chat WITH explicit system prompt (should use provided prompt)
    print("\n2. Testing chat WITH custom system prompt...")
    result = await handle_call_tool("chat", {
        "prompt": "Write a haiku about coding",
        "system_prompt": "You are a creative poet who writes about technology.",
        "temperature": 0.9,
        "max_tokens": 100
    })
    print("Response:")
    print(result[0].text)
    
    # Test 3: Code analysis without system prompt (should use developer prompt)
    print("\n3. Testing analyze_code WITHOUT system prompt...")
    test_code = '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
'''
    
    result = await handle_call_tool("analyze_code", {
        "code": test_code,
        "question": "Review this code and suggest improvements",
        "temperature": 0.3
    })
    print("Response preview:")
    print(result[0].text[:500] + "..." if len(result[0].text) > 500 else result[0].text)
    
    # Test 4: Code analysis WITH custom system prompt
    print("\n4. Testing analyze_code WITH custom system prompt...")
    result = await handle_call_tool("analyze_code", {
        "code": test_code,
        "question": "Is this code correct?",
        "system_prompt": "You are a beginner-friendly tutor. Explain things simply.",
        "temperature": 0.5
    })
    print("Response preview:")
    print(result[0].text[:400] + "..." if len(result[0].text) > 400 else result[0].text)
    
    print("\n" + "-" * 50)
    print("Developer context tests completed!")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set")
        print("Please set it with: export GEMINI_API_KEY='your-api-key'")
        exit(1)
    
    asyncio.run(test_developer_context())