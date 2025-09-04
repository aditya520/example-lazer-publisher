import asyncio
import aiohttp
from typing import List

from .config import load_config
from .coingecko import CoinGeckoClient
from .transforms import build_push_update
from .agent_ws import PythLazerAgentClient
from .util import lifespan

async def publisher_loop(cfg_path: str):
    cfg = load_config(cfg_path)

    async with aiohttp.ClientSession() as http:
        cg = CoinGeckoClient(http, cfg.publisher.coingecko_api_key)
        print("coin gecko client initialized")

        agent = PythLazerAgentClient(cfg.agent.listen_address, cfg.agent.bearer_token)
        print("Pyth Lazer Agent client initialized")
        
        await agent.connect()
        print("agent connected")

        async with lifespan(agent.close):
            ids = [m.coingecko_id for m in cfg.publisher.markets.values()]
            print(f"ids to fetch: {ids}")
            feed_id_by_cg_id = {v.coingecko_id: v.feed_id for v in cfg.publisher.markets.values()}

            interval = cfg.publisher.interval_ms / 1000.0
            while True:
                try:
                    spot = await cg.prices_usd(ids)
                    print(f"spot prices: {spot}")
                    updates: List[dict] = []
                    for cg_id, price in spot.items():
                        feed_id = feed_id_by_cg_id[cg_id]
                        updates.append(
                            build_push_update(feed_id, price, cfg.pricing.expo)
                        )

                    if updates:
                        await agent.publish_updates(updates)
                        print(f"updates published for {ids}: {updates}")

                except Exception as e:
                    print(f"publish error for {ids}: {e}")

                await asyncio.sleep(interval)

def run():
    asyncio.run(publisher_loop("config/publisher.toml"))

if __name__ == "__main__":
    run()