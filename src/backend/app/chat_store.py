"""
Utility module for persisting chat interactions to a JSONL log.
"""
from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def _default_log_path() -> Path:
    env_path = os.getenv("MARC_CHAT_LOG_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    base_dir = Path(__file__).resolve().parent
    return base_dir / "data" / "chat_history.jsonl"


@dataclass(frozen=True)
class ChatRecord:
    """
    Structured representation of a single user-assistant exchange.
    """

    timestamp: str
    request_id: str
    persona: str
    user_message: Dict[str, Any]
    assistant_message: Dict[str, Any]
    conversation: List[Dict[str, Any]]
    metadata: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(
            {
                "timestamp": self.timestamp,
                "request_id": self.request_id,
                "persona": self.persona,
                "user_message": self.user_message,
                "assistant_message": self.assistant_message,
                "conversation": self.conversation,
                "metadata": self.metadata,
            },
            ensure_ascii=False,
        )


class ChatLogger:
    """
    Append-only logger that writes chat exchanges to disk.
    """

    def __init__(self, log_path: Optional[Path] = None) -> None:
        self._path = (log_path or _default_log_path()).resolve()
        self._lock = asyncio.Lock()

    @property
    def path(self) -> Path:
        return self._path

    async def log(
        self,
        *,
        request_id: str,
        persona: Optional[str],
        user_message: Dict[str, Any],
        assistant_message: Dict[str, Any],
        conversation: Iterable[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        record = ChatRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            request_id=request_id,
            persona=(persona or "unknown").strip() or "unknown",
            user_message=user_message,
            assistant_message=assistant_message,
            conversation=list(conversation),
            metadata=metadata or {},
        )
        await self._append(record.to_json())

    async def _append(self, line: str) -> None:
        async with self._lock:
            await asyncio.to_thread(self._write_line, line)

    def _write_line(self, line: str) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.write("\n")


_logger: Optional[ChatLogger] = None


def get_logger() -> ChatLogger:
    global _logger
    if _logger is None:
        _logger = ChatLogger()
    return _logger
