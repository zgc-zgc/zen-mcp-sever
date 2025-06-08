"""
Test that imports work correctly when package is installed
This helps verify CI setup is correct
"""

import pytest


def test_direct_import():
    """Test that gemini_server can be imported directly"""
    try:
        import gemini_server

        assert hasattr(gemini_server, "GeminiChatRequest")
        assert hasattr(gemini_server, "CodeAnalysisRequest")
        assert hasattr(gemini_server, "handle_list_tools")
        assert hasattr(gemini_server, "handle_call_tool")
    except ImportError as e:
        pytest.fail(f"Failed to import gemini_server: {e}")


def test_from_import():
    """Test that specific items can be imported from gemini_server"""
    try:
        from gemini_server import (
            GeminiChatRequest,
            CodeAnalysisRequest,
            DEFAULT_MODEL,
            DEVELOPER_SYSTEM_PROMPT,
        )

        assert GeminiChatRequest is not None
        assert CodeAnalysisRequest is not None
        assert isinstance(DEFAULT_MODEL, str)
        assert isinstance(DEVELOPER_SYSTEM_PROMPT, str)
    except ImportError as e:
        pytest.fail(f"Failed to import from gemini_server: {e}")


def test_google_generativeai_import():
    """Test that google.generativeai can be imported"""
    try:
        import google.generativeai as genai

        assert hasattr(genai, "GenerativeModel")
        assert hasattr(genai, "configure")
    except ImportError as e:
        pytest.fail(f"Failed to import google.generativeai: {e}")
