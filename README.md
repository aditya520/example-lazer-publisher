# Example Publisher (CoinGecko → Lazer Agent JSON-RPC)

This is a minimal example that:
- polls CoinGecko prices,
- converts to fixed-point `(price, expo)`,
- connects to the Lazer Agent WS at `/v1/jrpc` and sends `push_update` JSON-RPC calls.

## Quickstart

```bash
# 1) Install
pipx install poetry  # or pip install --user poetry
poetry install

# 2) Configure
# Edit config/publisher.toml
# - set agent.listen_address to the HTTP base of the Lazer Agent
# - set bearer_token if required by relayer

# 3) Run
poetry run publisher