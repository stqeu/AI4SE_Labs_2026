"""LangGraph state shared by all nodes.

Each node returns a partial dict; LangGraph merges it into the state.
``candidates``, ``batch_results`` and ``review_history`` use an additive
reducer so that parallel branches (one Extractor per document, one
Consolidator per topic, via ``Send``) and repeated review rounds append
instead of overwrite.
"""
from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from schemas import (BatchResult, BlacklistEntry, CandidateRequirement,
                     ConsolidationResult, GlossaryTerm, Issue, Requirement,
                     ReviewReport, SourceDocument, Topic)


class GraphState(TypedDict, total=False):
    # --- run configuration ---------------------------------------------
    input_dir: str
    output_dir: str
    max_rounds: int
    cache_dir: str | None              # extraction cache (None = disabled)
    cache_readonly: bool               # mock runs read the cache, never write

    # --- loader --------------------------------------------------------
    documents: list[SourceDocument]

    # --- extractor (fan-out, appended) ---------------------------------
    candidates: Annotated[list[CandidateRequirement], operator.add]

    # --- pre-dedup -----------------------------------------------------
    clusters: list[list[str]]          # groups of similar candidate IDs

    # --- planner -------------------------------------------------------
    topics: list[Topic]                # repaired topic batches
    plan_glossary: list[GlossaryTerm]  # shared vocabulary for all batches

    # --- consolidator (fan-out, appended) / assembler ------------------
    batch_results: Annotated[list[BatchResult], operator.add]
    consolidation: ConsolidationResult   # assembled / revised, validated next

    # --- validator -----------------------------------------------------
    glossary: list[GlossaryTerm]
    requirements: list[Requirement]
    blacklist: list[BlacklistEntry]
    validation_issues: list[Issue]

    # --- reviewer / reviser loop ---------------------------------------
    review: ReviewReport | None
    review_history: Annotated[list[ReviewReport], operator.add]
    round: int
    halt: str | None                   # set if a revision round failed

    # --- renderer ------------------------------------------------------
    output_files: list[str]


class ExtractorInput(TypedDict):
    """Payload sent to each parallel Extractor branch (via ``Send``)."""
    document: SourceDocument
    cache_dir: str | None
    cache_readonly: bool


class BatchInput(TypedDict):
    """Payload sent to each parallel Consolidator branch (via ``Send``).
    Keys are prefixed so they never collide with GraphState channels."""
    batch_topic: Topic
    batch_candidates: list[CandidateRequirement]
    batch_documents: list[SourceDocument]
    batch_glossary: list[GlossaryTerm]
    batch_all_topics: list[str]        # "name: scope" of every topic
