#!/usr/bin/env python3
"""
Test script for optimized Claude Code settings
"""

import os
import asyncio
from gemini_server import configure_gemini, handle_call_tool


async def test_optimized_settings():
    """Test the optimized temperature and developer settings"""
    print("Testing Optimized Claude Code Settings...")
    print("-" * 50)
    
    # Test configuration
    try:
        configure_gemini()
        print("✓ Gemini API configured successfully")
    except Exception as e:
        print(f"✗ Failed to configure Gemini API: {e}")
        return
    
    # Test 1: Default chat temperature (should be 0.5)
    print("\n1. Testing chat with default temperature (0.5)...")
    result = await handle_call_tool("chat", {
        "prompt": "Explain the concept of dependency injection in one paragraph. Be concise but thorough."
    })
    print("Response preview (should be balanced - accurate but not robotic):")
    print(result[0].text[:300] + "..." if len(result[0].text) > 300 else result[0].text)
    
    # Test 2: Code analysis with low temperature (0.2)
    print("\n2. Testing code analysis with default low temperature (0.2)...")
    code = '''
async def fetch_user_data(user_id: str, cache=None):
    if cache and user_id in cache:
        return cache[user_id]
    
    response = await http_client.get(f"/api/users/{user_id}")
    user_data = response.json()
    
    if cache:
        cache[user_id] = user_data
    
    return user_data
'''
    
    result = await handle_call_tool("analyze_code", {
        "code": code,
        "question": "Identify potential issues and suggest improvements"
    })
    print("Response preview (should be precise and technical):")
    print(result[0].text[:400] + "..." if len(result[0].text) > 400 else result[0].text)
    
    # Test 3: Creative task with higher temperature
    print("\n3. Testing creative task with custom higher temperature...")
    result = await handle_call_tool("chat", {
        "prompt": "Suggest 3 innovative ways to implement a rate limiter",
        "temperature": 0.8
    })
    print("Response preview (should be more creative):")
    print(result[0].text[:400] + "..." if len(result[0].text) > 400 else result[0].text)
    
    # Test 4: Verify developer context is applied
    print("\n4. Testing developer context (no system prompt)...")
    result = await handle_call_tool("chat", {
        "prompt": "What's the time complexity of quicksort?",
        "temperature": 0.3
    })
    print("Response (should be technical and developer-focused):")
    print(result[0].text[:300] + "..." if len(result[0].text) > 300 else result[0].text)
    
    print("\n" + "-" * 50)
    print("Optimized settings test completed!")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set")
        print("Please set it with: export GEMINI_API_KEY='your-api-key'")
        exit(1)
    
    asyncio.run(test_optimized_settings())