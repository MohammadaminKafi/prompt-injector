import argparse, json, sys
from pathlib import Path
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from .tools import AskSimulator
from common.cfg import load_agent_cfg

def build_agent(cfg_path: Path):
    cfg = load_agent_cfg(cfg_path)
    model = init_chat_model(
        model=cfg.model_config.model,
        model_provider="openai",
        openai_api_base=cfg.model_config.base_api,
        openai_api_key=cfg.model_config.api_key,
        temperature=cfg.model_config.temperature,
    )
    if cfg.monitoring.langsmith_api_key:
        import os
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_ENDPOINT"] = cfg.monitoring.langsmith_base_api
        os.environ["LANGSMITH_API_KEY"] = cfg.monitoring.langsmith_api_key
    return create_react_agent(model, tools=[AskSimulator])

def run_agent():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="Path to YAML agent config")
    p.add_argument("--input", required=True, help="Prompt payload file")
    p.add_argument("--output", default="result.json", help="Save benchmark results")
    args = p.parse_args()

    agent = build_agent(Path(args.config))
    prompts = Path(args.input).read_text().splitlines()

    results = []
    for prompt in prompts:
        out = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        results.append({"prompt": prompt, "response": out})
        print(json.dumps({"prompt": prompt, "response": out}, ensure_ascii=False))

    Path(args.output).write_text(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_agent()
