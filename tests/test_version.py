"""
Test version functionality
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from gemini_server import (
    __version__,
    __updated__,
    __author__,
    handle_list_tools,
    handle_call_tool,
)


class TestVersionFunctionality:
    """Test version-related functionality"""

    @pytest.mark.asyncio
    async def test_version_constants_exist(self):
        """Test that version constants are defined"""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert __updated__ is not None
        assert isinstance(__updated__, str)
        assert __author__ is not None
        assert isinstance(__author__, str)

    @pytest.mark.asyncio
    async def test_version_tool_in_list(self):
        """Test that get_version tool appears in tool list"""
        tools = await handle_list_tools()
        tool_names = [tool.name for tool in tools]
        assert "get_version" in tool_names

        # Find the version tool
        version_tool = next(t for t in tools if t.name == "get_version")
        assert (
            version_tool.description
            == "Get the version and metadata of the Gemini MCP Server"
        )

    @pytest.mark.asyncio
    async def test_get_version_tool_execution(self):
        """Test executing the get_version tool"""
        result = await handle_call_tool("get_version", {})

        assert len(result) == 1
        assert result[0].type == "text"

        # Check the response contains expected information
        response_text = result[0].text
        assert __version__ in response_text
        assert __updated__ in response_text
        assert __author__ in response_text
        assert "Gemini MCP Server" in response_text
        assert "Default Model:" in response_text
        assert "Max Context:" in response_text
        assert "Python:" in response_text
        assert "Started:" in response_text
        assert "github.com/BeehiveInnovations/gemini-mcp-server" in response_text

    @pytest.mark.asyncio
    async def test_version_format(self):
        """Test that version follows semantic versioning"""
        parts = __version__.split(".")
        assert len(parts) == 3  # Major.Minor.Patch
        for part in parts:
            assert part.isdigit()  # Each part should be numeric

    @pytest.mark.asyncio
    async def test_date_format(self):
        """Test that updated date follows expected format"""
        # Expected format: YYYY-MM-DD
        parts = __updated__.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4  # Year
        assert len(parts[1]) == 2  # Month
        assert len(parts[2]) == 2  # Day
        for part in parts:
            assert part.isdigit()
