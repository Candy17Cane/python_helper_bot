from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set, Tuple, Iterable
from data.content import CONTENT
from utils.text import tokens, norm

TopicId = Tuple[str, str] # (section_key, topic_key)

@dataclass(frozen=True)
class TopicMeta:
    section_key: str
    topic_key: str
    section_title: str
    topic_title: str
    blob: str

def build_index() -> tuple[Dict[str, Set[TopicId]], Dict[TopicId, TopicMeta]]:
    inverted: Dict[str, Set[TopicId]] = {}
    meta: Dict[TopicId, TopicMeta] = {}

    for section_key, section in CONTENT.items():
        section_title = section.get("title", section_key)
        for topic_key, topic in section.get("topics", {}).items():
            title = topic.get("title", topic_key)

            blob = norm("\n".join([
                topic.get("title", ""),
                topic.get("text", ""),
                topic.get("simple", ""),
                topic.get("example", ""),
            ]))

            tid: TopicId = (section_key, topic_key)
            meta[tid] = TopicMeta(
                section_key=section_key,
                topic_key=topic_key,
                section_title=section_title,
                topic_title=title,
                blob=blob,
            )

            for tk in tokens(blob):
                inverted.setdefault(tk, set()).add(tid)

    return inverted, meta

INVERTED_INDEX, TOPIC_META = build_index()

