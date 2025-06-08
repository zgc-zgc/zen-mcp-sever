"""
Token counting utilities
"""

from typing import Tuple

from config import MAX_CONTEXT_TOKENS


def estimate_tokens(text: str) -> int:
    """Estimate token count (rough: 1 token ≈ 4 characters)"""
    return len(text) // 4


def check_token_limit(text: str) -> Tuple[bool, int]:
    """
    Check if text exceeds token limit.
    Returns: (is_within_limit, estimated_tokens)
    """
    estimated = estimate_tokens(text)
    return estimated <= MAX_CONTEXT_TOKENS, estimated
