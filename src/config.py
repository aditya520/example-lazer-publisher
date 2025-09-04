from pydantic import BaseModel
import toml
from typing import Dict

class Market(BaseModel):
    coingecko_id: str
    product_id: str
    feed_id: int

class PublisherCfg(BaseModel):
    provider_engine: str
    interval_ms: int
    coingecko_api_key: str | None = None
    markets: Dict[str, Market]

class AgentCfg(BaseModel):
    listen_address: str
    bearer_token: str | None = None

class PricingCfg(BaseModel):
    expo: int

class AppCfg(BaseModel):
    publisher: PublisherCfg
    agent: AgentCfg
    pricing: PricingCfg

def load_config(path: str) -> AppCfg:
    data = toml.load(path)
    return AppCfg(**data)