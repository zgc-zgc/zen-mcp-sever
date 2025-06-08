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


class TestVerboseOutput:
    """Test verbose output functionality"""
    
    def test_verbose_true_shows_full_content(self, tmp_path):
        """Test that verbose=True shows full file content"""
        test_file = tmp_path / "test.py"
        content = "def hello():\n    return 'world'"
        test_file.write_text(content, encoding='utf-8')
        
        context, summary = prepare_code_context([str(test_file)], None, verbose=True)
        
        # With verbose=True, summary should equal context
        assert summary == context
        assert content in summary
        
    def test_verbose_false_shows_summary(self, tmp_path):
        """Test that verbose=False shows only summary"""
        test_file = tmp_path / "large_file.py"
        content = "x = 1\n" * 1000  # Large content
        test_file.write_text(content, encoding='utf-8')
        
        context, summary = prepare_code_context([str(test_file)], None, verbose=False)
        
        # Summary should be much smaller than context
        assert len(summary) < len(context)
        assert "Analyzing 1 file(s)" in summary
        assert str(test_file) in summary
        assert "bytes)" in summary
        # Content should not be in summary
        assert content not in summary
        
    def test_multiple_files_summary(self, tmp_path):
        """Test summary with multiple files"""
        files = []
        for i in range(3):
            file = tmp_path / f"file{i}.py"
            file.write_text(f"# File {i}\nprint({i})", encoding='utf-8')
            files.append(str(file))
        
        context, summary = prepare_code_context(files, None, verbose=False)
        
        assert "Analyzing 3 file(s)" in summary
        for file in files:
            assert file in summary
        assert "bytes)" in summary
        
    def test_code_and_files_summary(self, tmp_path):
        """Test summary with both files and direct code"""
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test file", encoding='utf-8')
        direct_code = "# Direct code\nprint('hello')"
        
        context, summary = prepare_code_context([str(test_file)], direct_code, verbose=False)
        
        assert "Analyzing 1 file(s)" in summary
        assert str(test_file) in summary
        assert "Direct code provided" in summary
        assert f"({len(direct_code):,} characters)" in summary