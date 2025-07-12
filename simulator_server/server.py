from flask import Flask, request, jsonify
import argparse
from pathlib import Path

from common.cfg import load_cfg
from openai import OpenAI

app = Flask(__name__)
handler = None


def create_handler(level: str, model_config: dict):
    """Loads the correct level strategy and injects model instance."""
    llm = OpenAI(
        base_url=model_config["base_api"],
        api_key=model_config["api_key"],
        model=model_config["model"],
        temperature=model_config["temperature"],
    )

    return llm


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    message = data.get("message", "")
    reply = handler(message)
    return jsonify({"answer": reply})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to server_config.yaml")
    args = parser.parse_args()

    cfg = load_cfg(args.config)

    global handler
    handler = create_handler(cfg.server.level, cfg.model_config.__dict__)
    app.run(host="0.0.0.0", port=cfg.server.port)


if __name__ == "__main__":
    main()
