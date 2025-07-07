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
from typing import Optional
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class FileBasedStorage:
    """Thread-safe storage for conversation threads with file-based persistence."""

    def __init__(self):
        self._store: dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()
        self.storage_dir = Path("zenMcp")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        timeout_hours = int(os.getenv("CONVERSATION_TIMEOUT_HOURS", "3"))
        self._cleanup_interval = (timeout_hours * 3600) // 10
        self._cleanup_interval = max(300, self._cleanup_interval)
        self._shutdown = False

        self._cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
        self._cleanup_thread.start()

        logger.info(
            f"File-based storage initialized at {self.storage_dir.resolve()} with {timeout_hours}h timeout, cleanup every {self._cleanup_interval//60}m"
        )

    def _format_to_markdown(self, data: str) -> str:
        try:
            context = json.loads(data)
            md = f"---\n"
            md += f"thread_id: {context.get('thread_id', '')}\n"
            md += f"parent_thread_id: {context.get('parent_thread_id', '')}\n"
            md += f"created_at: {context.get('created_at', '')}\n"
            md += f"last_updated_at: {context.get('last_updated_at', '')}\n"
            md += f"tool_name: {context.get('tool_name', '')}\n"
            md += f"initial_context: {json.dumps(context.get('initial_context', {}))}\n"
            md += f"---\n\n"
            md += f"# Conversation: {context.get('thread_id', '')}\n\n"

            for i, turn in enumerate(context.get('turns', [])):
                md += f"## Turn {i+1}: {turn.get('role', 'unknown')}\n"
                md += f"**Tool:** {turn.get('tool_name', 'N/A')}\n"
                if turn.get('model_name'):
                    md += f"**Model:** {turn.get('model_name')}\n"
                if turn.get('files'):
                    md += f"**Files:** {', '.join(turn.get('files'))}\n"
                md += f"\n> {turn.get('content', '')}\n\n"
            return md
        except Exception as e:
            logger.error(f"Error formatting to markdown: {e}")
            return data

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
                # This is a simplification. A real implementation would need to
                # parse the markdown back into the JSON structure.
                # For now, we'll just indicate it's not implemented.
                logger.warning("Reading from markdown not fully implemented. Just loading existence.")
                # This is where you would implement the parsing logic.
                return None
            except Exception as e:
                logger.error(f"Failed to read conversation from file {file_path}: {e}")
        return None

    def set_with_ttl(self, key: str, ttl_seconds: int, value: str) -> None:
        """Store value with expiration time and write to file."""
        with self._lock:
            expires_at = time.time() + ttl_seconds
            self._store[key] = (value, expires_at)
            logger.debug(f"Stored key {key} in memory with TTL {ttl_seconds}s")
            self._write_to_file(key, value)

    def get(self, key: str) -> Optional[str]:
        """Retrieve value if not expired from memory or file."""
        with self._lock:
            if key in self._store:
                value, expires_at = self._store[key]
                if time.time() < expires_at:
                    logger.debug(f"Retrieved key {key} from memory")
                    return value
                else:
                    del self._store[key]
                    logger.debug(f"Key {key} expired and removed from memory")

            logger.debug(f"Key {key} not in memory, trying to load from file.")
            file_content = self._read_from_file(key)
            if file_content:
                logger.info(f"Loaded conversation for key {key} from file.")
                self.set_with_ttl(key, int(os.getenv("CONVERSATION_TIMEOUT_HOURS", "3")) * 3600, file_content)
                return file_content

        return None

    def setex(self, key: str, ttl_seconds: int, value: str) -> None:
        """Redis-compatible setex method"""
        self.set_with_ttl(key, ttl_seconds, value)

    def _cleanup_worker(self):
        """Background thread that periodically cleans up expired entries"""
        while not self._shutdown:
            time.sleep(self._cleanup_interval)
            self._cleanup_expired()

    def _cleanup_expired(self):
        """Remove all expired entries"""
        with self._lock:
            current_time = time.time()
            expired_keys = [k for k, (_, exp) in self._store.items() if exp < current_time]
            for key in expired_keys:
                del self._store[key]

            if expired_keys:
                logger.debug(f"Cleaned up {len(expired_keys)} expired conversation threads from memory")

    def shutdown(self):
        """Graceful shutdown of background thread"""
        self._shutdown = True
        if self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=1)


# Global singleton instance
_storage_instance = None
_storage_lock = threading.Lock()


def get_storage_backend() -> FileBasedStorage:
    """Get the global storage instance (singleton pattern)"""
    global _storage_instance
    if _storage_instance is None:
        with _storage_lock:
            if _storage_instance is None:
                _storage_instance = FileBasedStorage()
                logger.info("Initialized file-based conversation storage")
    return _storage_instance
