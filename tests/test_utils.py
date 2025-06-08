"""
Tests for utility functions
"""

from utils import (check_token_limit, estimate_tokens, read_file_content,
                   read_files)


class TestFileUtils:
    """Test file reading utilities"""

    def test_read_file_content_success(self, tmp_path):
        """Test successful file reading"""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            "def hello():\n    return 'world'", encoding="utf-8"
        )

        content = read_file_content(str(test_file))
        assert "--- BEGIN FILE:" in content
        assert "--- END FILE:" in content
        assert "def hello():" in content
        assert "return 'world'" in content

    def test_read_file_content_not_found(self):
        """Test reading non-existent file"""
        content = read_file_content("/nonexistent/file.py")
        assert "--- FILE NOT FOUND:" in content
        assert "Error: File does not exist" in content

    def test_read_file_content_directory(self, tmp_path):
        """Test reading a directory"""
        content = read_file_content(str(tmp_path))
        assert "--- NOT A FILE:" in content
        assert "Error: Path is not a file" in content

    def test_read_files_multiple(self, tmp_path):
        """Test reading multiple files"""
        file1 = tmp_path / "file1.py"
        file1.write_text("print('file1')", encoding="utf-8")
        file2 = tmp_path / "file2.py"
        file2.write_text("print('file2')", encoding="utf-8")

        content, summary = read_files([str(file1), str(file2)])

        assert "--- BEGIN FILE:" in content
        assert "file1.py" in content
        assert "file2.py" in content
        assert "print('file1')" in content
        assert "print('file2')" in content

        assert "Reading 2 file(s)" in summary

    def test_read_files_with_code(self):
        """Test reading with direct code"""
        code = "def test():\n    pass"
        content, summary = read_files([], code)

        assert "--- BEGIN DIRECT CODE ---" in content
        assert "--- END DIRECT CODE ---" in content
        assert code in content

        assert "Direct code:" in summary


class TestTokenUtils:
    """Test token counting utilities"""

    def test_estimate_tokens(self):
        """Test token estimation"""
        # Rough estimate: 1 token ≈ 4 characters
        text = "a" * 400  # 400 characters
        assert estimate_tokens(text) == 100

    def test_check_token_limit_within(self):
        """Test token limit check - within limit"""
        text = "a" * 4000  # 1000 tokens
        within_limit, tokens = check_token_limit(text)
        assert within_limit is True
        assert tokens == 1000

    def test_check_token_limit_exceeded(self):
        """Test token limit check - exceeded"""
        text = "a" * 5_000_000  # 1.25M tokens
        within_limit, tokens = check_token_limit(text)
        assert within_limit is False
        assert tokens == 1_250_000
