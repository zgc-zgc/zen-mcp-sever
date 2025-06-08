"""
Test verbose output functionality
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from gemini_server import prepare_code_context


class TestNewFormattingBehavior:
    """Test the improved formatting behavior"""

    def test_file_formatting_for_gemini(self, tmp_path):
        """Test that files are properly formatted for Gemini"""
        test_file = tmp_path / "test.py"
        content = "def hello():\n    return 'world'"
        test_file.write_text(content, encoding="utf-8")

        context, summary = prepare_code_context([str(test_file)], None)

        # Context should have clear markers for Gemini
        assert "--- BEGIN FILE:" in context
        assert "--- END FILE:" in context
        assert str(test_file) in context
        assert content in context

        # Summary should be concise for terminal
        assert "Analyzing 1 file(s)" in summary
        assert "bytes)" in summary
        assert len(summary) < len(context)  # Summary much smaller than full context

    def test_terminal_summary_shows_preview(self, tmp_path):
        """Test that terminal summary shows small preview"""
        test_file = tmp_path / "large_file.py"
        content = "# This is a large file\n" + "x = 1\n" * 1000
        test_file.write_text(content, encoding="utf-8")

        context, summary = prepare_code_context([str(test_file)], None)

        # Summary should show preview but not full content
        assert "Analyzing 1 file(s)" in summary
        assert str(test_file) in summary
        assert "bytes)" in summary
        assert "Preview:" in summary
        # Full content should not be in summary
        assert "x = 1" not in summary or summary.count("x = 1") < 5

    def test_multiple_files_summary(self, tmp_path):
        """Test summary with multiple files"""
        files = []
        for i in range(3):
            file = tmp_path / f"file{i}.py"
            file.write_text(f"# File {i}\nprint({i})", encoding="utf-8")
            files.append(str(file))

        context, summary = prepare_code_context(files, None)

        assert "Analyzing 3 file(s)" in summary
        for file in files:
            assert file in summary
        assert "bytes)" in summary
        # Should have clear delimiters in context
        assert context.count("--- BEGIN FILE:") == 3
        assert context.count("--- END FILE:") == 3

    def test_direct_code_formatting(self):
        """Test direct code formatting"""
        direct_code = "# Direct code\nprint('hello')"

        context, summary = prepare_code_context(None, direct_code)

        # Context should have clear markers
        assert "--- BEGIN DIRECT CODE ---" in context
        assert "--- END DIRECT CODE ---" in context
        assert direct_code in context

        # Summary should show preview
        assert "Direct code provided" in summary
        assert f"({len(direct_code)} characters)" in summary
        assert "Preview:" in summary

    def test_mixed_content_formatting(self, tmp_path):
        """Test formatting with both files and direct code"""
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test file", encoding="utf-8")
        direct_code = "# Direct code\nprint('hello')"

        context, summary = prepare_code_context([str(test_file)], direct_code)

        # Context should have both with clear separation
        assert "--- BEGIN FILE:" in context
        assert "--- END FILE:" in context
        assert "--- BEGIN DIRECT CODE ---" in context
        assert "--- END DIRECT CODE ---" in context

        # Summary should mention both
        assert "Analyzing 1 file(s)" in summary
        assert "Direct code provided" in summary
