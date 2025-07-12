#!/usr/bin/env bash
python -m agent.main \
  --config agent/config/agent_config.yaml \
  --input agent/prompts/sample_payloads.txt \
  --output benchmark.json