"""
Tests for configuration
"""

from config import (DEFAULT_MODEL, MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS,
                    TEMPERATURE_ANALYTICAL, TEMPERATURE_BALANCED,
                    TEMPERATURE_CREATIVE, TOOL_TRIGGERS, __author__,
                    __updated__, __version__)


class TestConfig:
    """Test configuration values"""

    def test_version_info(self):
        """Test version information exists and has correct format"""
        # Check version format (e.g., "2.4.1")
        assert isinstance(__version__, str)
        assert len(__version__.split('.')) == 3  # Major.Minor.Patch
        
        # Check author
        assert __author__ == "Fahad Gilani"
        
        # Check updated date exists and has valid format (YYYY-MM-DD)
        assert isinstance(__updated__, str)
        assert len(__updated__) == 10
        assert __updated__[4] == '-' and __updated__[7] == '-'
        # Validate it's a valid date format
        year, month, day = __updated__.split('-')
        assert len(year) == 4 and year.isdigit()
        assert len(month) == 2 and month.isdigit() and 1 <= int(month) <= 12
        assert len(day) == 2 and day.isdigit() and 1 <= int(day) <= 31

    def test_model_config(self):
        """Test model configuration"""
        assert DEFAULT_MODEL == "gemini-2.5-pro-preview-06-05"
        assert MAX_CONTEXT_TOKENS == 1_000_000
        assert MAX_OUTPUT_TOKENS == 32_768

    def test_temperature_defaults(self):
        """Test temperature constants"""
        assert TEMPERATURE_ANALYTICAL == 0.2
        assert TEMPERATURE_BALANCED == 0.5
        assert TEMPERATURE_CREATIVE == 0.7

    def test_tool_triggers(self):
        """Test tool trigger phrases"""
        assert "think_deeper" in TOOL_TRIGGERS
        assert "review_code" in TOOL_TRIGGERS
        assert "debug_issue" in TOOL_TRIGGERS
        assert "analyze" in TOOL_TRIGGERS

        # Check some specific triggers
        assert "ultrathink" in TOOL_TRIGGERS["think_deeper"]
        assert "extended thinking" in TOOL_TRIGGERS["think_deeper"]
        assert "find bugs" in TOOL_TRIGGERS["review_code"]
        assert "root cause" in TOOL_TRIGGERS["debug_issue"]
