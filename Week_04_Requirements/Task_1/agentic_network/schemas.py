"""Data structures that flow through the agentic network.

Two families of models:
* LLM-facing models (``Extracted*``, ``Consolidated*``, ``ReviewReport``) are
  what the LLM nodes must return via structured output. They deliberately
  contain no IDs or source references the model could invent - those are
  filled in deterministically.
* Internal models (``SourceDocument``, ``CandidateRequirement``,
  ``Requirement``, ``BlacklistEntry``, ``Issue``) carry the IDs and tracing
  information (OS2, OS4) assigned by deterministic code.
"""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------
# Enumerations
# --------------------------------------------------------------------------
class DocType(str, Enum):
    EMAIL = "email"
    INTERVIEW = "interview"
    MEETING_MINUTES = "meeting_minutes"
    SURVEY = "survey"
    SPECIFICATION = "specification"
    REFERENCE = "reference"
    OTHER = "other"


class ReqType(str, Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"


class Priority(str, Enum):
    """MoSCoW priority scale (OS6)."""
    MUST = "Must"
    SHOULD = "Should"
    COULD = "Could"
    WONT = "Won't"


PRIORITY_SCALE: dict[Priority, str] = {
    Priority.MUST: (
        "Essential for the system to be acceptable. Explicitly demanded by "
        "stakeholders, required by a standard or legal obligation, or needed "
        "by many libraries for core daily work. The release fails without it."
    ),
    Priority.SHOULD: (
        "Important and clearly wanted by stakeholders, but a temporary "
        "workaround exists. Planned for the first release if at all possible."
    ),
    Priority.COULD: (
        "Desirable improvement with limited impact, requested by few "
        "stakeholders or described as 'nice to have'. Included if time allows."
    ),
    Priority.WONT: (
        "Acknowledged and valid, but explicitly deferred by stakeholders to a "
        "later phase. Kept in the document so the need is not lost."
    ),
}

PRIORITY_ORDER = {p: i for i, p in enumerate(Priority)}

ID_PREFIX: dict[ReqType, str] = {
    ReqType.FUNCTIONAL: "FR",
    ReqType.NON_FUNCTIONAL: "NFR",
    ReqType.CONSTRAINT: "CON",
}


class DiscardReason(str, Enum):
    CONFLICT = "conflict"          # contradicts a kept requirement
    NONSENSICAL = "nonsensical"    # vague, unrealistic, self-contradictory
    OUT_OF_SCOPE = "out_of_scope"  # not about the software (chit-chat, ...)


class IssueType(str, Enum):
    DUPLICATE = "duplicate"
    CONFLICT = "conflict"
    TERMINOLOGY = "inconsistent_terminology"
    MISSING = "missing_requirement"
    UNACCOUNTED = "unaccounted_candidate"
    WEAK_DESCRIPTION = "weak_description"
    PRIORITY = "questionable_priority"
    BAD_BLACKLIST = "unjustified_discard"
    SCHEMA = "schema_violation"
    REUSED = "candidate_reused"        # one candidate in 2+ requirements / kept+discarded
    TOO_BROAD = "too_broad"            # catch-all requirement merging many needs
    OTHER = "other"


class Severity(str, Enum):
    MAJOR = "major"    # must be fixed before approval
    MINOR = "minor"    # cosmetic; reported, does not block approval


# --------------------------------------------------------------------------
# Input documents
# --------------------------------------------------------------------------
class SourceDocument(BaseModel):
    doc_id: str = Field(description="Stable ID such as D01")
    path: str = Field(description="Path relative to the input directory")
    doc_type: DocType
    title: str
    date: str | None = None
    author: str | None = None
    text: str
    chunks: list[str] = Field(default_factory=list)


# --------------------------------------------------------------------------
# Extraction (LLM output + internal form)
# --------------------------------------------------------------------------
class ExtractedRequirement(BaseModel):
    """One requirement as returned by the Extractor LLM."""
    name: str = Field(description="Short descriptive name, 3-8 words")
    description: str = Field(
        description="What the system must do or be, in the stakeholders' "
                    "terms, 1-3 sentences")
    req_type: ReqType
    category: str = Field(
        description="Functional area, e.g. 'Reporting', 'Circulation', "
                    "'Cataloging', 'Security', 'Performance'")
    evidence: str = Field(
        description="Short verbatim quote from the document that supports it")
    stakeholder_priority_hint: str | None = Field(
        default=None,
        description="Any wording about importance/urgency found in the text "
                    "(e.g. 'critical', 'nice to have', 'phase 2'), else null")


class ExtractionResult(BaseModel):
    requirements: list[ExtractedRequirement]


class CandidateRequirement(ExtractedRequirement):
    """Extracted requirement with deterministic ID and source (OS4)."""
    cand_id: str = Field(description="e.g. D03-C07")
    source_doc_id: str
    evidence_found: bool | None = Field(
        default=None, description="Was the evidence quote found verbatim in "
                                  "the source? (checked deterministically)")


# --------------------------------------------------------------------------
# Consolidation (LLM output)
# --------------------------------------------------------------------------
class GlossaryTerm(BaseModel):
    term: str = Field(description="Preferred term used in all requirements")
    definition: str
    synonyms_replaced: list[str] = Field(
        default_factory=list,
        description="Variants found in sources that were normalised to term")


class ConsolidatedRequirement(BaseModel):
    name: str = Field(description="Short descriptive name, 3-8 words")
    description: str = Field(
        description="One paragraph (3-6 sentences) starting with "
                    "'The system shall ...' explaining behaviour, context "
                    "and acceptance intent")
    req_type: ReqType
    category: str
    priority: Priority
    priority_rationale: str = Field(description="One sentence")
    merged_from: list[str] = Field(
        description="ALL candidate IDs (e.g. D03-C07) merged into this one")


class ConsolidatedDiscard(BaseModel):
    name: str
    description: str
    reason: DiscardReason
    explanation: str = Field(description="Why it was discarded, 1-3 sentences")
    conflicts_with: str | None = Field(
        default=None,
        description="Name of the kept requirement it conflicts with, if any")
    candidate_ids: list[str]


class ConsolidationResult(BaseModel):
    glossary: list[GlossaryTerm]
    requirements: list[ConsolidatedRequirement]
    blacklist: list[ConsolidatedDiscard]


class PatchResult(BaseModel):
    """Reviser output: replaces exactly the requirements/discards it was given."""
    requirements: list[ConsolidatedRequirement]
    blacklist: list[ConsolidatedDiscard]


# --------------------------------------------------------------------------
# Planning (topic batching)
# --------------------------------------------------------------------------
class PlannedTopic(BaseModel):
    name: str = Field(description="Topic name, 2-5 words, Title Case")
    scope: str = Field(description="One sentence: what belongs in this topic")
    candidate_ids: list[str] = Field(description="Candidate IDs in this topic")


class PlanResult(BaseModel):
    """Planner output."""
    glossary: list[GlossaryTerm]
    topics: list[PlannedTopic]


class Topic(PlannedTopic):
    """Repaired topic batch (internal)."""
    topic_id: str = Field(description="e.g. T03 or T03.2 for a split part")


class BatchResult(BaseModel):
    topic_id: str
    topic_name: str
    result: ConsolidationResult


# --------------------------------------------------------------------------
# Final internal forms (after deterministic validation)
# --------------------------------------------------------------------------
class Requirement(ConsolidatedRequirement):
    req_id: str = Field(description="e.g. FR-001 (OS2)")
    sources: list[str] = Field(description="Document IDs, derived from "
                                           "merged_from (OS4)")


class BlacklistEntry(ConsolidatedDiscard):
    entry_id: str = Field(description="e.g. BL-001")
    sources: list[str]


# --------------------------------------------------------------------------
# Feedback loop
# --------------------------------------------------------------------------
class Issue(BaseModel):
    issue_type: IssueType
    affected: list[str] = Field(
        default_factory=list,
        description="Requirement IDs, candidate IDs or document IDs involved")
    description: str
    suggested_fix: str | None = None
    severity: Severity = Field(
        default=Severity.MAJOR,
        description="major = must be fixed (duplicates, conflicts, lost needs, "
                    "wrong discards); minor = wording/cosmetic")
    origin: str = Field(default="reviewer",
                        description="'validator' or 'reviewer'")


class ReviewReport(BaseModel):
    """Output of the Reviewer LLM."""
    approved: bool = Field(
        description="True only if no significant issues remain")
    issues: list[Issue]
    summary: str = Field(description="2-3 sentence overall assessment")
