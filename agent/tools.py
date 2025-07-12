from langchain.tools import StructuredTool
from typing import Dict, Any
import requests

def _ask_simulator(msg: str, endpoint: str) -> Dict[str, Any]:
    resp = requests.post(endpoint, json={"message": msg}, timeout=10)
    resp.raise_for_status()
    return resp.json()

AskSimulator = StructuredTool.from_function(
    func=_ask_simulator,
    name="ask_simulator",
    description="Query the simulator server with user text.",
    args_schema=None,  # simple signature, dataclass optional
)