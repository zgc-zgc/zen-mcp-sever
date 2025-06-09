"""
Tests for MAX_OUTPUT_TOKENS configuration
"""

from unittest.mock import Mock, patch

import pytest

from config import MAX_OUTPUT_TOKENS
from tools.base import BaseTool, ToolRequest


class TestMaxOutputTokens:
    """Test that MAX_OUTPUT_TOKENS is properly applied"""

    def test_max_output_tokens_value(self):
        """Test the MAX_OUTPUT_TOKENS constant value"""
        assert MAX_OUTPUT_TOKENS == 32_768

    def test_tool_request_default_max_tokens(self):
        """Test that ToolRequest has correct default max_tokens"""
        request = ToolRequest()
        assert request.max_tokens == MAX_OUTPUT_TOKENS

    @pytest.mark.asyncio
    @patch("google.generativeai.GenerativeModel")
    async def test_base_tool_uses_max_output_tokens(self, mock_model):
        """Test that BaseTool properly uses MAX_OUTPUT_TOKENS in model creation"""

        # Create a concrete implementation of BaseTool for testing
        class TestTool(BaseTool):
            def get_name(self):
                return "test_tool"

            def get_description(self):
                return "Test tool"

            def get_input_schema(self):
                return {
                    "type": "object",
                    "properties": {
                        "test": {"type": "string"}
                    },
                    "required": ["test"]
                }

            def get_system_prompt(self):
                return "Test prompt"

            def get_request_model(self):
                class TestRequest(ToolRequest):
                    test: str
                return TestRequest

            async def prepare_prompt(self, request):
                return f"Test: {request.test}"

        # Mock response
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock(text="Test response")]

        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance

        # Execute tool
        tool = TestTool()
        await tool.execute({"test": "value"})

        # Verify model was created with MAX_OUTPUT_TOKENS
        mock_model.assert_called_once()
        call_args = mock_model.call_args

        # Check generation_config
        assert "generation_config" in call_args[1]
        config = call_args[1]["generation_config"]
        assert config["max_output_tokens"] == MAX_OUTPUT_TOKENS

    @pytest.mark.asyncio
    @patch("google.generativeai.GenerativeModel")
    async def test_custom_max_tokens_override(self, mock_model):
        """Test that custom max_tokens value overrides the default"""

        class TestTool(BaseTool):
            def get_name(self):
                return "test_tool"

            def get_description(self):
                return "Test tool"

            def get_input_schema(self):
                return {
                    "type": "object",
                    "properties": {
                        "test": {"type": "string"},
                        "max_tokens": {"type": "integer"}
                    },
                    "required": ["test"]
                }

            def get_system_prompt(self):
                return "Test prompt"

            def get_request_model(self):
                class TestRequest(ToolRequest):
                    test: str
                return TestRequest

            async def prepare_prompt(self, request):
                return f"Test: {request.test}"

        # Mock response
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock(text="Test response")]

        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance

        # Execute tool with custom max_tokens
        tool = TestTool()
        custom_max_tokens = 16384
        await tool.execute({"test": "value", "max_tokens": custom_max_tokens})

        # Verify model was created with custom max_tokens
        mock_model.assert_called_once()
        call_args = mock_model.call_args

        # Check generation_config
        assert "generation_config" in call_args[1]
        config = call_args[1]["generation_config"]
        assert config["max_output_tokens"] == custom_max_tokens


class TestServerMaxOutputTokens:
    """Test that server.py properly uses MAX_OUTPUT_TOKENS"""

    @pytest.mark.asyncio
    @patch("google.generativeai.GenerativeModel")
    async def test_handle_chat_uses_max_output_tokens(self, mock_model):
        """Test that handle_chat uses MAX_OUTPUT_TOKENS"""
        from server import handle_chat

        # Mock response
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock(text="Chat response")]

        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance

        # Call handle_chat
        await handle_chat({"prompt": "Test question"})

        # Verify model was created with MAX_OUTPUT_TOKENS
        mock_model.assert_called_once()
        call_args = mock_model.call_args

        # Check generation_config
        assert "generation_config" in call_args[1]
        config = call_args[1]["generation_config"]
        assert config["max_output_tokens"] == MAX_OUTPUT_TOKENS
