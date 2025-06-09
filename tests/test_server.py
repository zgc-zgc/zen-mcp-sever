"""
Tests for the main server functionality
"""

import json
from unittest.mock import Mock, patch

import pytest

from server import handle_call_tool, handle_list_tools


class TestServerTools:
    """Test server tool handling"""

    @pytest.mark.asyncio
    async def test_handle_list_tools(self):
        """Test listing all available tools"""
        tools = await handle_list_tools()
        tool_names = [tool.name for tool in tools]

        # Check all core tools are present
        assert "think_deeper" in tool_names
        assert "review_code" in tool_names
        assert "debug_issue" in tool_names
        assert "analyze" in tool_names
        assert "chat" in tool_names
        assert "list_models" in tool_names
        assert "get_version" in tool_names

        # Should have exactly 7 tools
        assert len(tools) == 7

        # Check descriptions are verbose
        for tool in tools:
            assert (
                len(tool.description) > 50
            )  # All should have detailed descriptions

    @pytest.mark.asyncio
    async def test_handle_call_tool_unknown(self):
        """Test calling an unknown tool"""
        result = await handle_call_tool("unknown_tool", {})
        assert len(result) == 1
        assert "Unknown tool: unknown_tool" in result[0].text

    @pytest.mark.asyncio
    @patch("google.generativeai.GenerativeModel")
    async def test_handle_chat(self, mock_model):
        """Test chat functionality"""
        # Mock response
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [
            Mock(text="Chat response")
        ]

        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance

        result = await handle_call_tool("chat", {"prompt": "Hello Gemini"})

        assert len(result) == 1
        assert result[0].text == "Chat response"

    @pytest.mark.asyncio
    @patch("google.generativeai.list_models")
    async def test_handle_list_models(self, mock_list_models):
        """Test listing models"""
        # Mock model data
        mock_model = Mock()
        mock_model.name = "models/gemini-2.5-pro-preview-06-05"
        mock_model.display_name = "Gemini 2.5 Pro"
        mock_model.description = "Latest Gemini model"
        mock_model.supported_generation_methods = ["generateContent"]

        mock_list_models.return_value = [mock_model]

        result = await handle_call_tool("list_models", {})
        assert len(result) == 1

        models = json.loads(result[0].text)
        assert len(models) == 1
        assert models[0]["name"] == "models/gemini-2.5-pro-preview-06-05"
        assert models[0]["is_default"] is True

    @pytest.mark.asyncio
    async def test_handle_get_version(self):
        """Test getting version info"""
        result = await handle_call_tool("get_version", {})
        assert len(result) == 1

        response = result[0].text
        assert "Gemini MCP Server v" in response  # Version agnostic check
        assert "Available Tools:" in response
        assert "think_deeper" in response
