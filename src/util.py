import asyncio
import contextlib

@contextlib.asynccontextmanager
async def lifespan(*cleanups):
    try:
        yield
    finally:
        await asyncio.gather(*[c() for c in cleanups if c])