"""Run-time settings, read from .env / environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent

try:
    from dotenv import load_dotenv
    load_dotenv(HERE / ".env")
except ImportError:  # dotenv is optional for offline tests
    pass


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, default))


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, default))


@dataclass(frozen=True)
class Settings:
    model_extractor: str = os.getenv("MODEL_EXTRACTOR", "gpt-5-mini")
    model_consolidator: str = os.getenv("MODEL_CONSOLIDATOR", "gpt-5.6-luna")
    model_reviewer: str = os.getenv("MODEL_REVIEWER", "gpt-6-luna")
    # planner sorts all candidates into topics; needs a strong model
    model_planner: str = os.getenv("MODEL_PLANNER", "gpt-5.6-luna")

    # loader
    file_suffixes: tuple[str, ...] = (".txt", ".md", ".eml")
    chunk_chars: int = _int("CHUNK_CHARS", 12000)

    # pre-dedup: TF-IDF cosine threshold for grouping candidates (0-1)
    dedup_threshold: float = _float("DEDUP_THRESHOLD", 0.45)
    # validator: cosine above which two final requirements look duplicate
    duplicate_threshold: float = _float("DUPLICATE_THRESHOLD", 0.6)

    # planner repair: candidates at least this similar stay in one topic
    colocate_threshold: float = _float("COLOCATE_THRESHOLD", 0.55)
    # max candidates per consolidator call (larger topics are split)
    max_batch_size: int = _int("MAX_BATCH_SIZE", 60)
    # topics smaller than this are merged into the most similar topic
    min_batch_size: int = _int("MIN_BATCH_SIZE", 8)

    # validator: descriptions shorter than this are flagged (OS5)
    min_description_words: int = _int("MIN_DESCRIPTION_WORDS", 30)
    # validator: requirements merging more candidates are flagged too broad
    too_broad_candidates: int = _int("TOO_BROAD_CANDIDATES", 15)

    # reviser: max candidates of context per revision work package
    max_package_candidates: int = _int("MAX_PACKAGE_CANDIDATES", 60)
    # parallel LLM calls inside the reviser node
    revise_concurrency: int = _int("REVISE_CONCURRENCY", 6)

    # feedback loop
    max_rounds: int = _int("MAX_ROUNDS", 3)

    # output-token ceilings per LLM call (include reasoning tokens)
    # 16000 was too low for dense spec sections (run 2: SRS part 2/3 truncated)
    max_tokens_extractor: int = _int("MAX_TOKENS_EXTRACTOR", 32000)
    max_tokens_consolidator: int = _int("MAX_TOKENS_CONSOLIDATOR", 100000)
    max_tokens_reviewer: int = _int("MAX_TOKENS_REVIEWER", 32000)
    max_tokens_planner: int = _int("MAX_TOKENS_PLANNER", 40000)


SETTINGS = Settings()
