import json
from pathlib import Path
from pydantic import Field, model_validator
from .schemas import StrictModel

ROOT = Path(__file__).resolve().parents[1]


class Category(StrictModel):
    id: str = Field(pattern=r'^[a-z][a-z0-9_-]{0,40}$')
    label: str = Field(min_length=1, max_length=100)
    keywords: list[str] = Field(max_length=50)
    draft: str = Field(min_length=1, max_length=2000)
    policy_ids: list[str] = Field(max_length=8)


class Policy(StrictModel):
    id: str = Field(pattern=r'^[a-z][a-z0-9_-]{0,80}$')
    text: str = Field(min_length=1, max_length=2000)


class DomainPack(StrictModel):
    id: str = Field(pattern=r'^[a-z][a-z0-9_-]{0,40}$')
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=300)
    sample: str = Field(min_length=1, max_length=8000)
    categories: list[Category] = Field(min_length=1, max_length=30)
    policies: list[Policy] = Field(min_length=1, max_length=50)

    @model_validator(mode='after')
    def references(self):
        ids = [c.id for c in self.categories]
        policies = [p.id for p in self.policies]
        if len(set(ids)) != len(ids) or 'unknown' not in ids:
            raise ValueError('Unique categories including unknown are required')
        if len(set(policies)) != len(policies):
            raise ValueError('Duplicate policy ID')
        for category in self.categories:
            if not set(category.policy_ids) <= set(policies):
                raise ValueError('Unknown policy reference')
            if any(not k.strip() for k in category.keywords):
                raise ValueError('Empty keyword')
        return self


def load_domains():
    result = {}
    for path in sorted((ROOT / 'domain_packs').glob('*.json')):
        pack = DomainPack.model_validate_json(path.read_text(encoding='utf-8')).model_dump()
        if pack['id'] in result:
            raise ValueError('Duplicate domain')
        categories = {c['id'] for c in pack['categories']}
        if 'unknown' not in categories:
            raise ValueError('A domain must include unknown')
        result[pack['id']] = pack
    return result
