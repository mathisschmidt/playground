"""CSV profiling: infer column types and semantic roles so the frontend
can choose how to render a dataset it has never seen before."""

from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

MAX_CATEGORICAL_CARDINALITY = 40
CATEGORICAL_RATIO = 0.5  # distinct/filled must be below this to be a facet
LONG_TEXT_AVG_LEN = 35
LONG_TEXT_MAX_LEN = 100

URL_RE = re.compile(
    r"^(https?://)?([a-z0-9-]+\.)+[a-z]{2,}(/[^\s]*)?$", re.IGNORECASE
)
YEAR_RE = re.compile(r"^(18|19|20)\d{2}$")
NUMBER_RE = re.compile(r"^-?\d+([.,]\d+)?$")


@dataclass
class ColumnProfile:
    name: str
    type: str = "text"  # text | long_text | categorical | number | year | url
    role: str = "detail"  # title | subtitle | description | link | facet | metric | detail
    fill_rate: float = 0.0
    distinct: int = 0
    top_values: list[dict] = field(default_factory=list)
    min: float | None = None
    max: float | None = None

    def to_dict(self) -> dict:
        d = {
            "name": self.name,
            "type": self.type,
            "role": self.role,
            "fillRate": round(self.fill_rate, 3),
            "distinct": self.distinct,
        }
        if self.top_values:
            d["topValues"] = self.top_values
        if self.min is not None:
            d["min"] = self.min
            d["max"] = self.max
        return d


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    if not rows:
        return [], []
    header = [h.strip() for h in rows[0]]
    width = len(header)
    body = []
    for row in rows[1:]:
        # normalise width and drop fully empty rows
        row = [c.strip() for c in row[:width]] + [""] * (width - len(row))
        if any(row):
            body.append(row)
    return header, body


def _classify_type(values: list[str]) -> str:
    n = len(values)
    if n == 0:
        return "text"
    if sum(bool(URL_RE.match(v)) for v in values) / n > 0.8:
        return "url"
    if sum(bool(YEAR_RE.match(v)) for v in values) / n > 0.9:
        return "year"
    if sum(bool(NUMBER_RE.match(v.replace(" ", ""))) for v in values) / n > 0.9:
        return "number"
    if (
        sum(len(v) for v in values) / n >= LONG_TEXT_AVG_LEN
        or max(len(v) for v in values) >= LONG_TEXT_MAX_LEN
    ):
        return "long_text"
    return "text"


def profile_columns(header: list[str], rows: list[list[str]]) -> list[ColumnProfile]:
    n_rows = max(len(rows), 1)
    profiles: list[ColumnProfile] = []

    for i, name in enumerate(header):
        values = [row[i] for row in rows if row[i]]
        p = ColumnProfile(name=name)
        p.fill_rate = len(values) / n_rows
        p.distinct = len(set(values))
        p.type = _classify_type(values)

        if p.type in ("number", "year") and values:
            nums = []
            for v in values:
                try:
                    nums.append(float(v.replace(",", ".").replace(" ", "")))
                except ValueError:
                    pass
            if nums:
                p.min, p.max = min(nums), max(nums)

        # A column with few distinct values is a facet even if the labels are
        # long (e.g. a "Category" column). This takes priority over long_text.
        if (
            p.type in ("text", "long_text")
            and values
            and p.distinct <= MAX_CATEGORICAL_CARDINALITY
            and p.distinct / len(values) < CATEGORICAL_RATIO
        ):
            p.type = "categorical"
            counts = Counter(values)
            p.top_values = [
                {"value": v, "count": c} for v, c in counts.most_common()
            ]
        profiles.append(p)

    _assign_roles(profiles, n_rows)
    return profiles


def _assign_roles(profiles: list[ColumnProfile], n_rows: int) -> None:
    # title: first text column that is mostly unique and well filled
    for p in profiles:
        if p.type == "text" and p.fill_rate > 0.9 and p.distinct >= 0.9 * n_rows * p.fill_rate:
            p.role = "title"
            break

    title_found = any(p.role == "title" for p in profiles)
    for p in profiles:
        if p.role == "title":
            continue
        if p.type == "url":
            p.role = "link"
        elif p.type == "categorical":
            p.role = "facet"
        elif p.type == "long_text":
            p.role = "description"
        elif p.type in ("number", "year"):
            p.role = "metric"
        elif p.type == "text" and not title_found:
            p.role = "title"
            title_found = True

    # subtitle: first non-facet text detail column after the title
    seen_title = False
    for p in profiles:
        if p.role == "title":
            seen_title = True
            continue
        if seen_title and p.role == "detail" and p.type == "text" and p.fill_rate > 0.5:
            p.role = "subtitle"
            break


def profile_file(path: Path) -> dict:
    header, rows = read_csv(path)
    profiles = profile_columns(header, rows)
    return {
        "columns": [p.to_dict() for p in profiles],
        "rows": rows,
        "rowCount": len(rows),
    }
