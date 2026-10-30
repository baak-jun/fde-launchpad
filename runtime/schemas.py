from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Principal(StrictModel):
    tenant: str
    actor: str
    roles: frozenset[str] = frozenset({'submit', 'review', 'execute'})


class Proposal(StrictModel):
    category: str = Field(max_length=64)
    title: str = Field(min_length=1, max_length=120)
    summary: str = Field(min_length=1, max_length=2000)
    policy_ids: list[str] = Field(default_factory=list, max_length=8)
    blocked_reason: str | None = Field(default=None, max_length=500)


class Submit(StrictModel):
    domain: str = Field(pattern=r'^[a-z][a-z0-9_-]{0,40}$')
    text: str = Field(min_length=1, max_length=8000)
    idempotency_key: str = Field(min_length=8, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')


class Revision(StrictModel):
    text: str = Field(min_length=1, max_length=8000)
    expected_version: int = Field(ge=1)


class Decision(StrictModel):
    expected_version: int = Field(ge=1)
    decision: Literal['approve', 'reject']


class Execution(StrictModel):
    expected_version: int = Field(ge=1)
    proposal_hash: str = Field(pattern=r'^[a-f0-9]{64}$')
