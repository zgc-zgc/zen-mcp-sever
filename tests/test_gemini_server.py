"""
Unit tests for Gemini MCP Server
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys
import os

# Add parent directory to path for imports in a cross-platform way
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from gemini_server import (
    GeminiChatRequest,
    CodeAnalysisRequest,
    read_file_content,
    prepare_code_context,
    handle_list_tools,
    handle_call_tool,
    DEVELOPER_SYSTEM_PROMPT,
    DEFAULT_MODEL
)


class TestModels:
    """Test request models"""
    
    def test_gemini_chat_request_defaults(self):
        """Test GeminiChatRequest with default values"""
        request = GeminiChatRequest(prompt="Test prompt")
        assert request.prompt == "Test prompt"
        assert request.system_prompt is None
        assert request.max_tokens == 8192
        assert request.temperature == 0.5
        assert request.model == DEFAULT_MODEL
    
    def test_gemini_chat_request_custom(self):
        """Test GeminiChatRequest with custom values"""
        request = GeminiChatRequest(
            prompt="Test prompt",
            system_prompt="Custom system",
            max_tokens=4096,
            temperature=0.8,
            model="custom-model"
        )
        assert request.system_prompt == "Custom system"
        assert request.max_tokens == 4096
        assert request.temperature == 0.8
        assert request.model == "custom-model"
    
    def test_code_analysis_request_defaults(self):
        """Test CodeAnalysisRequest with default values"""
        request = CodeAnalysisRequest(question="Analyze this")
        assert request.question == "Analyze this"
        assert request.files is None
        assert request.code is None
        assert request.max_tokens == 8192
        assert request.temperature == 0.2
        assert request.model == DEFAULT_MODEL


class TestFileOperations:
    """Test file reading and context preparation"""
    
    def test_read_file_content_success(self, tmp_path):
        """Test successful file reading"""
        test_file = tmp_path / "test.py"
        test_file.write_text("def hello():\n    return 'world'", encoding='utf-8')
        
        content = read_file_content(str(test_file))
        assert "=== File:" in content
        assert "def hello():" in content
        assert "return 'world'" in content
    
    def test_read_file_content_not_found(self):
        """Test reading non-existent file"""
        # Use a path that's guaranteed not to exist on any platform
        nonexistent_path = os.path.join(
            os.path.sep, "nonexistent_dir_12345", "nonexistent_file.py"
        )
        content = read_file_content(nonexistent_path)
        assert "Error: File not found" in content
    
    def test_read_file_content_directory(self, tmp_path):
        """Test reading a directory instead of file"""
        content = read_file_content(str(tmp_path))
        assert "Error: Not a file" in content
    
    def test_prepare_code_context_with_files(self, tmp_path):
        """Test preparing context from files"""
        file1 = tmp_path / "file1.py"
        file1.write_text("print('file1')", encoding='utf-8')
        file2 = tmp_path / "file2.py"
        file2.write_text("print('file2')", encoding='utf-8')
        
        context = prepare_code_context([str(file1), str(file2)], None)
        assert "file1.py" in context
        assert "file2.py" in context
        assert "print('file1')" in context
        assert "print('file2')" in context
    
    def test_prepare_code_context_with_code(self):
        """Test preparing context from direct code"""
        code = "def test():\n    pass"
        context = prepare_code_context(None, code)
        assert "=== Direct Code ===" in context
        assert code in context
    
    def test_prepare_code_context_mixed(self, tmp_path):
        """Test preparing context from both files and code"""
        test_file = tmp_path / "test.py"
        test_file.write_text("# From file", encoding='utf-8')
        code = "# Direct code"
        
        context = prepare_code_context([str(test_file)], code)
        assert "# From file" in context
        assert "# Direct code" in context


class TestToolHandlers:
    """Test MCP tool handlers"""
    
    @pytest.mark.asyncio
    async def test_handle_list_tools(self):
        """Test listing available tools"""
        tools = await handle_list_tools()
        assert len(tools) == 3
        
        tool_names = [tool.name for tool in tools]
        assert "chat" in tool_names
        assert "analyze_code" in tool_names
        assert "list_models" in tool_names
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_unknown(self):
        """Test calling unknown tool"""
        result = await handle_call_tool("unknown_tool", {})
        assert len(result) == 1
        assert "Unknown tool" in result[0].text
    
    @pytest.mark.asyncio
    @patch('google.generativeai.GenerativeModel')
    async def test_handle_call_tool_chat_success(self, mock_model):
        """Test successful chat tool call"""
        # Mock the response
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock(text="Test response")]
        
        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        
        result = await handle_call_tool("chat", {
            "prompt": "Test prompt",
            "temperature": 0.5
        })
        
        assert len(result) == 1
        assert result[0].text == "Test response"
        
        # Verify model was called with correct parameters
        mock_model.assert_called_once()
        call_args = mock_model.call_args[1]
        assert call_args['model_name'] == DEFAULT_MODEL
        assert call_args['generation_config']['temperature'] == 0.5
    
    @pytest.mark.asyncio
    @patch('google.generativeai.GenerativeModel')
    async def test_handle_call_tool_chat_with_developer_prompt(self, mock_model):
        """Test chat tool uses developer prompt when no system prompt provided"""
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock(text="Response")]
        
        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        
        await handle_call_tool("chat", {"prompt": "Test"})
        
        # Check that developer prompt was included
        call_args = mock_instance.generate_content.call_args[0][0]
        assert DEVELOPER_SYSTEM_PROMPT in call_args
    
    @pytest.mark.asyncio
    async def test_handle_call_tool_analyze_code_no_input(self):
        """Test analyze_code with no files or code"""
        result = await handle_call_tool("analyze_code", {
            "question": "Analyze what?"
        })
        assert len(result) == 1
        assert "Must provide either 'files' or 'code'" in result[0].text
    
    @pytest.mark.asyncio
    @patch('google.generativeai.GenerativeModel')
    async def test_handle_call_tool_analyze_code_success(self, mock_model, tmp_path):
        """Test successful code analysis"""
        # Create test file
        test_file = tmp_path / "test.py"
        test_file.write_text("def hello(): pass", encoding='utf-8')
        
        # Mock response
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock(text="Analysis result")]
        
        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        
        result = await handle_call_tool("analyze_code", {
            "files": [str(test_file)],
            "question": "Analyze this"
        })
        
        assert len(result) == 1
        assert result[0].text == "Analysis result"
    
    @pytest.mark.asyncio
    @patch('google.generativeai.list_models')
    async def test_handle_call_tool_list_models(self, mock_list_models):
        """Test listing models"""
        # Mock model data
        mock_model = Mock()
        mock_model.name = "test-model"
        mock_model.display_name = "Test Model"
        mock_model.description = "A test model"
        mock_model.supported_generation_methods = ['generateContent']
        
        mock_list_models.return_value = [mock_model]
        
        result = await handle_call_tool("list_models", {})
        assert len(result) == 1
        
        models = json.loads(result[0].text)
        assert len(models) == 1
        assert models[0]['name'] == "test-model"
        assert models[0]['is_default'] == False


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    @patch('google.generativeai.GenerativeModel')
    async def test_handle_call_tool_chat_api_error(self, mock_model):
        """Test handling API errors in chat"""
        mock_instance = Mock()
        mock_instance.generate_content.side_effect = Exception("API Error")
        mock_model.return_value = mock_instance
        
        result = await handle_call_tool("chat", {"prompt": "Test"})
        assert len(result) == 1
        assert "Error calling Gemini API" in result[0].text
        assert "API Error" in result[0].text
    
    @pytest.mark.asyncio
    @patch('google.generativeai.GenerativeModel')
    async def test_handle_call_tool_chat_blocked_response(self, mock_model):
        """Test handling blocked responses"""
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = []
        mock_response.candidates[0].finish_reason = 2
        
        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        
        result = await handle_call_tool("chat", {"prompt": "Test"})
        assert len(result) == 1
        assert "Response blocked or incomplete" in result[0].text
        assert "Finish reason: 2" in result[0].text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])