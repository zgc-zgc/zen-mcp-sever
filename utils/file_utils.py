"""
File reading utilities
"""

from pathlib import Path
from typing import List, Tuple, Optional


def read_file_content(file_path: str) -> str:
    """Read a single file and format it for Gemini"""
    path = Path(file_path)

    try:
        # Check if path exists and is a file
        if not path.exists():
            return f"\n--- FILE NOT FOUND: {file_path} ---\nError: File does not exist\n--- END FILE ---\n"

        if not path.is_file():
            return f"\n--- NOT A FILE: {file_path} ---\nError: Path is not a file\n--- END FILE ---\n"

        # Read the file
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Format with clear delimiters for Gemini
        return f"\n--- BEGIN FILE: {file_path} ---\n{content}\n--- END FILE: {file_path} ---\n"

    except Exception as e:
        return f"\n--- ERROR READING FILE: {file_path} ---\nError: {str(e)}\n--- END FILE ---\n"


def read_files(
    file_paths: List[str], code: Optional[str] = None
) -> Tuple[str, str]:
    """
    Read multiple files and optional direct code.
    Returns: (full_content, brief_summary)
    """
    content_parts = []
    summary_parts = []

    # Process files
    if file_paths:
        summary_parts.append(f"Reading {len(file_paths)} file(s)")
        for file_path in file_paths:
            content = read_file_content(file_path)
            content_parts.append(content)

    # Add direct code if provided
    if code:
        formatted_code = (
            f"\n--- BEGIN DIRECT CODE ---\n{code}\n--- END DIRECT CODE ---\n"
        )
        content_parts.append(formatted_code)
        code_preview = code[:50] + "..." if len(code) > 50 else code
        summary_parts.append(f"Direct code: {code_preview}")

    full_content = "\n\n".join(content_parts)
    summary = (
        " | ".join(summary_parts) if summary_parts else "No input provided"
    )

    return full_content, summary
