# Prompt Injector

Two components:

1. **agent/** – LangGraph-based ReAct agent that tries to exfiltrate the *flag*.
2. **simulator_server/** – Flask server exposing a simple OpenAI-backed chatbot.
   Each difficulty level is available under its own endpoint (`/level1` … `/level5`).

## Quick start

```bash
# install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# in one terminal
bash scripts/run_server.sh

# in another
bash scripts/run_agent.sh
```

Both components read YAML configs (agent/config/…, simulator/config/…).