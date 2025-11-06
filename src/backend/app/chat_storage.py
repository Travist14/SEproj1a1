"""Utilities for persisting chat transcripts to disk."""

from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

CHAT_STORAGE_DIR_ENV = "CHAT_STORAGE_DIR"
DEFAULT_CHAT_STORAGE_SUBDIR = "chats"


def _normalise_persona(persona: Optional[str]) -> str:
    """Create a filesystem-friendly slug for the persona (stakeholder)."""
    if not persona:
        return "general"
    slug = re.sub(r"[^a-z0-9]+", "-", persona.strip().lower())
    slug = slug.strip("-")
    return slug or "general"


@dataclass
class ChatTranscript:
    """Represents a single interaction captured by the backend."""

    request_id: str
    messages: Any
    response_text: str
    finish_reason: Optional[str]
    persona: Optional[str]
    parameters: Dict[str, Any]
    created_at: datetime
    source_path: Optional[Path] = None

    def as_dict(self) -> Dict[str, Any]:
        """Serialise the transcript into JSON-compatible data."""
        return {
            "request_id": self.request_id,
            "created_at": self.created_at.isoformat(),
            "persona": self.persona,
            "stakeholder": self.persona,  # Retained for orchestrator terminology.
            "messages": self.messages,
            "response": {
                "content": self.response_text,
                "finish_reason": self.finish_reason,
            },
            "generation_parameters": self.parameters,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, Any], *, source_path: Optional[Path] = None) -> "ChatTranscript":
        """Rehydrate a transcript from persisted JSON."""
        created_at_raw = payload.get("created_at")
        created_at = datetime.fromisoformat(created_at_raw) if isinstance(created_at_raw, str) else datetime.utcnow()
        return cls(
            request_id=payload.get("request_id", ""),
            messages=payload.get("messages", []),
            response_text=payload.get("response", {}).get("content", ""),
            finish_reason=payload.get("response", {}).get("finish_reason"),
            persona=payload.get("persona"),
            parameters=payload.get("generation_parameters", {}),
            created_at=created_at,
            source_path=source_path,
        )


class ChatStorage:
    """Persist chat transcripts as JSON files for later orchestration."""

    def __init__(self, root_directory: Optional[Path] = None) -> None:
        configured = os.getenv(CHAT_STORAGE_DIR_ENV)
        base_path = Path(configured) if configured else None

        if root_directory is not None:
            base_path = Path(root_directory)

        if base_path is None:
            package_root = Path(__file__).resolve().parent
            base_path = package_root / DEFAULT_CHAT_STORAGE_SUBDIR

        self._base_path = base_path

    @property
    def base_path(self) -> Path:
        return self._base_path

    def _build_file_path(self, transcript: ChatTranscript) -> Path:
        persona_slug = _normalise_persona(transcript.persona)
        timestamp = transcript.created_at.strftime("%Y%m%dT%H%M%SZ")
        filename = f"{timestamp}_{transcript.request_id}.json"
        return self._base_path / persona_slug / filename

    def _write_transcript(self, path: Path, transcript: ChatTranscript) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = transcript.as_dict()
        path.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")
        return path

    def _discover_transcript_files(self) -> List[Path]:
        if not self._base_path.exists():
            return []
        return sorted(self._base_path.rglob("*.json"))

    def _load_transcripts_sync(
        self,
        personas: Optional[Iterable[str]],
        limit_per_persona: Optional[int],
    ) -> Dict[str, List[ChatTranscript]]:
        persona_filter = {p.strip().lower() for p in personas} if personas else None
        transcripts_by_persona: Dict[str, List[ChatTranscript]] = {}

        for transcript_path in self._discover_transcript_files():
            try:
                payload = json.loads(transcript_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue

            persona = payload.get("persona") or "general"
            if persona_filter and persona.strip().lower() not in persona_filter:
                continue

            transcript = ChatTranscript.from_dict(payload, source_path=transcript_path)
            transcripts = transcripts_by_persona.setdefault(persona, [])
            transcripts.append(transcript)

        if limit_per_persona:
            for persona, transcripts in transcripts_by_persona.items():
                transcripts.sort(key=lambda item: item.created_at, reverse=True)
                limited = transcripts[:limit_per_persona]
                limited.sort(key=lambda item: item.created_at)
                transcripts_by_persona[persona] = limited
        else:
            for transcripts in transcripts_by_persona.values():
                transcripts.sort(key=lambda item: item.created_at)

        return transcripts_by_persona

    async def save_transcript(self, transcript: ChatTranscript) -> Path:
        """Persist the transcript asynchronously to avoid blocking the event loop."""
        path = self._build_file_path(transcript)
        return await asyncio.to_thread(self._write_transcript, path, transcript)

    async def load_transcripts(
        self,
        personas: Optional[Iterable[str]] = None,
        limit_per_persona: Optional[int] = None,
    ) -> Dict[str, List[ChatTranscript]]:
        """Load transcripts grouped by persona."""
        return await asyncio.to_thread(self._load_transcripts_sync, personas, limit_per_persona)
