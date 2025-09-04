# Pyth Lazer Publisher Example

A comprehensive example publisher example that integrates with the Pyth Lazer Agent that publishes price data the Pyth Lazer. This publisher fetches cryptocurrency prices from CoinGecko and pushes them to the Lazer Agent via WebSocket connections.

## Overview

This publisher:

- Polls CoinGecko for cryptocurrency prices at configurable intervals
- Converts prices to fixed-point format `(price, expo)` compatible with Pyth
- Connects to the Lazer Agent WebSocket at `/v1/jrpc` endpoint
- Sends `push_update` JSON-RPC calls to publish price data

## Prerequisites

- Python 3.10 or higher
- Poetry (Python dependency management)
- CoinGecko API key (for fetching price data)
- Access to a running Pyth Lazer Agent

## Installation

### 1. Install Poetry

If you don't have Poetry installed:

```bash
# Via pipx (recommended)
pipx install poetry

# Or via pip
pip install --user poetry
```

### 2. Install Dependencies

```bash
poetry install
```

This will create a virtual environment and install all required dependencies including:

- `aiohttp` - For HTTP requests to CoinGecko
- `websockets` - For WebSocket connections to Lazer Agent
- `pydantic` - For data validation and configuration
- `toml` - For configuration file parsing
- `fastapi` & `uvicorn` - For potential HTTP endpoints

## Configuration

### Step 1: Set up Pyth Lazer Agent

Before running this publisher, you need to start the Pyth Lazer Agent. Follow the integration guide at:
https://pyth-network.notion.site/Pyth-Lazer-Agent-Integration-Guide-2332eecaaac9806aa999f47732e6f2a7

### Step 2: Configure Lazer Agent Settings

Copy the sample configuration file and customize it:

```bash
cp config/config_sample.toml config/config.toml
```

Edit `config/config.toml` with your Lazer Agent settings:

```toml
relayer_urls = ["wss://relayer.pyth-lazer-staging.dourolabs.app/v1/transaction"]
publish_keypair_path = "./config/secrets/agent-lazer-keypair.json"
authorization_token = ""  # Add if required by your relayer
listen_address = "0.0.0.0:8910"  # Agent's HTTP listen address
publish_interval_duration = "25ms"
```

### Step 3: Configure Publisher Settings

Copy the publisher sample configuration:

```bash
cp config/publisher_sample.toml config/publisher.toml
```

Edit `config/publisher.toml` with your specific settings:

```toml
[publisher]
# Data source configuration
provider_engine = "coin_gecko"
interval_ms = 2000  # Poll CoinGecko every 2 seconds
coingecko_api_key = "YOUR_COINGECKO_API_KEY_HERE"

# Market configuration - map symbols to CoinGecko IDs and product IDs
[publisher.markets]
BTCUSD = { coingecko_id = "bitcoin",  product_id = "BTC/USD",  feed_id = 1 }
ETHUSD = { coingecko_id = "ethereum", product_id = "ETH/USD", feed_id = 2 }
# Add more markets as needed

[agent]
listen_address = "0.0.0.0:8910"  # Must match your Lazer Agent's listen address
bearer_token = ""  # Add if your agent requires authentication. Check the Lazer Agent documentation for more details.

[pricing]
expo = -8  # Price precision (1e-8, standard for Pyth)
```

### Step 4: Get CoinGecko API Key

1. Visit [CoinGecko API](https://www.coingecko.com/en/api)
2. Sign up for a free or paid account
3. Generate an API key
4. Add the API key to your `config/publisher.toml` file in the `coingecko_api_key` field

### Step 5: Ensure Keypair File

Make sure you have the Lazer Agent keypair file at:
```
config/secrets/agent-lazer-keypair.json
```

This file should be generated when you set up your Lazer Agent following the integration guide.

## Running the Publisher

Once everything is configured, run the publisher:

```bash
poetry run publisher
```

The publisher will:
1. Load configuration from `config/publisher.toml`
2. Connect to the Lazer Agent WebSocket
3. Start polling CoinGecko for price data
4. Push price updates to the Lazer Agent

## Project Structure

```
example-publisher-lazer/
├── config/
│   ├── config_sample.toml          # Lazer Agent configuration template
│   ├── publisher_sample.toml       # Publisher configuration template
│   ├── config.toml                 # Your Lazer Agent config (create this)
│   ├── publisher.toml              # Your publisher config (create this)
│   └── secrets/
│       └── agent-lazer-keypair.json  # Lazer Agent keypair
├── src/
│   ├── main.py                     # Entry point and main application logic
│   ├── config.py                   # Configuration loading and validation
│   ├── coingecko.py               # CoinGecko API client
│   ├── agent_ws.py                # Lazer Agent WebSocket client
│   ├── transforms.py              # Price transformation utilities
│   └── util.py                    # General utilities
├── pyproject.toml                 # Poetry configuration and dependencies
└── README.md                      # This file
```

## Configuration Details

### Publisher Markets

Each market in `[publisher.markets]` defines:

- `coingecko_id`: The CoinGecko identifier for the asset
- `product_id`: Human-readable product identifier
- `feed_id`: Numeric feed identifier (must be unique)

Example:
```toml
[publisher.markets]
SOLUSD = { coingecko_id = "solana", product_id = "SOL/USD", feed_id = 3 }
ADAUSD = { coingecko_id = "cardano", product_id = "ADA/USD", feed_id = 4 }
```
Check the Lazer Agent documentation for more details on the feed_id.

### Agent Connection

The `[agent]` section configures the connection to your Lazer Agent:

- `listen_address`: Must match your Lazer Agent's HTTP listen address
- `bearer_token`: Authentication token (if required by your setup)

### Pricing Configuration

The `[pricing]` section sets the price format:
- `expo`: Price exponent (e.g., -8 means prices are multiplied by 1e8 for integer representation)

## Support

For issues related to:
- **Pyth Lazer Agent**: Refer to the [official integration guide](https://pyth-network.notion.site/Pyth-Lazer-Agent-Integration-Guide-2332eecaaac9806aa999f47732e6f2a7)
- **Pyth Lazer**: Refer to the [official documentation](https://docs.pyth.network/lazer)
- **CoinGecko API**: Check the [CoinGecko API documentation](https://www.coingecko.com/en/api/documentation)
- **This Publisher**: Review the source code in the `src/` directory for implementation details