"""Thin wrapper around the OpenAI Chat Completions API returning validated JSON.

Why not ``with_structured_output``?  The course models differ (reasoning and
non-reasoning, old and new), and strict JSON-schema mode rejects some schema
features. JSON mode + schema in the prompt + Pydantic validation + one repair
retry works the same for every model and is easy to explain.

Token usage of every call is tracked so a run can report its cost.
"""
from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass, field
from typing import TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

_client = None
_client_lock = threading.Lock()


def get_client():
    """Create the OpenAI client lazily (lets offline tests run without it)."""
    global _client
    with _client_lock:
        if _client is None:
            from openai import OpenAI
            _client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL") or None,
                             timeout=600, max_retries=3)
    return _client


# --------------------------------------------------------------------------
# usage tracking
# --------------------------------------------------------------------------
@dataclass
class Usage:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    seconds: float = 0.0


@dataclass
class UsageLog:
    by_model: dict[str, Usage] = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def add(self, model: str, prompt: int, completion: int, seconds: float) -> None:
        with self.lock:
            u = self.by_model.setdefault(model, Usage())
            u.calls += 1
            u.prompt_tokens += prompt
            u.completion_tokens += completion
            u.seconds += seconds

    def report(self) -> str:
        lines = ["model            calls   prompt_tok  completion_tok"]
        for m, u in sorted(self.by_model.items()):
            lines.append(f"{m:<16} {u.calls:>5} {u.prompt_tokens:>12,} {u.completion_tokens:>15,}")
        return "\n".join(lines)


USAGE = UsageLog()


# --------------------------------------------------------------------------
# main entry point
# --------------------------------------------------------------------------
class LLMError(RuntimeError):
    pass


def schema_hint(schema: type[BaseModel]) -> str:
    return json.dumps(schema.model_json_schema(), indent=1)


def _raw_call(model: str, messages: list[dict], max_tokens: int):
    t0 = time.time()
    resp = get_client().chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        max_completion_tokens=max_tokens,
    )
    u = resp.usage
    USAGE.add(model, getattr(u, "prompt_tokens", 0) or 0,
              getattr(u, "completion_tokens", 0) or 0, time.time() - t0)
    choice = resp.choices[0]
    return choice.message.content or "", choice.finish_reason


def call_json(model: str, system: str, user: str, schema: type[T],
              max_tokens: int = 16000, label: str = "",
              history: list[dict] | None = None) -> T:
    """Call ``model`` and return an instance of ``schema``.

    The JSON schema is appended to the system prompt. If the reply is not
    valid JSON or fails validation, the error is sent back once for repair.
    ``history`` (assistant/user turns) is appended after the first user
    message, e.g. to ask for a correction of a previous answer.
    """
    system_full = (f"{system}\n\nRespond with a single JSON object that conforms "
                   f"to this JSON Schema (no prose, no markdown):\n{schema_hint(schema)}")
    messages = [{"role": "system", "content": system_full},
                {"role": "user", "content": user}] + list(history or [])
    last_err = ""
    for attempt in (1, 2):
        content, finish = _raw_call(model, messages, max_tokens)
        if finish == "length":
            raise LLMError(f"{label}: output truncated at {max_tokens} tokens "
                           f"(model {model}); raise the max_tokens limit.")
        try:
            return schema.model_validate_json(content)
        except ValidationError as exc:
            last_err = str(exc)[:2000]
        if attempt == 1:
            print(f"  [{label}] invalid JSON from {model}, asking for a repair")
            messages += [{"role": "assistant", "content": content},
                         {"role": "user", "content":
                          "Your JSON did not validate against the schema:\n"
                          f"{last_err}\nReturn the corrected, complete JSON object."}]
    raise LLMError(f"{label}: {model} returned invalid JSON twice: {last_err[:300]}")
