"""Metadata schema for the Udemy replica entity."""
from dataclasses import dataclass
from typing import Dict, Any

try:  # pragma: no cover - optional dependency for Agenticverse environments
    from agenticverse_entities.base.metadata_base import BaseMetadata, Metadata
except ImportError:  # pragma: no cover
    @dataclass
    class Metadata:  # type: ignore
        domain: str
        parameters: Dict[str, Any]

    class BaseMetadata:  # type: ignore
        def get_metadata(self) -> "Metadata":  # noqa: D401
            raise NotImplementedError


class UdemyReplicaMetadata(BaseMetadata):
    """Describes injectable parameters for the Udemy experience."""

    def get_metadata(self) -> "Metadata":
        return Metadata(
            domain="*.udemy.com",
            parameters={
                "port": "integer",
                "section": "string",  # page section identifier
                "title": "string",
                "description": "string",
                "category": "string",
                "image_url": "string",
                "price": "string",
                "old_price": "string",
                "rating": "string",
                "reviews": "string",
                "instructor": "string",
                "badge_text": "string",
                "featured": "boolean",
            },
        )
