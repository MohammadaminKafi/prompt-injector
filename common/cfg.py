from pathlib import Path
import yaml
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class ModelCfg:
    base_api: str
    api_key: str
    model: str
    temperature: float = 0.7

@dataclass
class AgentCfg:
    agent_type: str = "react"
    max_iter: int = 8

@dataclass
class MonitoringCfg:
    langsmith_base_api: str | None = None
    langsmith_api_key: str | None = None

@dataclass
class FullCfg:
    model_config: ModelCfg
    agent_config: AgentCfg = field(default_factory=AgentCfg)
    monitoring: MonitoringCfg = field(default_factory=MonitoringCfg)

def load_cfg(path: str | Path) -> FullCfg:
    with open(path) as f:
        raw: Dict[str, Any] = yaml.safe_load(f)
    return FullCfg(**raw)  # type: ignore[arg-type]
