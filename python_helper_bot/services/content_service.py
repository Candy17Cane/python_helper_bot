from __future__ import annotations
from services.content_index import INVERTED_INDEX, TOPIC_META

from dataclasses import dataclass
from typing import Optional

from data.content import CONTENT
from utils.text import norm, tokens, highlight

@dataclass(frozen=True)
class TopicRef:
    section_key: str
    topic_key: str
    section_title: str
    topic_title: str
    score: int
    snippet_html: str

def get_section(section_key: str) -> Optional[dict]:
    return CONTENT.get(section_key)

def get_topic(section_key: str, topic_key: str) -> Optional[dict]:
    section = CONTENT.get(section_key)
    if not section:
        return None
    return section.get("topics", {}).get(topic_key)

def topic_blob(topic: dict) -> str:
    parts = [
        topic.get("title", ""),
        topic.get("text", ""),
        topic.get("simple", ""),
        topic.get("example", ""),
    ]
    return norm("\n".join(parts))

def score_topic(q_tokens: list[str], title: str, blob: str) -> int:
    score = 0 
    title_n = norm(title)

    for t in q_tokens:
        if t in title_n:
            score += 5 
        if t in blob:
            score += 2

    phrase = " ".join(q_tokens)
    if phrase and phrase in blob:
        score += 3

    return score

def search(query: str, limit: int = 10) -> list[TopicRef]:
    q_tokens = tokens(query)
    if not q_tokens:
        return []
    
    candidates = set()
    for t in q_tokens:
        candidates |= INVERTED_INDEX.get(t, set())
    
    results: list[TopicRef] = []
    for tid in candidates:
        meta = TOPIC_META[tid]
        sc = score_topic(q_tokens, meta.topic_title, meta.blob)
        if sc <= 0:
            continue

        snippet = highlight(meta.blob, q_tokens, limit=140)

        results.append(
            TopicRef(
                section_key=meta.section_key,
                topic_key=meta.topic_key,
                section_title=meta.section_title,
                topic_title=meta.topic_title,
                score=sc,
                snippet_html=snippet,
            )
        )

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]

