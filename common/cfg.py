from pathlib import Path
import yaml
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable

@dataclass
class ModelCfg:
    base_api: str
    api_key: str
    model: str
    temperature: float = 0.7
    base_prompt: str | None = None

@dataclass
class AgentCfg:
    agent_type: str = "react"
    max_iter: int = 8

@dataclass
class MonitoringCfg:
    langsmith_base_api: str | None = None
    langsmith_api_key: str | None = None

@dataclass
class ServerCfg:
    port: int = 8000
    # Optional base endpoint prefix. Unused by the current server
    # implementation but tolerated in configuration files for
    # forward compatibility.
    endpoint: str | None = None

@dataclass
class ServerFullCfg:
    model_config: ModelCfg
    server: ServerCfg = field(default_factory=ServerCfg)
    monitoring: MonitoringCfg = field(default_factory=MonitoringCfg)


@dataclass
class AgentFullCfg:
    model_config: ModelCfg
    agent_config: AgentCfg = field(default_factory=AgentCfg)
    monitoring: MonitoringCfg = field(default_factory=MonitoringCfg)

def _validate_model_cfg(raw_model: Dict[str, Any], required: Iterable[str]) -> None:
    missing = [key for key in required if not raw_model.get(key)]
    if missing:
        raise ValueError(
            "Model configuration missing required fields: " + ", ".join(missing)
        )

def _load_raw(path: str | Path) -> Dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)


def load_server_cfg(path: str | Path) -> ServerFullCfg:
    raw = _load_raw(path)
    raw_model = raw.get("model_config", {})
    _validate_model_cfg(raw_model, ("base_api", "api_key", "model"))
    model_cfg = ModelCfg(**raw_model)
    server_cfg = ServerCfg(**raw.get("server", {}))
    monitoring_cfg = MonitoringCfg(**raw.get("monitoring", {}))
    return ServerFullCfg(
        model_config=model_cfg,
        server=server_cfg,
        monitoring=monitoring_cfg,
    )


def load_agent_cfg(path: str | Path) -> AgentFullCfg:
    raw = _load_raw(path)
    raw_model = raw.get("model_config", {})
    _validate_model_cfg(raw_model, ("base_api", "api_key", "model"))
    model_cfg = ModelCfg(**raw_model)
    agent_cfg = AgentCfg(**raw.get("agent_config", {}))
    monitoring_cfg = MonitoringCfg(**raw.get("monitoring", {}))
    return AgentFullCfg(
        model_config=model_cfg,
        agent_config=agent_cfg,
        monitoring=monitoring_cfg,
    )


def load_cfg(path: str | Path) -> AgentFullCfg | ServerFullCfg:
    raw = _load_raw(path)
    if "server" in raw and "agent_config" not in raw:
        return load_server_cfg(path)
    return load_agent_cfg(path)

