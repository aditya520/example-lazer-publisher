def price_to_int(price: float, expo: int) -> int:
    """
    Convert a float to fixed-point int given expo, e.g. expo=-8 → multiply by 1e8.
    """
    scale = 10 ** (-expo)
    return int(round(price * scale))

def conf_from_bps(price: float, conf_bps: int, expo: int) -> int:
    conf = price * (conf_bps / 10_000)
    return price_to_int(conf, expo)

def build_push_update(feed_id: int, price: float, expo: int) -> dict:
    now_us = __import__("time").time_ns() // 1_000  # microseconds per example
    price_int = price_to_int(price, expo)
    return {
        "feed_id": feed_id,
        "source_timestamp": now_us,
        "update": {
            "type": "price",
            "price": price_int,
        },
    }