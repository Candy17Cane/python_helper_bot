from __future__ import annotations
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def add_favorite(self, user_id: int, section_key: str, topic_key: str) -> None: ...

    @abstractmethod
    def remove_favorite(self, iser_id: int, section_key: str, topic_key: str) -> None: ...

    @abstractmethod
    def is_favorite(self, user_id: int, section_key: str, topic_key: str) -> bool: ...

    @abstractmethod
    def list_favorites(self, user_id: int) -> list[tuple[str, str]]: ...

