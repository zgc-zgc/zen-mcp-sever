"""
In-memory storage backend for conversation threads

This module provides a thread-safe, in-memory alternative to Redis for storing
conversation contexts. It's designed for ephemeral MCP server sessions where
conversations only need to persist during a single Claude session.

⚠️  PROCESS-SPECIFIC STORAGE: This storage is confined to a single Python process.
    Data stored in one process is NOT accessible from other processes or subprocesses.
    This is why simulator tests that run server.py as separate subprocesses cannot
    share conversation state between tool calls.

Key Features:
- Thread-safe operations using locks
- TTL support with automatic expiration
- Background cleanup thread for memory management
- Singleton pattern for consistent state within a single process
- Drop-in replacement for Redis storage (for single-process scenarios)
"""

import logging
import os
import threading
import time
from typing import Optional, Dict, Any
import json
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class FileBasedStorage:
    """Thread-safe storage for conversation threads with file-based persistence."""

    def __init__(self):
        self._store: dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()
        self.storage_dir = Path(".zenMcpSession")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"File-based storage initialized at {self.storage_dir.resolve()}")

    def _format_to_markdown(self, data: str) -> str:
        try:
            context = json.loads(data)
            md = f"---\n"
            # Simple metadata with only essential info
            simplified_metadata = {
                'thread_id': context.get('thread_id'),
                'created_at': context.get('created_at'),
                'tool_name': context.get('tool_name')
            }
            md += f"metadata: {json.dumps(simplified_metadata)}\n"
            md += f"---\n\n"
            md += f"# Conversation: {context.get('thread_id', '')}\n\n"

            # Record all turns - no need for complex deduplication
            for i, turn in enumerate(context.get('turns', [])):
                md += f"## Turn {i+1}: {turn.get('role', 'unknown')}\n"
                md += f"**Tool:** {turn.get('tool_name', 'N/A')}\n"
                if turn.get('model_name'):
                    md += f"**Model:** {turn.get('model_name')}\n"
                md += f"\n```\n{turn.get('content', '')}\n```\n\n"
            return md
        except Exception as e:
            logger.error(f"Error formatting to markdown: {e}")
            return data

    def _parse_from_markdown(self, markdown_content: str) -> Optional[str]:
        try:
            # Extract JSON from YAML-like front matter
            match = re.search(r"^---\s*\nmetadata:\s*(.*?)\n---\s*\n", markdown_content, re.DOTALL)
            if match:
                json_str = match.group(1)
                # Basic validation to see if it looks like a JSON object
                if json_str.strip().startswith('{') and json_str.strip().endswith('}'):
                    # Parse the simplified metadata and reconstruct full context if needed
                    simplified_metadata = json.loads(json_str)
                    
                    # Build minimal context structure for compatibility
                    full_context = {
                        'thread_id': simplified_metadata.get('thread_id', ''),
                        'created_at': simplified_metadata.get('created_at', ''),
                        'last_updated_at': simplified_metadata.get('created_at', ''),
                        'tool_name': simplified_metadata.get('tool_name', ''),
                        'turns': [],  # Empty turns for file-based storage
                        'initial_context': {}
                    }
                    
                    return json.dumps(full_context)
            logger.warning("Could not parse metadata from markdown file.")
        except Exception as e:
            logger.error(f"Error parsing markdown file: {e}")
        return None

    def _write_to_file(self, key: str, value: str):
        thread_id = key.split(":")[-1]
        file_path = self.storage_dir / f"{thread_id}.md"
        try:
            markdown_content = self._format_to_markdown(value)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            logger.debug(f"Saved conversation {thread_id} to {file_path}")
        except Exception as e:
            logger.error(f"Failed to write conversation to file {file_path}: {e}")

    def _read_from_file(self, key: str) -> Optional[str]:
        thread_id = key.split(":")[-1]
        file_path = self.storage_dir / f"{thread_id}.md"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return self._parse_from_markdown(content)
            except Exception as e:
                logger.error(f"Failed to read conversation from file {file_path}: {e}")
        return None

    def setex(self, key: str, ttl_seconds: int, value: str) -> None:
        """Store value in file and memory with expiration."""
        with self._lock:
            expires_at = time.time() + ttl_seconds
            self._store[key] = (value, expires_at)
            self._write_to_file(key, value)
            logger.debug(f"Stored key {key} in-memory and on-disk.")

    def get(self, key: str) -> Optional[str]:
        """Retrieve value from memory first, then from file."""
        with self._lock:
            # Check memory first
            if key in self._store:
                value, expires_at = self._store[key]
                if time.time() < expires_at:
                    logger.debug(f"Retrieved key {key} from memory cache.")
                    return value
                else:
                    # Expired from memory, but might still be on disk
                    del self._store[key]
                    logger.debug(f"Key {key} expired from memory cache.")

            # If not in memory, try loading from file
            logger.debug(f"Key {key} not in memory, trying to load from file.")
            file_content_json = self._read_from_file(key)
            if file_content_json:
                logger.info(f"Loaded conversation for key {key} from file.")
                # Load into memory with a fresh TTL
                timeout_hours = int(os.getenv("CONVERSATION_TIMEOUT_HOURS", "3"))
                ttl = timeout_hours * 3600
                self.setex(key, ttl, file_content_json)
                return file_content_json

        return None

    def get_default_conversation_id(self) -> Optional[str]:
        """Get the most recent conversation thread ID to use as default."""
        try:
            # Get all conversation files
            conversation_files = list(self.storage_dir.glob("*.md"))
            if not conversation_files:
                return None
            
            # Sort by modification time, get the most recent
            most_recent = max(conversation_files, key=lambda f: f.stat().st_mtime)
            thread_id = most_recent.stem  # filename without extension
            
            # Verify this conversation still exists and is valid
            key = f"thread:{thread_id}"
            if self.get(key):
                logger.debug(f"Found default conversation ID: {thread_id}")
                return thread_id
            
            return None
        except Exception as e:
            logger.debug(f"Error getting default conversation ID: {e}")
            return None

# Global singleton instance
_storage_instance = None
_storage_lock = threading.Lock()


def get_storage_backend() -> "FileBasedStorage":
    """Get the global storage instance (singleton pattern)"""
    global _storage_instance
    if _storage_instance is None:
        with _storage_lock:
            if _storage_instance is None:
                _storage_instance = FileBasedStorage()
                logger.info("Initialized file-based conversation storage")
    return _storage_instance
