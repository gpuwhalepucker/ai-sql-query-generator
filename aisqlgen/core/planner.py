"""Lightweight pre-planner. Classifies intent so we can bias the prompt."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

Intent = Literal["select", "aggregate", "join", "ddl", "dml", "unknown"]

_AGG = re.compile(r"\b(count|sum|avg|min|max|group by|per|total|average)\b", re.I)
_JOIN = re.compile(r"\b(join|related|linked|with their|alongside|between)\b", re.I)
_DDL = re.compile(r"\b(create table|alter table|add column|index on)\b", re.I)
_DML = re.compile(r"\b(insert|update|delete|remove|set .* to)\b", re.I)


@dataclass(frozen=True, slots=True)
class Plan:
    intent: Intent
    hint: str


def classify(prompt: str) -> Plan:
    text = prompt.strip()
    if _DDL.search(text):
        return Plan("ddl", "Emit DDL only. No data manipulation.")
    if _DML.search(text):
        return Plan("dml", "Emit a single DML statement. Do not include a SELECT preview.")
    if _JOIN.search(text):
        return Plan("join", "Prefer explicit JOIN ... ON syntax over comma joins.")
    if _AGG.search(text):
        return Plan("aggregate", "Use GROUP BY with explicit column list. Alias aggregates.")
    if text:
        return Plan("select", "Return a single SELECT. Alias every projected column.")
    return Plan("unknown", "Ask for clarification in a SQL comment.")