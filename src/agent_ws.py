import asyncio
import json
import aiohttp
import websockets
from typing import Optional, List, Dict, Any

class PythLazerAgentClient:
    def __init__(self, listen_address: str, bearer_token: Optional[str] = None):
        self.listen_address = listen_address
        self.bearer = bearer_token
        self._id = 0
        self.ws = None

    async def _await_agent_health(self, headers: Dict[str, str]):
        base = f"http://{self.listen_address}"
        timeout = aiohttp.ClientTimeout(total=5)
        deadline = asyncio.get_event_loop().time() + 10
        last_error: Optional[str] = None
        
        async with aiohttp.ClientSession(timeout=timeout) as http:
            while True:
                try:
                    async with http.get(f"{base}/ready", headers=headers) as resp:
                        if resp.status == 200:
                            break
                        last_error = f"HTTP {resp.status}"
                except Exception as e:
                    last_error = str(e)

                if asyncio.get_event_loop().time() >= deadline:
                    raise TimeoutError(f"Agent readiness check failed: {last_error}")
                await asyncio.sleep(0.5)

            async with http.get(f"{base}/live", headers=headers) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Agent liveness check failed: HTTP {resp.status}")

    async def connect(self):
        headers = {}
        if self.bearer:
            headers["Authorization"] = f"Bearer {self.bearer}"
        
        await self._await_agent_health(headers)
        
        ws_url = f"ws://{self.listen_address}/v1/jrpc"
        self.ws = await websockets.connect(
            ws_url, 
            extra_headers=headers, 
            ping_interval=20, 
            ping_timeout=20
        )

    async def close(self):
        if self.ws:
            await self.ws.close()

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    async def _send_jsonrpc(self, method: str, params: Dict[str, Any]) -> Any:
        if not self.ws:
            raise RuntimeError("WebSocket is not connected")

        request = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params,
        }

        await self.ws.send(json.dumps(request))

        try:
            raw = await asyncio.wait_for(self.ws.recv(), timeout=10)
        except asyncio.TimeoutError:
            raise TimeoutError("JSON-RPC response timeout")

        try:
            response = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON-RPC response: {e}")

        if isinstance(response, dict) and "error" in response:
            err = response["error"]
            code = err.get("code")
            message = err.get("message")
            data = err.get("data")
            raise RuntimeError(f"JSON-RPC error {code}: {message} | data={data}")

        return response.get("result") if isinstance(response, dict) else response

    async def publish_updates(self, updates: List[Dict]) -> Any:
        """
        Submit price updates using the Pyth Lazer Agent JSON-RPC API.
        """
        results = []
        for payload in updates:
            result = await self._send_jsonrpc("push_update", payload)
            results.append(result)
        return results