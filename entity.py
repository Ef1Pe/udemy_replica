"""Entity definition for the Udemy replica."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from metadata import UdemyReplicaMetadata
from server import start_server

try:  # pragma: no cover
    from agenticverse_entities.base.entity_base import EntityBase
except ImportError:  # pragma: no cover
    class EntityBase:  # type: ignore
        name: str
        description: str

        def start(self, *args: Any, **kwargs: Any):  # noqa: D401
            raise NotImplementedError


@dataclass
class UdemyReplicaEntity(EntityBase):
    """Minimal entity wrapper compatible with Agenticverse tooling."""

    name: str = "udemy_replica"
    description: str = "Pixel-perfect replica of udemy.com with injectable content."
    metadata: UdemyReplicaMetadata = UdemyReplicaMetadata()

    def start(self, port: int = 5000, threaded: bool = False, content_data: Dict[str, Any] | None = None):
        return start_server(port=port, threaded=threaded, content_data=content_data)
