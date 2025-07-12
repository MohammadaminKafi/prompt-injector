from flask import Flask, request, jsonify
from pathlib import Path
import argparse
from common.cfg import load_cfg
from .levels import LEVEL_MAP

def create_app(cfg_path: Path) -> Flask:
    cfg = load_cfg(cfg_path)

    level = cfg.agent_config.agent_type  # reuse field, or add server.level in YAML
    handler = LEVEL_MAP.get(level, LEVEL_MAP["level1"])

    app = Flask(__name__)

    @app.route("/ask", methods=["POST"])
    def ask():
        data = request.get_json(force=True)
        message = data.get("message", "")
        return jsonify({"answer": handler(message)})

    return app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Server YAML config")
    args = parser.parse_args()
    cfg = load_cfg(args.config)
    app = create_app(args.config)
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    main()
